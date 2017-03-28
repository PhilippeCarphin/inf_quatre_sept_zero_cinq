Exemplaires
===========

Les exemplaires sont dans le dossier *tp2-donnees*

Code:
=====

Le code est dans le dossier racine

* lazy_DAG.py : classe qui implémente un graphe avec "lazy-deletion" des noeuds
* chains.py : module qui implémente les fonctions longest_chain() et
  longest_chain_decomp()
* entropy.py : classe qui implémente l'algo d'estimation
* backtrack.py : classe qui implémente l'algo de backtracking
* dynamic.py : classe qui implémente l'algoritme dynamic

* tp.sh : interface pour utiliser les algorithmes selon l'interface standard
  pour Sam.
* exec_all.sh : script qui exécute les algorithmes sur tous les exemplaires 

Notes: Chaque classe implémente la mesure de temps des algorithmes.

Données:
========

Les données brutes sont dans le dossier *Donnees_brutes*

* master_data.csv : L'ensemble des donnees utilisées pour avoir un data-frame en
  R

* backtrack_data.csv, dynamic_data.csv, entropy_data.csv : Données brutes
  séparées par algorithmes

* failed.txt: Les exemplairs pour lesquels des algos ont échoué.

Vérification:
=============

Nous avons vérifié nos réponses pour l'algorithme dynamique.  Backtrack donnait
toujours les bonnes réponses mais échouait pour presque tout.

Dans le dossier *Donnees_Brutes/checks*, nous avons les fichiers

* correct_values.csv : Les valeurs qui sont pareilles 
* wrong_values.csv : Les valeurs qui sont différentes de la réponse.  Pour ces
  cas, les deux valeurs sont montrées pour voir la différence.

	

		
