---
name: documentation-manager
description: >
  Use when bootstrapping, completing, updating, or auditing project documentation,
  or documenting a feature/module/epic: AGENTS.md (or agents.md) + docs/, ADRs,
  roadmap, docs/features/<slug>/, docs/plans/<slug>/. Triggers: "document this project",
  "bootstrap docs", "sync docs", "audit docs", "docs vs code", "generate docs in test/",
  "from zero", "write ADRs", "document module", "new feature", "nueva feature",
  "plan feature", "promové el plan", /documentation-manager. Intents: integrate, audit,
  from-zero. Feature autopilot: plain "new feature X" → plan or pack without expert
  prompts. On conflict code wins. Mature repos default integrate after optional audit.
license: MIT
metadata:
  author: pedroknigge
  version: "1.3.0"
---

# Documentation Manager

Living project knowledge for humans and AI agents. **Code is the source of truth for *how* and for whether a claim is true.**  
**AGENTS.md + docs/** capture *what*, *why*, decisions, and plans — but **never override code** when they disagree.

## Core rules

1. Prefer **`AGENTS.md`** as the hub. If `agents.md` already exists, use it. If only `CLAUDE.md` exists, either extend it with a docs index or add `AGENTS.md` and cross-link — do not create three competing hubs.
2. Every generated/updated doc uses relative Markdown links back to the hub and related docs.
3. Never delete durable knowledge without a reason; prefer **Superseded by** notes on ADRs.
4. Do **not** auto-commit or auto-push. Leave git to the user.
5. Write generated content in the **user's language** (or the repo's dominant language). This skill body is English for ecosystem compatibility.
6. Prefer accuracy and usefulness over volume. Core set first; optional docs on demand.
7. **Intent first (project-level).** Classify **Intent**: `integrate` | `audit` | `from-zero` (and optional hybrid). See Step 0. **Not required** for pure feature/plan/sync.
8. **Code wins on conflict.** Doc claims that fail structural verification are marked Contradicted/Missing — do not invent code to match docs; fix or flag the doc.
9. **Integrate-first (when Intent=integrate).** Mature docs → index + gaps + canonical links; no parallel rewrite of product-vision/requirements/ADRs. See **adopt-integrate**.
10. **One authority per topic.** Each topic has one canonical doc; everything else links.
11. **Coverage matrix on adopt/from-zero project.** Product surfaces (nav, ModuleId, package) appear as documented / linked / gap.
12. **Feature atomicity.** One slug ≈ one ModuleId or bounded context. Clusters = **index** + **children**.
13. **Status taxonomy.** [references/status-taxonomy.md](references/status-taxonomy.md).
14. **Sandbox opt-in / first-class from-zero.** `Out: sandbox:path` when user asks (`test/`, etc.). Sandbox hubs banner non-SSOT + **promotion plan**.
15. **Feature autopilot (v1.3).** Plain “new feature X” / “documentá X” → skill chooses **plan** vs **feature pack**, applies default **non-writes**, writes files. User need not know layout or what not to touch. See [modes.md §3](references/modes.md#3-feature-autopilot--plan-v13).
16. **Plan mode (v1.3).** Greenfield feature ideas land in **`docs/plans/<slug>/`**, not a fake implementation pack and not a full project bootstrap. Promote to `docs/features/<slug>/` when code is real.

## Step 0 — Detect scope, mode, and Intent

**Scope** (required):

| Scope | When | Output focus |
|-------|------|--------------|
| **project** | Whole product / “docs for the project” | Hub + project docs (per Intent) |
| **feature** | Named feature/module **with code** (or refresh pack) | `docs/features/<slug>/` + hub link |
| **plan** | Named new feature / epic **before or without** solid code | `docs/plans/<slug>/` + hub link |
| **hybrid** | Feature/plan when no hub yet | Pack or plan + minimal hub |

**Mode** (required):

| Mode | Signals |
|------|---------|
| **bootstrap** | Greenfield, no hub/docs, or Intent **from-zero** on empty/thin |
| **adopt** | Code exists; docs thin/missing or Intent **integrate** |
| **audit** | “audit docs”, “docs vs code”, drift, validate claims |
| **plan** | “new feature”, “plan”, “epic”, “vamos a construir X” without code |
| **feature** | Document one feature/module that has (or is) code |
| **sync** | Diff / PR / update docs for a change |
| **roadmap** | Plan release / epic list refresh |

**Intent** (required for **project-level** work only):

| Intent | User signals (examples) | Behavior |
|--------|-------------------------|----------|
| **integrate** | “mejorar docs”, “ordenar”, “sync hub”, mature improve | adopt-integrate (or full if thin); optional pre-audit if drift suspected |
| **audit** | “auditar”, “¿las docs mienten?”, “docs vs code”, “validar paths” | Code inventory + claim matrix only (or then hand off) |
| **from-zero** | “toda nueva”, “de cero”, “generá docs en test/”, “full KB en carpeta X” | Full knowledge base; prefer **sandbox** if path given; code-inferred; old docs = hypothesis only |

**Inference (do not over-ask):**

- “nueva feature X” / “new feature X” / “quiero agregar X” → **Feature autopilot** (plan if no code, feature if code). Intent = n/a
- “generá toda la documentación en `test/`” → **Intent: from-zero | Out: sandbox:test/**
- Mature repo + “mejorá / integrá / indexá” → **Intent: integrate**
- “auditar docs” / “código vs docs” → **Intent: audit**
- Ambiguous **project** work with existing `docs/` → **ask once**: integrate | audit | from-zero
- Named single surface → **never** require the user to list non-writes or choose folders

**Maturity** (when relevant): thin | mixed | mature — see [modes.md](references/modes.md#2-adopt-project).

If scope/mode still ambiguous after inference, ask once. Load procedures from [references/modes.md](references/modes.md).

**Announce before writing:**

```text
Scope: <x> | Mode: <y> | Intent: <integrate|audit|from-zero|n/a> | Variant: <full|integrate|n/a> | Maturity: <…|n/a> | Out: <root|sandbox:path> | Slug: <slug|n/a>
```

When **integrate**, list **non-writes**. When **audit**, list matrix path and top contradictions. When **from-zero** + sandbox, include **promotion plan**. When **plan** or **feature**, list path + **default non-writes**.

## Recommended layout

```
project-root/
├── AGENTS.md
└── docs/
    ├── product-vision.md      # bootstrap / from-zero / adopt-full
    ├── requirements.md
    ├── architecture.md
    ├── roadmap.md
    ├── audit/                 # Intent audit (optional)
    │   └── claims-matrix.md
    ├── plans/<slug>/          # v1.3 plan mode (pre-code / epic)
    │   └── README.md
    ├── decisions/
    └── features/<slug>/       # code-backed feature packs
```

Supporting docs only when justified (except **from-zero**, which may create a full minimal core set).

### Artifact matrix (summary)

| Artifact | from-zero / bootstrap | integrate (mature) | audit | **plan** | feature | sync |
|----------|----------------------|--------------------|-------|----------|---------|------|
| Hub | create | extend / index | update status optional | link Plans | link | if needed |
| Core narrative docs | yes | **no rewrite** | no (read only) | **no** | **no** | if impact |
| Coverage matrix | yes | **required** | part of inventory | row optional | row | update |
| Claims matrix | optional pre | recommended if drift | **required** | n/a | scoped if audit | if drift |
| **Plans** `docs/plans/` | n/a | n/a | n/a | **required** | link if exists | if impact |
| Feature packs | key domains | gaps / entries | no (unless asked) | no (until promote) | **required** | if impact |
| Parallel full tree | sandbox ok | **forbidden** at root | n/a | n/a | n/a | n/a |

## Workflow (all modes)

1. **Step 0** — scope, mode, **Intent** (if project), maturity/variant, Out, slug.
2. **Discover code first** — tree, manifests, entry points, ModuleIds/routes/packages, sample tests. Then docs (if any). For named features, search that surface first.
3. If **audit** or docs exist and Intent is integrate/from-zero with suspected drift: run **reconciliation** ([modes.md § Audit](references/modes.md#6-audit-project), [audit-template.md](references/audit-template.md)).
4. **Plan files** — creates/updates **and** non-writes (defaults for feature/plan).
5. **Load templates** → write/edit → hub pass.
6. **Summary** — Intent/mode, files, non-writes, matrix stats, promotion notes. **No auto-commit.**

### Bootstrap / from-zero
Greenfield interview **or** code archaeology for brownfield from-zero. Full core set + hub. Sandbox if Out says so. See [modes.md](references/modes.md#1-bootstrap-project) and [§ from-zero](references/modes.md#7-from-zero).

### Adopt / integrate
Maturity → adopt-full or adopt-integrate. See [modes.md §2](references/modes.md#2-adopt-project).

### Audit
Code inventory → structural claims → matrix → report. **Code wins.** See [modes.md §6](references/modes.md#6-audit-project).

### Plan / Feature (v1.3 autopilot)
Named surface → **plan** (`docs/plans/<slug>/`) if no code / planning language; **feature** (`docs/features/<slug>/`) if code-backed. Default non-writes always. Promote plan → pack when implementation is real. See [modes.md §3](references/modes.md#3-feature-autopilot--plan-v13).

### Sync / Roadmap
Blast-radius sync; roadmap links plans for net-new work. See modes §4–5.

## Hub requirements

- Overview, nav links, agent instructions (read docs; update after significant work; ADRs; **code wins**), status line.
- Link **Plans** (`docs/plans/`) and **Features** (`docs/features/`) when present.
- Adopt / from-zero project: **Surface coverage** matrix.
- After audit: link to claims matrix if written.

Template: [agents-md-template.md](references/agents-md-template.md)

## Quality bar

Follow [quality-checklist.md](references/quality-checklist.md).

**Anti-snapshot:** no hardcoded table/route/endpoint counts.

## Templates & references

| File | Use |
|------|-----|
| [references/agents-md-template.md](references/agents-md-template.md) | Hub + coverage |
| [references/adr-template.md](references/adr-template.md) | ADRs |
| [references/plan-template.md](references/plan-template.md) | **Plan mode** (`docs/plans/<slug>/`) |
| [references/feature-readme-template.md](references/feature-readme-template.md) | Feature entry |
| [references/feature-cluster-template.md](references/feature-cluster-template.md) | Cluster index |
| [references/architecture-template.md](references/architecture-template.md) | Architecture |
| [references/status-taxonomy.md](references/status-taxonomy.md) | Status tokens |
| [references/audit-template.md](references/audit-template.md) | Claims matrix + verdicts |
| [references/modes.md](references/modes.md) | Full procedures |
| [references/quality-checklist.md](references/quality-checklist.md) | Done criteria |

## When NOT to use / defaults

- Pure code with no doc intent
- Throwaway notes outside the repo
- **Silent overwrite** of productive SSOT without Intent from-zero or explicit user order
- Mature improve without audit request → **integrate** (not full parallel tree)
- Replacing MkDocs/Docusaurus wholesale — integrate with it
- **New feature request** → do **not** run full project from-zero; use plan/feature autopilot

## Activation

Standalone or with coding skills. Suggest doc updates after significant architecture/product changes; ask before large narrative rewrites unless Intent is from-zero or audit-driven patch.

After shipping a coded feature that only had a plan, suggest **promote plan → feature pack**.
