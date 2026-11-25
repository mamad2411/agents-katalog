---
name: codex-prompt-optimize
description: >
  Auto-trigger this skill when the user's input is vague, ambiguous, incomplete, or too brief to
  act on reliably in Codex. Indicators: single-sentence requests with no success criteria, missing
  target files or scope, unclear intent ("fix this", "make it better", "help me"), mixed unrelated
  asks in one message, or prompts that would force Codex to guess critical details. Do NOT trigger
  when the user's intent, scope, and done-state are already clear — even if the prompt is short.
user-invocable: false
---

# Codex Prompt Optimize

Intercept low-quality prompts before execution. Analyze user intent, infer missing structure, and
emit a well-formed Codex prompt — then execute the task using that prompt.

---

## When to Activate

Activate when the raw input matches **two or more** of these signals:

| Signal | Example |
|---|---|
| No explicit goal | "look at auth" |
| No scope or target files | "fix the bug" |
| No success criteria | "make it faster" |
| Ambiguous verb | "handle the errors", "clean this up" |
| Multiple unrelated asks | "fix login, add dark mode, update deps" |
| Zero context or constraints | "refactor the backend" |

Do **not** activate when:
- The prompt already contains a clear goal + scope + done-state, even in plain language.
- The user explicitly asks to explore or brainstorm (open-ended intent is the goal).
- The prompt is short but unambiguous (e.g., "run tests" or "format src/app.ts").

---

## Analysis Protocol

Extract four dimensions from the raw input. Mark each as **present**, **inferable**, or **missing**.

1. **Intent** — Map to: Diagnosis, Implementation, Fix, Review, Refactor, or Research.
2. **Scope** — Target files, directories, modules. Extract `@file` mentions and paths. If uninferrable, flag as missing.
3. **Constraints** — Check `AGENTS.md`, conversation context, language/framework conventions.
4. **Done-State** — What success looks like. Infer from intent category if unstated. If uninferrable, ask one targeted question — never more than one.

---

## Prompt Assembly

Build the optimized prompt using XML blocks. Always include `<task>` and `<default_follow_through_policy>`. Add conditional blocks by intent category:

| Intent | Add these blocks |
|---|---|
| Diagnosis | `compact_output_contract`, `verification_loop`, `missing_context_gating` |
| Implementation | `completeness_contract`, `verification_loop`, `action_safety` |
| Fix | `structured_output_contract`, `completeness_contract`, `verification_loop`, `action_safety` |
| Review | `structured_output_contract`, `grounding_rules`, `dig_deeper_nudge` |
| Refactor | `completeness_contract`, `verification_loop`, `action_safety` |
| Research | `structured_output_contract`, `research_mode`, `citation_rules` |

Optimization rules:
1. One task per prompt — split mixed asks, optimize the first, queue the rest.
2. Prefer contracts over nudges — "verify against requirements" beats "try really hard."
3. Keep the output contract minimal — ask only for what the user will use.
4. Never inflate complexity — if `<task>` alone is sufficient after rewriting, skip optional blocks.
5. Preserve user vocabulary and anchor to actual repo paths from `AGENTS.md`.

---

## Execution Flow

```
User input → Quality gate (≥2 signals?) ─── No ──→ Pass through
                    │ Yes
                    ▼
            Extract 4 dimensions
                    │
                    ▼
            Any uninferrable? ─── Yes ──→ Ask ONE question
                    │ No
                    ▼
            Assemble XML prompt
                    │
                    ▼
            Emit summary → Execute
```

Summary output before executing:

```
Prompt optimized: [what was clarified]
Intent: [category]  Scope: [files/modules]  Done: [criteria]
```

Proceed immediately. Do not ask for approval unless a clarifying question was needed.

---

Reusable XML block templates live in [references/prompt-blocks.md](references/prompt-blocks.md).
End-to-end optimization examples live in [references/optimization-recipes.md](references/optimization-recipes.md).
Common anti-patterns to detect and correct live in [references/anti-patterns.md](references/anti-patterns.md).
