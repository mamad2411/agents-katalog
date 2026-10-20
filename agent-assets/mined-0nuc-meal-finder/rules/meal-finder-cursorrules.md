Projet : MealFinder

Description :
MealFinder est une application mobile permettant aux utilisateurs de trouver des recettes adaptées à leurs besoins nutritionnels. Chaque recette affiche les macros (protéines, glucides, lipides) ainsi que les calories par repas, facilitant ainsi le suivi des objectifs alimentaires.

Technologies utilisées :

React Native

Expo

Express ( API)

SupaBase


API de nutrition (ex: Spoonacular, Edamam)

Pages de l'application :

Accueil : Page d'accueil avec une barre de recherche et suggestions de recettes populaires.

Recherche avancée : Permet aux utilisateurs de filtrer les recettes selon leurs besoins en macros et calories.

Détails de la recette : Affiche la recette complète avec les ingrédients, instructions, valeurs nutritionnelles et un bouton d'ajout aux favoris.

Favoris : Liste des recettes sauvegardées par l'utilisateur.

Profil utilisateur : Gestion du compte utilisateur, paramètres et suivi des objectifs nutritionnels.

Fonctionnalités principales :

Inscription et Connexion : Authentification via e-mail/mot de passe ou Google.

Recherche intelligente : Rechercher des recettes par nom, ingrédients ou valeurs nutritionnelles.

Personnalisation : Filtrer et trier les recettes en fonction des objectifs (perte de poids, prise de masse, maintien).

Ajout aux favoris : Permet de sauvegarder des recettes pour un accès rapide.

Historique de recherche : Liste des recherches récentes pour une navigation plus rapide.

Mode hors ligne : Possibilité d'enregistrer des recettes pour les consulter sans connexion Internet.






Process : 

# Télécharge et installe PostgreSQL depuis :
https://www.postgresql.org/download/windows/


npm install prisma --save-dev
npm install @prisma/client


npx prisma init

npx prisma db push