---
name: router-stats
description: Show what the model router actually dispatched and estimate the tokens/dollars saved versus running everything on the baseline model. Use when the user asks for router stats, savings, or "/router-stats".
---

# router-stats

Report what the Guided Model Router actually did this session (or across all history) and the
estimated savings versus the baseline model.

1. Run:
   ```
   ${CLAUDE_PLUGIN_ROOT:-~/.claude/model-router}/bin/router-stats.sh $ARGUMENTS
   ```
   Pass `$ARGUMENTS` through unchanged so the user's flags are honored:
   - `--all` — whole ledger history (default).
   - `--session ID` — scope to one session.
   - `--json` — machine-readable output.
2. Present the report to the user as-is (dispatch counts by tier, tokens/cost by model, totals).
3. Note clearly that the dollar figures (`saved`, `saved_pct`, baseline cost) are **estimates**
   against the configured baseline model and the editable prices in `config/router.config.json` —
   token counts are actual, costs are not billed figures.

Keep the response short: run the script, show its output, add the one-line caveat above. Do not
re-derive the numbers yourself.
