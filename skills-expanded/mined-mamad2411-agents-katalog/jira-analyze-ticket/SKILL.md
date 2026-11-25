---
name: jira-analyze-ticket
description: Full analysis of a Jira ticket in one command. Use when user says 'analyze PROJ-123', 'jira-analyze', 'analyze this ticket', or 'analyze jira ticket'.
---

# jira-analyze

## Overview

Fetches a Jira ticket, its comments, linked issues, Confluence pages, and sprint/epic context, then delivers a structured analysis across four lenses: requirements clarity, technical feasibility, story breakdown, and key concerns. Detects staleness, surfaces drift, and concludes with a planning phase — either drafting a closure comment or producing an actionable story plan.

**Args:** `[ticket-key]` — Jira issue key (e.g. `PROJ-123`). Optional `-H` / `--headless` to skip all interaction and write directly to file.

**MCP dependency:** All Jira and Confluence fetching requires Atlassian MCP tools. If unavailable at any step, stop and ask the user to start the MCP server. Do not fall back to paste mode.

## On Activation

Load `workflow.md` and follow it from the beginning.

Run these git operations before any Jira fetching. Use `resolved_key` exactly as provided — the branch name is case-sensitive (e.g. `GRSC-14397`, not `grsc-14397`).
