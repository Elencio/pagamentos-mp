import os
from dotenv import load_dotenv

load_dotenv(override=False)

MERCADO_PAGO_TOKEN = os.getenv("MERCADO_PAGO_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
