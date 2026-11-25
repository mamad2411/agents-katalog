---
name: simplify
description: Simplify code, plans, architectures, or workflows by removing unnecessary parts, reducing coupling, and preserving verified behavior. Use when the user asks to simplify, reduce complexity, cut scope, refactor for clarity, streamline a plan, or apply first-principles cleanup before implementation or review.
origin: ECC automation-pack
---

# Simplify

Use this skill when the work is too complicated, over-designed, duplicated, slow to explain, or hard to verify.

## Goal

Reduce the system to the smallest version that still satisfies the real requirement.

Do not make cosmetic rewrites. Simplification must improve one or more of:

- fewer moving parts
- clearer ownership boundaries
- smaller public API surface
- fewer dependencies or configuration knobs
- less duplicated logic
- easier tests and verification
- lower operational risk

## Workflow

1. State the target behavior that must remain unchanged.
2. Identify complexity sources:
   - unused requirements
   - duplicated abstractions
   - premature generality
   - hidden mutable state
   - unclear error paths
   - excessive configuration
3. Propose the smallest simplification that preserves behavior.
4. Apply changes in small, reversible steps.
5. Verify with the nearest reliable checks: tests, typecheck, lint, build, or manual reproduction.

## First-Principles Questions

Ask these before editing:

- What requirement would break if this part disappeared?
- Is this abstraction carrying real variation or imagined future variation?
- Can the same behavior be expressed with fewer states, branches, files, or dependencies?
- Is this code compensating for an unclear boundary elsewhere?
- Can a test lock the behavior before simplifying it?

## Output

For non-trivial work, report:

- what was removed or merged
- what behavior was preserved
- what checks were run
- what complexity remains and why

## Guardrails

- Do not remove security checks, validation, logging needed for diagnosis, migrations, or compatibility without explicit evidence.
- Do not flatten architecture just because it has layers; remove layers only when they do not enforce a useful boundary.
- Do not change public behavior unless the user explicitly asks for a behavior simplification.
