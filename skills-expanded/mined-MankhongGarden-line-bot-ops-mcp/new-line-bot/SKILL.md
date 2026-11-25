---
name: new-line-bot
description: Start a new LINE bot project on Next.js and Supabase with create-line-bot, which ships a fast-ack webhook, a job queue the line-bot-ops tools can read, idempotency and LIFF login. Use when the user wants to build or scaffold a new LINE bot or LINE Official Account backend.
---

# Start a new LINE bot

1. Ask for a project folder name if the user didn't give one.
2. Run `npx create-line-bot@0.2.1 <folder> --install`. It copies the template and installs dependencies; it asks no questions.
3. Apply `supabase/migrations/0001_init.sql` from the new project to the user's Supabase database. It creates the `line_jobs` and `line_users` tables that `line_queue_health`, `line_failed_jobs` and `line_find_users` read.
4. Set the variables listed in the new project's `.env.example` on the hosting platform, deploy, then paste the webhook URL into the LINE Developers console.
5. Point this plugin's settings at the same LINE channel and Supabase project, then run `line_bot_info` and `line_queue_health` to confirm both connections.

The generated project also has its own `.mcp.json` that starts the same server from `node_modules`. Inside that project either one works; tell the user that two copies of the tools may appear and that they can disable one.

The generated README explains the webhook, the queue and the worker. Read it before changing that code.
