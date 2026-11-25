---
name: code-review-checklist
description: Five-axis code review checklist (correctness, security, readability, performance, test coverage) producing actionable comments instead of style nitpicks. Use when the user asks to review code, a diff, or a pull request.
license: MIT
---

# Code Review Checklist

One review answers a single question: "Will this code become someone else's problem within three months?" Walk the five axes in order; each axis gets pass / fail / N-A, and every failure must come with a concrete fix.

## Workflow

1. **Check the scope first**: look at the diff size. Over ~400 changed lines, ask for a split before reviewing — review quality on huge diffs always collapses.
2. **Check axis by axis** (order = priority):
   - **Correctness**: edge cases (null, empty, zero, negative, oversized), concurrency/timing assumptions, error handling (are exceptions swallowed?). One of the two axes that can block a merge (with Security).
   - **Security**: is user input concatenated into SQL / shell commands / HTML; are secrets or tokens hard-coded; does logging leak sensitive data. One of the two axes that can block a merge (with Correctness).
   - **Readability**: do names say what things are; does each function do one thing; are magic numbers named. Flag only what you can't understand — not "I'd write it differently."
   - **Performance**: repeated queries or recomputation inside loops; N+1 problems; avoidable large-object copies. No data-free performance speculation ("this might get slow" is not a comment).
   - **Test coverage**: does new logic have tests; do edge cases have cases. All-green tests with the critical path uncovered still earn a `Should fix` — flag it explicitly, but tests alone don't block the merge.
3. **Write the comments**: fixed format — `[axis] file:line problem → suggested fix`. Only actionable suggestions; "could be optimized" is not one.
4. **Triage**: `Must fix` = a concrete correctness or security failure (these two axes, and only these, can block a merge) vs `Should fix` (readability / performance / tests). "Should fix" doesn't block the merge, but say so explicitly.

## Rules

- At most 10 comments per review. More than that means the code is too broken — send it back for a rewrite instead of grading 50 items.
- No style policing: indentation, quotes, semicolons — that's the linter's job, not a human's.
- Speak with the diff: every comment must cite a concrete line of code. A comment without a code reference is invalid.

## Checklist (minimal executable version)

```markdown
## Code review checklist

- [ ] Correctness: edge cases (null/0/negative/oversized) handled, exceptions not swallowed
- [ ] Correctness: concurrency/timing assumptions hold, no races
- [ ] Security: no SQL/shell/HTML injection points, no hard-coded secrets, no sensitive data in logs
- [ ] Readability: names are descriptive, functions have a single responsibility, no magic numbers
- [ ] Performance: no repeated queries/computation in loops, no N+1, no evidence-free performance worries
- [ ] Tests: new logic is covered, edge cases have cases
- [ ] Scope: diff ≤ ~400 lines, otherwise split first
```

Example review comments:

```text
[Must fix][Correctness] order.py:87 empty order list triggers IndexError → guard for empty before taking [0]
[Should fix][Readability] order.py:92 magic number 86400 → name it SECONDS_PER_DAY
```

## Worked example

A 14-line diff adds a discount endpoint. The full review this checklist produces:

```python
@app.get("/discount")
def discount(code: str):
    row = db.execute(f"SELECT pct FROM coupons WHERE code = '{code}'").fetchone()
    return {"pct": row[0], "label": "SAVE" + str(row[0]) + "%"}
```

```text
[Must fix][Security] discount.py:3 user input interpolated into SQL → parameterize the query (code = ?)
[Must fix][Correctness] discount.py:4 unknown code makes fetchone() return None, row[0] raises TypeError → return 404 when row is None
[Should fix][Readability] discount.py:5 label built by string concatenation → use an f-string or a named helper
Verdict: do not merge — 2 must-fix items (security + correctness). The readability item does not block.
```

Note what the checklist kept out: no comment on quotes, line length, or naming taste, and no performance remark — there is no data showing this query is slow. Two blocking findings, one non-blocking note, one explicit verdict: that ratio is the point of the triage rule.

## Anti-patterns

- ❌ Drive-by LGTM: approving before reading the whole diff — the review is theater.
- ❌ Style police: 18 of 20 comments about quotes and line breaks while a null-pointer dereference slips through.
- ❌ Comments without code: "this logic looks off" — which logic? Which line? Unsaid means invalid.
- ❌ Performance speculation: "this loop might be slow at scale" — a performance comment without data is noise.
- ❌ Grading 50 items: when there are too many problems to list, the right move is "rewrite and resubmit", not playing teacher.
