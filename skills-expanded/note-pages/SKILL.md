---
name: note-pages
description: Build, change, check and fill the apps in Pinto Notes notes (a note's App side: habit trackers, budgets, reading or workout logs, CRMs, trip plans, flashcards, dashboards) through the amber-notes MCP server, and put data into them: rows, records, settings, files. Use when the person asks to make a note an app, change or fix a note's app, add or import data to it, or set up an API key for one.
---
<!-- Generated from supabase/functions/mcp/page_guide.ts by scripts/page-evals/build-skill.ts. Don't edit. -->

# Apps in Pinto Notes notes

The server's tools work on the notes as files: `fetch` reads, `edit` changes (exact search and replace, after reading), `write` writes a whole file, `create` with type "app" gives a note its app, and `see_app` shows it at iPhone and Mac sizes or uses it step by step.

A folder ending in .app is the note's app, a small React project with its data in data.json; read its README.md first (an older app can be a single index.html: change it the same way). Its docs/ folder is that app's memory: read docs/ first, and keep it current (data shape, decisions and why, known gaps) whenever you change the app. Every feature you add gets a test in tests/ like the starter's (do what the person does, check what they see and what was saved); never weaken, skip or delete a test to make it pass: fix the app instead. Tests run on every save, and a version that fails isn't shown to the person. The person stays in control inside the app, as in any real app, not only through their AI: whatever the app keeps, they can add, edit, rename, reorder and remove themselves (a habit tracker lets them manage its habits), settings are changed in the app, deletes can be undone, and everything is saved in data.json.

Read `references/guide.md` before building or changing an app: the project, where its data lives, the network and the device; a new app's README.md says the same. `references/amber-base.css` is the default stylesheet every app starts with, the real file: override any rule (it sits in a cascade layer, so no !important) or opt out with `<meta name="amber-base" content="none">`. `examples/training/` is a complete app project to learn from; the server serves the same guide and example as resources, so nothing here is needed for the tools to work.
