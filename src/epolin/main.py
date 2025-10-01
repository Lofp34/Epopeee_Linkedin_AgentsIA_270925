#!/usr/bin/env python
import re
import sys
import unicodedata
import warnings
from typing import Any, Dict

from epolin.crew import Epolin

# CrewAI utilise pysbd pour segmenter du texte. On masque ce warning connu afin
# de garder la sortie console propre pour un utilisateur final.
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def _slugify(*parts: str) -> str:
    """Créer un slug URL-safe à partir de plusieurs fragments de texte."""
    raw = "-".join(part for part in parts if part).strip()
    normalized = unicodedata.normalize("NFKD", raw)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^a-z0-9]+", "-", ascii_only.lower())
    return cleaned.strip("-") or "prospect"


def _tokenize(*parts: str) -> str:
    """Transformer du texte en jetons compatibles avec un nom de fichier."""
    raw = "_".join(part for part in parts if part).strip()
    normalized = unicodedata.normalize("NFKD", raw)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", ascii_only.upper())
    return cleaned.strip("_") or "PROSPECT"


BASE_INPUTS: Dict[str, Any] = {
    "prospect": "Marc Seguret de Seguret Decoration à Montpellier",
    "company": "Seguret Decoration",
    "first_name": "Marc",
    "last_name": "Seguret",
    "website_url": "https://seguret-decoration.fr",
}


def _prepare_inputs(overrides: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Composer les inputs attendus par la crew en ajoutant les dérivés utiles."""
    data: Dict[str, Any] = {**BASE_INPUTS}
    if overrides:
        data.update({k: v for k, v in overrides.items() if v is not None})

    company = str(data.get("company", "")).strip()
    first_name = str(data.get("first_name", "")).strip()
    last_name = str(data.get("last_name", "")).strip()

    data["company_token"] = _tokenize(company)
    data["first_name_token"] = _tokenize(first_name)
    data["last_name_token"] = _tokenize(last_name)
    data["prospect_slug"] = _slugify(company, first_name, last_name)
    data["prospect_directory"] = f"prospects/{data['prospect_slug']}"
    data["prospect_filename_stub"] = (
        f"{data['company_token']}_{data['first_name_token']}_{data['last_name_token']}"
    )

    return data


def run():
    """Point d'entrée principal utilisé par ``crewai run``."""
    # On prépare un nouveau dictionnaire pour éviter les effets de bord.
    Epolin().crew().kickoff(inputs=_prepare_inputs())


def train():
    """Boucle d'entraînement (replay automatisé) fournie par CrewAI."""
    Epolin().crew().train(
        n_iterations=int(sys.argv[1]),
        filename=sys.argv[2],
        inputs=_prepare_inputs(),
    )


def replay():
    """Relance la crew depuis un identifiant de tâche enregistré."""
    Epolin().crew().replay(task_id=sys.argv[1])


def test():
    """Évalue la crew en boucle en utilisant un LLM d'auto-évaluation."""
    Epolin().crew().test(
        n_iterations=int(sys.argv[1]),
        eval_llm=sys.argv[2],
        inputs=_prepare_inputs(),
    )
