---
name: add-adr
description: Record an architectural decision in Prudent's docs/DECISIONS.md using the jZen ADR format. Use when a decision changes or supersedes something in an earlier doc (AGENTS.md, the migration prompt, or a prior Prudent ADR), when the conversion settles a rule (Flyway band, money type, repo shape), or the user asks to log/document a decision.
---

# Adding a Prudent ADR

`docs/DECISIONS.md` is Prudent's running log of architectural decisions and, crucially, where they
**change earlier docs and why**. `AGENTS.md`, `docs/prudent-migration-prompt.md` and any plan
document describe intent; when the product drifts from them, the drift is recorded here with
justification — **newest ADRs win on conflict**.

## Two archives, never mixed

- **`docs/DECISIONS.md`** — Prudent's own log. Numbering starts at **ADR-001** and is Prudent's
  alone. Everything decided in this repository goes here.
- **`../jZen/docs/architecture/DECISIONS.md`** — jZen's archive, read-only from here. Cite it as
  `jZen ADR-0NN` when a Prudent decision depends on or is constrained by one; never renumber
  against it, never write into it. A decision that changes *jZen* is made in the jZen repository.

If `docs/DECISIONS.md` does not exist yet, create it with a short intro (what the file is,
newest-first, append-only) and ADR-001.

## Format (match the existing entries exactly)

Entries are **newest first** — insert directly under the intro, above the previous highest ADR.
Number sequentially. Use this shape:

```markdown
## ADR-0NN — <short imperative title>

**Date:** YYYY-MM-DD. **Status:** accepted | deferred | proposed.

### Decision

<What was decided, concretely. Bullet the moving parts.>

### What this supersedes, and why

- **"<the exact earlier wording/decision>"** (<which doc + section>) → **reversed | changed |
  refined | reframed.** *Why:* <the justification — this is the load-bearing part>.

### Consequence

<What now holds as a result — invariants, versioning impact, what was verified green.>
```

House style:

- A short entry may collapse to **Decision** / **Supersedes** / **Why** inline — match the weight
  of the decision.
- Cite the **exact prior wording** you are superseding and name the doc + section.
- Convert relative dates to absolute (`YYYY-MM-DD`).
- State what was **verified** (tests green, build passes) in the Consequence, not what you expect.
- When a decision is forced by a jZen rule, name the rule and the document
  (`../jZen/docs/architecture/STANDARDS.md` §…, or `jZen ADR-0NN`) so the constraint is traceable.

## Decisions this repository is known to owe an ADR

Written down so they are not settled silently: the repository shape and the path-dependency on the
`../jZen` sibling checkout (and what replaces it once jZen publishes); the **money
representation**; the **Flyway version band** Prudent owns; the locale set; whether Prudent has an
admin panel; and the deployment target.

## After writing

If the decision changes wording elsewhere, the ADR is authoritative — but update the affected
document's prose too (`AGENTS.md` in particular) when practical, and say so in the entry. Never
delete the superseded text from history; the ADR *is* the record of the change.
