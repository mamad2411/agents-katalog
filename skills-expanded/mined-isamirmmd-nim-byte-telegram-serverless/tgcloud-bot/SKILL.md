---
name: tgcloud-bot
description: Start, scaffold or grow a Telegram bot on Telegram Serverless (tgcloud) with a proven architecture — tgcloud/ layout (schema, lib per feature, thin handlers and endpoints), users tracking, a /start menu, deep links, multi-step input, feedback to the admin, offline tests on a mock SDK, and auto-deploy on GitHub Actions; optionally a React Mini App. Admin tools (`npm run sql`, admin commands, an admin panel, scheduled jobs, secrets) are added on request from references/admin-tools.md. Use when the user wants to create, scaffold, start or set up a new Telegram serverless / tgcloud bot (or Mini App), asks to "use tgcloud-kit", asks for one of those admin tools, or wants an existing tgcloud project brought to this structure.
argument-hint: "[admin telegram id] [what the bot should do]"
---

# tgcloud bot: start here

This is the entry point of **tgcloud-kit**. It turns an empty folder into a
working Telegram Serverless bot with the architecture of a production bot, then
builds the requested features on it. The architecture and its conventions are
in [references/architecture.md](references/architecture.md). Read it before
writing feature code. The scaffold also copies it into the project as
`docs/ARCHITECTURE.md`.

The Bot API is at **10.4** (November 2026).
[references/bot-api.md](references/bot-api.md) lists every update type (one
handler file each) and the newer features: ephemeral messages, rich messages,
streaming drafts, disabled buttons, guest mode, widgets. Read it before using
a Bot API feature you're unsure of. The project gets a copy as `docs/BOT-API.md`.

Sibling skills in this kit:

| Skill | Use it for |
|---|---|
| **tgcloud-endpoints** | Writing Mini App endpoints: auth, errors, pagination |
| **tgcloud-mini-app** | The React front-end: wiring, styling with the Telegram theme, deploy |
| **tgcloud-widgets** | HTML widgets inside messages (Bot API 10.4): sendWidget, `widget_query`, the widget's state |

## Step 1: Inputs

Take them from `$ARGUMENTS` or the conversation. Ask only for what is missing:
- **Admin Telegram user id**: a number. The user gets it from @userinfobot.
  It receives the users' feedback, and any admin tool added later checks it.
- **What the bot does**: the features. These decide whether it needs a
  **Mini App** (dashboards, forms, catalogs → `--mini-app`).
- **Design system**, whenever the bot gets a Mini App (now, or later when one
  is added): always ask, as a choice with two options:
  - **Default**: the starter's look. It uses Telegram's own theme colors
    (light, dark and custom themes, automatically) and the system font.
    Nothing more to provide.
  - **My own design system**: the user types or links it: a website or Figma
    link, a CSS / design-tokens file, a design-system skill they have
    installed, a UI library (Tailwind, MUI, …), or a description (colors,
    font, corner radius, mood).

  In Claude Code use AskUserQuestion with these two options; its free-text
  answer carries the details of their own system. Other agents ask the same
  two options in the chat. Don't pick for the user. After the scaffold, apply
  the answer with the tgcloud-mini-app skill (Step 1b) and record it in
  `docs/DESIGN.md` (the scaffold writes it as "Chosen by the user: not yet").
- **Project folder**: default to the current directory when it's empty or
  already a tgcloud project. Never scaffold into the tgcloud-kit repository
  itself: if the current folder is the kit's repo, use a new sibling folder
  (e.g. `../my-bot`), because the bot becomes its own git repository.

## Step 2: Scaffold

In the project folder:

```
npx -y @tgcloud/cli@0.2.0 init                  # skip if tgcloud/ already exists; writes AGENTS.md, docs/tgcloud-sdk.md, tgcloud.jsonc, git repo
node "${CLAUDE_SKILL_DIR}/scripts/scaffold.mjs" . --admin <ADMIN_ID> [--mini-app] [--title "<app title>"]
npm install
npm test                                          # 12 offline tests (15 with --mini-app) must pass before you change anything
```

The kit's repository also has `scripts/create-bot.mjs`, which does all four
steps for a new folder:
`node <kit repo>/scripts/create-bot.mjs ../my-bot --admin <ADMIN_ID> [--mini-app]`.

`scaffold.mjs` overlays the template and never overwrites the user's files. It
only replaces the stock `init` versions of `schema.js` and
`handlers/message.js`. It adds:

- `tgcloud/`:
  - `schema.js`: `settings`, `users`
  - `lib/`: config, settings, users, feedback, access, menu, i18n, query,
    html, time, files
  - `handlers/`: `message` (`/start`, `/stop`, `/help`, reply-keyboard buttons and back, feedback),
    `callback_query`, `my_chat_member`
  - `endpoints/`: `me` (the caller's own profile)
- `test/` (a mock SDK on node:sqlite)
- `.github/workflows/deploy.yml`
- `docs/ARCHITECTURE.md`, `docs/ADMIN-TOOLS.md` and `docs/BOT-API.md`, plus a
  pointer section in `AGENTS.md`
- npm scripts (`test`, `deploy`, `migrate`, `status`, …)
- `.claude/settings.json`, which enables this kit for the project. Pass
  `--no-claude-settings` to skip it.

`--mini-app` adds:
- the React + Vite front-end: the user's profile and a feedback form, styled
  with Telegram's own theme colors;
- `endpoints/feedback.js` (validated, throttled) and its tests;
- `docs/DESIGN.md` (the default design, "Chosen by the user: not yet");
- `tgcloud.jsonc` → `"static"`.

**No admin routes or admin commands are scaffolded.** There is no `/api/sql`,
no `/stats` or `/backup`, no admin panel and no scheduled job until the user
asks for one. See Step 6.

## Step 3: Link to the bot (the user does this)

`tgcloud login` is interactive, so ask the user to run it. In Claude Code they
can type `! npx tgcloud login`. The token comes from **BotFather → the bot →
Serverless → CLI Access → Access token**. Never ask them to paste the token into
the chat.

Serverless isn't open to every account yet. If the user has no Serverless
section or can't enable it, they request access first: open the BotFather Mini
App, create a new bot, go to its **Serverless** section and request access.
Once BotFather messages them that their whitelist is open, they can continue.
The scaffold and `npm test` work offline in the meantime.

Then:

```
npm run deploy                        # push the code (builds the Mini App first if there is one)
npx tgcloud migrate                   # create the tables (interactive; or `npx tgcloud migrate --safe`)
```

Then the admin sends `/start` to the bot. **The bot sets up Telegram by
itself** (`syncBotSetup()` in `lib/menu.js`), so nothing is set by hand in
BotFather:
- the command list, in English and Persian (`setMyCommands` with `language_code`);
- the Mini App button next to the input field (`setChatMenuButton`), in each
  user's language.

It calls Telegram only when something changed. With a Mini App, put the URL
that `push` printed in `MINI_APP_URL` (`lib/config.js`) and deploy: the next
`/start` shows the button.

## Step 4: Build the features

Follow the architecture. Summary:

1. **Schema**: tables go in `tgcloud/schema.js`. New columns on existing tables
   are nullable or have a default. No foreign keys. Drop only with
   `.deprecated()`.
2. **Logic**: one `tgcloud/lib/<feature>.js` per feature, holding its queries,
   its Bot API calls, and its `handleXCallback(query)` that returns `true`
   when a button was its own.
3. **Entry points**: keep them thin.
   - Public bot commands: a line in the public section of
     `handlers/message.js`.
   - Buttons: a `<feature>:` prefix in `handlers/callback_query.js`.
   - Deep links: `startPayload()`.
   - A question and its answer: `askFor()` / `takePending()`.
   - Mini App calls: `endpoints/<name>.js`. Use the tgcloud-endpoints skill.
   - Other update types (reactions, join requests, payments, …): a new
     `handlers/<type>.js`. The types are listed in
     [references/bot-api.md](references/bot-api.md).
   - Interactive messages (a live counter, a poll, a small game): widgets,
     with the tgcloud-widgets skill.
4. **Tests**: `test/<feature>.test.mjs` with the helpers (`msg`, `press`,
   `ctxOf`, `take`, `failNext`, `row`). Run `npm test`. See the existing
   tests for the shape.
5. **Check in the cloud** when the Bot API's real behavior matters:
   `npx tgcloud run handlers/message '{ text: "/help", from: { id: <ADMIN_ID> }, chat: { id: <ADMIN_ID>, type: "private" } }'`.

Code patterns (buttons, upserts, files, channel posts, deep links, ephemeral
replies) are in [references/patterns.md](references/patterns.md).

Rules that break bots most often (AGENTS.md has the full list):
- **Every action has a way back.** Every screen a button (inline or reply
  keyboard) or a command opens has `🔙 Back` to the screen before it, and a
  final result has `🏠 Main menu`. Only the root has none. Add screens to
  `SCREENS` / `KEYBOARDS` in `lib/menu.js` with a `parent`, and the back
  button comes automatically. Use `withBack(lang, …)` for keyboards a feature builds
  itself. The navigation test fails when a screen leads nowhere.
  ([patterns](references/patterns.md#menus-as-screens-always-with-a-way-back))
- Relative imports **with `.js`**. Import the SDK by name. No npm packages,
  filesystem or env vars at runtime.
- `await` every DB call.
- Raw SQL returns raw values (0/1, strings), so convert them.
- `push` never changes the DB. Schema changes need `migrate`.
- Every endpoint can be called by every Mini App user. Authorize from
  `ctx.initData.user.id` inside each one, and validate `input`.
- **English by default, and bilingual.** Every user-facing text goes in
  `lib/i18n.js`, in English and Persian (`t(lang, 'key')`, with
  `const lang = await userLang(user)`). Never hard-code user text in handlers
  or lib modules. Users switch languages in the 🌐 Language screen; otherwise
  their Telegram app's language decides (Persian for `fa`, English for
  everything else). The Mini App follows the same choice
  ([architecture](references/architecture.md#5-conventions)).

## Step 5: Auto-deploy

1. Push the project to its own GitHub repository.
2. Add the repository secret **TGCLOUD_TOKEN** (the same token as `login`).
3. From then on, every push to `main` that touches the bot or the front-end:
   1. builds;
   2. pushes;
   3. runs `migrate --safe` and `webhook sync`. Each of these is its own
      `always()` step; [architecture §9](references/architecture.md) explains
      why.

Without the secret, the workflow does nothing.

## Step 6: Admin tools, only on request

When the user asks for any of these, build it from
[references/admin-tools.md](references/admin-tools.md) (the project has a copy
in `docs/ADMIN-TOOLS.md`), with its tests, and tell them how to use it:

| The user asks for | What you add |
|---|---|
| "query the database", `npm run sql` | `endpoints/sql.js` (admin only), `scripts/sql.mjs`, the `sql` npm script. Then: `npm run sql -- "SELECT * FROM users LIMIT 5"` |
| `/stats`, `/backup`, other admin commands | `lib/admin.js` and an `adminCommand()` router in `handlers/message.js`, with failures reported to the admin |
| an admin panel in the Mini App | `adminStats`, `adminUsers`, … endpoints with `requireAdmin(ctx)` first |
| a daily / weekly job | an admin command plus `.github/workflows/scheduled.yml` |
| storing an API key | a `/setkey` admin command into the `settings` table |

Never add an admin tool the user didn't ask for.

## Existing projects

For a project with its own `tgcloud/schema.js`, the scaffold runs in
**existing-project mode** and leaves `tgcloud/` alone. It only adds:
- `.github/workflows/deploy.yml`;
- the test harness (`test/sdk/`, `test/helpers.mjs`);
- `docs/ARCHITECTURE.md`, `docs/ADMIN-TOOLS.md`, `docs/BOT-API.md` and the
  `AGENTS.md` section;
- the npm scripts that are missing (existing ones are kept);
- `.claude/settings.json`.

With `--mini-app`:
- The front-end goes in only if there's no `index.html`.
- The feedback endpoint goes in only if `tgcloud/lib` came from this kit
  (`lib/feedback.js`, `profileOf`).

After that:
1. Write `test/<feature>.test.mjs` for the project's existing handlers. The
   harness runs real production code unchanged.
2. Move logic toward the architecture one feature at a time.
3. Run `npm test` after each step.
