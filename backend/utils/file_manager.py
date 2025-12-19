import json
from pathlib import Path

def read_json(file_path: str):
    """Lee un archivo JSON y devuelve su contenido."""
    path = Path(file_path)
    if not path.exists():
        return {}  # O [] según tu estructura
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(file_path: str, data):
    """Guarda datos en un archivo JSON."""
    path = Path(file_path)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
