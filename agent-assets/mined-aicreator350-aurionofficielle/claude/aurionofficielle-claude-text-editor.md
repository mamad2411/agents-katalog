# AURION TEXT EDITOR — CONTEXTE SPÉCIFIQUE

## URL
https://text-editor-aurion1.vercel.app

## ARCHITECTURE
- Entry : src/main.ts (2736 lignes — MONOLITHIQUE bootstrap, pas standard React)
- 190 fichiers .ts, ~873 KB total — le plus gros codebase par nombre de fichiers
- TipTap/ProseMirror avec 20+ extensions
- Collaboration : Y.js + WebrtcProvider P2P avec awareness cursors
- i18n : src/i18n/

## STRUCTURE src/
- components/ — composants UI
- agent/ — AI agent intégré
- ai/ — intégrations AI
- core/ — logique métier central
- extensions/ — extensions TipTap custom
- features.ts — features système
- lib/ — utilitaires
- styles/ — CSS

## API
api/agent.ts, api/ai.ts, api/collab-server.ts, api/mcp.ts, api/publish.ts, api/sync.ts

## FEATURES FONCTIONNELLES
- TipTap rich text avec 20+ extensions
- Kanban : drag-drop HTML5 DnD, moveKanbanTask()
- Databases : 4 vues (Table, Calendar, Gallery, Kanban) via initDbViewTabs()
- Comments : add/resolve/delete/reopen avec commentCountBadge
- Web Clipper, Emoji picker, Pomodoro timer
- Outbound webhooks : createWebhookEndpoint() avec X-Webhook-Secret
- Cloud storage : cloudSave/cloudLoad via authFetch + Bearer token
- Mentions utilisateurs

## TECH DEBT
- main.ts = 2736 lignes → monolithique, pas un composant React standard
- Pas de framework de routing

## TESTER
1. Ouvrir https://text-editor-aurion1.vercel.app
2. Créer un document → taper du texte
3. Tester Kanban → drag-drop
4. Console DevTools = zéro erreur
