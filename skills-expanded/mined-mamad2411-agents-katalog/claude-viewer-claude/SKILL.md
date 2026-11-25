# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

A purely client-side web viewer for Claude CLI session files (`.jsonl` format found at `$HOME/.claude/projects/*/*.jsonl`). No backend. The user uploads a file, the browser parses and renders it as a chat-like conversation, and IndexedDB caches the raw file so a page refresh restores the view.

## Key Requirements

- **Input:** Claude JSONL session files — each line is a JSON object representing one event in the session.
- **Primary focus:** Render the user↔AI exchange (user prompts and assistant responses) as a readable chat log.
- **Secondary:** Collapsible one-line summaries for meta events (tool calls, file reads/writes, etc.) — collapsed by default.
- **Persistence:** Store only the raw uploaded JSONL in IndexedDB; re-parse on restore. Uploading a new file replaces the stored one and resets the view.

## Architecture Constraints

- Pure frontend — no server, no build server required for production.
- IndexedDB is the sole persistence layer; no localStorage, no cookies.
- The JSONL parser must handle unknown/future event types gracefully (skip or summarise rather than crash).

## Stack Decisions

No framework has been chosen yet. Prefer a minimal approach:
- Vanilla JS or a small library (e.g. Preact) over a heavy framework.
- No bundler if the scope stays small enough for ES modules.
- No external UI component libraries — keep the dependency count near zero.
