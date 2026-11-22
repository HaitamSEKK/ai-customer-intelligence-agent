from customer_manager import CustomerManager
from models import Customer


def main() -> None:
    initial_clients = [
        Customer(1, "Ahmed", "ahmed@example.com", "Bonjour, où en est ma livraison ?", "pending"),
        Customer(2, "Sara", "sara@example.com", "Je souhaite un remboursement.", "resolved"),
        Customer(3, "Youssef", "youssef@example.com", "Mon produit est arrivé endommagé.", "pending"),
    ]

    manager = CustomerManager(initial_clients)

    print("=== 1. Affichage initial ===")
    manager.display_clients()

    print("\n=== 2. Recherche de clients ===")
    found = manager.search_client(2)
    not_found = manager.search_client(99)
    print("Recherche ID 2 :", found)
    print("Recherche ID 99 :", not_found)
    assert found is not None and found.name == "Sara"
    assert not_found is None

    print("\n=== 3. Ajout d'un 4e client ===")
    new_client = manager.add_client(
        name="Nadia",
        email="nadia@example.com",
        message="Problème de facturation sur ma commande.",
    )
    print("Nouveau client ajouté :", new_client)
    assert new_client.id == 4
    assert new_client.status == "pending"

    print("\n=== 4. Filtrage par statut ('pending') ===")
    pending_list = manager.filter_clients("pending")
    CustomerManager(pending_list).display_clients()
    assert len(pending_list) == 3

    print("\n=== 5. Mise à jour de statut ===")
    updated_ok = manager.update_status(1, "resolved")
    updated_fail = manager.update_status(99, "resolved")
    print("Mise à jour ID 1 :", updated_ok)
    print("Mise à jour ID 99 :", updated_fail)
    assert updated_ok is True
    assert updated_fail is False

    print("\n=== 6. Statistiques globales & Cas limite (gestionnaire vide) ===")
    stats = manager.get_customer_statistics()
    empty_stats = CustomerManager().get_customer_statistics()
    print("Statistiques actuelles :", stats)
    print("Statistiques liste vide :", empty_stats)
    assert stats == {"total_clients": 4, "pending_clients": 2, "resolved_clients": 2}
    assert empty_stats == {"total_clients": 0, "pending_clients": 0, "resolved_clients": 0}

    print("\n=== 7. Tests de validation & Sérialisation JSON ===")
    try:
        Customer(10, "Test", "email-invalide", "Message")
        assert False, "Devrait lever ValueError pour email invalide"
    except ValueError as e:
        print("Validation email OK :", e)

    try:
        manager.update_status(1, "statut_inconnu")
        assert False, "Devrait lever ValueError pour statut invalide"
    except ValueError as e:
        print("Validation statut OK :", e)

    reconstructed = Customer.from_dict(new_client.to_dict())
    assert reconstructed.to_dict() == new_client.to_dict()
    print("Sérialisation to_dict / from_dict OK :", reconstructed)

    print("\nTous les tests POO ont réussi avec succès.")


if __name__ == "__main__":
    main()