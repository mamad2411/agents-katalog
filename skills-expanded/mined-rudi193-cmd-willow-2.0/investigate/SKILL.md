---
name: investigate
description: Systematic problem-solving — brainstorm new approaches or debug existing issues
---

@markdownai v1.0

# /investigate — Problem-Solving Framework

Two modes: design new solutions (brainstorm) or fix existing problems (debug).

## Brainstorm Mode — Before any plan or implementation

**Use when:** Designing a new feature, solving an open problem, or deciding between approaches.

### Steps

1. **Search existing KB** — `kb_search` on the feature/problem. Read relevant atoms before forming opinions.
2. **Search prior sessions** — `soil_search` on `hanuman/atoms` with relevant keywords. Check if this was approached before.
3. **State the problem** — one sentence. What are we solving?
4. **Generate 3 approaches** — for each: name it, state the core tradeoff in one sentence.
5. **Recommend one** — which approach and why, in 2 sentences.
6. **Flag constraints** — does this touch:
   - MCP tools → use `_mcp.call()` subprocess client, not direct import
   - Session state → use `_state.py` functions, not direct file writes
   - Hook events → each behavior needs its own `try/except`
   - `settings.json` → use `install.py`, not manual edits
7. **Stop** — do not implement until USER confirms the approach.

### Rules

- KB search first. Never brainstorm in a vacuum.
- Three approaches minimum. Two is lazy, four is stalling.
- Constraints are hard gates, not suggestions.

---

## Debug Mode — Before coding a fix

**Use when:** A bug is reported, tests fail, or unexpected behavior occurs.

### Steps

1. **Search prior context** — `soil_search` on `hanuman/atoms` for the error message or module name. This bug may have been seen before.
2. **State the bug** — exact error, `file:line` if known, expected vs actual behavior.
3. **Identify reproduction** — what is the minimum input that triggers this?
4. **Hypothesize** — list 2-3 candidate causes, ranked by likelihood.
5. **Test the top hypothesis** — read the relevant file, check the line. Confirm or eliminate.
6. **Fix only what is broken** — no surrounding cleanup, no refactoring. One surgical change.
7. **Test the fix** — run the relevant test. If no test exists, write one first.
8. **Commit** — message: `fix(<module>): <what was wrong> — <why it was wrong>`

### Rules

- Never skip step 1. Prior context often contains the root cause.
- Never fix without a test. A fix without a test is just a guess.
- Step 6 is hard: surgical only. Bug fixes don't get free refactors.

---

## Choosing Your Mode

- **Brainstorm** — "How should we build this?"
- **Debug** — "Why is this broken?"

Use brainstorm when there are multiple valid approaches and you need to decide on one. Use debug when something specific is failing and needs a fix.
