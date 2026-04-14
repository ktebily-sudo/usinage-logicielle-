# Compte-rendu TP 2 - Integration Continue avec GitHub Actions

La liste fournie dans le sujet contient 11 points. Les reponses
ci-dessous couvrent l'ensemble des questions demandees.

## 1. Signification de `on`, `jobs`, `runs-on`, `steps` et `uses`

- `on` definit les evenements qui declenchent le workflow, par exemple
  un `push` ou une `pull_request`.
- `jobs` regroupe les taches principales du workflow. Chaque job
  s'execute dans un environnement isole.
- `runs-on` indique le type de machine utilisee pour executer le job,
  par exemple `ubuntu-latest`.
- `steps` correspond a la suite d'actions executees dans le job.
- `uses` permet de reutiliser une action publiee sur GitHub Marketplace
  ou definie dans un autre depot.

## 2. Role de la fixture `client` et de `app.test_client()`

La fixture `client` centralise la creation d'un client de test Flask.
Elle evite de dupliquer le meme code dans chaque test et garantit un
contexte de test propre.

`app.test_client()` simule des requetes HTTP sans lancer un vrai serveur.
On peut donc tester les routes, les codes de statut et les reponses de
maniere rapide, fiable et reproductible.

## 3. Pourquoi tester localement avant de pousser

Tester localement permet de detecter les erreurs avant d'envoyer le code
sur GitHub. Cela fait gagner du temps, evite des allers-retours
inutiles et limite les echecs visibles dans la CI.

Si un test echoue dans la CI, le job est marque en echec. Dans un projet
avec branche `main` protegee, la fusion peut alors etre bloquee tant que
le probleme n'est pas corrige.

## 4. Qu'est-ce qu'un artefact GitHub Actions

Un artefact est un fichier ou un dossier produit par un workflow et
conserve apres l'execution pour etre telecharge ou consulte.

Trois exemples d'artefacts :

1. un rapport HTML de couverture de code
2. un binaire ou une archive de build
3. des journaux de test ou un rapport XML/JUnit

## 5. Couverture de code et limite du 100 %

La couverture de code mesure la proportion du code executee par les
tests. Elle donne un indicateur utile pour reperer les zones non
testees.

Viser 100 % n'est pas toujours souhaitable, car cela peut encourager des
tests artificiels qui verifient l'implementation au lieu du comportement
metier. Une bonne strategie consiste a privilegier les cas critiques, les
branches utiles et les regressions probables plutot qu'un score parfait
pour lui-meme.

## 6. Role d'un linter et pourquoi l'executer avant les tests

Un linter analyse le code source pour detecter des problemes de style,
des incoherences et certaines erreurs simples avant l'execution.

L'executer avant les tests permet de stopper rapidement une revision qui
ne respecte pas les conventions du projet. Cela economise du temps de CI
et rend le pipeline plus lisible : on valide d'abord la qualite
statique, puis le comportement.

## 7. Fonctionnement du cache dans GitHub Actions

Le cache permet de reutiliser des dependances deja telechargees au lieu
de tout reinstaller a chaque execution. Ici, la cle du cache repose sur
le hash de `requirements.txt`.

Si `requirements.txt` change, le hash change aussi. GitHub Actions ne
retrouve alors pas l'ancien cache exact et reconstruit un nouveau cache
adapte aux nouvelles dependances.

## 8. GitHub-hosted vs self-hosted runners

Les runners GitHub-hosted sont fournis et maintenus par GitHub. Ils sont
simples a utiliser, preconfigures et bien adaptes a un TP ou a un petit
projet.

Les runners self-hosted sont geres par l'equipe du projet. Ils offrent
plus de controle sur la machine, le reseau et les outils installes, mais
ils demandent plus d'administration, de maintenance et de securisation.

## 9. Workflow complet avec une branche `main` protegee

Workflow recommande :

1. le developpeur cree une branche de travail
2. il code, lance `flake8` et `pytest` en local
3. il pousse sa branche sur GitHub
4. il ouvre une Pull Request vers `main`
5. le workflow CI se declenche automatiquement
6. GitHub execute le linting, les tests et publie l'artefact
7. si tout est vert, la revue peut etre validee
8. la fusion dans `main` est autorisee seulement si les checks requis
   passent

Avec une branche `main` protegee, on evite les pushes directs non
verifies et on impose un passage par la PR et les checks obligatoires.

## 10. Action de marketplace a integrer et pourquoi

Une action utile ici est `actions/upload-artifact@v4`. Elle permet de
conserver le rapport HTML de couverture apres l'execution du workflow.

Exemple concret : meme si un test echoue, on peut telecharger
`coverage-report/` depuis l'onglet Actions pour analyser ce qui a ete
couvert et garder une trace exploitable du job.

## 11. Utilisation de `@pytest.mark.parametrize` pour `/add`

`@pytest.mark.parametrize` permet d'executer le meme test avec plusieurs
jeux de donnees. C'est ideal pour `/add`, car on veut verifier plusieurs
couples de valeurs sans dupliquer le code de test.

Exemple :

```python
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (0, 0, 0),
        (2, 3, 5),
        (10, 15, 25),
    ],
)
def test_add_route(client, a, b, expected):
    response = client.get(f"/add/{a}/{b}")
    assert response.status_code == 200
    assert response.get_json()["result"] == expected
```

Cette approche rend la suite de tests plus compacte, plus lisible et
plus facile a faire evoluer.
