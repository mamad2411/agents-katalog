---
description: Run the full quality gate (typecheck + tests + build) and give a go/no-go
allowed-tools: Bash
---
Run this repo's quality gate and report a clear go/no-go.

Run all three even if an earlier one fails (so I see the full picture):

1. `npm run typecheck`
2. `npx vitest run`
3. `npm run build`

Then give a one-line verdict: **GO** (all three green) or **NO-GO** with the exact
failing output quoted. Do not fix anything unless I ask — just report.
