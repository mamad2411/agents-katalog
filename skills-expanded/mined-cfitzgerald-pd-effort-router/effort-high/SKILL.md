---
name: effort-high
description: >-
  Run substantial coding tasks at high effort. Use this for multi-file
  features, debugging when the root cause is unknown, refactors of any size,
  writing or overhauling test suites, performance tuning, and integrating new
  libraries or services. Use it whenever a task needs real investigation or
  restructures existing code — more than a routine single-file addition
  (that's effort-medium), but short of architecture decisions, migrations, or
  anything security-sensitive like auth or crypto (that's effort-xhigh, even
  for small security changes).
effort: high
---

# High effort

This task needs real investigation. The frontmatter has raised effort to high
— use it. Understand the relevant code before changing it, form a hypothesis
before fixing a bug, and verify the result end-to-end (run the tests, exercise
the change), not just by inspection.

Don't gold-plate: high effort means thoroughness on the user's actual task,
not extra scope. If the task turns out to be an architecture decision or a
genuinely gnarly bug, that's effort-xhigh territory for next time.
