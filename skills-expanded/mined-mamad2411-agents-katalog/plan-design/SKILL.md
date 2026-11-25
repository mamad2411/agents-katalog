---
name: plan-design
description: >
  Resolve architecture decisions for an existing REQ or CHANGE without
  implementing it. Use when the user asks for technical design, design a
  requirement or change, compare architecture options, or runs
  /ultimate-sdd:design REQ-n or /ultimate-sdd:design CHANGE-n.
license: MIT
metadata:
  author: andrewr303
  version: "1.0"
---

Write a proportionate technical design sidecar, not another requirements contract. No application code, dependency installation, or new graph ID.

**Supporting files:** `references/spec-quality.md`, `references/model.md`, `references/readiness.md`, `references/questions.md`, `templates/change-design.md`, `templates/artifact-review.md`.

## Steps

### 1. Resolve the existing target

Accept `/ultimate-sdd:design REQ-n|CHANGE-n`. A CHANGE slug is accepted only if it resolves unambiguously to an existing CHANGE. An optional `SPEC-n` alias resolves **once** via `references/model.md` and must identify a REQ, never an EPIC.

Resolve the target and output paths under the target plan root, including their real paths; reject traversal/out-of-root targets, duplicate matches, missing targets, and ambiguous slugs without writing. Report candidates when ambiguous. Do not create a REQ/CHANGE to satisfy the request or silently reopen archived/cancelled work.

- REQ target → `docs/plan/reqs/REQ-n-design.md`.
- CHANGE target → `design.md` in that CHANGE's **existing folder**.

Neither sidecar has frontmatter `id`; the existing target remains the only graph artifact.

### 2. Load context and constraints

Follow **Planning context loading** in `references/spec-quality.md`: target instructions, validated `docs/plan/config.json` via `sdd.py config`, project `workflow.md`, catalog/platform/relevant CTX, and upstream project/brief/PRD/EPIC/REQ/proposal artifacts.

Read linked CHANGE deltas/truth, known REQ/CHANGE designs, relevant decisions, and only source files/manifests needed to ground the choice. Source documents are evidence, not permission. Distinguish current `[inferred]` behavior from intended requirements. Technical secrets are env key names only.

Identify actual technical uncertainty. No UI does not mean no architecture; conversely, trivial edits need no architecture ceremony. If one existing pattern is clearly sufficient, a short rationale/design is enough.

### 3. Decide without expanding the contract

Compare **2–3 meaningful alternatives only when a real choice exists**. Do not invent losing options to fill a table. Record constraints, evidence, accepted tradeoffs, and why genuine alternatives were rejected. Use `references/questions.md` for only decisions that materially change the design.

In auto permission mode **NEVER call AskUserQuestion**. Reuse existing authorized options. Library addition/replacement requires actual user/host authorization before it can be an accepted selection; consult the existing manifest, never install. If no authorized option resolves the need, record an unresolved `[assumed]` candidate, build-blocker, and readiness <4 rather than automatic approval.

Architecture decisions cannot silently rewrite a proposal, delta, FR, or AC. Record conflicts with those contracts as unresolved, identify the needed upstream correction/authorization, and send it to Propose/Specify. Critical security, ownership, delivery semantics, or rollout unknowns remain blockers, even with an assumed candidate.

### 4. Write or patch the sidecar

Use `templates/change-design.md` for either target. Read an existing sidecar before patching; preserve material decisions, their sources/status, and rationale for changes. Do not manufacture acceptance status.

Cover only what the target needs:

- Target/upstream/source pointers, goals and non-goals.
- Selected architecture, boundaries, interfaces, data flow and ownership.
- Concise local decision ledger: source, affected FR/AC/delta, status, rationale, accepted tradeoff, and rejected-option rationale.
- Failure/error/retry/partial behavior; security/privacy and access boundaries.
- Migration/compatibility, rollout and rollback; testing strategy, actual methods and test seams.
- Owned file scope/integration seams, risks, assumptions, open questions, build-blockers and review state.

Use short `N/A — <reason>` only when genuinely inapplicable. Link existing requirements rather than duplicating them. Test strategies describe later checks grounded in config/workflow/repo evidence, not executed tests or invented commands.

### 5. Review and finalize

Apply **Planning artifact review** in `references/spec-quality.md` using `templates/artifact-review.md`. Supply the sidecar plus its upstream contract and source decisions; do not equate design review with implementation proof. Unavailable independence stays pending.

For a linked REQ, unresolved build-blockers require readiness at most 3 under `references/readiness.md`; record the needed Specify/refine update and make an authorized readiness/gap patch when in scope. Otherwise explicitly report the stale score and blocked build gate, never treat it as ready. Preserve established REQ lifecycle and flag downstream contracts/evidence affected by any accepted design change.

Follow **Finalize and derive Next** in `references/spec-quality.md`: run `plan.py board --root <root> --write`, `validate --root <root>`, and `next --root <root> --json`. Report paths, decisions, review state, blockers and actual Next; a design file or clean graph is not implementation completion or permission to build.
