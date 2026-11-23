import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from agent import CustomerIntelligenceAgent
from customer_manager import CustomerManager


class TestCustomerIntelligenceAgent(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = TemporaryDirectory()
        self.storage_path = Path(self.tmp_dir.name) / "test_customers.json"
        self.manager = CustomerManager(storage_path=self.storage_path)
        self.agent = CustomerIntelligenceAgent(api_key="")  # Force le moteur déterministe

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def test_high_urgency_triggers_hitl_escalation(self) -> None:
        self.manager.add_client("Youssef", "youssef@example.com", "Produit arrivé endommagé.")
        results = self.agent.process_pending_tickets(self.manager)

        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].requires_escalation)
        self.assertEqual(results[0].urgency, "haute")
        self.assertEqual(self.manager.filter_clients("pending")[0].id, 1)

    def test_standard_ticket_auto_resolves_and_persists(self) -> None:
        self.manager.add_client("Nadia", "nadia@example.com", "Problème de facturation.")
        results = self.agent.process_pending_tickets(self.manager)

        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].requires_escalation)

        reloaded = CustomerManager(storage_path=self.storage_path)
        self.assertEqual(reloaded.get_customer_statistics()["resolved_clients"], 1)


if __name__ == "__main__":
    unittest.main()