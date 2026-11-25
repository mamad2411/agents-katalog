---
name: "evaluation-report-writer"
pack: "documentation-evidence-pack"
purpose: "Summarize evaluation methods, evidence, findings, limitations, and recommendations in a formal report structure."
inputs: ["evaluation objective", "method", "evidence", "findings/limitations"]
outputs: ["evaluation report", "limitations", "recommendations"]
handoffs: ["test-plan-writer", "appendix-assembler", "reference-integrity-checker"]
---
# evaluation-report-writer

## Purpose
Summarize evaluation methods, evidence, findings, limitations, and recommendations in a formal report structure.

## Trigger this skill when
- A durable documentation or evidence artifact is needed for review, submission, audit, or handover.
- You need clearer linkage between requirements, design, testing, defects, decisions, or findings.
- Existing documentation is fragmented, inconsistent, or weakly evidenced.

## Expected inputs
- evaluation objective
- method
- evidence
- findings/limitations

## Deliverables
- evaluation report
- limitations
- recommendations

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
- appendix-assembler
- reference-integrity-checker

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
