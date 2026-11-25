---
name: typescript-strict-rules
description: Keeps TypeScript code strictly typed with no escape hatches. Use in any TypeScript project that wants the compiler to catch mistakes.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: rule
  category: conventions
  source: https://hermes-ide.com/prompts/typescript-strict-rules
  catalog: 2026.1002.0
---

# TypeScript strict rules

Apply these rules to files matching: `**/*.ts`, `**/*.tsx`.

- Never use `any`. Use `unknown` and narrow it.
- Do not silence the compiler with `@ts-ignore`; fix the type or use `@ts-expect-error` with a reason.
- Prefer `readonly` data and exhaustive `switch` statements over defaults that hide new cases.
