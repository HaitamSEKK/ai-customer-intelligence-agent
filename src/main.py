from customer_manager import (
    add_client,
    display_clients,
    filter_clients,
    get_customer_statistics,
    search_client,
    update_status,
)
def main() -> None:
    """Point d'entrée principal pour tester la gestion des clients."""
    clients = [
    {
        "id": 1,
        "name": "Ahmed",
        "email": "ahmed@example.com",
        "message": "Bonjour, où en est ma livraison ?",
        "status": "pending",
    },
    {
        "id": 2,
        "name": "Sara",
        "email": "sara@example.com",
        "message": "Je souhaite un remboursement.",
        "status": "resolved",
    },
    {
        "id": 3,
        "name": "Youssef",
        "email": "youssef@example.com",
        "message": "Mon produit est arrivé endommagé.",
        "status": "pending",
    },
]
    print("=== 1. Affichage initial ===")
    display_clients(clients)

    print("\n=== 2. Recherche de clients ===")
    found = search_client(clients, 2)
    not_found = search_client(clients, 99)
    print("Recherche ID 2 :", found)
    print("Recherche ID 99 :", not_found)
    assert found is not None and found["name"] == "Sara"
    assert not_found is None

    print("\n=== 3. Ajout d'un 4e client ===")
    new_client = add_client(
        clients,
        name="Nadia",
        email="nadia@example.com",
        message="Problème de facturation sur ma commande.",
    )
    print("Nouveau client ajouté :", new_client)
    assert new_client["id"] == 4
    assert new_client["status"] == "pending"
    assert len(clients) == 4

    print("\n=== 4. Filtrage par statut ('pending') ===")
    pending_list = filter_clients(clients, "pending")
    display_clients(pending_list)
    assert len(pending_list) == 3

    print("\n=== 5. Mise à jour de statut ===")
    updated_ok = update_status(clients, 1, "resolved")
    updated_fail = update_status(clients, 99, "resolved")
    print("Mise à jour ID 1 :", updated_ok)
    print("Mise à jour ID 99 :", updated_fail)
    assert updated_ok is True
    assert updated_fail is False

    print("\n=== 6. Statistiques globales & Cas limite (liste vide) ===")
    stats = get_customer_statistics(clients)
    empty_stats = get_customer_statistics([])
    print("Statistiques actuelles :", stats)
    print("Statistiques liste vide :", empty_stats)
    assert stats == {
        "total_clients": 4,
        "pending_clients": 2,
        "resolved_clients": 2,
    }
    assert empty_stats == {
        "total_clients": 0,
        "pending_clients": 0,
        "resolved_clients": 0,
    }

    print("\n=== 7. Affichage final ===")
    display_clients(clients)
    print("\nTous les tests ont réussi avec succès.")

    
if __name__ == "__main__":
    main()