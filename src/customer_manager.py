from models import VALID_STATUSES, Customer

class CustomerManager:
    """Gère une collection d'instances Customer et leurs opérations métier."""

    def __init__(self, clients: list[Customer] | None = None) -> None:
        """Initialise le gestionnaire avec une liste optionnelle de clients."""
        self.clients: list[Customer] = list(clients) if clients else []

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
        """Crée un nouveau client avec le statut pending, l'ajoute à la liste et le retourne."""
        new_id = max((c.id for c in self.clients), default=0) + 1
        new_client = Customer(
            id=new_id,
            name=name,
            email=email,
            message=message,
            status="pending"
        )
        self.clients.append(new_client)
        return new_client


    def filter_clients(self, status: str) -> list[Customer]:
        """Retourne la liste des clients correspondant au statut demandé."""
        return [client for client in self.clients if client.status == status]


    def update_status(self, client_id: int, new_status: str) -> bool:
        """Met à jour le statut d'un client et retourne True si trouvé, False sinon."""
        if new_status not in VALID_STATUSES:
            raise ValueError(f"Statut invalide : {new_status}")
        client = self.search_client(client_id)
        if client is None:
            return False
        else:
            client.status = new_status
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

