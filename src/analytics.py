from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from agent import AnalysisResult
from customer_manager import CustomerManager


class AnalyticsReporter:
    """Génère des indicateurs KPI et exporte les données clients au format CSV."""

    def __init__(self, manager: CustomerManager) -> None:
        self.manager = manager

    def compute_kpis(self, analyses: list[AnalysisResult] | None = None) -> dict[str, Any]:
        stats = self.manager.get_customer_statistics()
        total = stats["total_clients"]
        resolved = stats["resolved_clients"]
        pending = stats["pending_clients"]
        resolution_rate = round((resolved / total) * 100, 1) if total > 0 else 0.0

        escalated_count = (
            sum(1 for item in analyses if item.requires_escalation)
            if analyses
            else 0
        )

        return {
            "total_clients": total,
            "resolved_clients": resolved,
            "pending_clients": pending,
            "resolution_rate_pct": resolution_rate,
            "escalated_tickets": escalated_count,
        }

    def export_csv(
        self,
        output_path: str | Path = "data/report.csv",
        analyses: list[AnalysisResult] | None = None,
    ) -> Path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)

        analysis_by_id = {item.customer_id: item for item in (analyses or [])}

        fieldnames = [
            "id",
            "name",
            "email",
            "status",
            "message",
            "ai_category",
            "ai_urgency",
            "ai_sentiment",
            "hitl_escalation",
            "ai_engine",
        ]

        all_clients = self.manager.filter_clients("pending") + self.manager.filter_clients("resolved")

        with target.open("w", encoding="utf-8-sig", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()

            for client in all_clients:
                analysis = analysis_by_id.get(client.id)
                writer.writerow(
                    {
                        "id": client.id,
                        "name": client.name,
                        "email": client.email,
                        "status": client.status,
                        "message": client.message,
                        "ai_category": analysis.category if analysis else "non_analyse",
                        "ai_urgency": analysis.urgency if analysis else "non_analyse",
                        "ai_sentiment": analysis.sentiment if analysis else "non_analyse",
                        "hitl_escalation": analysis.requires_escalation if analysis else False,
                        "ai_engine": analysis.engine_used if analysis else "none",
                    }
                )

        return target