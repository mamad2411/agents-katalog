---
name: journal
description: Generate the daily work journal — collect today's AI usage across Claude Code, Copilot CLI, and Codex CLI plus git activity into a digest, then write the narrative, technical, and next-day-plan summaries. Use when the user asks for their work journal, daily summary, "what did I do today", or to plan tomorrow.
allowed-tools: Bash, Read, Write
---

# Daily work journal

Resolve the plugin root before shelling out: use `${CLAUDE_PLUGIN_ROOT}` if it is set; otherwise
resolve `../..` relative to this SKILL.md to an ABSOLUTE path (bash cwd is not the skill dir).
Call that root `$ROOT` below.

## Collect the digest

Run the collector to build today's digest from local, read-only sources:

```bash
python3 "$ROOT/bin/journal_collect.py"
```

Useful flags: `--date YYYY-MM-DD` for a specific day (default: today), `--repo PATH` to add a
git repo to scan (repeatable), `--print` to echo the digest to stdout as well as writing it.
The collector is deterministic and read-only over `~/.claude`, `~/.copilot`, and `~/.codex` —
it never calls a model and never touches the network. It writes only under the gitignored
`journal/<date>/` directory (`digest.json`), nowhere else. The digest now also deepens Codex
with the day's rollout files and, when tokens are found, carries a clearly-labeled
API-equivalent relative-burn proxy under `sources.codex_cli.extra.codex_proxy` — never a bill
(`billed_usd` stays null), never counted into `usd_priced`.

## Persist today's telemetry (right after collecting)

Capture the day's analytics into the durable store — the transcript dirs the digest
reads from ROTATE, and this snapshot is what survives:

```bash
python3 "$ROOT/bin/telemetry_snapshot.py"
```

It imports the analytics modules and calls their builders directly — read-only over
`~/.claude`, `~/.codex`, and `~/.copilot`, spawning no CLI and writing only under the
gitignored `telemetry/` (dated envelopes, one per source per day; same-day re-runs
overwrite, except that a failed re-run never replaces a good envelope). The envelope's
filename date is the LOCAL day — the same day this journal is keyed on, so an evening run
files under today, not tomorrow (`captured_at` inside each envelope stays UTC).
Best-effort: if it fails, note the failure and continue with the journal —
the snapshot never blocks the summaries.

## Write the summaries (in this session — default)

Get the exact prompts for today's digest:

```bash
python3 "$ROOT/bin/journal_summarize.py" --date <date> --dry-run
```

This prints the three prompts (narrative, technical, next-day-plan) without dispatching any
model — the current session is already paid for, so write the documents yourself instead of
spawning a nested call. Read `journal/<date>/digest.json` for the facts, follow each printed
prompt's required headings exactly, and use only digest facts — no invented details, no
transcript text. Save your three drafts as `journal/<date>/narrative.md`,
`journal/<date>/technical.md`, and `journal/<date>/next-day.md`. When done, summarize the three
documents for the user and link their paths — do not paste full drafts back into chat. When
`signals.harness` is present, follow the next-day prompt's `## Harness plan` section —
per-task harness + model tier + ready-to-paste command + one-line WHY, advisory only.

## Or run it headless

For an unattended run (e.g. from the nightly schedule) let the script dispatch a model itself:

```bash
python3 "$ROOT/bin/journal_summarize.py" --date <date>
```

This tries a routed cheap/mid model tier first, with at most one escalation to the next tier,
and exits with code 3 if any of the three documents still failed after that escalation. Use
`--start-tier` to pick the starting tier and `--model` to pin one model id explicitly (this
skips escalation).

## Inbox & schedule

Drop meeting notes or email to-dos into `journal/inbox.md` as plain lines; the next collection
folds them into the digest so they resurface as next-day to-dos. Read
`references/scheduling.md` when the user wants the journal to run unattended: the launchd
install/uninstall/status/run surface and the manual `launchctl` step it never performs for
them.

## Next-day runbook

Once a digest exists, build tomorrow's runbook — a dated, checkable plan of next-day tasks:

```bash
python3 "$ROOT/bin/journal_plan.py" build
```

It writes `journal/plan/<date>.md` — one dated, checkable card per planned task (drawn from
open kit tasks, WIP repos, the inbox, and `journal/plan/seed.md`), each with a What/How, an
ideal-harness line, and ready-to-paste commands for Claude Code, Copilot CLI, and Codex CLI
with cost estimates from the pricing files (Codex figures are API-equivalent proxies, never a
bill). Unchecked cards from earlier days carry forward automatically.

Enrich the What/How steps in this session (the current session is already paid for — the
summaries precedent): run

```bash
python3 "$ROOT/bin/journal_plan.py" prompt
```

follow the printed prompt exactly (rewrite ONLY the What/How bodies, keep every other line
byte-identical — the H1, checkboxes, field lines, and Harness blocks), and save the revised
document back over the same `journal/plan/<date>.md` path.

On the day tasks are due, check and track them:

```bash
python3 "$ROOT/bin/journal_plan.py" check
python3 "$ROOT/bin/journal_plan.py" done <id> --date <file-date>
python3 "$ROOT/bin/journal_plan.py" defer <id> --to <date> --date <file-date>
```

(or just edit the checkboxes in the markdown by hand — the file is yours). On quiet days,
hand-add lines to `journal/plan/seed.md` (same plain-line format as the inbox) and rebuild.

Advisory only: the runbook prepares and tracks — it never schedules or executes anything.
Every command above is text you choose to run, and there is no scheduler here by design (the
user tabled it).

## External tools (Teams / Outlook / Copilot Studio)

The journal has no Graph/OAuth/MCP connectors and never will by default: it never adds network,
OAuth, Graph, or MCP calls to fetch this content — any Teams/Outlook/Copilot Studio context
comes in only as offline text you carry over by hand. Read `references/ask-the-tools.md` when
the user wants that context folded into the journal: the offline ask-the-tools prompt pack and
the manual paste-back loop.

## Privacy

Writing the summaries sends the digest — project and repo names, commit subjects, kit task
titles, and any inbox text — to a model. The digest itself is metadata-only: it never carries
transcript or message text, only counts, ids, titles, and short strings like the above.
Everything the journal produces stays under the gitignored `journal/` directory; nothing here
is committed to git. Pasted ask-the-tools bullets become inbox text, so they also travel to
the model when you write the summaries.
