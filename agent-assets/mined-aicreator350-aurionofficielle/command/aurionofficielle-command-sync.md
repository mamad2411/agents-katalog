Synchroniser la mémoire locale avec la base de données Supabase.

## Usage
`/memory:sync`

## Instructions

1. Collecter toutes les entrées mémoire locales
2. Comparer avec l'état dans Supabase (si configuré)
3. Résoudre les conflits (local gagne par défaut)
4. Pousser les nouvelles entrées vers Supabase
5. Tirer les entrées manquantes depuis Supabase
6. Afficher le rapport de synchronisation :
   - Entrées poussées
   - Entrées tirées
   - Conflits résolus
   - Erreurs éventuelles
