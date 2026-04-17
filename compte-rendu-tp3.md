# Compte-rendu TP 3 - Qualite de code dans la CI Flask

## 1. Difference entre un linter et un formatter

Un linter analyse le code pour detecter des problemes de qualite
statique : erreurs probables, imports inutiles, conventions non
respectees ou constructions risquant de produire des bugs. Par exemple,
`ruff check src/ tests/` peut signaler un import non utilise ou un ordre
d'import incorrect.

Un formatter, lui, reecrit automatiquement le code pour uniformiser sa
presentation sans changer son comportement. Par exemple,
`black src/ tests/` reformate les sauts de ligne, l'indentation et les
espaces pour obtenir un style coherent dans tout le projet.

## 2. Pourquoi utiliser `--check` dans la CI avec Black

Dans la CI, on utilise `black --check` pour verifier que le code est
deja formate, sans le modifier automatiquement. Le role de la CI est de
valider un etat du depot, pas de le transformer dans le runner.

Si la CI reformatait le code elle-meme, le job ne verifierait plus
exactement ce qui a ete pousse dans le commit. Cela introduirait aussi
des differences entre le code local, le code versionne et le code
execute dans la CI. Avec `--check`, on oblige donc le developpeur a
committer un code deja propre.

## 3. Avantages de Ruff par rapport a flake8 et interet de `pyproject.toml`

Ruff est plus rapide que flake8 car il est ecrit en Rust et regroupe
dans un seul outil plusieurs familles de regles souvent ajoutees via des
plugins flake8. Il couvre donc a la fois le linting classique, le tri
des imports et de nombreuses verifications de qualite ou de
modernisation.

Centraliser la configuration dans `pyproject.toml` est plus propre que
multiplier les arguments CLI. La configuration est versionnee, lisible,
partagee entre la machine locale, les hooks pre-commit et la CI. Cela
evite aussi les divergences entre les commandes documentees et celles
reellement executees.

## 4. Difference entre Bandit et Semgrep

Bandit est specialise dans la securite Python. Il inspecte le code pour
reperer des patterns dangereux connus dans l'ecosysteme Python, par
exemple `eval`, `exec`, l'usage d'un mode debug non securise ou des
faiblesses cryptographiques.

Semgrep est plus generaliste et plus flexible. Il permet d'utiliser des
regles existantes multi-langages, mais aussi d'ecrire ses propres regles
metier. On l'utilise donc a la fois pour la securite applicative, les
anti-patterns d'architecture et les conventions propres au projet.

## 5. Analyse statique vs tests unitaires

L'analyse statique etudie le code sans l'executer. Elle cherche des
problemes de style, de securite, de structure ou des erreurs probables
directement dans le source.

Les tests unitaires, au contraire, executent le code dans des scenarios
precis pour verifier son comportement. Les deux approches sont
complementaires : l'analyse statique detecte tres tot des problemes
structurels, alors que les tests valident la logique fonctionnelle.

## 6. Interet des pre-commit hooks par rapport a la CI

Les hooks pre-commit executent des verifications avant la creation du
commit. Ils donnent un retour quasi immediat au developpeur et evitent
de pousser un code manifestement non conforme.

La CI reste indispensable car elle rejoue les controles dans un
environnement propre, identique pour toute l'equipe, et sert de verite
partagee avant une fusion. On utilise donc les deux : pre-commit pour le
feedback rapide, CI pour la verification officielle.

## 7. Pourquoi `git commit --no-verify` peut poser probleme

`git commit --no-verify` contourne les hooks locaux. Un developpeur peut
alors committer du code non formate, non linted ou avec des problemes de
qualite qui auraient normalement ete bloques.

Sur un projet d'equipe, cela diminue la confiance dans l'automatisation
locale et reporte les erreurs sur la CI ou sur la revue. Cette option ne
devrait etre reservee qu'a des cas exceptionnels et justifies.

## 8. Qu'est-ce qu'un Quality Gate

Un Quality Gate est un ensemble de conditions minimales que le projet
doit respecter avant d'etre considere comme acceptable pour la fusion ou
la livraison. C'est un mecanisme de decision automatique base sur des
indicateurs de qualite.

Exemples de conditions possibles :

1. tous les tests doivent passer
2. la couverture doit rester superieure ou egale a 70 %
3. aucun probleme critique de securite ne doit etre detecte
4. le linting et le formatage doivent etre conformes
5. le Quality Gate SonarCloud doit etre vert

## 9. Ordre des verifications dans le pipeline et justification

L'ordre recommande est : Black, Ruff, Bandit, Semgrep, puis les tests et
la couverture, puis enfin SonarCloud. Cet ordre permet d'echouer vite
sur les controles les plus simples et les moins couteux.

Black et Ruff sont tres rapides et evitent de lancer des etapes plus
lourdes sur un code deja non conforme. Bandit et Semgrep viennent
ensuite pour verifier la securite statique. Les tests et la couverture
arrivent apres, car ils sont plus couteux a executer. SonarCloud vient a
la fin pour consolider les resultats dans une vue globale.

## 10. Analyse du tableau de bord SonarCloud

Le tableau de bord SonarCloud apporte une vision centralisee de la
qualite du projet. Le Quality Gate donne un verdict global. Les
indicateurs "bugs" signalent des defauts potentiels, les "code smells"
des points de maintenabilite, la couverture mesure la part du code
executee par les tests, les duplications detectent les repetitions de
code et la dette technique estime l'effort necessaire pour revenir a un
etat plus propre.

Une reponse claire pour le compte-rendu peut etre : SonarCloud me permet
de verifier en un seul endroit si le projet respecte le seuil de qualite
attendu. Je peux y suivre la couverture, les problemes de
maintenabilite, les duplications et les alertes, puis prioriser les
corrections avant la fusion.

## 11. SonarCloud vs outils locaux

Ruff, Bandit et Semgrep sont excellents pour avoir un retour local
rapide, mais ils restent des outils separes. SonarCloud centralise les
resultats, historise les analyses et fournit un tableau de bord
partageable par toute l'equipe.

Une plateforme centralisee apporte plusieurs avantages : suivi dans le
temps, Quality Gate unique, visualisation dans les Pull Requests,
historique des tendances, priorisation des problemes et vision globale
de la dette technique.

## 12. Deux nouvelles categories Ruff pertinentes

Deux categories supplementaires pertinentes pour ce projet sont `SIM`
(flake8-simplify) et `RET` (flake8-return).

`SIM` aide a simplifier certaines constructions conditionnelles ou
booleennes, ce qui rend le code plus lisible et plus direct.
Documentation :
https://docs.astral.sh/ruff/rules/#flake8-simplify-sim

`RET` detecte des retours inutiles ou des structures de controle qui
peuvent etre simplifiees autour des `return`. Cela ameliore la
lisibilite et limite le bruit dans des fonctions courtes comme les vues
Flask.
Documentation :
https://docs.astral.sh/ruff/rules/#flake8-return-ret

Pour les activer, on peut completer `pyproject.toml` ainsi :

```toml
[tool.ruff.lint]
select = [
  "E",
  "W",
  "F",
  "I",
  "B",
  "UP",
  "SIM",
  "RET",
]
```

## Annexe - Regle Semgrep personnalisee

Une regle simple et utile consiste a interdire `print()` dans `src/`
pour eviter de laisser du debug en production :

```yaml
rules:
  - id: no-print-in-src
    languages: [python]
    severity: WARNING
    message: "Evite print() dans le code applicatif. Utilise plutot un logger."
    paths:
      include:
        - "**/src/**/*.py"
    pattern: print(...)
```

Commande de test :

```powershell
semgrep --config .semgrep/custom-rules.yml src/
```
