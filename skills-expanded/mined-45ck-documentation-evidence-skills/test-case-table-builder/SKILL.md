---
name: "test-case-table-builder"
pack: "documentation-evidence-pack"
purpose: "Generate test case tables with IDs, preconditions, inputs, expected results, and evidence hooks."
inputs: ["requirements", "scenario list", "expected behaviors", "environment assumptions"]
outputs: ["test case table", "coverage notes", "evidence hooks"]
handoffs: ["test-plan-writer", "traceability-matrix-writer", "bug-report-writer"]
---
# test-case-table-builder

## Purpose
Generate test case tables with IDs, preconditions, inputs, expected results, and evidence hooks.

## Trigger this skill when
- A durable documentation or evidence artifact is needed for review, submission, audit, or handover.
- You need clearer linkage between requirements, design, testing, defects, decisions, or findings.
- Existing documentation is fragmented, inconsistent, or weakly evidenced.

## Expected inputs
- requirements
- scenario list
- expected behaviors
- environment assumptions

## Deliverables
- test case table
- coverage notes
- evidence hooks

## Operating procedure
1. Clarify the artifact boundary, audience, and review objective.
2. Separate known facts from assumptions, placeholders, and missing evidence.
3. Produce the skill-specific artifact in a form that can be reused directly.
4. Link the result to upstream and downstream artifacts where helpful.
5. Recommend the next best handoff instead of trying to do every document at once.

## Quality gates
- The output is specific to the current system, feature, or report context.
- Identifiers, references, and labels are internally consistent.
- Missing evidence or unresolved questions are made visible.
- The result is directly usable in a repo, report, appendix, or review packet.

## Handoff targets
- test-plan-writer
- traceability-matrix-writer
- bug-report-writer

## Output style
- Prefer structured, reusable artifacts over generic prose.
- Make IDs, labels, references, and evidence explicit where possible.
- Preserve traceability between related artifacts.
- Surface missing evidence or unresolved questions instead of inventing closure.

## Failure modes to avoid
- Do not fabricate evidence, references, or approval.
- Do not collapse requirements, decisions, tests, and findings into one undifferentiated blob.
- Do not leave identifiers or document links inconsistent.
- Do not confuse “described” with “verified”.
