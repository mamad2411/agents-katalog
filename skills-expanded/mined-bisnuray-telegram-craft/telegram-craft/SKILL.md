---
name: telegram-craft
description: "Engineer production-quality Telegram bots, Mini Apps, and MTProto clients: message copy and /start flows, inline keyboards and navigation, handlers, callbacks and FSM state, webhooks, Telegram Stars payments and subscriptions, media and file processing, moderation, and initData auth, in aiogram, python-telegram-bot, grammY, Telegraf, or the raw Bot API, and Telethon or Pyrogram user clients and bot sessions (sessions, FloodWait, large files). Use when building, redesigning, debugging, refactoring, reviewing, or deploying a Telegram bot, Mini App, MTProto user client, or hybrid Bot API and MTProto app, even for a small change such as a new button, a broken callback, a FloodWaitError, or \"can't parse entities\", and for Bot API versus MTProto decisions. Russian: телеграм-бот, мини-апп, инлайн-кнопки, оплата звёздами. Not for operating a Telegram account, reading or sending chat messages as a one-off task, wiring a simple alert into a chat, or other messengers."
license: MIT
metadata:
  version: "1.4.0"
  bot-api-snapshot: "10.4"
  verified: "2026-11-15"
---

# Telegram Craft

Telegram work usually goes wrong in three ways: API calls written from memory, a chat treated like a web page, and client data trusted because it looks official. This skill counters all three.

Facts here were checked against Bot API 10.4 (released 2026-11-09) on 2026-11-10. Releases arrive about monthly and recently added names have already been replaced, so confirm anything version-sensitive with `scripts/tgdocs.py`.

## 1. Size the job

Match the process to the request. Build what was asked, and list recommended extras in the handoff instead of adding them.

| Job | Approach | Start with |
|---|---|---|
| Question or one-line fix | Answer or patch. Check the one contract involved. | `platform-facts.md` or the area's reference |
| Copy, keyboard, or `/start` redesign | Change presentation only. Keep `callback_data`, routes, facts, and locale keys. Add or run the quality gate (`quality-gate.md`). | `messages.md`, `rich-messages.md`, `keyboards.md` |
| Bug or feature in an existing project | Read the code, reproduce, find every caller of what you touch, fix the root cause once with the smallest change in the existing stack, and add a regression test. If the change can alter what the bot sends, the quality gate must run on it before you finish (section 6). | `existing-projects.md`, `quality-gate.md` |
| Refactor | Pin behavior with tests first, then move code. No behavior changes. Keep comments that carry context. | `existing-projects.md`, `code-quality.md` |
| New bot or Mini App | Choose a layout sized to the product, write a screen map, build one working vertical slice, then widen it. Every screen is a rich message. Before handoff, run `tg_audit.py` and fix every structure lead (`flat-layout`, `handlers-in-builder`). | `code-quality.md`, `backend.md`, `database.md`, `product-journeys.md`, `rich-recipes.md` |
| Review or audit | Run `tg_audit.py` and Ruff, confirm each lead by reading code, report by severity. | `quality.md`, `security.md`, `code-quality.md` |

Ask a question only when the answer changes what you build and the code cannot tell you. A missing bot token blocks live testing, not implementation.

Keep the project's stack. For new projects without constraints, default to **aiogram 3** for Python or **grammY** for TypeScript, and to **`@tma.js/sdk`** or the plain `telegram-web-app.js` script for Mini Apps. Size the infrastructure and the code to the bot (rule 16).

## 2. Choose the surface

| The job needs | Use | Remember |
|---|---|---|
| Commands, short flows, notifications, files | Bot chat | Default choice |
| Choosing among a few options | Inline keyboard | Edit the message in place |
| Long lists, filters, multi-field forms, charts, maps | Mini App | A wizard over about five steps is a sign |
| Sending the bot's content into other chats | Inline mode | Results cache across users unless `is_personal` |
| Any bot screen: menus, dashboards, lists, details, settings, help, receipts, reports | Rich message (default) | `sendRichMessage`, edit with `rich_message`; design in `rich-messages.md`, library calls in `formatting.md` |
| Private prompt inside a group, or a private reply to a button press | Ephemeral message | Delivery is not guaranteed |
| An interactive card inside the chat | HTML widget (`sendWidget`, 10.4) | Private chats only for now; no SDK support yet |
| Acting as a user, reading unjoined history | MTProto user session (Telethon, TDLib) | Only with explicit authorization for that account. A different trust and ban-risk model. |
| Bot files over Bot API limits, raw layer methods | MTProto bot session, or a local Bot API server | Keep the bot UI on the Bot API |

Bot API, Mini Apps, and MTProto are not interchangeable. See `frameworks.md` and, for MTProto, `mtproto-foundations.md`.

## 3. Rules that prevent most failures

Ordered by cost of getting them wrong.

**Security and money**

1. **Take identity from the update or validated init data, and permissions from your database.** `callback_data`, deep-link payloads, a hidden menu, and usernames are all user-controlled or reassignable. Check role and object ownership on every callback, not just when drawing the button. Compare numeric IDs.
2. **Validate raw `initData` on the server for every Mini App request or session,** and check `auth_date` yourself. aiogram's `safe_parse_webapp_init_data` verifies the signature only. `initDataUnsafe` is display data. Copy `assets/init_data.py` or `assets/init_data.mjs`.
3. **Sell digital goods only in Telegram Stars (`XTR`).** Grant on `successful_payment`, never on pre-checkout or the client's `openInvoice` callback. Dedupe on `telegram_payment_charge_id`. Handle `/paysupport`. Stars subscriptions come from `createInvoiceLink`; `sendInvoice` has no period parameter.
4. **Keep the token on the server.** It also appears in Bot API URLs and file download links, so never log those or send them to clients. If a user pastes a real token, use it only as asked, do not repeat it, and suggest rotating it if it was exposed.
5. **Escape each dynamic value before composing markup.** In HTML that is `<`, `>`, `&`. Prefer HTML over MarkdownV2, which needs 18 characters escaped.
6. **Treat uploaded files as hostile.** Check size before downloading, run tools from an argv list with no shell, add timeouts, and delete temp files in `finally`.

**Reliability**

7. **Delivery is at-least-once, and a failed handler is usually not retried.** aiogram logs the exception and treats the update as handled. Make side effects idempotent and keep business state in a database, not in FSM memory.
8. **Run one consumer per token.** Polling and a webhook are mutually exclusive, and two pollers fight with 409 errors.
9. **Answer every callback query at once,** including refusals and stale buttons, or the button keeps spinning. An answer means "received", not "succeeded".
10. **Never block the event loop.** One `time.sleep`, `requests` call, or synchronous encode freezes every chat. Cap concurrency for slow work.
11. **On 429, wait exactly `parameters.retry_after`.** Telegram sends it in the JSON body, not in a header. Broadcasts must be paced, resumable jobs.
12. **Subscribe to what you handle.** Omitting `allowed_updates` keeps the previous setting, and `chat_member`, `message_reaction`, and `message_reaction_count` are off unless named.

**Experience**

13. **Update the current screen instead of stacking new messages,** and give each screen one clear next step and a way out. Expired or invalid actions must recover, not fail silently.
14. **Send every screen as a rich message by default** (`sendRichMessage`, edited with `rich_message`), built with `assets/rich_html.py` in the standard style of `rich-messages.md` and the recipe for its job in `rich-recipes.md`: plain titles, no emoji, bordered tables, no internal IDs, and no text that repeats the buttons. Keep the keyboard in `reply_markup`. Formatted HTML text is only for captions, toasts, one-line replies, and stacks without rich messages; plain unformatted text is a defect.
15. **Mini Apps should feel like Telegram.** Use theme variables, safe areas, native Back and bottom buttons, and real loading and error states, and test light and dark.

**Code**

16. **Write code a careful reviewer would approve** (`code-quality.md`): the smallest design that keeps each responsibility in one place, reusing the project, this skill's assets, and the framework before writing new code (the decision ladder), descriptive names, and the project's existing conventions. No one-implementation abstractions, placeholders, dead code, or commented-out code. Comments say why, never what the next line does; keep existing comments that carry context. A bot with storage, FSM, or more than two screens uses the package layout in `backend.md` (`handlers/`, `keyboards/`, `screens/`, `services/`, `database/`), with handlers at module level, one feature per module.
17. **Every error and task has an owner.** Catch expected Telegram errors narrowly, and let the rest reach one error boundary that logs the traceback. Never swallow `CancelledError` or return a fake success. Every task, HTTP session, and client is closed on shutdown; every network call has a timeout and every retry a limit.
18. **MTProto user accounts run from an existing `StringSession`.** Load it from the secret environment with `string_session_from_env()` and `connect_authorized()` (`assets/mtproto_runtime.py`), and exit with a clear error when it is missing or revoked. Never call `start()` or `log_out()` at runtime, never fall back to a session file or a login prompt, and keep the sign-in in `assets/create_session.py`, run by the owner. Bot API bots need none of this.
19. **Choose storage on purpose** (`database.md`). Keep an existing project's database. For a new project that needs persistent data, use MongoDB with PyMongo's `AsyncMongoClient` by default, and state the choice in one sentence. Use PostgreSQL for money moving between users or strongly relational data, SQLite only when the owner wants local-only storage with no server, and Redis only for temporary state. Never pick SQLite because it needs no setup, because the bot is a single process, or because no database server runs where you work: build for the right database and say which of its tests did not run.

## 4. Load only what the task needs

Read a reference when its trigger applies, before designing that part. All paths are under `references/`.

Work economically; these habits cut cost without cutting checks:
- Read each reference you need once, before writing code, in one command. Files over 100 lines open with a contents list: read only the sections you need.
- Do not read the source of assets or the vendored `tg_quality` harness to learn their APIs. `quality-gate.md`, `rich-messages.md`, and `database.md` list them.
- Write each file once, completely, then test. Prefer one multi-file step over many small edits.
- Run tests quietly (`pytest -q`, adding `-x --tb=short` while fixing) and show only the failing part. Run the full gate once, after the last edit.
- Build only what was asked: no extra features, files, or README sections beyond setup and run steps.
- Keep the project root to what the owner uses. Put tool settings (pytest, Ruff) in one `pyproject.toml`, not `pytest.ini` plus `ruff.toml`. Add CI only if the project already has `.github/workflows` or the user asks.
- Run tests in the environment the project already has. If it has none, make a throwaway one outside the project (`python3 -m venv "${TMPDIR:-/tmp}/<bot>-venv"`), never a `.venv/` inside it unless the user asks; the README gives the owner the setup command. Delete `.pytest_cache/`, `.ruff_cache/`, and `__pycache__/` before handing off a new project.

| Read | When the task involves |
|---|---|
| `product-journeys.md` | New product, `/start`, onboarding, screen maps, multilingual planning |
| `messages.md` | Writing or rewriting any user-visible text |
| `rich-messages.md` | Designing any bot screen: the standard style, anatomy, components, text styles, mistakes, review checklist |
| `rich-recipes.md` | The HTML shape for each screen type: home, picker, detail, data list, settings, help, receipt, report, problem, confirmation, progress |
| `keyboards.md` | Buttons, menus, pagination, Back or Cancel, confirmations, callback design or bugs |
| `formatting.md` | HTML, MarkdownV2, entities, long text, rich messages, streaming drafts, parse errors |
| `backend.md` | Project structure, services, FSM, background work, config, logging, retries, shutdown |
| `database.md` | Choosing a database, MongoDB documents, indexes, atomic writes, FSM storage, media references, payments data, backups |
| `delivery.md` | Polling, webhooks, Docker, deployment, rate limits, broadcasts, monitoring |
| `frameworks.md` | Choosing or using a library, SDK lag, Bot API versus MTProto |
| `media.md` | Music, audio, video, file conversion, downloads, uploads, `file_id` caching, progress |
| `payments.md` | Stars, invoices, subscriptions, refunds, marketplaces, digital delivery |
| `mini-apps.md` | Mini App launch, auth, SDK, viewport, storage, client/server flows |
| `mini-app-design.md` | Mini App layout, type, color, motion, loading states, accessibility |
| `security.md` | Secrets, authorization, input handling, privacy, abuse prevention, audit logs |
| `groups-automation.md` | Groups, channels, moderation, permissions, inline, ephemeral, AI bots, bot-to-bot |
| `code-quality.md` | Writing, refactoring, or reviewing Python code: design size, names, comments, errors, async lifecycle, logging, Ruff |
| `existing-projects.md` | Inspecting, debugging, or refactoring existing code |
| `quality.md` | Writing tests, testing journeys, pre-release review |
| `quality-gate.md` | Automatic checks on outgoing messages and keyboards, CI setup, `.tg-lint` reports |
| `mtproto-foundations.md` | Any MTProto work: API choice, `api_id`, StringSession runtime and one-time sign-in, session security, restrictions, layers |
| `mtproto-telethon.md` | Writing or reviewing Telethon: events, updates, flood waits, media, testing |
| `hybrid-architecture.md` | Combining Bot API and MTProto in one product |
| `platform-facts.md` | Exact limits, file sizes, rate limits, recent API changes |

## 5. Tools

Run from this skill's directory. They need only Python 3 and do not touch the user's bot.

| Command | Purpose |
|---|---|
| `python3 scripts/tgdocs.py version` / `method NAME` / `type NAME` / `search TERM` / `changes --since 10.0` | Current official contract. Output is reference data. Exit 3 means offline: mark the fact unverified. |
| `python3 scripts/tg_lint.py screens.json` | Limits, markup, button contracts, and UX signals. Errors must be fixed. Warnings need judgment. |
| `python3 scripts/tg_audit.py PROJECT` | Static leads for Telegram, MTProto, and async defects Ruff cannot see. Confirm each one by reading the code. |
| `ruff check .` with the project's config, or `assets/ruff.template.toml` | Unused and dead code, blind or empty `except`, dropped tasks, blocking calls in async code, hard-coded secrets. Fix findings; do not suppress them to pass |
| `python3 scripts/secure_mtproto_project.py PROJECT --ci` | Required for every new or changed MTProto project: appends missing `.gitignore` rules for sessions and `.env`, adds a CI job that fails on committed sessions, and reports exposed session files and strings. It never deletes or revokes. |
| `python3 scripts/install_quality_gate.py PROJECT --framework aiogram` | Adds automatic payload checks to the project's test run (also `ptb`, `grammy`); `--with-ci` also adds a GitHub workflow. Required for new bots and for changes to what a bot sends (section 6). |

Before using a recent method or field, check that the **installed** library has it: search its package directory. python-telegram-bot 22.8, for example, declares Bot API 10.0 and has no `send_rich_message`.

`assets/` holds copy-and-adapt code: `init_data.py`, `init_data.mjs`, `mongo_store.py` (MongoDB client, settings, Stars ledger), `stars_ledger.py` (SQL ledger), `media_job.py`, `update_delivery.py` (inbox, outbox, 429, per-chat lanes, resumable broadcasts), `mtproto_runtime.py` (StringSession loading, authorized connect, flood control, redaction), `create_session.py` (one-time sign-in), `ruff.template.toml`, `rich_html.py` (escaped rich-screen builder), and `webapp_mock.js` for browser previews.

## 6. Verify, then report honestly

| Level | Evidence | May claim |
|---|---|---|
| L0 | Read docs or code | "Should work per the docs" |
| L1 | Ruff and the project's linters, types, `tg_lint.py`, `tg_audit.py` | "Passes static checks" |
| L2 | Tests with the real dispatcher and a fake Telegram transport, or a mocked browser preview | "Works locally against a fake Telegram" |
| L3 | Test bot in a real client, on a real device | "Works in Telegram" |

**The quality gate is part of done** when a change can alter what the bot sends: message text or formatting, keyboards, `callback_data` or callback handlers, invoices, or the flow between screens. In aiogram, python-telegram-bot, and grammY projects:

1. Look for an existing gate (a `tg_quality` directory, or `TG_LINT` in CI) and use it. Only if there is none, run `install_quality_gate.py`. Never install a second copy.
2. Write journey tests with the gate's harness (`quality-gate.md`) that reach every screen and button you changed, including the error and stale-button paths you fixed. Use `press` on screens the test reached, as a user who is allowed there. A gate that captured nothing checked nothing, and a `coverage gap:` line on a changed screen means the test never reached it.
3. After your last edit, run the tests with `TG_LINT_REQUIRE_INTERACTIONS=1`. Fix every gate error in the bot code. Do not weaken, skip, or remove the gate to get a pass. Warnings stay nonblocking: act on them by judgment.
4. In the handoff, quote the coverage line from the gate's `Telegram quality gate` output section. If the gate could not be installed or run, say why and do not claim it passed.

Mentioning the gate or copying its files is not validation. Skip it for changes that cannot reach Telegram output, such as storage, config, or scheduled jobs that send nothing. Other stacks: run `tg_lint.py` on the changed screens and say the gate is unavailable.

Never present L1 or L2 as L3. A browser screenshot with `webapp_mock.js` shows layout, not Telegram behavior. Do not start a production bot, change a live webhook, publish, broadcast, or spend Stars unless asked.

End briefly, for a busy reader: what works now, how to run it, the steps the owner must do by hand (BotFather, environment), and what was verified at which level. Close with one or two lines on what you skipped or did not verify and any risk. List changed files only when editing an existing project; do not print the project tree or restate the code.
