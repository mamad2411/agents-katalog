---
name: deep-code-review
description: 8-angle deep code review methodology extracted from Claude Code bundled skills — catches bugs that standard reviews miss.
---

# Deep Code Review — 8-Angle Methodology

Extracted from Claude Code's bundled `code-review` skill. This is the most thorough code review methodology available.

Review for **recall**: catch every real bug a careful reviewer would catch in one sitting. Catching real bugs matters more than avoiding false positives.

## Phase 0 — Gather the diff

Run `git diff @{upstream}...HEAD` (or `git diff main...HEAD` / `git diff HEAD~1`) to get the unified diff under review. If there are uncommitted changes, also run `git diff HEAD` and include working-tree changes.

## Phase 1 — Find candidates (8 independent angles)

Each angle surfaces up to 6 candidate findings with `file`, `line`, `summary`, and `failure_scenario`.

### Angle A — Line-by-line diff scan

Read every hunk in the diff, line by line. Then read the enclosing function for each hunk — bugs in unchanged lines of a touched function are in scope. For every line ask: what input, state, timing, or platform makes this line wrong? Look for:
- Inverted/wrong conditions
- Off-by-one errors
- Null/undefined dereference
- Missing `await`
- Falsy-zero checks
- Wrong-variable copy-paste
- Error swallowed in catch
- Unescaped regex metacharacters

### Angle B — Removed-behavior auditor

For every line the diff DELETES or replaces, name the invariant or behavior it enforced, then search the new code for where that invariant is re-established. If you can't find it, that's a candidate: a removed guard, a dropped error path, a narrowed validation, a deleted test covering a real case.

### Angle C — Cross-file tracer

For each function the diff changes, find its callers (Grep for the symbol) and check whether the change breaks any call site: a new precondition, a changed return shape, a new exception, a timing/ordering dependency. Also check callees: does a parallel change in the same PR make a call unsafe?

### Angle D — Reuse check

Flag new code that re-implements something the codebase already has. Grep shared/utility modules and files adjacent to the change, and name the existing helper to call instead.

### Angle E — Simplification

Flag unnecessary complexity the diff adds: redundant or derivable state, copy-paste with slight variation, deep nesting, dead code left behind. Name the simpler form that does the same job.

### Angle F — Efficiency

Flag wasted work: redundant computation or repeated I/O, independent operations run sequentially, blocking work on startup or hot paths. Also flag long-lived objects built from closures — they keep the entire enclosing scope alive (memory leak). Name the cheaper alternative.

### Angle G — Altitude

Check that each change is implemented at the right depth, not as a fragile bandaid. Special cases layered on shared infrastructure are a sign the fix isn't deep enough — prefer generalizing the underlying mechanism.

### Angle H — Conventions

Find the project's coding conventions (CLAUDE.md, .cursorrules, AGENTS.md, etc.) that govern the changed code. Check the diff for clear violations. Only flag a violation when you can quote the exact rule and the exact line that breaks it.

## Phase 2 — Verify (1-vote, recall-biased)

For each candidate, verify: **CONFIRMED / PLAUSIBLE / REFUTED**

**PLAUSIBLE by default** — do not refute for being "speculative" when the state is realistic: concurrency races, nil/undefined on rare paths, falsy-zero, off-by-one on boundaries, retry storms.

**REFUTED** only when: factually wrong (quote the line), provably impossible, already handled in this diff, or pure style with no observable effect.

Keep CONFIRMED and PLAUSIBLE. Drop REFUTED.

## Output

Return findings ranked most-severe first, max 10:

```json
[
  {
    "file": "path/to/file.ext",
    "line": 123,
    "summary": "one-sentence statement of the bug",
    "failure_scenario": "concrete inputs/state → wrong output/crash"
  }
]
```
