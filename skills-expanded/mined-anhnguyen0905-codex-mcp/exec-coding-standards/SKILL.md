---
name: exec-coding-standards
description: Language-agnostic senior-developer coding standards to embed into every Codex execution prompt — KISS/DRY/YAGNI, immutability, error handling, validation, naming, structure limits.
---

# Coding Standards (embed into Codex prompts)

These rules go INTO the `codex_execute` prompt so Codex writes to senior standard. Include the block below (plus the matching language skill) in every execution task.

## Standards block

```
Coding standards (mandatory):
- KISS: simplest solution that works; no premature optimization or speculative abstraction (YAGNI).
- DRY: extract repeated logic; but prefer a little duplication over the wrong abstraction.
- Immutability: return new values instead of mutating inputs/shared state.
- Errors: handle explicitly at every level; never swallow silently; user-facing messages friendly,
  logs detailed; fail fast on programmer errors.
- Validation: validate ALL external input (user, API, file, env) at the boundary with clear failures.
- No hardcoded secrets/config — env vars or config files; validate presence at startup.
- Naming: descriptive; booleans read as predicates (is/has/can/should); constants UPPER_SNAKE_CASE.
- Structure: functions < 50 lines, files < 800, nesting < 4 (use early returns).
- Comments: only for constraints code can't express (the "why"); no narration of the obvious.
- Match the existing codebase's style, structure, and idioms over any personal preference.
- No debug prints (console.log/print) left in production code paths.
```

## Why embedded, not assumed

Codex doesn't see Claude's skills or the user's global rules — the prompt is the only channel. A plan without embedded standards produces stylistically alien code that fails review round 1 on preventable findings.
