import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_KEY = os.getenv("KEY")
SUMMONER_NAME = os.getenv("SUMMONER_NAME")
