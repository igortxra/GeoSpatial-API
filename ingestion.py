import io
import os
import time

import polars as pl
import requests

from src.db import get_session, init_db

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/app"
FILENAME_LINKS_PARQUET = "./links.parquet.gz"
FILENAME_SPEED_RECORDS_PARQUET = "./speed_records.parquet.gz"

def download_parquet_file_from_cdn(path_to_download, file_url):
    if not os.path.exists(path_to_download):
        with requests.get(file_url, stream=True) as response:
            with open(path_to_download, mode="wb") as file:
                 for chunk in response.iter_content(chunk_size=10 * 1024):
                     file.write(chunk)

def ingest_links():
    with get_session() as session:
        cur = session.connection().connection.cursor()
        cur.execute(""" CREATE TEMP TABLE links_raw ( link_id BIGINT, geo_json TEXT, road_name TEXT) """)

        columns = ["link_id", "geo_json", "road_name"]

        lazy_df = pl.scan_parquet(FILENAME_LINKS_PARQUET).select(columns)

        for batch in lazy_df.collect(engine="streaming").iter_slices(100_000):
            buffer = io.StringIO()
            batch.write_csv(buffer)
            buffer.seek(0)

            cur.copy_expert("COPY links_raw (link_id, geo_json, road_name) FROM STDIN WITH CSV HEADER",
                buffer
            )

        cur.execute("""
            INSERT INTO links (id, geom, road_name)
            SELECT
                link_id,
                ST_LineMerge(
                    ST_SetSRID(
                        ST_GeomFromGeoJSON(geo_json),
                        4326
                    )
                ),
                road_name
            FROM links_raw
            ON CONFLICT (id) DO NOTHING
        """)

        cur.execute("DROP TABLE links_raw")
        cur.close()
        session.commit()


def ingest_speed_records():

    with get_session() as session:
        cur = session.connection().connection.cursor()

        cur.execute(""" CREATE TEMP TABLE speed_records_raw ( timestamp TIMESTAMP, speed float8, link_id BIGINT, day_of_week INT, period INT) """)

        
        lazy_df = (
            pl.scan_parquet(FILENAME_SPEED_RECORDS_PARQUET).select(["date_time", "average_speed", "link_id", "day_of_week", "period"])
        )

        for batch in lazy_df.collect(engine="streaming").iter_slices(n_rows=100_000):
            buffer = io.StringIO()
            batch.write_csv(buffer)
            buffer.seek(0)

            cur.copy_expert(
                "COPY speed_records_raw (timestamp, speed, link_id, day_of_week, period) FROM STDIN WITH CSV HEADER",
                buffer
            )



        cur.execute("""
            INSERT INTO speed_records (timestamp, speed, link_id, day_of_week, period)
            SELECT *
            FROM speed_records_raw
            ON CONFLICT (timestamp, link_id) DO NOTHING
        """)

        cur.execute("DROP TABLE speed_records_raw")
        cur.close()
        session.commit()


##################################################
start_time = time.perf_counter()         # TIMER #
##################################################


download_parquet_file_from_cdn(FILENAME_LINKS_PARQUET, "https://cdn.urbansdk.com/data-engineering-interview/link_info.parquet.gz")

download_parquet_file_from_cdn(FILENAME_SPEED_RECORDS_PARQUET, "https://cdn.urbansdk.com/data-engineering-interview/duval_jan1_2024.parquet.gz")

init_db(DATABASE_URL)
ingest_links()
ingest_speed_records()


####################################################
end_time = time.perf_counter()                     #
elapsed_time = end_time - start_time       # TIMER #
print(f"Elapsed time: {elapsed_time:.4f} seconds") #
####################################################

