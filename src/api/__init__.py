from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.api.routes import router
from src.database import init_db
from src.settings import Settings


def create_app() -> FastAPI:

    app = FastAPI()

    @app.on_event("startup")
    def on_startup():
        settings = Settings.get()
        init_db(settings.database_url)

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
