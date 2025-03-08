import os
from dotenv import load_dotenv

load_dotenv(override=False)

MERCADO_PAGO_TOKEN = os.getenv("MERCADO_PAGO_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
MERCADO_PAGO_URL = os.getenv("MERCADO_PAGO_URL")

SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-for-jwt") 
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))