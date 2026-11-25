---
name: tgcloud-mini-app
description: Build, add or update a Telegram Mini App hosted on Telegram Serverless (tgcloud) — the front-end build served at app<id>.tgcloud.ai, its server side as tgcloud/endpoints/<name>.js (POST /api/<name>), calls via Telegram.WebApp.Serverless.call, the tgcloud.jsonc "static" config (source, spa, immutable, headers, redirects), and build + deploy. Use whenever the user wants to create, implement, change, debug or deploy a serverless Mini App, web app or endpoint for a tgcloud bot.
---

# tgcloud Mini App

A Mini App on Telegram Serverless is two halves deployed together by `npx tgcloud push`:

| Half | Lives in | Runs | Can use |
|---|---|---|---|
| Front-end | project root (Vite/React/Vue/…), build → `dist/` | the user's browser in Telegram | npm packages, `window.Telegram.WebApp` |
| Endpoints | `tgcloud/endpoints/<name>.js` | the platform's V8 isolate | `sdk` only: `db`, `api`, `fetch`, `EndpointError` |

The front-end never imports `tgcloud/` code. It talks to the server **only** through endpoints. Site URL: `https://app<app_id>.tgcloud.ai/` (`push` prints it). Endpoints answer `POST /api/<name>` on the same host.

Source: https://core.telegram.org/bots/serverless#mini-app-front-end. Re-check it with WebFetch if something here doesn't match the CLI's behavior.

Something small that should live **inside a message** (a counter, a poll, a
price, a code to copy) is a widget (Bot API 10.4), not a Mini App. Use the
`tgcloud-widgets` skill. A widget can open the Mini App with
`openTelegramLink('https://t.me/<bot>/<app>')`.

## Step 1: Inspect the project

- Is there a `tgcloud/` folder? If not, set up the bot first (the `tgcloud-bot` skill, or `npm create @tgcloud/bot .`). Read the project's `AGENTS.md`, since it holds the module rules.
- Is there a front-end? Look at `package.json`, `vite.config.*` and `index.html`. If there's none, create one at the **project root**, next to `tgcloud/`, keeping the existing files.
- Check `tgcloud.jsonc` → `"static"`.

**The front-end is always React (Vite + `@vitejs/plugin-react`).** Never write a vanilla-JS UI. Its look follows the design system the user chose (Step 1b, `docs/DESIGN.md`). The default is Telegram's own theme: `telegram-web-app.js` sets `--tg-theme-*` CSS variables (bg, text, hint, link, button, section…) from the user's theme and keeps them updated, so the app looks native in light, dark and custom themes. The starter's `src/app.css` maps them to a few app variables with fallbacks for the browser. Write endpoints with the `tgcloud-endpoints` skill.

**Fastest start:** the tgcloud-bot scaffold with `--mini-app` copies the starter in [assets/app/](assets/app/):
- `index.html` and `vite.config.js`;
- `src/main.jsx` (ready, expand, fullscreen, close confirmation);
- `src/App.jsx` (calls `me`, shows the user's own profile, and a feedback form that calls the `feedback` endpoint with loading and error states);
- `src/app.css` (the Telegram theme variables, safe areas, sections, rows, inputs, buttons);
- `src/lib/` (`serverless.js`, `useEndpoint.js`, `telegram.js` with theme following, haptics, native dialogs and `useBackButton`, `i18n.js` with every text in English and Persian, `format.js` with numbers and dates in the UI's language);
- `tgcloud/endpoints/feedback.js` (validated, throttled), with `test/miniapp.test.mjs`.

There is no admin panel in the starter. When the user asks for one, build it from the tgcloud-bot skill's `references/admin-tools.md` §3 (`requireAdmin` first in every admin endpoint).

With the bot already scaffolded:

`node "${CLAUDE_SKILL_DIR}/../tgcloud-bot/scripts/scaffold.mjs" . --admin <ADMIN_ID> --mini-app`

The scaffold adds only the missing files. Build new pages on that starter rather than from scratch.

## Step 1b: Design system

`docs/DESIGN.md` is the project's design choice. If it records a choice the user made, follow it for every UI change and don't ask again. If it is missing, or still says **"Chosen by the user: not yet"** (the scaffold's default), **ask which design system to use**, as a choice:

- **Default**: Telegram's own theme. Nothing to provide.
- **My own design system**: they type or link it. In Claude Code, AskUserQuestion with these two options; the free-text answer carries the details.

**Default.** Keep `src/app.css` as it is. New components use only its variables (`--bg`, `--section-bg`, `--text`, `--hint`, `--link`, `--button`, `--button-text`, `--destructive`, `--separator`, `--section-title`, `--radius`), never hard-coded colors. In `docs/DESIGN.md`, change "Chosen by the user: not yet" to "Chosen by the user: yes" (or write the file from the scaffold's version if it's missing).

**Their own.** Turn what they gave into tokens, then wire them in:
1. **Read the source.**
   - A website or brand guide: WebFetch it and take the colors, fonts, sizes, radii, shadows and spacing from its CSS.
   - Figma: use the Figma tools if they're connected; otherwise ask for exported tokens or screenshots.
   - A CSS or tokens file: copy it into `src/styles/`.
   - An installed design-system skill: load it and follow it.
   - A UI library: `npm i` it in the front-end only (never in `tgcloud/`) and follow its setup for Vite + React.
   - A description: turn it into a small palette and type scale, and show it to the user before building on it.
   Ask for whatever is missing (a dark-mode palette, the font's license) instead of guessing.
2. **One token file.** Put the tokens on `:root` in `src/styles/design.css`, plus a dark set under `:root[data-theme='dark']` (`useTelegramTheme` sets `data-theme` from `Telegram.WebApp.colorScheme`). Import it in `src/main.jsx` before `app.css`.
3. **Map the app variables** in `src/app.css` (`--bg`, `--text`, `--button`, …) to the new tokens, so the existing components switch over at once. Then restyle components in the new language: borders, shadows, radii, spacing.
4. **Fonts**: self-host them in `src/fonts/` (or load them from a CDN) with a system fallback. Persian UI needs a font with Persian glyphs.
5. **Keep the Mini App rules**: `dir="rtl"` / logical properties, the safe-area padding on `.app`, tap targets of at least 44px, readable contrast in both themes. Pass the design's background as a hex color to `setHeaderColor` / `setBackgroundColor` in `src/lib/telegram.js`.
6. **Don't copy someone else's brand** (logo, name, paid fonts) unless the user owns it or its license allows it.
7. **Save it**: rewrite `docs/DESIGN.md` with the source, the tokens, the fonts and the component rules, so later sessions and other agents keep using it.
8. **Check it**: build, then screenshot at 390px wide in light and dark (see Step 5).

## Step 2: Wire the front-end

0. React setup in an existing project: `npm i react react-dom` and `npm i -D vite @vitejs/plugin-react`. Then add `vite.config.js` with `plugins: [react()]`, `index.html` with `<div id="root">` and `<script type="module" src="/src/main.jsx">`, and the scripts `"dev": "vite"`, `"build": "vite build"`, `"deploy": "vite build && tgcloud push"`. Add `dist/` to `.gitignore`.
1. Add the Telegram script to `index.html` `<head>`, before the app bundle:
   `<script src="https://telegram.org/js/telegram-web-app.js"></script>`
2. Copy [assets/app/src/lib/serverless.js](assets/app/src/lib/serverless.js) to `src/lib/serverless.js` and [assets/app/src/lib/useEndpoint.js](assets/app/src/lib/useEndpoint.js) to `src/lib/useEndpoint.js`. The first turns `Serverless.call` into a promise (`await callEndpoint('getProfile', { lang: 'en' })`). The second is a React hook: `const { data, error, loading, reload } = useEndpoint('myOrders', { page, size })`. It refetches when the input changes and drops stale responses.
3. On startup: `Telegram.WebApp.ready(); Telegram.WebApp.expand();`. Use `Telegram.WebApp.themeParams` / CSS vars (`var(--tg-theme-bg-color)`) so the app matches the Telegram theme.
3a. Fullscreen and close confirmation (the starter's `src/main.jsx` does both):
   ```js
   if (tg?.isVersionAtLeast?.('8.0') && !tg.isFullscreen) tg.requestFullscreen();   // fails → 'fullscreenFailed' event { error: 'UNSUPPORTED' | 'ALREADY_FULLSCREEN' }
   if (tg?.isVersionAtLeast?.('6.2')) tg.enableClosingConfirmation();               // "are you sure?" on close
   ```
   In fullscreen, Telegram's buttons overlay the page. Pad the top and bottom with `var(--tg-safe-area-inset-top, 0px) + var(--tg-content-safe-area-inset-top, 0px)` (and `-bottom`). `telegram-web-app.js` sets these variables, and they update on the `safeAreaChanged` / `contentSafeAreaChanged` events. Call `setHeaderColor` so the status bar stays readable. Also available: `exitFullscreen()`, `isFullscreen`, the `fullscreenChanged` event, and `disableClosingConfirmation()`. Docs: https://core.telegram.org/bots/webapps
4. `initDataUnsafe` is for display only (name, photo). Anything that needs trust goes through an endpoint, which receives **verified** init data.
3b. **English by default, and bilingual.** Every text goes in `src/lib/i18n.js` (`TEXTS.en`, `TEXTS.fa`), read with `const { t, lang } = useI18n(me.data?.lang)`. The language is the one the user chose in the bot (`me.lang`), else the Telegram app's, else English. `useI18n` also sets `<html lang dir>`, so Persian is right-to-left. Write the CSS with logical properties (`padding-inline`, `margin-inline-start`, `text-align: start`) so both directions work. Numbers and dates go through `formatNumber(lang, n)` / `formatDate(lang, unix)`. Endpoint errors arrive already in the user's language.
4a. **Every screen except the first has a way back.** Call `useBackButton(goBack)` (in the starter's `src/lib/telegram.js`) on each such screen. It shows Telegram's native back button, which returns to the previous screen. The first screen calls `useBackButton(null)`. The same rule holds for the bot's own messages (the tgcloud-bot skill's `lib/menu.js`).
5. Keep the bundler's `base` at `/`. Never put files under `/api/` in the build output. Don't set `X-Frame-Options` or a restrictive `frame-ancestors`, because Telegram Web loads the app in an iframe.
6. **Same origin only** (Bot API 10.2, on for every Mini App since July 20, 2026): `Telegram.WebApp` methods work only from the Mini App's own origin, `https://app<app_id>.tgcloud.ai`. Keep every screen on that host. A page on another domain (an external checkout, a redirect, another site in an iframe) can't call them. Use exactly the URL that `push` printed (in `MINI_APP_URL`; the bot sets its menu button from it). BotFather can turn the protection off, but then the bot is responsible for the app linking to no untrusted site, so leave it on.

## Step 3: Configure static hosting (`tgcloud.jsonc`)

```jsonc
{
  "static": {
    "source": "dist",             // the build folder (Vite: dist). Next/Nuxt/SvelteKit/Angular: configure static export first
    "spa": true,                  // client-side routing: index.html for missing extension-less paths
    "immutable": ["/assets/*"],   // content-hashed files only → cached 1 year
    // "headers":   [{ "path": "/assets/*", "set": { "X-Foo": "bar" } }],   // exact path or prefix/*; null removes
    // "redirects": [{ "from": "/old", "to": "/new", "status": 301 }],       // first match wins; real files beat rules
  },
  "$schema": "./node_modules/@tgcloud/cli/schema/tgcloud.json"
}
```

`"static": "dist"` is shorthand for this. `"static": false` **deletes** the deployed site on the next push. Removing the key only stops managing it, and the deployed site stays. Use either `tgcloud.jsonc` or `tgcloud.json`, never both.

## Step 4: Write endpoints

Scaffold: `npx tgcloud add endpoints/<name>`. Names use letters, digits and `_`, don't start with a digit, and the folder is flat (no subfolders).

```js
// tgcloud/endpoints/getProfile.js
import { db, EndpointError } from 'sdk';
import { eq } from 'sdk/db';
import { profiles } from '../schema.js';

export default async function (input, ctx) {
  const user = ctx.initData.user;              // verified by the platform; there is no ctx.user
  const profile = await db.select().from(profiles).where(eq(profiles.userId, user.id)).get();
  if (!profile) throw new EndpointError('Profile not found', { code: 'NO_PROFILE' });
  return profile;                              // sent back as JSON
}
```

Rules:
- **Identify the caller only from `ctx.initData.user.id`.** Never trust a user id sent in `input`.
- Refusals use `throw new EndpointError(description, { code })` → HTTP 400, and the client gets `err.message` and `err.parameters.code`. Any other throw becomes a generic 500, and its message never reaches the client.
- Bad or missing init data → 401 before your code runs.
- Validate `input` (types, lengths). It's arbitrary JSON from the client.
- Admin-only endpoints (only when the user asks for them) call `requireAdmin(ctx)` from `lib/access.js` first.
- Anything that sends messages, writes or costs money is throttled per user: every Mini App user can call every endpoint, in a loop.
- Shared logic goes in `tgcloud/lib/`, imported with relative paths that end in `.js`. The bot's handlers and the endpoints can share it.
- Every DB call is `await`ed. Schema changes go in `tgcloud/schema.js` and then `npx tgcloud migrate`.

More recipes (sending a message from the app, upserting the user, pagination, errors in the UI): [references/recipes.md](references/recipes.md).

## Step 5: Test

- Endpoint logic, without deploying (`--ctx` isn't verified, so this tests your logic only):
  `npx tgcloud run endpoints/getProfile '{}' --ctx '{ initData: { user: { id: 1, first_name: "Ann" } } }'`
- Front-end layout: `npm run dev` in a browser works, but `Telegram.WebApp.Serverless` only works inside Telegram. The wrapper in `src/lib/serverless.js` rejects with `type: 'NOT_IN_TELEGRAM'` outside Telegram, and the starter shows a notice for it.
- Endpoints: `npm test` runs them offline on the mock SDK (see `test/miniapp.test.mjs`).
- Layout without Telegram: build, serve `dist/` with Playwright, and stub `window.Telegram.WebApp.Serverless.call` in an init script so it returns fixture data. Screenshot the result at 390px wide. For real calls, deploy and open the app in Telegram.

## Step 6: Build and deploy

`push` uploads the build folder **as it is on disk** and never builds. Always build first:

```
npm run deploy           # vite build → tgcloud push
npx tgcloud migrate      # when schema.js changed
```

`migrate --yes` applies every safe and warning schema change without asking. Changes that need manual handling are never applied automatically. Use `npx tgcloud migrate --dry-run` first if you aren't sure.

- `npx tgcloud push`: modules + static files (only changed files are uploaded).
- `npx tgcloud push dist/`: static files only. `npx tgcloud push tgcloud/endpoints/x.js`: that module only (leaves the site untouched).
- The kit's `.github/workflows/deploy.yml` already runs `npm run build --if-present` before `push`, and its `paths:` filter covers `src/`, `index.html` and `vite.config.*`.

## Step 7: Open it in Telegram

Copy the URL that `push` printed (`https://app<app_id>.tgcloud.ai/`) into `MINI_APP_URL` in `tgcloud/lib/config.js` and deploy again. **The bot sets up the rest itself**, with nothing to set in BotFather. On the next `/start`, `syncBotSetup()` / `syncMenuButton()` in `lib/menu.js` put the Mini App button next to the input field (`setChatMenuButton`), labelled in each user's language. The menu's «📱 Open the app» button uses the same URL. The Mini App files are also visible under **Serverless** in BotFather. Other inline or keyboard buttons can open it too: `{ text: t(lang, 'open_app'), web_app: { url } }`.

## Limits

Upload 50 MB per file (10 MB photo). `api.getFileContent`/`getFileStream` 20 MB. `fetch` response 30 MB. A batch insert is one statement, limited by SQLite's variable count (rows × columns). No foreign keys.
