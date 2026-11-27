from __future__ import annotations

from agent import AnalysisResult, CustomerIntelligenceAgent
from analytics import AnalyticsReporter
from customer_manager import CustomerManager


class CustomerSupportCLI:
    """Interface interactive en ligne de commande pour gérer les tickets et l'agent IA."""

    def __init__(
        self,
        manager: CustomerManager | None = None,
        agent: CustomerIntelligenceAgent | None = None,
    ) -> None:
        self.manager = manager or CustomerManager()
        self.agent = agent or CustomerIntelligenceAgent()
        self.reporter = AnalyticsReporter(self.manager)
        self.last_analyses: list[AnalysisResult] = []

    def display_menu(self) -> None:
        print("\n=== Customer Intelligence Agent — Console Interactive ===")
        print("1. Lister les tickets (tous / pending / resolved)")
        print("2. Créer un nouveau ticket client")
        print("3. Lancer l'agent IA sur les tickets 'pending'")
        print("4. Valider manuellement un ticket escaladé (HITL)")
        print("5. Afficher les KPIs & exporter le rapport CSV")
        print("0. Quitter")

    def handle_list_tickets(self) -> None:
        status_filter = input("Filtrer par statut (all / pending / resolved) [all] : ").strip().lower()
        if status_filter in {"pending", "resolved"}:
            clients = self.manager.filter_clients(status_filter)
        else:
            clients = self.manager.filter_clients("pending") + self.manager.filter_clients("resolved")

        if not clients:
            print("Aucun ticket trouvé.")
            return
        for client in clients:
            print(f"[{client.id}] {client.name} ({client.email}) | Statut={client.status} | Sujet: {client.message}")

    def handle_create_ticket(self) -> None:
        name = input("Nom du client : ").strip()
        email = input("Email du client : ").strip()
        message = input("Description du problème : ").strip()
        try:
            client = self.manager.add_client(name=name, email=email, message=message)
            print(f"Ticket #{client.id} créé avec succès pour {client.name} (statut: {client.status}).")
        except ValueError as exc:
            print(f"Erreur de validation : {exc}")

    def handle_run_agent(self) -> None:
        results = self.agent.process_pending_tickets(self.manager)
        if not results:
            print("Aucun ticket 'pending' à analyser.")
            return
        self.last_analyses = results
        for res in results:
            print(
                f"\n[Ticket #{res.customer_id}] Moteur={res.engine_used} | "
                f"Catégorie={res.category} | Urgence={res.urgency} | Escalade={res.requires_escalation}"
            )
            print(f"  -> Réponse générée : {res.suggested_reply}")

    def handle_hitl_approval(self) -> None:
        pending = self.manager.filter_clients("pending")
        if not pending:
            print("Aucun ticket en attente de validation humaine.")
            return
        for client in pending:
            print(f"[{client.id}] {client.name} — {client.message}")
        raw_id = input("ID du ticket à approuver et clôturer ('resolved') : ").strip()
        if not raw_id.isdigit():
            print("ID invalide.")
            return
        updated = self.manager.update_status(int(raw_id), "resolved")
        if updated:
            print(f"Ticket #{raw_id} validé par opérateur humain et passé en 'resolved'.")
        else:
            print(f"Ticket #{raw_id} introuvable.")

    def handle_export_analytics(self) -> None:
        kpis = self.reporter.compute_kpis(self.last_analyses)
        csv_path = self.reporter.export_csv("data/report.csv", self.last_analyses)
        print("\n--- Indicateurs Clés (KPI) ---")
        print(f"Total tickets       : {kpis['total_clients']}")
        print(f"Tickets résolus     : {kpis['resolved_clients']} ({kpis['resolution_rate_pct']}%)")
        print(f"Tickets en attente  : {kpis['pending_clients']}")
        print(f"Escalades critiques : {kpis['escalated_tickets']}")
        print(f"Rapport CSV exporté : {csv_path}")

    def run(self) -> None:
        while True:
            self.display_menu()
            choice = input("\nVotre choix : ").strip()
            if choice == "1":
                self.handle_list_tickets()
            elif choice == "2":
                self.handle_create_ticket()
            elif choice == "3":
                self.handle_run_agent()
            elif choice == "4":
                self.handle_hitl_approval()
            elif choice == "5":
                self.handle_export_analytics()
            elif choice == "0":
                print("Fermeture de la console.")
                break
            else:
                print("Option non reconnue.")


if __name__ == "__main__":
    CustomerSupportCLI().run()