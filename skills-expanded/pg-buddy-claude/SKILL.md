# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PG Buddy is a mobile-first single-page web app that helps a medical student prepare for India's NEET PG exam (August 2026). It features an AI study mentor powered by Google Gemini, a subject planner, motivational tools, and curated resources.

## Architecture

**Single-file app:** The entire application lives in one `index.html` file — all HTML, CSS, and JS inline. No build tools, no frameworks, no npm, no separate files.

- `index.html` — The complete app (output artifact)
- `PRD.md` — Full product specification (read-only)

**Tech stack:** Vanilla HTML/CSS/JS, Google Fonts (Playfair Display + Nunito), Gemini 2.0 Flash API via direct `fetch()`, `localStorage` for persistence.

## Key Constraints

- **No React, no build tools, no npm** — vanilla JS with DOM manipulation only
- **No separate files** — everything in `index.html`
- **Mobile-first** — max-width 480px, touch-friendly (44px min tap targets)
- **API key is intentionally client-side** — private single-user tool, no proxy/backend needed
- **Spin wheel uses `requestAnimationFrame`** — not CSS transitions (they're unreliable for this)
- **News is static** — uses hardcoded fallback items, no API call (Gemini free tier lacks grounding)

## App Structure (5 tabs)

1. **Home** — Greeting, streak tracker, countdown to exam, daily quote, progress summary, news, quick-access grid, journey badges
2. **Study AI** — Gemini-powered chat mentor with bookmarks, quick prompts, WhatsApp-style bubbles, chat persistence (50 messages max)
3. **Planner** — 19 NEET PG subjects with status tracking (not started/in progress/done), filters, detail modals, weightage chart, "Ask AI" integration
4. **Motivate** — SVG spin wheel with `requestAnimationFrame` animation (~3.5s cubic ease-out), reveals random quote
5. **Resources** — 9 curated links, fallback news, prep tips, app data reset

## localStorage Keys

All prefixed with `pgbuddy-`: `pgbuddy-subjects`, `pgbuddy-chat`, `pgbuddy-bookmarks`, `pgbuddy-streak`.

## Gemini API

- Model: `gemini-2.0-flash` via `generativelanguage.googleapis.com/v1beta`
- System prompt copied verbatim from the reference TSX file
- Chat history: last 20 messages sent as context
- Error messages: friendly fallback strings (no raw errors shown to user)

## Deployment

GitHub Pages from `main` branch, root `/`. Live at `https://zaryab2000.github.io/pg-buddy/`.

## Data Constants

All data constants live directly in `index.html`:
- 19 subjects with weightage, difficulty, topics, tips
- 50+ motivational quotes
- 11 resource links
- 5 fallback news items
- Theme color system (CSS custom properties)
