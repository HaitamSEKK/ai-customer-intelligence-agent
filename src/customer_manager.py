from pathlib import Path

from models import VALID_STATUSES, Customer
from storage import load_customers, save_customers


class CustomerManager:
    """Gère une collection d'instances Customer avec persistance JSON optionnelle."""

    def __init__(
        self,
        clients: list[Customer] | None = None,
        storage_path: str | Path | None = None,
    ) -> None:
        """Initialise le gestionnaire depuis une liste ou un fichier JSON."""
        self.storage_path = Path(storage_path) if storage_path else None
        if clients is not None:
            self.clients: list[Customer] = list(clients)
        elif self.storage_path is not None:
            self.clients = load_customers(self.storage_path)
        else:
            self.clients = []

    def _save(self) -> None:
        """Sauvegarde les clients sur disque si un chemin de stockage est configuré."""
        if self.storage_path is not None:
            save_customers(self.clients, self.storage_path)

    def display_clients(self) -> None:
        """Affiche l'identifiant, le nom et le statut de chaque client."""
        if not self.clients:
            print("Aucun client enregistré.")
        else:
            for client in self.clients:
                print(f"[{client.id}] {client.name} - Statut : {client.status}")

    def search_client(self, client_id: int) -> Customer | None:
        """Recherche un client par son identifiant et retourne son objet ou None."""
        for client in self.clients:
            if client.id == client_id:
                return client
        return None

    def add_client(self, name: str, email: str, message: str) -> Customer:
        """Crée un nouveau client, l'ajoute à la liste, sauvegarde et le retourne."""
        new_id = max((c.id for c in self.clients), default=0) + 1
        new_client = Customer(
            id=new_id,
            name=name,
            email=email,
            message=message,
            status="pending",
        )
        self.clients.append(new_client)
        self._save()
        return new_client

    def filter_clients(self, status: str) -> list[Customer]:
        """Retourne la liste des clients correspondant au statut demandé."""
        return [client for client in self.clients if client.status == status]

    def update_status(self, client_id: int, new_status: str) -> bool:
        """Met à jour le statut d'un client, sauvegarde et retourne True/False."""
        if new_status not in VALID_STATUSES:
            raise ValueError(f"Statut invalide : {new_status}")
        client = self.search_client(client_id)
        if client is None:
            return False
        client.status = new_status
        self._save()
        return True

    def get_customer_statistics(self) -> dict[str, int]:
        """Calcule et retourne les statistiques globales des clients par statut."""
        total_clients = len(self.clients)
        pending_clients = len(self.filter_clients("pending"))
        resolved_clients = len(self.filter_clients("resolved"))
        return {
            "total_clients": total_clients,
            "pending_clients": pending_clients,
            "resolved_clients": resolved_clients,
        }