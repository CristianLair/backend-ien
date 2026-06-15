from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId

cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["prode-ien"]
coleccion = db["paises"]

def obtener_paises():
    documento = coleccion.find_one({}, {"_id": 0})  # excluye _id

    if documento:
        return documento, None

    return None, "No hay datos"