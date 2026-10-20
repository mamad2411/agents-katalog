# Architecture Documentation

Génère la documentation d'architecture du système.

## Instructions

1. **Vue d'ensemble système**
   - Diagramme des composants (landing, dashboard, 11 outils, API, DB)
   - Flux d'authentification : Clerk → JWT → TOOL_AUTH_SECRET → Supabase RLS
   - Flux de paiement : Stripe → Webhook → Credits
   - Flux AI : Client → API → OpenRouter/Gemini → Response

2. **Architecture par couche**
   - **Frontend** : React + Vite + Tailwind + Framer Motion
   - **API** : Vercel Edge Functions (api/_lib/ middleware stack)
   - **Database** : Supabase PostgreSQL (32 migrations, RLS policies)
   - **Storage** : Supabase Storage (fichiers utilisateurs)
   - **CDN** : Vercel Edge Network

3. **Architecture des outils**
   - Chaque outil = app React indépendante dans tools-deploy/
   - Auth bridge : postMessage entre landing et outil
   - Crédits : deduct → use → reconcile
   - Research : shouldResearch() → quickResearch() → injectResearch()

4. **Patterns d'architecture**
   - Feature-based modular architecture
   - Service layer (api calls) → Hook layer (business logic) → UI layer
   - Zustand stores pour le state complexe
   - React Query pour le cache serveur

5. **Output : docs/ARCHITECTURE.md**
   - Mermaid diagrams pour les flux
   - Tableaux pour les composants
   - Décisions d'architecture documentées
