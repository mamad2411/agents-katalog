Exécuter le pipeline d'optimisation performance.

## Usage
`/stream:optimize [cible]`

## Instructions

1. **Profiling** — Mesurer les performances actuelles :
   - Bundle size (Vite build)
   - Render time (React Profiler)
   - API latency (Vercel logs)
   - DB query time (Supabase)

2. **Identification** — Lister les optimisations possibles :
   - Code splitting non utilisé
   - Composants sans React.memo
   - Queries non mises en cache (React Query)
   - Images non optimisées

3. **Implémentation** — Appliquer les optimisations :
   - Lazy loading des routes
   - Memoization des composants lourds
   - Stale-while-revalidate pour les données
   - Compression des assets

4. **Mesure** — Comparer avant/après avec métriques
