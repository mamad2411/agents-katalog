---
name: effort-xhigh
description: >-
  Run very hard tasks at extra-high reasoning effort. Use this for
  architecture and design decisions (including advice-only discussions with
  no code changes), gnarly bugs (concurrency, state corruption, flaky or
  heisenbug behavior), large migrations, and whenever the user says the
  problem is hard. A normal multi-file feature or ordinary debugging session
  is effort-high instead; security-sensitive work, retries after a failed
  attempt, and explicit think-as-hard-as-possible requests go to effort-max.
effort: xhigh
---

# Extra-high effort

This problem is hard or expensive to get wrong. The frontmatter has raised
effort to xhigh — spend it on thinking, not on ceremony. Consider alternative
designs or root causes before committing to one, look for the failure mode
that isn't the obvious one, and state your assumptions and tradeoffs
explicitly so the user can catch a wrong turn early.

If the task turns out to be security-sensitive, that's effort-max territory
for next time.
