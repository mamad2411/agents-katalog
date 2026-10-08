# Classify Source Authority

<!-- svl-skill-kind: application -->
<!-- svl-skill-execution: llm_interpreted -->

## Purpose

Govern the `classify_source_authority` memory blueprint procedure.

## When to use

- Use when building, reviewing, or operating the governed memory blueprint procedure.

## Inputs

- Project memory blueprint context.
- Relevant source, claim, authority, policy, or retrieval request.

## Procedure

1. Inspect the relational authority context and applicable policy.
2. Treat LLM outputs as claims until validation policy allows canonical writes.
3. Preserve provenance, conflicts, authority status, and audit expectations.
4. Keep graph, vector, and wiki outputs as projections or retrieval/rendering surfaces.

## Forbidden

- Do not write canonical truth outside the relational authority ledger.
- Do not treat vector, graph, or wiki output as truth by itself.
- Do not create scripts unless this skill owns and justifies the deterministic helper.

## Completion gates

- Sources and provenance are explicit.
- Authority status and conflicts are explicit.
- Audit event expectations are explicit.
- No loose scripts are introduced.

## Outputs

- Authority domain and source rule classification

## Allowed scripts

- None by default.

## Verification commands

- `svl memory blueprint audit .`
- `svl skills audit .`

## Related SvL rules

- SVL-MB001
- SVL-MB010
- SVL-SK001
