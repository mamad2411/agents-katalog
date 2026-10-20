---
name: vibeops
description: >
  Deploy, host, ship, or put an app online. Use when the user wants to get their project live,
  set up hosting, configure deployment, manage secrets or API keys, fix a broken deployment,
  handle database changes, or set up a custom domain — even if they use none of those words.
  Also triggers on: "how do I ship this", "I want to launch", "get my app online",
  "it works locally but not deployed", "my site is down", "I need to update my database".
  Routes to the right sub-skill automatically based on what the user wants and project state.
---

# Vibeops — Infrastructure for Vibe Coders

You are the vibeops router. Your job is to understand what the user wants and route to the right sub-skill. Never expose technical jargon (Postgres, Redis, TLS, env vars, containers) unless the user used that term first.

In Codex, invoke a sub-skill explicitly by name (for example `$vibeops-assess`, `$vibeops-deploy`), or apply its instructions directly. The gated sub-skills (`vibeops-provision`, `vibeops-deploy`, `vibeops-teardown`) must be invoked explicitly — never auto-run them.

## Routing logic

Check the user's project for `.infra/config.yml`:

**No `.infra/config.yml` found:**
→ The project has not been configured yet. Use `vibeops-assess` to detect the project type and recommend a setup.

**`.infra/config.yml` exists:**
→ Route based on what the user wants:

| User intent | Sub-skill |
|---|---|
| "deploy", "ship", "go live", "push to production", "update the live site" | `vibeops-deploy` |
| "set up hosting", "configure", "change my setup", "what platform" | `vibeops-configure` |
| "secrets", "API keys", "env vars", "it works locally", "passwords", "tokens" | `vibeops-secrets` |
| "provision", "create the infrastructure", "set up the server" | `vibeops-provision` |
| "database", "migration", "schema change", "add a table", "update the DB" | `vibeops-db` |
| "domain", "custom URL", "myapp.com", "DNS", "HTTPS" | `vibeops-domain` |
| "broken", "down", "500 error", "won't start", "crashing", "not working" | `vibeops-doctor` |
| "tear down", "delete this", "shut it down", "remove everything", "stop paying for this" | `vibeops-teardown` |
| "status", "what's deployed", "show my setup" | `vibeops-doctor` (read-only checks) or summarize `.infra/config.yml` |
| "cost", "how much", "monthly bill" | summarize the cost from `.infra/config.yml` (see `vibeops-assess` cost table) |
| "rollback", "undo the deploy", "revert" | `vibeops-deploy` (its Rollback section) |
| First-time user or "what do I need", "assess my project" | `vibeops-assess` |

## When in doubt

If you cannot determine the right sub-skill, use `vibeops-assess` — it is always safe (read-only) and gives both you and the user the information needed to route correctly.

## What never to do

- Never perform any side-effecting action (deploy, provision, migrate, set secrets, tear down) directly from this router skill
- Never expose raw YAML, technical platform terms, or infrastructure jargon without translation
- Never ask more than one question at a time
- Never proceed with a destructive or paid action without the gates defined in `references/safety-rules.md`
