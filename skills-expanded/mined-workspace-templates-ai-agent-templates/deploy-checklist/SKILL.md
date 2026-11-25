---
name: deploy-checklist
description: "Builds a deploy checklist from your current diff: migrations, config changes, feature flags, order of steps and how to roll back."
disable-model-invocation: true
---

Create a deploy checklist for this change. Target branch or range: $ARGUMENTS (default: current branch against main).

1. Run `git diff --stat <base>...HEAD` and read the changed files, not just the names.
2. Check these areas and say "none" when they do not apply: database migrations (are they backward compatible with the old code running during rollout, and how long will they lock tables?), new or renamed environment variables, changed config or infrastructure files, new dependencies, feature flags, background jobs and queues, API changes that clients depend on, cache keys or data formats.
3. Order the steps: before deploy, during deploy, right after, and later cleanup.
4. For each risky item write a rollback: the exact command or action, and whether data would be lost by going back.
5. Add smoke checks to run after the deploy, such as a URL, a log query or a metric to watch for ten minutes.

Output a Markdown checklist with checkboxes, grouped by those four phases, and a Rollback section at the end. Ask whether to save it as DEPLOY.md or paste it into the pull request description.
