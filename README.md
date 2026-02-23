# GeoSpatial API for Traffic Speed Data
<img width="1101" height="516" alt="Pasted image 20260219112151" src="https://github.com/user-attachments/assets/a85d9d71-7714-4fa6-83a2-0d3663bff31f" />

## What is
**FastAPI microservice** ([See](./src))
- Implements **RESTful API** endpoints for **spatial and temporal aggregation**
- Uses **SQL Alchemy ORM** for all database interactions

**Ingestion Script** ([See](./ingestion_script/ingestion.py))
- Ingests and stores geospatial datasets (**parquet** files) using **PostgresSQL + PostGIS**

**Jupyter Notebook** ([See](./jupyter_notebook/original.ipynb))
- That demonstrate the API being consumed and the geospatial data being presented.

**Documentations** ([See](./docs/))
- About everything

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

**Stack** \
Python | FastAPI | SQLAlchemy + GeoAlchemy | PostgresSQL + PostGIS extension | Mapbox | Jupyter Notebook | Polars | Requests
