import json

def load_lottiefile(filepath: str):
    with open(filepath, "r",encoding="utf-8") as f:
        return json.load(f)



