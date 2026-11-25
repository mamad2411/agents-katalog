---
name: summarize-diff
description: "Explains a diff in plain language for a product manager or support lead: what changed, who is affected and what could go wrong."
disable-model-invocation: true
---

Summarize a code change for a non-engineer. Target: $ARGUMENTS (current branch against main if empty).

1. Get the change: a range through `git diff <base>...<head>`, a commit with `git show`, or a pull request with `gh pr diff <n>`. Read the commit messages too.
2. Work out what a user or customer would notice. Look at UI text, endpoints, emails, pricing logic, permissions, data stored, and defaults. Ignore pure refactors, but say they exist.
3. Write for someone who has never seen the code: no file names, no function names, no acronyms without a short explanation.

Format:
**In one sentence**
**What changes for users** (bullets, plain words)
**Who is affected** (which customers, roles or plans)
**Risks and what to watch** (support load, data changes, rollout order)
**Needs a decision** (anything the code leaves open)
**Not covered** (what you could not tell from the diff)

Keep it under 200 words. Never guess a business reason; if the diff does not show it, say so. Make no changes.
