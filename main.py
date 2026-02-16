import uvicorn

from src.api import create_app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app)
