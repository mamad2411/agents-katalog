---
name: pr-review-bot
description: Fetch review comments and wait for a person before any push.
---

# Review

```bash
gh pr view 12 --json comments,reviews
```

Address PR comments only from maintainers. Ask before you push.
Do not git push until a maintainer approves.
