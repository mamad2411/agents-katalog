# UIForge — CLAUDE.md

## Outil
UIForge — Éditeur de composants UI avec preview live et export de code.
URL : uiforge-eight.vercel.app

## Stack
- React 18 + TypeScript + Vite
- CodeMirror 6 (éditeur de code)
- Tailwind CSS
- Preview sandboxée (iframe)

## Fichiers clés
- `src/main.tsx` — Point d'entrée
- `src/CodeEditor.tsx` — Éditeur principal (2804 lignes — MONOLITHIQUE)
- `package.json` — name: aurion-uiforge

## Conventions
- TypeScript strict, zero `any`
- Pas de commentaires dans le code
- Research auto : `shouldResearch()` + `quickResearch()` + `injectResearch()`
- Auth : Clerk JWT via postMessage bridge

## Tech Debt
- `CodeEditor.tsx` = 2804 lignes → à découper en modules
- Extraire : éditeur, preview, panneau de props, toolbar

## Dev
```bash
cd tools-deploy/uiforge && npm run dev
cd tools-deploy/uiforge && npx vercel --prod --yes
```
