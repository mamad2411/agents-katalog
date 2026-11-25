# Windrunner Skills

Windrunner skills convert risky changes into bounded, reviewable, survivable work. Use them when the question is not merely "can this ship?" but "how do we keep other people safe while it ships?"

## Available skills

- [`pr-shield.md`](./pr-shield.md) — produce the merge packet for a risky PR: blast radius, reviewer hotspots, rollout plan, and rollback plan.
- [`guardrail-audit.md`](./guardrail-audit.md) — audit defaults, validation, limits, idempotency, kill switches, and other safety rails around a change.

## Usage contract

1. Pick the narrowest skill that matches the problem.
2. Ask for concrete edits, checks, and artifacts, not generic caution.
3. Prefer small guardrails with clear ownership over broad procedural theater.
4. If the risk cannot be evaluated from the available evidence, escalate to Truthwatcher.
