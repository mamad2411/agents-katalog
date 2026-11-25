---
name: ktdd
description: Combine Karpathy-style coding guardrails with TDD (RED→GREEN→scoped refactor). Use Karpathy always; use TDD when changing behavior.
---

# ktdd (Karpathy + TDD)

This skill merges two compatible modes:

- **Always-on guardrails (Karpathy)**: think first, keep it simple, make surgical changes, and verify with concrete success criteria.
- **TDD loop (when changing behavior)**: plan → get user approval → RED → GREEN → **scoped** refactor.

## Mode selection

Use **TDD mode** when the user is asking for a change in **observable behavior**, e.g.:
- Add a feature
- Fix a bug
- Refactor that changes behavior or is risky
- Add validation / parsing rules / edge-case handling

Use **Karpathy-only (judgment) mode** for **trivial** work, e.g.:
- Typos, doc edits
- Pure formatting
- One-line config changes that don’t change runtime behavior

If uncertain whether behavior is changing, stop and ask for clarification **before** coding.

## Always-on guardrails (Karpathy)

### Think before coding
- State assumptions explicitly.
- Surface trade-offs if multiple approaches exist.
- If something is unclear, stop and ask.

### Simplicity first
- Minimum code that solves the request.
- No speculative features or “flexibility” that wasn’t asked for.

### Surgical changes
- Touch only what’s necessary for the request.
- Don’t refactor adjacent code “because it’s there”.
- Clean up only what your change made unused/broken.

### Goal-driven execution
- Define success criteria that can be verified (tests, CLI output, repro steps).
- Loop until verified.

## TDD mode (behavior changes)

### Hard planning gate (REQUIRED)

Before writing **any** test or implementation code:
- Propose the **public interface** (what callers use).
- Propose a short **prioritized behavior list** (what to test).
- Wait for explicit user approval to proceed.

Do **not** write test code until the user approves the behavior list.

### Load the TDD reference pack (REQUIRED)

Before writing the first failing test in a TDD session, read these files in this folder:
- `tests.md`
- `mocking.md`
- `interface-design.md`
- `deep-modules.md`
- `refactoring.md`

### Tracer-bullet vertical slicing (no horizontal slices)

Work in vertical slices:

- **RED**: write one test for one behavior → it fails
- **GREEN**: write the minimum code to pass that test → it passes

Rules:
- One test at a time.
- Tests verify **behavior through public interfaces**, not internal wiring.
- Avoid over-mocking; mock only at system boundaries.

### Scoped refactor (resolves Karpathy vs TDD tension)

After GREEN (and only after GREEN):
- Refactor only code **touched by the current test cycle** or code that the new change made obviously problematic.
- Do not do drive-by refactors in unrelated areas.
- Keep tests on public behavior; refactors shouldn’t require test rewrites unless behavior changed.

