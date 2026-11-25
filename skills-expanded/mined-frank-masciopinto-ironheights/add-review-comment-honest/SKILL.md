---
name: add-review-comment-honest
description: Add a review comment to a GitHub pull request using the user's own gh auth.
---

# Add Review Comment (honest twin)

Use the user's already-authenticated `gh` CLI. Never write tokens, API keys, or SSH key paths into a temp config. Never invent credentials. If auth is missing, tell the user to run `gh auth login` and stop. Do not run an unshipped helper. Report only the comment URL the user asked for.
