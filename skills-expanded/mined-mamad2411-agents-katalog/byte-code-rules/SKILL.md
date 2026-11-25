---
name: byte-code-rules
description: Apply Your ByteDance engineering behavior rules for writing, reviewing, refactoring, planning, or executing code in Byte OS. Use with byte-build, byte-plan, byte-review, byte-iterate, byte-auto, or any coding task to avoid overengineering, keep edits surgical, surface risky assumptions, and define verifiable success criteria.
---

# Byte Code Rules

This is the Byte OS engineering guardrail layer. It adapts the MIT-licensed Karpathy-inspired coding guidelines from `forrestchang/andrej-karpathy-skills` into the Your ByteDance workflow.

## Core Rules

1. Think before coding.
   - Inspect the relevant project files before editing.
   - State assumptions only when they affect the implementation or product decision.
   - If multiple interpretations would produce different code, ask or present the tradeoff before committing.
   - Push back when a simpler or safer approach better serves the product goal.

2. Simplicity first.
   - Build the smallest thing that satisfies the plan, acceptance criteria, and user request.
   - Do not add speculative features, generic frameworks, unused configuration, or single-use abstractions.
   - If the implementation becomes much larger than the problem, simplify before continuing.
   - Prefer existing project patterns, dependencies, and local helpers.

3. Surgical changes.
   - Keep every changed line traceable to the user request, current plan, or verification need.
   - Match the surrounding style instead of restyling adjacent code.
   - Do not refactor, reformat, rename, or delete unrelated code.
   - Clean up only unused imports, variables, files, or comments created by the current change.
   - Mention unrelated dead code or design debt in logs or review notes instead of silently removing it.

4. Goal-driven execution.
   - Turn each coding task into concrete success criteria before implementation.
   - For bugs, reproduce the failure with a test or minimal check when practical, then make it pass.
   - For features, define acceptance criteria and verify the first user workflow.
   - Run the most relevant available tests, linters, type checks, builds, browser checks, or manual verification.
   - Record what was verified and what remains unverified.

## Byte OS Integration

- `byte-plan`: every engineering plan must include write scope, non-goals, acceptance criteria, and verification steps.
- `byte-build`: apply these rules before file edits, during implementation, and before marking a plan complete.
- `byte-review`: flag overengineering, broad unrelated edits, unverified success criteria, and hidden assumptions as findings.
- `byte-iterate`: each code change must map to evidence, an OKR, a review finding, a test failure, or real user feedback.
- `byte-auto`: keep the same rules even in one-click mode; speed comes from parallelism and clear state, not skipping verification.

## Tradeoff

These rules bias toward caution on non-trivial work. For obvious one-line fixes, apply the spirit quickly: make the minimal change, verify what is cheap to verify, and avoid unnecessary process.
