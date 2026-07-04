# TaskFlow - Gestionnaire de Taches Personnel
Application en console Python connectee a une base de donnees MySQL.
## Auteur
Chadral ANKOUNKOU - Licence Informatique 1 - Groupe ISI
## Technologies utilisees
- Python 3.x
- MySQL
- mysql-connector-python
## Prerequis
- Python 3.8 ou superieur
- MySQL installe et demarre
- pip install mysql-connector-python
## Installation et lancement
1. Cloner le depot
2. Creer la base de donnees en executant les scripts SQL
3. Adapter les parametres de connexion dans connexion.py
4. Lancer l'application : python main.py
## Fonctionnalites implementees
- [x] Connexion MySQL
- [x] Inscription et connexion utilisateur
- [x] Ajout, affichage, modification, suppression de taches
- [x] Changement de statut avec historique
- [x] Filtres et recherche
- [ ] Gestion des categories
- [ ] Statistiques
## Structure du projet
taskflow/
+-- main.py
+-- connexion.py
+-- utilisateur.py
+-- tache.py
+-- categorie.py
+-- etiquette.py
+-- historique.py
+-- affichage.py
+-- README.md