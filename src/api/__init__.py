import time

from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi

from src.api.routes import router
from src.database import create_db_and_tables


def create_app() -> FastAPI:

    app = FastAPI()

    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    app.include_router(router)

    # NOTE: Keep it after all routes
    app.openapi_schema = get_openapi(
        title="GeoSpatial API",
        version="1.0.0",
        summary="Provide spatial insights about traffic speed through an API",
        description="",
        routes=app.routes,
    )

    return app
