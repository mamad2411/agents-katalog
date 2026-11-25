---
name: pm-clarify-requirements
description: (NS) Resolve ambiguities, gaps, and unstated assumptions in a scope description before generating requirements. On brownfield repos, runs harness-bootstrap-brownfield when brownfield-map.md is missing; when a map exists, mandatory human gate to refresh or keep it (shows last map date). Use when the user gives a vague or incomplete scope, mentions "dashboard", "notifications", "integration with X" without detail, or before requirements generation when terms are ambiguous — even if they do not ask to "clarify". Do NOT generate requirements.md in this skill; output enriched context only.
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.0"
depends:
  - nextstage-harness
---

# Clarify Requirements

Pre-planning workflow: identify and resolve ambiguities **before** invoking `pm-requirements-generator`.

## Harness discovery

See `../nextstage-harness/references/harness-discovery.md` and `../nextstage-harness/references/artifact-layout.md`.

**Resolve `{product_root}`:** read `AGENTS.md` at the repo entry. Prefer the documented anchor. If the path is missing, outside the open workspace, or points at another clone, use the directory that contains `AGENTS.md`.

Stack and architecture questions belong to stack detection — not this skill.

## When to use

- Vague or incomplete scope from the user
- Ambiguous terms (dashboard, integration, notification system)
- First version of a new system without prior documentation
- Orchestrator judges scope too thin (< 3 paragraphs or vague terms)

## Workflow

### Step 0 — Brownfield gate (before analysis)

**Do not grep or explore application source code** until this step completes.

1. Check `{product_root}/docs/context/brownfield-map.md`.
2. Detect brownfield signals under `{product_root}`: `backend/`, `frontend/`, `src/`, `app/`, or equivalent application code (not docs-only repos).
3. **If brownfield signals exist and `brownfield-map.md` is missing:**
   - Stop — do not ask clarification questions yet.
   - Invoke **`harness-bootstrap-brownfield`** and produce `{product_root}/docs/context/brownfield-map.md`.
   - Tell the user briefly that brownfield context was required before refining scope.
   - Resume this skill at **Step 0.4** (refresh gate) once the map file exists.
4. **If greenfield** (no application code) — skip bootstrap; proceed to Step 1.
5. **If `brownfield-map.md` already exists** — run **Step 0.4** before any scope analysis.

#### Step 0.4 — Brownfield refresh gate (mandatory human confirmation)

**Stop. Do not proceed to Step 1 until the human replies.**

1. Read `{product_root}/docs/context/brownfield-map.md`.
2. Extract the map date from the `**Date:**` line in the file header. If absent, state `date unknown`.
3. Present the gate to the human:

```
Brownfield map found: docs/context/brownfield-map.md
Last updated: {date from file, or "date unknown"}

Before clarifying this version's scope, do you want to refresh the brownfield map
(re-scan codebase with harness-bootstrap-brownfield) or keep the existing map?

Reply with one of:
- refresh — update brownfield-map.md, then continue clarification
- keep — use the existing map as-is and continue clarification
```

4. **Wait for an explicit reply.** Valid answers: `refresh` / `keep` (or clear equivalent in natural language).
5. **Never assume** `keep` because the map looks recent, because planning is urgent, or because the user already pasted a descritivo.
6. On **`refresh`:** invoke **`harness-bootstrap-brownfield`** (update in place), then continue to Step 1 with the new map.
7. On **`keep`:** note in session context that the human accepted map date `{date}`; continue to Step 1 using the existing file.
8. On ambiguous reply: ask once more — do not start Step 1 until `refresh` or `keep` is clear.

Also read `{product_root}/docs/context/system-reverse-spec.agent.md` when present (prefer over the prose body); else `system-reverse-spec.md` (after the gate resolves).

Allowed reads before Step 1 (brownfield): user scope file, `brownfield-map.md`, `system-reverse-spec.agent.md` / `system-reverse-spec.md`, `{harness_root}/rules/architecture-rules.md`, files under `{product_root}/docs/versions/{version_san}/` for the active version.

**Forbidden before Step 1:** ad-hoc `grep`/code search in `backend/`, `frontend/`, or `src/` to "reduce ambiguity"; skipping Step 0.4 when a map exists.

### Step 1 — Analyze raw scope

Read the user's description (and brownfield context when Step 0 applied). Flag ambiguities:

| Category        | Example                           |
| --------------- | --------------------------------- |
| Actors          | "the user does X" — which role?   |
| Data scope      | list fields, pagination, filters? |
| Integrations    | REST, webhook, auth method?       |
| Multitenancy    | multi-company isolation?          |
| Business rules  | which validations exactly?        |
| State lifecycle | allowed transitions?            |
| Scope limits    | what's in/out of this version?    |
| Performance     | volume, concurrency, SLA?         |
| Security        | auth required, role permissions?  |

Use the brownfield map for **what exists** — ask the user only for **what the version should change or add**.

### Step 2 — Ask questions

- Maximum **5 questions per round**
- Prioritize blockers for correct feature generation
- Group related questions when possible
- Plain language, numbered, self-contained

Present:

```
Before generating requirements, I need to clarify a few points:

1. [actor question]
2. [data scope]
...

Reply in free form. I will proceed with requirements once I have these answers.
```

### Step 3 — Consolidate answers

After responses:

1. Confirm understanding in a short summary (3–5 bullets)
2. Ask: "Shall I proceed with requirements generation?"
3. Wait for yes or correction
4. **Maximum one clarification round** — if still unclear, document reasonable assumptions as "Assumed premises"

### Step 4 — Hand off to pm-requirements-generator

Compile enriched context:

```markdown
## Original scope (user-provided):

[original text]

## Brownfield context (if applicable):

[Summary from brownfield-map.md — modules and constraints relevant to this version]
[Brownfield gate: human chose refresh | keep on {date shown in gate}]

## Clarifications obtained:

1. Question: [...]
   Answer: [...]

## Confirmed premises:

- [Premise 1]
- [Premise 2]
```

Pass this document as input to `pm-requirements-generator`. Do **not** write `requirements.md` here.

## Critical rules

- **Brownfield without map:** run `harness-bootstrap-brownfield` first — never skip by grepping the codebase instead
- **Brownfield with map:** Step 0.4 gate is **mandatory** — show last map date; wait for explicit `refresh` or `keep`; never assume
- **One round of questions max** — then assume conservatively and document premises
- **No requirements document** in this workflow
- **No stack/architecture questions** — defer to stack profiles / project rules and brownfield map
- If user answers "don't know" on a critical point: assume smallest safest scope and document it

## Integration

```
planning start → [brownfield + no map?] → harness-bootstrap-brownfield → [brownfield refresh gate] → pm-clarify-requirements → pm-requirements-generator → Gate 1
```

Brownfield refresh gate: human confirms `refresh` or `keep` after seeing `brownfield-map.md` date.

## Related skills

- `harness-bootstrap-brownfield` — mandatory prerequisite when code exists and `brownfield-map.md` is missing
- `pm-requirements-generator` — next step after clarification
- `harness-architecture-rules` — constitution when `architecture-rules.md` is still a stub (separate from this skill)
