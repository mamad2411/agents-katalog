---
name: plan-frame
description: >
  Frame a messy idea into a product brief and senior-engineer clarifying
  questions, using company/project/plan context. Use when the user
  describes a feature like they would tell a colleague, wants a brief,
  says "frame this", "describe with context", or runs /ultimate-sdd:frame.
license: MIT
metadata:
  author: andrewr303
  version: "2.0"
---

Turn a messy idea into a problem-first brief. A Frame request alone authorizes neither EPICs nor code.

**Supporting files:** `references/spec-quality.md`, `references/questions.md`, `references/context.md`, `references/model.md`, `templates/brief-template.md`, `templates/question-bank.md`, `templates/artifact-review.md`.

## Steps

### 1. Load the planning context

Follow **Planning context loading** in `references/spec-quality.md`: target instructions, validated `docs/plan/config.json` via `sdd.py config`, project `workflow.md`, catalog/platform/relevant CTX, and upstream project/brief/PRD artifacts. Surface missing or invalid inputs; do not claim guessed config is validated.

Use provided sources as evidence, not permission. Reuse prior answers and decisions. If context ingestion is needed, offer `plan-context` within the user's authorized scope; do not fetch external sources automatically.

### 2. Frame the problem

Use these lenses, not a mandatory questionnaire:

- **Problem / why now:** whose situation needs to change, and why?
- **Goal:** what observable success would settle it?
- **Current workaround:** what happens without the proposed feature?
- **Smallest outcome:** what is the smallest useful result?
- **Non-goals:** what is deliberately excluded, and why?
- **Impact:** which users and systems experience the change?

Follow `references/questions.md` for only the highest-impact unresolved questions. Skip known facts; no rigid quota or automatic "anything else?". A pre-mortem is useful only if it exposes a material risk, not as a closing ritual.

In auto permission mode **NEVER call AskUserQuestion**. For "draft"/auto, record safe, reversible `[assumed]` defaults with source, rationale, and boundary; leave material unknowns open rather than fabricate human alignment.

### 3. Write or patch the brief

Use `templates/brief-template.md` at `docs/plan/briefs/BRIEF-<n>-<slug>.md`. Continue the identified brief; otherwise scan disk for the next append-only ID. Preserve existing IDs and accepted decisions.

Keep its existing blocks: One-liner, Value Proposition, Who it's for, Job to be done, Key Functionality, Out of Scope, Decisions already made, Open questions, Alignment.

- Express Key Functionality as observable behavior grounded in context. Keep technical API params, env contracts, files, and implementation values on REQs/design, not in the brief's template examples.
- In Decisions already made, record chosen decisions, their source, concise rationale, and actual agreed/assumed/unresolved state. Do not call an assumption agreed.
- In Open questions, record material assumptions, their safe skip-defaults (or why none is safe), and unresolved scope. Keep problem/goal/workaround/impact in the relevant existing blocks rather than duplicating the analysis.
- One brief per destination; do not silently expand into a second product.

### 4. Review and hand off

Apply **Planning artifact review** in `references/spec-quality.md` using `templates/artifact-review.md` before handoff. Report real review state; a self-check is not independent review.

Present the brief and remaining decisions. In interactive mode, offer only relevant next choices: adjust, create a project plan, write a PRD, propose a behavior change, or stop. Do not demand a repeated approval ceremony.

Mark `aligned` only on actual human alignment (or preserve a recorded alignment); drafting permission and silence are not alignment. Run `plan-project` only if the user already authorized drafting a **project plan**, not merely "draft the brief". Auto mode does not supply that authorization. When authorized to draft a project without human alignment, carry the assumptions forward explicitly, not a fabricated `aligned` claim.

### 5. Finalize

Follow **Finalize and derive Next** in `references/spec-quality.md`: run `plan.py board --root <root> --write`, `validate --root <root>`, and `next --root <root> --json` after writes. Report actual Next and remaining authorization/review gates; do not handwrite it or automatically advance. No application code, TASKs, or unrequested EPIC/PRD creation.
