# Compte-rendu TP5 - Livraison Continue

## Partie 1 - Dockerfile

**Question 1 : Expliquez chaque instruction du Dockerfile. Pourquoi copie-t-on requirements.txt avant le code source ?**

`FROM python:3.12-slim AS builder` utilise une image Python legere pour construire les dependances. `WORKDIR /app` fixe le dossier de travail. `COPY requirements.txt .` copie seulement les dependances. `RUN pip install --no-cache-dir --prefix=/install -r requirements.txt` installe les paquets dans un dossier qui sera recopie dans l'image finale. Le second `FROM python:3.12-slim` cree l'image finale. `RUN apt-get ... curl` installe `curl` pour le health check. `COPY --from=builder /install /usr/local` recopie les dependances. `COPY src/ ./src/` copie le code applicatif. `HEALTHCHECK` verifie que `/health` repond. `EXPOSE 5000` documente le port utilise. `CMD` lance l'application avec `gunicorn`.

On copie `requirements.txt` avant le code source pour profiter du cache Docker : si le code change mais pas les dependances, Docker ne reinstalle pas tous les paquets.

**Question 2 : Quelle est la difference entre une VM et un container Docker ? Quel est l'avantage principal des containers ?**

Une VM embarque un systeme d'exploitation complet avec son noyau virtuel. Un container partage le noyau de la machine hote et isole seulement le processus, les fichiers et l'environnement. L'avantage principal est la legerete : demarrage rapide, taille plus faible et meilleure portabilite.

## Partie 2 - Docker Compose

**Question 3 : Quel est l'interet de Docker Compose par rapport a un simple docker run ? Dans quel cas Docker Compose devient-il indispensable ?**

Docker Compose permet de declarer la configuration dans un fichier : build, ports, variables d'environnement, volumes et healthcheck. Il evite de retaper de longues commandes `docker run`. Il devient indispensable quand l'application utilise plusieurs services, par exemple une app Flask avec une base PostgreSQL, Redis ou un reverse proxy.

## Partie 3 - Registres et tagging

**Question 4 : Pourquoi tagger une image avec plusieurs tags (SHA, version, latest) ? Pourquoi ne doit-on pas utiliser :latest en production ?**

Plusieurs tags donnent plusieurs usages : le SHA identifie exactement le commit, la version semantique est lisible, et `latest` donne un pointeur pratique vers la derniere image. En production, `latest` est dangereux car il change avec le temps : on ne sait pas toujours quelle version exacte est executee, ce qui complique le rollback et le diagnostic.

**Question 5 : Qu'est-ce qu'un registre de conteneurs ? Comparez ghcr.io, Docker Hub et Google Artifact Registry.**

Un registre de conteneurs stocke et distribue des images Docker. `ghcr.io` est integre a GitHub et pratique pour un projet GitHub Actions. Docker Hub est le registre public historique et tres utilise par defaut. Google Artifact Registry est un registre gere par Google Cloud, adapte aux deploiements professionnels sur GCP.

## Partie 4 - CI/CD

**Question 6 : Pourquoi teste-t-on le conteneur dans la CI avant de le pousser sur le registre ?**

On teste le conteneur avant le push pour eviter de publier une image qui build mais ne demarre pas ou ne repond pas. Cela garde le registre propre avec seulement des images utilisables.

**Question 7 : Expliquez la condition if: github.ref == 'refs/heads/main'. Pourquoi le build Docker ne se declenche-t-il pas sur les Pull Requests ?**

La condition limite le job Docker aux pushs sur la branche `main`. Sur une Pull Request, la reference GitHub n'est pas `refs/heads/main`, donc le job ne publie pas d'image. Cela evite de pousser dans le registre du code non encore valide ou non merge.

**Question 8 : Pourquoi utilise-t-on ${{ github.sha }} comme tag d'image ? Quel avantage par rapport a un numero de version manuel ?**

`${{ github.sha }}` correspond au commit exact qui a produit l'image. C'est automatique, unique et tracable. Contrairement a un numero de version manuel, il ne peut pas etre oublie ou reutilise par erreur.

## Partie 5 - Versions et rollback

**Question 9 : Qu'est-ce qu'un rollback ? Pourquoi est-il essentiel de versionner les images Docker avec des tags precis ?**

Un rollback consiste a revenir a une version precedente si la derniere version pose probleme. Des tags precis permettent de relancer exactement l'image connue comme stable, sans ambiguity.

**Question 10 : Expliquez la difference entre Continuous Delivery et Continuous Deployment. Lequel avez-vous mis en place dans ce TP ?**

La Continuous Delivery prepare automatiquement une version livrable, mais le deploiement final peut rester manuel. La Continuous Deployment deploie automatiquement en production apres validation. Dans ce TP, on met en place de la Continuous Delivery : l'image est construite, testee et publiee, mais elle n'est pas automatiquement deployee en production.

**Question 11 : Quels risques pose le deploiement automatique ? Comment les attenuer ?**

Le deploiement automatique peut publier rapidement un bug, une faille ou une regression. On attenue ces risques avec des tests, des analyses de securite, des validations humaines, des environnements de staging, des tags precis, des rollbacks et de la surveillance.

## Partie 6 - Recherche autonome

**Question 12 : Expliquez le principe du multi-stage build. Quel est l'avantage en termes de taille et de securite ? Montrez votre Dockerfile modifie et la difference de taille. Indiquez le lien vers la documentation que vous avez consultee.**

Un multi-stage build utilise plusieurs etapes dans un Dockerfile. La premiere etape sert a construire ou installer les dependances, puis l'image finale ne recupere que le resultat utile. Cela reduit la taille finale et limite les outils presents dans l'image de production, ce qui reduit aussi la surface d'attaque.

Documentation consultee : https://docs.docker.com/build/building/multi-stage/

Dockerfile modifie :

```Dockerfile
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY src/ ./src/

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:app"]
```

Difference de taille : impossible a mesurer dans cet environnement car le client Docker est installe mais le daemon Docker Desktop n'est pas accessible. La commande `docker info` echoue avec une erreur sur `dockerDesktopLinuxEngine`.

## Plateforme de deploiement cloud choisie

Plateforme choisie : GCP Cloud Run.

Cloud Run deploie des conteneurs Docker sans gerer directement les serveurs. On fournit une image de conteneur, Cloud Run cree un service HTTP, gere le scaling automatique et permet d'injecter des variables d'environnement. L'application Flask dockerisee pourrait donc etre publiee sur un registre, puis deployee comme service Cloud Run.

## Partie 7 - Pull Request

La Pull Request doit resumer :

- Dockerfile avec HEALTHCHECK
- Docker Compose pour le developpement local
- Job Docker dans la CI
- Tags Docker avec SHA, sha court et latest

Le merge et la publication GHCR doivent etre faits sur GitHub, apres CI verte.
