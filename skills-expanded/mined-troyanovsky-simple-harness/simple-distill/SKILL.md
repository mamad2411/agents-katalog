---
name: simple-distill
description: >
  Promote durable, high-level knowledge from a completed feature's docs into app-level documentation
  (docs/architecture.md, docs/capabilities.md, docs/adr/, docs/CHANGELOG.md), then archive the
  feature folder. Distills first, retires second. Use when a feature is finished and you want to
  capture its lasting decisions and behavior before its planning docs go stale. Triggers: "distill
  this feature", "promote the docs", "update the architecture doc", "write an ADR for this",
  "archive this feature", "capture what we learned".
disable-model-invocation: true
---

# Simple Distill — Promote Durable Knowledge and Retire a Feature

You are distilling a completed feature into durable, app-level documentation, then retiring its
planning docs to an archive. Feature docs (`spec.md`, `design.md`, `issues.json`,
`progress-log.md`) record a **delta** — the journey from one system state to the next. Once the
feature ships, that delta goes stale. Your job is to lift the parts worth keeping — the *why*, the
*shape*, the *stable intent* — up into living app-level docs, then move the now-historical feature
folder into `docs/archive/`.

This skill runs **after** a feature is complete (all tasks `done`). It consumes the output of
**simple-spec**, **simple-design**, and **simple-implement**, and complements **simple-cleanup**
(which compacts artifacts *within* a feature; this skill promotes knowledge *across* features and
retires the feature).

## Governing principle — altitude and the anti-bloat contract

> Durable docs capture what code **can't** tell you — the **why**, the **shape**, and the **stable
> intent** — at the **lowest level of detail that is still useful**. Anything a future agent could
> recover by reading the code in under a minute does **not** belong in a durable doc. Point to
> *where* in the code it lives; do not reproduce it.

A comprehensive, always-current, detailed description of the whole system is neither feasible nor
maintainable — and it duplicates the code, which is already the source of truth for detail. Durable
docs earn their keep precisely by staying **high-level and slow-changing**. Every artifact below has
a fixed altitude and an explicit "what does NOT go here" rule. When in doubt, leave it out and trust
the code.

## Folder convention

Durable docs live at the `docs/` root, alongside the existing app-level `visual.md`:

```
docs/
  index.json            ← feature manifest (gains an "archived" key — see step 5)
  visual.md             ← how the app looks (app-level, from simple-visual)
  architecture.md       ← how the app is built, high-level (living — THIS SKILL)
  capabilities.md       ← what the app does, high-level (living — THIS SKILL)
  CHANGELOG.md          ← one entry per distilled feature (append-only — THIS SKILL)
  adr/
    0001-<title>.md     ← one decision per file (immutable — THIS SKILL)
  archive/
    <feature-name>/     ← retired feature folders (moved here by THIS SKILL)
  <feature-name>/       ← active feature folders
```

## The durable doc set — what goes where

| Doc | Altitude (what goes in) | Does NOT contain | Mode |
|---|---|---|---|
| **`adr/NNNN-*.md`** | One cross-cutting, hard-to-reverse, or non-obvious decision: context & forces, the decision, alternatives rejected, consequences. ~1 page. | Routine choices that follow existing convention; implementation walkthroughs. | **Immutable, append-only** |
| **`architecture.md`** | The *map*: major components and their responsibilities, how they communicate, system-level data flows, cross-cutting patterns (auth, errors, config), major external dependencies. | File/function-level detail, code blocks (except ≤3-line illustrative signatures), anything cheaper to read from the code. **Cap ~200 lines.** | **Living** (reconciled vs. code) |
| **`capabilities.md`** | Stable user-facing behavior — the capability map, one or two lines per capability, in user terms. | Acceptance criteria, edge cases, UI specifics, logic restatement. If it reads like a spec, it's too deep. **Cap ~150 lines.** | **Living** (merged each run) |
| **`CHANGELOG.md`** | One entry per distilled feature: date, name, a one-paragraph "what shipped", and links to the ADRs created and the archived feature folder. | Task-level detail — that lives in the archived `progress-log.md`. | **Append-only** |

Notes:
- **No standalone API doc.** Exhaustive endpoint listings drift fastest and are codegen territory.
  A *significant contract decision* becomes an ADR; a *stable contract shape* is a section in
  `architecture.md`.
- **The CHANGELOG is the traceability spine.** It links each distilled feature to its archived
  folder, so a future agent can walk back to full historical detail (changelog → archive → git)
  without that detail being duplicated into the durable docs.
- **Length caps are forcing functions**, not hard limits. They exist to keep altitude honest.

## Source-of-truth hierarchy

When sources disagree, resolve in this order — but note that durable docs and code sit at
**different altitudes**, so they rarely truly compete:

1. **Durable docs** (`architecture` / `capabilities` / `adr` / `visual`) — current truth for the
   *why* and the *high-level shape*.
2. **Archived feature docs** — historical record of how a past round was built.
3. **Active (non-archived) feature docs** — *intended* state after the current round; not yet true.
4. **Code** — ground truth for *what* and for all detail.

Durable docs win on *why/shape*; code wins on *what/detail*. If a durable doc appears to conflict
with code on a **detail**, that is the bloat smell — the doc has drifted too low; raise its altitude
rather than "correcting" the detail.

## Workflow

### 1. Orient

- Identify the feature. The user usually names it. If not, check `docs/index.json` for a feature
  with `status: "done"` that is not yet `"archived": true`. If several qualify, ask which one.
- Confirm the feature is actually complete: all tasks in `issues.json` are `"done"`. If tasks
  remain, say so and suggest finishing them (via **simple-implement** / **simple-run**) before
  distilling. You can proceed if the user insists, but flag that the distillation will be partial.
- Read the feature's `spec.md`, `design.md`, and `progress-log.md` in full (and any `spec/` or
  `design/` child files they index). These are your distillation sources.
- Read the existing durable docs: `architecture.md`, `capabilities.md`, `CHANGELOG.md`, the `adr/`
  index, and `visual.md`. You are merging into these, so you must know their current contents and
  altitude.
- Read the relevant **code** for any area the feature touched. The living docs are reconciled
  against code, not copied from the (now-stale) feature docs.

### 2. Triage — decide what is durable (the proportionality gate)

Before writing anything, decide what — if anything — is worth promoting. Assess each source:

- **ADR candidates** (from `design.md` § Key decisions + `progress-log.md` deviations): Is there a
  decision that is cross-cutting, hard to reverse, or non-obvious? Routine choices that follow
  existing convention do **not** warrant an ADR.
- **Capability changes** (from `spec.md` § Proposed product state): Did this feature add or change
  *stable, user-facing* behavior worth recording at the capability-map altitude?
- **Architecture changes** (from `design.md` § Proposed technical state, reconciled vs. code): Did
  this feature change the *shape* of the system — new major component, changed data flow, new
  cross-cutting pattern or external dependency?

**"Nothing to promote" is a valid and common outcome.** Many features — bug fixes, small tweaks,
convention-following additions — yield no ADR and no architecture change. Do not invent durable
content to justify the run. If the only output is a CHANGELOG entry and a retire, that is correct.

Present this triage plan to the user as a short preview (what you'll write, where, and what you're
**deliberately not** promoting and why) before writing anything.

### 3. Distill the append-only docs (ADRs + CHANGELOG)

These are additive and safe — do them first.

- **ADRs:** For each promoted decision, create `docs/adr/NNNN-<kebab-title>.md` using the next
  zero-padded sequential number. Follow `references/adr_template.md`. An ADR is **immutable**: never
  edit a published one. If this feature *reverses* a past decision, write a **new** ADR that
  references and supersedes the old one, and set the old ADR's status to `superseded-by-NNNN`
  (the single status-line edit is the one permitted change to a published ADR).
- **CHANGELOG:** Append one entry to the top of the entries section in `docs/CHANGELOG.md` (newest
  first), using the format below. Create the file with a header if it doesn't exist.

```markdown
## YYYY-MM-DD — <feature-name>
<One paragraph: what shipped, in product terms.>
- ADRs: [0007](adr/0007-foo.md), [0008](adr/0008-bar.md)   ← omit if none
- Archived docs: [docs/archive/<feature-name>/](archive/<feature-name>/)
```

### 4. Distill the living docs (architecture + capabilities)

These are **rewritten** to reflect the current system, not appended. Reconcile against the **code**,
not the stale feature docs — the feature docs tell you *what changed and where to look*; the code
tells you *what is now true*.

- Edit only the sections the feature actually affected. Leave unrelated sections untouched.
- **Remove superseded content.** When this feature changed how something works, update the
  description and delete the old one — a living doc that only grows is drifting toward bloat. An edit
  should remove roughly as much as it adds, except for genuinely new surface area.
- Respect the altitude rules and length caps. If an edit pushes a doc well past its cap, that is a
  signal you have gone too low — raise the altitude or move detail back to "go read the code."
- If `architecture.md` or `capabilities.md` does not exist yet, create it from the corresponding
  template (`references/architecture_template.md`, `references/capabilities_template.md`),
  seeded from the current code and this feature — not a from-scratch audit of the whole system
  unless the user asks for one.

Show the user the proposed diffs (or a clear before/after summary) for each living doc and get
approval before writing.

### 5. Retire the feature folder

Only after steps 3–4 are written and approved — **never retire a source before its knowledge is
promoted.**

- Move `docs/<feature-name>/` to `docs/archive/<feature-name>/` (create `docs/archive/` if needed).
  Move the whole folder intact — `spec.md`, `design.md`, `issues.json`, `progress-log.md`, and any
  `spec/`, `design/`, archive sub-files. Nothing is deleted.
- Update `docs/index.json`: keep `status` as `"done"`, add `"archived": true`, and repoint `path`
  to the new location:

```json
{
  "features": {
    "<feature-name>": {
      "status": "done",
      "archived": true,
      "path": "docs/archive/<feature-name>/"
    }
  }
}
```

### 6. Report

Give the user a concise summary:
- ADRs created (IDs and titles), and any ADR superseded.
- CHANGELOG entry added.
- Which living docs changed, and a one-line note on each change.
- **What was deliberately not promoted, and why** — this documents the proportionality judgment.
- Where the feature docs now live (`docs/archive/<feature-name>/`).

## Important notes

- **Distill first, retire second — always in that order, gated.** If distillation can't be
  completed or approved, do not move the feature folder.
- **High-level only.** The most common failure is a durable doc creeping down into detail the code
  already owns. When tempted to add specifics, add a pointer to the code instead.
- **ADRs are immutable.** The only permitted edit to a published ADR is flipping its status to
  `superseded-by-NNNN`. Everything else is a new ADR.
- **User approval is mandatory** before writing living docs and before retiring the folder — this
  skill is never invoked in automated mode. Follow the preview-then-write pattern of
  **simple-cleanup**.
- **Scale to the feature.** A large feature may yield two ADRs and edits to both living docs; a
  bug fix may yield only a CHANGELOG line and a retire. Don't inflate.
