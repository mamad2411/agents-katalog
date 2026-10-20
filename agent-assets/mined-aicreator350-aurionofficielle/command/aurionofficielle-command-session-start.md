Configurer un hook de démarrage de session.

## Usage
`/hooks:session-start`

## Instructions

1. Définir les actions de démarrage de session :
   - Charger CLAUDE.md et PROGRESS.md
   - Vérifier l'état du projet (`npm run typecheck`)
   - Restaurer le contexte de la session précédente
   - Initialiser le suivi des métriques
   - Créer un snapshot de l'état initial

2. Configurer dans `.claude/settings.json` :
   ```json
   "SessionStart": [{
     "hooks": [{
       "type": "command",
       "command": "echo 'Session started' && npx tsc --noEmit 2>&1 | head -5"
     }]
   }]
   ```

3. Actions optionnelles :
   - Vérifier les env vars critiques
   - Charger la mémoire persistante
   - Afficher les TODO en cours
