import csv
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from agent import CustomerIntelligenceAgent
from analytics import AnalyticsReporter
from customer_manager import CustomerManager


class TestAnalyticsReporter(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = TemporaryDirectory()
        self.storage_path = Path(self.tmp_dir.name) / "clients.json"
        self.csv_path = Path(self.tmp_dir.name) / "report.csv"
        self.manager = CustomerManager(storage_path=self.storage_path)
        self.agent = CustomerIntelligenceAgent(api_key="")
        self.reporter = AnalyticsReporter(self.manager)

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def test_kpis_and_csv_export(self) -> None:
        self.manager.add_client(
            name="Youssef",
            email="youssef@example.com",
            message="Produit arrivé cassé et endommagé.",
        )
        self.manager.add_client(
            name="Nadia",
            email="nadia@example.com",
            message="Question sur ma facture.",
        )

        analyses = self.agent.process_pending_tickets(self.manager)
        kpis = self.reporter.compute_kpis(analyses)

        self.assertEqual(kpis["total_clients"], 2)
        self.assertEqual(kpis["resolved_clients"], 1)
        self.assertEqual(kpis["pending_clients"], 1)
        self.assertEqual(kpis["resolution_rate_pct"], 50.0)
        self.assertEqual(kpis["escalated_tickets"], 1)

        exported = self.reporter.export_csv(self.csv_path, analyses)
        self.assertTrue(exported.exists())

        with exported.open("r", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f, delimiter=";"))

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["hitl_escalation"], "True")
        self.assertEqual(rows[1]["status"], "resolved")


if __name__ == "__main__":
    unittest.main()