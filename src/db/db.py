from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["prode-ien"]

try:
    client.admin.command("ping")
    print(" Conexión exitosa a MongoDB Atlas")
except Exception as e:
    print(f" Error de conexión: {e}")