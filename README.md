# HelpFlow AI Customer — Support Client & Analytique Décisionnelle

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Stdlib%20Only)-brightgreen)
![Architecture](https://img.shields.io/badge/Architecture-Modular%20OOP%20%2B%20HITL-orange)
![Tests](https://img.shields.io/badge/Unit%20Tests-Passing-success)

SystÃ¨me modulaire de gestion, de routage et d'analyse intelligente de tickets clients dÃ©veloppÃ© en **Python orientÃ© objet pur** (bibliothÃ¨que standard uniquement, **zÃ©ro dÃ©pendance externe**).

ConÃ§u pour allier la puissance d'un **LLM cloud (Groq API)** Ã  la robustesse d'un **moteur NLP symbolique dÃ©terministe**, le systÃ¨me automatise le traitement des demandes courantes tout en maintenant un **contrÃ´le humain dans la boucle (*Human-in-the-Loop*)** sur les incidents critiques.

---

## Table des matiÃ¨res

- [AI Customer Intelligence Agent](#helpflow-ai-customer)
  - [Table des matiÃ¨res](#table-des-matiÃ¨res)
  - [Architecture \& Flux de donnÃ©es](#architecture--flux-de-donnÃ©es)
  - [Structure du dÃ©pÃ´t](#structure-du-dÃ©pÃ´t)
  - [FonctionnalitÃ©s clÃ©s](#fonctionnalitÃ©s-clÃ©s)
    - [1. Agent IA Hybride (*Strategy Pattern \& Graceful Fallback*)](#1-agent-ia-hybride-strategy-pattern--graceful-fallback)
    - [2. Garde-fou *Human-in-the-Loop* (HITL)](#2-garde-fou-human-in-the-loop-hitl)
    - [3. Persistance \& Analytique dÃ©cisionnelle](#3-persistance--analytique-dÃ©cisionnelle)
  - [Installation \& Configuration](#installation--configuration)
  - [Utilisation](#utilisation)
    - [Mode Console Interactive (CLI)](#mode-console-interactive-cli)
    - [Mode Pipeline AutomatisÃ©](#mode-pipeline-automatisÃ©)
  - [Tests unitaires](#tests-unitaires)
  - [Ã‰volution du projet (Roadmap)](#Ã©volution-du-projet-roadmap)
  - [Auteur](#auteur)

---

## Architecture & Flux de donnÃ©es

```text
  [Console CLI / Pipeline]
             â”‚
             â–¼
  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”      Persistance atomique      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
  â”‚   CustomerManager   â”‚ â—„â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–º â”‚ data/customers.jsonâ”‚
  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                                â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
             â”‚
             â–¼  Tickets 'pending'
  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
  â”‚               CustomerIntelligenceAgent                  â”‚
  â”‚                                                          â”‚
  â”‚   1. Moteur Primaire : Groq LLM (openai/gpt-oss-20b)     â”‚
  â”‚      â””â”€ Sortie JSON stricte (temperature=0)              â”‚
  â”‚   2. Repli DÃ©terministe : NLP Symbolique (NFD + Lexique) â”‚
  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
             â”‚
             â”œâ”€â”€â–º Urgence basse / moyenne â”€â”€â–º RÃ©solution automatique ('resolved')
             â”‚
             â””â”€â”€â–º Urgence haute (HITL) â”€â”€â”€â”€â”€â–º Escalade prioritaire ('pending')
                                                   â”‚
                                                   â–¼
                                         [Validation Humaine CLI]
                                                   â”‚
                                                   â–¼
                                         [AnalyticsReporter -> CSV]
```

---

## Structure du dÃ©pÃ´t

```text
helpflow-ai-customer/
â”œâ”€â”€ .vscode/
â”‚   â””â”€â”€ settings.json           # Configuration Pylance (extraPaths -> src)
â”œâ”€â”€ data/
â”‚   â””â”€â”€ customers.json          # Base de donnÃ©es persistante (sauvegarde atomique)
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ models.py               # EntitÃ© Customer et validation des invariants mÃ©tier
â”‚   â”œâ”€â”€ storage.py              # Couche d'accÃ¨s et sÃ©rialisation JSON
â”‚   â”œâ”€â”€ customer_manager.py     # OpÃ©rations CRUD, filtrage par statut et mÃ©triques
â”‚   â”œâ”€â”€ agent.py                # Agent IA hybride (LLM Groq + Fallback NLP + HITL)
â”‚   â”œâ”€â”€ analytics.py            # Calcul des KPIs et export analytique CSV (UTF-8 BOM)
â”‚   â”œâ”€â”€ cli.py                  # Console interactive en ligne de commande
â”‚   â””â”€â”€ main.py                 # Point d'entrÃ©e d'orchestration du pipeline
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ test_agent.py           # Tests unitaires de l'agent hybride et du garde-fou HITL
â”‚   â””â”€â”€ test_analytics.py       # Tests unitaires des KPIs et de l'export CSV
â”œâ”€â”€ .gitignore
â””â”€â”€ README.md
```

---

## FonctionnalitÃ©s clÃ©s

### 1. Agent IA Hybride (*Strategy Pattern & Graceful Fallback*)
- **Moteur primaire LLM (Groq API â€” `openai/gpt-oss-20b`)** :
  - Classification sÃ©mantique en sortie JSON structurÃ©e (`temperature=0`) parmi 5 catÃ©gories : `livraison`, `remboursement`, `produit_endommage`, `facturation`, `demande_generale`.
  - Analyse de sentiment (`positif`, `neutre`, `negatif`), Ã©valuation du niveau d'urgence (`basse`, `moyenne`, `haute`) et gÃ©nÃ©ration d'une rÃ©ponse client contextualisÃ©e en franÃ§ais.
  - Protection anti-injection de prompt via isolation des messages clients entre balises XML (`<customer_message>`).
- **Repli dÃ©terministe (*Fallback* hors-ligne)** :
  - Moteur NLP symbolique basÃ© sur la normalisation Unicode NFD (suppression des diacritiques) et un scoring lexical pondÃ©rÃ©.
  - Bascule automatique et transparente en cas d'absence de clÃ© API, d'erreur rÃ©seau (`urllib.error.URLError`) ou de quota dÃ©passÃ©.

### 2. Garde-fou *Human-in-the-Loop* (HITL)
- Tout ticket dÃ©tectÃ© avec une urgence **`haute`** (ex. produit endommagÃ©, fraude, double prÃ©lÃ¨vement) dÃ©clenche automatiquement le prÃ©fixe `[ESCALADE PRIORITAIRE]`.
- Le ticket est maintenu en statut **`pending`** jusqu'Ã  sa revue et sa clÃ´ture explicite par un opÃ©rateur humain depuis la console interactive.

### 3. Persistance & Analytique dÃ©cisionnelle
- **ZÃ©ro dÃ©pendance externe** : RequÃªtes HTTP via `urllib.request`, persistance JSON avec Ã©criture atomique, export CSV via `csv.DictWriter`.
- **Tableau de bord KPI & Export CSV** : Calcul en temps rÃ©el du taux de rÃ©solution automatique, suivi du volume d'escalades critiques et export au format CSV compatible Excel (`delimiter=";"`, encodage `utf-8-sig`).

---

## Installation & Configuration

1. **Cloner le dÃ©pÃ´t** :
   ```bash
   git clone https://github.com/HaitamSEKK/helpflow-ai-customer.git
   cd helpflow-ai-customer
   ```

2. **Configurer la clÃ© API Groq** *(optionnel â€” sans clÃ©, l'agent bascule automatiquement sur le moteur heuristique local)* :
   CrÃ©er un fichier `.env` Ã  la racine du projet :
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
2. **CrÃ©er un nouveau ticket client** avec validation des donnÃ©es (`Customer`).
3. **Lancer l'agent IA** sur la file d'attente `pending`.
4. **Valider manuellement un ticket escaladÃ© (HITL)** et le clÃ´turer en `resolved`.
5. **Afficher les KPIs & exporter le rapport CSV** (`data/report.csv`).

### Mode Pipeline AutomatisÃ©
```bash
python src/main.py
```

---

## Tests unitaires

L'ensemble de la logique mÃ©tier (classification, bascule *fallback*, escalade HITL, persistance JSON, calcul des KPIs et export CSV) est couvert par la suite `unittest` :

```bash
python -m unittest discover -s tests -v
```

---

## Ã‰volution du projet (Roadmap)

- **Module 1** : Prototypage procÃ©dural et contrÃ´les unitaires initiaux.
- **Module 2** : Refactorisation en architecture orientÃ©e objet (`Customer`, `CustomerManager`).
- **Module 3** : Couche de persistance JSON (`storage.py`) et sauvegarde automatique.
- **Module 4** : Agent IA hybride (Groq LLM + Fallback NLP), garde-fou HITL et tests unitaires (`test_agent.py`).
- **Module 5** : Console interactive CLI (`cli.py`), reporting KPI & export CSV (`analytics.py`, `test_analytics.py`).

---

## Auteur

**Haitam Sekkouri** â€” Ã‰lÃ¨ve-ingÃ©nieur Ã  l'Ã‰cole Centrale Casablanca  
[GitHub](https://github.com/HaitamSEKK) Â· [LinkedIn](https://www.linkedin.com/in/haitam-sekkouri)
