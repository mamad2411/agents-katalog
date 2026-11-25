---
name: mota-dapp-stack
description: |
  How to work with the ĐApp Starter (dapp-starter), addon CLI, and mota-dapp (SvelteKit) project structure.
  Use this skill whenever the user is working on or asking about SvelteKit routes, addons, npx addon,
  dapp-starter, start.mjs, vite.config.ts modules, i18n in src/i18n, env variables ($env/static/private,
  $env/dynamic/private, import.meta.env), default packages, addon script execution order, or the mota-dapp
  folder layout. Also use it for route conventions ([param], [[optional]], (group)), _config/_lang/_scripts
  in addons, CONTRIBUTING/Code of Conduct, and template updates.
compatibility: []
---

# MOTA ĐApp Stack – SvelteKit, ĐApp Starter, Addons

This skill describes the **ĐApp Starter** installer, default packages, the **addon** CLI and its exact execution flow, the **mota-dapp** (sveltekit-mota) project structure, SvelteKit routing and env rules, Vite config, and project governance (CONTRIBUTING, Code of Conduct). Use it when editing or scaffolding SvelteKit apps created with this stack.

---

## ĐApp Starter (dapp-starter)

- **One-shot installer:** `npx github:bchainhub/dapp-starter` (or clone repo, `npm install`, `node start.mjs`).
- **Template:** Default template is **mota-dapp** (repo name; local project may be `sveltekit-mota`). Override with `--template URL` or `-t URL`. Pin version: append `@version` to URL (e.g. `...mota-dapp.git@1.2.3`) or use `--template-version REF` / `--tv REF`.
- **Update from template:** From project root run `node /path/to/dapp-starter/start.mjs --update` (or `-u`). Template is copied over **except `vite.config.ts`**, which is always preserved. Script may offer a git checkpoint commit before overwriting.
- **What it sets up:** Runs `sv create`, installs base + addon tooling deps, writes `bin/addon.mjs`, maps `addon` in `package.json`, composes project README, and optionally translations, skills, template merge, license, first commit. Requirements: Node.js 18+, git, one of npm/pnpm/yarn/bun.

---

## Default packages (installer)

**Base dependencies** (added by `start.mjs` after `sv create`):

- `@blockchainhub/blo`, `@blockchainhub/ican`, `@tailwindcss/vite`, `tailwindcss`
- `blockchain-wallet-validator`, `device-sherlock`, `exchange-rounding`
- `lucide-svelte`, `payto-rl`, `txms.js`, `vite-plugin-pwa`, `zod`

**Addon tooling** (dev):

- `hygen`, `tiged`, `json5`, `ejs`, `prompts`

**Optional (if user opts in):**

- **Translations:** `typesafe-i18n`; scripts `i18n:extract`, `i18n:watch`, `typesafe-i18n`
- **Skills:** [skills.sh](https://skills.sh/) (e.g. MOTA Skills, custom repo)
- **Other:** `.editorconfig`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, issue templates, license

---

## Addon CLI

After installation, projects run:

```bash
npx addon <repo> <generator> <action> [options]
```

Examples:

```bash
npx addon bchainhub@mota-support auth install
npx addon owner/repo auth uninstall
npx addon owner/repo auth install -c
npx addon owner/repo auth install -d
npx addon owner/repo#v1.2.3 auth install
```

- **Versioning:** Pin with `#<ref>` (tiged): e.g. `owner/repo#v1.2.3`, `owner/repo#main`, `owner/repo#<commit-hash>`. Do **not** use `@1.2.3` (that's npm; addon uses `#`).
- **Options:** `-c`/`--cache`, `-d`/`--dry-run`, `-nt`/`--no-translations`, `-ns`/`--no-scripts`, `-nc`/`--no-config`.

---

## How the addon script works (exact order)

The addon script (`bin/addon.mjs`) runs in this order:

1. **Parse argv** – repo, generator, action, and flags (`-c`, `-d`, `-nt`, `-ns`, `-nc`). Cache dir: `.addon-cache/<repo_sanitized>`; else temp dir.
2. **fetchAddon()** – Clone the addon repo with **tiged** (mode `git`) into cache or temp. If `-c` and cache exists, skip clone.
3. **resolveActionDir()** – Path is `tmpDir/generator/action`. If that folder doesn't exist, exit with "Addon action not found".
4. **loadPrompts(actionDir)** – If `prompt.js` exists, load it (array or function). If function: call with `{ prompts, cwd, generator, action, repo }`. Result is `locals` for the rest of the run.
5. **runHygen(locals)** – Run Hygen with `locals`; only **\*.ejs.t** templates generate project files. Hidden files are not Hygen targets.
6. **runHiddenScript(actionDir, locals)** – Skip if `-ns`. For each dir in `[actionDir, actionDir/_scripts]` (if `_scripts` exists), look for `_scripts.ejs.sh` or `_scripts.sh`. First found: render EJS if needed, write to temp script, run with env `ADDON_REPO`, `ADDON_GENERATOR`, `ADDON_ACTION`, `ADDON_CONTEXT_JSON`, `ADDON_VAR_<name>`.
7. **applyHiddenConfig(actionDir, locals)** – Skip if `-nc`. For each dir in `[actionDir, actionDir/_config]`, look for `_config.ejs.json5` or `_config.json5`. First found: render EJS if needed, parse JSON5, apply `$remove` then deep-merge into the **modules** block in `vite.config.ts` (finds block via regex), write back. Config is **client-side** — no secrets.
8. **applyHiddenLang(actionDir, locals)** – Skip if `-nt`. Collect all _lang entries from `[actionDir, actionDir/_lang]`: in action root files named `_lang.<code>.json5` (or `.ejs.json5`); in `_lang/` folder files named `<code>.json5` (or with path suffix). For each: read, EJS if needed, parse JSON5, resolve `$path` (default `modules.<generator>`), apply `$remove`, deep-merge into `src/i18n/<lang>/index.ts` (parse TS object, merge, serialize back). Only normal `.ejs.t` and these merges write to the project; prompt.js, _scripts, _config are never copied.
9. **runTypesafeI18n()** – If any _lang file was applied (and not `-d`), run `npx typesafe-i18n --no-watch` in project cwd so i18n types update.
10. **Cleanup** – If not using cache, delete the temp clone.

Dry-run (`-d`): no script execution, no config write, no lang write; only Hygen and prompts run, and addon logs what it would do.

---

## Addon structure and file roles

Addon repo layout: `<repo>/<generator>/<action>/`. Hidden files can live in the **action root** or in **optional subfolders** `_scripts/`, `_config/`, `_lang/`.

```text
<generator>/<action>/
  prompt.js
  *.ejs.t
  _scripts.ejs.sh    or  _scripts/_scripts.ejs.sh
  _scripts.sh            _scripts/_scripts.sh
  _config.ejs.json5  or  _config/_config.ejs.json5
  _config.json5          _config/_config.json5
  _lang.sk.json5     or  _lang/sk.json5, _lang/en.ejs.json5, ...
  _lang.en.json5         _lang/en.json5
```

- **prompt.js** – Optional. Collects answers once; same values reused by Hygen, _scripts, _config. Export **array** of prompt definitions or **function** returning answers.

  **Example (array):**
  ```js
  export default [
    { type: 'text', name: 'provider', message: 'Auth provider' },
    { type: 'text', name: 'route', message: 'Route name', initial: 'auth' }
  ];
  ```
  **Example (function):**
  ```js
  export default async ({ prompts, cwd, generator, action, repo }) => {
    const answers = await prompts([{ type: 'text', name: 'provider', message: 'Auth provider' }]);
    return answers;
  };
  ```

- **\*.ejs.t** – Normal Hygen templates; **only these** generate project files. Example:
  ```text
  ---
  to: src/routes/auth/+page.svelte
  ---
  <h1>Hello</h1>
  ```

- **_scripts** – Executed after Hygen; never copied. EJS example:
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  npm install <%= packageName %>
  echo "Route: <%= routeName %>"
  ```
  Env vars: `ADDON_CONTEXT_JSON`, `ADDON_REPO`, `ADDON_GENERATOR`, `ADDON_ACTION`, `ADDON_VAR_<NAME>`.

- **_config** – Merged into `modules` in `vite.config.ts`. **Client-only; no secrets.** Example with `$remove` and `$expr`:
  ```json5
  {
    "auth": { "enabled": true, "provider": "github" },
    "$remove": { "legacyAuth": true }
  }
  ```
  Raw TS expression: `"strategy": "$expr(resolveAuthStrategy())"` → written as TypeScript, not a string.

- **_lang** – Merged into `src/i18n/<lang>/index.ts`. `$path` (default `modules.<generator>`), `$remove` (array, string, or object). Example:
  ```json5
  { "$path": "modules.myAddon", "title": "Názov", "actions": { "submit": "Odoslať" } }
  ```
  With EJS: `"welcome": "Welcome to <%= featureName %>"`. Removing keys: `"$remove": ["oldTitle"]` or `"$remove": { "oldTitle": true, "nested": { "key": true } }`.

- **_migrations** – If present, copied into project; in `.gitignore` by default. Configure ORM (e.g. Drizzle `out: "./_migrations"`).

**These are never copied into the project:** `prompt.js`, `_scripts*`, `_config*`, `_lang*` files (only their **effects** — script run, config merge, lang merge — are applied).

---

## mota-dapp (sveltekit-mota) project structure

Template repo: **mota-dapp**; local app often **sveltekit-mota**. Typical layout:

```text
src/
  app.html
  app.d.ts           # Config, NavbarItem, LayoutData, $env/dynamic/private
  routes/
    +layout.svelte
    +error.svelte
    [[lang]]/        # Optional lang segment
      +layout.svelte
      +layout.server.ts
      +layout.ts
      +page.svelte
    api/[version]/   # e.g. /api/v1/ping
  lib/helpers/, lib/components/, lib/modules/, lib/server/
  i18n/en/, i18n/sk/, i18n-util.ts, i18n-svelte.ts, formatters.ts
static/
vite.config.ts
svelte.config.js
```

Site config is built in `vite.config.ts` and injected as `__SITE_CONFIG__`; types in `app.d.ts`; access via e.g. `getSiteConfig()` from `$lib/helpers/siteConfig`. Never put secrets in that config.

---

## Helpers (`$lib/helpers`)

Reusable utilities live in `src/lib/helpers/`. Import from `$lib/helpers/<name>` (e.g. `import { getSiteConfig } from '$lib/helpers/siteConfig'`).

| Helper | Purpose |
|--------|--------|
| **siteConfig** | Client-safe site config from `__SITE_CONFIG__`. `getSiteConfig()` returns cached `Config`; `isApiVersionEnabled(version, api?)` checks `api.activeVersions` (string or string[]). |
| **modules** | Module enablement from site config. `getPrimaryAuthModuleName()` → e.g. `auth.passkey`; `isModuleEnabled(module)` (e.g. `auth.passkey`, `banking`); `getModuleRoute(module)` → `$modules/auth/passkey`; `loadModule(module)` → dynamic import when enabled (client-safe). |
| **modules.server** | Server-only: `loadAuthModuleServer(module)` loads `$modules/auth/**/server.ts` (e.g. for `authHandle` in hooks); use in `hooks.server.ts` so private env never hits client. |
| **keys** | Clipboard and download: `copyToClipboard(text, successMsg, errorMsg)` (toast on success/fail); `downloadTextFile(content, filename, mimeType)`; `downloadGPGKey(keyContent, keyName)` → `.asc` file. |
| **i18n** | Locale and translations: `detectLocale(navigatorLanguage, availableLocales)`; `getAvailableLocales()` / `getAvailableLocalesWithNames()` from config; `getLocale()`; `applyLocale(locale)` (load + set + persist); `loadLocaleAsync(locale)` (preload); `createI18nLayoutLoad()` for layout; `t(key, LL, vars?)` resolve dotted key on `$LL` with optional vars; `deepMergeDict(base, overlay)` for locale overlays. |
| **nav** | Navbar/footer visibility: `ItemWithShow` has optional `show` rule string. `shouldShowItem(item, context)`; `filterNavItemsByShow(items, context)`; `filterNavItemsByAuth(items, context, authEnabled)`. Context: `{ loggedIn, connected, authIn }`. |
| **showRule** | Evaluate show rules: `evaluateShowRule(show, context)`. Terms: `always`, `hide`, `loggedIn`, `loggedOut`, `signedOut`, `connected`, `disconnected`, `authIn`, `authOut`. Combine with `and` / `or` and `()`. |
| **shortFormat** | Shorten identity strings for UI: `shortFormat(value, kind)` with `kind`: `'core'` (Core ID, 4+⋯+4 upper), `'wallet'` (0x…), `'user'` (user id). |
| **storageKeys** | localStorage keys: `STORAGE_KEY_LOCALE`, `STORAGE_KEY_THEME`; `getStoredLocale` / `setStoredLocale`, `getStoredTheme` / `setStoredTheme` / `removeStoredTheme` (with legacy migration). |
| **redirect** | Post-auth redirect: `getRedirectTo(configFallback?, queryName?, options?)` — reads `?redirect=` (or custom param), validates same-origin path, strips `//`; optional `keepOtherQueryParams`. |
| **dev** | `isDev` — true when SvelteKit `dev` or `import.meta.env.DEV` is truthy (e.g. Cloudflare Preview with `DEV_MODE=1`). |
| **geo** | **Server-only.** `getGeoData(event)` — sets `event.locals.country` / `event.locals.city` from Cloudflare `platform.cf`, Vercel/Netlify headers; respects `CAPTURE_COUNTRY` / `CAPTURE_CITY` in private env. |
| **icon** | `asDynamicIcon(icon)` — cast for dynamic icon component (e.g. when icon comes from config). |
| **ipfs** | `getIpfsUrl(url, ns?)` — convert `ipfs://<cid>` to gateway URL (e.g. `https://ipf.sk/<cid>` or `https://ipf.sk/<ns>/<cid>`). |
| **coreIdValidation** | `validateCoreId(id, updateField, messages?)` — validate Core ID via blockchain-wallet-validator (network xcb); returns `{ isValid, isEnterprise, description, error, field }`; enterprise addresses rejected for payments. |
| **urlValidation** | `validateSecureUrl(url)` — HTTPS + valid domain; skips in development. |
| **globalPolyfill** | Sets `window.global = window` when `global` is undefined (browser). Side-effect import. |
| **navigation** | `goUpOneLevel(currentPath)` — navigate to parent path (e.g. `/exchange-rates/usd` → `/exchange-rates`), preserves query params; uses SvelteKit `goto`. |
| **euclideanDistance** | `hexToRgb(hex)`; `calculateColorDistance(color1, color2)` — RGB Euclidean distance for HEX colors. |
| **blo** | `getIcon(address)` — returns identicon URL from `@blockchainhub/blo` for a wallet/address. |

**How to use (typical):**

- **Config / modules:** Call `getSiteConfig()` in components or load functions; use `isModuleEnabled('auth.passkey')` before loading auth UI; in `hooks.server.ts` use `loadAuthModuleServer(getPrimaryAuthModuleName())` for the auth handle.
- **i18n:** In `[[lang]]/+layout.ts` use `loadLocaleAsync(data.locale)`; in layout load return `{ locale }`; use `$LL` and `t('key', $LL, { var: value })` when you need manual key resolution.
- **Nav:** Get items from config, then `filterNavItemsByAuth(items, showRuleContext, authEnabled)` and render; each item can have `show: "loggedIn and connected"` etc.
- **Redirect:** After login/connect call `getRedirectTo(configRedirect)` and `goto(url)` or redirect response.
- **Storage:** Use `getStoredLocale()` / `setStoredLocale()` for language; `getStoredTheme()` / `setStoredTheme()` for theme.
- **Geo:** In `hooks.server.ts` handle, call `getGeoData(event)` so `event.locals.country` / `city` are set for server load/layout.

---

## SvelteKit routing

- **`[param]`** – Required dynamic segment (e.g. `[version]` → `/api/v1`).
- **`[[param]]`** – Optional dynamic segment (e.g. `[[lang]]` → `/` or `/en`).
- **`(group)`** – Layout group; does **not** add to URL (e.g. `(auth)/login` → path `/login`).

Files: `+page.svelte`, `+page.server.ts`, `+layout.svelte`, `+layout.server.ts`, `+layout.ts`, `+server.ts`, `+error.svelte`. Params in load/server as `event.params`.

---

## Environment variables

- **Server-only (secrets):** `import { X } from '$env/static/private'` or `$env/dynamic/private`. Declare in `app.d.ts`; never in client or in `define`.
- **Client/build:** `import.meta.env`, `VITE_*` only. Addon _config and `__SITE_CONFIG__` are client-visible — no secrets.

---

## Vite config (mota-dapp)

Plugins: `sveltekit()`, Tailwind, optional VitePWA. Client config object → `define: { __SITE_CONFIG__: JSON.stringify(siteConfigClient) }`. `modules` is the object addons merge into (via _config). Types in `app.d.ts`.

---

**Core principles (non-negotiable):**

- SvelteKit-first. No custom servers or other web frameworks.
- File-based routing under `src/routes` only.
- TypeScript everywhere. Avoid `any` unless justified.
- Simplicity and local reasoning over abstraction.
- Security fixes always override convenience; vulnerable solutions must be replaced.
- Create separate helper functions in `$lib/helpers` instead of adding them to the main file.

**Dependency updates:** Use `ncu -i`; review manually; prefer latest stable; breaking upgrades must document impact, include migration, update tests.

**Technology constraints:**

- **Frontend:** SvelteKit, Tailwind CSS, Lucide icons. No component libraries unless approved.
- **Backend:** SvelteKit server routes, native Web APIs, Supabase or other SQL-compatible; no separate backend unless necessary.
- **State:** `svelte/store` only. No Redux/Zustand/MobX.
- **i18n:** If used, **typesafe-i18n** only. Scripts: `typesafe-i18n`, `i18n:extract`, `i18n:watch`. Run `i18n:watch` during translation work.

**Full-stack / domain libraries (first-class primitives):** blockchain-wallet-validator, country-codes-and-flags, device-sherlock, exchange-rounding, payto-rl, txms.js, @blockchainhub/ican, typesafe-i18n, vite-plugin-pwa.

**Domain protocols and concepts** (respect semantics; do not invent alternatives):

- **ICAN** (International Crypto Account Number): IBAN-like for crypto. Format: country/network prefix + checksum + BBAN. Spec: https://payto.onl/solutions/ican. Validate with proper checksum (ican.js).
- **Payto:** Universal payment routing (RFC 8905 extension). Use Payto URLs for payment routing. Spec: https://payto.onl/solutions/payto, https://payto.money/, https://github.com/core-laboratories/payto.
- **Fintag:** Human-friendly alias/metadata discovery (HTML meta or `.well-known`). Treat as resolvable identifiers, not raw addresses.
- **TxMS** (Transaction Message System): Message-based transaction transport. Not "Transaction Management System". Core mainnet: +12019715152; testnet (Devín): +12014835939. Spec: https://payto.onl/solutions/txms.
- **PayPass:** Payment identifier as mobile wallet pass (.pkpass / Google Wallet). Spec: https://payto.onl/solutions/paypass.
- **ORIC** (Organization Identification Code): Organization identifier. API: https://oric.payto.onl/. Spec: https://payto.onl/solutions/oric.

**Authentication and identity:**

- Passkey (WebAuthn) or CorePass connector. CorePass: https://corepass.net/ (identity wallet, Passkey support).
- **CorePass enriched identity:** Registration can provide (with consent) email, o18y, o21y, kyc, kycDoc, dataExp. Data provided once, signed by user CoreID (Ed448); trust only if signature valid.
- **Data expiration:** `dataExp` (minutes). Server: `provided_till = now + (dataExp * 60)`. Enforce strictly; never extend without new signature; expired data = non-existent.
- **Enrichment endpoint:** `POST /webauthn/data`. Plugin repository: https://github.com/CorePass/better-auth-corepass-passkey

**Formatting:** Follow `.editorconfig` if present. Else: tabs, tab width 4; no tabs↔spaces mix; no trailing whitespace; files end with one newline. Reformat to match.

---

## Contributing and Code of Conduct

**Contributing (CONTRIBUTING.md):** Open an issue → fork and clone → create a branch → make changes → push and open a PR. Follow existing style; ensure tests/docs as needed. Contributions under same license as project (see `LICENSE`).

**Code of Conduct (CODE_OF_CONDUCT.md):** Community pledges a harassment-free, inclusive environment. Welcoming language, respect, constructive criticism, empathy. No trolling, harassment, or publishing others' private info. Reports to maintainers; appropriate response.

---

## Quick reference

| Topic | Use |
|-------|-----|
| New project | `npx github:bchainhub/dapp-starter` or clone + `node start.mjs` |
| Update from template | `node start.mjs --update` (keeps `vite.config.ts`) |
| Install addon | `npx addon <repo> <generator> <action>`; pin with `#tag` or `#branch` |
| Addon order | fetch → prompts → Hygen → _scripts → _config → _lang → typesafe-i18n |
| Required route param | `[param]` |
| Optional route param | `[[param]]` |
| Route group (no URL) | `(groupName)` |
| Server secrets | `$env/static/private`, `$env/dynamic/private` |
| Client env | `import.meta.env`, `VITE_*`; no secrets in _config or __SITE_CONFIG__ |
| i18n | `src/i18n/<lang>/index.ts`; addon _lang merges; then `typesafe-i18n --no-watch` |
| Migrations | `_migrations` (gitignored); set ORM `out` to `./_migrations` |

Use this skill whenever you edit or generate code in a SvelteKit project that uses the ĐApp Starter, addons, or the mota-dapp layout and conventions.
