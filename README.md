# TP 3 - Qualite de code dans la CI Flask

![CI](https://github.com/ktebily-sudo/usinage-logicielle-/actions/workflows/ci.yml/badge.svg)

Projet Flask minimal pour le TP 3 "Qualite de code". Le depot contient
une application simple, une suite de tests `pytest` et un pipeline
GitHub Actions qui verifie le formatage, le linting, l'analyse de
securite, la couverture et l'analyse SonarCloud.

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
pip install pre-commit
```

## Lancer l'application

```powershell
python src/app.py
```

L'application est alors accessible sur `http://127.0.0.1:5000`.

## Verification locale

```powershell
black --check --diff src/ tests/
ruff check src/ tests/
bandit -r src/
semgrep --config auto src/
python -m pytest --cov=src --cov-report=term-missing --cov-report=html:coverage-report --cov-report=xml --cov-fail-under=70 -v
```

Le rapport HTML est genere dans `coverage-report/` et le rapport XML
dans `coverage.xml`.

## Hooks pre-commit

```powershell
pre-commit install
pre-commit run --all-files
```

## Workflow GitHub Actions

Le workflow `ci.yml` :

- se declenche sur `push` et `pull_request` vers `main`
- installe Python 3.12
- restaure le cache `pip` a partir de `requirements.txt`
- installe les dependances
- verifie le formatage avec `black --check`
- execute `ruff check`
- execute `bandit -r src/ -ll`
- execute `semgrep --config auto --error src/`
- execute `pytest` avec couverture et seuil minimal
- lance SonarCloud si `SONAR_TOKEN` est configure
- publie `coverage-report/` et `coverage.xml` en artefacts

## Protection de la branche `main`

Configuration recommandee dans GitHub :

1. Ouvrir `Settings > Branches > Add branch protection rule`
2. Cibler la branche `main`
3. Activer `Require a pull request before merging`
4. Activer `Require status checks to pass before merging`
5. Selectionner le job CI comme verification obligatoire

Ainsi, aucun code non valide ne peut etre fusionne directement dans
`main` sans passer par la revue et la CI.
