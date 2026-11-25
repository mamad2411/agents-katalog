---
name: rule-candidate
description: Draft a rule candidate as a standalone file in the project's gitignored candidates folder. No commitment. Promote later via /rule-review.
---

# Rule Candidate

Capture a candidate as a **standalone rule-shaped file** in the project's gitignored candidates folder. Promotion is later just a `git mv`. Never silently discard — keep the file even on rejection.

## Input

`<directive>` = one-line imperative ("Don't add Result<T> for expected failures") or empty for interactive.

## Steps

1. **Directive.** If args empty, ask via `AskUserQuestion` (free-text). Else use args verbatim.
2. **Category.** Infer prefix from directive keywords:
   - module structure, deps, abstraction → `arch-`
   - idiom, error handling, naming, control flow → `cq-`
   - how Claude behaves, when to ask, output format → `wf-`
   - config / file placement / tooling → `meta-`

   Ambiguous? `AskUserQuestion` with the four options.
3. **Slug.** Compute from directive — lowercase + hyphenate the main noun/verb, prepend the category prefix. Example: "Justify state mirrors" → wf-justify-state-mirrors.
4. **Signal.** Auto-fill from conversation context (e.g. "from /audit-architecture on `b24f06c..HEAD`"). Free-text if nothing fits.
5. **Dup check.** Glob `<project>/.claude/local/rule-candidates/*.md`, `~/.claude/rules/*.md`, and `<project>/.claude/rules/*.md` for similar slugs or directives. If close match found, ask: **merge** / **save with different slug** / **cancel**.
6. **Write file** at `<project>/.claude/local/rule-candidates/<slug>.md`. Create the folder if missing.

   Format (standard rule shape — promotion is just a move into `rules/`):

   ```markdown
   # <Title — capitalized form of slug>

   <Directive, one imperative sentence>.

   ## Why

   <1–2 sentences on the failure mode this prevents — only if non-obvious>

   ## How

   <Concise application guidance — only if non-obvious>

   <!-- Captured: YYYY-MM-DD from <signal> -->
   ```

7. **Report** the saved path: `Saved <path>. Promote via /rule-review.`

## Rules

- **Always per-project.** No project context = abort and ask the user to invoke from inside a project.
- **Path is `.claude/local/rule-candidates/`** — outside `rules/` on purpose, since rule discovery walks that tree recursively and would load every draft into every session. `.claude/local/` must be in `.gitignore` (one-time setup; `/rule-review` checks and proposes the entry).
- **Standalone file per candidate** — never a shared dump file. One slug = one file.
- **Don't auto-promote** — `/rule-review` and `/capture-rule` are the only gates.
- Be silent on success — one-line confirmation, no narration.
