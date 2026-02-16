import io
import time

import polars as pl
import psycopg2

from src.db import init_db

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/app"
LINK_PARQUET = "./utils/link_info.parquet.gz"
SPEED_RECORDS_PARQUET = "./utils/duval_jan1_2024.parquet.gz"

init_db(DATABASE_URL)

conn = psycopg2.connect(dbname="app", user="postgres", password="postgres", host="localhost", port="5432")


def ingest_links():
    cur = conn.cursor()
    cur.execute(""" CREATE TEMP TABLE links_raw (
        link_id BIGINT,
        geo_json TEXT
    )
    """)

    columns = ["link_id", "geo_json"]

    lazy_df = pl.scan_parquet(LINK_PARQUET).select(columns)

    cur = conn.cursor()
    for batch in lazy_df.collect(engine="streaming").iter_slices(100_000):
        buffer = io.StringIO()
        batch.write_csv(buffer)
        buffer.seek(0)

        cur.copy_expert(
            "COPY links_raw (link_id, geo_json) FROM STDIN WITH CSV HEADER",
            buffer
        )
        conn.commit()

    cur.execute("""
        INSERT INTO links (id, geom)
        SELECT
            link_id,
            ST_LineMerge(
                ST_SetSRID(
                    ST_GeomFromGeoJSON(geo_json),
                    4326
                )
            )
        FROM links_raw
        ON CONFLICT (id) DO NOTHING
    """)

    cur.execute("DROP TABLE links_raw")
    cur.close()


def ingest_speed_records():
    cur = conn.cursor()
    lazy_df = (
        pl.scan_parquet(SPEED_RECORDS_PARQUET).select(["date_time", "average_speed", "link_id", "day_of_week", "period"])
    )

    for batch in lazy_df.collect(engine="streaming").iter_slices(n_rows=100_000):
        buffer = io.StringIO()
        batch.write_csv(buffer)
        buffer.seek(0)

        cur.copy_expert(
            "COPY speed_records (timestamp, speed, link_id, day_of_week, period) FROM STDIN WITH CSV HEADER",
            buffer
        )
        conn.commit()

    cur.close()


##################################################
start_time = time.perf_counter()         # TIMER #
##################################################

ingest_links()
ingest_speed_records()

conn.close()


####################################################
end_time = time.perf_counter()                     #
elapsed_time = end_time - start_time       # TIMER #
print(f"Elapsed time: {elapsed_time:.4f} seconds") #
####################################################

