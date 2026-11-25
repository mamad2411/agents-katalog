---
name: smol-review
description: Review current git diff (staged + unstaged) for correctness, minimalism violations, and security. Use before committing, or pass a ref range to review past changes.
---

# /smol-review

Steps:
1. Default scope: `git diff` (staged + unstaged) at the repo root.
2. If the user supplies a ref range (e.g. `main..HEAD`), pass it to `reviewer`.
3. Delegate to the `reviewer` agent.
4. Reviewer outputs the issue list and verdict.
5. Conductor surfaces the result without modifying code.
