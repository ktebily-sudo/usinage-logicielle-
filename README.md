# TP 2 - Integration Continue avec Flask

[![CI](https://github.com/ktebily-sudo/usinage-logicielle-/actions/workflows/ci.yml/badge.svg)](https://github.com/ktebily-sudo/usinage-logicielle-/actions/workflows/ci.yml)

Projet Flask minimal pour le TP 2 "Integration Continue avec GitHub
Actions". Le depot contient une application simple, une suite de tests
`pytest` et un pipeline CI qui execute le linting, les tests et la
generation d'un rapport de couverture HTML.

## Structure du projet

```text
.
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- src/
|   |-- __init__.py
|   `-- app.py
|-- tests/
|   `-- test_app.py
|-- .gitignore
|-- compte -rendu.md
|-- pytest.ini
|-- README.md
`-- requirements.txt
```

## Installation locale

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Lancer l'application

```powershell
python src/app.py
```

L'application est alors accessible sur `http://127.0.0.1:5000`.

## Verification locale

```powershell
python -m flake8 src tests
python -m pytest --cov=src --cov-report=term-missing --cov-report=html:coverage-report
```

Le rapport HTML est genere dans `coverage-report/`. Ouvrir ensuite
`coverage-report/index.html` dans un navigateur pour consulter la
couverture.

## Workflow GitHub Actions

Le workflow `ci.yml` :

- se declenche sur `push` et `pull_request` vers `main`
- installe Python 3.11
- restaure le cache `pip` a partir de `requirements.txt`
- installe les dependances
- execute `flake8`
- execute `pytest` avec couverture
- genere `coverage-report/`
- publie le rapport en artefact, meme si les tests echouent

## Protection de la branche `main`

Configuration recommandee dans GitHub :

1. Ouvrir `Settings > Branches > Add branch protection rule`
2. Cibler la branche `main`
3. Activer `Require a pull request before merging`
4. Activer `Require status checks to pass before merging`
5. Selectionner le job CI comme verification obligatoire

Ainsi, aucun code non valide ne peut etre fusionne directement dans
`main` sans passer par la revue et la CI.
