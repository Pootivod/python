from dotenv import load_dotenv
import sqlite3
import os
from datetime import datetime
import json
from pathlib import Path
load_dotenv()
FILE = os.getenv("DATABASE")

def update_json(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_json():
    Path(FILE).touch(exist_ok=True)
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def reset():
    data = read_json()
    for key in data.keys():
        data[key]["downloaded"] = False
    update_json(data)
    return "Data base has been reseted. You can downloaded all tracks."