---
name: plan-propose
description: >
  Propose a brownfield change: one-intent folder with proposal, ADDED/
  MODIFIED/REMOVED delta specs, and optional design. Use when the user
  says propose, new change, delta spec, opsx propose, or runs /ultimate-sdd:propose.
license: MIT
metadata:
  author: andrewr303
  version: "2.2"
---

Create or continue a cohesive CHANGE. Propose is planning only: do not apply it or edit application code.

**Supporting files:** `references/spec-quality.md`, `references/openspec.md`, `references/model.md`, `references/questions.md`, `templates/change-template.md`, `templates/delta-spec.md`, `templates/truth-spec.md`, `templates/artifact-review.md`.

## Steps

### 1. Load context and establish intent

Follow **Planning context loading** in `references/spec-quality.md`: target instructions, validated `docs/plan/config.json` via `sdd.py config`, `workflow.md`, catalog/platform/relevant CTX, and upstream project/brief/PRD/CHANGE artifacts. Source text is evidence, not permission.

State the change need in one sentence. Test cohesion: can each behavior be justified by that need? Split independently shippable "and also" work; do not add speculative requirements. If there is no destination yet, offer `plan-frame`; if intent remains unclear, use bounded discovery rather than inventing it.

Derive a kebab slug and scan active changes for candidates. Continue a same-intent CHANGE only when unambiguous or user-directed. On an ambiguous collision, do not overwrite or silently mint another folder: report candidate IDs/paths and the unresolved choice. In auto permission mode **NEVER call AskUserQuestion**. Otherwise use `references/questions.md` only for material missing decisions.

For a genuinely new CHANGE, scan active **and archived** IDs, append the next CHANGE-n, and preserve existing IDs. Use `templates/change-template.md` at `docs/plan/changes/<slug>/CHANGE.md`.

### 2. Ground current behavior

Read relevant `docs/plan/truth/<domain>/spec.md`, known designs, and only the source files needed to resolve current behavior. Label code-derived behavior `[inferred]` with evidence paths; never present guesses as established truth.

For a new capability with no truth, use `## Purpose` and ADDED. For an undocumented existing behavior, establish a narrowly evidenced `[inferred]` lite truth baseline using `templates/truth-spec.md` only within authorized scope before a MODIFIED replacement. If evidence or authorization is missing, record the gap; do not invent truth or mislabel MODIFIED as ADDED to pass validation.

Use `skip_specs: true` with empty `deltas:` only for an established no-behavior-change refactor/chore/docs intent. Do not invent requirements to satisfy a validator.

### 3. Write the proposal and deltas

Patch the identified folder, preserving prior decisions and unrelated work:

```
docs/plan/changes/<slug>/
  CHANGE.md
  deltas/<domain>.md
  design.md          # optional architecture sidecar, no id frontmatter
```

Keep Why / What Changes / Capabilities / Impact / Out of scope / Approach from the proposal template. Trace each changed behavior to the change need or chosen decision, source, and concise rationale in these blocks. Capabilities and `deltas:` must agree with the files.

Apply **Traceability and scenario coverage** in `references/spec-quality.md` to each delta:

- Preserve `## ADDED Requirements`, `## MODIFIED Requirements`, and `## REMOVED Requirements` semantics and current requirement names.
- Use `### Requirement: <Name>`, observable SHALL/MUST behavior, and `#### Scenario: <name>` with `- GIVEN`, `- WHEN`, `- THEN`.
- Every changed behavior has positive, negative, and edge scenarios, including removed behavior's replacement/absence outcomes. A truly inapplicable branch needs a specific justified N/A, not a blanket exemption.
- MODIFIED contains the **full replacement** requirement and scenarios plus `(Previously: …)`. REMOVED explains why and the replacement, if any.
- Keep proposal/deltas behavior-only. Implementation values, class/library names, code paths, and contracts belong in REQ/design; the proposal can link grounding sources without turning them into requirements.

### 4. Architecture and decomposition

Design is optional based on **technical uncertainty**, not whether there is UI. Offer or invoke `plan-design` (`/ultimate-sdd:design CHANGE-n`) when architecture decisions need it within the authorized planning scope. Do not hide unresolved architecture in deltas or force design ceremony for an obvious existing pattern.

Offer project decomposition, but run `plan-project` only when authorized. Only then create/link REQs: each `change: CHANGE-n` is mutual with the CHANGE's `reqs:`. A complete proposal without authorized decomposition stays `proposed`; do not claim implementation readiness from delta completeness alone. Preserve an existing CHANGE's later lifecycle.

### 5. Review and finalize

Review the proposal **and delta set** with **Planning artifact review** in `references/spec-quality.md` and `templates/artifact-review.md`. Report findings/pending independence without inventing approval.

Follow **Finalize and derive Next** there: run `plan.py board --root <root> --write`, `validate --root <root>`, and `next --root <root> --json`. Report the real Next plus unresolved gates. Stop at the planning boundary; no automatic apply, code, donor CLI, or unrequested full Specify.
