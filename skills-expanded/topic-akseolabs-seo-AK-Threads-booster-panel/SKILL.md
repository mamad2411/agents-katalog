---
name: panel
description: "Launch or prepare the optional local visual panel for AK-Threads-Booster. Use when the user asks for a dashboard, visual panel, local UI, data cockpit, or quick way to view tracker/compiled data."
version: "2.0.0"
allowed-tools: Read, Bash, Glob
---

# AK-Threads-Booster Local Panel Module

This module is the optional zero-token UI layer. It helps users inspect their tracker and compiled memory before asking the agent for deeper analysis.

## Scope

Use this module when the user asks to:

- open a local panel
- create a dashboard
- view tracker data visually
- inspect posts, topics, metrics, or compiled memory through a UI
- make AK-Threads-Booster easier for non-technical users

Do not run `/analyze`, `/topics`, `/draft`, `/predict`, or `/review` unless the user asks for AI interpretation after viewing data.

## Required Reads

Read these small files only:

- `panel/README.md`
- `panel/DESIGN.md`

You do not need the runtime budget prompt because opening the panel itself uses no model tokens beyond the current conversation.

## Data Boundary

- `threads_daily_tracker.json` remains the source of truth.
- `compiled/` files are optional display context.
- The panel must not fabricate data-backed claims.
- AI actions must be explicit user-triggered follow-up steps, not automatic panel load behavior.

## Launch Path

Preferred command from the workspace root:

```bash
python scripts/panel_server.py --open
```

If the user's tracker and companion files live outside the skill folder, pass that folder as `--data-root`:

```bash
python scripts/panel_server.py --data-root "<user data folder>" --open
```

If browser opening is unavailable, run:

```bash
python scripts/panel_server.py
```

Then give the user the printed local URL.

The server searches `--data-root` recursively for:

- `threads_daily_tracker.json`
- `compiled/next_move_queue.md`
- `compiled/account_state.md`
- `brand_voice.md`
- `style_guide.md` / `寫作風格指南.md`
- `posts_by_date.md` / `歷史貼文-按時間排序.md`
- `posts_by_topic.md` / `歷史貼文-按主題分類.md`
- `comments.md` / `留言記錄.md`

## Coverage Guarantee

Every user should see useful panel data in this order:

1. If `threads_daily_tracker.json` exists, the panel computes core analysis from the tracker alone: totals, median views, recent average, P90 threshold, performance distribution, time slots, content types, topic ranking, top posts, low performers, and conversation signals.
2. If companion files exist, the panel adds readable archives: posts by date, posts by topic, comments, brand voice, and style guide.
3. If compiled memory exists, the panel adds next-move and account-state blocks.
4. If optional files are missing, the panel still loads and shows source/companion coverage so the user knows which layers are present.
5. If the user clicks rebuild, the local server runs `scripts/build_compiled_memory.py` and writes `compiled/` beside the discovered tracker.

Do not promise that every optional block will be populated for every user. Promise that the tracker-only analysis layer will appear whenever a valid tracker exists.

## Fallback Path

If Python is unavailable, tell the user to open:

```text
panel/index.html
```

Folder access may require a Chromium browser. File import still works without folder access.

## Output Shape

Keep the response short:

1. Confirm the panel is local-only and zero-token at rest.
2. Give the local URL or file path.
3. Mention that AI analysis starts only when they ask for it.
