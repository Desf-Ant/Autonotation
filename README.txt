AUTONOTATION 

Ce projet permet de naviguer dans un dataset d'image et de les annoter afin d'obtenir un CSV pour de la classification.
Le dataset d'entrée est composé d'image avec les coordonnées de l'objet à annoter, les sous-images (coordonnée en rectangle)
Il utilise pour cela une interface graphique Qt.

Pour l'utiliser il vous faudra :
 - Avoir un CSV d'entrée de la forme suivante :
	__________________________________________
	|C:/.../name0001.jpg | x1 | y1 | x2 | y2 |
   Où x1, y1, x2 et y2 définissent le rectangle contenant la sous-image à annoter.

 - Lancer Autonotation.py

 - Ouvrir ce CSV avec Autonotation.py (file -> ouvrir)

 - Annoter les images !

 - Vous pouvez quitter autonotation à tous moments. A la réouverture de du CSV, autonotation reprendra à la derniere image non annontées.

 - Vous pouvez ajouter des images dans le CSV? autonotation mettra à jour.
   /!\ Ne pas supprimer ou changer des images dans le CSV 

 - Autonotation créé un dossier crops où se trouveront toutes les sous images avec un nom propre et un csv (annotations.csv) où pour chaque sous-image est associé un label.
