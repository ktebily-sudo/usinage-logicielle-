Question 1 : 
Le répertoire .git/ contient toutes les données internes de Git pour le projet : l'historique des commits, les objets (blobs, trees, commits), les références (branches, tags), la configuration locale du dépôt et l'index (staging area).
Il sert de base de données Git : c'est là que Git stocke tout ce qui permet de suivre les versions, reconstruire l'état du projet à une révision donnée et gérer les branches et tags.
$ ls -la .git/
total 11
drwxr-xr-x 1 ktebi 197609   0 Mar 27 12:06 ./
drwxr-xr-x 1 ktebi 197609   0 Mar 27 12:06 ../
-rw-r--r-- 1 ktebi 197609  23 Mar 27 12:06 HEAD
-rw-r--r-- 1 ktebi 197609 130 Mar 27 12:06 config
-rw-r--r-- 1 ktebi 197609  73 Mar 27 12:06 description
drwxr-xr-x 1 ktebi 197609   0 Mar 27 12:06 hooks/
drwxr-xr-x 1 ktebi 197609   0 Mar 27 12:06 info/
drwxr-xr-x 1 ktebi 197609   0 Mar 27 12:06 objects/
drwxr-xr-x 1 ktebi 197609   0 Mar 27 12:06 refs/



Question 2 : 
Untracked : fichier présent dans le répertoire de travail mais que Git ne suit pas encore, il n'a jamais été ajouté avec git add.
Staged : fichier ajouté à l'index avec git add, ses modifications sont prêtes à être incluses dans le prochain commit.
Committed : fichier dont l'état actuel a été enregistré dans l'historique Git via un commit, il fait partie d'une version figée du projet.

Question 3 : 
On utilise git diff pour vérifier les changements en cours avant de décider quoi ajouter.
On utilise git diff --staged pour relire précisément ce qui sera committé avant d'exécuter git commit.

Question 4 : 
On utilise git revert pour annuler un commit déjà poussé sur un dépôt partagé.
On utilise git reset (surtout --soft ou --hard) pour réorganiser ou corriger l'historique local avant de pousser.

Question 5 : 
Un fast-forward merge est une fusion où Git avance simplement le pointeur de la branche cible vers le commit de la branche fusionnée, sans créer de commit de merge.
Git effectue un fast-forward quand la branche cible n'a pas de commits supplémentaires par rapport à la branche à fusionner, c'est-à-dire qu'il n'y a pas de divergence dans l'historique.

Question 6 : 
On supprime les branches une fois fusionnées pour :
•	Garder un dépôt propre et organisé
•	Éviter l'accumulation de branches obsolètes
•	Encourager un flux de travail clair (chaque branche sert à une feature ou un bugfix précis)
Différence :
•	git branch -d supprime une branche seulement si elle a été fusionnée dans la branche courante (protection contre la perte de travail).
•	git branch -D force la suppression même si la branche n'est pas fusionnée.

Question 7 : 
Décrivez en vos propres mots ce qu'est un conflit Git, pourquoi il survient, et quelles sont les étapes pour le résoudre.
Définition
Un conflit Git se produit lorsque Git ne peut pas fusionner automatiquement des modifications car la même partie d'un fichier a été modifiée différemment dans deux branches.
Causes
Il survient typiquement lors d'un git merge ou d'un git rebase quand les changements se chevauchent sur les mêmes lignes.
Étapes de résolution
1.	Identifier les fichiers en conflit (Git les signale avec des marqueurs : <<<<<<<, =======, >>>>>>>)
2.	Éditer les fichiers conflictuels et choisir ou combiner les versions souhaitées
3.	Supprimer les marqueurs de conflit
4.	Faire git add sur les fichiers corrigés
5.	Terminer la fusion par git commit

Question 8 :
Quelle est la différence entre git fetch et git pull ? Dans quel cas préférer l'un à git fetch récupère les nouveaux commits du dépôt distant vers les branches distantes locales (par exemple origin/main) sans modifier la branche courante.
•	git pull équivaut à git fetch suivi d'un merge (ou rebase) dans la branche courante, il met directement à jour ton travail local.
Préférence :
•	On préfère git fetch quand on veut d'abord inspecter les changements ou contrôler manuellement la manière de les intégrer.
•	On préfère git pull pour se mettre rapidement à jour quand on accepte l'intégration automatique.

Question 9 : 
Intérêt des Pull Requests
•	Proposer des changements avant qu'ils ne soient fusionnés dans main
•	Introduire une étape de revue, de discussion et de validation
•	Protéger la branche principale contre des erreurs ou régressions
code review
•	La lisibilité et la qualité du code
•	Le respect des conventions du projet
•	La présence de tests pertinents
•	L'impact sur la sécurité et les performances
•	La cohérence fonctionnelle avec la spécification
•	Pas de code dupliqué ou inutile
•	Documentation adéquate

Question 10 
Il est important de ne pas versionner certains fichiers pour :
•	Éviter d'exposer des secrets et des données sensibles
•	Éviter de polluer l'historique avec des fichiers générés ou spécifiques à un environnement
•	Limiter la taille du dépôt
•	Maintenir une cohésion entre développeurs
Trois exemples
1. Fichiers de secrets ou de configuration sensible (.env, *.key, *.pem)
•	Contiennent des mots de passe, tokens ou clés privées
•	Ne doivent jamais être partagés ou visibles dans l'historique public
•	Risque majeur de sécurité
2. Fichiers générés ou de cache (__pycache__/, *.pyc, artefacts de build)
•	Peuvent être recréés à partir du code source
•	Encombrent inutilement le dépôt et augmentent sa taille
•	N'apportent aucune valeur à la collaboration
3. Fichiers spécifiques à un IDE ou au système (.vscode/, .idea/, .DS_Store, Thumbs.db)
•	Dépendent de la machine et de l'outil de chaque développeur
•	N'ont pas d'intérêt fonctionnel pour le projet
•	Créent du bruit dans les diffs et les commits

Question 11 : Utilisation avancée de Git
Expliquez dans quelles situations git stash, git bisect et git reflog vous seraient utiles dans un projet réel.
git stash
Utilité : Sauvegarder temporairement des modifications en cours sans les committer.
Situations réelles :
•	On a du travail en cours non terminé mais on doit changer de branche d'urgence
•	On doit faire un git pull proprement sans ses modifications locales
•	On veut tester une autre version du code sans perdre ses modifications actuelles
•	On doit nettoyer le working directory avant une opération Git
Exemple : Stash les modifications de la branche feature, switch vers main pour un hotfix, puis pop le stash pour reprendre le travail.
git bisect
Utilité : Retrouver rapidement le commit qui a introduit un bug en testant automatiquement une série de commits par dichotomie.
Situations réelles :
•	Un bug a été découvert mais on ne sait pas quel commit l'a causé
•	On doit localiser une régression dans une longue série de commits
•	On veut diagnostiquer un problème de performance ou d'intégrité
Exemple : Entre le commit v1.0 (bon) et maintenant (mauvais), git bisect teste automatiquement le point médian, on indique si c'est bon ou mauvais, et il resserre progressivement la recherche jusqu'au commit coupable.
git reflog
Utilité : Récupérer des commits "perdus" et consulter la trace complète de tous les mouvements de HEAD.
Situations réelles :
•	On a fait un git reset --hard et on veut annuler cette action
•	On a accidentellement changé de branche et perdu une série de commits
•	On doit auditer l'historique des manipulations locales
•	On a besoin de retrouver un commit qu'on croyait supprimé
Exemple : Après un reset malencontreux, git reflog montre tous les commits antérieurs, on peut alors faire git cherry-pick <hash> pour récupérer le travail "perdu".

https://github.com/ktebily-sudo/usinage-logicielle-
