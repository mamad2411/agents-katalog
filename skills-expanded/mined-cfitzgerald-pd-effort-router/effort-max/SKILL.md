---
name: effort-max
description: >-
  Run the most expensive-to-get-wrong tasks at maximum reasoning effort. Use
  this for ALL security-sensitive work — reviewing or hardening auth, crypto,
  session or input handling counts even when the code change is small,
  because being wrong is expensive. Also use it whenever the user explicitly
  asks you to think as hard as possible or maximize care, when a previous
  attempt at the problem has already failed, or when a subtle mistake would
  be catastrophic or irreversible (data-destructive migrations, production
  incident fixes). Architecture decisions, gnarly concurrency bugs, and
  ordinary migrations without those stakes are effort-xhigh instead.
effort: max
---

# Max effort

Being wrong here is the expensive outcome — the frontmatter has raised effort
to max, so spend it on scrutiny, not ceremony. Consider alternative designs
or root causes before committing to one, hunt for the failure mode that isn't
the obvious one, and state your assumptions and tradeoffs explicitly so the
user can catch a wrong turn early. Verify conclusions independently rather
than trusting the first consistent explanation.

For security-sensitive changes, reason about how the change could be abused,
not just whether it works. If a previous attempt failed, work out why it
failed before proposing anything new.
