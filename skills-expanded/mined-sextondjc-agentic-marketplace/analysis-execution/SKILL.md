---
name: analysis-execution
description: Use when discovery work must produce traceable requirements, not just notes — covers structured discovery execution, assumption ledger, contradiction logging, synthesis, and requirement hardening.
---

# Analysis Execution

## Specialization

Execute structured discovery and produce traceable outputs: an assumption ledger, requirement candidates, contradiction log, open questions list, and a hardening-ready recommendation note.

This skill bridges the gap between discovery activities (interviews, research, spikes) and the requirement artifacts that downstream planning and engineering need. It does not perform the upstream discovery itself — it structures and hardens what discovery surfaces.

## Trigger Conditions

- Discovery work has produced notes, findings, or raw inputs and they must be converted into traceable requirement candidates.
- Assumption drift is a risk: multiple stakeholders are involved or inputs arrived at different times.
- An analysis phase is ending and design cannot begin until requirements are hardened.
- Contradictions exist between discovery inputs and must be logged and resolved before execution starts.

## Inputs

- Raw discovery inputs: notes, interview summaries, spike results, research outputs.
- Constraint list: known boundaries, technology decisions, and non-negotiables.
- Stakeholder list for assumption ownership.
- Originating plan or workstream ID for traceability.

## Required Outputs

| Output | Description |
|---|---|
| Assumption ledger | Named, owned assumptions with confidence level (High / Medium / Low) and validation status. |
| Requirement candidate list | Structured requirement statements with source, type (functional / non-functional / constraint), and acceptance shape. |
| Contradiction log | Any inputs that conflict, with disposition (resolved / deferred / escalated). |
| Open questions list | Unresolved questions blocking hardening, each with an owner and target resolution date. |
| Recommendation note | One synthesised recommendation for design handoff: what is hardened, what is deferred, and what must be resolved before execution. |

## Workflow

1. Collect all discovery inputs into a single intake list. Tag each with source and date.
2. Build the assumption ledger: extract every implicit or explicit assumption from inputs. Assign ownership and confidence.
3. Log contradictions: identify any two inputs that cannot both be true. Record disposition.
4. Draft requirement candidates: convert hardened inputs into structured requirement statements. Reference source input for traceability.
5. Populate the open questions list: anything blocking hardening gets a named owner and target date.
6. Write the recommendation note: state what is ready for design, what is deferred, and what needs escalation.
7. Verify the originating plan or workstream ID appears on each output artifact.

## Done Criteria

- Assumption ledger exists with confidence levels and named owners.
- Requirement candidate list has at least one traceable source reference per item.
- Contradiction log is complete: all identified contradictions have a disposition.
- Open questions list identifies blockers with owners.
- Recommendation note is present and references the plan or workstream ID.

## References

- Related skills: `task-research`, `critical-thinking`, `writing-plans`
