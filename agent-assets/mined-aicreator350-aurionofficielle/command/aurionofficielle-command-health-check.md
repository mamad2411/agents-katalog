# Project Health Check

Analyse complète de la santé du projet.

## Instructions

1. **Build Status**
   - `npm run build` → succès ?
   - `npm run typecheck` → zero erreurs ?
   - `npm audit` → vulnérabilités critiques ?

2. **État des outils (11)**
   - Pour chaque outil dans tools-deploy/ :
     - `cd tools-deploy/[outil] && npm run build` → succès ?
     - Dernière modification des fichiers clés
     - Taille du bundle

3. **Database**
   - Nombre de migrations : `ls supabase/migrations/ | wc -l`
   - Dernière migration appliquée
   - Tables critiques : user_credits, profiles

4. **API**
   - Nombre d'endpoints dans api/
   - Health check : GET /api/health
   - Endpoints sans tests

5. **Code Quality Metrics**
   - Fichiers > 500 lignes (tech debt)
   - Nombre de `any` dans le codebase
   - Nombre de `// @ts-ignore`
   - Dépendances outdated

6. **Documentation**
   - PROGRESS.md à jour ?
   - docs/API.md couvre tous les endpoints ?
   - CLAUDE.md reflète l'état actuel ?

7. **Rapport santé**
   | Catégorie | Score /10 | Détails |
   |-----------|-----------|---------|
   | Build | X | ... |
   | Sécurité | X | ... |
   | Performance | X | ... |
   | Code Quality | X | ... |
   | Documentation | X | ... |
