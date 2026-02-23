import time

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi

from src.api.routes import router


def create_app() -> FastAPI:

    app = FastAPI()

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    @app.get("/", tags=["Healthy Check"])
    def index():
        return {"message": "up and running..."}
    
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
