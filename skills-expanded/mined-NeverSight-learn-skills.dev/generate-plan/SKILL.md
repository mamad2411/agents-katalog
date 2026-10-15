---
name: generate-plan
version: 5
description: >-
  Generate a phased implementation plan from a PRD — triggers like "generate a plan", "break down the PRD into phases", "tracer-bullet plan", "turn my PRD into phases". Reads a single `<cwd>/.plans/<feature>/prd.md`, writes `<cwd>/.plans/<feature>/plan.md` as tracer-bullet vertical slices (each phase a thin end-to-end cut through schema, API, UI, tests). Every phase contains `### What to build` plus `### Acceptance criteria` with `- [ ]` checkboxes — downstream implementer skills parse on this contract. One PRD → one plan; never aggregates. Hard-stops if no PRD exists at `.plans/<feature>/prd.md`.
---

# Generate Plan

Turn a single PRD into a phased implementation plan made of **tracer-bullet vertical slices**. Output is one file at `<cwd>/.plans/<feature>/plan.md`, sibling of the source `prd.md`.

## Inputs and outputs

**One PRD → one plan file. One invocation processes exactly one PRD.** Never aggregate multiple PRDs into a single plan; if the user wants that, redirect them to merge at the discussion stage and regenerate a single PRD.

- **Input:** `<cwd>/.plans/<feature>/prd.md` — a finalized PRD.
- **Output:** `<cwd>/.plans/<feature>/plan.md`. The `<feature>` slug **must equal** the source PRD's folder slug — keeps the PRD ↔ plan link 1:1.
- **No draft checkpoint.** One-shot — if interrupted mid-quiz, restart from step 1.

## Workflow

### 1. Discover the PRD

Glob `<cwd>/.plans/*/prd.md`.

- **Zero matches** → **hard-stop**. Tell the user: _"No PRD found under `.plans/<feature>/prd.md`. A plan needs a real PRD as grounding — a PRD must exist at `.plans/<feature>/prd.md` first, then re-run me."_ Do not accept an inline brief; do not fabricate a PRD.
- **One match** → use it. Capture the `<feature>` slug from its folder name.
- **Multiple matches** → AskUserQuestion, listing each feature with a one-line summary derived from its PRD's Solution section. The user picks **exactly one**. Reject any "do them all" request — this skill plans one PRD at a time.

Read the chosen PRD in full.

### 2. Guard the output

If `<cwd>/.plans/<feature>/plan.md` already exists, **stop** and ask whether to overwrite. Never silently overwrite. Only proceed on explicit confirmation.

### 3. Explore the codebase

Use Read / Grep / Glob to understand:

- Existing architecture and folder layout
- Established patterns (routing, data access, auth, testing)
- Integration layers a vertical slice will need to cut through
- Any prior art relevant to the modules listed in the PRD's Implementation Decisions

Skip this step **only** if the modules referenced in the PRD's Implementation Decisions were already explored earlier in this session.

### 4. Identify durable architectural decisions

Before slicing, extract the high-level decisions that won't churn during implementation. These go in the plan header so every phase can reference them:

- **Routes / URL patterns**
- **Database schema shape** — table or collection names, key relations
- **Key data models** — names only (no field-by-field detail; that goes in the slice)
- **Authentication / authorization approach**
- **Third-party service boundaries**

Pull these from the PRD's Implementation Decisions + your codebase exploration. If a decision is missing or ambiguous, ask the user before proceeding — do not invent.

### 5. Draft tracer-bullet vertical slices

Break the PRD's user stories into phases. Each phase is a thin **vertical** slice that cuts through every layer end-to-end.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests).
- A completed slice is demoable or verifiable on its own.
- Prefer many thin slices over few thick ones.
- Each slice maps to one or more user stories from the PRD.
- Do NOT include specific file names, function names, or implementation details that are likely to change as later phases are built.
- DO include durable decisions: route paths, schema shapes, data model names.
</vertical-slice-rules>

### 6. Quiz the user on granularity

Present the proposed breakdown as a numbered list. For each phase show:

- **Title** — short descriptive name
- **User stories covered** — references back to the PRD's numbered stories
- **Draft acceptance criteria** — 2–3 observable outcomes phrased as `- [ ]` checkboxes (see [REFERENCE.md](REFERENCE.md#acceptance-criteria-style) for the style)

Ask:

- Does the granularity feel right (too coarse / too fine)?
- Should any phases be merged or split further?
- Is the ordering correct? (Earlier phases should unblock later ones.)
- Do the draft ACs describe the right observable outcomes, or do any need rewording / adding / removing?

Iterate until the user explicitly approves the breakdown **and the ACs**. Do not write the plan file before approval. **If the user abandons the quiz** (asks to stop, walks away from approval, or rejects the framing entirely), exit without writing anything — leave no partial `plan.md` behind.

### 7. Validate phase shapes (pre-write gate)

Before rendering the file, assemble the plan in memory and verify it against the **Phase shape contract** in [REFERENCE.md](REFERENCE.md#phase-shape-contract). Each phase block must have:

- `## Phase N: <Title>` heading
- `**User stories:**` line
- `### What to build` section (2–4 sentences, end-to-end behaviour — no bold-label substitutions like `**Goal.**` or `**Slice contents.**`)
- `### Acceptance criteria` section with **≥1 `- [ ]` checkbox** — never zero, never prose, never `**Verification.**`
- Trailing `---` separator

Whole-file checks:

- Single trailing `---` followed by the `_Generated by `generate-plan` from `.plans/<feature>/prd.md`._` footer line
- **No appendix sections** between the last phase and the footer (coverage maps, summary tables, status notes) — those break the downstream `\n---\n` parser contract. Surface such artefacts inline in the conversation instead.

If any phase or the whole-file check fails, fix the offending block(s) internally and re-validate. **Do not write the file until every check passes.**

### 8. Write the plan file

Create `<cwd>/.plans/<feature>/` if missing (it should already exist beside `prd.md`). Write `plan.md` using the template in [REFERENCE.md](REFERENCE.md#plan-template) **exactly** — do not substitute bold-label paragraphs (`**Goal.**`, `**Slice contents.**`, `**Verification.**`) for the required `###` headings; downstream implementer skills parse on them. Confirm to the user with the absolute path and a one-line summary (`N phases, covering stories X–Y`).

## What NOT to do

- **Don't aggregate multiple PRDs into one plan.** One invocation processes exactly one PRD. If the user wants a multi-feature plan, ask them to merge at the discussion stage and regenerate a single PRD first.
- **Don't fabricate a PRD.** Hard-stop if none exists. Plans built on an inline brief drift from any future PRD that gets written.
- **Don't bake in volatile details.** No file paths, function names, or class names in the plan — they rot. Routes, schema names, and data model names are stable enough to include.
- **Don't substitute the template's `###` sections with bold-label prose.** `### What to build` and `### Acceptance criteria` (with `- [ ]` checkboxes) are part of the contract; downstream implementer skills parse on them. Headings like `**Goal.**`, `**Slice contents.**`, or `**Verification.**` in their place are a hard failure of step 7's validation gate.
- **Don't append extra sections after the last phase.** Coverage maps, summary tables, status notes, or any prose after the final phase block break the `\n---\n` parser contract that downstream tooling depends on. The rendered file must end with the single `---` separator and the `_Generated by …_` footer. Surface those artefacts inline in the conversation instead.
- **Don't silently overwrite.** An existing `plan.md` requires explicit overwrite confirmation.
- **Don't skip the quiz.** The user must approve the breakdown before the file is written.
- **Stay read-only except for the plan file.** This skill writes only `<cwd>/.plans/<feature>/plan.md` — no other files, no production code.
