---
name: onsite-measure
description: Use to measure applied/published changes at day 7 and day 28 - "measure outcomes", /organic-os:measure, or the daily routine's follow-up step.
---

# Measure outcomes (closing the loop)

1. Scan outcomes/ for records with a due measurement date <= today that lack
   that measurement.
2. Per record: pull GSC for the target URL - clicks/impressions/CTR/position
   for the 7 (or 28) days after the change vs the same window before.
   GSC data lags 2-3 days: fetch the day-7 window no earlier than day 10,
   and the day-28 window no earlier than day 31.
   No GSC connector: record "unmeasured (no GSC)" honestly.
3. Append the delta to the outcome record + one signal line
   ("outcome <item-id>: position 8.2 -> 5.9 after title rewrite").
   "After" is a sequence, not a cause. Attributing the move to the change
   follows the attribution rule (canonical in hoo-daily's anomaly
   section, step 2.7): the claim, the comparison actually run, and what
   would falsify it - for example "compared the 28 days after against the
   same 28-day window before, same URL; if the site-wide trend moved the
   same way over those windows, the change is not what did it." Where
   that comparison was not run, the record reads `cause: unknown
   (before/after window not compared)` and keeps the delta. A measured
   number with an honest unknown is what lets the reflector score a
   skillbook entry later; a confident story that nobody checked teaches
   the loop the wrong lesson.
4. Wins and losses BOTH matter: the reflector reads outcomes to score
   skillbook entries helpful/harmful. At day-28, set the item to measured
   via `PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -m core status
   <item-path> measured --actor agent`. Never edit brain frontmatter
   directly. The contract CLI is the only write path for status and
   approvals.
