# 🚀 Epopee LinkedIn – CrewAI

Epopee LinkedIn automatise la collecte et l'analyse d'informations autour d'un prospect afin de préparer une stratégie de prise de contact multicanale. Le projet s'appuie sur [CrewAI](https://crewai.com) et une série d'agents spécialisés (LinkedIn, scraping web, veille sectorielle, stratégie commerciale).

## 🧰 Prérequis

- Python ≥ 3.10 et < 3.14
- [uv](https://docs.astral.sh/uv/) pour la gestion des dépendances Python
- Node.js ≥ 18 (utilisé pour lancer les serveurs MCP via `npx`)
- Accès aux API nécessaires :
  - `OPENAI_API_KEY` (modèle principal de génération)
  - `SERPER_API_KEY` (recherche web)
  - `HDW_ACCESS_TOKEN` & `HDW_ACCOUNT_ID` (serveur Horizon Data Wave pour LinkedIn)
  - Autres clés optionnelles selon vos outils (`XAI_API_KEY`, LM Studio, etc.)

## ⚙️ Installation

1. Cloner le dépôt puis se placer à la racine du projet (`epolin`).
2. Installer les dépendances Python :

   ```bash
   uv sync
   ```

   Le fichier `pyproject.toml` déclare toutes les dépendances ; aucun `requirements.txt` supplémentaire n'est nécessaire.

3. (Optionnel) Si vous préférez `crewai install`, la commande reste compatible.

## 🔐 Configuration des secrets

1. Dupliquer le fichier `.env.example` → `.env`.
2. Renseigner les valeurs des clés :

   ```env
   OPENAI_API_KEY=...
   SERPER_API_KEY=...
   XAI_API_KEY=...
   CREWAI_TRACING_ENABLED=true
   HDW_ACCESS_TOKEN=...
   HDW_ACCOUNT_ID=...
   LM_STUDIO_API_BASE=...
   LM_STUDIO_API_KEY=...
   ```

   > Ne versionnez jamais votre `.env` rempli.

## 🧠 Données d'entrée & personnalisation

- Les paramètres par défaut sont définis dans `src/epolin/main.py` via `DEFAULT_INPUTS` (`prospect`, `website_url`). Adaptez-les ou chargez vos propres valeurs depuis la CLI/`.env` si besoin.
- Les agents sont décrits dans `src/epolin/config/agents.yaml` et les tâches dans `src/epolin/config/tasks.yaml`. Chaque tâche référence un agent et génère un livrable (`01_PROFIL_LINKEDIN.md`, etc.).
- Les fichiers de connaissance situés dans `knowledge/` peuvent être enrichis pour fournir du contexte supplémentaire (ex. `info_laurent.md`).

### Agents principaux

- `profil_social_agent` : recherche et enrichissement LinkedIn via MCP Horizon Data Wave.
- `web_company_agent` : scraping du site officiel + fiche MCP recherche-entreprises.
- `sector_watch_agent` : veille sectorielle assistée par Serper.
- `outreach_strategy_agent` : synthèse finale et stratégie de contact.

## ▶️ Lancer la crew

Depuis la racine du projet :

```bash
uv run run_crew
```

ou avec l'alias CrewAI :

```bash
crewai run
```

Les livrables sont générés à la racine (`01_PROFIL_LINKEDIN.md`, `02_POSTS_LINKEDIN.md`, etc.).

### Autres commandes utiles

- `uv run train <n> <fichier>.jsonl` : replays automatiques.
- `uv run replay <task_id>` : relancer une exécution.
- `uv run test <n> <eval_llm>` : boucle d'évaluation automatique.

## 🛠️ Outils MCP

Le projet utilise deux serveurs MCP démarrés via `npx` :

- `@horizondatawave/mcp` (LinkedIn)
- `mcp-recherche-entreprises` (données INSEE)

Assurez-vous que `npx` est disponible et que vos tokens HDW sont valides. Ajustez le timeout ou les paramètres dans `src/epolin/crew.py` si nécessaire.

## 🧪 Tests & validation

- Après modification, exécuter `uv run run_crew` pour valider le pipeline.
- Les tests automatisés (répertoires `tests/`) peuvent être adaptés pour vérifier des modules spécifiques.

## 🤝 Contribution

1. Fork / branche dédiée
2. `uv sync`
3. Implémentation + génération des livrables
4. `uv run run_crew` pour valider
5. Commit + PR

## 📚 Ressources complémentaires

- [Documentation CrewAI](https://docs.crewai.com)
- [Documentation MCP](https://modelcontextprotocol.io)
- Support interne : voir les fichiers `knowledge/`

Bon build ! 🚀
