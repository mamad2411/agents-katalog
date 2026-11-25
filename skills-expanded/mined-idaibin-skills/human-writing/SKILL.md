---
name: human-writing
description: "Draft, rewrite, proofread/校对, or adapt source-grounded prose for the requested document type while preserving meaning; owns wording, not test coverage, API contracts, or product facts; not translation-only work or fiction."
---

# Human Writing

## Entry Gate

Produce writing that preserves the requested meaning, audience, authority, and evidence boundary. Resolve the requested operation (draft, proofread, local edit, structural rewrite, or adaptation), the reader’s task and existing knowledge, output format, content type, and authoritative source before writing; a file extension or directory alone never decides the owner. Require source material or clearly label assumptions; do not convert a style request into unauthorized publication or new factual/product decisions.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Choose drafting/editing operation and content mode | [content modes](references/content-modes.md) | Audience-fit output |
| Message/email, status/notice, product/release copy, or analytical commentary | [practical forms](references/practical-forms.md) | Reader-specific information and action |
| Typed document brings another owner's semantics or a workspace format authority (test cases, API docs, manuals, Word/Excel deliverables) | [typed-document rules](references/content-modes.md#typed-document-boundaries) | Minimal compatible composition |
| Draft or edit from supplied source material, or facts/attribution matter | [fact integrity](references/fact-integrity.md) | Evidence-bound prose |
| Tone/style/platform calibration matters | [style diagnostics](references/style-diagnostics.md) and/or [platform calibration](references/platform-calibration.md) | Calibrated revision |
| Explain reasoning or make revisions transparent | [reasoning/explanation](references/reasoning-and-explanation.md) and/or [revision transparency](references/revision-transparency.md) | Traceable rationale |
| Quality check/examples are needed | [quality rubric](references/quality-rubric.md) and/or [before/after examples](references/before-after-examples.md) | Bounded quality pass |

## Invariants

- Preserve source fact/claim boundaries and name uncertainty; never fabricate citations or experience. Before returning source-based writing, apply the source-based editing check in fact integrity to each artifact or candidate.
- Typed-document semantics stay with their owners: test coverage with the testing workflow, wire contracts with the API-contract workflow, product and project facts with their accepted authority; this Skill owns their prose presentation.
- Keep writing, product/technical decisions, external sends, and Git delivery separate.
- Return the requested format and scope without silently expanding the audience or claim.

## Output Map

For draft, rewrite, proofreading, or adaptation, return the requested finished artifact
only. For diagnosis, return the concrete problem, impact, and editing direction. Add
source/assumption disposition, unresolved facts, alternatives, or revision rationale
only when the user requests them or the safe supported artifact requires a named gap.

## Reference Map

- Load each condition-specific reference named in the Route Map only when applicable.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
