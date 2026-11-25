---
name: scrape
description: Read-only structured extraction from pages, tables, listings, or web apps using Browser, Chrome, web fetch, or repo-local evidence; return JSON or tables.
---

# Scrape

Use this skill when the user asks to pull data from a page, table, listing, or web app.

## Workflow

1. Clarify the target URL and desired fields if not obvious.
2. Use the safest read-only inspection path:
   - `@Browser` for public/local unauthenticated pages
   - `@Chrome` only when signed-in browser state is required and approved
   - web fetch or repo-local fixtures when rendered interaction is unnecessary
3. Extract only the requested data.
4. Return JSON or a table with source notes.
5. If the flow is useful and repeated, suggest `skillify` to preserve it as a reusable browser skill.

## Guardrails

- Treat scraping as read-only.
- Respect authentication boundaries and site terms.
- Do not fabricate missing fields.
- Include selectors, URLs, or evidence notes when the extraction may need to be repeated.
