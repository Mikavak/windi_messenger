from fastapi import FastAPI

app = FastAPI(title='WinDI Messenger')

@app.get("/")
async def root():
    return {"message": "Привет! Это API мессенджера WinDI"}