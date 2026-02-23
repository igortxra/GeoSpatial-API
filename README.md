# GeoSpatial API for Traffic Speed Analisys
This project involves building a geospatial microservice using FastAPI, PostgreSQL/PostGIS, and SQLAlchemy to process and analyze traffic speed data. The service ingests Parquet datasets, stores spatial road segment data, and exposes RESTful endpoints for temporal and spatial aggregations, including time-period averages, slow-link detection, and bounding box filtering. Results are visualized in a Jupyter Notebook using MapboxGL, with road segments dynamically styled by average speed. The solution demonstrates scalable microservice architecture, spatial querying, and geospatial data visualization best practices.
## Stack
Python | Fast API | Pydantic | SQLAlchemy | GeoAlchemy | Alembic | uv | docker | Docker Compose | Polars | Psycopg | Requests | Jupyter Noebook | Ruff | Pyink | MapBox | PostgresSQL | PostGIS

## Preview Images
|Traffic Speed Visualization  | Components  | OpenAPI |
|-----------------------------|-------------|---------|
| <img width="1101" height="516" alt="Pasted image 20260219112151" src="https://github.com/user-attachments/assets/a85d9d71-7714-4fa6-83a2-0d3663bff31f" />  | <img width="1533" height="418" alt="image" src="https://github.com/user-attachments/assets/fd0e0fbc-0fea-411d-aeed-f281fb02dc56" /> | <img width="1335" height="923" alt="image" src="https://github.com/user-attachments/assets/174d63ef-a8ca-48fa-b5a1-25cb7630bf64" />

## Content
**FastAPI microservice** ([See](./src))
- Implements **RESTful API** endpoints for **spatial and temporal aggregation**
- Uses **SQL Alchemy ORM** for all database interactions

**Ingestion Script** ([See](./utils/ingestion.py))
- Ingests and stores geospatial datasets (**parquet** files) using **PostgresSQL + PostGIS**

**Jupyter Notebook** ([See](./utils/original.ipynb))
- That demonstrate the API being consumed and the geospatial data being presented.

## How to run everything

### Requirements
- `docker`
- `docker-compose`
- `make`
- Mapbox Token (https://mapbox.com) 

### Running
```bash
make up 
make migration
make ingestion 
make notebook
```
--> Override the `MAPXBOX_TOKEN` variable in the notebook


## Other Informations
**Period filter reference**
|Period Name      |Period Time    |
| ----------------|---------------|
| Overnight       | 00:00 - 03:59 |
| Early Morning   | 04:00 - 06:59 |
| AM Peak         | 07:00 - 09:59 |
| Midday          | 10:00 - 12:59 |
| Early Afternoon | 13:00 - 15:59 |
| PM Peak         | 16:00 - 18:59 |
| Evening         | 19:00 - 23:59 |
