# Aura — Cursor Rules

## Structure
- `api/` → Fastify backend (Node 20+, TypeScript strict)
- `web/` → Next.js 14 App Router (TypeScript strict, Tailwind)
- `app/` → React Native Expo (mobile, optionnel)
- `supabase/schema.sql` → source de vérité pour le schéma DB

## Règles de code

### Backend (api/)
- Toutes les routes auth utilisent `verifyAccessToken` preHandler
- Toutes les entrées validées avec Zod avant usage
- Aucune logique métier dans les routes : tout passe par des fonctions Postgres `SECURITY DEFINER`
- Jamais de secrets dans les logs (tokens, OTP, coordonnées GPS)
- Rate limiting sur endpoints sensibles

### Web (web/)
- Tokens JWT en `localStorage` (pour simplicité MVP)
- Jamais de logique côté client qui contourne le backend
- Tous les appels passent par `src/lib/api.ts`
- État global : Zustand avec `persist` + `partialize`

### Database
- Jamais d'appel Supabase direct depuis le web pour des writes
- RLS activé partout
- `cast_vote()`, `apply_promo_code()`, `claim_username()` sont les seuls chemins pour muter users/businesses

## Conventions
- Fichiers : camelCase pour utilitaires, PascalCase pour composants
- DB : snake_case
- Env : SCREAMING_SNAKE_CASE
- Import alias : `@/` → `web/src/` ou `api/src/`

## Valeurs à ne pas changer sans raison
- 200 pts/jour/user
- Vote ±10 à ±50
- Score business : start à 5000, légendaire ≥9000
- 1 vote / heure / business
- Ban auto : >5 votes/24h sur même cible
- Decay businesses non-inscrits : -20/jour
- Tile GPS : 2 décimales (~1km²), cache 24h
