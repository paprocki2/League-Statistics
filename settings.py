import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_KEY = os.getenv("KEY")
SUMMONER_NAME = os.getenv("SUMMONER_NAME")
DB_IP = os.getenv("DB_IP")
DB_PASS = os.getenv("DB_PASS")