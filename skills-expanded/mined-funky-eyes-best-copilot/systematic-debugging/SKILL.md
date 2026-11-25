---
name: systematic-debugging
description: "Use when a bug, failing test, incident, or unexpected behavior has unknown cause and scope is not yet frozen."
---

# Systematic Debugging

## Loop

1. Capture the exact failure and reproduction path.
2. Map observed behavior to expected behavior.
3. Generate ranked hypotheses.
4. Run the cheapest falsification check.
5. Narrow scope to files/components.
6. Hand off to `root-cause-investigation` or implementation once the cause is bounded.

## Rules

- Do not edit before reproducing or proving a likely cause.
- Stop repeated retries after the same blocker appears twice.
- Preserve raw failure snippets or recovery commands when outputs are long.
