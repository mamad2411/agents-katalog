---
name: review-pr
description: Reviews a pull request by number or link and returns a verdict with blocking issues, optional suggestions and what was checked.
disable-model-invocation: true
---

Review the pull request: $ARGUMENTS (number or URL).

1. Fetch it with `gh pr view <pr> --json title,body,author,baseRefName,files,reviews,comments` and `gh pr diff <pr>`. If `gh` is unavailable, ask for the diff.
2. Read the description first and state in one sentence what the change should do. Check the diff does that and nothing else.
3. Read changed files in full where the diff lacks context. Check callers of changed functions with search.
4. Look for, in order: correctness bugs and unhandled edge cases; security (input handling, secrets, authorization); data loss or migration risk; missing or weak tests; performance traps such as queries in loops; unclear names; leftover debug code.
5. Check CI status with `gh pr checks <pr>`.
6. Write each comment as `path:line`, the problem, why it matters and a suggested fix. Mark it **Blocking** or **Optional**.

End with a verdict: approve, approve with optional comments, or request changes, plus a short list of what you did not check. Do not post anything; ask first whether to submit with `gh pr review`.
