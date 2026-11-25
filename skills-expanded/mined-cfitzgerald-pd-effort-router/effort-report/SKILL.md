---
name: effort-report
description: >-
  Report effort-router token savings and likely misroutes: tokens saved by
  downshifting, turns routed too low that flailed and wasted their tokens,
  and trivial turns that burned high/xhigh/max reasoning — plus tier/day/model/
  session breakdowns. Use whenever the user asks about effort-router stats,
  token savings, wasted tokens, misrouted turns, effort tier usage, "how
  much has the router saved", or routing behavior over time. This is a
  reporting task — do not route it through an effort tier first.
---

# Effort usage report

Run the bundled aggregator and present its output:

```bash
python3 "$(dirname "$SKILL_PATH")/scripts/effort_report.py"
```

(If `$SKILL_PATH` is unavailable, the script lives at
`skills/effort-report/scripts/effort_report.py` inside this plugin.)

The report leads with what matters: the downshift savings estimate, then
likely misroutes — turns routed low/medium that ran far past their tier's
norm (probably flailed for lack of reasoning; the whole turn's tokens are at
risk), and high/xhigh/max turns that were tiny (paid heavy reasoning for
trivial work). Breakdown tables (tier, day, model, session with turn count, tokens,
and one-line summary) follow as context.

Present the output as-is, then interpret: call out flagged misroutes worth
inspecting (the flags are token-size heuristics, not verdicts — a small
xhigh turn can be a legitimately hard question with a short answer), whether
`unrouted` dominates (sessions that predate a plugin install or update keep
their old hooks until restarted, so the per-turn routing nudge never fires
in them),
and the savings estimate with its caveat: it compares low-routed turns
against the mean medium-tier turn — tiers see different task mixes, so treat
it as directional, not accounting.

The underlying data lives in `~/.claude/effort-router/usage/<session_id>.jsonl`,
rewritten by the plugin's Stop hook after every completed turn: a session
meta line (`{"meta": true, "summary": ...}`) followed by one record per turn.
If the user wants a cut the script doesn't offer (per-week, a chart), read
those files directly and compute it.
