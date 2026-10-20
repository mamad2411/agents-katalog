# AURION AGENT BUILDER — CONTEXTE SPÉCIFIQUE

## URL
https://agent-ai-cyan.vercel.app

## ARCHITECTURE
- Entry : src/main.tsx → src/App.tsx (814 lignes) — bien structuré
- 42 fichiers .tsx, ~421 KB total
- Canvas : src/components/aurora/auroraCanvas.tsx (ReactFlow)
- Execution Engine : src/lib/execution-engine.ts (1834 lignes)
- Connectors : src/lib/connectors.ts (~1600 lignes, 99 connectors)
- Credential Vault : src/lib/credential-vault.ts (AES-256-GCM + PBKDF2)
- OAuth : src/lib/oauth-manager.ts + api/oauth-callback.ts
- Store : src/store/ (Zustand)

## API
api/chat.ts, api/cron.ts, api/cron-trigger.ts, api/health.ts,
api/marketplace.ts, api/mcp.ts, api/oauth-callback.ts, api/send-email.ts,
api/sync.ts, api/webhooks.ts, api/webhook/[id].ts,
api/agent/, api/cron/, api/studio/

## FEATURES FONCTIONNELLES
- Canvas ReactFlow drag-and-drop avec 8 types de nœuds (tool, router, loop, ai, input, output, condition)
- 99 connectors avec fetch() réels vers APIs tierces
- OAuth2 complet : popup → callback → token exchange → storeCredential AES-256-GCM
- Cron : Vercel cron daily + agent_cron_jobs table Supabase
- Exécution parallèle : Promise.allSettled()
- Background execution : bouton "BG" → POST /api/cron-trigger
- Cloud storage : agentCloudSave/Load via authFetch → Supabase Storage
- Marketplace templates
- Notifications : MSTeams, Postmark, Resend, Zapier/Make/n8n, GitLab, Pushover, PagerDuty, WhatsApp

## TESTS
- Répertoire tests/ avec Playwright config
- Scripts : test, test:ui, test:headed, test:debug

## TESTER
1. Ouvrir https://agent-ai-cyan.vercel.app
2. Créer workflow → HTTP GET jsonplaceholder.typicode.com/posts/1
3. Execute → vérifier résultat réel
4. Console DevTools = zéro erreur
