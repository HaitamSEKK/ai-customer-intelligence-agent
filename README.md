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
│   ├── customer_manager.py     # CRUD, filtrage multicritère et métriques KPI
│   ├── agent.py                # Agent IA hybride (LLM Groq + Fallback NLP + HITL)
│   └── main.py                 # Orchestration complète du pipeline de traitement
└── tests/
    └── test_agent.py           # Suite de tests unitaires (unittest)