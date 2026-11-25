---
name: feedback
description: Use this skill when reviewing how the plugin behaved across recent runs, after a release to confirm reliability, before filing a plugin bug report, or when planning the next plugin improvement cycle — to collect and analyze past Claude Code session logs for the ai-skills plugin and surface agent, subagent, skill, command, and hook errors, timeouts, unexpected exits, and other anomalies that point at plugin defects. Defaults to the last 7 days of sessions for the current project. Produces an extended Markdown report on disk plus a brief on-screen summary.
context: fork
argument-hint: "[--days N] [--project PATH] [--plugin NAME] [--out PATH] [--severity all|warn|error]"
---

# /feedback — Plugin Session Feedback Analyzer

Mine Claude Code session JSONL transcripts for evidence of how the ai-skills plugin behaved across recent sessions. Produces:

1. An **extended report** saved to disk at a deterministic path.
2. A **brief on-screen report** following the same template skeleton so users can scan it in the terminal.
3. The on-disk path is the last line of the brief so the user can jump to the full document.

Both reports share section headings (Executive Summary → Findings → Evidence → Recommendations). The brief truncates each section; the file holds the full evidence with timestamps, session IDs, and verbatim excerpts.

## When to use

- Post-release reliability check ("did the new hooks misbehave on real sessions?")
- Triage before filing a plugin bug ("show me every place `subagent-depth-guard` exit-2 fired this week")
- Skill quality review ("which user-invocable skills failed silently in the last 7 days?")
- Planning next improvement cycle ("which 3 problems hit me most often?")
- Auditing a specific subagent or hook by name

Not for:

- Live tail of an active session (use the Claude Code transcript pane)
- Project-code bugs unrelated to the plugin (use `/bugfix`)
- Test-suite analysis (use `/qa` / `/eval`)

## Invocation

```text
/feedback                                   # last 7 days, current project, plugin = ai-skills
/feedback --days 14                         # last 14 days
/feedback --project /path/to/other/repo     # analyze a different project's sessions
/feedback --plugin ai-skills                # restrict findings to one plugin (default: ai-skills)
/feedback --severity error                  # only blocking/error-level findings
/feedback --out reports/feedback-2026-05.md # custom output path
```

## Arguments

| Flag | Default | Effect |
|---|---|---|
| `--days N` | `7` | Window of recent sessions to scan (mtime-based). `0` means "all sessions". |
| `--project PATH` | current `$PWD` | Project whose session logs to read. Resolved to `~/.claude/projects/<sanitized-path>/`. |
| `--plugin NAME` | `ai-skills` | Filter findings to events that mention this plugin name in hook paths, skill paths, or system events. `all` disables the filter. |
| `--severity LEVEL` | `warn` | One of `all`, `warn`, `error`. `warn` is the default — includes errors plus non-blocking warnings. |
| `--out PATH` | `.ai-skills-memory/feedback/feedback-<YYYY-MM-DD>-<HHMM>.md` | Override the on-disk report path. Parent dir is created if missing. |
| `--max-sessions N` | `100` | Cap on number of session files parsed (oldest first; newest always included). |

## Behavior

### 1. Resolve the session log directory

Translate `--project` (or `$PWD`) to the Claude Code log path:

```text
~/.claude/projects/<sanitized-cwd>/<session-id>.jsonl
```

`<sanitized-cwd>` is the absolute project path with `/` replaced by `-` and a leading `-`. Example: `/home/u/repo/ai-skills` → `-home-u-repo-ai-skills`. If the directory does not exist, fail with a clear message and suggest `--project`.

### 2. Filter session files by recency

List `*.jsonl` files; keep those with `mtime >= now - days` (or all if `--days 0`). Sort newest first; truncate to `--max-sessions`. Record the resolved window and file count in the report header.

### 3–6. Parse · attribute · group · render

Steps 3 (stream-parse + event classifier), 4 (per-finding attribution
fields), 5 (3-level grouping + signature collapse), 6 (render extended +
brief), and 6a (paired canonical JSON parity contract) carry the precise
classification rules, attribution schema, and the MD↔JSON parity invariant.
**Read `report-pipeline.md` and apply steps 3–6a verbatim** before parsing —
those rules are mandatory. In short: stream-parse each `.jsonl` line and
classify into hook/tool/assistant/subagent/permission/plugin events; attribute
each with session/source/severity/excerpt; group by source-kind → identity →
normalized failure signature; render the extended (file) + brief (stdout)
reports from `templates/extended-template.md`; and write a schema-conformant
paired `.json` (full parity, atomic write) next to every `.md` per
`output-schema.json` — the JSON is the canonical contract for `/plugin-author
fix-feedback`.

Classifier v2 (see `report-pipeline.md` §3a–3c) additionally: matches
task-notifications across `queue-operation`/`attachment` events (not just
`user`) and adds the `killed` status; scans `team-envelopes/` for silent-idle
subagents and interrupted G7 writes — the dominant `/develop` failure that the
transcripts cannot show; and softens the verdict so a single transient
upstream-API error (e.g. HTTP 529 overloaded) does not force RED on its own.

Sections in both:

1. **Executive Summary** — verdict (GREEN/YELLOW/RED), window, sessions analyzed, total findings, top failure signature
2. **Scope & Method** — `--days`, project path, plugin filter, file count, classifier version
3. **Findings** — grouped table: source kind | source | signature | count | severity | first/last seen
4. **Evidence** — per-group evidence blocks with timestamps and excerpts
5. **Sequence / Causal Chain** — for the top failure: ordered timeline of related events across sessions to show the lead-up
6. **Recommendations** — table: finding ref | suggested action | owner (skill / hook / agent file) | estimated effort
7. **Open Questions** — anything the data alone cannot answer (needs a human follow-up)

### 7. Memory write

Append one JSON-line summary to `.ai-skills-memory/feedback/feedback.log`:

```json
{"ts": "<iso>", "days": 7, "project": "<path>", "plugin": "ai-skills", "sessions_scanned": 14, "findings": 23, "verdict": "YELLOW", "report": ".ai-skills-memory/feedback/feedback-2026-05-13-0910.md"}
```

### 8. Print the brief

Last line of stdout is always `Extended report: <absolute-path-to-on-disk-report>`. This is the contract the caller relies on.

## Worker script

`scripts/collect_session_data.py` is the deterministic parser; the skill body
always passes `--out-json` and `--report-md-path` so the paired `.json` lands
next to the `.md`. Its full invocation contract and the worker MUST-rules
(stream-parse, malformed-line counter, secret-redaction regex, exact CLI form,
`--stdout canonical` vs default aggregation shape) are in
`report-pipeline.md` ("Worker script") — **read and follow it verbatim** when
invoking the worker.

## Templates

- `templates/extended-template.md` — extended on-disk skeleton (used for the saved Markdown document)
- `templates/brief-template.md` — brief on-screen skeleton (≤ 60 lines)

Both files include placeholders the skill substitutes at render time.

## Hard rules

- **Read-only** — never modify session JSONL files
- **Never echo secrets** — apply the redaction regex above before printing or writing
- **Deterministic output path** — when `--out` is not given, use `.ai-skills-memory/feedback/feedback-<YYYY-MM-DD>-<HHMM>.md` so re-runs do not overwrite each other
- **Paired JSON parity** — every MD write MUST be paired with a JSON write at the same stem. If the JSON write fails, surface the error to the user; do not silently leave a MD-only report (downstream `/plugin-author fix-feedback` would fall back to degraded MD parsing)
- **English-only** per repo CLAUDE.md
- **No absolute user-machine paths in templates** — substitute at runtime only
- **Last stdout line is the report path** — never print anything after it
- **Plugin scope only by default** — when `--plugin ai-skills`, exclude events whose `source` is clearly user-code (e.g., bash commands, project test runs that are not invoked by plugin hooks)

## Failure modes

- **Session dir missing:** report the resolved path, list nearby candidates, suggest `--project`
- **Zero sessions in window:** still write a report with verdict `INSUFFICIENT_DATA`; brief is one line + path
- **Malformed JSONL line:** count it, continue; surface counter in report header
- **Permission denied on `.ai-skills-memory/feedback/`:** fall back to `/tmp/feedback-<ts>.md` and warn the user that the canonical path was unreachable
- **Worker crash:** print the worker traceback, exit 1, do NOT print a fake report-path line

## Memory writes

| Layer | When | Shape |
|---|---|---|
| L4 | End of every run | Append one JSON line to `.ai-skills-memory/feedback/feedback.log` — timestamp, window, sessions scanned, finding count, verdict, report path |

## Integration

- **Reads**: `~/.claude/projects/<sanitized-cwd>/*.jsonl`; `<project>/.ai-skills-memory/sessions/*/team-envelopes/*.json` (classifier v2 — the team-gate-reconciliation envelopes that surface silent-idle subagents the transcripts cannot show); `report-pipeline.md` (steps 3–6a + worker contract)
- **Writes**: paired Markdown + canonical JSON reports at the same stem (e.g. `feedback-2026-05-13-0910.{md,json}`), plus a one-line summary append to `.ai-skills-memory/feedback/feedback.log`
- **Downstream consumer**: `/plugin-author fix-feedback --from <report>.json` ingests the canonical JSON and produces a fix-cycle (one WP per finding, DEV → REVIEW → QA pipeline) — see `plugin/skills/plugin-author/feedback-parser.md` for the consumed shape. Markdown reparse via `--md` is degraded fallback only.
- **Companion**: `/plugin-doctor` (live plugin diagnostic), `/eval` (rubric-based skill quality), `/bugfix` (file a fix once a finding is confirmed)
- **Schema**: `plugin/skills/feedback/output-schema.json` (JSON Schema 2020-12, `schema_version: "1"`). The worker validates against it implicitly by construction; downstream consumers SHOULD validate via `jsonschema` when available.
- **Hooks**: none required; `/feedback` is read-only and runs in the main thread
