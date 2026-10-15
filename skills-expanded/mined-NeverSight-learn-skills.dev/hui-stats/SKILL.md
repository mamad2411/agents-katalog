---
name: hui-stats
description: >
  Show observed local token usage for current Claude Code session.
  Reads session log directly. Triggers on /hui-stats. Output is injected by
  mode-tracker hook; model does not compute numbers.
---

This skill is delivered by `hooks/hui-stats.js`, invoked by `hooks/hui-mode-tracker.js` on `/hui-stats`. Hook returns `decision: "block"` with locally observed output-token, cache-read-token, and turn counts. It does not estimate savings, cost, or a non-HUI baseline.
