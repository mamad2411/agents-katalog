---
name: hoo-verify-outcome
description: Use to re-check a recorded outcome against raw data - "verify that outcome", "did that change really do that", /organic-os:verify-outcome. Recomputes the delta from the connectors before reading what was claimed.
---

# Verify an outcome (recompute first, read the claim second)

Takes an item slug or a path to a record in `outcomes/`. The job is to
recompute the number from raw data and only then look at what the record
claimed, so the recomputation cannot be steered by the answer.

Read-only over the brain except for the run report and the one signal in
step 5. Nothing here changes an item's status, edits an outcome record, or
touches the claimed numbers.

## 1. Identity, URL, windows - and nothing else

`PYTHONPATH="$CLAUDE_PLUGIN_ROOT/lib" python3 -c` into
`core.outcomes.parse_outcome(<path>)`, and use ONLY these three from what
comes back:

- `item` - which item this is
- `url` - the page to pull
- `windows` - the before and after date ranges the claim was measured over

**Do not read `claimed_before`, `claimed_after`, or `claimed_delta` yet, and
do not print them.** This is the whole exercise. A number you have already
seen is a number you will unconsciously reproduce: the pull gets framed
around it, a mismatch gets re-run "to check", and the verification becomes a
confirmation. Steps 2 and 3 happen with the claim unread.

No `windows` in the record: derive them from `applied_at` (the 28 days
after, against the same 28 days before) and say in the report that the
windows were derived, not read. No `applied_at` either - stop and report
the record as unverifiable, naming the missing key. Do not invent a window.

An item slug rather than a path: resolve it to `outcomes/<item-id>.md` in
the active brain (`registry.get_active()`). No such record - say so and
stop; there is nothing to verify.

## 2. Pull the raw windows independently

Through the configured capability slots (ADR-0009), not from anything the
brain already stored:

- **search-data** (GSC for most sites): clicks, impressions, CTR, and
  average position for `url` over each window.
- **analytics** (GA4 for most sites), when configured: sessions for `url`
  over the same windows.

Never substitute a stored signal line for a fresh pull. A signal is the
brain's own prior reading, so checking a claim against it verifies nothing.

**Connector unreachable, or the window falls outside its retention: the
claim is unverified.** Say that, name which connector and why, and stop. An
unverified claim is not a confirmed claim, and a verification run that
cannot pull data has found nothing - not agreement.

## 3. Compute the delta from the raw data

After minus before, per metric, from the numbers pulled in step 2. Write
them down in the run report before step 4. GSC lags 2-3 days: if the after
window ends inside that lag, say the window is still filling and treat the
result as provisional.

## 4. Now read the claim, and compare

Read `claimed_delta` (or `claimed_before` / `claimed_after` when the record
states those instead) and call
`core.outcomes.compare(claimed, recomputed, tolerance=0.05)`.

Report what it returns as it returns it:

- `agrees: True` - the claim holds within tolerance. Say which metrics were
  compared. It confirms the arithmetic, nothing more.
- `divergences` - list each one: the metric, the claimed number, the
  recomputed number, and how far apart they are.
- `unverifiable` - metrics only one side has, or values that are not
  numbers. These are neither agreement nor divergence; name them as
  unchecked.
- `agrees: False` with an empty `compared` - nothing was actually compared.
  Report it as unverified, never as disagreement.

## 5. Report it, including the parts that look bad

Write `runs/<UTCdate>-verify-outcome/REPORT.md`: the item, the URL, the
windows used (and whether they were read or derived), the raw pulls, the
recomputed delta, the claim, and the comparison.

**A divergence is a finding, not an error.** Append it as a signal
(`core.contracts.append_signal`) in the same shape the daily uses:
`outcome <item-id>: claimed clicks +120, recomputed +38 over the same
window`. Do not re-run the pull hoping for a better number, do not widen the
tolerance to make it pass, do not quietly drop the metric that disagreed,
and do not edit the outcome record to match. The reflector reads these
signals; a divergence that never reached the brain teaches it nothing, and a
loop that hides its own misses is worth less than no loop.

## What agreement does and does not mean

Agreement means the recorded number matches what the raw data says over the
same window. It does not mean the change caused the move. Attribution
follows the same rule everywhere else in this plugin (canonical in
hoo-daily's anomaly section, step 2.7): the claim, the comparison actually
run, and what would falsify it. Verification and attribution are two
different questions, and this skill answers only the first. See
`plugin/docs/reproducing-results.md` for how someone outside the project
runs the same check by hand.
