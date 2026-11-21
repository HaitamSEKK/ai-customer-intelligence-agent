

def display_clients(clients: list[dict]) -> None:
    """Affiche l'identifiant, le nom et le statut de chaque client."""
    if not clients:
        print("Aucun client enregistré.")
    else:
        for client in clients:
            print(f"[{client['id']}] {client['name']} - Statut : {client['status']}")


def search_client(clients: list[dict], client_id: int) -> dict | None:
    """Recherche un client par son identifiant et retourne son dictionnaire ou None."""
    for client in clients:
        if client["id"] == client_id:
            return client
    return None


def add_client(clients: list[dict], name: str, email: str, message: str) -> dict:
    """Crée un nouveau client avec le statut pending, l'ajoute à la liste et le retourne."""
    new_id = max((c["id"] for c in clients) , default=0) + 1
    new_client = {
        "id": new_id,
        "name": name,
        "email": email,
        "message": message,
        "status": "pending",
    }
    clients.append(new_client)
    return new_client


def filter_clients(clients: list[dict], status: str) -> list[dict]:
    """Retourne la liste des clients correspondant au statut demandé."""
    return [client for client in clients if client["status"] == status]


def update_status(clients: list[dict], client_id: int, new_status: str) -> bool:
    """Met à jour le statut d'un client et retourne True si trouvé, False sinon."""
    client = search_client(clients, client_id)
    if client is None:
        return False
    else:
        client["status"] = new_status
        return True

def get_customer_statistics(clients: list[dict]) -> dict[str, int]:
    """Calcule et retourne les statistiques globales des clients par statut."""
    total_clients = len(clients)
    pending_clients = len(filter_clients(clients, "pending"))
    resolved_clients = len(filter_clients(clients, "resolved"))
    return {
        "total_clients": total_clients,
        "pending_clients": pending_clients,
        "resolved_clients": resolved_clients,
    }

