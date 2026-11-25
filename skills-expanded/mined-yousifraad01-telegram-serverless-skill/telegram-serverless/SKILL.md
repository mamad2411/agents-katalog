---
name: telegram-serverless
description: Create, configure, develop, troubleshoot, and deploy Telegram bots on Telegram's first-party Serverless platform (tgcloud CLI, @tgcloud/cli, npm create @tgcloud/bot, handlers/*.js, the sdk db/api/fetch runtime, BotFather CLI Access token). Use when the user mentions Telegram Serverless, tgcloud, cloud.telegram.org, a bot hosted by Telegram itself, or asks to add handlers, callback buttons, inline queries, database tables, migrations, or to fix a tgcloud push, migrate, login, or webhook problem. For a generic "serverless Telegram bot" request, confirm the platform first. Do not use for bots the user explicitly wants on Cloudflare Workers, AWS Lambda, Vercel, or another provider.
license: MIT
metadata:
  version: "1.0.0"
  verified-against: "@tgcloud/cli 0.1.2, Bot API 10.3, sources checked 2026-09-08"
---

# Telegram Serverless

Telegram Serverless runs a bot's backend on Telegram's own infrastructure. You write plain
JavaScript ES modules (`schema.js`, `lib/**`, `handlers/<update_type>.js`), deploy them with
the `tgcloud` CLI, and the platform owns the webhook, injects an authenticated Bot API client,
and provides a per-bot SQLite database. There is no server, no bot token in your code, and
no npm packages at runtime.

Official reference: https://core.telegram.org/bots/serverless

## 1. Establish the platform

- Requests naming Telegram Serverless, tgcloud, `@tgcloud/cli`, `npm create @tgcloud/bot`,
  `cloud.telegram.org`, or BotFather's Serverless menu: this skill applies.
- A bare "serverless Telegram bot" is ambiguous. Ask once whether they mean Telegram's own
  Serverless platform or a third-party provider. If they already named Cloudflare Workers,
  AWS Lambda, Vercel, or similar, keep that provider and do not redirect them here.
- Check suitability before scaffolding. The platform has no inbound HTTP endpoints, no cron or
  scheduled triggers, no queues, no npm packages at runtime, and no documented secrets store.
  If the request needs one of those, say so and propose the hybrid shape in
  [references/patterns.md](references/patterns.md) instead of forcing it onto the platform.

## 2. Inspect before acting

1. Look for an existing project: a `.tgcloud/` directory, `schema.js`, `handlers/`, `lib/`,
   or `@tgcloud/cli` in `package.json` devDependencies. Never re-scaffold or overwrite one.
2. Read the project's own `AGENTS.md` and `docs/tgcloud-sdk.md` if present. They are generated
   by the CLI and are the authoritative SDK reference for that project's CLI version.
3. Check tooling: `node --version` (18 or newer is required) and `npx tgcloud --version`.
4. Check state without spending credentials: `npx tgcloud status` (offline diff against the
   local snapshot) and `git status` if it is a repository. Note any uncommitted local changes
   and leave them intact.
5. Run the bundled lint before and after edits:
   `node <skill-dir>/scripts/lint-project.mjs <project-dir>`. It needs no credentials.

Full checklist: [references/setup.md](references/setup.md).

## 3. CLI ACCESS onboarding

Installing this skill needs no Telegram credentials. Creating, deploying, running, or
migrating a real bot needs the bot's **Serverless CLI access token**. This is not the Bot API
token; the platform keeps the Bot API token away from your code entirely.

Reuse valid existing authentication. If `.tgcloud/credentials` exists or `TGCLOUD_TOKEN` is
set, do not ask again; confirm with a real command such as `npx tgcloud webhook`.

When authentication is missing, show the user exactly this:

```text
CLI ACCESS required.
Enable Serverless for your bot in @BotFather and obtain its CLI access token.
Enter the access token in the local terminal when tgcloud login prompts.
```

Path in Telegram: **@BotFather → select the bot → Serverless → enable it → CLI Access →
Access token**. The token looks like `app123456:XXXXXX` (`XXXXXX` is a placeholder).

Collect only what is missing:

- the intended bot username (the bot must already exist in @BotFather),
- the target project directory,
- what the bot should do.

Verified setup flow (the argument is a directory, which may be named after the bot; it does
not select or authenticate the bot):

```bash
npm create @tgcloud/bot <project-directory>
cd <project-directory>
npx tgcloud login
```

`npm create` installs `@tgcloud/cli` locally, runs `tgcloud init`, and in an interactive
terminal offers to run `login` immediately. `login` prompts with hidden input, validates the
token against the platform, and stores it in `.tgcloud/credentials` (git-ignored).

Credential rules:

- The user types the token into their own terminal or another secure secret input. Never ask
  for it in chat, never echo it, never put it in commands, examples, source, logs, or commits.
- If your environment cannot run an interactive prompt, `tgcloud login` will refuse to run.
  Give the user the exact command to run locally and continue with work that does not need
  authentication (handlers, schema, lint). For CI, the documented alternative is the
  `TGCLOUD_TOKEN` environment variable supplied by the CI secret store.
- `.tgcloud/`, `node_modules/`, and any real secret files stay git-ignored.

Details and edge cases: [references/setup.md](references/setup.md).

## 4. Runtime rules that must hold

- Deployed files: `schema.js` at the root, `.js` under `lib/` (nesting allowed), `.js` under
  `handlers/` (flat). Nothing else is deployed. A stray root `.js` is flagged by the CLI.
- Import by bare module name only: `'schema'`, `'lib/cart'`, `'sdk'`, `'sdk/db'`. Relative
  paths and `.js` extensions do not compile.
- `handlers/<update_type>.js` default-exports `async function (payload, ctx)`. `payload` is
  the unwrapped update object (a `Message` for `message`, a `CallbackQuery` for
  `callback_query`); `ctx.update` is the raw `Update` with `update_id`.
- A handler runs only if the file exists and is non-empty. The platform derives the webhook's
  `allowed_updates` from the deployed handler set.
- Handler names are a closed set advertised by the platform (26 names on 2026-09-08;
  `stopped_message_generation` was not among them). `npx tgcloud add handlers` (no name)
  prints the accepted names the project does not have yet.
- `db` is SQLite through a Drizzle-style builder. Every call is async. Foreign keys throw at
  declaration. Drops happen only through `.deprecated('reason')` plus a confirmed migration.
- `api.<method>(params)` returns the unwrapped result and throws `BotApiError`
  (`.code`, `.description`, `.method`, `.parameters`). `setWebhook` and friends are restricted;
  the platform owns the webhook.
- `fetch` is outbound only, web-like, streams via `for await (const chunk of res.body)`,
  never throws on non-2xx (check `res.ok`), body readable once, 30 MB response cap.
- Execution time, memory, concurrency, timers, and log retention are undocumented. Keep
  handlers short, idempotent, and bounded.

Full runtime reference: [references/runtime.md](references/runtime.md).

## 5. Engineering workflow

1. Understand the requested behaviour and confirm the platform fits (section 1).
2. Inspect the project and read its generated docs (section 2).
3. Scaffold only when there is no project. Add handlers with `npx tgcloud add handlers/<type>`
   and shared code with `npx tgcloud add lib/<name>` (both refuse to overwrite).
4. Implement handlers and `lib/` modules. Put state in `schema.js` tables. Follow
   [references/patterns.md](references/patterns.md): answer `callback_query` first, dedupe on
   `update_id`, tolerate benign Bot API 400s, chunk text at 4096 characters.
5. Validate: run the lint script, then `npx tgcloud run handlers/<type> '<json5 payload>'
   --ctx '{ update: { update_id: 1 } }'`. `run` executes **remotely** with the real `api` and
   the bot's real database: it can send real messages and write real rows. Use a test chat id
   and non-destructive payloads.
6. Review what deployment will change: `npx tgcloud status`, `npx tgcloud diff`, and
   `npx tgcloud migrate --dry-run` (or `--local` to diff the local schema before pushing).
7. Deploy within the user's authorised scope: `npx tgcloud push`, then `npx tgcloud migrate`
   for schema changes. Code deploys never touch the database; migrations are a separate step.
8. Confirm: `npx tgcloud webhook` should report in sync with the deployed handlers. Then verify
   the requested behaviour in a real chat or with `run`.

`status` and `diff` are offline comparisons against the local snapshot. They do not prove
that a token is valid or that a deployment succeeded; only a networked command
(`push`, `webhook`, `migrate --dry-run`, `run`) does.

Deployment details, CI, and migration classes: [references/deployment.md](references/deployment.md).

## 6. Safety defaults

- Never use `push --force`, `migrate --yes`, or `webhook sync --drop-pending` as routine
  fixes. Each discards something (teammates' cloud revision, warning-class migration review,
  queued updates). Use them only after the user explicitly chooses that outcome.
- Resolve a revision conflict with `npx tgcloud fetch` or `npx tgcloud pull`, review, then push.
- In a non-interactive shell, `push` proceeds without the deletion prompt and `migrate`
  refuses to run without `--dry-run`, `--safe`, or `--yes`. Prefer `--safe`.
- Warning-class migrations (drops, large-table indexes) are confirmed one at a time by a
  human in a terminal.
- Treat `run` as production. Do not run handlers that delete or broadcast against real ids.
- Log status codes and ids, not tokens, response bodies, or user secrets.

## 7. Optional branches (only when the user asks)

- **Mini Apps**: the platform has no inbound HTTP, so a Mini App reaches the bot only through
  Telegram (`web_app_data` from keyboard-button launches, deep links). Anything needing an API
  or `initData` validation needs a backend the user hosts.
- **AI streaming**: `sendMessageDraft` is private-chat only, ephemeral (30-second preview),
  and must be followed by `sendMessage`. Do not rely on `can_stop` until the platform accepts
  a `stopped_message_generation` handler.
- **External services and secrets**: no documented secrets store; prefer a backend proxy
  with a per-bot bearer token.
- **Scheduled or background work**: not available on the platform; use the user's own
  worker tier.

All branches: [references/patterns.md](references/patterns.md).
Symptoms and fixes: [references/troubleshooting.md](references/troubleshooting.md).
Sources, dates, and verification status: [references/sources.md](references/sources.md).
Worked example (`/start` plus a callback button): [assets/examples/starter-bot/](assets/examples/starter-bot/).

## 8. Reporting

When you finish, tell the user which steps ran and which did not. Distinguish "lint passed
and `run` returned the expected result" from "pushed and webhook in sync" from "not deployed
because no CLI access token was available". Never report a deployment, login, or live test
that did not happen.
