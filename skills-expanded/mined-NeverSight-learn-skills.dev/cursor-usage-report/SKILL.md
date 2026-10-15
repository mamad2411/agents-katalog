---
name: cursor-usage-report
description: Generate a styled Excel report of Cursor usage by session for a given month or date range. Reads JSONL session logs from ~/.cursor/projects/**/agent-transcripts/, pulls token-level usage events from api2.cursor.sh (using the local IDE access token in vscdb), attributes events to sessions by timestamp, summarizes each session via cursor-agent (Haiku), and outputs an XLSX to the Desktop. Use this when the user asks for a Cursor usage report — phrases like "帮我总结X月份我的cursor报告", "总结我X月份的Cursor使用", "出X月Cursor报表", "我这个月在Cursor里做了什么", "summarize my Cursor usage for [period]".
---

# cursor-usage-report

Produces an Excel report of the user's Cursor activity, grouped by day, with one row per session: Date | 星期 | Project | Model | Duration | Msgs | Tokens | Cost | cursor-agent-generated summary.

## When to invoke

User asks to **summarize their Cursor usage** over a period — typically a month, a date range, or "last N days". Sample triggers:
- "帮我总结 4 月份我的 cursor 报告"
- "出一下我 3 月的 Cursor 使用报表"
- "我这个月在 Cursor 里都做了什么"
- "summarize my Cursor usage for April"

Do NOT invoke for:
- Per-token / per-dollar cost analysis → Cursor is subscription-based; transcripts have no usage field. Tell the user to check cursor.com Usage page instead.
- Single-session questions without a date scope → ask user for a date range first

## Workflow

### Step 1 — Determine the date range

Parse from the user request. Resolve relative dates against the current date.

- "4 月份" / "April" → first-of-month to last-of-month
- "上个月" / "last month" → previous calendar month
- "这周" / "this week" → Monday to today
- Custom range → use as-is

Always express as ISO dates: `--since YYYY-MM-DD --until YYYY-MM-DD` (since inclusive, until exclusive).

### Step 2 — Run the pipeline

Run the orchestrator from the **skill root directory** (the directory containing this `SKILL.md`) with a sensible output path:

```bash
node ./scripts/run.js \
  --since 2026-04-01 --until 2026-05-01 \
  --out ~/Desktop/cursor-usage-2026-04.xlsx
```

The script does four things internally and prints progress:

1. **extract** — scan `~/.cursor/projects/*/agent-transcripts/*/*.jsonl`, filter by file ctime (session creation time), parse user messages
2. **fetch usage events** — read the IDE access token from `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb` (key `cursorAuth/accessToken`), then call `POST https://api2.cursor.sh/aiserver.v1.DashboardService/GetFilteredUsageEvents` (Bearer JWT) for every event in the date range. Each event has model + `tokenUsage` (input/output/cacheRead/cacheWrite) + `chargedCents`. Events are attributed to sessions by timestamp falling inside `[ctime - 2min, mtime + 10min]`.
3. **summarize** — for each session not already in cache, send its user messages to `cursor-agent` for a one-line abstract summary (no verbatim copy). If `cursor-agent` is unavailable, print warning and continue with cache + heuristic summary.
4. **build-xlsx** — invoke `scripts/build-xlsx.py` to write the styled Excel

The script prints, in order:
- Progress for each step
- A final "统计 / Stats" block (session count, active days, project count, user message total)
- A final highlighted block with the **report file path** — this is the most important thing to relay to the user

Concurrency for summarization is 4 by default. ~100–200 sessions per month finishes in ~3–10 minutes depending on cursor-agent latency.

### Step 3 — Report back

When the script finishes, tell the user (in this order, terse):

1. **报表位置** — the Desktop xlsx path (paste verbatim from the final highlighted block; this is what the user wants most)
2. **总账** — total sessions, total tokens (M), total cost ($), active days
3. **归属率** — `X/Y events attributed, Z unattributed ($N)`. If unattributed > 30%, note it: most likely IDE-side requests (Tab autocomplete, Cmd+K inline edits, background composer) that don't write transcript files.
4. **Top 3 高消费日** with the heaviest session summary each — optional, only if it fits

Keep under 10 lines unless the user asks for more detail.

## Prerequisites (check before running)

- `node` >= 18
- `python3` with `openpyxl` (`pip3 install --user openpyxl` if missing)
- `cursor-agent` CLI on PATH and authenticated. Verify with `which cursor-agent`; it lives at `~/.local/bin/cursor-agent` on most installs.

If `openpyxl` is missing, run `pip3 install --user openpyxl` and continue — do not ask the user unless install fails.

## Notes / gotchas

- **Token / cost data source.** Cursor transcripts themselves don't carry usage. We pull them from `https://api2.cursor.sh/aiserver.v1.DashboardService/GetFilteredUsageEvents` using the IDE's JWT access token (read from the local vscdb). This is a private/undocumented API that powers the Cursor Settings → Usage page. **Always-true caveat:** Cursor can change or break this endpoint at any time without warning.
- **Token = sum of input + output + cacheRead + cacheWrite** as returned per-event. Cost is `chargedCents` (the value Cursor actually billed you for, after included quota and bonus credits).
- **Attribution rule**: an event is attributed to a session if its timestamp falls inside `[session.ctime - 2min, session.mtime + 10min]`. Multiple matches → pick the session whose mtime is closest to the event. No matches → goes into a red `(未归属)` footer row.
- **Unattributed events are normal.** Cursor's Tab autocomplete, Cmd+K inline edits, Composer in background mode, and various IDE-internal model calls do NOT create transcript jsonl files but still consume tokens. Expect 20–40% of events / spend to land in the `(未归属)` row, especially for users who lean on Tab heavily.
- **Most transcripts have zero attributed tokens.** Many `agent-transcripts/<uuid>.jsonl` files are short scratch sessions where the user opened Composer but didn't actually send a paid request. ~60–80% of session rows showing `tokens=-` is expected.
- **Timestamps come from file ctime / mtime**, not from inline event timestamps (which Cursor doesn't write). `firstTs = file ctime` (creation), `lastTs = file mtime` (last write). Duration = mtime - ctime; capped at `12h+` for sanity.
- **Session is included if ctime falls in `[since, until)`.** A session that started 2026-04-30 and was resumed on 2026-05-02 is still attributed to 2026-04-30; we do NOT split per-day for Cursor (unlike the Claude Code version).
- **Project label** is derived from the directory slug (e.g. `Users-yinminqian-Code-iHealth-needleApp` → `iHealth/needleApp`). The slug→path reverse is lossy (dots and spaces are eaten), so weird-looking paths happen — that's expected.
- **System / tmp slugs** (`var-folders-...`) and **bare numeric workspaceIds** are filtered out or labeled `(workspace#N)` since they aren't real projects.
- **Sessions with zero real user messages** (`<system_*>` only, automation, etc.) are dropped from the report.
- **The cache at `<skillRoot>/cache/`** is keyed by `md5(sessionFile + first 3 user messages)`. Safe to delete to force re-summarization.
- **Model**: default is `haiku-4.5` (cheap, fast). Override with `--model sonnet-4` if you want higher-quality summaries.
- **Access token comes from vscdb.** If `sqlite3` isn't on PATH or the user isn't signed into Cursor IDE, the script falls back to producing a report without Token/Cost columns and prints an explicit warning.
