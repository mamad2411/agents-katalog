---
name: knock-setup
description: Connect Knock to your coding agent, discover and build notification workflows, and recommend how to trigger them from your application.
---

# Setup

End-to-end Knock setup for a coding agent: connect tooling, design and build notification workflows, then wire them into the application. Work through the rules below in order.

While working, keep every response to one short line — no summaries, no menus, no extra questions unless a step fails. The only exceptions are the opening encouragement + account ask (step 1), the workflow proposals, a prior-confirmation restatement (2–3 lines max), the implementation confirmation ask, the import-users id ask, the wrap-up signup-email ask (only when whoami has no email), the final wrap-up output, the ChatGPT and Codex in-app plugin surfacing, Codex CLI `/plugins` path, and new-session handoff in `rules/connect-codex.md`, and the Claude connector instructions in `rules/connect-claude.md` (directory link + connected ask), which have their own formats. When you end with a confirmation question (account, workflows, implementation, import-users id, wrap-up signup email, or wrap-up guides ask), that question must be the very last line of the message, on its own, and bolded.

## How to use this skill

**Grok Bot:** if this is Grok Bot (desktop/iOS teammate, Agent Computer, or `/workspace`), stop here and follow `rules/connect-grok-bot.md` instead of the steps below.

1. **Open with encouragement, then confirm Knock account** (required first action — do this before anything else)
   - **ChatGPT and Codex (in-app or Codex CLI):** skip this whole step. Do not ask about a Knock account. Do not install skills. Go to step 2 and follow `rules/connect-codex.md`. Plugin sign-in covers signup. The Codex IDE extension is unsupported — that rule will stop.
   - **Opening (first message only).** Before the account ask, say a short word of encouragement (about 2–3 sentences): they are going to save a lot of time building notifications with Knock, this was a good call, and we will give it our best shot to get them set up as fast as possible. Keep it warm and plain — not a feature pitch, not a menu of next steps.
   - **Default: always ask.** That same first message must then ask whether they have a Knock account. Do not add MCP, run OAuth, install skills, discover workflows, or call Knock tools until they answer.
   - **Skip the ask only if** the user's message explicitly says they started from the Knock dashboard (e.g. pasted a dashboard setup prompt, or says "from the Knock dashboard"). MCP already configured, a prior chat, or guessing they might have an account does **not** count — still ask. Still include the opening encouragement in that first message.
   - If they say no: do **not** send them to the dashboard to sign up separately. Tell them in one line that they'll create their account during the sign-in step — signup, onboarding, and returning here all happen in that one browser flow — then continue to Connect Knock tooling.
   - End the ask as the last line, bolded, e.g. **Do you already have a Knock account?**

2. **Connect Knock tooling for the current tool** (hard gate — do not discover, propose, or build workflows until a Knock MCP tool call, or `knock whoami` on the CLI path, has succeeded)
   - Route by tool family, then follow the **surface check at the top of that rule** (app vs CLI) — do not pick a path from this list alone:
     - **Cursor** (editor or Cursor CLI) → `rules/connect-cursor.md` — editor uses MCP; Cursor CLI is routed to `rules/connect-knock-cli.md`
     - **Claude** (app or Claude Code) → `rules/connect-claude.md` — app adds Knock from the connectors directory (give the user the directory link and wait); Claude Code is routed to `rules/connect-knock-cli.md`
     - **ChatGPT or Codex** → `rules/connect-codex.md` — identify the host interface (in-app, Codex CLI, or IDE extension). Do not use shell access to decide. In-app and Codex CLI use the Knock plugin; the IDE extension stops. Do not install skills separately.
     - **Any other terminal/CLI agent** → `rules/connect-knock-cli.md` — install the Knock CLI and auth with `knock login`
   - If the tool is unknown, ask which one, then follow the matching rule.
   - On the Knock CLI path, do **not** set up MCP at any point in this skill — no `claude mcp add`, no `codex mcp add`, no `mcp.json` edits, no connector ask. Use `knock` CLI equivalents wherever later steps mention Knock MCP tools.
   - Auth proof: call `list_environments` or `execute_mapi_read` `GET /v1/whoami` (MCP), or run `knock whoami` (CLI), and wait for success. Checking that MCP or the CLI is installed is not enough.

3. **Discover workflows** (`rules/discover-workflows.md`) — only after step 2 auth proof
   - If this conversation already has an approved build list from `knock-lifecycle-opportunities` or `knock-product-messaging-strategy`, skip rediscovery (see prior-confirmation gate in that rule).
   - Otherwise learn the product, propose high-value workflows, and confirm which to build.

4. **Build workflows** (`rules/build-workflows.md`)
   - Create confirmed workflows in the Knock development environment via MCP.

5. **Recommend an implementation approach** (`rules/recommend-implementation.md`)
   - Pick one trigger path, ask the user to confirm, then create branch `knock-implementation` before file changes.
   - For a Knock Data Source (CDP or custom HTTP), follow `rules/implement-data-source.md`.

6. **Wrap up** (`rules/wrap-up.md`)
   - Always send a test. Follow the MCP path or Knock CLI path in `rules/wrap-up.md` (do not mix). Shared recipient rules: whoami email + name, or ask for signup email only if missing. Then next steps, dashboard link, and close with Knock agent help.
   - Always mention setting up in-app notifications via `knock-in-app-ui`. If guides were created or mentioned, note that guides need app wiring — then **ask** before starting `knock-in-app-ui` (do not proceed until the user says yes).

## Extension rules (not on the first pass)

Use these when preparing for production or when the user asks — they are optional after the main flow:

- **Import users** (`rules/import-users.md`) — choose a stable Knock user id, research how users are stored, set `KNOCK_API_KEY`, and write a dry-run-first bulk-identify script. Do not run against production unless the user explicitly asks.

## Rule files reference

- `rules/connect-cursor.md` — Cursor: surface check, then editor MCP + skills install (Cursor CLI routes to `connect-knock-cli.md`)
- `rules/connect-claude.md` — Claude: surface check, then app directory connector (Claude Code routes to `connect-knock-cli.md`)
- `rules/connect-codex.md` — ChatGPT and Codex: host-interface surface check, then in-app plugin or Codex CLI `/plugins`
- `rules/connect-grok-bot.md` — Grok Bot escape hatch: intro, MCP connect, then route
- `rules/connect-knock-cli.md` — shared Knock CLI path: install + `knock login` auth for CLI-based tools
- `rules/discover-workflows.md` — Product discovery and workflow proposals
- `rules/build-workflows.md` — Build confirmed workflows with Knock MCP
- `rules/recommend-implementation.md` — Choose a trigger path, confirm, branch, then implement
- `rules/implement-data-source.md` — Source setup: identify user, mappings, MCP prompts, testing
- `rules/wrap-up.md` — Test send (separate MCP vs Knock CLI paths) + next steps, dashboard link, and Knock agent help
- `rules/import-users.md` — Extension: bulk-identify users for production readiness

## Quick reference

- MCP server URL: `https://mcp.knock.app/mcp`
- ChatGPT / Codex plugin: https://chatgpt.com/plugins/plugin_asdk_app_6a8dddd50424819196928510eff4c70f
- Knock CLI: install with `npm install -g @knocklabs/cli`, auth with `knock login` ([docs](https://docs.knock.app/cli/overview))
- Install open-source skills: `npx skills add knocklabs/skills`
- Prefer Knock MCP tools (or Knock CLI commands on the CLI path) for workflow, step, and template creation after tooling is connected
