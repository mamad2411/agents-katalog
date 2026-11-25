---
name: engineer-pre-pr
description: Run validate, review, sync-docs, and coverage checks before opening a PR
---

# Pre-PR

We're wrapping up work on this branch and getting ready to open a pull request. This skill is an orchestrator — it invokes the four checks below in order, so you don't have to invoke them one by one. Each is also its own standalone skill, if you only need one of them.

Invoke these, in this order:

1. `engineer-validate` — verifies the branch is aligned with the project's master docs.
2. `engineer-review` — reviews the code and confirms it's ready to ship.
3. `engineer-sync-docs` — updates the project's documentation.
4. `engineer-coverage` — finishes writing tests for the branch.

Handle any feedback each of these produces, and make the necessary changes and fixes before moving to the next one.

Once done, let me know and ask my permission to open the Pull Request.
