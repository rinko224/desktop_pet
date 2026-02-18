import json
import os

def load_persona(name):
    path = os.path.join("resource/persona", name + ".json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    