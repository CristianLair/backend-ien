from flask import Flask
import sys
import os

# Agrega la carpeta src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.db import db

app = Flask(__name__)

@app.route("/")
def home():
    return {"mensaje": "Servidor funcionando ✅"}

if __name__ == "__main__":
    app.run(debug=True, port=3000)