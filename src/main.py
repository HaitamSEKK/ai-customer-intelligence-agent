from pathlib import Path

from customer_manager import CustomerManager

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "customers.json"


def main() -> None:
    # 0. Nettoyage préalable pour démarrer le test sur une base vierge
    if DATA_FILE.exists():
        DATA_FILE.unlink()

    print("=== 1. Initialisation avec persistance JSON ===")
    manager = CustomerManager(storage_path=DATA_FILE)
    assert manager.clients == []

    manager.add_client("Ahmed", "ahmed@example.com", "Bonjour, où en est ma livraison ?")
    manager.add_client("Sara", "sara@example.com", "Je souhaite un remboursement.")
    manager.add_client("Youssef", "youssef@example.com", "Mon produit est arrivé endommagé.")
    manager.update_status(2, "resolved")
    manager.display_clients()

    print("\n=== 2. Ajout et mise à jour persistés automatiquement ===")
    nadia = manager.add_client("Nadia", "nadia@example.com", "Problème de facturation.")
    manager.update_status(1, "resolved")
    assert nadia.id == 4

    print("\n=== 3. Rechargement depuis le disque (nouvelle instance) ===")
    reloaded_manager = CustomerManager(storage_path=DATA_FILE)
    reloaded_manager.display_clients()

    stats = reloaded_manager.get_customer_statistics()
    print("Statistiques après rechargement :", stats)
    assert stats == {"total_clients": 4, "pending_clients": 2, "resolved_clients": 2}

    found_nadia = reloaded_manager.search_client(4)
    assert found_nadia is not None and found_nadia.name == "Nadia"
    assert DATA_FILE.exists()

    print("\nTous les tests de persistance JSON ont réussi avec succès.")


if __name__ == "__main__":
    main()