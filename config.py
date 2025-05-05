import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:9078@localhost:5432/ava_messenger')


# Другие настройки приложения
API_PREFIX = "/api"
