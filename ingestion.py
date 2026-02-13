from pandas import read_parquet
from sqlalchemy import text
from src.db import get_engine, init_db


# TODO: Improve this script
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/app"
LINK_PARQUET = "./link_info.parquet.gz"
SPEED_RECORDS_PARQUET = "./link_info.parquet.gz"


init_db(DATABASE_URL)
engine = get_engine()

# Link Info Upload
raw_link_df = read_parquet("", columns=["link_id", "geo_json"])

raw_link_df.to_sql(
    "links_raw",
    engine,
    if_exists="append",
    index=False,
    method="multi",
)

with engine.begin() as conn:
    conn.execute(text("""
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
    """))
    conn.execute(text("DROP TABLE links_raw"))


# Speed Records Ulpload
raw_speed_records = read_parquet("./utils/duval_jan1_2024.parquet.gz", columns=["date_time", "average_speed", "link_id", "day_of_week", "period"])

raw_speed_records = raw_speed_records.rename(columns={"date_time": "timestamp", "average_speed":"speed"})

raw_speed_records.to_sql(
    "speed_records",
    engine,
    if_exists="append",
    index_label="id",
    method="multi",
)
