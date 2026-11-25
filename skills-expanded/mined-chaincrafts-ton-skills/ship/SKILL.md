# Ship

Use this skill when a TON feature is functionally complete and needs a disciplined path to release.

## Inputs

- change summary
- risk areas
- validation results
- rollout or communication notes

## Process

1. confirm the scope and affected user flows
2. run the required tests and environment checks
3. review migrations, config changes, and operational dependencies
4. capture release notes and rollback conditions

## Guardrails

- do not ship with unresolved correctness or security questions
- do not skip validation because a change looks small
- do not merge content or routing changes without checking canonical slugs and links

## Output

- a release-ready summary
- the checklist items that passed
- the remaining blockers, if any
