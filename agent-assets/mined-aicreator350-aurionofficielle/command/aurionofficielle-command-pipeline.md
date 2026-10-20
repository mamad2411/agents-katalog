Exécuter un pipeline SPARC multi-étapes.

## Usage
`/sparc:pipeline [analysis|refactor|test|optimize|deploy]`

## Pipelines disponibles

### analysis
1. Scanner la structure du projet
2. Identifier les problèmes (types, sécurité, perf)
3. Générer un rapport avec recommandations prioritisées

### refactor
1. Identifier les candidats au refactoring
2. Planifier les changements (fichiers monolithiques prioritaires)
3. Implémenter le refactoring avec tests
4. Vérifier la non-régression

### test
1. Analyser la couverture actuelle
2. Identifier les zones non testées
3. Générer les tests manquants
4. Exécuter la suite complète

### optimize
1. Profiler les performances (bundle, render, API)
2. Identifier les bottlenecks
3. Implémenter les optimisations
4. Mesurer l'amélioration

### deploy
1. Typecheck + lint + tests
2. Build (`npm run build`)
3. Déployer sur Vercel (`npx vercel --prod`)
4. Vérifier le health check
