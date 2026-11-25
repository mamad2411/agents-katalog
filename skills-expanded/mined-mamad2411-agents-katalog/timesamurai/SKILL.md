---
name: timesamurai
description: "Use the timesamurai CLI to track work time — start/stop work sessions, add/subtract hours, day off, time reports, and find/modify/delete/undo log entries. Use when asked to log work time, clock in/out, add hours, record a lunch or day off, show a time report/balance, or fix an entry in the worktime log. Triggers: work time, time tracking, log hours, clock in, clock out, day off, time report, worktime."
---

# timesamurai

`timesamurai` is a command-line worktime tracker. It keeps a JSONL log per
host (new entries are appended; `modify`/`delete` rewrite the file) and can
print accounting reports against a weekly hours target. The binary is on the
PATH as `timesamurai`.

Data lives in `~/git/worktime/timesamuraidb/`:

- `db.<host>.jsonl` — one JSON entry per line (the log). Never edit by hand.
- `undo.<host>.jsonl` — pending undo records, one per recent
  insert/modify/delete (consumed records are dropped).

Each entry has: `id`, `action` (`login`, `logout`, or `add`), `epoch`
(unix seconds), `host`, `value` (signed seconds; **0** for login/logout,
which omit the key on disk), `tags`, `descr` (empty fields are omitted on
disk). Worked time is computed by the report from
`logout epoch − login epoch`; `add` entries carry the seconds directly.

## The five commands you will use 90% of the time

```bash
timesamurai work start              # clock in (opens a session, tag "work")
timesamurai work stop               # clock out (closes the session)
timesamurai work status             # is there an open session?
timesamurai work report week        # this week's accounting report
timesamurai work add 1h -d "what it was"   # credit a fixed duration
```

## Decision guide

| The user wants to... | Run |
|---|---|
| Clock in / start work | `timesamurai work start` |
| Clock out / stop work | `timesamurai work stop` |
| See open sessions | `timesamurai work status` |
| Credit hours ("I worked 2h on X") | `timesamurai work add 2h -d "X"` |
| Take time back ("undo that 30m", "deduct 1h") | `timesamurai work sub 1h` |
| Log a lunch break | `timesamurai work add 1h lunch` |
| Record a full day off | `timesamurai work day-off` (no duration; 8h against "off", timestamped at midnight) |
| Move selfdevelopment buffer hours into work | `timesamurai work usebuffer 2h` |
| See hours for today / this week / a month | `timesamurai work report today` / `week` / `month` |
| See the full accounting report | `timesamurai work report` (no range) |
| Find entries matching text | `timesamurai work search "podcast"` |
| List entries by filter | `timesamurai work list --tag work --limit 20` |
| Change an entry's time/tags/descr | `timesamurai work modify <host:id> --...` (see below) |
| Remove an entry | `timesamurai work delete <host:id>` (try `--dry-run` first) |
| Revert the last change made from this machine | `timesamurai work undo` |
| Edit entries interactively | `timesamurai work edit [range]` (opens $EDITOR) |
| Record for another machine | add `--host <name>` (entry-creating commands only: `start`/`stop`/`add`/`sub`/`day-off`/`usebuffer`/`import`) |

## Sessions (start / stop / status)

- `start` writes a `login` entry (value 0) for the tag category — default `work`.
- `stop` writes a `logout` entry (value 0). The report computes the duration.
- Only **one** open session per tag category exists across all hosts:
  - `start` while one is open → error `already logged in`.
  - `stop` while none is open → error `not logged in`.
- `start`/`stop` accept tags as arguments: `timesamurai work start lunch`
  opens a lunch session. Default (no tags) is `work`.
- `-d/--descr` adds a free-text description to the entry.
- `--at` backdates the entry (see Time formats below).

Check `timesamurai work status` before suggesting `start` if the user's
request implies a session may already be open.

## Durations (add / sub / usebuffer)

```bash
timesamurai work add <duration> [tags...] [-d descr] [--at time]
timesamurai work sub <duration> [tags...] [-d descr] [--at time]
timesamurai work usebuffer <duration> [-d descr] [--at time]
```

Duration formats:

- `30m`, `1h`, `1h30m`, `2.5h`, `45s` — Go duration syntax (unit letters case-insensitive).
- **A bare integer is SECONDS**, not minutes: `3600` = 1 hour, `60` = 1 minute.
  When a user says "60", ask or assume minutes and use `60m`.
- `add` must be positive; `sub` is a withdrawal (writes a negative value).
- Default tag is `work`. Extra tags are positional: `add 1h30m pet`.
- `usebuffer` is always selfdevelopment → work, two `add` entries.

## Reports

```bash
timesamurai work report            # full history
timesamurai work report [range]    # one range
```

Range formats (all inclusive of their natural boundaries):

- `today`, `yesterday`
- `week` — the current ISO week (Monday start; **not** the last 7 days)
- `lastweek`
- `month` — the current calendar month
- `YYYY-MM` — e.g. `2026-08`
- `YYYY-MM-DD..YYYY-MM-DD` — e.g. `2026-09-01..2026-09-07` (both days included)

Output is per-day lines (e.g. `Tue 20260908 37: work:6.69h`) plus a week
totals line. Both always print `work:` (even at zero) and the other fixed
categories — `balance`, `lunch`, `off`, `sick`, `bank`, `pet`,
`selfdevelopment` — only when non-zero, in that order; the week totals line
additionally always ends with a `buffer:` token. `balance` is the running
total against the weekly target (default 40h/week, from config). A `*`
before a day marks a weekend or a day with ≥8h off **or** ≥8h bank.

To answer "how many hours this week?" run `work report week` and read the
totals line. To answer "today?" run `work report today`. A range with no
entries prints nothing (exit 0) — that means "no time recorded", not an
error.

## Finding entries (list / search)

```bash
timesamurai work list [range] [filters]
timesamurai work search <text> [filters]     # case-insensitive substring in descr
```

Shared filters: `--since` / `--until` (inclusive time bounds, same formats
as `--at`), `--min` / `--max` (inclusive value bounds, durations like `1h`,
`8h`), `--tag work`, `--action add`, `--host earth`, `--limit 20` (0 =
unlimited). `list` additionally has `-d/--descr` (description contains
text). Add `--format json` for machine-readable output: the file's fields
plus an `address` (`host:id`) field on each row.

Table output looks like:

```
ADDRESS          ACTION  WHEN                 VALUE  TAGS   DESCR
earth:146        add     2023-03-23 10:34:50  7200   selfdevelopment  Podcasts
```

The **ADDRESS column (`host:id`) is the key to modify/delete**. Copy it
verbatim from the output; never invent ids. Rows are sorted **oldest first**,
and `--limit N` keeps the N *oldest* rows — so to see recent entries use
`--since` (or `search`), not `--limit`. `list` without a range spans all
hosts, so always combine a range or `--since` with `--limit`.

## Changing entries (modify / delete / undo / edit)

```bash
timesamurai work modify <host:id> [--action login|logout|add] [--at time]
                       [-d descr] [--value 1h] [--tags work,pet]
timesamurai work delete <host:id> [<host:id> ...] [--dry-run]
timesamurai work undo [--host <name>]
timesamurai work edit [range]
```

- `modify` changes **only** the flags you pass. `--tags` is comma-separated
  and **replaces** the whole tag list (it does not append). `--value` is a
  signed duration or bare seconds. Host and id can never be changed.
- `delete` accepts several addresses, but a multi-address delete without
  `--dry-run` asks for interactive confirmation (`[y/N]`) — it can hang or
  cancel in a non-interactive context. Run with `--dry-run` first when unsure.
- `undo` reverts exactly **one** change, LIFO: the newest insert/modify/delete
  **made from this machine** (searching all hosts' undo logs).
  `undo --host X` instead pops the newest change in **X's** log, no matter
  which machine made it. It is not a general "undo last N".
- `edit` opens entries in `$EDITOR` as a text block for a range.

Typical fix flow:

1. `timesamurai work search "thing"` (or `list` with filters)
2. Read the `host:id` address from the table
3. `timesamurai work modify <host:id> --value 2h --tags work`
4. Verify the entry: `timesamurai work list --since <the entry's date> --limit 20`
   and check the row for your `host:id` — `--since` must be on or before the
   entry's date, otherwise it won't show (plain `list --limit N` shows the N
   oldest entries across all hosts, not the one you just changed)
5. If it was wrong: `timesamurai work undo`

## Time formats (`--at`, `--since`, `--until`)

All accept:

- Clock time: `9:30` or `9:30:05` — always applied to **today**.
- `today`, `yesterday` — midnight of that day.
- ISO-8601 / RFC3339: `2026-09-12T14:30:00Z` (or with offset).
- Local date/time: `2026-09-12`, `2026-09-12T14:30`, `2026-09-12 14:30:05`.
- Relative offsets from now: `-2h`, `+30m`, `-24h`. Only `h`/`m`/`s` units
  work — there is no `d`; use `-24h` for a day.
- A bare integer is **unix epoch seconds** (not a clock time).

Defaults: `--at` is now; `--since`/`--until` are inclusive bounds.

## Tags and accounting

Default configuration categories (see config for the live lists):

- `work` — default tag; worked time.
- `lunch` — subtracted from the report (minus category).
- `off`, `sick`, `bank`, `bufferuse` — added as positive (plus category).
- Buffer categories: `tools`, `pet`, `selfdevelopment`, `workrebalance`,
  `compensate`, `travel`, `rebalance` — tracked separately, movable into
  work via `usebuffer` (only `selfdevelopment` is drawn by `usebuffer`).
- Any other tag is a label; it is stored but not accounted.

An entry gets **one** primary accounting tag (work/plus/minus). If you pass
several primary tags, the command errors (`multiple accounting tags`).
Buffer tags can ride along as extra labels.

## Hosts, storage, config

- Every entry is recorded for a host. Default: the current machine's
  hostname. `--host <name>` records elsewhere instead; it exists on
  `start`, `stop`, `add`, `sub`, `day-off`, `usebuffer`, and `import`
  (and as a *filter* on `list`/`search`; on `undo` it means something
  different — see above).
- `timesamurai work --store <dir>` overrides the JSONL store directory for
  the whole `work` command tree. **Use this for experiments** — see below.
- `timesamurai work --db <dir>` overrides the legacy `db.*.json` directory.
- `timesamurai --config <path>` selects a different config file.
- Config file: `$XDG_CONFIG_HOME/timesamurai/config.toml` (usually
  `~/.config/timesamurai/config.toml`). Precedence, highest first:
  command-line flags → `TIMESAMURAI_*` environment variables → config
  file → built-in defaults. `store_dir` defaults to
  `~/git/worktime/timesamuraidb`.
- `timesamurai completion bash|zsh|fish|powershell` prints a completion
  script.

## Safe experiments

To test any command without touching the real log, point at a throwaway
store:

```bash
timesamurai work --store /tmp/ts-test add 1h -d "experiment"
timesamurai work --store /tmp/ts-test report
rm -rf /tmp/ts-test
```

Do this when the user asks "what would happen if..." or before trying a
tricky `modify`/`delete`. Real data mutations (start/stop/add/sub/modify/
delete) should be made deliberately, one at a time, and verified.

## Legacy import/export (only when asked)

- `timesamurai work migrate` — one-shot import of the old Ruby
  `db.<host>.json` files into the JSONL store (`--force` to re-run).
- `timesamurai work export [--strict]` — rewrite legacy `db.<host>.json`
  from the JSONL store (keeps the old `worktime.rb` tool working).
- `timesamurai work import <file> [--host h]` — import report.txt-format
  lines as work/lunch/off entries.

Do not run these unless the user explicitly asks for a migration/export.

## Gotchas

- Bare integers: in durations = **seconds**; in `--at` = **unix epoch**.
- `login`/`logout` entries have `value` 0 — their hours only appear in
  reports. Don't "fix" them by adding a value.
- `week` = current ISO week starting Monday, not a rolling 7-day window.
- `modify --tags` replaces all tags; include the tags you want to keep.
- Plain `undo` reverts one change, only from this machine, in LIFO order.
- To move a clock-in/clock-out, `modify <host:id> --at 10:30`. Passing
  `--value` on a login/logout entry is rejected.
- A report may print warnings without failing, e.g.
  `warning: skipped host:id (logout without a matching login) at epoch N`
  (after a deleted or inconsistent entry) or `warning: superseded login
  discarded (never logged out): …`. Those are warnings, not failures.
- Never hand-edit the JSONL files; use modify/delete/edit/undo.
- When in doubt about a flag: `timesamurai work <cmd> --help` is
  authoritative. `-v/--verbose` on any `work` command prints full entry
  details instead of a one-line confirmation.
