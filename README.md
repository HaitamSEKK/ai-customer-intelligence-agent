# AI Customer Intelligence Agent

Système modulaire de gestion, de routage et d'analyse intelligente de tickets clients développé en Python orienté objet (bibliothèque standard uniquement, zéro dépendance externe).

## Architecture du Projet

```text
ai-customer-intelligence-agent/
├── data/
│   └── customers.json          # Base de données persistante (sauvegarde atomique)
├── src/
│   ├── models.py               # Modèle Customer et validation des invariants métier
│   ├── storage.py              # Couche d'accès et sérialisation JSON
│   ├── customer_manager.py     # CRUD, filtrage par statut et métriques KPI
│   ├── agent.py                # Agent IA hybride (LLM Groq + Fallback NLP + HITL)
│   ├── analytics.py            # Calcul des KPIs et export analytique CSV (UTF-8 BOM)
│   ├── cli.py                  # Console interactive en ligne de commande
│   └── main.py                 # Orchestration complète du pipeline de traitement
└── tests/
    ├── test_agent.py           # Tests unitaires de l'agent hybride et du garde-fou HITL
    └── test_analytics.py       # Tests unitaires des KPIs et de l'export CSV