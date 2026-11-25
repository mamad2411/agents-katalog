---
name: repo-guides
description: >-
  First-time knowledge setup for a repository: survey the stack, generate the
  curated guide tree under .agentic/guides/, and wire the AI entrypoint
  (AGENTS.md plus a CLAUDE.md shim). User-triggered only. Invoke when the user
  says "repo guides", "set up repo guides", "generate the guides", "bootstrap
  this repo for AI", "agentic init", "create AGENTS.md", or "wire the AI
  entrypoint". On a brownfield repo, run repo-audit-guides first and feed its
  "# Repo Knowledge Audit" in here. Writes tracked files (blast radius R2) —
  no writes happen until the user approves the plan.
  Not for: ongoing guide-drift sync after merges (the guide-sync agent), read-only readiness audits (repo-audit-guides), or authoring application code.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, Agent, Skill
---

# repo-guides

One-time onboarding that turns a repository into a knowledge base coding agents can read. You survey the repo, get user sign-off on a plan, render a curated guide tree under `.agentic/guides/`, and idempotently connect it to the project's assistant entrypoint.

> `.agentic/guides/` is the single source of guidance consumed by every agentic-sdlc skill and agent. Do not create a parallel doc tree. Everything you generate lands here or in the entrypoint files.

## Blast radius

R2 — you write tracked repo files (the guide tree and the entrypoint) plus one R1 run-artifact (the local run journal). No R3 external side-effects: no git operations, no network, no tooling install. Every write is gated behind explicit user approval.

## When to use

- User is bootstrapping a repo for AI-assisted work and asks for repo guides / an entrypoint.
- Trigger phrases: "repo guides", "set up repo guides", "agentic init", "create AGENTS.md", "wire the AI entrypoint".

Run the **repo-audit-guides** skill (R0, read-only) FIRST on any brownfield repo. It emits the `# Repo Knowledge Audit` this skill consumes. On a truly empty/greenfield repo you may proceed without an audit, but the halt conditions below still apply.

## Inputs

| Input | Source | Required |
|---|---|---|
| Audit report | repo-audit-guides output, marker `# Repo Knowledge Audit` | brownfield: yes |
| Repo signals | manifests, `git remote -v`, `git log --oneline -10`, `.pre-commit-config.yaml`, CI files, `Makefile`, `pyproject.toml`, `package.json`, `tox.ini`, `setup.cfg` | detected, not asked |
| User decisions | plan approval, per-file entrypoint diffs, gate/adapter confirmations | interactive |

> Detection before prompt, everywhere. Read the repo before you ask a question; only ask about what detection cannot resolve.

## Audit contract (consumed)

The report carries marker `# Repo Knowledge Audit` and these sections: `Where the docs live`, `How usable the docs are`, `Assistant instruction files`, `Agents, skills and hooks`, `Where they disagree`, `Ready to plant?`, `Evidence`. Per-item verdict vocabulary: `preserve` / `incorporate` / `merge` / `replace` / `skip` / `ask` / `halt`.

## Operating flow

Seven phases. Each lazy-loads its own reference doc. Nothing is written before Phase 2 approval.

| Phase | Action | Reference | Gate |
|---|---|---|---|
| 1 | Survey + consume audit; detect stack; classify existing docs. No writes. | `references/survey.md` | halt conditions |
| 2 | Propose the guide plan. | `references/plan-and-generate.md` | **HARD user approval** |
| 3 | Render the guide set + Steps A–D (config files). | `references/plan-and-generate.md`, `references/writing-guides.md`, `references/templates/` | — |
| 4 | Merge managed regions into the entrypoint(s). | `references/entrypoint-wiring.md`, `references/templates/` | per-file diff approval |
| 4A | Add `.agentic/runs/` to `.gitignore`. | — | ask if tracked |
| 5 | Run ~14 validation checks. | — | ask on failure |
| 6 | Write the run journal. | — | local-only |
| 7 | Handoff prompt. | — | user choice |

### Phase 1 — survey

Load `references/survey.md`. Consume the audit (or run the survey directly on greenfield). Establish tech-stack confidence and the doc map. Write nothing.

**Halt before Phase 2 if ANY of these hold:**

- tech-stack confidence < 80%
- audit verdict recommends `halt`
- unresolved `conflicting` evidence affecting generation, commands, or wiring
- no AI-tool signals AND the user will not pick a target entrypoint
- repo is empty (no manifests, no source)

### Phase 2 — plan (hard gate)

Load `references/plan-and-generate.md`. Propose which guides you will write, the entrypoint target(s), and the config files. Then STOP. Proceed only on explicit approval — `approve` / `yes` / `go`. Customize loops are allowed; `cancel` halts with zero writes. No file is touched before this gate clears.

### Phase 3 — generate

Load `references/plan-and-generate.md` for orchestration and `references/writing-guides.md` for craft rules. Render each planned guide from its template under `references/templates/guides/<area>/<name>.md.template` to the fixed output path.

**Guide set — output paths are a fixed contract:**

| Template | Output |
|---|---|
| `references/templates/guides/api/api-patterns.md.template` | `.agentic/guides/api/api-patterns.md` |
| `references/templates/guides/architecture/architecture.md.template` | `.agentic/guides/architecture/architecture.md` |
| `references/templates/guides/data/database-patterns.md.template` | `.agentic/guides/data/database-patterns.md` |
| `references/templates/guides/development/development-practices.md.template` | `.agentic/guides/development/development-practices.md` |
| `references/templates/guides/integration/external-integrations.md.template` | `.agentic/guides/integration/external-integrations.md` |
| `references/templates/guides/security/security-practices.md.template` | `.agentic/guides/security/security-practices.md` |
| `references/templates/guides/standards/code-quality.md.template` | `.agentic/guides/standards/code-quality.md` |
| `references/templates/guides/standards/git-workflow.md.template` | `.agentic/guides/standards/git-workflow.md` |
| `references/templates/guides/testing/testing-patterns.md.template` | `.agentic/guides/testing/testing-patterns.md` |

> `testing/` is seeded here but owned going forward by **qa-baseline** — do not fight it for that subtree after handoff. `integration/ticket-flow.md` (Step D, below) is read by the ticket-sync hook and is separate from `integration/external-integrations.md`.

**Steps A–D — schema-strict config files (same generation phase):**

- **A — `.agentic/guides/project.md`.** Exactly five sections: `## Project Identity`, `## Work Item Tracker`, `## Work Item Adapter`, `## Source Control And Review`, `## Review Adapter`. `## Work Item Adapter` allows ONLY `**Status**`, `**Adapter**`, `**Lookup**`, `**Create**`, `**Output**` — `**Underlying command**`, `**Multi-turn follow-up**`, `**Notes**` are schema violations. `## Review Adapter` fields: `**Status**`, `**Adapter**`, `**Instructions**`, `**Body Template**`. `**Status**` values: `configured | not configured`. Review artifact type: `MR | PR`. Keep project.md schema-pure.
- **B — `.agentic/guides/standards/git-workflow.md`** (also a guide-set member). Required sections: Branch Naming Convention, Commit Message Format, Merge Strategy, Anti-Patterns, Troubleshooting — real project keys substituted for placeholders.
- **C — `.agentic/guides/quality-gates.md`.** One `###` per gate, ordered fastest-to-slowest. Per gate: **Run**, **Pass**, **Fail**, optional **Auto-fix**, optional **Skip if**.
- **D — `.agentic/guides/integration/ticket-flow.md`** (optional). Runs ONLY when project.md carries `**Status**: configured` in the Work Item Adapter; otherwise silent skip — the hook is a no-op without the file. User decline ⇒ no file, logged in the Phase 5 report.

**quality-gate candidate resolution** — for each type (lint, format, type-check, test, secret-scan, license-check, static-analysis): 1 candidate ⇒ confirm yes/no/modify; multiple ⇒ propose the best (prefer `Makefile` targets over raw tool commands) and let the user choose.

**Ticket adapter prompting** — read `ticket_detection.provider` / `ticket_detection.key_prefix`. Prompt only when `confidence` is `low`/`none`. Emit `not configured` only when `ticket_detection.adapter_source === "none"` and the user offers no correction. High confidence ⇒ confirm the pre-filled values.

**ticket-flow.md schema** (source of truth `${CLAUDE_PLUGIN_ROOT}/references/ticket-flow.md`). Required fields: `**Adapter invocation**` (adapter command carrying a `{message}` placeholder), `**Known states**`, `**Action message template**` (default `"Transition ticket {ticket_id} to status {state}, then tell me the current status of the ticket."`), and a `**Transitions**` table (forward-only, in workflow order). Plus `**Status**`, `**Adapter**`, `**Workflow source**`, `**Timeout**: 120`. The hook re-parses on every fire. Default state mapping: a "dev / in progress"-like state ← event `phase.completed phase=2`; a "review"-like state ← `work_item.linked_artifact kind=mr`; no match ⇒ ask explicitly. `feature.verified` is an example extension event.

**Content / craft rules** (from `references/writing-guides.md`):

- Placeholder contract: `[NAME]` = required, fill it; `[NAME?]` = drop the whole row if unknown. No bracketed placeholder may survive to Phase 5.
- Practices over code dumps; contrast tables (bad vs. best); `file:line` references to real code.
- Hard size max, no minimum, no filler padding.

**Monorepo generation** — dispatch one subagent per module in a single message for parallelism; each writes to its own module's `.agentic/guides/`. Use `superpowers:brainstorming` (Phase 2 shaping) and `superpowers:dispatching-parallel-agents` (Phase 3 fan-out) only if the host exposes them; otherwise fall back to native subagents with `subagent_type: "general-purpose"`.

> Drift redistribution — route each fact to its home: branch/commit/merge conventions → git-workflow guide; exact commands → quality-gates guide; agent routing → entrypoint managed regions; ownership → architecture guides. project.md stays schema-pure.

### Phase 4 — entrypoint wiring

Load `references/entrypoint-wiring.md`. `AGENTS.md` is the canonical generated entrypoint; `CLAUDE.md` becomes a minimal shim that imports it via `@AGENTS.md` — never duplicate tables, classifiers, or command lists across the two.

Merge only inside managed regions delimited by matching `start`/`end` marker pairs. Content outside those regions is untouchable. With multiple entrypoint targets, show one diff and take one approval **per file** — never bulk-approve. Always show the diff first.

### Phase 4A — gitignore

Add `.agentic/runs/` to `.gitignore`. If a `.agentic/runs/<branch>.json` is already tracked, never remove it silently — ask about untracking.

### Phase 5 — validate

Run the checks; on any failure, list them and ask the user. Never silently auto-fix.

- guides ≤ 400 lines; entrypoint ≤ 300 lines
- no `[PLACEHOLDER]` / `[PLACEHOLDER?]` remains
- `git check-ignore -v .agentic/runs/` resolves
- project.md Work Item Adapter carries no forbidden fields (schema check)
- reject filler tokens `Review reminder`, `Foundation reminder`, `Operating reminder`
- every Adapter value is a skill/MCP invocation, not an internal CLI — grep for `--` flags and binary paths (e.g. `assistants chat`) and reject them
- managed regions have matching `start`/`end` marker pairs

### Phase 6 — run journal

Write `.agentic/runs/<branch>.json` (R1, local-only state; never present it as a commit artifact; remove on request after the report). Fields:

```json
{
  "step": "00",
  "agent_skill": "repo-guides",
  "primitive": "skill",
  "started_at": "...",
  "completed_at": "...",
  "status": "completed",
  "outcome": "...",
  "artifacts": ["..."],
  "next_step": "sdlc-guided or story-author"
}
```

### Phase 7 — handoff

Offer the next step (yes/no/other). Point the user at `sdlc-guided` or `story-author`.

## Outputs

| Path | Meaning |
|---|---|
| `.agentic/guides/` | guide-tree root (single source of guidance) |
| `.agentic/guides/<category>/<file>.md` | the nine content guides |
| `.agentic/guides/project.md` | project identity + adapters (five-section schema) |
| `.agentic/guides/standards/git-workflow.md` | git conventions |
| `.agentic/guides/quality-gates.md` | ordered quality gates |
| `.agentic/guides/integration/ticket-flow.md` | ticket state-sync config (optional; read by ticket-sync hook) |
| `.agentic/runs/<branch>.json` | run journal (local-only) |
| `.gitignore` | gains `.agentic/runs/` |
| `AGENTS.md` | canonical entrypoint |
| `CLAUDE.md` | shim importing `@AGENTS.md` |

## References tree

| File | Loaded at | Purpose |
|---|---|---|
| `references/survey.md` | Phase 1 | repo survey, stack detection, audit consumption |
| `references/plan-and-generate.md` | Phases 2–3 | plan the guide set, orchestrate generation |
| `references/writing-guides.md` | Phase 3 | craft rules for guide content |
| `references/entrypoint-wiring.md` | Phase 4 | managed-region merge into the entrypoint |
| `references/templates/guides/<area>/<name>.md.template` | Phases 3–4 | nine guide templates (paths above) |
| `${CLAUDE_PLUGIN_ROOT}/references/ticket-flow.md` | Phase 3-D | ticket-flow schema source |

## Cross-references

- **Consumes:** repo-audit-guides audit report (`# Repo Knowledge Audit`).
- **Feeds:** `sdlc-guided` and `story-author` (handoff via `next_step`); `story-intake` and `story-author` read `## Work Item Adapter`; MR/PR skills read `## Review Adapter`; the ticket-sync Stop/SubagentStop hook reads `integration/ticket-flow.md`; every agentic-sdlc skill reads the guide tree.
- **Ongoing sync:** the **guide-sync** agent keeps the guide tree current on post-merge runs — this skill is one-time setup, harvester is continuous upkeep. `testing/` upkeep belongs to **qa-baseline**.
- **Kept separate:** the agentic-os `/agentic-init` skill at `plugins/agentic-os/skills/agentic-init/` is a sibling — do NOT modify it or its templates.

## Non-goals

- No tooling installation.
- No lint/build/test execution on the target project.
- No writes outside the guide tree, the entrypoint(s), and the `.agentic/runs/` gitignore rule.
- No git operations.
- No adapter installation or modification — the ticket/MR adapter must pre-exist for Step D.
- No edits to the agentic-init skill or its templates.
