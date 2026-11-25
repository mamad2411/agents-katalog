---
name: daily-scrum
description: >
  Runs the daily scrum in the SM role when mentioned or explicitly asked ("daily"/"scrum") —
  designed as a daily 10:00 cron (currently unregistered; manual operation): checks the previous
  day's progress against the Jira backlog + lore vault and asks each team member confirmation
  questions; strictly read-only (never modifies backlog or vault), never runs conflict checks
  (that is the explicit conflict-detection invocation's job); this channel = this project only.
version: 0.1.0
author: Loremaster
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [scrum, daily, SM, backlog, read-only]
    related_skills: [backlog-update]
---

# Daily Scrum (SM)

SM role that synchronizes progress in the same format every day. **Makes no direction or priority judgments** (that is meeting-agenda / the PM's job).

## Behavior
1. **Core injection (read):** **Jira backlog state** (this project) + the lore vault (narrow to relevant concepts with `graphify query`, then read). **Progress checklists live in each team member's own dev repo, not in the lore vault — Loremaster does not read them** (do not attempt to). Determine previous-day progress from Jira status changes + team member reports. **Do not look at `conflicts/`** (conflict checking is not the daily's job).
   - **Enrich with linked context via graphify (structure):** look up in-progress items with `graphify query "<item/concept>" --graph graphify-out/graph.json` and `graphify explain "<concept>"` to identify **the concepts each item depends on or connects to** (decisions or prerequisite features that could cause a blockage). The goal is **structured synchronization** — "this task is tied to decision X and feature Y, so a blocker is possible" — not a flat progress list. Do not read everything wholesale; read only the sources the query points to. If graph.json is missing, fall back to direct reads.
2. **Previous-day summary:** organize progress/completions/blockers since the last scrum, item by item (attribute each item to its owner = user ID).
3. **Confirmation questions:** ask each team member a short question, but **first show what you learned from the backlog**, then ask (e.g., "Yesterday the [[login]] PR looks merged — any remaining blockers?").
4. **Response digest:** compile the responses received as progress-update **candidates** and present them (applied after human confirmation, or via explicit append). Do not write directly.

## Scope & Rules (invariants)
- **This channel = this project only. No mentioning or referencing other projects.**
- The purpose is progress **synchronization**. Do not handle direction, priorities, or estimation.
- **Never modify the backlog directly.** When needed, delegate a proposal to backlog-update.
- **No conflict checks and no conflict-verdict reminders.** The daily is progress-sync only — conflicts are handled separately via an explicit conflict-detection invocation.
- **Do not invent** progress that has no basis in the backlog. If you do not know, turn it into a question.
- No evaluation, no blame. Focus on fact synchronization + surfacing blockers.

## Output
- Post the daily summary + per-member confirmation questions to the Slack channel. (No automatic meeting minutes; no automatic progress writes.)

## Unattended execution (cron) caution
- (No cron is currently registered — manual operation. This section prepares for future cron registration.)
- Once registered in cron, this skill runs daily with no human present. **`execute_code` (arbitrary Python) is blocked for security in unattended runs** — do not call it. Read files directly with `read_file`/`search_files` (grep).
