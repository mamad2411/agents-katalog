---
name: decompose-feature
description: Turn a feature or epic into ATOMIC, agent-ready issues — one concern per issue, dependencies mapped, per-issue security notes (RLS allow/deny), tests, and acceptance criteria — then append them to scripts/kanban/issues.csv and mirror in docs/planning/kanban-backlog.md. Use when planning a new feature, breaking down an epic, or filling the backlog. Trigger words — decompose, break down, backlog, issues, kanban, atomic issues, plan a feature, sprint.
---
# Decompose feature into atomic issues

**Use when:** planning a feature/epic into buildable, single-concern issues. **Owners:** tech-lead-orchestrator.
Stack-neutral: the columns and the atomicity rule hold whatever `vantry.yml` `stack:` names.

## Inputs
The feature/epic, the relevant spec in `docs/specs/*` (its `REQ-###` ids), the current
`scripts/kanban/issues.csv` (for the id prefix + last number), and the agent roster in `agents/`.

## Procedure
1. **Read** the spec + `CLAUDE.md`. Restate the feature's core loop in one line so every issue traces to it,
   and list the `REQ-###` ids in `docs/specs/functional-spec.md` this feature is meant to satisfy.
2. **Slice into ATOMIC issues — one concern each**, respecting the natural build order:
   **migration+RLS → security policy/test → API/service → UI → tests/e2e**. If an issue needs two agents or
   two PRs, split it. Rule of thumb: one issue = one PR = one reviewable concern.
3. **Map dependencies** as ids in the `deps` column (semicolon-separated, e.g. `PRJ-006;PRJ-007`). A
   *foundation* issue with no unmet deps that unblocks others → `status=todo`; everything else → `backlog`.
4. **Per issue, capture**: acceptance criteria (Given/When/Then), affected tables/routes/components,
   **security notes** (who may read/write; the RLS **allow AND deny** cases to test), and test requirements.
   Anything touching auth/RLS/payments/PII/AI must be flagged for `security-engineer` review.
5. **Assign** `area` + lead `agent` from the roster; set `priority` (P0–P2) and `size` (S/M/L).
6. **Fill the three traceability columns.** None is decoration — each is read by a machine downstream:
   - **`req`** — the requirement ids this issue serves (`REQ-004;REQ-011`). Empty is legitimate for
     infrastructure. An issue that is neither infrastructure nor traceable to a REQ is **scope creep** — say so
     out loud, and either cut it or raise the requirement first. `/sprint-review` reads this column for MUST
     coverage, so a wrong id is worse than an empty one.
   - **`paths`** — the globs the issue will touch (`src/billing/**;tests/billing/**`). **This is what makes
     parallel dispatch legal:** `/next` co-dispatches two issues only when their declared globs are provably
     disjoint, so an issue with no `paths` is never co-run. Declare the narrowest globs that are actually true —
     a generous glob silently serializes the sprint.
   - **`security`** — `yes` when the issue touches `vantry.yml` **`sensitive_paths`** (auth, payments, PII, AI
     context, RLS); else empty. `yes` obliges `/pickup-issue` to commit a `security-review` verdict.
7. **APPEND rows** to `scripts/kanban/issues.csv` with **all 13 columns**
   `id,title,epic,area,agent,priority,size,deps,status,sprint,paths,req,security` — new issues default
   **`sprint=Backlog`** (unscheduled; the `sprint-planner` moves them into `S1…SN`). Keep **titles comma-free**
   (the importer splits on commas and aborts on a wrong column count); `epic` becomes a milestone (readable,
   e.g. `EPIC 3 — Billing`). Continue the existing id sequence; never renumber shipped rows.
8. **Write the real acceptance criteria to `scripts/kanban/details/<id>.md`** — `import-kanban.sh` inlines this
   file into the issue body. Without it the issue ships generic boilerplate and this decomposition is thrown
   away before anyone implements it. Open with `**Satisfies:** REQ-004 — <the requirement verbatim>` for each
   id in `req`, then one **Given/When/Then** block per criterion, plus the **deny** case for anything
   authorization-shaped. Write what a human would accept, not what is easy to phrase.
9. **Mirror** each issue in `docs/planning/kanban-backlog.md` with its full context/AC/security notes/tests
   (the CSV is the index; the doc is the detail the importer body links to).
10. **Import** via `scripts/kanban/import-kanban.sh` (run `DRY_RUN=1 ./import-kanban.sh` first to preview) —
    check the row count, the inlined criteria in the preview, and that no title carries a stray comma.

## Guardrails
- Never write a non-atomic "and also" issue — split it. Never create an issue whose deps aren't in the CSV.
- Never put a comma in a title, or renumber/rewrite an already-shipped id. Foundation-only rows get `todo`.
- Every issue that touches sensitive data carries an explicit allow/deny security note — no silent gaps.
- Never invent a `REQ-###` that is not in the spec, and never widen `paths` to "be safe" — a false glob makes
  two independent issues look conflicting, and a stale one lets two agents collide in the same file.

## `security: yes` and `sensitive_paths` are two claims about the same thing
The CSV's `security` column drives the extra Definition-of-Done line on the issue. `vantry.yml`
`sensitive_paths` drives the **gate that actually blocks the merge**. Nothing reconciles them, and they drift in
both directions:

- `security: yes` on an issue whose `paths` match no `sensitive_paths` glob → the issue promises a security
  review that CI will never require. The promise is decorative.
- `security: no` on an issue whose `paths` **do** match → CI blocks the PR and the author had no warning.

Set them together. When you mark an issue `security: yes`, check that its `paths` are covered by
`vantry.yml` `sensitive_paths` — and if the area genuinely is sensitive but the contract does not say so, **add
the glob to `sensitive_paths` in the same change**. `scripts/kanban/lint-kanban.sh` now warns on the mismatch.

## `paths` must include the tests, or co-dispatch is a coin flip
`/next` decides whether two issues can run in parallel by intersecting their `paths`. An issue whose `paths`
name only production code looks isolated and is not: in a real three-sprint run, three issues with disjoint
`src/**` globs all conflicted because each appended to the same `tests/unit.mjs`.

So: **every issue's `paths` names where its tests live too.**

```
paths: src/booking/**;tests/booking.*
```

And prefer **one test file per feature** over one growing suite file. A single `tests/unit.mjs` is a shared
surface that silently serialises the whole board — `/next` will (correctly) refuse to co-dispatch anything.

## Done when
Issues are atomic + ordered by dependency; CSV appended (all 13 columns incl. `sprint=Backlog`, `paths`, `req`,
`security`, comma-free titles, correct statuses); every issue has `scripts/kanban/details/<id>.md` with real
Given/When/Then and its `**Satisfies:**` line; backlog doc mirrors them; `DRY_RUN=1` import previews cleanly.
