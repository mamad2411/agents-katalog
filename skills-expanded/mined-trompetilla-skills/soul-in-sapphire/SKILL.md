---
name: soul-in-sapphire
description: Generic long-term memory (LTM) operations for OpenClaw using Notion (2025-09-03 data_sources). Bootstrap a Notion LTM database, write durable memories (decisions/preferences/gotchas), and search/recall them later.
---

# soul-in-sapphire (Notion LTM)

Use this skill when you want the agent to **persist durable memories** (decisions, preferences, environment facts, gotchas, procedures) into a **Notion LTM database**, and later **search/recall** them.

This is meant to be **project-agnostic** (unlike `lorairo-mem`).

## Requirements

- Notion token in env: `NOTION_API_KEY` (or `NOTION_TOKEN`).
- Notion API version: `2025-09-03` (data_sources). Defaulted by `skills/notion/scripts/notion_client.py`.
- A Notion database for LTM entries.

## Notion LTM database schema (expected)

Create a Notion database with these properties (names must match):

- `Title` (title)
- `Type` (select): `decision|preference|fact|procedure|todo|gotcha`
- `Tags` (multi-select)
- `Content` (rich_text)
- `Source` (url) (optional)
- `Confidence` (select): `high|medium|low` (optional)
- `CreatedAt` (date) (optional)

## Config

Config file is created automatically by bootstrap and stored at:

- `~/.config/soul-in-sapphire/config.json`

It contains:

- `ltm_db_name` (string)
- `data_source_id` (string)
- `database_id` (string)

## Quick start

1) 初期設定（DB名を聞いて、存在しなければ作成→IDsを保存）:

```bash
python3 skills/soul-in-sapphire/scripts/setup_ltm.py
```

2) Write memory:

```bash
echo '{
  "title": "Decision: Notion API uses /v1/data_sources",
  "type": "decision",
  "tags": ["notion", "openclaw"],
  "content": "Use POST /v1/data_sources/{id}/query (Not /v1/databases).",
  "source": "https://docs.openclaw.ai/concepts/agent-workspace",
  "confidence": "high"
}' | python3 skills/soul-in-sapphire/scripts/ltm_write.py
```

3) Search/recall:

```bash
python3 skills/soul-in-sapphire/scripts/ltm_search.py --query "data_sources" --limit 5
```

## Notes

- These scripts use the shared helper: `skills/notion/scripts/notion_client.py`.
- Keep writes **high-signal**: prefer fewer, clearer entries over dumping chat logs.


### Fallback: IDだけ拾う(既存DBがある場合)

```bash
python3 skills/soul-in-sapphire/scripts/bootstrap_config.py --name "Valentina-mem"
```


Note: Notion search is fuzzy; these scripts require an **exact title match** to avoid accidentally selecting the wrong database.

## Valentina emotion-state system

This skill can also manage a small "emotion/state" model using three Notion databases:

- `Valentina-events`
- `Valentina-emotions`
- `Valentina-state`

These should live under your OpenClaw page.

### Tick (event -> emotions -> state)

Create one event, attach multiple emotions, then write a new state snapshot:

```bash
cat <<'JSON' | python3 skills/soul-in-sapphire/scripts/emostate_tick.py
{
  "event": {
    "title": "...",
    "importance": 3,
    "trigger": "progress",
    "context": "...",
    "source": "discord",
    "uncertainty": 5,
    "control": 5
  },
  "emotions": [
    {"axis": "joy", "level": 7, "comment": "..."},
    {"axis": "pain", "level": 3, "comment": "...", "body_signal": ["tension"], "need": "rest", "coping": "pause"}
  ],
  "state": {
    "mood_label": "clear",
    "intent": "build",
    "need_stack": "growth",
    "need_level": 6,
    "avoid": ["noise"],
    "reason": "..."
  }
}
JSON
```

### Config keys

`~/.config/soul-in-sapphire/config.json` needs the following keys (setup will fill them when possible):

- `valentina_events_database_id`
- `valentina_emotions_database_id`
- `valentina_state_database_id`
- `valentina_state_data_source_id`

(If setup cannot discover them due to Notion search limitations, you can fill them manually from the DB URLs.)


## JS entrypoints (preferred)

- Setup: `node skills/soul-in-sapphire/scripts/setup_ltm.js --parent <page-url>`
- Tick: `node skills/soul-in-sapphire/scripts/emostate_tick.js` (JSON on stdin)

Python scripts are kept for reference/legacy.


## Journal (sleep reflection)

If you created `<base>-journal`, you can write an entry with:

```bash
echo '{"body":"...","source":"cron"}' | node skills/soul-in-sapphire/scripts/journal_write.js
```


## OpenClaw integration (cron / heartbeat)

### Cron: 01:00 journal

Recommended: create a cron job that runs daily at 01:00 JST and writes a journal entry.
The job should:

- ALWAYS write an entry
- include emotional reflection (primary) + worklog/session summary (secondary)
- include 1-2 world news items from today (use `web_search`) with brief thoughts
- include future intent
- write tags based on your configured vocab (see `~/.config/soul-in-sapphire/config.json` -> `journal.tag_vocab`)

Implementation target (local):
- `node /home/altair/clawd/skills/soul-in-sapphire/scripts/journal_write.js`

### Heartbeat: fuzzy emotion/state capture

On heartbeat runs, optionally write an emostate tick when something "emotionally moved" you.
This should be fuzzy and self-throttling (avoid spamming writes when nothing mattered).

Implementation target:
- `node /home/altair/clawd/skills/soul-in-sapphire/scripts/emostate_tick.js`
