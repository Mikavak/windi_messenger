from fastapi import FastAPI

from backend.api.routers import main_router

app = FastAPI(title='WinDI Messenger')

@app.get("/")
async def root():
    return {"message": "Привет! Это API мессенджера WinDI"}


app.include_router(main_router)