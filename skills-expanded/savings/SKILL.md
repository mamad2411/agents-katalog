---
name: savings
description: Show the MetaHarness routing ledger inline — which model each task was routed to, what it displaced, and the percentage + dollars saved — plus the learned router's training state. Use when the user says "savings", "show my savings", "metaharness report", "metaharness/report", "routing report", "routing receipts", "who is the router choosing", "how much has routing saved me", "is the meta harness working", or "show me the routing". All numbers come from the real receipts log; never fake or extrapolate a number.
updated: 2026-07-13
---

# Savings — the MetaHarness routing ledger, inline

Show the user their routing wins the way a bank statement shows transactions: real rows, real
totals, zero vibes. Everything below comes from live artifacts on their machine; if a file is
missing or empty, say exactly that — an honest "nothing routed yet" builds more trust than a
padded number.

## Steps (run these, verbatim — then render)

1. **The ledger**:
   `node scripts/metaharness-receipts.mjs`
   (falls back to `~/.claude/metaharness/routing-receipts.jsonl` raw if the script is absent —
   the plugin repo root or the installed package both carry it under `scripts/`).
2. **The learner's state**:
   `node -e "import(REPO+'/scripts/metaharness-router.mjs').then(m=>{const r=m.loadLabelledRows();console.log(JSON.stringify({labels:r.rows.length,needed:m.MIN_LABELS}))})"`
3. Optional, if the user asks who decides: run one live decision
   `node scripts/model-router-engine.mjs --prompt "<their current task>"` and quote `routedBy`.

## Render

The receipts script already draws the full card (percentage-first headline + spent-vs-unrouted
bar + audit table) — **show its output verbatim in a code block**; do not re-format or re-total
it. Then append the learner's state on two lines:

```
🧠 Learned router: <routedBy state>
  <labels>/<needed> outcome examples → <"learning-routed decisions live" | "cold-start: static
  tiers deciding (honest fallback) — N more outcomes to go">
```

## Hard rules

- **Never fake a number.** Every dollar figure must trace to a receipt row. If `token_source`
  says estimated, the totals line keeps the script's own "est." qualifier.
- **Print the honest router state.** If the learner is below MIN_LABELS, say cold-start plainly —
  the fallback tiers still save money and that is a true story worth telling.
- **One screen.** Cap the table at 10 most-recent rows; state "+N earlier rows" if truncated.
- After showing the ledger, offer ONE next action, not a menu: if labels < 20, offer the
  calibration run ("want me to train it up with a $0 calibration batch?"); otherwise offer
  nothing.
