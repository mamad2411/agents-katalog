---
name: account
description: Use when the user asks which account is active or current, account or subscription limits, quota or rate-limit usage, the 5-hour or weekly window, when the next claude launch will rotate accounts, remaining subscription days, or wants a claude-rotate account overview.
metadata:
  short-description: Show the active account and quota limits via claude-rotate
---

# Account Status (claude-rotate)

Reports which account **this agent session** is running on and the quota/limits
of every configured account, via `claude-rotate`.

## How to run

Run the command and show its output to the user **verbatim** — it is already
formatted (a status line, one fenced block per account, a short warnings list
only when action is needed, and one card for the other coding subscriptions on
the machine when Codex or Gemini is installed). Keep every code fence intact so
each account stays its own card. Do not reformat, merge the blocks, summarize,
or add commentary.

```bash
claude-rotate status --report
```

If `claude-rotate` is not installed or reports no accounts, relay that message
as-is. Never fabricate numbers.

## What it reports

- **Markers**: `@` = the account this session runs on; `>` = the account the
  rotator would pick next; `@>` = both (no rotation on the next launch).
- **One fenced block per account** (narrow, no table borders, readable on a
  phone — each fence renders as its own card): a header with the account name and
  days left on the subscription, then — per window (`5h`, `week`, and any
  model-scoped weekly window like `fable`, which tracks that model's separate
  weekly cap) — a *fact line* and a *forecast sub-line* beneath it. The fact
  line carries a progress bar
  (`█`/`░`), the current usage % and the reset as an absolute clock (with a
  weekday when it lands on another day) plus a compact relative duration, e.g.
  `Thu 13:00 (4d 20h)`. A `~` before the % (e.g. `~88%`) marks a cached
  last-known value — the live fetch failed, so treat it as a lower bound, not
  the current usage. The label-less sub-line carries the projection: the
  `→`-prefixed forecast % and, when the limit is crossed before reset, the clock
  and relative duration at which usage hits 100% — shown as `→XX% —` when the
  window resets first, a lone `—` when there is no trend yet, or `reached` once
  usage is already ≥100%. Both lines share one column grid, so the forecast %
  stacks under the current % and the limit-ETA clock under the reset clock.
- **Groups** (only when account groups are configured): each header ends with
  the account's group (`· client`) and `· not allowed here` when the current
  directory may not use that account — it is shown but never picked here. The
  `>` marker names the account the next launch *in this directory* would use.
  To report another directory, run `claude-rotate status --report --dir <path>`.
- **Warnings** (only when action is needed; absent otherwise): an account needs
  re-login, or a subscription expires within 7 days. Quota-usage risk and the
  fallback recommendation are intentionally not shown.
- **Other providers** (only when Codex or Gemini is installed): one fenced card
  under the heading `other providers`, with the same fact line and projection
  sub-line per window. Display-only — these quotas never affect rotation.

## Maintenance

This skill is a thin wrapper; all logic lives in `claude-rotate` itself
(`claude_rotate.report.build_report`, exercised by its test suite). Update the
tool to change the output. Reinstall the skill with `claude-rotate
install-skill`.
