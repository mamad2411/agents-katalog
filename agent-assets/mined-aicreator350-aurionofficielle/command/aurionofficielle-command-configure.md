Configurer et gérer les hooks actifs.

## Usage
`/hooks:configure [action]`

## Actions
- `list` — Lister tous les hooks configurés
- `enable [hook]` — Activer un hook
- `disable [hook]` — Désactiver un hook
- `test [hook]` — Tester un hook sans effet
- `reset` — Réinitialiser tous les hooks aux valeurs par défaut

## Instructions

1. Lire la configuration actuelle dans `.claude/settings.json`
2. Exécuter l'action demandée
3. Pour `list`, afficher :
   ```
   🔗 Hooks Configurés

   | Hook | Type | Matcher | Status | Commande |
   |------|------|---------|--------|----------|
   | PreToolUse | pre-edit | Write|Edit | ✅ | tsc --noEmit |
   | PostToolUse | post-edit | Write|Edit | ✅ | tsc && eslint |
   | PreCommit | pre-commit | * | ✅ | tsc && eslint |
   ```
4. Pour `test`, exécuter le hook en mode dry-run
5. Pour `reset`, restaurer la configuration par défaut Aurion
