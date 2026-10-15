---
name: plan-and-confirm
description: >
  Explore the codebase, challenge the idea with a CTO-level critic, present a clear implementation plan,
  and wait for explicit user approval before writing any code. Use for any non-trivial change
  (new feature, bug fix, refactor). Launches parallel research agents. Rule #1 — never code without OKAY.
---

# Plan & Confirm — KLASSCI Frontend

## Options

Parse `$ARGUMENTS` for flags. **Default mode is FULL**.

| Flag | Short | Effect |
|------|-------|--------|
| `--quick` | `-q` | Skip critic + deep research, local explore only |
| `--no-issue` | `-ni` | Skip GitHub issue creation after OKAY |
| `--no-worktree` | `-nw` | Skip worktree creation |

Default (no flag) = FULL (critic + parallel research + issue + worktree).

---

## Phase 0 — CTO Critic (skip if `--quick`)

**Before exploring a single file, challenge the idea.**

Launch an Agent (`subagent_type: "general-purpose"`) with this role:

> You are a CTO reviewing a proposal. Your job is to protect the product, not be nice.
>
> THE PROPOSAL: {{task description}}
>
> Rules:
> 1. Never open with praise. Start with your highest-severity concern.
> 2. If fundamentally wrong, say "wrong approach entirely" and explain why.
> 3. If there's a better way, present it with concrete file references from this Next.js 15 + TanStack Query + Shadcn/ui codebase.
> 4. Check UX/ergonomics — suggest better alternatives if they exist.
> 5. Severity: BLOCKER / HIGH / MEDIUM / NOTE
> 6. State every assumption and whether it's SAFE / RISKY / WRONG.
>
> Format: [VERDICT: PROCEED / PROCEED WITH CHANGES / RETHINK / REJECT]
> Recommend: QUICK or FULL mode.

Present the critic's feedback verbatim. The user can debate (max 2 rounds).

---

## Phase 1 — Explorer & Recherche

### FULL mode (default): 3 agents en parallèle

**Agent 1 — `explore-codebase`**: trouver fichiers concernés, patterns existants, imports/exports affectés.

**Agent 2 — `explore-docs`** (Context7 MCP): documentation Next.js 15, TanStack Query v5, Shadcn/ui, Zod, NextAuth v5.

**Agent 3 — `websearch`**: best practices et solutions éprouvées.

### QUICK mode (`--quick`): explore locale

1. Lire les fichiers liés (pages, composants, hooks, schémas Zod)
2. Grep usages des symboles affectés
3. Identifier : `"use client"`, contraintes Zod, dépendances backend
4. Vérifier tests existants

**Règle : zéro modification de fichier.**

---

## Phase 2 — Présenter le plan

### Verdict du critique (FULL uniquement)
- Résumer le feedback CTO et les ajustements

### Ce que j'ai compris
- Références précises `fichier:ligne`
- Points ambigus signalés

### Ce que je vais faire
- Chaque fichier à modifier/créer avec justification
- Server Component vs Client Component pour chaque nouveau fichier
- Ce qui NE sera PAS modifié et pourquoi

### Recherche (FULL uniquement)
- Patterns trouvés dans le codebase
- Documentation/API pertinente
- Best practices et pièges à éviter

### Routing agent recommandé

| Type de tâche | Approche |
|---------------|----------|
| Bug simple (1-2 fichiers) | Fix direct |
| Bug complexe | Pattern `gsd-debugger` |
| Feature CRUD | `createCrudApi` + `createCrudHooks` + `CrudTable` + `CreateModal` |
| Nouveau composant | `/new-component` skill |
| Refactor multi-fichiers | Agent avec `isolation: "worktree"` |
| Tâches indépendantes | Agents parallèles |

### Points d'attention
- Code qui pourrait casser ailleurs
- Hypothèses faites et pourquoi
- Dépendances backend (endpoint existant ?)
- Breaking API changes, migrations

---

## Phase 3 — Attendre l'approbation

**STOP. Ne toucher à aucun fichier.**

```bash
curl -s -X POST "http://127.0.0.1:18789/hooks/agent" \
  -H "x-openclaw-token: 342f171b9e6b74f2eb63c8a1b41d9fdd381df7ff020d3ae8" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"📋 [\`$(basename $(pwd))\`] Plan prêt — en attente de ton OKAY ✅\", \"deliver\": true, \"channel\": \"last\"}" \
  > /dev/null 2>&1
```

> Merci de confirmer avec **OKAY** si la compréhension et le plan sont corrects.
> Sinon, dites-moi ce qui est inexact et je vais ajuster avant de coder.

**Règle absolue :** pas de OKAY = pas de code.

---

## Phase 4 — Issue + Worktree (skip si `--no-issue`)

### 4a. Créer l'issue GitHub
```bash
gh issue create --repo African-DC/klassci-college-frontend \
  --title "<type>(<scope>): <description>" \
  --body "<plan approuvé résumé>" \
  --label "<label>"
```

### 4b. Créer worktree (skip si `--no-worktree`)
```bash
git checkout develop && git pull origin develop
git checkout -b <type>/<issue>-<slug>
```

---

## Phase 5 — Implémenter (après OKAY + issue/worktree)

1. Implémenter exactement le plan approuvé — sans ajouts hors périmètre
2. Suivre le routing agent de Phase 2
3. Si découverte change le plan → **stopper et re-présenter**
4. Vérifier : `pnpm tsc --noEmit`
5. Résumer les changements `fichier:ligne`

**Ne jamais committer** sauf demande explicite → `/commit`.

---

## Phase 6 — Post-implémentation

1. Si le changement a un impact UI → proposer : `/visual-check <route>` pour vérifier avec dev-browser
2. Proposer `/commit` pour commit conventionnel
3. Proposer `/create-pr` avec `Closes #<issue>`
4. Après merge : cleanup branche

---

## Règles

- **Jamais de code sans OKAY** — règle #1
- **Le critique est obligatoire en FULL** — Phase 0 avant toute exploration
- **Le critique ne mâche pas ses mots** — jamais filtrer son feedback
- **L'utilisateur peut le contredire** — après débat, sa décision est finale
- Analyse basée sur fichiers lus — jamais de suppositions
- Changement trivial (typo) → suggérer `--quick` ou skip

$ARGUMENTS
