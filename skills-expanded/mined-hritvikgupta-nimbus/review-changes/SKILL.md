---
name: review-changes
description: How to review a change in this project before calling it done.
---

# Reviewing a change

1. `diagnostics` on every file you touched — zero errors, or you are not finished.
2. `find_referencing_symbols` on anything whose signature moved.
3. `typecheck` once at the end.

Report what you changed, what you verified, and what you deliberately left alone.
