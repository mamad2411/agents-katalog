---
name: cost-report
description: Analyze historical Claude Code usage from local transcripts — spend by model, most expensive sessions, and sessions where a cheaper model would have sufficed. Use when the user asks what they've spent, which model they've been using, or where they could save.
allowed-tools: Bash, Read
---

# Historical cost report

Run the analyzer script that ships with this plugin. Use the `${CLAUDE_PLUGIN_ROOT}` env var
Claude Code sets for plugin-executed content; if it is unset, fall back to resolving
`../../bin/cost_report.py` relative to this SKILL.md to an absolute path:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/bin/cost_report.py" --days 30
```

Flags:
- `--days N` — lookback window (default 30)
- `--mode api|subscription` — framing (default: `billing_mode` from `${CLAUDE_PLUGIN_ROOT}/data/pricing.json`)
- `--top N` — how many top sessions to list (default 10)
- `--json` — print the report payload as JSON instead of markdown
- `--projects-dir DIR` — point the walk at a non-default transcript directory (the only way to run this against anything but the live `~/.claude/projects`)

The script walks `~/.claude/projects/**/*.jsonl`, extracts per-message model + usage (input/output/cache tokens), dedupes by message id, and prices everything from `data/pricing.json` (any `intro_pricing` window a row carries is applied by date).

## Presenting the results

The script emits markdown. Summarize it for the user rather than dumping raw output:

1. **Headline**: total API-equivalent cost over the window and which model dominated.
2. **By-model table**: as emitted.
3. **Downgrade candidates** (sessions on Fable/Opus with a small footprint — under ~50K tokens and few tool calls):
   - In `api` mode: present the dollar delta as savings ("these sessions would have cost $X.XX less on the Sonnet tier").
   - In `subscription` mode: present it as burn share ("these sessions spent rate-limit budget on Fable for Sonnet-sized work") — dollars are API-equivalent, not spend.
4. One actionable recommendation, e.g. a default-model or effort-level change, based on what the data shows.

If the script errors on unexpected transcript formats, show the error and the file it choked on — don't silently skip everything.

Two no-data outcomes are distinct, not both "broken": a **missing** projects directory exits
with `No transcript directory at <path>` and renders nothing; a **present-but-empty** directory
still renders the full report with a `no transcripts in window: <dir>` label — a zero-row report
is honest output, not a failure. Don't tell the user the tool is broken on either outcome, and
don't present the empty case's zeros as measured spend.
