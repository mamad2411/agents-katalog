---
name: token-audit
description: Find what is spending tokens and suggest concrete config changes, using Codeburn usage data. Use when the user asks about token use, cost, or why a session burned so much.
---

# token-audit

1. Get the last 7 days: `npx -y codeburn@0.9.27 report -p week --format json` (the version in core/pins.json). Codeburn needs Node 22.13 or newer. If it fails or has no data, say so and stop. Never invent numbers.
2. List the top cost drivers from the data, biggest first: models, sessions, tools, large outputs. Give the real number for each.
3. For each driver, suggest one change this repository already supports:
   - Search or read-heavy work on a strong model: route it to the `explore` subagent on the fast tier.
   - Large test, log or API output: turn on Context Mode (`--tools context-mode`) and use it for that output.
   - Long shell output: turn on RTK.
   - A session that grew too long: split the work and compact earlier.
4. State the expected effect only if the data supports it. Otherwise say it is unmeasured.
5. Ask before changing any config. Run the audit again a week later to compare.
