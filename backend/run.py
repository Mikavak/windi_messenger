import asyncio
import uvicorn
from backend.main import app  # Импорт с учетом вашей структуры проекта

async def main():
    config = uvicorn.Config(
        app,
        host="localhost",
        port=8000,
        reload=True  # Автореload в режиме разработки
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Принудительная остановка")