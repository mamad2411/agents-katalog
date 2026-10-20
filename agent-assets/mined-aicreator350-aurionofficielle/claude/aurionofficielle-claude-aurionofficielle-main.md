# AURION STUDIO — CONTEXTE PERMANENT

## PROJET
SaaS AI — landing + dashboard + 9 outils actifs sur Vercel. URL : https://aurion.studio

### ⚠️ ÉTAT CRITIQUE — LIRE AVANT TOUTE ACTION
- **Score moyen outils : 4.4/10** — Voir `_AUDIT/` pour détails
- **3 bloquants** : UIForge API 404, 1code COEP cassé, Text Editor AI broken
- **Priorités** : Voir `_PLAN/01_PRIORITES.md`
- **Contexte par outil** : `_PLAN/[OUTIL]_CONTEXT.md`
- **NE PAS INVENTER DES FEATURES** — vérifier `_AUDIT/11_TOUT_CE_QUI_MANQUE.md`

### Outils (tools-deploy/) — 9 actifs
| Outil | Dossier | URL | Score |
|-------|---------|-----|-------|
| Chat AI | chat/ | chat-aurion1.vercel.app | 5.5/10 |
| Dev Pilot | 1code/ | 1code-omega.vercel.app | 5.2/10 |
| Agent Builder | agent-ai/ | agent-ai-cyan.vercel.app | 6/10 |
| Text Editor | text-editor/ | text-editor-aurion1.vercel.app | 4/10 |
| Studio | studio/ | studio-aurion1.vercel.app | 6.5/10 |
| UIForge | uiforge/ | uiforge-eight.vercel.app | 2/10 |
| Code Editor | code-editor/ | code-editor-aurion1.vercel.app | 3/10 |
| AI Marketing | ai-marketing/ | ai-marketing-xi.vercel.app | 5/10 |
| LSP Server | lsp-server/ | Docker/Railway | 2/10 |

### Outils à supprimer (recommandation audit)
- **Code Editor** : redondant avec Dev Pilot, regex highlighting seulement
- **LSP Server** : orphelin, aucun outil ne l'utilise
- **Cowork** : supprimé dans sessions précédentes

## STACK
- React 18 + TypeScript strict + Vite + Tailwind CSS (Studio = Next.js + pnpm)
- Vercel Edge Functions (api/*.ts) — 31 handlers, 19 shared modules in api/_lib/
- Supabase (PostgreSQL + Realtime + Storage + RLS) — 37 migrations
- Auth : Clerk → JWT → TOOL_AUTH_SECRET → postMessage bridge → Supabase RLS
- AI : OpenRouter → Gemini fallback → Ollama Cloud fallback
- Payments : Stripe (webhooks + credit packs)
- Credits : deduct_credits() atomic + lazy monthly reset, reconcile_credits() post-req

## COMMANDES
```bash
npm run dev                             # Landing + dashboard
npm run build                           # Build Vite
npm run typecheck                       # TSC strict
cd tools-deploy/[outil] && npm run dev  # Dev un outil
cd tools-deploy/[outil] && npx vercel --prod  # Deploy un outil
node scripts/deploy-all-tools.cjs       # Deploy les 11 outils
```

## RÈGLES
1. Zéro `any` TypeScript — strict mode
2. Pas de commentaires sauf si demandé explicitement
3. CSRF token (X-CSRF-Token) sur tous les POST auth'd — getCsrfToken() depuis src/lib/security/csrf.ts
4. Console Chrome = zéro erreur rouge
5. Lire PROGRESS.md au début, mettre à jour avant d'arrêter
6. Français quand l'utilisateur parle français
7. Scores honnêtes et brutaux, jamais gonflés

## ARCHITECTURE CRÉDITS
- user_credits : balance, monthly_allowance, bonus_credits, period_start/end
- deduct_credits() → lazy monthly reset → déduit → log
- reconcile_credits() → rembourse la diff estimé vs réel
- Plans : free=50K, creator=2M, pro=10M, enterprise=50M
- Webhook Stripe → update_monthly_allowance()
- 402 quand crédits insuffisants

## MCP SERVERS
| Serveur | Transport | Usage |
|---------|-----------|-------|
| blender | stdio (uvx) | 3D |
| paper | HTTP :29979 | UI design (HTML/CSS → screenshot → fix → export JSX) |
| figma | SSE mcp.figma.com | Design systems, fichiers Figma |

## FICHIERS CLÉS
- PROGRESS.md → état de chaque outil
- docs/ARCHITECTURE.md, docs/API.md, docs/DEPLOYMENT.md
- api/_lib/ → 17 modules partagés
- api/_handlers/ → 29 handlers
- supabase/migrations/ → 32 migrations

## GRAPH MEMORY
```bash
node .claude/graph-memory/engine.cjs recall "sujet" 2 5
node .claude/graph-memory/engine.cjs learn "Topic" "Insight" "source" 0.9
node .claude/graph-memory/engine.cjs journal "résumé" "tags"
```
Hook Stop auto : journal + decay 0.01

## SKILLS — 16 (dans .claude/skills/)
| Skill | Quand l'utiliser |
|-------|-----------------|
| react-best-practices | Composants React, hooks, performance |
| typescript-strict | Types, generics, strict mode |
| tailwind-aurion | Styling, design system Aurion |
| supabase-best-practices | DB, RLS, migrations, Edge Functions |
| clerk-auth | Auth flows, Clerk→JWT→Supabase bridge |
| stripe-best-practices | Paiements, webhooks, subscriptions |
| security-review | Audit sécurité, OWASP, XSS/CSRF |
| frontend-design | UI haute qualité, composants visuels |
| paper-design | Mockups UI via Paper MCP |
| web-design-guidelines | Audit UI, accessibilité |
| ai-orchestration | Multi-agent, routing AI, pipelines |
| graph-memory | Knowledge graph persistant |
| vercel-deployment | Deploy Vercel, Edge Functions |
| deploy-to-vercel | CLI deploy Vercel |
| vitest | Tests unitaires |
| webapp-testing | Tests E2E Playwright |

## SLASH COMMANDS — 30 (dans .claude/commands/)
```
/audit  /deploy  /fix  /progress  /research
/deploy:deploy-tool  /deploy:hotfix-deploy  /deploy:prepare-release
/dev:all-tools  /dev:code-review  /dev:create-ui-component
/dev:debug-error  /dev:fix-issue  /dev:refactor-code
/docs:architecture  /docs:doc-api
/memory:graph-recall  /memory:graph-learn  /memory:graph-journal  /memory:graph-stats
/performance:optimize-bundle-size  /performance:performance-audit
/project:create-feature  /project:health-check
/security:dependency-audit  /security:security-audit
/test:coverage  /test:e2e  /test:generate-tests  /test:write-tests
```

## AGENTS — 14 (dans .claude/agents/)
| Agent | Rôle |
|-------|------|
| architecture-auditor | Design patterns, structure système |
| code-auditor | Qualité code, détection bugs |
| test-engineer | Génération tests, couverture |
| development/frontend-developer | React, UI, responsive |
| development/backend-architect | API, Edge Functions, DB |
| development/react-pro | React avancé, hooks, perf |
| development/typescript-pro | TypeScript strict, types |
| development/ui-designer | Design system, composants |
| data-ai/ai-engineer | Pipelines AI, orchestration |
| data-ai/database-optimizer | Supabase, queries, RLS |
| quality-testing/code-reviewer | Review code, standards |
| quality-testing/debugger | Debug, stack traces |
| quality-testing/qa-expert | QA, test strategy |
| security/security-auditor | Audit sécurité, pentest |

## PRÉFÉRENCES
- Monochrome (#F2F2F2 bg, #0D0D0D text), coins 24px
- Serif Italic display (Newsreader), Sans body (Inter)
- Français quand l'utilisateur parle français
- Scores honnêtes et brutaux

## QUAND LES TOKENS S'ÉPUISENT
```
⚠️ PAUSE — ✅ Fait : [...] — 📍 Reprendre : [fichier] → [ligne] → [action]
```
