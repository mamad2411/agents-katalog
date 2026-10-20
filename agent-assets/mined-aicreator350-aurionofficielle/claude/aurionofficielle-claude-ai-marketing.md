# AI Marketing — CLAUDE.md

## Outil
AI Marketing — Outil de création marketing avec canvas Fabric.js et AI.
URL : ai-marketing-xi.vercel.app

## Stack
- React 18 + TypeScript + Vite
- Fabric.js (canvas editing)
- Tailwind CSS
- AI text/image generation

## Fichiers clés
- `src/main.tsx` — Point d'entrée
- `App.tsx` — Application principale (4177 lignes — MONOLITHIQUE)
- `package.json` — name: aurion-ai-marketing

## Conventions
- TypeScript strict, zero `any`
- Pas de commentaires dans le code
- Auth : Clerk JWT via postMessage bridge

## Tech Debt
- `App.tsx` = 4177 lignes → à découper en modules
- Extraire : canvas controller, toolbar, templates panel, AI panel, export module

## Dev
```bash
cd tools-deploy/ai-marketing && npm run dev
cd tools-deploy/ai-marketing && npx vercel --prod --yes
```
