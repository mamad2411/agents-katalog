---
name: req-specify
description: >
  Specify or refine a REQ into an implementation-ready spec with clarifying
  questions, exact values, Given/When/Then acceptance criteria, and a 1–5
  readiness score. Use when the user says specify REQ, refine a requirement,
  click Specify, start the Specify→Refine→Build pipeline, or runs
  /ultimate-sdd:specify or /ultimate-sdd:refine.
license: MIT
metadata:
  author: andrewr303
  version: "2.0"
---

Turn a REQ into a technical build contract. Nothing is implemented and no TASKs are written here.

**Supporting files:** `references/spec-quality.md`, `references/readiness.md`, `references/questions.md`, `references/model.md`, `templates/req-template.md`, `templates/req-question-bank.md`, `templates/artifact-review.md`.

## Modes

- **Specify** — REQ is `idea` / `framing` / missing body.
- **Refine** — REQ already has a contract; patch gaps, accept/reject material suggestions, re-score.

Use Refine when requested or when an existing contract has listed gaps. Preserve its body, metadata, FR/AC IDs, accepted decisions, and lifecycle in either mode.

## Steps

### 1. Load

Follow **Planning context loading** in `references/spec-quality.md`: target instructions, validated `docs/plan/config.json` via `sdd.py config`, `workflow.md`, catalog/platform/relevant CTX, project/brief/PRD, and parent EPIC. Read the target REQ before patching. Resolve a `SPEC-n` alias once through `references/model.md`; require an unambiguous REQ, not an EPIC.

If `change: CHANGE-n` is linked, read its proposal, deltas, relevant truth, and optional `changes/<slug>/design.md`. Also read optional `reqs/REQ-n-design.md`. FRs implement the upstream behavior, not a parallel contract. Read actual existing files/manifests/APIs only where needed to ground the slice. Record conflicts instead of silently changing scope.

If blocked, report what blocks the REQ; specifying does not remove that gate. Infrastructure-only skips **UI Layout**, not architecture design. Offer `plan-design` (`/ultimate-sdd:design REQ-n`) when meaningful architecture decisions remain.

### 2. Resolve only material unknowns

Use `references/questions.md` and the question bank as aids, not a quota. Reuse known facts; ask about choices an implementer would otherwise invent, such as exact access boundaries, formats, failure outcomes, or TTL justified by the contract.

In auto permission mode **NEVER call AskUserQuestion**. "Just specify", "make it 5/5", or silence does not authorize dependencies or erase uncertainty. Use safe reversible `[assumed]` defaults only with source/rationale/boundary; unresolved scope, architecture, authorization, or other build-blocking questions cap readiness at **3**.

New library additions/replacements need actual user/host authorization before acceptance. This skill never installs dependencies.

### 3. Patch the spec

Use `templates/req-template.md` as the required shape, **not permission to overwrite an existing body**. Fill missing sections and patch changed passages; retain material accepted facts/tradeoffs, not all analysis. Keep stable FR/AC IDs and append new IDs without renumbering.

- Overview, Problem Statement, Solution, and Out of scope describe only this slice.
- UI Layout defines relevant regions/copy/states, or says "Infrastructure-only — no UI screens" with a separate architecture assessment.
- Source/decision ledger uses local D-n labels, source/evidence, agreed/assumed/unresolved state, affected FR/AC, and concise rationale/default.
- Every FR has SHALL/MUST behavior, exact technical values, and positive/negative/edge GIVEN/WHEN/THEN scenarios. Narrowly justified N/A is allowed only for truly inapplicable branches.
- Measurable NFRs name threshold, conditions, and actual verification method. Constraints cite real files, APIs, types, auth format, and env **key names only**; do not invent a platform contract.
- Coverage maps **each FR → decision/source → scenario kinds → AC IDs**. Technical AC are observable, stable, and complete enough to copy verbatim into TASKs later.
- Record config/workflow inputs, optional Design link, blockers, review state, and a changelog row.

### 4. Refine and re-score immediately

Apply `references/readiness.md`; update `readiness`, `readiness_gaps`, the five-dimension table, and build-blocker list whenever an answer, context, or patch changes the assessment. Overall is at least 1 and any build-blocker caps it at 3, irrespective of dimension count.

Offer concrete numbered patches with rationale only for real gaps. Interactive Refine can use **Accept / Reject / Edit**, **Accept all / Reject all / Save**; do not force extra approvals for already authorized edits. Rejected material patches stay as gaps. Auto/draft applies only safe in-scope defaults, labeled `[assumed]`, not automatic acceptance of risky decisions. Never increase a score by deleting the hard requirement.

### 5. Review, preserve lifecycle, finalize

Run **Planning artifact review** from `references/spec-quality.md` using `templates/artifact-review.md`; re-score for material findings. Pending/unavailable independence is not a pass. Flag downstream TASK contracts and prior evidence made stale by changes; do not rewrite TASKs or reuse stale implementation proof.

For planning-state REQs (`idea`, `framing`, `specified`, `ready`, `blocked`), recompute status from readiness and blockers: unfinished dependency → `blocked`; readiness ≥4 with no build-blocker → `ready`; otherwise `specified` or `framing` if still hollow. Keep `in-progress`, `review`, `done`, and `cancelled` lifecycles intact: specifying never promotes them back to `ready`. Record stale contracts/evidence and unresolved gates separately.

Follow **Finalize and derive Next** in `references/spec-quality.md`: run `plan.py board --root <root> --write`, `validate --root <root>`, and `next --root <root> --json`.

Show Specify · Refine · Start Building, the FR/UI/env/AC coverage, score/derived label/effort, gaps, review state, and actual derived Next. Start Building is not this skill; suggest Scope only when readiness and separate gates allow it. No TASK writing or application code.
