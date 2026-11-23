import json
from pathlib import Path

from models import Customer


def save_customers(clients: list[Customer], filepath: str | Path) -> None:
    """Sérialise une liste d'instances Customer dans un fichier JSON."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [client.to_dict() for client in clients]
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_customers(filepath: str | Path) -> list[Customer]:
    """Charge une liste d'instances Customer depuis un fichier JSON."""
    path = Path(filepath)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        raw_data = json.loads(content)
    return [Customer.from_dict(item) for item in raw_data]