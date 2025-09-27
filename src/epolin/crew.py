from typing import Any, Dict, List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


def _resolve_config(config: Dict[str, Any], key: str, section: str) -> Dict[str, Any]:
    """Return the configuration block associated with ``key``."""
    # YAML peut être structuré comme {"agents": {...}} ou déjà aplati. On
    # accepte les deux cas pour laisser de la flexibilité à l'utilisateur.
    if key in config and isinstance(config[key], dict):
        return config[key]
    nested = config.get(section)
    if isinstance(nested, dict) and key in nested and isinstance(nested[key], dict):
        return nested[key]
    raise KeyError(f"Configuration '{key}' non trouvée dans '{section}'.")


@CrewBase
class Epolin:
    """Définition de la crew Epolin alignée sur les fichiers YAML."""

    agents: List[BaseAgent]
    tasks: List[Task]

    def _agent_config(self, key: str) -> Dict[str, Any]:
        """Lire la configuration de l'agent correspondant dans le YAML."""
        return _resolve_config(self.agents_config, key, "agents")  # type: ignore[arg-type]

    def _task_config(self, key: str) -> Dict[str, Any]:
        """Lire la configuration de la tâche correspondante dans le YAML."""
        return _resolve_config(self.tasks_config, key, "tasks")  # type: ignore[arg-type]

    def _agent_instance(self, key: str) -> Agent:
        """Instancier dynamiquement l'agent nommé dans le YAML."""
        agent_builder = getattr(self, key, None)
        if callable(agent_builder):
            return agent_builder()
        raise KeyError(f"Agent '{key}' introuvable dans la crew.")

    def _build_task(self, key: str) -> Task:
        """Construire un objet Task complet à partir du YAML."""
        # On copie le dict pour le manipuler sans modifier la config chargée en
        # mémoire. Cela permet par exemple de supprimer la clé "agent" une fois
        # qu'on l'a traduite en instance Python.
        config = dict(self._task_config(key))
        agent_key = config.pop("agent", None)
        expected_output = config.get("expected_output")
        agent_instance = self._agent_instance(agent_key) if agent_key else None

        return Task(
            config=config,
            agent=agent_instance,
            output_file=expected_output,
        )

    @agent
    def profil_social_agent(self) -> Agent:
        """Collecte toutes les données publiques du profil LinkedIn."""
        return Agent(
            config=self._agent_config("profil_social_agent"),
            verbose=True,
        )

    @agent
    def web_company_agent(self) -> Agent:
        """Scraping du site de l'entreprise et consolidation légale."""
        return Agent(
            config=self._agent_config("web_company_agent"),
            verbose=True,
        )

    @agent
    def sector_watch_agent(self) -> Agent:
        """Analyse des tendances et actualités du secteur cible."""
        return Agent(
            config=self._agent_config("sector_watch_agent"),
            verbose=True,
        )

    @agent
    def outreach_strategy_agent(self) -> Agent:
        """Génération de la stratégie de prise de contact personnalisée."""
        return Agent(
            config=self._agent_config("outreach_strategy_agent"),
            verbose=True,
        )

    @task
    def t1_profil_linkedin(self) -> Task:
        """Étape 1 : fiche profil LinkedIn structurée."""
        return self._build_task("t1_profil_linkedin")

    @task
    def t2_cinq_derniers_posts(self) -> Task:
        """Étape 2 : extraction des 5 derniers posts."""
        return self._build_task("t2_cinq_derniers_posts")

    @task
    def t3_commentaires_du_prospect_sur_nos_posts(self) -> Task:
        """Étape 3 : collecte des commentaires sur nos contenus."""
        return self._build_task("t3_commentaires_du_prospect_sur_nos_posts")

    @task
    def t4_fiche_entreprise_site(self) -> Task:
        """Étape 4 : fiche entreprise basée sur le site officiel."""
        return self._build_task("t4_fiche_entreprise_site")

    @task
    def t5_fiche_officielle_mcp(self) -> Task:
        """Étape 5 : enrichissement avec la base MCP officielle."""
        return self._build_task("t5_fiche_officielle_mcp")

    @task
    def t6_veille_sectorielle(self) -> Task:
        """Étape 6 : synthèse de veille sectorielle."""
        return self._build_task("t6_veille_sectorielle")

    @task
    def t7_strategie_prise_de_contact(self) -> Task:
        """Étape 7 : plan d'approche multicanal personnalisé."""
        return self._build_task("t7_strategie_prise_de_contact")

    @crew
    def crew(self) -> Crew:
        """Assembler agents et tâches puis renvoyer la crew prête à lancer."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
