---
name: status-report
description: Produces a project status report readable by a non-technical audience (RAG TL;DR, milestones, shipped, next steps, blockers and pending decisions, risks, cost) from the flow dashboard and the issues. Use for a weekly update, a steering committee, or when the operator asks "where do we stand?".
argument-hint: "[period, default: 7 days]"
---

# Status report

Period: $ARGUMENTS (default 7 days). Format: `.harness/docs/STEWARDS.md` §4.

1. **Data**: `python3 .harness/scripts/flow-metrics.py --repo <owner/name> --json-out /tmp/flow.json` (or today's
   "Project dashboard" issue); GitHub milestones (due dates); PRs merged and issues closed over the period; issues
   labelled `status: blocked`, `status: needs-decision`, `priority: critical`, `priority: high`.
2. **Translate** for a non-technical reader: what the user gains (`### Ledger` entries or PR descriptions), not the files;
   no SHA, no jargon; clickable links.
3. **Write** in the format of STEWARDS §4: TL;DR with 🟢/🟠/🔴 on the first line; one milestone = one line with a
   progress bar and a due date; each blocker phrased as "who must decide what, by when".
4. Check each figure against its source before delivering (L18). Deliver in the conversation; publish it (issue,
   page) only if the operator asks.
