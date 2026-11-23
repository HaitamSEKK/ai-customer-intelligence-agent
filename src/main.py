from pathlib import Path

from agent import CustomerIntelligenceAgent
from customer_manager import CustomerManager

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "customers.json"


def main() -> None:
    if DATA_FILE.exists():
        DATA_FILE.unlink()

    manager = CustomerManager(storage_path=DATA_FILE)
    manager.add_client("Ahmed", "ahmed@example.com", "Bonjour, où en est ma livraison ?")
    manager.add_client("Sara", "sara@example.com", "Je souhaite un remboursement.")
    manager.add_client("Youssef", "youssef@example.com", "Mon produit est arrivé endommagé.")
    manager.add_client("Nadia", "nadia@example.com", "Problème de facturation.")

    # Ahmed et Sara ont déjà été traités précédemment
    manager.update_status(1, "resolved")
    manager.update_status(2, "resolved")

    print("=== État initial avant intervention de l'agent ===")
    manager.display_clients()

    print("\n=== Exécution de CustomerIntelligenceAgent sur les tickets 'pending' ===")
    agent = CustomerIntelligenceAgent()
    analyses = agent.process_pending_tickets(manager)

    for res in analyses:
        print(
            f"\n[Ticket #{res.customer_id}] Moteur={res.engine_used} | "
            f"Catégorie={res.category} | Urgence={res.urgency} | "
            f"Escalade={res.requires_escalation}"
        )
        print(f"  -> Réponse : {res.suggested_reply}")

    print("\n=== État persisté après intervention de l'agent ===")
    reloaded = CustomerManager(storage_path=DATA_FILE)
    reloaded.display_clients()

    stats = reloaded.get_customer_statistics()
    print("Statistiques finales :", stats)

    # Vérifications automatisées :
    # - Ahmed (1) et Sara (2) restent 'resolved' sans être retraités (2 analyses au total)
    # - Nadia (4, facturation) est résolue automatiquement -> 'resolved'
    # - Youssef (3, produit endommagé) est escaladé (HITL) -> reste 'pending'
    assert len(analyses) == 2
    assert stats == {"total_clients": 4, "pending_clients": 1, "resolved_clients": 3}
    print("\nValidation du Module 4 (Agent IA + Persistance) réussie.")


if __name__ == "__main__":
    main()