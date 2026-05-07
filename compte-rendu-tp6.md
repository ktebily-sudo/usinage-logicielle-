# Compte-rendu TP6 - Gestion des artefacts

## Partie 0 - Etat des lieux

**Question 1 : Qu'est-ce qu'un artefact dans le contexte d'une usine logicielle ? Donnez 3 exemples d'artefacts differents.**

Un artefact est un livrable produit par le pipeline et conserve pour etre teste, deploye ou audite. Exemples : une image Docker, un package Python publie, un rapport de couverture ou de securite.

## Partie 1 - Multi-tagging

**Question 2 : Pourquoi tagger une image avec plusieurs tags (SHA complet, SHA court, latest) ? Dans quel cas utilise-t-on chacun ?**

Le SHA complet donne une tracabilite exacte vers le commit. Le SHA court est plus lisible pour les humains, par exemple dans les logs ou les commandes de rollback. `latest` est pratique pour le developpement ou les tests rapides, mais il ne doit pas etre la reference principale en production car il change avec le temps.

## Partie 2 - Versioning semantique

**Question 3 : Expliquez le versioning semantique (SemVer). Pour chaque cas, indiquez si c'est un changement MAJOR, MINOR ou PATCH : ajout d'une route, correction d'un bug, changement du format de reponse JSON.**

SemVer utilise le format `MAJOR.MINOR.PATCH`. `MAJOR` change quand il y a une rupture de compatibilite. `MINOR` change quand on ajoute une fonctionnalite compatible. `PATCH` change quand on corrige un bug sans casser l'existant.

Ajout d'une route : `MINOR`. Correction d'un bug : `PATCH`. Changement du format de reponse JSON : `MAJOR` si cela casse les clients existants.

**Question 4 : Quelle est la difference entre un tag Git leger et un tag annote ?**

Un tag leger est juste un pointeur vers un commit. Un tag annote est un objet Git complet avec un message, un auteur, une date et eventuellement une signature. Pour une release, le tag annote est preferable car il porte plus de contexte.

## Partie 3 - Releases GitHub automatisees

**Question 5 : Comment release-please determine-t-il le numero de version a partir des commits ? Quel est le lien avec les Conventional Commits ?**

release-please analyse les messages de commits au format Conventional Commits. Un commit `fix:` provoque generalement un bump `PATCH`, un commit `feat:` provoque un bump `MINOR`, et un commit avec rupture de compatibilite, par exemple `BREAKING CHANGE`, provoque un bump `MAJOR`.

**Question 6 : Quel est l'avantage d'automatiser les releases plutot que de les creer manuellement ?**

L'automatisation evite les oublis, standardise le changelog, applique toujours les memes regles de versioning et reduit les erreurs humaines. Elle rend aussi le lien entre commits, tag Git, release GitHub et artefact Docker plus clair.

## Partie 4 - Pipeline de release complet

**Question 7 : Decrivez le pipeline de release complet, du commit au deploiement. Combien de workflows sont impliques et quel est leur role ?**

Deux workflows sont impliques. Le workflow `ci.yml` verifie la qualite, la securite et les tests sur les pushs et Pull Requests vers `main`. Le workflow `release.yml` lance release-please sur `main`, cree une PR de release avec changelog et bump de version, puis, quand une release est creee, build l'image Docker avec le tag de version et la deploie sur Cloud Run.

**Question 8 : Quelle est la difference entre deployer avec github.sha et deployer avec un tag de version SemVer ? Quand utiliser chacun ?**

`github.sha` identifie un commit exact et convient tres bien pour la tracabilite technique, les environnements de test et les rollbacks precis. Un tag SemVer comme `v1.1.0` est plus lisible et convient mieux aux releases stables communiquees aux humains. En production, le tag SemVer donne un cycle de release plus clair.

**Question 9 : Pourquoi le principe d'immutabilite des artefacts est-il important ? Que se passe-t-il si on ecrase un tag Docker existant ?**

L'immutabilite garantit qu'un artefact publie ne change plus. Si on ecrase un tag Docker existant, deux deploiements avec le meme tag peuvent lancer deux images differentes. Cela casse la tracabilite, complique les audits et rend les rollbacks peu fiables.

## Partie 5 - Recherche autonome

**Question 10 : Analysez les 5 dernieres releases du projet choisi.**

Projet choisi : Flask.

Page Releases : https://github.com/pallets/flask/releases

Les 5 dernieres releases consultees le 7 mai 2026 via l'API GitHub sont :

- `3.1.3`, publiee le 19 fevrier 2026 : release de securite, donc `PATCH`.
- `3.1.2`, publiee le 19 aout 2025 : corrections de bugs, donc `PATCH`.
- `3.1.1`, publiee le 13 mai 2025 : corrections de bugs et securite, donc `PATCH`.
- `3.1.0`, publiee le 13 novembre 2024 : feature release, donc `MINOR`.
- `3.0.3`, publiee le 7 avril 2024 : corrections de bugs, donc `PATCH`.

Les tags suivent SemVer, avec un format `MAJOR.MINOR.PATCH`. Les changelogs renvoient vers la documentation Flask et les milestones GitHub. Les releases semblent publiees par `github-actions`, donc le projet utilise une automatisation GitHub Actions pour publier ses releases.

## Politique de retention Artifact Registry

Documentation consultee : https://cloud.google.com/artifact-registry/docs/repositories/cleanup-policy

Fichier cree : `artifact-registry-cleanup-policy.json`.

Politique configuree dans le depot :

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

Commande a executer avec un compte GCP authentifie :

```powershell
gcloud artifacts repositories set-cleanup-policies flask-repo `
  --project=VOTRE_PROJECT_ID `
  --location=europe-west1 `
  --policy=artifact-registry-cleanup-policy.json `
  --no-dry-run
```

Cette application reelle est impossible depuis ce terminal sans authentification GCP et sans connaitre le `GCP_PROJECT_ID`.
