---
name: second-brain-pipeline
description: Classify and organize Second Brain atoms into PARA/CODE structures with confidence and conflict flags.
---

# Second Brain Pipeline

## Purpose

Classify and organize Second Brain knowledge atoms into PARA structures with explicit confidence and conflict flags after Sync Work ingest.

Use this skill when processing Second Brain atoms after Sync Work.

## Capture

- Identify whether each atom is a task, risk, decision, insight, dependency, or skip.
- Preserve source facts. Do not invent business context that is not present in title, summary, labels, source provider, or metadata.
- Mark `skip=true` for noise, empty records, duplicates, or records that are not useful organizational memory.

## Organise

- Assign `area_key` only when the business vertical is clear.
- Assign `para_bucket` using PARA: project for time-bound outcomes, area for ongoing responsibility, resource for reference material, archive for stale/closed records.
- Use `confidence < 0.6` and `conflict_flag=true` when the atom has mixed signals or weak vertical evidence.
- Human approval remains the gate for proposals and materialization.

## When to Use

- After Sync Work ingest completes and atoms need agentic classification.
- When reviewing unclassified org-visible atoms via `second_brain_list_unclassified`.
- When suggesting classification metadata with `second_brain_classify_atom` without materializing changes.

## When NOT to Use

- Direct planning materialization without a human-approved proposal.
- Per-agent CML memory workflows (use **syncolab-cognitive-memory** instead).
- Arbitrary doc search without Second Brain atom context.

## Expected Outcome

- Capture output with `signal_type`, `urgency`, `skip`, and `dimensions`.
- Organise output with `area_key`, `para_bucket`, `confidence`, `conflict_flag`, and `mapped_entity_type`.
- Weak or mixed signals flagged for human review instead of forced classification.

## Workflow

1. List or search candidate atoms (`second_brain_list_unclassified`, `second_brain_search_atoms`).
2. Run **Capture**: classify `signal_type`, `urgency`, `skip`, and `dimensions` from source facts only.
3. Run **Organise**: assign `area_key`, `para_bucket`, `confidence`, `conflict_flag`, and `mapped_entity_type`.
4. Use `second_brain_classify_atom` for suggest-only review; do not materialize without pipeline or human approval.
5. Surface proposals for human approval before planning materialization.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Full Second Brain tools | Inspect atoms, proposals, and classification candidates. |
| Read-only | List and search; do not materialize organise results without pipeline approval. |
| No integration | State limitation; do not fabricate atom metadata. |

### Related tool sets

- `second-brain`
- `planning`
- `internal-wiki`

## Output Format

Report:

1. Atoms processed and stages completed (Capture / Organise).
2. Classification results with confidence and conflict flags.
3. Items skipped or deferred for human review.
4. Recommended next steps (proposal review, re-classify, or materialization).

## Quality Bar

- Ground every classification in atom title, summary, labels, provider, or metadata.
- Prefer `conflict_flag=true` over guessing when signals are weak.
- Concise summaries unless the user asked for detail.

## Safety and Boundaries

- Do not invent business verticals or PARA buckets without evidence in the atom.
- Prefer `conflict_flag=true` over guessing when signals are weak.
- Proposal approval and task materialization remain human gates.
