# AI Customer Intelligence Agent

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Stdlib%20Only)-brightgreen)
![Architecture](https://img.shields.io/badge/Architecture-Modular%20OOP%20%2B%20HITL-orange)
![Tests](https://img.shields.io/badge/Unit%20Tests-Passing-success)

Système modulaire de gestion, de routage et d'analyse intelligente de tickets clients développé en **Python orienté objet pur** (bibliothèque standard uniquement, **zéro dépendance externe**).

Conçu pour allier la puissance d'un **LLM cloud (Groq API)** à la robustesse d'un **moteur NLP symbolique déterministe**, le système automatise le traitement des demandes courantes tout en maintenant un **contrôle humain dans la boucle (*Human-in-the-Loop*)** sur les incidents critiques.

---

## Table des matières

- [AI Customer Intelligence Agent](#ai-customer-intelligence-agent)
  - [Table des matières](#table-des-matières)
  - [Architecture \& Flux de données](#architecture--flux-de-données)
  - [Structure du dépôt](#structure-du-dépôt)
  - [Fonctionnalités clés](#fonctionnalités-clés)
    - [1. Agent IA Hybride (*Strategy Pattern \& Graceful Fallback*)](#1-agent-ia-hybride-strategy-pattern--graceful-fallback)
    - [2. Garde-fou *Human-in-the-Loop* (HITL)](#2-garde-fou-human-in-the-loop-hitl)
    - [3. Persistance \& Analytique décisionnelle](#3-persistance--analytique-décisionnelle)
  - [Installation \& Configuration](#installation--configuration)
  - [Utilisation](#utilisation)
    - [Mode Console Interactive (CLI)](#mode-console-interactive-cli)
    - [Mode Pipeline Automatisé](#mode-pipeline-automatisé)
  - [Tests unitaires](#tests-unitaires)
  - [Évolution du projet (Roadmap)](#évolution-du-projet-roadmap)
  - [Auteur](#auteur)

---

## Architecture & Flux de données

```text
  [Console CLI / Pipeline]
             │
             ▼
  ┌─────────────────────┐      Persistance atomique      ┌────────────────────┐
  │   CustomerManager   │ ◄────────────────────────────► │ data/customers.json│
  └─────────────────────┘                                └────────────────────┘
             │
             ▼  Tickets 'pending'
  ┌──────────────────────────────────────────────────────────┐
  │               CustomerIntelligenceAgent                  │
  │                                                          │
  │   1. Moteur Primaire : Groq LLM (openai/gpt-oss-20b)     │
  │      └─ Sortie JSON stricte (temperature=0)              │
  │   2. Repli Déterministe : NLP Symbolique (NFD + Lexique) │
  └──────────────────────────────────────────────────────────┘
             │
             ├──► Urgence basse / moyenne ──► Résolution automatique ('resolved')
             │
             └──► Urgence haute (HITL) ─────► Escalade prioritaire ('pending')
                                                   │
                                                   ▼
                                         [Validation Humaine CLI]
                                                   │
                                                   ▼
                                         [AnalyticsReporter -> CSV]
```

---

## Structure du dépôt

```text
ai-customer-intelligence-agent/
├── .vscode/
│   └── settings.json           # Configuration Pylance (extraPaths -> src)
├── data/
│   └── customers.json          # Base de données persistante (sauvegarde atomique)
├── src/
│   ├── models.py               # Entité Customer et validation des invariants métier
│   ├── storage.py              # Couche d'accès et sérialisation JSON
│   ├── customer_manager.py     # Opérations CRUD, filtrage par statut et métriques
│   ├── agent.py                # Agent IA hybride (LLM Groq + Fallback NLP + HITL)
│   ├── analytics.py            # Calcul des KPIs et export analytique CSV (UTF-8 BOM)
│   ├── cli.py                  # Console interactive en ligne de commande
│   └── main.py                 # Point d'entrée d'orchestration du pipeline
├── tests/
│   ├── test_agent.py           # Tests unitaires de l'agent hybride et du garde-fou HITL
│   └── test_analytics.py       # Tests unitaires des KPIs et de l'export CSV
├── .gitignore
└── README.md
```

---

## Fonctionnalités clés

### 1. Agent IA Hybride (*Strategy Pattern & Graceful Fallback*)
- **Moteur primaire LLM (Groq API — `openai/gpt-oss-20b`)** :
  - Classification sémantique en sortie JSON structurée (`temperature=0`) parmi 5 catégories : `livraison`, `remboursement`, `produit_endommage`, `facturation`, `demande_generale`.
  - Analyse de sentiment (`positif`, `neutre`, `negatif`), évaluation du niveau d'urgence (`basse`, `moyenne`, `haute`) et génération d'une réponse client contextualisée en français.
  - Protection anti-injection de prompt via isolation des messages clients entre balises XML (`<customer_message>`).
- **Repli déterministe (*Fallback* hors-ligne)** :
  - Moteur NLP symbolique basé sur la normalisation Unicode NFD (suppression des diacritiques) et un scoring lexical pondéré.
  - Bascule automatique et transparente en cas d'absence de clé API, d'erreur réseau (`urllib.error.URLError`) ou de quota dépassé.

### 2. Garde-fou *Human-in-the-Loop* (HITL)
- Tout ticket détecté avec une urgence **`haute`** (ex. produit endommagé, fraude, double prélèvement) déclenche automatiquement le préfixe `[ESCALADE PRIORITAIRE]`.
- Le ticket est maintenu en statut **`pending`** jusqu'à sa revue et sa clôture explicite par un opérateur humain depuis la console interactive.

### 3. Persistance & Analytique décisionnelle
- **Zéro dépendance externe** : Requêtes HTTP via `urllib.request`, persistance JSON avec écriture atomique, export CSV via `csv.DictWriter`.
- **Tableau de bord KPI & Export CSV** : Calcul en temps réel du taux de résolution automatique, suivi du volume d'escalades critiques et export au format CSV compatible Excel (`delimiter=";"`, encodage `utf-8-sig`).

---

## Installation & Configuration

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/HaitamSEKK/ai-customer-intelligence-agent.git
   cd ai-customer-intelligence-agent
   ```

2. **Configurer la clé API Groq** *(optionnel — sans clé, l'agent bascule automatiquement sur le moteur heuristique local)* :
   Créer un fichier `.env` à la racine du projet :
   ```env
   GROQ_API_KEY=votre_cle_api_groq
   ```

---

## Utilisation

### Mode Console Interactive (CLI)
```bash
python src/cli.py
```
Le menu interactif propose 5 actions :
1. **Lister les tickets** (`all` / `pending` / `resolved`).
2. **Créer un nouveau ticket client** avec validation des données (`Customer`).
3. **Lancer l'agent IA** sur la file d'attente `pending`.
4. **Valider manuellement un ticket escaladé (HITL)** et le clôturer en `resolved`.
5. **Afficher les KPIs & exporter le rapport CSV** (`data/report.csv`).

### Mode Pipeline Automatisé
```bash
python src/main.py
```

---

## Tests unitaires

L'ensemble de la logique métier (classification, bascule *fallback*, escalade HITL, persistance JSON, calcul des KPIs et export CSV) est couvert par la suite `unittest` :

```bash
python -m unittest discover -s tests -v
```

---

## Évolution du projet (Roadmap)

- **Module 1** : Prototypage procédural et contrôles unitaires initiaux.
- **Module 2** : Refactorisation en architecture orientée objet (`Customer`, `CustomerManager`).
- **Module 3** : Couche de persistance JSON (`storage.py`) et sauvegarde automatique.
- **Module 4** : Agent IA hybride (Groq LLM + Fallback NLP), garde-fou HITL et tests unitaires (`test_agent.py`).
- **Module 5** : Console interactive CLI (`cli.py`), reporting KPI & export CSV (`analytics.py`, `test_analytics.py`).

---

## Auteur

**Haitam Sekkouri** — Élève-ingénieur à l'École Centrale Casablanca  
[GitHub](https://github.com/HaitamSEKK) · [LinkedIn](https://www.linkedin.com/in/haitam-sekkouri)