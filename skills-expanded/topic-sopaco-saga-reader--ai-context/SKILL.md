# Saga Reader — AI Context

> Last updated: 2026-06-07

## Activation Rules

Read these files at session start when working on this project:

| When | Read |
|------|------|
| Session start | `references/PROJECT-ESSENCE.md` |
| Working across components | `references/ARCHITECTURE.md` |
| Changing patterns or design | `references/DECISIONS.md` |
| Debugging or handling blockers | `DYNAMICS.md` |

## Project Overview

Saga Reader (麒睿智库) — AI-driven reader that auto-retrieves internet content based on user interests, summarizes via cloud/local LLMs, and provides an AI companion reading feature.

**Stack:** Rust + Tauri (backend) · Svelte/SvelteKit (frontend) · SQLite/SeaORM (storage)

## Key Entry Points

| Area | Path |
|------|------|
| Tauri app entry | `app/src-tauri/src/lib.rs` |
| Frontend routes | `app/src/routes/` |
| Core API facade | `crates/feed_api_rs/src/features/api.rs` |
| LLM providers | `crates/llm/src/providers/` |
| Search scrapers | `crates/scrap/src/search/` |
| Article intelligence | `crates/intelligent/src/article_processor/` |

## How to Update This Knowledge

See `meta/MAINTENANCE.md` for update triggers and quality standards.
