---
name: seameet
description: >-
  Operate the SeaMeet desktop recorder via its MCP tools. Use when the user
  wants to record their screen or a meeting, transcribe audio, capture a
  reproducible bug report, take a screenshot, pull action items or decisions
  from past meetings, or search across recorded meeting transcripts and
  summaries.
---

# SeaMeet workflows

SeaMeet is a desktop meeting recorder + AI note taker. This plugin's MCP
server (`seameet`, from `@seameet/mcp`) exposes its tools; the SeaMeet
desktop app must be installed and **running** on this machine
(download: https://seameet.ai/download/).

## 0. Check app status first

If any tool returns `{"success": false, "error": {"code": "app_not_running"}}`,
ask the user to launch the SeaMeet desktop app, then retry. When the app is
closed, `tools/list` exposes only `seameet_desktop_app_status` — call it for
an actionable status. `app_not_ready` means the app is still starting: retry
in a few seconds. All tool errors are structured JSON — branch on
`error.code` (`timeout` → check `seameet_recording_status()`, retry once;
`not_found` → discover files with `seameet_list_recordings`).

## 1. Record and transcribe anything

1. Pick the source (ask the user or infer):
   - `microphone` — voice only (dictation, voice notes)
   - `screen` — screen video + microphone (demos, walkthroughs)
   - `both` — screen + mic + system/speaker audio (meetings, webinars)
2. Start: `seameet_start_recording(source=...)`. If it returns
   `needsClarification`, present the choices to the user.
3. Monitor: `seameet_recording_status()` for elapsed time;
   `seameet_get_live_transcript(lastN=20)` to follow along mid-recording.
4. Stop: `seameet_stop_recording()` → returns the saved `filePath`.
5. Retrieve artifacts (they generate shortly after stop; retry briefly):
   `seameet_get_artifact(filePath, key="transcription")` and
   `seameet_get_artifact(filePath, key="summary")`.
6. Optionally persist your own work:
   `seameet_save_artifact(filePath, artifactKey="notes", content=...,
   mimeType="text/markdown", generatedBy="claude")`.

Notes: only audio-only recordings can be paused
(`seameet_pause_recording`). Recordings save to
`seameet_get_settings().defaultSaveDirectory`.

## 2. Capture a bug report

When the user reports a bug you cannot reproduce, capture ground truth
instead of guessing from a text description:

1. Tell the user: "I'll record your screen while you reproduce the bug —
   narrate what you're doing and what you expected."
2. `seameet_start_recording(source="both")`.
3. Optionally poll `seameet_get_live_transcript(lastN=10)` to follow along.
4. When they're done: `seameet_stop_recording()` → `filePath`.
5. Gather evidence:
   - `seameet_get_artifact(filePath, key="transcription")` — the narration
   - `seameet_take_screenshot()` → `screenshotPath` at the moment of
     failure, then `seameet_get_artifact(screenshotPath, key="ocr-text")`
     — exact error text on screen
6. Debug from transcript + OCR. Quote the user's own words in the bug
   ticket; attach the recording `filePath` as the repro artifact.
7. Save your diagnosis back so it travels with the evidence:
   `seameet_save_artifact(filePath, artifactKey="bug-analysis", ...)`.

## 3. Turn meetings into work (action items, decisions)

Find the meeting:
- Most recent: `seameet_list_recordings(limit=5)` (newest first)
- By content: `seameet_search_text(query="pricing discussion")` — searches
  every summary, transcript, and action item; returns filePaths + snippets
- By date: `seameet_list_recordings(dateFrom="2026-07-01T00:00:00Z")`

Read the pre-generated artifacts — do not re-derive from the raw transcript
(check what exists with `seameet_get_asset_bundle(filePath)`):
- `seameet_get_artifact(filePath, key="action-items")` — JSON array
- `seameet_get_artifact(filePath, key="key-decisions")` — JSON
- `seameet_get_artifact(filePath, key="summary")` — Markdown
- `seameet_get_artifact(filePath, key="chapters")` — JSON outline

Act on them:
- Turn action items into tracker issues/todos, preserving owners and due
  phrasing from the source.
- Draft follow-up email from `summary` + `action-items`; save it back with
  `seameet_save_artifact(filePath, artifactKey="email-draft", ...)`.
- Different summary style? `seameet_list_templates()` then
  `seameet_regenerate_summary(filePath, templateSlug=...)`.
- "What did we decide?" → `seameet_search_text(query=...)`, then read each
  hit's `key-decisions` artifact; cite recording name + timestamp.

## References

- Full tool reference (LLM-oriented): https://seameet.ai/llms.txt
  (also served locally at http://localhost:3741/llms.txt while the app runs)
- Canonical skill recipes:
  https://app.seameet.ai/.well-known/skills/index.json
