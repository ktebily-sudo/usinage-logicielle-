# Compte-rendu commun - TP5 et TP6

## Usine Logicielle - Livraison continue et gestion des artefacts

**Projet :** Application Flask dockerisée
**Objectif général :** Mettre en place une chaîne de livraison continue complète, depuis la construction d'une image Docker jusqu'à la gestion versionnée des artefacts et des releases.

## 1. Contexte

Les TP5 et TP6 s'inscrivent dans la continuité de la mise en place d'une usine logicielle autour d'une application Flask. Le TP5 a pour objectif de dockeriser l'application, de la rendre exécutable dans un environnement reproductible, puis d'automatiser la construction et la publication de l'image Docker dans un pipeline CI/CD.

Le TP6 complète ce travail en ajoutant une gestion plus professionnelle des artefacts : multi-tagging des images, versioning sémantique, tags Git, releases GitHub automatisées et pipeline de déploiement déclenché par les releases.

## 2. Travail réalisé dans le TP5

### 2.1 Ajout de Gunicorn

L'application Flask a été adaptée pour être exécutée avec `gunicorn`, serveur WSGI plus adapté à un contexte de production que le serveur de développement Flask. La dépendance a été ajoutée dans `requirements.txt`.

### 2.2 Dockerisation de l'application

Un `Dockerfile` a été créé afin de construire une image Docker de l'application. Il utilise une image `python:3.12-slim` et lance l'application avec la commande suivante :

```Dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]
```

Le Dockerfile contient également un `HEALTHCHECK` sur la route `/health`, ce qui permet à Docker ou à une plateforme d'orchestration de vérifier automatiquement que le conteneur répond correctement.

Le fichier `.dockerignore` a été ajouté pour exclure du contexte Docker les fichiers inutiles au build : cache Python, fichiers Git, tests, rapports de couverture, fichiers Markdown et environnements virtuels.

### 2.3 Docker Compose

Un fichier `docker-compose.yml` a été créé pour faciliter le lancement local de l'application. Il définit un service `web`, expose le port `5000`, injecte des variables d'environnement et monte le dossier `src` en volume afin de faciliter le développement local.

Docker Compose apporte une configuration plus lisible et reproductible qu'une longue commande `docker run`. Il devient indispensable lorsqu'un projet contient plusieurs services, par exemple une application web, une base de données et un cache.

### 2.4 Automatisation CI/CD

Le workflow GitHub Actions du projet a été complété afin de construire, tester et publier automatiquement l'image Docker. Le pipeline construit l'image, lance un conteneur de test, vérifie la route `/health`, puis pousse l'image dans le registre.

Les images sont taguées avec plusieurs tags :

- le SHA complet du commit, pour une traçabilité exacte ;
- le SHA court, plus lisible pour les développeurs ;
- `latest`, pratique pour les environnements de test mais à éviter comme référence principale en production.

Le job Docker est conditionné à la branche `main`, afin d'éviter la publication d'images issues de code non encore validé dans une Pull Request.

### 2.5 Rollback et livraison continue

Le versioning des images permet de revenir rapidement à une version précédente si une nouvelle image présente un problème. C'est le principe du rollback : on redéploie une image déjà publiée et identifiée par un tag précis.

Le TP5 met donc en place une logique de Continuous Delivery : l'image est construite, testée et publiée automatiquement, mais le déploiement final reste contrôlé.

## 3. Travail réalisé dans le TP6

### 3.1 Gestion des artefacts

Un artefact est un livrable produit par une chaîne CI/CD. Dans ce projet, les principaux artefacts sont :

- l'image Docker de l'application Flask ;
- les rapports de couverture ;
- les releases GitHub et leurs changelogs ;
- les tags Git associés aux versions.

La gestion des artefacts permet de conserver un historique clair des versions livrées et d'assurer la traçabilité entre code source, image Docker et release applicative.

### 3.2 Versioning sémantique

Le projet adopte le versioning sémantique, ou SemVer, au format `MAJOR.MINOR.PATCH`.

- `MAJOR` : changement incompatible avec les versions précédentes ;
- `MINOR` : ajout de fonctionnalité compatible ;
- `PATCH` : correction de bug sans rupture.

Une première version stable a été créée avec le tag Git annoté `v1.0.0`. Un tag annoté est préférable à un tag léger pour une release, car il contient un message, un auteur, une date et peut être signé.

Une route `/version` a également été ajoutée à l'application afin d'exposer la version applicative :

```json
{
  "version": "1.1.0"
}
```

Un test automatisé vérifie que cette route répond correctement et contient bien une clé `version`.

### 3.3 Release-please

Un workflow `.github/workflows/release.yml` a été ajouté avec `release-please`. Cet outil analyse les messages de commits selon la convention Conventional Commits :

- `fix:` déclenche une version `PATCH` ;
- `feat:` déclenche une version `MINOR` ;
- `BREAKING CHANGE` déclenche une version `MAJOR`.

release-please automatise la création des Pull Requests de release, la mise à jour du numéro de version et la génération du changelog.

### 3.4 Déplacement du déploiement vers le workflow de release

Le job Docker a été retiré du workflow `ci.yml` afin de séparer clairement les responsabilités :

- `ci.yml` vérifie la qualité, la sécurité et les tests ;
- `release.yml` gère les releases et le build de l'image versionnée.

Cette séparation évite de publier ou déployer une image à chaque push sur `main`. Le déploiement est désormais lié à une release versionnée, ce qui rend le cycle de livraison plus maîtrisé.

### 3.5 Image Docker versionnée

Lorsqu'une release est créée, le workflow construit une image Docker avec plusieurs tags :

- le tag SemVer de release, par exemple `v1.1.0` ;
- le SHA complet du commit ;
- le SHA court ;
- `latest`.

Le tag SemVer est plus lisible pour les releases officielles, tandis que le SHA reste utile pour la traçabilité technique.

### 3.6 Politique de rétention

Une politique de nettoyage Artifact Registry a été préparée dans le fichier `artifact-registry-cleanup-policy.json`. Elle supprime les images non taguées de plus de 30 jours :

```json
[
  {
    "name": "delete-untagged-older-than-30d",
    "action": {
      "type": "Delete"
    },
    "condition": {
      "tagState": "untagged",
      "olderThan": "30d"
    }
  }
]
```

Cette politique permet de limiter l'accumulation d'artefacts inutiles dans le registre et de maîtriser les coûts de stockage.

## 4. Recherche autonome

Pour analyser les pratiques de release d'un projet open source, le projet Flask a été choisi.

Page consultée : https://github.com/pallets/flask/releases

Les cinq dernières releases observées sont :

- `3.1.3` : release de sécurité, type `PATCH` ;
- `3.1.2` : corrections de bugs, type `PATCH` ;
- `3.1.1` : corrections de bugs et sécurité, type `PATCH` ;
- `3.1.0` : ajout de fonctionnalités, type `MINOR` ;
- `3.0.3` : corrections de bugs, type `PATCH`.

Les releases Flask suivent une logique proche du versioning sémantique. Les changelogs sont structurés, liés à la documentation officielle et aux milestones GitHub. Les releases semblent publiées via une automatisation GitHub Actions.

## 5. Vérifications effectuées

Les vérifications suivantes ont été exécutées localement :

```powershell
python -m black --check src/ tests/
python -m ruff check src/ tests/
python -m pytest --cov=src --cov-report=term-missing --cov-report=xml --cov-fail-under=70 -v
python -m bandit -r src/ -ll
```

Résultats :

- formatage valide ;
- linting valide ;
- tests unitaires valides ;
- couverture de tests à 100 % ;
- aucune alerte Bandit détectée.

Les fichiers YAML des workflows GitHub Actions et le fichier JSON de politique de rétention ont également été validés syntaxiquement.

## 6. Limites rencontrées

Certaines opérations n'ont pas pu être réalisées localement dans l'environnement disponible :

- le client Docker est installé, mais le daemon Docker Desktop n'était pas accessible ;
- le build et le test local de l'image Docker n'ont donc pas pu être exécutés depuis cette machine ;
- la commande Artifact Registry via `gcloud` a échoué à cause d'un problème de token d'authentification ;
- la création automatique de Pull Request avec `gh` n'a pas pu être faite car GitHub CLI n'est pas installé.

Ces limites ne concernent pas la structure du projet ni les fichiers de configuration livrés. Les workflows sont prévus pour s'exécuter dans GitHub Actions avec les secrets nécessaires.

## 7. Conclusion

Les TP5 et TP6 ont permis de faire évoluer l'application Flask vers une chaîne de livraison plus complète et plus proche d'un contexte professionnel.

Le projet dispose maintenant d'une image Docker reproductible, d'un lancement local via Docker Compose, d'un pipeline CI centré sur la qualité et la sécurité, d'une gestion de releases automatisée avec release-please, d'un versioning sémantique et d'une stratégie de conservation des artefacts.

La séparation entre CI, release et déploiement améliore la lisibilité du pipeline et renforce la traçabilité. Chaque version peut être reliée à un commit, à un tag Git, à une release GitHub et à une image Docker versionnée, ce qui facilite l'audit, le rollback et la maintenance du projet.
