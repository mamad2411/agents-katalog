---
name: verification-first-delivery
description: Use when shipping changes, building automations with side effects, or planning long-running agent work. Trigger for code changes, integrations, migrations, device or network debugging, or any task where the agent needs deterministic evidence and rollback paths.
---
# Verification-First Delivery

Goal: make execution safe by creating deterministic evidence, checkpoints, and rollback before large actions.

## Design procedure
1. Define done in externally checkable terms.
2. Define preconditions and assumptions.
3. Design the smallest reversible probe.
4. Add validators, tests, or graders.
5. Capture artifacts and logs.
6. Define rollback and retry strategy.

## Required checks
- dry-run or read-only probe first when possible
- structured output or schema validation
- tests or executable validators
- timeouts and retries for external calls
- snapshot before destructive change
- idempotency or duplicate protection
- explicit handoff if human approval is required

## Output
### Preconditions
### Probe
### Validators
### Evidence to capture
### Rollback
### Done criteria
