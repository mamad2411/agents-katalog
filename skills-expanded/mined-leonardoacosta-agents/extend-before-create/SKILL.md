---
name: extend-before-create
description: >
  Search-first protocol for T3 Turbo monorepos. Before adding a new service, schema column,
  tRPC procedure, custom API endpoint, UI component, type, Zod schema, test file, query key,
  one-off script (seeder, mock, backfill, ops action), or doc — walk these decision trees first.
  Operationalizes the Reader Gate Iron Law (rules/CORE.md) with stack-specific search paths.
  Use when: (1) about to write `new`, `add`, or `create` anything, (2) starting a multi-file
  change, (3) any "what if we need X later" instinct fires.
  Triggers: new service, add endpoint, create component, new type, new schema, new test,
  new script, seeder, backfill, mock, ops script, new doc, add column, refactor, abstract,
  future-proof.
allowed-tools: Read, Glob, Grep, Bash
---


# Extend Before Create

> **North Star.** Reader Gate (rules/CORE.md Iron Law) establishes the principle:
> *"Reuse before reinvention. Search first. If a function, type, hook, component, or skill does
> the job — even imperfectly — extend, import, or compose it."*
>
> This skill is the **stack-specific playbook**: where to search, how to decide, when to defer.

## Effort Gates

Adaptive depth based on `${CLAUDE_EFFORT}` (v2.1.120+):

| Effort | Decision Trees To Walk |
|---|---|
| `low` | Primary decision tree only for the relevant domain (e.g. "is there an existing tRPC procedure that handles this?"). Skip the cross-domain trees and the conciseness audit. |
| `medium` and above | Full protocol — walk all relevant domain trees + atomic UI ladder + doc reuse + conciseness audit. |

Threshold rationale: low effort signals targeted single-domain lookup; full protocol is overkill. Medium and above is the safe default for any non-trivial change.

## Decision Default

For every domain below, the order is the same:

1. **Search** the canonical locations
2. **Extend** the lowest-friction match (add a parameter, a column, a variant)
3. **Compose** if extension would muddy the existing thing
4. **Defer to user** if no fit and the new thing is non-trivial — frame the trade-off, do not silently greenfield
5. **Create** only when reuse genuinely doesn't apply and the cost is approved

Defer-to-user is a real step. Do not skip it. Frame: *"Existing `<thing>` does X but not Y. Options: (a) extend `<thing>` with new param — risk Z; (b) new `<thing>` — duplicates A. Which?"*

---

## Reuse Ladder (climb before any domain tree)

The domain trees below search **in-repo** code first — but in-repo is only the second rung. Before
writing anything, climb the ladder and stop at the first rung that holds. The biggest over-builds
happen *above* the codebase: an agent reaches for a dependency (or hand-rolls a helper) for something
the platform already ships.

```
1. Needed at all?            → speculative: skip it, say so in one line (YAGNI — see §10)
2. Already in this codebase? → reuse the helper/util/type/component (the domain trees below)
3. Stdlib does it?           → use it (Intl, URLSearchParams, structuredClone, crypto, Array/Object methods)
4. Native platform feature?  → use it (<input type="date|color|email">, CSS over JS, a DB constraint over app code, HTTP caching headers over a cache layer)
5. Already-installed dep?    → use it — never add a NEW dependency for what a few lines or an existing dep covers
6. One line?                 → make it one line
7. Only then                 → the minimum new code that works
```

Rungs 3-5 are the ones the corpus's Reader Gate did not name explicitly. Concrete reaches: a date field is
`<input type="date">`, not a picker library; debounce/throttle and deep-clone are often a few lines
or already in `lodash`/`radash` if installed; date formatting is `Intl.DateTimeFormat`, not `moment`;
a uniqueness rule is a DB `unique` constraint, not app-layer dedup. Climb *after* you understand the
change (trace the real flow first) — the smallest diff in the wrong place is a second bug, not laziness.

Adopted from `DietrichGebert/ponytail` (MIT) — recon `docs/recon/ponytail.md`.

---

## 1. Service (Business Module)

**Before adding** `packages/api/src/services/<new-service>.ts`:

```bash
grep -rln "<verb><Noun>\|<noun><Verb>" packages/api/src/services/
grep -rln "ServiceCtx\|createServiceCtx" packages/api/src/
```

| If existing service… | Action |
| --- | --- |
| Handles same external system (Stripe, Better Stack, etc.) | **Extend ServiceCtx fn** — add a method to the existing factory |
| Handles same domain (badges, vendors, payouts) but different verb | **Add namespace fn** — `PaymentCheckout.forVendor` style (see `service-layer-style` § Namespace Factory) |
| Has overlap but genuinely different auth/transaction boundary | **Defer** — propose split-vs-extend trade-off |

Cross-ref: `service-layer-style` skill for ServiceCtx + Style A/B/namespace decision tree.

---

## 2. Schema (DB Column / Table)

**Before adding** new column or table to `packages/db/src/schema/`:

```bash
grep -rln "<entity>\|<related-noun>" packages/db/src/schema/
grep -rln "<existing-table>" packages/api/src/  # see all callers
```

| If existing schema… | Action |
| --- | --- |
| Has a column that could widen (text → jsonb, enum + new variant) | **Widen** — single migration, all callers keep working |
| Has a near-table joinable by FK | **Add column to existing** — avoid orphan join |
| Would require >5 query rewrites to extend | **Defer** — propose new-table cost vs widen cost |

Constraints: never `@deprecated` without approval (see `rules/CORE.md` § Breaking Changes). Cross-ref: `drizzle-best-practices`, `database-schema-designer-ext`.

---

## 3. Business Logic (tRPC Procedure)

**Before adding** new procedure in `packages/api/src/routers/`:

```bash
grep -rln "<verb>\.\(query\|mutation\)" packages/api/src/routers/
grep -rln "<noun>Router" packages/api/src/
```

| If existing procedure… | Action |
| --- | --- |
| Returns superset of what you need | **Use as-is** — filter on client, derive via selector |
| Returns subset — needs one more field | **Extend output** — add field to existing procedure |
| Takes nearly the same input | **Add optional input field** — discriminated union if behavior diverges |
| Has fundamentally different auth scope (public vs protected) | **Defer** — security concern, user decides split |

Cross-ref: `trpc-patterns`, `frontend-api-contracts`.

---

## 4. Endpoint (tRPC > Custom API)

**Default: tRPC.** Custom `/api/*` route handlers are reserved for these exceptions ONLY:

| Exception | Why |
| --- | --- |
| External webhook receivers (Stripe, Better Stack, GitHub) | Third party POSTs raw HTTP — they don't speak tRPC |
| File streaming (uploads, downloads, SSE) | tRPC over HTTP doesn't stream binary efficiently |
| OAuth callbacks | Provider redirects with query params, not RPC |
| Server-sent events / long polling | Out of tRPC's request/response model |
| Health checks consumed by infra (Vercel, k8s) | Must be plain HTTP `GET /health` |

If your case isn't on this list → **defer to user** before greenfield. Propose tRPC procedure as alternative.

---

## 5. UI (Atomic Ladder)

**Before building** a new component, walk the ladder bottom-up:

```
primitive (HTML / shadcn) → atom (packages/ui) → molecule → organism → template → page
```

```bash
# T3 atomic search
ls packages/ui/src/                               # atoms (Button, Input, Card)
find apps/nextjs/src/components -type d            # composite components
grep -rln "<feature>" packages/ui apps/nextjs/src/components
```

| Found at rung… | Action |
| --- | --- |
| **Atom** that almost fits | Extend atom with prop variant — shadcn `cva` is the right surface |
| **Molecule** with similar composition | Compose its atoms in a new molecule — don't fork the molecule |
| **Organism** with similar structure | Extract shared molecule, then build new organism on top |
| **Nothing fits at any rung** | Build at LOWEST rung that fits — atom if reusable, organism only if page-bound |

Defer trigger: visual divergence IS the design request (e.g., new brand surface). Cross-ref: `frontend-design` (see its `references/design-system-starter/README.md`), `shadcn`.

---

## 6. Types & Validation (Derive, Don't Declare)

**Before declaring** a new `interface` / `type` / Zod schema:

```bash
# Derive from existing
grep -rln "RouterInputs\|RouterOutputs\|\$inferSelect\|\$inferInsert" packages/api packages/db
grep -rln "z\.object\|z\.discriminatedUnion" packages/validators/
```

| Pattern | Always prefer |
| --- | --- |
| DB row type | `typeof <table>.$inferSelect` over hand-written `interface` |
| DB insert type | `typeof <table>.$inferInsert` |
| tRPC input | `RouterInputs['<router>']['<proc>']` |
| tRPC output | `RouterOutputs['<router>']['<proc>']` |
| New Zod schema | Extend existing via `.extend()` / `.merge()` / `.pick()` |
| Genuinely new external contract | **Defer** — confirm it's not tRPC-derivable first |

Banned: redeclaring DB row types or tRPC payload types in components. Cross-ref: `t3-code-patterns` § Type Ownership.

---

## 7. Tests (Case > File)

**Before creating** `tests/<new-feature>.spec.ts`:

```bash
find tests -name '*.spec.ts' | xargs grep -ln '<feature>\|<related-feature>'
ls tests/fixtures/                                 # check shared fixtures
```

| If existing test file… | Action |
| --- | --- |
| Covers same user journey | **Add `test()` case** — keep journey tests cohesive |
| Covers adjacent journey | **Extend describe block** with new it() if shared setup applies |
| Has fixture you can reuse | **Import fixture** — never re-create test data |
| Doesn't exist for this journey | **New file** — but only after confirming journey is genuinely new |

Defer trigger: test would force a new test runner config / new browser context. Cross-ref: `test-driven-development`, `playwright-auth`.

---

## 8. State & Cache (Extend Key Tree)

**Before adding** a new query key, atom, or store slice:

```bash
grep -rn "queryKey\|atomFamily\|createStore" packages/api/src apps/nextjs/src
```

| If existing tree… | Action |
| --- | --- |
| Has a parent key (`['trades', 'list']`) | **Extend with child** (`['trades', 'list', { vendorId }]`) |
| Has an atom you can derive from | **Use selector** (`useAtomValue(selectAtom(parent, fn))`) |
| Genuinely independent concern | **New key** — but verify it doesn't shadow existing key prefix |

Cache invalidation note: extending the tree means your invalidations cascade correctly. Forking creates orphan caches. Cross-ref: `state-handling`, `trpc-patterns`.

---

## 9. Documentation (Reuse + Conciseness)

The most over-created domain. Two protocols apply.

### 9a. Reuse Protocol

| Before adding… | Search | Extend by |
| --- | --- | --- |
| New `README.md` section | `git grep -l "<topic>" -- '*.md'` | Adding to existing section |
| New `openspec/specs/` capability | `ls openspec/specs/` | Adding `## ADDED Requirements` to existing capability |
| New `design.md` next to tasks.md | Touches 3+ loosely-coupled systems? | If no — skip the design doc, tasks.md is enough |
| New code comment | Self-document via better naming first | Comment WHY, never WHAT |
| New ADR | `ls docs/decisions/` | Append to existing ADR if same domain |
| New `CHANGELOG.md` entry | n/a | Auto-generated by `/project:changelog` — never write manually |

**Hard rule from `rules/CORE.md` § File Placement:** NEVER create `*.md` in project root unless explicitly requested. New docs go in `docs/`.

### 9b. Conciseness (when you must write new)

See `CLAUDE.md` § Communication Style for the canonical voice rules (tables > prose, density gradient, imperative voice, etc.). This skill adds two doc-specific bullets that aren't in CLAUDE.md:

- **One question per section** — split or kill if it answers two
- **Delete drift on sight** — docs that say things the code doesn't are worse than no docs

Cross-ref: `crafting-effective-readmes` and any repository-local writing guidance.

---

## 10. Abstraction (YAGNI / Defer)

**Before solving "what if":**

| Question | Action |
| --- | --- |
| Does the spec literally ask for this generality? | **Yes** → proceed |
| | **No** → DEFER to user. Frame: *"Spec asks for X. I could solve only X (simpler), or X+Y+Z (handles future cases). Which?"* |

**Banned phrases** (treat as YAGNI drift — defer to user):
- "future-proofing"
- "what if we need to..."
- "make it generic in case..."
- "while we're here, let's also..."
- "this should be configurable"

The cost of speculative generality always exceeds the cost of refactoring later. The agent does not know what the user will need next; the user does.

---

## 11. Scripts (One-Off / Ops)

**Before creating** a domain script (`apps/scripts/src/<new>.ts`):

```bash
ls apps/scripts/src/                             # centralized home — extend a sibling first
sed -n '/inventory/,/^$/p' apps/scripts/README.md 2>/dev/null   # inventory table (name -> purpose -> env)
ls <repo>/scripts/                                   # root — pure infra ONLY (no workspace imports)
```

| If new script needs… | Place at |
| --- | --- |
| ANY workspace import — `@{ws}/db`, `@{ws}/api`, services, drizzle (seeder / backfill / mock / ops) | `apps/scripts/src/<name>.ts` — extend existing siblings first |
| Pure infra (cron diagnose, config parse, lint tooling), NO workspace internals | `<repo>/scripts/<name>.ts` (legitimate root case) |
| e2e suite infrastructure (fixtures, storage-state seeders) | `packages/e2e/scripts/` — suite infra, not a domain script |
| Anything else | **Defer** — extend an existing surface vs propose a new package |

Wire it: `"<name>": "pnpm with-env tsx src/<name>.ts"` in `@{ws}/scripts`, delegated from root as
`"scripts:<name>": "pnpm --filter @{ws}/scripts <name> --"` (invoke `pnpm scripts:<name>`).

Banned: root `scripts/foo.ts` importing `@{ws}/db` schemas — pnpm doesn't hoist workspace
internals across boundaries; resolution fails or requires `createRequire()` fragility. Such
scripts belong in `apps/scripts`. (The former co-location home, `packages/db/src/scripts/`,
is the migration source under `standardize-fleet-scripts-package` — not a destination for new work.)

Defer trigger: script doesn't fit `apps/scripts` AND isn't pure infra → don't fall back to
root `scripts/` as a default. Ask whether to extend an existing surface or create a new package.

Cross-ref: `t3-code-patterns` § Script Placement (full package shape, wiring template, turbo
criterion, env prefix, anti-patterns).

---

## Worked Example — Service Domain

Spec: *"Add Stripe payout retry logic for failed Connect transfers."*

Tempting: create `packages/api/src/services/payouts/retry.ts` (new file).

**Search first:**

```bash
grep -rln "payout\|transfer" packages/api/src/services/
# → packages/api/src/services/payouts/index.ts (existing PayoutService)
```

**Decision:** PayoutService already handles transfer creation. Same external system (Stripe), same domain (payouts), needs new verb (retry).

**Action:** Extend ServiceCtx fn — add `retryFailedTransfers(ctx, transferId)` method to existing factory.

**Defer trigger:** None — extension is one method on existing factory. No new file needed.

The pattern: search → match domain → extend lowest-friction surface. The new file you almost created becomes a 20-line method on a service that already exists.

---

## NEVER (Consolidated)

- NEVER create `*.md` in project root (CORE.md § File Placement)
- NEVER write `CHANGELOG.md` manually — auto-generated by `/project:changelog`
- NEVER redeclare DB row types or tRPC payload types in components — derive from `$inferSelect` / `RouterOutputs`
- NEVER reach for `/api/*` route handlers outside the §4 exception list — defer first
- NEVER speak the banned phrases: *"future-proofing"*, *"what if we need to..."*, *"make it generic in case..."*, *"while we're here..."*, *"this should be configurable"*
- NEVER `@deprecated` without explicit user approval (CORE.md § Breaking Changes)
- NEVER fork a molecule when extending atoms would compose the same surface
- NEVER fork a query key tree — creates orphan caches that don't invalidate
- NEVER create `<repo>/scripts/*.ts` that imports workspace internals (`@{ws}/db`, `@{ws}/api`) — place script in the owning package's `src/scripts/` instead (see §11)
- NEVER greenfield silently — defer with two named options when reuse genuinely doesn't fit

---

## When To Defer (Explicit Triggers)

You MUST defer to the user — not silently create — when ANY of these fire:

- Reuse genuinely doesn't fit AND the new thing crosses a package boundary
- Extension would require >5 caller updates
- Auth/security scope differs between old and new
- New thing duplicates >50% of existing thing's surface
- You catch yourself solving a problem the spec doesn't have
- The decision feels load-bearing for the architecture

Frame the defer as **two named options** with explicit trade-offs. Never "should I X?" — always "X has cost A, Y has cost B, which?".

---

## Templates (portable canon)

This skill ships reusable templates that downstream T3 Turbo repos vendor in.
Templates live in `~/.claude/skills/extend-before-create/templates/` and target
repos copy them into their working trees per the install doc.

| Template | Purpose | Anti-pattern source | Install doc |
| --- | --- | --- | --- |
| `ci-template.yml` | Canonical GitHub Actions CI workflow (lint/format/typecheck/test/build/fallow/e2e) | A2 — Missing CI / `ignoreBuildErrors: true` (CRITICAL, 5 repos) | `ci-install.md` |
| `pre-commit-block-doc-rot.sh` | Pre-commit hook rejecting `*_SUMMARY.md`, root `test.js`, `*.bak`, `*.log` | A6 — Doc rot + root junk (HIGH, 4 repos) | inline header docstring |
| `pre-commit-block-ts-migrations.sh` | Pre-commit hook rejecting hand-written `.ts` migration files | A8 — Hand-written `.ts` migration files (MEDIUM, 1 repo) | inline header docstring |

Companion ESLint rule templates live under `~/.claude/skills/t3-code-patterns/templates/eslint-rules/` — see that skill's README for the full catalog (service-layer rules + audit-driven rules + canon rules like `no-restricted-imports`).

Update protocol: edit the canon copy here, then each downstream repo pulls the diff manually (the rules are short; periodic search-and-replace across the fleet keeps the canon in sync).

---

## Understanding Dependency Internals (opensrc)

The Reader Gate's first question is "does code already exist that solves this?" — but you can't
reuse what you can't read. Type signatures (`.d.ts`) tell you the *interface*; they rarely tell
you whether a dependency already does the thing you're about to rebuild.

When you need a dependency's **implementation**, not just its types, fetch its source with
`opensrc` (zero install — `npx`). The CLI is subcommand-based:

```bash
npx opensrc fetch zod              # npm package
npx opensrc fetch pypi:requests    # Python package
npx opensrc fetch crates:serde     # Rust crate
npx opensrc fetch vercel/ai        # GitHub repo (owner/repo)
npx opensrc path zod               # print the cached source path (fetches on miss)
npx opensrc list                   # list everything cached
```

Source lands in a **global cache** at `~/.opensrc/` (e.g. `~/.opensrc/repos/github.com/colinhacks/zod/4.4.3`),
not a project-local dir — so there is nothing to gitignore per-project. Resolve a path with
`opensrc path <pkg>`, read it, then decide reuse-vs-build with full information. This
operationalizes `rules/CORE.md` Iron Law § Reader Gate ("Reuse before reinvention"): prefer
reading the real source over guessing from types or memory.
Source / adoption verdict: `docs/recon/vercel-labs-ai-cli.{md,html}` (verified against
`opensrc` CLI 2026-06-03 — the bare `npx opensrc <pkg>` form in the upstream repo's AGENTS.md is
stale; current CLI requires the `fetch` subcommand).

---

## Cross-References

| Domain | Skill |
| --- | --- |
| Service decisions | `service-layer-style` |
| Schema design + migration safety | `drizzle-best-practices`, `database-schema-designer-ext` |
| tRPC procedure design | `trpc-patterns`, `frontend-api-contracts` |
| Atomic UI patterns | `frontend-design` (`references/design-system-starter/`), `shadcn` |
| Type ownership | `t3-code-patterns` § Type Ownership |
| Script placement (full wiring) | `t3-code-patterns` § Script Placement |
| Test discipline | `test-driven-development` |
| State patterns | `state-handling` |
| Doc style | `crafting-effective-readmes`, plus repository-local writing guidance |
| Code reuse mechanics | `simplify` |

This skill operationalizes `rules/CORE.md` Iron Law § Reader Gate. The Iron Law is the gate; this skill is the playbook.
