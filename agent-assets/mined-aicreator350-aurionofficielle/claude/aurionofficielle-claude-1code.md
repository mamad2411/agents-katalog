# Dev Pilot (1code) — CLAUDE.md

## Outil
Dev Pilot — IDE léger avec Monaco + WebContainer pour exécution de code directe.
URL : 1code-omega.vercel.app

## Stack
- React 18 + TypeScript + Vite
- Monaco Editor (VS Code engine)
- WebContainer (exécution côté client)
- xterm.js (terminal intégré)

## Fichiers clés
- `src/main.tsx` — Point d'entrée
- `OneCodeInterface.tsx` — Interface principale (6570 lignes — LE PLUS GROS MONOLITHE)
- `package.json` — name: aurion-dev

## Conventions
- TypeScript strict, zero `any`
- Pas de commentaires dans le code
- Research auto : `shouldResearch()` + `quickResearch()` + `injectResearch()`
- Auth : Clerk JWT via postMessage bridge + TOOL_AUTH_SECRET

## Tech Debt CRITIQUE
- `OneCodeInterface.tsx` = 6570 lignes → PRIORITÉ #1 à refactorer
- Extraire : éditeur Monaco, terminal, file tree, toolbar, settings panel, AI panel

## Gotchas
- CSRF token requis sur POST /api/tool-token (sinon silence 403)
- WebContainer ne fonctionne que sur Chrome/Chromium

## Dev
```bash
cd tools-deploy/1code && npm run dev
cd tools-deploy/1code && npx vercel --prod --yes
```
