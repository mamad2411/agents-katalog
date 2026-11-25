---
name: commit-message
description: Writes a conventional commit message from the staged diff, one logical change at a time.
disable-model-invocation: true
metadata:
  version: 0.1.0
---

# commit-message
Turn whatever is currently staged into one well-formed conventional
commit message the user can apply as-is. The user gets the message text;
you never run `git commit` yourself.

## Steps

1. Run: `git diff --cached --stat` then `git diff --cached`. If nothing is
   staged, say so and stop; never guess from unstaged changes.
2. Check the diff is **atomic** (one logical change). If it mixes concerns,
   propose how to split it (`git reset -p` / staging hunks) instead of
   writing a muddled message.
3. Pick the type and scope. When unsure which type fits, first read
   `references/conventional-commits.md`.
4. Write the message: imperative subject ≤ 50 chars
   (`type(scope): change`), blank line, body wrapped at 72 explaining what
   changed and why, not how.
5. Present the message in a fenced block, then ask whether to adjust tone
   or detail.

## References

Keep this file lean; put branch-only detail behind pointers so it loads
only when that branch is hit:

- When choosing the commit type or handling a breaking change, first read
  `references/conventional-commits.md`.

## Gotchas

- Empty staged diff → stop at step 1; do not invent a message.
- Generated/lockfile-only diffs (`uv.lock`, `package-lock.json`) → say the
  change is mechanical and suggest `chore(deps)`.
- Never include ticket numbers or co-author trailers unless the user asks.
