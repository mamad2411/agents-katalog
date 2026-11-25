---
name: spec-driven
description: Default OpenSpec change workflow — scaffold a change through proposal → specs → design → tasks, apply it, then archive once merged. Use to start a change, write a proposal/spec/design/tasks, implement a tasks checklist, or archive a merged change.
---

# Spec-Driven Change Workflow (OpenSpec)

A change moves through four authored artifacts, an execution phase, and a closing phase. Each
artifact answers a different question, and each builds on the one before it:

```
proposal.md → specs/**/*.md → design.<side>.md → tasks.<side>.md → apply → archive
WHY           WHAT            HOW                 WORK BREAKDOWN    EXECUTE  RECONCILE & SHIP
```

The whole point of doing this up front is that decisions get cheaper the earlier you make them.
The proposal pins down *why* and *what scope*; the specs pin down *observable behavior*; the
design pins down *technical approach*; the tasks turn all of that into a checklist someone can
execute and track. Skipping straight to code loses the contract these documents create with
each other — most notably the **Capabilities** contract between the proposal and the specs.
And the lifecycle only closes at **archive**: until the implemented change is merged and its
delta specs are folded into the shipped specs, the source of truth is not yet updated.

## Where artifacts live

The OpenSpec tree root resolves through **`SPEC_VAULT_PATH`** — set it in the host repo's
`.claude/settings.json` `env` block or the shell — and falls back to `./openspec` in the host
repo when unset. Pointing it at a shared **vault** (a plain folder of Markdown that is itself a
git repository, typically also opened in Obsidian as the human's reader) lets sessions in
different host repos — a backend repo and a frontend repo — read and write the *same* truth.
Access is always plain filesystem (Read/Write/Glob/git) against the local checkout; the operative
truth never depends on an MCP being available.

A change lives in its own directory under `<root>/changes/<slug>/`. Generated artifacts:

```
proposal.md          ← the change proposal, with `status:` frontmatter (always)
specs/<capability>/spec.md   ← one delta spec file per capability (always)
design.<side>.md     ← per-side technical design (only when warranted)
tasks.<side>.md      ← per-side implementation checklist (always)
```

`<side>` is `backend` or `frontend`. The suffix applies **always** — even when a feature touches
only one side — so every consumer (architects, delivery loops, archive) parses exactly one
format instead of detecting variants. `proposal.md` and `specs/` are never split per side: they
are product truth (a requirement like "user exports CSV" doesn't belong to a repo), while design
and tasks are execution truth that each repo's loop owns and updates without write contention.

What makes the per-side split *pull its weight* (not just mirror the folders) are two artifacts the
references detail: each side's design carries a machine-readable **task manifest**
(`files_owned` / `deps` / `exports_promised`, in [`references/tasks-and-apply.md`](references/tasks-and-apply.md)),
and any shared boundary (a contract field, an enum like the set of cancellable states) is named in
a **cross-side ripple note** so a change on one side is visibly tracked on the other (see
[`references/loop-integration.md`](references/loop-integration.md)). When you author a cross-side
change, produce both — they're the difference between two task lists and two *coordinated* task lists.

Existing, already-shipped specs live under `<root>/specs/<capability>/spec.md`. Read those
before proposing changes to existing capabilities — the proposal and the delta specs reference
them by their exact folder name. When the feature carries an API contract, it lives as OpenAPI
YAML under `<root>/contracts/` (the archive phase projects it to Postman; the file is master,
Postman is never edited directly).

## The change lifecycle

`status:` frontmatter in `proposal.md` tracks the change through four states (a missing field
reads as `in-progress`, for changes authored before this convention):

```
draft → in-progress → in-review → archived
```

- **draft** — being authored: proposal → specs → design → tasks.
- **in-progress** — under implementation. The delivery loops act as the apply phase: they check
  off `tasks.<side>.md` as their gates pass, and the spec is the **authority** — an approved
  deviation is amended into the change folder and committed at approval time, never deferred
  (product/UX/contract drift is approved synchronously by the human; purely technical
  reconciliations are auto-amended with a marker and ratified asynchronously — the two-tier
  gate in [`references/loop-integration.md`](references/loop-integration.md)).
- **in-review** — every `tasks.<side>.md` is complete; the human is reviewing/merging the MR(s).
  Review feedback re-enters through the loops as `## R<n>` task sections and flips the change
  back to `in-progress` until the round closes.
- **archived** — the MR(s) merged and the archive phase ran. Shipped specs describe **merged
  code only**: archive is gated on the merge, not on task completion.

The loop orchestrators maintain the field; only the archive phase may set `archived`.

## Templates

Each artifact has a starter template in [`templates/`](templates/) — read the relevant one
before authoring and copy its skeleton into the target file, then fill it in. The templates
carry the exact section headers and HTML-comment guidance the workflow expects, so starting
from them keeps the artifacts parseable downstream.

## Dependency order

Honor the `requires` chain — never author a downstream artifact before its inputs exist:

- **proposal** requires nothing — it is the foundation.
- **specs** require the proposal (one spec per capability the proposal names).
- **design** requires the proposal. The design phase is a **routing gate, not hand-authoring**:
  it detects which side(s) the change touches and dispatches `frontend-architect` /
  `backend-architect` to author each side's `design.<side>.md` — skipping a side whose design
  already exists, or whose slice is too small to warrant one. See
  [`references/design.md`](references/design.md).
- **tasks** require both specs and design.
- **apply** requires tasks.
- **archive** requires the change to be `in-review` with the MR(s) merged — see
  [`references/archive.md`](references/archive.md) for the full precondition gate.

If the user asks for a later artifact and an earlier one is missing or stale, say so and offer
to create or refresh it first rather than guessing at the missing contract.

## References

Read the reference for the phase you're authoring — each carries the sections, format rules,
and worked examples for that artifact:

- [`references/proposal.md`](references/proposal.md) — the WHY: sections, the load-bearing
  **Capabilities** contract, researching existing specs · read before writing `proposal.md`.
- [`references/specs.md`](references/specs.md) — the WHAT: delta operations
  (ADDED/MODIFIED/REMOVED/RENAMED), requirement/scenario format (`####` exactly), the MODIFIED
  full-block workflow · read before writing any `specs/<capability>/spec.md`.
- [`references/design.md`](references/design.md) — the HOW: the **architect-routing gate**
  (detect side(s) → dispatch the architect, skip a side whose design exists), when a design is
  warranted (it's conditional — skip it when not), and its sections · read before deciding on /
  writing `design.<side>.md`.
- [`references/tasks-and-apply.md`](references/tasks-and-apply.md) — the checklist format the
  apply phase parses (`- [ ] X.Y`), how execution is delegated to the delivery loops, and the
  inline fallback · read before writing `tasks.<side>.md` or applying.
- [`references/archive.md`](references/archive.md) — the RECONCILE & SHIP: the precondition
  gate (merged MRs, no open review round, clean vault tree), merging delta specs into shipped
  specs, the Postman contract sync, the **project-doc reconciliation sweep** (catch the
  `CLAUDE.md` / ADRs / runbooks / architecture blueprints / tech-debt / config the change made
  stale), and filing the change away · read before archiving.
- [`references/loop-integration.md`](references/loop-integration.md) — how a delivery loop
  drives a change through the lifecycle: attach, cycle-boundary vault sync, task tracking, the
  drift gate, cross-side ripple, the closing protocol, MR-review re-entry · read by the
  delivery-loop orchestrators (all three loops link here so the rules live in one place).
