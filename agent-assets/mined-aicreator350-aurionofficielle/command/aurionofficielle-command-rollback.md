Annuler un changement qui a échoué à la vérification.

## Usage
`/truth:rollback [fichier ou commit]`

## Instructions

1. Identifier le changement à annuler :
   - Fichier spécifique → Restaurer depuis Git
   - Commit → `git revert [hash]`
   - Dernier changement → `git checkout -- [file]`
2. Vérifier l'état après rollback :
   - Typecheck passe
   - Tests passent
   - Pas de régressions
3. Confirmer le rollback avec résumé
4. Stocker la raison du rollback en mémoire

## Sécurité
- Toujours créer un backup avant rollback
- Ne jamais rollback des migrations Supabase sans plan
- Confirmer avec l'utilisateur pour les changements à plusieurs fichiers
