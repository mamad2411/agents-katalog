---
name: simplify
description: Make a behavior-preserving quality pass over changed files for reuse, clarity, types, dead code, structure, and accidental inefficiency. Use after significant implementation, before a PR, when the user asks to simplify or clean up a diff, or as the closing pass of $implement.
---

# Simplify

Never change observable behavior. Report a real bug instead of hiding its fix inside cleanup, because a semantic change invalidates prior verification. Limit edits to the target diff and files that must change with it; do not perform drive-by refactors.

Read every changed file in full and every applicable `AGENTS.md`, then inspect:

- **Reuse** — Search for existing utilities, components, and types before adding another. Consolidate repeated code only when it represents the same concept and extraction reduces total complexity; two call sites alone do not justify an abstraction.
- **Dead code** — Remove unused imports, variables, branches, commented-out code, and debug logging introduced or exposed by the diff. Use configured project tooling such as Knip and linters when available. Do not add a dependency for this pass, and corroborate analyzer output against dynamic imports, generated code, exports, tests, and external consumers.
- **Comments** — Remove narration, stale history, and comments that merely restate code. Preserve intent, invariants, constraints, and non-obvious tradeoffs.
- **Naming and structure** — Ensure names describe current behavior and flatten avoidable nesting with early returns when clearer.
- **Types** — Remove unjustified `any`, broad object types, and unchecked assertions or casts. Preserve `unknown` at untrusted boundaries and narrow or validate it immediately. Use configured cycle analysis when available; do not assume Madge is installed.
- **Efficiency** — Remove accidental quadratic work and repeated parsing or fetching. Avoid speculative micro-optimization.

Run the smallest relevant tests, lint, typecheck, and diagnostics required by the repository and changed code. Summarize what changed, what was intentionally left alone, and any bugs reported.

- Prefer readable code over compact cleverness.
- Follow an established repository pattern even when another style is personally preferable.
- Leave unproven fallback, compatibility, and legacy-path removal out of scope. Suggest a separately scoped `$improve-vibecode` audit when broader evidence-backed cleanup is warranted.
