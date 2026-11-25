---
name: code-review
description: Reviews code changes with a risk-ordered checklist and finds what a diff touches. Use whenever the user asks to review a pull request, diff, commit or file, wants feedback on their code, asks "is this safe to merge", or wants a self-review before opening a PR, even if they only paste code and say "thoughts?". Reports blockers separately from suggestions and nits, with concrete fixes.
---

# code-review

Review for correctness and risk first, style last. Report findings so the author knows what blocks the merge and what is optional.

```
code-review/
├── SKILL.md
├── scripts/
│   └── review_scope.sh    size, categories, risk flags, missing tests, debug leftovers
└── references/
    └── checklist.md       design, correctness, security, tests, performance, comment style
```

## When to use

- Reviewing a PR, branch, commit or pasted snippet
- Self-review before opening a PR
- Deciding whether a change is safe to merge or release

## Workflow

1. **Scope**: run `bash scripts/review_scope.sh origin/main` inside the repo. It shows size, risk flags (migrations, auth, dependencies, CI, secret-like files), whether tests changed, and leftover debug lines.
2. **Understand intent**: read the PR description or commit messages. State the goal in one sentence. If it is unclear, ask.
3. **Read for design**: wrong approach beats any line level comment.
4. **Read for correctness and risk** using `references/checklist.md`, in order: design, correctness, security, tests, performance and operations, readability.
5. **Verify claims**: run the tests, reproduce the bug, or trace one path by hand. Do not assume the tests cover it.
6. **Write the review** with severity prefixes (below).

## Output format

```
Summary: one or two sentences on what the change does and the overall verdict.

Blockers
- path:line  what is wrong, why it matters, suggested fix

Suggestions
- path:line  ...

Questions
- ...

Nits
- ...

What is good
- one or two specific things
```

Verdict is one of: **approve**, **approve with suggestions**, **request changes**. Use request changes only when there is at least one blocker.

## Rules

- Be specific: file, line, reason, fix. "Looks wrong" is not a review.
- Separate blockers from preferences. Never block on style a formatter can handle.
- Review the change, not the author. Prefer questions to accusations.
- Do not review what you did not read; say which parts you skipped.
- Large diffs: say so, review by risk, and ask to split.
- If you find a secret, say "possible secret in file:line" without repeating it, and point to `secrets-hygiene`.

## What to report back

| Field | Content |
|-------|---------|
| Verdict | approve, approve with suggestions, request changes |
| Scope | files, size, risk flags from the script |
| Verified | tests run, paths traced, what was not checked |
| Findings | grouped by severity with file and line |

## Related skills

- `secrets-hygiene`: scan the change for credentials
- `systematic-debugging`: reproduce and prove a suspected bug found in review
- `commitsmith`: clean, scoped commit messages for the fixes
