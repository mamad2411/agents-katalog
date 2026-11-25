---
name: docs-pack
description: Use this skill when onboarding users to a feature, producing API documentation, or writing operational procedures — to generate a user-facing documentation pack (README, API reference, runbook, tutorial) for a module or feature; distinct from the `docs` knowledge skill — `docs-pack` produces git-versioned user docs while `docs` is general documentation guidance.
context: fork
argument-hint: "<path> [--template api-reference|user-guide|runbook|architecture] [--audience developer|operator|user]"
---

# /docs-pack — User-Facing Documentation Pack

Generate a coherent set of user-facing docs for a module or feature. Output goes to `<repo>/docs/<module>/` (versioned in git, NOT in `.ai-skills-memory/`) — same convention exception as `/feature-design`: docs are versioned with the code, not with project memory.

## When to use

- Onboarding users to a feature: `/docs-pack ./features/auth --type user-guide --audience user`
- API documentation: `/docs-pack src/api --template api-reference --audience developer`
- Operational runbook: `/docs-pack ./services/payment --template runbook --audience operator`
- Architecture overview: `/docs-pack . --template architecture --audience developer`

## Not for

- Internal technical docs (ADRs, design decisions) → use internal wiki / `docs` skill
- Code comments, docstrings → IDE / language-native tools
- Marketing copy or blog posts → `/content-creation`

## Invocation

```
/docs-pack src/api --template api-reference
/docs-pack ./features/auth --type user-guide
/docs-pack . --template architecture --audience developer
```

## Arguments

| Flag | Default | Effect |
|---|---|---|
| `<path>` (positional) | required | Directory or file to document |
| `--template` | auto-detect | `api-reference`, `user-guide`, `runbook`, `architecture` |
| `--audience` | `developer` | `developer`, `operator`, `user` |

## Templates

Each `--template` value maps to a starter document under
[`assets/templates/`](./assets/templates/). Copy the file into
`<repo>/docs/<module>/`, rename, and fill in the placeholders.

| `--template` | File | What it covers |
|---|---|---|
| `api-reference` | [`assets/templates/api-reference.md`](./assets/templates/api-reference.md) | OpenAPI 3.1-aligned endpoint reference: per-endpoint Summary, Auth, Request/Response, Errors, Rate limits, curl + Python + JS examples, related endpoints. Top-level Overview, Auth, Versioning, Common patterns. For HTTP APIs the OpenAPI spec is the preferred co-output |
| `user-guide` | [`assets/templates/user-guide.md`](./assets/templates/user-guide.md) | Diátaxis Tutorial + How-to hybrid: a 10-minute learning tutorial (Goal, Prerequisites, Steps, Verify, Recap) followed by a set of problem-oriented How-to procedures |
| `runbook` | [`assets/templates/runbook.md`](./assets/templates/runbook.md) | SRE-aligned operator runbook: service overview, SLO/SLI/SLA, Alert → Diagnose → Mitigate → Verify per alert, top 5 incident playbooks, rollback, escalation matrix, on-call cheatsheet |
| `architecture` | [`assets/templates/architecture.md`](./assets/templates/architecture.md) | C4-aligned architecture doc: Mermaid C4Context + C4Container diagrams, 3–5 sequenceDiagram flows, tech stack table, quality attributes, ADR ledger, risks |

## Output (versioned with code, not with project memory)

Files written to **`<repo>/docs/<module>/`** — versioned in git as project documentation:

- `README.md` — overview + quick-start
- `API-REFERENCE.md` (if applicable) — endpoint/function docs
- `RUNBOOK.md` (if operational) — procedures, troubleshooting
- `EXAMPLES.md` — code examples, use cases
- (Optional) Mermaid diagrams for flows / architecture

Memory writes (workflow run logs) go to L4 `.ai-skills-memory/docs/<module>/` separately.

## Agent roster

| Agent | Model | Effort | Tools | Role |
|---|---|---|---|---|
| `content-writer` | inherit | medium | Read, Grep, Glob, Write | Writes documentation from code + examples |
| `solution-architect` (default reviewer) | inherit | medium | Read, Bash, Grep | Cross-stack technical review, accuracy check |
| stack-specific engineer (optional, per `team-protocols/role-selection-table.md`) | inherit | medium | Read, Bash, Grep | Deep accuracy review when the docs target a single stack — `backend-engineer` (`software-engineer`/`python-engineer`/`java-engineer`), `frontend-engineer`, `db-engineer`, `sre-engineer`, etc. Selected by the Lead from the role-selection table |
| `seo-engineer` (if public-facing) | inherit | low | Read, Write | GEO/SEO optimization pass per `geo-content` rule + `geo-writer` skill |

## Pipeline

```
┌─ content-writer:
│  - Read source code, docstrings, tests
│  - Extract examples
│  - Generate documentation per template
│  → Draft docs in <repo>/docs/<module>/
│
├─ Reviewer (solution-architect by default; stack-specific engineer
│  selected per team-protocols/role-selection-table.md when scope is
│  single-stack — e.g. python-engineer for a FastAPI service,
│  frontend-engineer for a React component, sre-engineer for runbooks):
│  - Review accuracy, completeness, runnability of examples
│  - Suggest improvements
│  → feedback.md (in .ai-skills-memory/docs/<module>/)
│
├─ content-writer revisions:
│  └─ Address feedback, finalize
│
├─ (If --audience = user OR public-facing) seo-engineer:
│  └─ Apply @geo-writer (structure pass) + @humanizer (voice pass) per geo-content + humanize-content rules
│
└─ Memory write: L4 generation summary
   Report: docs location + update reminder
```

No RALF — docs generated in one pass with optional reviewer pass.

## G7 spawn payloads

content-writer, the reviewer (solution-architect or stack-specific engineer), and seo-engineer spawns use structured G7 payloads per `plugin/schemas/spawn-payload.schema.json`. Returns validated against `plugin/schemas/return-contract.schema.json`. Reviewer role selection follows `plugin/skills/team-protocols/role-selection-table.md`.

## Eval rubric

Pointer: `plugin/eval/judge-rubrics/docs-pack.md` (B10).

Dimensions:
1. **Completeness** — all key concepts documented per template
2. **Clarity** — examples are runnable, explanations clear
3. **Accuracy** — matches actual code behavior (verified by reviewer — solution-architect or stack-specific engineer)
4. **Organization** — logical flow, easy to navigate
5. **Style consistency** — follows `docs` skill style guide + `geo-content` rule (if public-facing)

Pass: avg ≥ 4.0, no dimension < 3.

## Memory writes

| Layer | When | Shape |
|---|---|---|
| L4 | After complete | `.ai-skills-memory/docs/<module>/generation-summary.md` — what was documented, when, audience, files emitted |

## Failure modes

- **Source code poorly documented (no docstrings, no tests):** content-writer infers from code + flags as `[INFERRED — needs review]` in the doc
- **API changed since docs written (re-run scenario):** reviewer catches; content-writer updates affected sections
- **Examples don't run:** content-writer tests examples; fixes or removes broken ones; flags as `[EXAMPLE TESTED]` for those that pass
- **Public-facing flag set but no `marketing/MARKETING.md`:** seo-engineer warns about missing brand context; uses generic GEO defaults

## Observability events

- `workflow_start` — docs-pack + path + template
- `agent_spawned` × 2–3 (content-writer, reviewer, optional seo-engineer)
- `workflow_end` — `COMPLETE` with file count

## Integration

- **Orchestrator**: `feature-design-lead`
- **Schemas**: `plugin/schemas/spawn-payload.schema.json`, `plugin/schemas/return-contract.schema.json`
- **Companions**: `/subagent-spawn`, `/context-load`
- **Knowledge skills**: `docs` (general writing patterns), `geo-writer` (GEO structure pass), `humanizer` (voice pass), `content-creation` (when marketing/blog content overlaps with the docs pack)
- **Rules**: `subagent-isolation`, `untrusted-content-wrapping` (G1 wrap on source code reads), `geo-content` (if public-facing — mandatory per rule), `humanize-content` (mandatory for public-facing per rule), `memory-discipline`
- **Hooks**: `tool-output-normalize.py` (G2 on extracted code samples)
