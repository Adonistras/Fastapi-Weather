import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from core.routers import routers
from settings import settings


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )

app.include_router(routers)