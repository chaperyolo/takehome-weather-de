from dotenv import load_dotenv
import os

load_dotenv()

STATION_ID = os.getenv("STATION_ID")
API_BASE_URL = os.getenv("API_BASE_URL")
DB_PATH = os.getenv("DB_PATH")