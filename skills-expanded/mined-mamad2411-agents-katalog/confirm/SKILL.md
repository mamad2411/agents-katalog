---
name: confirm
description: Pause before writing code to summarize understanding of the task, ask clarifying questions, and get explicit user confirmation. Use when the user invokes /confirm, asks you to confirm before coding, wants to align on approach first, or says "don't write code yet".
---

# Confirm

Before writing any code, align with the user on what the task actually is.

## Workflow

1. **Summarize understanding** — In your own words, state:
   - The goal (what outcome the user wants)
   - The scope (what's in, what's out)
   - The approach you'd take (key files, structure, libraries)
   - Any assumptions you're making

2. **Ask clarifying questions** — Only ask about things that genuinely change the implementation. Skip questions whose answers won't affect the code. If you have no real questions, say so.

3. **Wait for confirmation** — Stop. Do not write or edit code. Do not run commands that modify state. Ask **"OK to proceed?"** and wait for the user to either confirm, correct, or redirect.

4. **Proceed only after explicit confirmation** — A "yes", "go ahead", "looks good", or similar. Silence or tangential replies are not confirmation.

## Rules

- **No code edits before confirmation.** Read-only exploration (Read, Grep, Glob) is fine and often necessary to write a useful summary.
- **Keep the summary tight.** A few bullets, not paragraphs. The user should be able to scan it and spot misunderstandings fast.
- **Surface disagreements early.** If the user's request seems wrong or risky, say so in the summary rather than silently complying.
- **One round is usually enough.** Don't loop endlessly — once the user confirms, get to work.

## Format

```
**Understanding:**
- Goal: ...
- Scope: ...
- Approach: ...
- Assumptions: ...

**Questions:**
1. ...
2. ...

OK to proceed?
```
