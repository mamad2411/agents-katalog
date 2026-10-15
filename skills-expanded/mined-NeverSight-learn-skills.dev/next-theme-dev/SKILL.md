---
name: next-theme-dev
version: 1.10.0
description: |
  Next Commerce theme development for Spark, Intro Bootstrap, and custom
  storefront themes. Use when building, modifying, or debugging themes with
  Django Template Language, Theme Settings, ntk CLI, storefront GraphQL,
  Tailwind/Spark Web Components, or Intro Bootstrap/SCSS patterns. Also use
  after next-theme-figma has prepared a Figma storefront handoff package.
  Trigger when working in a theme directory with manifest.json, config.yml, or
  standard directories such as assets/, configs/, layouts/, templates/, and
  partials/.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Next Commerce Theme Development

## Using This Skill

This skill works with any AI coding tool that can load a markdown file as context.

| Tool | How to Use |
|------|-----------|
| **Recommended** | Clone `NextCommerceCo/skills` and run `./skills.sh`; choose your local agent target and this skill. |
| **No checkout** | Use `npx skills add NextCommerceCo/skills -g --skill next-theme-dev` and add `-a <agent>` when you want a specific agent. |
| **Fallback** | Load this `SKILL.md` as a system prompt, context file, rule, or chat upload if your tool does not support native skills. |
| **Version check** | From a source checkout, run `./skills.sh status all next-theme-dev`. `stale` means the installed copy is older, `modified` means equal versions differ, `local-newer` protects a newer installed copy, and `unknown-version` flags a version outside `X.Y.Z`. Review with `dry-run` before refreshing. |

---

## Preamble — Environment Check

If the task starts from a Figma storefront design, run `next-theme-figma` first
when practical. That upstream skill validates the Figma source, classifies
sections/assets, records theme/platform divergences, captures reference
screenshots, and produces the implementation handoff. Use this skill after that
handoff exists to make the actual DTL, Spark, CSS, ntk, and storefront QA
changes.

Run these checks at the start of every theme task to understand the working context:

```bash
# Check ntk installation
if command -v ntk >/dev/null 2>&1; then
  NTK_PATH="$(command -v ntk)"
  echo "$NTK_PATH"
  "$NTK_PATH" --help 2>&1 | sed -n '/NEXT Theme Kit version/{p;q;}'
else
  echo "ntk not installed — install via pipx, uv, or pip"
fi

# Check Python
python3 --version 2>/dev/null || python --version 2>/dev/null || echo "Python not found"

# Check for theme config
[ -f config.yml ] && echo "config.yml found" || echo "No config.yml — use 'ntk checkout' for an existing theme or 'ntk init' from a complete theme codebase"

# Identify theme
[ -f manifest.json ] && cat manifest.json || echo "No manifest.json"
```

Use the public Theme Kit guide for connection setup and command behavior:
`https://developers.nextcommerce.com/docs/storefront/themes/theme-kit`.

The CLI guidance in this skill targets NEXT Theme Kit 1.2.0. Its released
commands are `init`, `list`, `checkout`, `pull`, `push`, `watch`, and `sass`.
Identify the active CLI from the resolved executable and the version line it
emits. Do not infer its version from a different Python interpreter's package
metadata: pipx, uv, and system Python can each contain separate installations.

Create the API key in Storefront admin under **Settings > API Access**:

1. Create an OAuth app, give it a name, and assign a user.
2. Enable `themes:read` and `themes:write` in the Permissions tab.
3. Save the app and copy the generated API key.

For an existing store theme, load the API key into `NTK_APIKEY`, list themes,
and then check out the intended theme. `ntk checkout` downloads the files and
writes `config.yml` without saving an environment-supplied key:

```bash
export NTK_APIKEY="$THEME_API_KEY"
ntk list --env=development --store="https://<store-subdomain>.29next.store"
ntk checkout --env=development --theme_id=<id> --store="https://<store-subdomain>.29next.store"
```

For a new theme, start from a complete theme codebase such as Spark, then run
`ntk init`. `ntk init` registers the current codebase and writes `config.yml`;
it does not scaffold or download theme files. Do not run it from an empty
directory.

Do not create `config.yml` by hand during normal setup. Manual configuration is
only a recovery path:

```yaml
development:
  apikey: <api_key>
  store: https://<store-subdomain>.29next.store
  theme_id: <theme_id>
```

When `--apikey` is used, `ntk init` and `ntk checkout` save the key in
`config.yml` as plaintext. Prefer `NTK_APIKEY` for CI and agent runs because
Theme Kit 1.2.0 does not save an environment-supplied key. The environment
value takes precedence over both `--apikey` and the value in `config.yml`.
Ensure `config.yml` is gitignored before running either command, and never
commit or share it.

The file can contain several environments. Commands use `development` by
default; use `-e` or `--env` to select another entry. Treat the environment,
store, and theme ID as one deployment target when requesting approval.

`ntk pull` downloads the same theme files without writing `config.yml`. Use
`checkout` for initial connection and `pull` for later downloads that must not
change the saved connection settings.

---

## Implementation-Handoff Entry Contract

Apply this contract when the work mode is `implementation-handoff`: a
`next-theme-figma` handoff package exists or was promised because the task
references one or the upstream skill was run.

If the package directory was not provided, ask the operator for it. Do not
guess. Run the upstream strict validation gate before implementation:

```bash
node <next-theme-figma skill dir>/scripts/theme-figma.js validate-package /path/to/handoff
```

The validator script lives in the installed `next-theme-figma` skill directory,
which is a sibling of this skill in a `NextCommerceCo/skills` checkout or skills
install target. If that directory is unavailable, re-run `next-theme-figma` to
regenerate and validate the package. After `validate-package` passes, read
`figma-handoff.json` and confirm its `mode` is exactly
`implementation-handoff`.

**HARD STOP:** In `implementation-handoff` mode, if the package is missing or
`validate-package` fails, or `figma-handoff.json` has any other mode, STOP and
request the package or its regeneration in `implementation-handoff` mode from
the operator or `next-theme-figma`. Never silently fall back to re-reading the
Figma file or re-inferring the design. Do not re-infer the design from the
Figma source as a fallback.

### Prescribed Reading Order

Read the package in this order. The documented package has all eight files; the
strict validator requires the first seven, but does not require `notes.md`.

| Order | Package file | Implementation pass |
|------:|--------------|---------------------|
| 1 | `figma-handoff.json` | Task context: target store, repo, Figma source, theme family, and runtime contract. Read first. |
| 2 | `routes.json` | Templates plan for Step 4: Template Assembly: which templates/pages exist and their section order. |
| 3 | `sections.json` | Partials/section work: classification decides semantic rebuild vs. asset vs. live commerce component. Use for Step 4 partials and the Step 1 component inventory. |
| 4 | `assets.json` | Existing asset validation path: `scripts/validate-theme-assets.py --strict` in Step 2: Asset Preparation. |
| 5 | `platform-divergence-ledger.json` | Intentional platform deviations: only entries with decision `platform-wins` or `figma-wins-with-guardrails` and status `approved`, `implemented`, or `accepted-gap` are pre-approved `intentional-platform-divergence` items. Do not re-litigate those resolved entries. Entries with decision `needs-approval` or `blocked`, or status `open` or `blocked`, are unresolved; surface them to the operator before implementing the affected surfaces. |
| 6 | `viewport-coverage.json` | Responsive QA: the desktop/tablet/mobile reference set the Figma Fidelity Loop compares against. Availability is per route: check the route's `coverage` entry (`figma_ref`/`status`), not just the global `viewports` flags. |
| 7 | `validation-checklist.md` | Completion review before handback. |
| 8 | `notes.md` | Operator notes and unresolved questions. Read before building when present. If absent, note its absence in the handback and proceed; its absence alone is not a hard stop. |

The package is the design source of record in this mode. Consult the Figma file
only through the package, such as when exporting an asset named by a manifest.
Manifest guarantees are lost if implementation re-derives the design. A theme's
`DESIGN.md` still governs house style conventions where the package is silent;
when the two conflict directly, surface the conflict to the operator instead of
picking a winner.

The current v1 handoff records `target.theme_family` and
`target.runtime_contract` in `figma-handoff.json`; confirm that identity before
applying family-specific patterns. Legacy v0 packages remain readable during
the deprecation window: the `validate-package` command in `next-theme-figma`'s
bundled `scripts/theme-figma.js` normalizes `spark-divergence-ledger.json` and
`spark-wins` to the v1 contract and emits a deprecation warning. Treat that
warning as a migration prompt, not a validation failure. The strict
`validate-package` HARD STOP still applies to actual validation failures.

---

## From an Empty Store (Greenfield Path)

Use this path when the merchant store already exists but there is no theme
checkout, local theme directory, `config.yml`, or existing `theme_id`. The goal
is a new, unpublished theme in the selected family with a working preview URL.
Do not activate the new theme during development.

### 1. Identify and Choose the Theme Family

Identify the family before acquiring starter code or running setup. Use the
markers and runtime-contract tables in `Identify the Theme Family First` below,
then choose Spark, Intro Bootstrap, or a custom theme with the operator. Do not
default to Spark merely because the store is empty.

### 2. Acquire the Selected Theme

**Spark branch:** Clone the public Spark starter over HTTPS into a new local
directory:

```bash
git clone https://github.com/NextCommerceCo/spark.git theme
cd theme
```

Keep Spark's existing `.gitignore`; it already ignores `config.yml`.

**Intro Bootstrap branch:** Intro Bootstrap is distributed as a ZIP upload and
dashboard install, not as a public git clone. Obtain the approved ZIP from the
operator, use the Storefront dashboard theme-install flow to install it as an
unpublished theme, and then check out that installed theme after credentials
are available. Do not invent or recommend an upstream git URL.

**Custom-theme branch:** Obtain the owner-approved complete theme codebase or
installable package. Preserve its local runtime and build contract.

### 3. Get Theme API Credentials

In Storefront admin, go to **Settings > API Access**, create an OAuth app,
assign a user, and enable these permissions:

- `themes:read`
- `themes:write`

### 4. Create or Check Out the New Unpublished Theme

Install `ntk` first if it is missing (`pip install next-theme-kit`; see the
Preamble environment check).

**Spark branch:** From the Spark directory, run this invocation with the long
flags:

```bash
# Load THEME_API_KEY from a secret manager or protected environment file, then:
NTK_APIKEY="$THEME_API_KEY" ntk init --name="<theme name>" --store="https://<store-subdomain>.29next.store"
```

Set `THEME_API_KEY` from an environment file or in the shell without echoing
it. Spark's `.gitignore` does not cover conventional env files, so add the
chosen filename (for example `.theme-build.env`) to `.gitignore` before
creating it, or keep the file outside the checkout entirely. Rotate the key if
it was ever pasted literally into a command.

The short forms `-n`, `-a`, and `-s` also exist. Prefer the long flags in
handoffs and runbooks.

`ntk init` does not require an existing `theme_id`. It creates a new theme on
the store through the Admin themes API, then writes `config.yml` in the current
directory. That file includes the newly assigned `theme_id`.

`ntk init` does not create theme directories or starter files. Run it only
after cloning or copying a complete theme codebase.

**Intro Bootstrap branch:** After the dashboard ZIP install, use `ntk list` to
find the installed unpublished theme ID, then use the existing-theme
`ntk checkout` flow from the Preamble. Do not run `ntk init` from an empty
directory and do not substitute Spark files for the Intro package.

**Custom-theme branch:** Follow the owner-approved package/install path. Use
`ntk init` only when the local directory is already a complete theme codebase;
otherwise install it through the dashboard and check it out as an existing
theme.

The new theme is not active and does not affect the live storefront unless
someone activates it in the dashboard. Do not activate it during development.

Theme Kit 1.2.0 writes human-readable output. For automation, save and inspect
the complete output as well as the exit code. Invalid credentials, missing
resources, persistent connection or throttle failures, and a failed push exit
non-zero. Other server responses are not guaranteed to do so, so a zero exit
code alone is not proof that the intended state exists.

### 5. Preflight With `ntk list`

Before the first push, run:

```bash
ntk list
```

First inspect `config.yml` and confirm its `store:` value is the expected
`<store-subdomain>.29next.store` store and its `theme_id` is the intended new
theme. Never push until both values match.

Then use the `ntk list` output to confirm both conditions:

1. The intended new `theme_id` appears in the theme list. For Spark, use the
   ID written by `ntk init`. For Intro Bootstrap and dashboard-installed custom
   themes, use the ID written by `ntk checkout` after selecting the installed
   theme.
2. The theme marked `(Active)` is not the new theme.

Read the human-readable list and confirm the new theme appears before
continuing. Do not infer success from the exit code alone.

### 6. Build and Review the Initial Upload

Run the selected theme's own build and verification pipeline before uploading.
For Spark, use the standalone Tailwind CLI through its Make targets: run
`make install-tailwind` when needed, then `make verify-theme` (the complete
pre-upload check; fall back to `make build` or `make css` plus `make css-check`
if the target is absent). For Intro Bootstrap, preserve its `sass/main.scss` to
`assets/main.css` path and use `ntk watch` for local Sass compilation only after
the live-mutation approval gate; watch also pushes. The `ntk` CLI has no
CSS-build subcommand beyond `sass`.

**Spark branch:** Review every file intended for the first upload. After
satisfying the "Live Theme Mutation Approval Gate", upload the reviewed Spark
baseline:

```bash
# Initial Spark upload, excluding saved Theme Editor state.
# (css/ source is not an ntk-accepted directory; the compiled
# assets/main.css artifact is what uploads.)
for dir in assets configs layouts locales partials templates; do
  [ -d "$dir" ] && find "$dir" -type f
done \
  | grep -v '^configs/settings_data.json$' \
  | while IFS= read -r file; do ntk push "$file" || exit 1; done
```

This first reviewed baseline is the exception to the changed-files-only rule.
For later uploads, follow "ntk Push: Only Changed Files". The approval gate
applies to every push, including this non-active theme. `settings_data.json` is
saved Theme Editor state; seed it only as a deliberate, separately called-out
store-state change. Theme Kit 1.2.0 stops a push on the first failed upload and
exits non-zero, but it does not report per-file results or the files it did not
attempt. Keep the reviewed file list, read the complete output, and verify the
remote result before treating a multi-file upload as complete.

**Intro Bootstrap branch:** The dashboard ZIP install is the initial baseline;
do not replace it with a Spark upload. Review the SCSS source, obtain approval
before `ntk watch`, inspect the generated `assets/main.css`, and follow "ntk
Push: Only Changed Files" for subsequent targeted changes.

**Custom-theme branch:** Treat a dashboard-installed package as the baseline,
or use the Spark-style reviewed first-upload loop only when the approved custom
source is a complete local codebase that still needs registration.

### 7. Derive and Verify the Preview URL

The CLI prints the preview URL only while `ntk watch` is running. Do not start a
watch session merely to discover it. Derive it from the confirmed store
subdomain and the `theme_id` in `config.yml`:

```text
https://<store-subdomain>.29next.store/?preview_theme=<theme_id>
```

Open that URL and verify that it renders the uploaded unpublished theme. Confirm
the URL uses the new theme ID and that the live storefront remains on the theme
marked `(Active)` by `ntk list`.

### 8. Credential and CLI Safety

`ntk init` and `ntk checkout` write `config.yml`. A key supplied through
`--apikey` is saved there as plaintext; a key supplied through `NTK_APIKEY` is
not. `NTK_APIKEY` takes precedence over both `--apikey` and the saved key.
Spark's `.gitignore` already ignores `config.yml`. If working in a non-Spark
bare directory instead, add it to `.gitignore` before the first `ntk` command.
Never commit or share `config.yml`.

For named environments and target confirmation, follow the connection setup in
the preamble.

The complete Theme Kit 1.2.0 command set is `init`, `list`, `checkout`, `pull`,
`push`, `watch`, and `sass`. There is no `tailwind` subcommand. Run the theme's
own local tests and build checks before upload, then verify the rendered route
on the preview domain.

---

## Architecture

### Directory Structure

Every Next Commerce theme follows this structure:

```
theme/
├── assets/          # CSS, JS, images, fonts (served via CDN)
├── checkout/        # Optional/legacy checkout overrides if the theme uses them
├── configs/
│   ├── settings_schema.json   # Theme editor field definitions
│   └── settings_data.json     # Stored setting values
├── layouts/
│   └── base.html    # Main layout (all pages extend this)
├── locales/         # Translation JSON files (en.json, fr.json, etc.)
├── partials/        # Reusable template fragments
├── sass/ or css/    # Source stylesheets (sass/ for SCSS, css/ for Tailwind)
└── templates/       # Page templates (index.html, catalogue/, blog/, etc.)
```

Spark does not ship checkout templates. Checkout is platform-managed, and Spark owns the storefront cart plus the handoff to `/checkout/`.

### Identify the Theme Family First

Do this before copying patterns between reference themes:

| Theme family | Markers | Use these patterns |
|--------------|---------|--------------------|
| **Spark** | `css/input.css`, committed `assets/main.css`, `scripts/sass-compat.py`, `assets/js/spark-cart.js`, `assets/js/components/spark-*`, `DESIGN.md` | Tailwind v4 standalone CLI, vanilla JS/Web Components, GraphQL-first side cart, fixed-order homepage section partials, app hooks |
| **Intro Bootstrap** | `sass/main.scss`, Bootstrap classes, `assets/js/cart.js`, `assets/js/side_cart.js`, jQuery before `{% core_js %}` | Bootstrap 5, SCSS, platform side cart scripts, jQuery/core_js integration |
| **Custom theme** | Mixed or merchant-specific structure | Preserve the local stack. Inspect README/CLAUDE/DESIGN docs before adding tools or renaming conventions |

For a v1 `next-theme-figma` handoff, `target.theme_family` and
`target.runtime_contract` are the recorded outcome of this identification.
Confirm those fields agree with the checked-out theme before implementation;
use the Implementation-Handoff Entry Contract when they do not.

Intro Bootstrap is a strong reference for DTL patterns, template contexts, URL names, and older storefront conventions. Spark is the modern starter direction: zero jQuery, zero Bootstrap, Tailwind CSS v4, GraphQL-first cart components, named homepage section partials, and public app-hook surfaces. Do not port stack-specific implementation details across themes unless the current theme already uses that stack.

Never recommend replacing a working Intro Bootstrap runtime -- including its
jQuery lifecycle, SCSS pipeline, and GraphQL fetch client -- with Spark's Web
Components or Tailwind stack merely because Spark is newer. A theme-family
migration is a separate, owner-approved project, not a byproduct of a design or
maintenance task.

Before attributing a defect to Spark or Intro Bootstrap, compare the exact
selector, template, asset, or line-ending behavior with the current upstream
starter and record the installed theme version when known. If the behavior is
absent upstream, classify it as store-local or version-specific rather than a
starter-theme defect.

Preserve the runtime contract for the identified family:

| Theme family | Runtime contract to preserve |
|--------------|------------------------------|
| **Spark** | `assets/js/spark-platform.js`; Web Components such as `<spark-cart-drawer>`, `<spark-add-to-cart>`, and `<spark-quantity>` from `assets/js/components/spark-*`; and `assets/js/spark-preview.js` when the theme exposes the preview indicator |
| **Intro Bootstrap** | jQuery loaded before `{% core_js %}`, plus the existing platform cart and side-cart scripts |
| **Custom theme** | Inspect the local base layout and scripts; do not infer either starter's contract |

### Template Language

Templates use Django Template Language (DTL):

- **Inheritance:** `{% extends "layouts/base.html" %}` + `{% block content %}...{% endblock %}`
- **Includes:** `{% include "partials/header.html" %}`
- **Variables:** `{{ product.get_title }}`, `{{ settings.primary_color }}`
- **Tags:** `{% for item in products %}...{% endfor %}`, `{% if condition %}...{% endif %}`
- **Filters:** `{{ price|currency:currency_code }}`, `{{ text|truncatewords:10 }}`

### Settings System

Theme settings let merchants customize their store without code:

- `settings_schema.json` defines the editor UI — groups of fields with types like `text`, `color`, `image_picker`, `select`, `menu`, `checkbox`
- `settings_data.json` stores the current live Theme Editor values
- Templates access values via `{{ settings.field_name }}`

**Settings Information Architecture:**
- **Organize by merchant mental model**, not developer taxonomy — use "Side Cart" not "Advanced > Cart Configuration"
- **5+ settings = own top-level section** — don't bury 14 cart settings inside a generic "Advanced" group
- **Use merchant-friendly labels** — "Suggested Products" not "Upsells", "Cart Title" not "cart_header_title"
- **Treat `settings_data.json` as merchant state, not code** — pushing it can overwrite Theme Editor changes made in the dashboard. For new controls, add the field/default to `settings_schema.json` and make templates handle missing values with `|default` or explicit fallback logic. Only push `settings_data.json` when intentionally changing the store's saved setting values.
- **Keep dev-only values out of the schema** — implementation details (e.g., `upsell_fallback_slots`) belong in `settings_data.json` defaults, not in the editor UI
- **Reward thresholds:** Core Spark ships one default threshold pair (`usd_goal_1`, `usd_goal_2`) with merchant-facing labels like "Free Shipping Threshold" and "Free Gift Threshold." Do not add hard-coded currency fields to a public starter unless the merchant specifically needs them. Theme developers can extend `partials/block_cart_progress_wrapper.html` and `settings_schema.json` for store-specific currency rules.
- **Geo/currency runtime data:** Templates can read active `currencies`, `storefront_geos`, `geo`, and `request.CURRENCY_CODE`, but `settings_schema.json` is static editor configuration. Do not assume Theme Settings can automatically generate fields from the store's configured markets.
- **Group ordering gotcha:** Display order is determined by first-seen in `settings_schema.json`, not JSON key order. Renaming a group key makes it appear last in the editor

---

## Reference Documentation

For detailed reference on template tags, objects, filters, and settings types, use the public developer docs first. These are the source of truth — consult them before writing template code.

| Topic | Public docs |
|-------|-----------|
| Theme Kit setup and commands | `https://developers.nextcommerce.com/docs/storefront/themes/theme-kit` |
| Template tags | `https://developers.nextcommerce.com/docs/storefront/themes/templates/tags` |
| Template filters | `https://developers.nextcommerce.com/docs/storefront/themes/templates/filters` |
| Template objects | `https://developers.nextcommerce.com/docs/storefront/themes/templates/objects` |
| URLs & template paths | `https://developers.nextcommerce.com/docs/storefront/themes/templates/urls-and-template-paths` |
| Settings field types | `https://developers.nextcommerce.com/docs/storefront/themes/settings` |
| Translations / i18n | `https://developers.nextcommerce.com/docs/storefront/themes/translations` |
| Storefront GraphQL API | `https://developers.nextcommerce.com/docs/storefront/graphql` |

If a local `developer-docs` checkout is available, it is useful for source-level docs changes and exact MDX references. Public merchant guidance should still point to `developers.nextcommerce.com`, not local absolute paths.

When you need to know what variables a template has access to, the objects reference includes a **Template Contexts** table that maps every template path to its available view-specific variables, plus a **Dashboard Cross-Reference** showing where variable data is configured in the admin.

---

## Critical Warnings

These will silently break things if ignored:

### Full-Page Caching: The Server vs. Client Boundary

This is the most important architectural constraint in Next Commerce themes. All storefront pages are **fully cached for 5 minutes** on mapped domains. The `.29next.store` network domain bypasses that mapped-domain edge cache layer; it does not bypass the page cache itself. After a push, page-cache turnover remains per-edge and non-atomic on any domain. The cache is keyed by URL + language + currency combination — so each locale variant (EN+USD, FR+EUR, etc.) has its own cached page, and all visitors with that same locale see the same cached HTML.

This means product pricing is safe in templates (it varies by currency, and the cache handles that). But per-user data — cart, authentication, wishlists — is unique to each individual and fundamentally incompatible with page caching.

**Server-side templates (DTL) are for public content (same for all visitors in a locale):**
- Product details, pricing, categories, blog posts, pages
- Store info, settings-driven UI, navigation menus
- SEO metadata, structured data

**Client-side JavaScript (via GraphQL API) is required for per-user content:**
- Cart state (item count, totals, line items)
- User authentication state (logged in/out, username)
- Wishlists, saved items, order history

Never put `{{ cart.num_items }}` or `{{ user.is_authenticated }}` in a cached template — one user's data gets served to everyone in that locale. This is why Next Commerce themes don't show a cart item counter in the nav by default — displaying it requires a client-side GraphQL call on every page load, which is an intentional performance tradeoff.

```
SAFE in templates (cached per locale)    REQUIRES GraphQL (per-user, client-side JS)
─────────────────────────────────────    ──────────────────────────────────────────
{{ product.get_title }}                  Cart contents, count, totals
{{ session.price.price|currency:... }}   User login state / profile
{{ settings.* }}                         Wishlists, saved items
{{ store.name }}, {{ menus.*.items }}    Order history
Product prices, categories, filters      Checkout state
```

The `/cart/`, `/checkout/`, and `/accounts/` paths are excluded from full-page caching, but any content in shared layouts (headers, footers via `layouts/base.html`) renders on every cached page.

### Compiled CSS Must Be Committed (Installable Themes)

The platform does not compile CSS server-side. Build tools (Tailwind binary, npm, Sass CLIs) are not preserved on `ntk push` and don't come down on `ntk pull`. This means **the compiled, minified output (`assets/main.css` for Tailwind themes, the compiled CSS for SCSS themes that build locally) MUST be committed to the repo** for the theme to be installable.

If `assets/main.css` is gitignored:
- Cloning the repo gives a styled-broken theme
- Pulling via ntk gives a styled-broken theme
- The merchant has to install a Tailwind toolchain just to get a working storefront

The right pattern:
- **Gitignore the binary** (`tailwindcss`, `node_modules/`) — platform-specific, large, and not needed at install time
- **Commit the artifact** (`assets/main.css`) — small, what actually ships, makes the theme self-contained
- **Add a `make release` (or equivalent) target** that rebuilds + stages the artifact so source and output stay in sync
- **Document the contract** in CLAUDE.md / README so future devs don't re-gitignore the artifact thinking it's "build output"

Treat the committed `main.css` as a versioned artifact. Drift between `css/input.css` and the committed output is a bug to be fixed before the next push, not a normal state.

### Tailwind + DTL: No Dynamic Class Construction

Never build Tailwind class names with template variables:
```django
{# BAD — Tailwind's purge scanner can't see runtime values #}
<div class="bg-{{ settings.primary_color }}">

{# GOOD — use CSS custom properties #}
<style>:root { --primary-color: {{ settings.primary_color|default:"#1E293B" }}; }</style>
<div class="bg-[var(--primary-color)]">
```

Tailwind scans source files at build time to determine which classes to include. Template variables only resolve at runtime on the server, so dynamically constructed class names get purged from the CSS output.

### No Non-ASCII in JavaScript Files

The platform processes all theme files through the DTL engine, including `.js` files. Non-ASCII characters (curly quotes, em dashes, emoji) in JS files cause encoding errors. Stick to plain ASCII in all JavaScript.

### Live Theme Mutation Approval Gate

`ntk push` and `ntk watch` both mutate the selected remote store theme. Before
running either command, use `AskUserQuestion` to show the operator the exact
store, environment, theme ID and status, and files or watch scope, then obtain
explicit confirmation. Do not push or start a watch session without that
confirmation; approval for one command or watch session does not authorize a
later one.

If the selected target is the active theme, read
`references/active-theme-publish-and-qa.md` completely before publishing. Its
manifest, rollback, publish-order, cache-bypass, smoke-test, and evidence gates
are required in addition to this approval. A targeted push reduces scope, but
it is still a sequential live mutation rather than an atomic deployment.

While `ntk watch` is running, deleting a recognized local theme file deletes
the corresponding file from the store. Include that behavior in the approval
prompt, and do not run watch across cleanup or generator steps that may remove
files unexpectedly.

### ntk Push: Only Changed Files

After the operator confirms the live mutation, push specific files, never the
entire theme:
```bash
# Good
ntk push templates/index.html
ntk push assets/main.css configs/settings_schema.json

# Bad — pushes everything, slow, unnecessary
ntk push
```

Be especially careful with `configs/settings_data.json`: it is the store's saved Theme Editor state. Do not include it in a push just because you added a schema field. Prefer schema defaults plus template fallbacks:
```django
{% if not settings.hide_media_bar %}
    {# media bar #}
{% endif %}
```

Push `settings_data.json` only when the task explicitly requires updating current saved values, and call that out in the summary.

### jQuery Before core_js (Intro Bootstrap / jQuery Themes)

Intro Bootstrap and other jQuery themes must load jQuery before the platform's `{% core_js %}` tag:
```django
<script src="{{ 'jquery.min.js'|asset_url }}"></script>
{% core_js %}
```

Spark does not use jQuery or `{% core_js %}`. It uses `assets/js/spark-platform.js` plus Spark Web Components instead.

### CDN Caching

CloudFront aggressively caches assets and full pages (5 minutes on mapped domains):
- **Always develop, preview, debug, and verify on the `.29next.store` network domain** — it bypasses the 5-minute mapped-domain edge cache layer, not the page cache itself
- Do not use a mapped public storefront domain to decide whether a change landed
- Check the public domain only after network-domain verification, as a final customer-path smoke test
- Do not require undocumented query parameters or response headers as proof of deployment
- Verify the served HTML, expected asset URLs, visible behavior, and screenshots on the network domain
- Asset changes (CSS/JS) may take a moment to propagate on CDN

### DTL Comments: Single-Line Only

Django template comments must be single-line. Multi-line comment blocks render as visible text:
```django
{# This is correct — single line #}

{# This is WRONG —
   it will render as visible text on the page #}
```

### Anti-Slop Design Rules

When building or modifying theme UI, enforce these rules to avoid generic "AI-generated" aesthetics:
- No 3-column icon grids (the default lazy layout)
- No centered-everything layouts
- No generic hero text ("Welcome to our store")
- No uniform rounded corners on everything
- No default blue buttons
- No decorative gradient blobs or abstract shapes
- No emoji in UI elements
- Default `text-sm` (14px) feels too small for marketing storefronts — prefer `text-base` (16px) for body copy
- In Spark, follow the theme's own `DESIGN.md`: sharp, minimal commerce UI; no Bootstrap imports, jQuery patterns, or app-dashboard design tokens

### Text Sizing

For marketing-forward storefronts, `text-sm` (14px) as the body default feels cramped. Use `text-base` (16px) minimum for body copy. Headlines should have clear hierarchy — don't let Tailwind defaults flatten your type scale.

---

## Known Gotchas

Start with shared diagnostics, then apply only the contracts for the identified
theme family. A merchant-session observation is not a starter-theme defect
until the exact behavior is confirmed in that starter and version.

| Scope | Gotcha | Details |
|-------|--------|---------|
| **Shared** | **Settings group ordering** | Group display order = first-seen in `settings_schema.json`, not JSON key order. Renaming a group makes it appear last |
| **Shared** | **Settings schema shape** | `settings_schema.json` is top-level section -> group -> array of setting objects. Do not use ad hoc object maps for new public examples |
| **Shared** | **Theme-family attribution** | Confirm the exact behavior in the current upstream starter and version before calling a merchant-theme issue a Spark or Intro Bootstrap defect |
| **Shared** | **CRLF line endings** | Theme files may use CRLF endings. Byte-exact text edits can then fail confusingly; detect line endings first and preserve or normalize them deliberately |
| **Shared** | **manifest.json can't be pushed** | ntk excludes `manifest.json` from push/watch. Version is set at `ntk init` only |
| **Shared** | **Preview URL** | `https://<store-subdomain>.29next.store/?preview_theme=<theme_id>` is the canonical URL for testing unpublished theme changes |
| **Shared** | **Preview session pinning** | Visiting `?preview_theme=<theme_id>` pins that browser session with a cookie. Use the preview indicator's **Exit preview** action or visit `/?deactivate-theme=true`; a plain URL does not exit preview |
| **Shared** | **ntk accepted directories** | Only these are recognized: assets, checkout, configs, layouts, partials, templates, locales, sass. Files outside these are silently ignored |
| **Shared** | **Asset path mapping** | A local file like `assets/img/merchant/hero.jpg` is uploaded as `assets/img/merchant/hero.jpg`, but templates reference it without the `assets/` prefix: `{{ 'img/merchant/hero.jpg'|asset_url }}` |
| **Shared** | **Figma export overlays** | Figma frames often include labels, badges, card UI, shadows, or text that the theme also renders. Inspect the node tree before export; export the clean underlying image/fill when the overlay is theme UI |
| **Shared** | **Build artifacts must be committed** | The platform doesn't compile CSS/JS server-side and doesn't preserve binaries on push. Compiled CSS must be checked in or the theme is unstyled on install. Gitignore the toolchain and commit the artifact |
| **Intro Bootstrap** | **jQuery before core_js** | Preserve jQuery before `{% core_js %}` and retain the existing platform cart/side-cart scripts unless intentionally replacing that stack |
| **Spark** | **Product picker returns parent PK** | `settings.gift_product` gives the parent product PK. For cart operations (`addCartLines`), use `.children.first.pk` to get the variant ID |
| **Spark** | **Reward thresholds** | Spark core exposes one default threshold pair. Currency-specific reward rules belong in a theme-developer extension, not hard-coded starter settings |
| **Spark** | **Shadow DOM ≠ slotted styles** | Shadow DOM styles don't apply to slotted light-DOM content. Inject a guarded `<style>` tag into `document.head` when that pattern is required |
| **Spark** | **connectedCallback fires early** | `connectedCallback` can fire before child elements are parsed. Use a lazy `_ensureRefs()` pattern plus `requestAnimationFrame` for initial updates |
| **Spark** | **Concurrent mutation guard** | Cart mutations must use an `_isMutating` flag to prevent races from rapid clicks |
| **Spark** | **sass-compat is required** | Every Tailwind build must run through `sass-compat.py`; the platform SCSS compiler rejects several modern CSS constructs |
| **Spark** | **App hooks are extension surfaces** | Use existing `{% app_hook %}` slots before forking Spark templates for app integrations |

---

## Dashboard-Theme Bridge

Some theme features require **both** theme settings AND dashboard configuration to work correctly. The theme handles the UI, but the actual discount/shipping logic lives in Dashboard > Marketing > Offers.

| Feature | Theme Side | Dashboard Side |
|---------|-----------|----------------|
| Free shipping progress bar | Settings: threshold amount, progress messages, bar UI | Requires: Conditional free shipping Offer matching the threshold |
| Free gift auto-add | Settings: gift product picker, threshold, auto-add JS | Requires: Conditional discount Offer that makes the gift $0 |
| Suggested products | Settings: product pickers, display logic | No Offer needed (products added at full price) |
| Discount codes | Coupon input UI in cart | Requires: Discount code created in Dashboard |

**Without the matching Offer, the theme UI will promise something it can't deliver** — e.g., the progress bar says "Free shipping at $50!" but checkout still charges shipping.

When adding these settings to `settings_schema.json`, include help text pointing merchants to the relevant dashboard setup. A link to documentation is the minimum viable approach.

---

## Design to Theme Workflow

Step-by-step process for assembling a working theme from a design file. This is the primary workflow for the marketer persona.

### Step 1: Design Intake

Accept any of: Figma link, screenshot, PDF, or verbal description. Extract:
- **Color palette** — primary, secondary, accent, neutrals, backgrounds
- **Typography** — font families, size scale, weight usage, line heights
- **Spacing system** — section padding, component gaps, content margins
- **Component inventory** — header, footer, hero, product cards, CTAs, nav, cart drawer
- **Static vs dynamic split** — which elements show the same content for all visitors (DTL) vs per-user content (GraphQL)

Identify the theme family before implementation. Spark designs should map to Tailwind tokens, Web Components, homepage section partials, and app hooks. Intro Bootstrap designs should map to Bootstrap/SCSS and the existing jQuery/platform side cart where present. If a `DESIGN.md` exists in the project, it is the **source of truth** for all visual decisions. Read it before making UI choices. In `implementation-handoff` mode, the handoff package is the design source of record and `DESIGN.md` governs house style where the package is silent; surface direct conflicts to the operator per the Implementation-Handoff Entry Contract.

### Step 1.25: Effective Typography Preflight

Before styling any custom template, resolve the store's effective font stack in
this order: current theme settings first, including font or typography controls
supported by the identified family, then the derived rules in the base layout
and compiled styles. A store-derived base may hardcode families that its
upstream starter does not, so inspect the installed code and state rather than
assuming upstream defaults. Custom templates inherit this effective stack
unless they explicitly declare otherwise. Prefer settings-driven tokens, and
do not redeclare fonts per node to paper over drift. For the Intro Bootstrap
adapter, follow `references/intro-preservation-contract.md` section
`Typography Inheritance` rather than duplicating that family contract here.

### Step 1.5: Figma Fidelity Loop

When a Figma source is provided, treat the Figma file as a visual spec, not merely an asset bucket. Run this loop proactively so visual deltas are found, fixed, or documented before handoff.

1. **Map the design.** Identify the Figma file key, desktop/tablet/mobile frames, page/frame names, and section order. Record which storefront route/template each frame maps to. In `implementation-handoff` mode, this mapping already exists: take the file key, frames, section order, and route mapping from `figma-handoff.json`, `routes.json`, and `sections.json` instead of re-deriving them from the Figma file.
2. **Classify every section before building.** Decide what should be semantic HTML/CSS, what should use live platform data, what should be an exported image/vector asset, and what is intentionally a static composed frame. Text, buttons, controls, product selectors, prices, tables, FAQs, and nav/footer links should normally be rendered by the theme, not baked into a screenshot. In `implementation-handoff` mode, surfaces covered by unresolved `platform-divergence-ledger.json` entries, using the resolved and unresolved definitions in the Implementation-Handoff Entry Contract, must be surfaced to the operator before building them.
3. **Extract the smallest real assets.** Inspect children, fills, masks, vectors, and hidden variants. Export the underlying image fill/vector node or intended composed asset. Full-frame exports are diagnostic unless the design intentionally calls for a static bitmap composition.
4. **Assemble semantically.** Build sections with real DTL/HTML, CSS, accessible controls, and platform contracts. Use extracted assets only for visual media, logos, product art, iconography, or intentional composites.
5. **Push and compare.** After upload, capture the preview URL and the matching Figma frame/section at the same viewport. In `implementation-handoff` mode, compare against the reference screenshots recorded in `viewport-coverage.json` for the matching route's `coverage` entry. A viewport has no design reference when it is globally unavailable or the route's entry lacks a `figma_ref` or marks the viewport missing (for example `documented-missing`): do not re-read the Figma file to invent one; implement responsive behavior at that viewport with theme judgment and record it in the handback as a package-documented gap. Compare section-by-section for image crop, asset choice, typography, spacing, alignment, colors, text wrapping, CTA size, touch targets, footer/header, and responsive behavior.
6. **Create a remediation queue.** For each mismatch, mark it `fix-now`, `intentional-platform-divergence`, or `blocked-input-needed`. In `implementation-handoff` mode, mismatches already recorded as resolved in `platform-divergence-ledger.json` are `intentional-platform-divergence` items and must not be re-opened. Platform divergences include the identified family's PDP/gallery behavior, live variant pickers, backend product imagery, app hooks, cart/auth state, and other dynamic commerce surfaces.
7. **Repeat.** Patch the `fix-now` items, push changed files only, and re-run visual/DOM checks. Continue until the page is close to Figma or every remaining difference is explicitly documented for the user.

Narrated screen recordings are an optional, high-bandwidth review input.
Transcribe the narration, turn each concrete complaint into a remediation-queue
entry with route, section, viewport, severity, and mismatch status, then verify
each fix individually. These entries join the same remediation queue as step 6
and use its exact status set: `fix-now`, `intentional-platform-divergence`, or
`blocked-input-needed`. A recording never substitutes for the visual-QA loop
or its matching screenshots.

If the task covers several pages, walk one page or section group at a time. It is acceptable to use subagents for independent section audits, but give them raw Figma/build screenshots or URLs and ask for deltas, not implementation conclusions.

**Hard stop:** Do not ship a page made mostly of full-section screenshots as a shortcut unless the user explicitly asks for a static visual prototype. A photocopy can be useful for diagnosis, but production storefronts should preserve text, links, controls, SEO, accessibility, live product data, and responsive behavior.

### Step 2: Asset Preparation

This is the **#1 time bottleneck** — design assets are merchant-specific and can't be templated.

- **Fonts:** Preserve the identified family's typography contract. Add local
  `.woff2` assets and `@font-face` only when the design and current theme call
  for them. In Intro Bootstrap, inspect `font_script`, `font_body`, and
  `font_header` settings plus the derived base before changing typography.
- **Images:** Hero images, product photography, lifestyle shots, product cutouts, and press logos must come from the merchant or the design source. Use placeholders only while blocked, and replace them before QA
- **Icons:** Prefer inline SVG (smallest payload, style-able) or an icon font. Avoid individual image files for icons
- **Optimization:** All assets serve via CDN. Keep routine images under 200KB when quality allows. `ntk` supports WebP, but the current accepted extension list does not include AVIF.
- **Optimization timing:** Optimize after confirming the correct source asset is selected, but before assembling the design into the theme.
- **Manifest:** For merchant-specific exports, keep an export checklist or manifest mapping Figma node IDs to local filenames. Prefer `docs/<merchant>-asset-manifest.json` so source metadata does not become a CDN-served storefront asset. Use `assets/img/<merchant>/manifest.json` only when the manifest is intentionally public and contains no internal design provenance.

### Figma Asset Export Runbook

Use this runbook before exporting design assets into the identified theme. The
main rule: **do not export a visible Figma frame until you know whether it is
the real asset or a composed UI artifact.**

**Identify the file key and node IDs**

- Figma design URLs have this shape: `https://www.figma.com/design/<file_key>/<file_name>?node-id=<node_id>`.
- The `file_key` is the path segment after `/design/` or `/file/`.
- The URL `node-id` usually appears with hyphens, such as `123-456`; Figma APIs and tools may return the same node as `123:456`. Preserve the exact ID returned by the tool you are using in any manifest.
- If exporting several assets from one file, record the file URL, file key, page/frame name, node ID, local filename, intended usage, and export scale.

**Inspect the node hierarchy before export**

Before exporting, inspect the layer tree and answer:

- Is the selected node a frame/card/section, a vector/logo layer, a masked image fill, or a nested bitmap?
- Are badges, prices, review stars, CTA text, shadows, gradients, or decorative labels children of the node?
- Is the asset clipped by a mask or frame that hides important subject matter on mobile?
- Does the node contain a clean image fill that should be exported instead of the containing frame?
- Are there hidden variants or responsive frames with cleaner desktop/mobile crops?

When using Figma MCP/API tools, fetch only the relevant node context, inspect children/visibility/fills, then export the smallest node that represents the intended asset.

**Export frames versus underlying fills**

- Export a frame when the whole composition is meant to be one static bitmap, such as a hero collage, UGC strip, lifestyle mosaic, or editorial block with intentionally baked layout.
- Export an underlying fill/image node when Spark will render the surrounding card, product title, price, CTA, sale badge, label, shadow, border, or responsive crop.
- Export a vector/SVG node when it is a clean logo or icon and does not contain raster screenshots, unwanted masks, or text that should remain rendered by the theme rather than baked into the asset.
- If the only available node is a composed product card, duplicate it in Figma or ask the designer/merchant for the source image, then hide the UI children before export.

**Badge doubling warning**

Always audit promotional labels in three places:

- Product/source image pixels: discount badges, "best value" stickers, price callouts, review badges, or guarantee marks baked into the image.
- Spark-rendered UI: product cards, PDP price blocks, on-sale sections, cart upsells, or custom homepage cards that add live sale labels.
- Dashboard/product pricing: compare-at/retail price states that cause Spark to render sale pricing or badges.

Only one layer should communicate the same discount. If product art already includes a "Save 50%" badge, disable/remove the Spark badge for that placement or export clean product art. If Spark needs live sale state, product art must be clean.

**Media and press logos**

- Export each logo as an individual transparent PNG or clean SVG, not as text typed into the theme.
- Preserve brand proportions. Set CSS max dimensions on the strip, but do not crop logos into identical boxes unless the design intentionally normalizes them.
- Use meaningful `alt` text for press/brand logos, such as `Women's Health`, `FOX`, or `The Verge`. If a repeated decorative logo is already announced in adjacent text, use empty `alt=""`.
- Prefer monochrome/grayscale treatment in CSS when possible; do not permanently recolor brand logos unless the design source and brand usage allow it.
- Verify the strip uses `<img>` elements backed by exported assets. Text fallbacks are acceptable only while blocked and should not survive final QA when the design uses real logos.

**Deterministic asset names**

Use lowercase, kebab-case names under a merchant folder:

```text
assets/img/<merchant>/hero.jpg
assets/img/<merchant>/product-knee.png
assets/img/<merchant>/logos/press-logo.png
assets/img/<merchant>/pdp/how-pull-on.png
```

Name by storefront role, not the raw Figma layer name. Avoid spaces, version suffixes like `final-final`, and opaque export names like `Frame 184.png`. Record source node IDs in a manifest instead of encoding them into filenames.

**Format selection**

- **PNG:** Transparent logos, product cutouts, UI composites with alpha, or images that must preserve crisp edges.
- **JPG/JPEG:** Opaque photography and lifestyle imagery where smaller files matter more than transparency.
- **SVG:** Clean vector logos/icons with no unwanted embedded raster, no design-only text, and acceptable brand usage. Omit `requires_alpha` for SVG entries; the validator treats SVG transparency as not mechanically provable.
- **WebP:** Opaque or transparent optimized images when the theme/storefront target supports it; `ntk` accepts `.webp`.
- **AVIF:** Do not rely on it for theme pushes unless the local `ntk` accepted extension list has been updated; current known `ntk` patterns do not include `.avif`.

**Verify dimensions, transparency, and paths**

- Check actual dimensions after export and put matching `width`/`height` attributes in templates to reduce layout shift.
- Confirm transparent logos/product cutouts have an alpha channel. A white-background logo exported as PNG is still wrong if the design expects transparency.
- Confirm file size and visual quality after compression. Do not crush medical/product detail just to hit an arbitrary byte target.
- Local asset files live under `assets/`, but `asset_url` paths are relative to the asset root. Example: `assets/img/merchant-slug/hero.jpg` renders as `{{ 'img/merchant-slug/hero.jpg'|asset_url }}`.
- `ntk` pushes nested asset paths as their relative template names, such as `assets/img/merchant-slug/logos/press-logo.png`. Push exact changed files: `ntk push assets/img/merchant-slug/logos/press-logo.png partials/home.html`.
- Root-level `manifest.json` is not part of the `ntk` accepted patterns. JSON under `assets/**/*.json`, `configs/**/*.json`, and `locales/**/*.json` is accepted. Do not store Figma file keys, node IDs, review notes, or clean-export attestations under `assets/` unless you are comfortable publishing that metadata through the storefront CDN.

**Manifest pattern**

Use a small JSON manifest when a design export has more than a few files or when product art/logos are easy to confuse:

```json
{
  "figma_file_key": "<figma_file_key>",
  "merchant": "merchant-slug",
  "assets": [
    {
      "path": "assets/img/merchant-slug/logos/example-magazine.png",
      "asset_url_path": "img/merchant-slug/logos/example-magazine.png",
      "figma_node_id": "<node_id>",
      "role": "press-logo",
      "alt": "Example Magazine",
      "expected_width": 148,
      "expected_height": 28,
      "requires_alpha": true,
      "max_bytes": 50000
    },
    {
      "path": "assets/img/merchant-slug/product-cutout.png",
      "asset_url_path": "img/merchant-slug/product-cutout.png",
      "figma_node_id": "<node_id>",
      "role": "clean-product-art",
      "alt": "Compression sleeve product cutout",
      "expected_width": 374,
      "expected_height": 312,
      "requires_alpha": true,
      "forbid_badges": true,
      "clean_export_verified": true
    }
  ]
}
```

The helper script at `scripts/validate-theme-assets.py` validates manifest paths, dimensions, alpha requirements, max file size, naming, expected `asset_url` paths, and explicit clean-export confirmations:

Pillow is required when the manifest contains PNG, JPEG, GIF, ICO, or WebP
assets. SVG-only manifests can be validated without Pillow.

```bash
cd /path/to/skills/next-theme-dev
python3 -m pip install Pillow
python3 scripts/validate-theme-assets.py \
  --theme /path/to/theme \
  --manifest docs/<merchant>-asset-manifest.json \
  --strict
```

The script cannot OCR an image or prove a badge is absent. It makes that limitation explicit by requiring `clean_export_verified: true` when `forbid_badges` or `forbid_baked_text` is set.

**Visual QA checks**

- Open the preview URL and scroll every lazy-loaded asset section into view. Watch the Network panel or DOM for broken images.
- Compare product cards, homepage product tiles, PDP galleries, and cart upsells for duplicated discount labels.
- Confirm media/press logos render as images, not fallback text, and that alt text is sensible.
- Check mobile crops at 375px and 390px widths. Product, joint/body, or logo subject matter should not be clipped out of the important region.
- Hard-refresh after asset pushes if the browser still holds an older asset.

### Step 3: Settings Schema Design

Map design tokens to merchant-configurable settings in `configs/settings_schema.json`:

Before hardcoding any copy into a template, run a settings-suitability pass.
Merchant-iterable copy such as trust lines, shipping promises, legal blocks,
and promotional text belongs in `settings_schema.json` and a wired template
region from the start. One settings edit should replace a template edit, push,
and cache-wait round trip for each copy iteration.

1. **Colors** → `color` type fields (primary, secondary, accent, background)
2. **Fonts** → `text` type fields for font family names
3. **Feature toggles** → `checkbox` type fields (show/hide sections)
4. **Content** → `text` fields for headlines, CTAs, placeholder copy
5. **Navigation** → `menu` type fields linked to dashboard menus
6. **Products** → `product` type fields for featured/upsell products

Follow the Settings IA principles: organize by merchant mental model, 5+ settings get their own section, use merchant-friendly labels.

### Step 4: Template Assembly

Build order:
1. **`layouts/base.html`** — Preserve the identified family's stylesheet and script order while wiring settings, global head/scripts, and header/footer includes. Independently injected global components must be wrapped in their own named blocks when the family exposes that override surface so page templates can override or suppress them without CSS hacks.
2. **Partials** — One per design component (`partials/header.html`, `partials/footer.html`, `partials/product_card.html`, etc.)
3. **Page templates** — `templates/index.html`, `templates/catalogue/product.html`, etc. using `{% extends %}` and `{% block %}`
4. **Cart/user features** — Keep per-user state client-side. In Spark, use the existing GraphQL/Web Component contract; in Intro Bootstrap, preserve the existing form POST, jQuery, GraphQL side-cart, and `{% core_js %}` integration described in `### Side Cart Customization` and `references/intro-preservation-contract.md`.

### Step 5: Styling

- Spark/Tailwind themes: configure tokens in `css/input.css`, compile to committed `assets/main.css`, and run `scripts/sass-compat.py`
- Intro Bootstrap/SCSS themes: use the existing `sass/` entrypoint and Bootstrap variable/utility patterns
- Wire CSS custom properties from theme settings in `layouts/base.html`:
  ```django
  <style>:root { --primary: {{ settings.primary_color|default:"#1E293B" }}; }</style>
  ```
- For Tailwind output, **run sass-compat.py before every push** (required — platform rejects modern CSS)
- Test responsive breakpoints: mobile (375px), tablet (768px), desktop (1280px+)
- Put decorative hover-only behavior behind `@media (hover: hover)`. Touch
  devices need an explicit tap/button interaction; do not rely on sticky
  emulated `:hover` state.

#### CSS Override Triage

When a visual property survives an apparently correct CSS change, inspect the
rendered element before adding another override:

1. Check the winning declaration and computed styles on the element and its
   ancestors, including inherited `color`, ancestor opacity, filters, and
   visibility.
2. Inspect `::before`, `::after`, and `::marker`; generated content can be the
   visible layer even when the element's own color is correct.
3. Check whether broad list or typography selectors are leaking into a custom
   component. Scope fixes to the component and prefer a direct child selector
   when only one list level should change.
4. Express de-emphasis with a muted color token when opacity would also fade
   child content or generated decoration.
5. Re-check the affected route on the `.29next.store` network domain, then
   compare the exact behavior with the relevant starter and version before
   treating it as a starter-theme or platform defect.

### Step 6: Client-Side Features

For per-user content (cart, auth, wishlists):
- Use the identified family's existing client-side API and transport contract.
- In Spark, preserve its `/api/graphql/` requests with CSRF, Web Components,
  document event bus, and `sessionStorage` plus cookie cart identity.
- In Intro Bootstrap, preserve its jQuery runtime, existing GraphQL side-cart
  fetch transport and injected endpoint, `storefront_cart_id` cookie, and
  platform `{% core_js %}` wiring; do not retrofit Spark components or add
  Spark transport assumptions.
- In a custom theme, inspect and preserve the local client/runtime contract.

### Step 7: Verify & Deploy

1. Preview unpublished changes: `https://<store-subdomain>.29next.store/?preview_theme=<theme_id>`
2. Always verify on the `.29next.store` network domain before checking a mapped public domain
3. Push only changed files: `ntk push templates/index.html partials/header.html`
4. Check dashboard-side requirements: free shipping/gift features need matching Offers (see Dashboard-Theme Bridge)
5. Verify cart operations work end-to-end (add, remove, quantity change, checkout)
6. When asserting on served markup, remember that `grep -c` counts lines, not
   occurrences; minified single-line HTML therefore caps the result at one.
   Count each match instead:

   ```bash
   grep -o 'data-template="product.<template-key>"' served.html | wc -l
   ```

Before handoff, use screenshot capability already available in the work
environment and save real PNGs under `./qa-output`. Capture desktop at
1440px and mobile at 390px. Do not install or bundle a new browser automation
dependency solely for this gate. If direct capture is unavailable, give the
operator the exact preview URLs and viewports for manual capture; if that also
cannot happen, record an explicit accepted gap with owner and scope. Wait for
fonts and lazy media to load, inspect both images, and record any route or
viewport that could not be captured.
DOM metrics can supplement screenshots but never replace them. For an
active-theme change, use the complete evidence ladder in
`references/active-theme-publish-and-qa.md`.

---

## Task Recipes

### Change Colors or Fonts

1. Add fields to `configs/settings_schema.json`:
```json
{
  "Theme Styles": {
    "Colors": [
      { "name": "primary_color", "type": "color", "label": "Primary Color", "default": "#1E293B" }
    ],
    "Typography": [
      { "name": "body_font", "type": "text", "label": "Body Font Family", "default": "system-ui, sans-serif" }
    ]
  }
}
```

2. Wire into `layouts/base.html` via CSS custom properties:
```django
<style>
:root {
    --primary-color: {{ settings.primary_color|default:"#1E293B" }};
    --body-font: {{ settings.body_font|default:"system-ui, sans-serif" }};
}
</style>
```

3. Push both files: `ntk push configs/settings_schema.json layouts/base.html`

### Generate a Family of Related Templates

When several similar pages share a design system, generate every template from
one source: a design-system module plus a per-item data dictionary or map. Any
scripting language is acceptable. Each feedback round should regenerate the
whole family identically, so merchant feedback becomes data edits rather than
hand-editing the same change into multiple files.

For example, the per-item data map can be keyed by template slug:

```json
{
  "overview": {
    "headline": "A clear overview",
    "hero_asset": "assets/img/overview-hero.webp",
    "sections": ["hero", "features", "faq"]
  },
  "details": {
    "headline": "The useful details",
    "hero_asset": "assets/img/details-hero.webp",
    "sections": ["hero", "specifications", "faq"]
  }
}
```

Keep the generator and its data inside the theme project, for example in its
`scripts/` folder, and make every run regenerate every template in the family.

### Add a Custom Page Template

1. For the default page template, modify or create `templates/pages/page.html`. For a custom page template selectable from the dashboard/API, create `templates/pages/page.<template-name>.html` (replace `<template-name>` with the actual template slug):
```django
{% extends "layouts/base.html" %}
{% block content %}
<div class="container">
    <h1>{% if page.title %}{{ page.title }}{% else %}{{ flatpage.title }}{% endif %}</h1>
    {% firstof page.url flatpage.url as page_url %}
    {% if page_url %}
        <a href="{{ page_url }}">View page</a>
    {% elif page.slug %}
        {# Use this fallback only after confirming root-slug routes for the store. #}
        <a href="/{{ page.slug }}/">View page</a>
    {% endif %}
    {% if page.content %}
        <div>{{ page.content }}</div>
    {% elif flatpage.content %}
        <div>{{ flatpage.content }}</div>
    {% endif %}
</div>
{% endblock %}
```

2. Push: `ntk push templates/pages/page.html` or `ntk push templates/pages/page.<template-name>.html`.
3. Create or update the Page record in the dashboard and select the custom template. If using the Admin API, set `template` to the template slug for `page.<template-name>.html`; leave it blank for the default `page.html`.
4. Verify the actual storefront route. Many Next Commerce flatpages route at `/<slug>/`, not `/pages/<slug>/`. Do not hardcode page links until a `curl -I` or browser check confirms the store's route shape.

**Admin API page creation:** `ntk` manages theme files only; it does not create dashboard Page records. If an admin token has `content:write`, create pages through the Admin API:

```bash
curl -sS -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "X-29next-API-Version: 2024-04-01" \
  -H "Content-Type: application/json" \
  -d '{"title":"Our Technology","slug":"our-technology","content":"<p>Theme-rendered page.</p>","template":"","meta_title":"Our Technology","meta_description":"Theme-rendered page."}' \
  "https://{store}.29next.store/api/admin/pages/"
```

All Admin API calls must use `https://{store}.29next.store/api/admin/`,
`Authorization: Bearer <api access token>`, and
`X-29next-API-Version: 2024-04-01`. Do not use `/api/v1/...` paths or
`Authorization: Token ...`; those commonly return storefront HTML 404 pages
instead of JSON. Confirm conventions against
https://developers.nextcommerce.com/docs/admin-api when adding new Admin API
requests.

For a custom template file such as `templates/pages/page.story.html`, send `"template":"story"` instead of the empty default-template value.

After creation, verify the route with the preview theme:

```bash
curl -I "https://{store}.29next.store/{slug}/?preview_theme={theme_id}"
```

**Context gotcha:** Some page routes expose `page.title`, `page.content`, `page.url`, and `page.slug`; older Spark examples use `flatpage.title`, `flatpage.content`, and `flatpage.url`. For merchant templates that need to be portable, support `page.*` first and keep `flatpage.*` as a fallback. Prefer `page.url` or `flatpage.url` when present; use `/<slug>/` only after confirming root-slug routes for the store. Admin page `content` is rich text; keep Django auto-escaping by default, and use `|safe` only for trusted admin-authored HTML after sanitizing any non-admin HTML.

### Add a Custom Product Template

1. Choose a stable `<template-key>` and create
   `templates/catalogue/product.<template-key>.html`. The product URL slug does
   not select this filename automatically. Until inheritance between product
   templates is proven safe for the target platform version, make the custom
   template standalone and extend only the base layout:
```django
{% extends "layouts/base.html" %}
{% load core_tags %}
{% block content %}
    {# Custom product layout #}
{% endblock %}
```

2. Run the theme's local tests and build checks, then push the exact file:

```bash
ntk push templates/catalogue/product.<template-key>.html
```

Read the complete command output and confirm the preview route after the push.

3. Set the product's `template` field to `<template-key>` in Dashboard or with
   the Admin API. `ntk` uploads theme files; it does not assign a product's
   template field.

   **Observed staged-rollout pattern (not a documented platform contract):**
   set the field while the custom template file exists only on the draft
   theme. On the live theme, `missing template ⇒ default template`.

   > **Observed behavior, not platform-documented:** Verify this fallback on
   > the target store before relying on it.

   Live traffic therefore stays on the default template while the preview uses
   the custom one. Cut over by pushing the custom file and its dependencies to
   the live theme ID; no product-field change is needed at cutover. Confirm the
   fallback and the custom resolution separately with the DOM marker below.

4. Request the product route on the preview/network domain with
   `?preview_theme=<theme-id>`. If the custom candidate is missing, invalid, or
   not assigned, resolution silently falls back to
   `templates/catalogue/product.html`. Detect that fallback with a
   template-specific DOM marker or structure and inspect the served HTML. For
   example, add `data-template="product.<template-key>"` to the custom
   template's existing root element and confirm that exact attribute is
   present in the response. Visual similarity alone is not proof that the
   custom template resolved.

Do not make a merchant-specific product template extend
`templates/catalogue/product.html` until that inheritance path has an explicit
platform regression test. Duplicate the required product/PDP contracts in the
standalone template and preserve the checklist below.

Use the identified family's preservation strategy at the available override
surface. **Spark:** prefer extending/overriding the theme's template blocks.
**Intro Bootstrap:** extract and preserve the working commerce core verbatim;
read `references/intro-preservation-contract.md` completely before changing an
Intro buy box, scripts, cart, settings, typography, or base-layout blocks.

### Custom Spark PDP Redesigns

Spark PDP work is behavior preservation first, visual matching second. A static Figma PDP can look correct while silently breaking variant matching, price updates, cart submission, subscriptions, reviews, or app tracking.

Before changing `templates/catalogue/product.html`, read the local Spark docs if available:

- `docs/pdp-customization.md` - PDP redesign preservation checklist, QA runbook, and partialization guidance
- `docs/pdp-variant-state.md` - selected-variant Interface for picker, price, gallery, and add-to-cart adapters

**Preservation checklist:**

| Surface | Preserve this |
| --- | --- |
| Product data JSON | Keep `{{ product.data|json_script:"product-data" }}` in `extrascripts`; `SparkVariantState` depends on `#product-data`. |
| Variant controls | Keep real controls named `attr_<code>` from `variant_form`. Custom swatches/buttons must update those real controls and values. |
| Price bindings | Keep a visible price node with `data-price` and a compare-at node with `data-price-retail`, hidden when empty. |
| Quantity | Keep a real `quantity` field or `<spark-quantity name="quantity">` inside the cart form. |
| Add-to-cart form | Keep `id="add-to-cart"`, CSRF, hidden `cart_form` fields, submit button, and POST action to `{% url 'cart:add' pk=product.pk %}`. |
| Subscription hooks | Preserve `<spark-subscription>` when `product.get_interval` and `interval_count_choices` exist. |
| App hooks | Preserve PDP app hooks such as `product_rating_summary`, `product_info`, `product_footer`, `product_reviews`, `product_review_cta`, `view_product`, and `add_to_cart`. |
| Inventory states | Preserve `session.availability.is_available_to_buy` branches and selected-variant CTA disablement. |
| Sticky/mobile CTA | The sticky CTA should click the real submit button; it should not duplicate cart logic. Check that it does not cover content on mobile. |
| Fallbacks | Products with no image, incomplete product data, no reviews, or no JS should still render usable UI. |

Missing product data, `attr_*` controls, price bindings, CSRF/quantity/cart fields, app hooks, or sold-out behavior is a hard stop before upload unless the merchant explicitly accepts that behavior change.

**Safe picker pattern:** visual markup can change, but the underlying control name and value must come from `variant_form`.

```django
{% for field in variant_form %}
    {% if 'attr' in field.id_for_label %}
        {% for choice in field.field.choices %}
            <label>
                <input type="radio" name="{{ field.html_name }}" value="{{ choice.0 }}">
                <span>{{ choice.1 }}</span>
            </label>
        {% endfor %}
    {% endif %}
{% endfor %}
```

**DOM smoke audit:** run this in the browser console after a redesign. It catches missing contracts, but it does not replace selecting variants and actually adding to cart.

```js
(function() {
  var form = document.getElementById('add-to-cart');
  var controls = Array.prototype.slice.call(document.querySelectorAll('[name^="attr_"]'));
  console.table({
    productData: !!document.getElementById('product-data'),
    variantControls: controls.length,
    variantNames: Array.from(new Set(controls.map(function(control) { return control.name; }))).join(', '),
    priceNode: !!document.querySelector('[data-price]'),
    retailPriceNode: !!document.querySelector('[data-price-retail]'),
    addToCartForm: !!form,
    csrf: !!(form && form.querySelector('[name="csrfmiddlewaretoken"]')),
    quantity: !!(form && form.querySelector('[name="quantity"], spark-quantity')),
    submitButton: !!(form && form.querySelector('button[type="submit"]')),
    subscription: !!document.querySelector('spark-subscription'),
    stickyCta: !!document.getElementById('sticky-atc'),
    horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth
  });
})();
```

**QA before push:**

1. Select all variants and confirm price, compare-at price, gallery image, form action, and CTA availability update.
2. Add to cart with quantity greater than 1 and confirm the selected child product reaches the cart.
3. Test subscription products, sold-out products, no-image products, and products with no reviews when available.
4. Check mobile widths around 375-430px for horizontal overflow and sticky CTA coverage.
5. Verify review/app hook surfaces still render or remain present for apps.

`configs/settings_data.json` is merchant Theme Editor state. Add controls to `settings_schema.json` and use template fallbacks for missing values. Push `settings_data.json` only for an intentional store-state change. One merchant's `variant_picker = radio` change was design-relevant, but it was still merchant state and should be called out when pushed.

Do not split Spark's PDP into partials just for one merchant design. If repeated custom PDP work justifies it, prefer stable partials for gallery/media, buy box, variant picker, quantity/cart controls, trust/benefit strip, size guide, reviews, and related products.

### Update Product Media From Figma

Use this recipe only when the user explicitly wants Figma PDP gallery/product imagery copied into the store's backend product listings. Product media is store data, not a theme asset, so `ntk` is not the upload path.

1. Consult the local `developer-docs/` checkout or public Admin API docs before writing requests. Confirm the product image endpoints, required permissions, request schema, and whether the current token has `catalogue:write`. Every Admin API request must use `https://{store}.29next.store/api/admin/`, `Authorization: Bearer <api access token>`, and `X-29next-API-Version: 2024-04-01`. If the token lacks `catalogue:write`, stop before any mutating call, report the exact missing scope, and point the user to the Admin API authentication docs for minting a scoped token.
2. Build or receive a product-media manifest from `next-theme-figma`: parent product ID, route, variant IDs, source Figma node IDs, captions, intended display order, replacement policy, and rollback notes.
3. Export original or canvas-rendered Figma media only. Do not use thumbnails, preview screenshots, estimated crops, or full PDP screenshots. If the product listing requires square media, produce square source files before upload.
4. Optimize after source selection is stable. Prefer WebP when supported by the store/theme pipeline; `cwebp -q 85..90` is a starting point for large PNG exports, but product/PDP media often merits `-q 95` when q85-90 shows softness or artifacts. Decide from visual review plus byte size, not a fixed quality number.
5. Upload with the Admin API product images endpoint, usually `POST /api/admin/products/{id}/images/` with `file_name`, `caption`, and `display_order`. The current Admin API supports JSON and `multipart/form-data`; base64 JSON `attachment` is acceptable for small optimized files, but prefer multipart or further optimization when the optimized source is over about 2 MB or the API reports body-size/rate-limit headers.
6. Treat create plus variant association as a transactional pair. As soon as a `POST` succeeds, record the new `imageId` and rollback command (`DELETE /api/admin/products/{id}/images/{imageId}/`) in the manifest. If variant associations are needed and the create endpoint does not persist them, patch each image afterward with `PATCH /api/admin/products/{id}/images/{imageId}/` and the documented `variants` payload; if any patch fails, abort the batch and roll back newly created images before touching old media.
7. Preserve Spark PDP behavior: the gallery should read backend product media, variant pickers keep their real `attr_*` controls, and product art should not be forced into theme static assets unless it is a non-commerce decorative asset.
8. Before deleting old product images, save a rollback manifest with old image IDs, URLs, captions, display order, and variant associations. Delete old media only after explicit user approval or when the user's current request explicitly named the existing images being replaced by URL, alt text, filename, or image ID.
9. Verify by API and storefront preview: re-fetch `GET /api/admin/products/{id}/images/` and diff IDs, `display_order`, captions, and variants against the manifest; confirm Admin API rate-limit or `Retry-After` headers were not hit; then check PDP gallery hero and thumbnails, product listing/card imagery when relevant, desktop/mobile viewport screenshots, and browser console errors.

Call out any platform-owned divergence in the final report, especially default variant image ordering or PDP galleries that do not dynamically swap images after a variant (`attr_*`) control changes.

### Add a Partial

1. Create `partials/{name}.html` with the fragment
2. Include it: `{% include "partials/{name}.html" %}`
3. Pass context if needed: `{% include "partials/product_card.html" with product=item %}`
4. Push both files

### Modify Navigation

Navigation menus are managed in Dashboard > Storefront > Navigation. The theme accesses them via the `menus` global object and a `menu` settings field:

1. Add a menu field to `configs/settings_schema.json`:
```json
{
  "Navigation": {
    "Menus": [
      { "name": "main_menu", "type": "menu", "label": "Main Navigation", "default": "main_menu" }
    ]
  }
}
```

2. Render in the template:
```django
{% for item in settings.main_menu.items %}
    <a href="{{ item.url }}" class="{% if item.current %}active{% endif %}">
        {{ item.name }}
    </a>
    {% if item.level > 0 %}
        {# Has children — render dropdown #}
        {% for child in item.items %}
            <a href="{{ child.url }}">{{ child.name }}</a>
        {% endfor %}
    {% endif %}
{% endfor %}
```

Menus support up to 3 levels of nesting. Read the objects reference for all `item` properties.

### Add Translations

1. Add keys to each locale file in `locales/`:
```json
{
  "cart": {
    "empty_message": "Your cart is empty",
    "checkout_button": "Proceed to Checkout"
  }
}
```

2. Use in templates: `{% t "cart.empty_message" %}`
3. With variables: `{% t "cart.item_count" with count=cart.num_items %}`
4. Push all changed locale files

### Cart and User State (Client-Side State Required)

Because of full-page caching, cart and user state must be resolved client-side;
server-side template variables for that per-visitor data can be cached and show
stale or wrong data. Use the storefront GraphQL API at `/api/graphql/` for
client-side cart reads/mutations and user queries. Preserve a family's existing
server form POST where it is the established add-to-cart contract. The
existence of Intro Bootstrap's server-side add-to-cart POST does not permit
rendering per-visitor cart state in cached DTL templates; cart and user state
must still be fetched client-side.

Use GraphQL for:
- Cart operations: `createCart`, `addCartLines`, `updateCartLines`, `removeCartLines`
- Reading cart state: `cart` query (item count, totals, line items)
- User state: `me` query (authentication, profile)
- Any data that varies per visitor

For new Spark-style GraphQL requests, include the CSRF token:
```javascript
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

fetch('/api/graphql/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        query: `{ cart { totalQuantity totalAmount { amount currency } } }`
    })
})
```

Do not force that transport example onto an existing family client. Intro
Bootstrap's side cart uses the endpoint injected by `partials/side_cart.html`
and its established plain fetch contract; preserve it together with the
platform runtime.

Read the public GraphQL reference for the full schema, all available queries/mutations, and example payloads.

For cart-line selections, `properties { key value }` is the current storefront
schema in both Spark and Intro Bootstrap. The former CartLineNode `attributes`
field was removed platform-side. Keep `properties { key value }` aligned in
create, update, and remove operations; changing only one operation leaves the
other cart paths incompatible.

### Side Cart Customization

Side carts are one of the most common theme customization requests. Start by identifying the theme family.

**Intro Bootstrap / platform side cart pattern:**
- Preserve `partials/side_cart.html`, `assets/js/cart.js`, and `assets/js/side_cart.js` unless intentionally replacing the cart stack.
- Keep jQuery before `{% core_js %}` in `layouts/base.html`.
- Style with Bootstrap 5 and existing SCSS partials.
- Use DTL for the static shell and translations, and the existing JS for cart mutations.
- Apply the family-neutral cart-line schema rule in
  `### Cart and User State (Client-Side State Required)`. In Intro Bootstrap,
  the create, update, and remove operations in `assets/js/side_cart.js` must
  move together.
- Preserve the `storefront_cart_id` cookie, the single delegated `change`
  listener on `#cart-modal`, and platform-owned remove/population wiring in
  `{% core_js %}`. See `references/intro-preservation-contract.md`.

**Spark side cart pattern:**
- Use `assets/js/spark-cart.js` as the GraphQL cart client.
- Use `assets/js/spark-platform.js` instead of `{% core_js %}`.
- Use these Web Components: `<spark-cart-drawer>`, `<spark-progress-bar>`, `<spark-upsell-item>`, `<spark-add-to-cart>`, `<spark-quantity>`.
- Keep the shell in `partials/side_cart.html`; keep progress and suggested-product fragments in `partials/block_cart_progress_wrapper.html`, `partials/block_cart_progress_bar.html`, `partials/block_cart_upsell.html`, and `partials/block_cart_upsell_item.html`.
- Treat `partials/block_cart_progress_wrapper.html` as the extension point for merchant-specific reward threshold logic.

**Spark Theme Settings shape:**

```json
{
  "Side Cart": {
    "General": [
      { "name": "cart_header_title", "type": "text", "label": "Cart Title", "default": "Your Cart" },
      { "name": "sidecart_open_on_add", "type": "checkbox", "label": "Open Cart After Add", "default": true }
    ],
    "Rewards Progress": [
      { "name": "enable_progress_bar", "type": "checkbox", "label": "Enable Progress Bar", "default": true },
      { "name": "usd_goal_1", "type": "number", "label": "Free Shipping Threshold", "default": 50 },
      { "name": "usd_goal_2", "type": "number", "label": "Free Gift Threshold", "default": 100 },
      { "name": "gift_product", "type": "product", "label": "Free Gift Product" },
      { "name": "step_1_message", "type": "text", "label": "Shipping Message", "default": "You are {amount} away from FREE shipping" },
      { "name": "step_2_message", "type": "text", "label": "Gift Message", "default": "You are {amount} away from a FREE gift!" },
      { "name": "final_step_message", "type": "text", "label": "Complete Message", "default": "You unlocked free shipping and a free gift!" }
    ],
    "Suggested Products": [
      { "name": "enable_upsells", "type": "checkbox", "label": "Enable Suggested Products", "default": true },
      { "name": "upsell_section_title", "type": "text", "label": "Section Title", "default": "You may also like" },
      { "name": "upsell_product_1", "type": "product", "label": "Product 1" },
      { "name": "upsell_product_2", "type": "product", "label": "Product 2" },
      { "name": "upsell_product_3", "type": "product", "label": "Product 3" }
    ]
  }
}
```

**Key implementation patterns:**

- **Event bus**: Spark cart components communicate via custom events on `document`: `spark:cart:updated` (after any mutation), `spark:cart:added` (item added), `spark:cart:toggle` (open/close drawer). Other components listen on `document` for these events — no direct component coupling.

- **Cart persistence**: Cart ID stored in both `sessionStorage` (fast access) and a 30-day cookie (cross-tab persistence). On page load, check `sessionStorage` first, fall back to cookie. Always sync both after cart creation.

- **Mutation guard**: All cart mutations must check/set an `_isMutating` flag to prevent race conditions from rapid clicks (e.g., quantity +/+ before first response returns). Reset the flag in `finally` block.

- **Success validation**: Check `result.success` not `result.cart.numItems > 0`. The latter fails on empty cart after removing last item. Surface `result.errors` array for descriptive messages instead of generic "Could not add to cart".

- **Product picker PK gotcha**: `settings.gift_product` returns the parent product PK. For cart operations (`addCartLines`), use `.children.first.pk` to get the actual variant ID.

- **Reward thresholds**: Core Spark uses one default threshold pair (`usd_goal_1`, `usd_goal_2`). Do not expose hard-coded multi-currency fields in the starter. If a merchant needs store-specific currency logic, extend the wrapper partial and schema deliberately.

- **Suggested product visibility**: Products may have metadata defining which suggested-product slots to show. When the cart changes, JS checks each cart product's metadata and hides products already in the cart.

- **Free gift auto-add/remove**: When cart total crosses the gift threshold, JS automatically adds the gift product via `addCartLines` with `isUpsell: true`. When it drops below, JS removes the gift line. The gift product is configured via a `product` type theme setting. **Note:** This only adds the product to cart — making it actually free requires a matching Offer in the dashboard (see Dashboard-Theme Bridge section).

- **Cart count badge**: Updated via JS after every cart operation by selecting all `[data-cart-count]` elements in the DOM and setting their text content. This is the only way to show cart count — never use `{{ cart.num_items }}` in cached templates.

- **Web Component timing**: Load component scripts BEFORE template inclusion. Use `_ensureRefs()` lazy pattern since `connectedCallback` fires before children parse. For slotted content styling, inject `<style>` into `document.head` with a guard flag (Shadow DOM styles don't reach slotted elements).

- **Design from Figma (Spark)**: When a design targets Spark, map visual
  elements to this component architecture. For Intro Bootstrap or a custom
  family, preserve that family's CSS and behavior contracts instead of
  introducing Spark Web Components.

**Files to create/modify:**

| File | Purpose |
|------|---------|
| `assets/js/spark-cart.js` | Spark GraphQL cart client |
| `assets/js/components/spark-cart-drawer.js` | Spark cart drawer Web Component |
| `assets/js/components/spark-progress-bar.js` | Spark reward progress Web Component |
| `assets/js/components/spark-upsell-item.js` | Spark suggested-product Web Component |
| `partials/side_cart.html` | Main cart drawer shell (included in `layouts/base.html`) |
| `partials/block_cart_progress_bar.html` | Progress bar with step indicators |
| `partials/block_cart_progress_wrapper.html` | Default threshold selector and extension point |
| `partials/block_cart_upsell.html` | Suggested product section |
| `partials/block_cart_upsell_item.html` | Individual suggested product row |
| `configs/settings_schema.json` | Add Side Cart settings section |
| `css/input.css` or `sass/components/_sidecart.scss` | Side cart styling, depending on theme stack |

**Important Spark constraints:**
- No non-ASCII characters in JS files (platform processes through DTL engine)
- All cart mutations require CSRF token (`X-CSRFToken` header from `csrftoken` cookie)
- Cart ID stored in both `sessionStorage` and cookie for cross-tab persistence
- Use `Intl.NumberFormat` for client-side currency formatting (matches browser locale)
- Only push changed files with ntk, never the entire theme

---

## Deployment Workflow

### Standard (SCSS themes)

```bash
ntk watch    # Watches for changes and auto-pushes
```

ntk watch handles Sass compilation automatically — `.scss` files in `sass/` are compiled to `assets/` before pushing.

### Tailwind Themes

Spark uses the Tailwind v4 standalone CLI with no Node dependency. In Spark, prefer the project commands:

```bash
make install-tailwind   # One-time local binary install
make dev                # Run the Tailwind watcher and ntk watch in parallel
ntk watch               # Watch and push files only; does not compile Tailwind
make css                # One-shot Tailwind compile + sass-compat
ntk push assets/main.css # Push the compiled CSS artifact
make release            # Compile, run sass-compat, and stage assets/main.css
```

`ntk watch` does not compile Tailwind or run `sass-compat.py`. Spark's
`make dev` target runs the Tailwind watcher and `ntk watch` together.

For custom Tailwind themes, use one of these setups:

**Standalone CLI (preferred when starting fresh).** Download the platform-specific binary from `tailwindlabs/tailwindcss` releases, gitignore it, and orchestrate via `Makefile`:

```makefile
TAILWIND = ./tailwindcss
COMPAT = python3 scripts/sass-compat.py

dev:
	@$(TAILWIND) -i css/input.css -o assets/main.css --watch &
	@ntk watch

css:
	$(TAILWIND) -i css/input.css -o assets/main.css --minify
	$(COMPAT) assets/main.css

release: css
	@git add assets/main.css
```

Add an `install-tailwind` Make target that detects the dev's OS/arch and curls the right release binary. The binary stays gitignored (76MB, platform-specific) but `assets/main.css` is **committed** (see "Compiled CSS Must Be Committed" critical warning).

**npm-based (only when the theme already has a Node toolchain).** Orchestrate via `package.json`:

```json
{
  "scripts": {
    "dev": "npm run tailwind:watch & ntk watch",
    "build": "npm run tailwind:build && npm run compat",
    "tailwind:watch": "npx @tailwindcss/cli -i css/input.css -o assets/main.css --watch",
    "tailwind:build": "npx @tailwindcss/cli -i css/input.css -o assets/main.css --minify",
    "compat": "python3 scripts/sass-compat.py assets/main.css"
  }
}
```

```bash
npm run dev    # Runs Tailwind watcher + ntk watch concurrently
```

ntk watch detects the Tailwind CSS output (`assets/main.css`) changes and pushes automatically. If you see partial CSS on the store (rare race condition), manually push after Tailwind finishes:
```bash
ntk push assets/main.css
```

**Either option:** `assets/main.css` must be committed to the repo so the theme is installable without a local toolchain. Recompile and recommit it on every CSS source change using the theme's release/build target.

### CSS Compatibility Pipeline (Required for Tailwind themes)

The platform's SCSS compiler rejects modern CSS features. **Every Tailwind build must run through `sass-compat.py`** — this is not optional. The script strips/converts: `@property` rules, `oklch()` → hex, `color-mix()`, `@layer`, logical properties (`margin-inline`), `:is()`/`:where()` pseudo-classes, and media range syntax (`width >= 768px`).

Run the theme's CSS build any time you edit `css/input.css` or templates/partials that introduce Tailwind classes:

```bash
make css          # compile Tailwind and run sass-compat
make css-check    # make css, then fail if generated CSS still has unsafe constructs
make verify-theme # preferred pre-upload/release check when present
```

`assets/main.css` is the uploaded artifact. The platform does not compile Tailwind or preserve local binaries on `ntk push`, so a theme can look correct locally and still ship broken styling if the generated CSS is stale, missing, or contains unsupported compiler syntax. Treat `assets/main.css` drift as a bug: rebuild and commit/push it with the source change.

Known risky generated CSS:

- `@supports`, `@property`, `@layer`
- `oklch()` and newer color functions
- `color-mix()` unless the local compat helper has an explicit safe conversion
- `:is()` / `:where()`
- logical properties such as `margin-inline`, `padding-block`, and `inset-inline-start`
- media range syntax such as `(width >= 768px)`
- scientific-notation lengths such as `3.40282e38px`
- `min()`, `max()`, and `clamp()` when debugging compiler-specific failures; do not ban these blindly unless the target platform path proves they fail

Add the compat step to the build pipeline:

```json
{
  "scripts": {
    "dev": "npm run tailwind:watch & ntk watch",
    "build": "npm run tailwind:build && npm run compat",
    "tailwind:watch": "npx @tailwindcss/cli -i css/input.css -o assets/main.css --watch",
    "tailwind:build": "npx @tailwindcss/cli -i css/input.css -o assets/main.css --minify",
    "compat": "python3 scripts/sass-compat.py"
  }
}
```

The compat script should be boring and predictable: transform only known patterns, fail loudly when unsupported CSS remains, and never silently "fix" unfamiliar syntax by guessing. If the theme has no checker yet, add one around `scripts/sass-compat.py --check assets/main.css` or a dedicated `make css-check` target.

Before upload, scan the generated artifact:

```bash
python3 scripts/sass-compat.py --check assets/main.css
ntk push assets/main.css
```

Troubleshooting CSS failures:

- **Local Tailwind/build failure:** `make css` fails before upload. Fix `css/input.css`, the local Tailwind binary, or the command setup.
- **Platform Sass/compiler failure:** local build passes but upload/storefront CSS parsing fails. Run `make css-check`; the failure should point to an unsupported construct and file. Minimize the generated CSS if needed, then extend `sass-compat.py` only for a safe, known transform.
- **CDN/cache issue:** pushed CSS is correct but the storefront looks stale. Test on the `.29next.store` network domain and hard-refresh before checking a mapped public domain.
- **Missing uploaded compiled CSS:** templates changed but styling did not. Rebuild `assets/main.css` and push that file explicitly.

Avoid dynamic Tailwind classes in DTL templates. Tailwind only emits classes it can see at build time, so `bg-{{ settings.primary_color }}` and string-built utilities disappear from `assets/main.css`. Use CSS custom properties (`bg-[var(--primary-color)]`) or static conditionals that include complete class names.

---

## Debugging

### Common ntk Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Bad API key or expired | Create or update the OAuth app in Storefront admin under Settings > API Access |
| `404 Not Found` | Wrong theme_id or store URL | Run `ntk list` to verify, check `config.yml` |
| `File not in valid path` | File outside recognized theme directories | Check file is in assets/, configs/, layouts/, locales/, partials/, sass/, templates/, or an optional checkout/ directory |
| `Connection refused` | Store URL wrong or store offline | Verify `store` value in config.yml uses the `.29next.store` domain |

### Template Syntax Errors

Template errors show as 500 pages on the storefront. Common causes:
- Unclosed tags (`{% if %}` without `{% endif %}`)
- Wrong variable paths (`product.title` vs `product.get_title`)
- Missing `{% load %}` tags for custom template tag libraries
- Using `{% url 'name' %}` with wrong URL name — check the URLs reference

To debug: check the store's `.29next.store` domain (it bypasses the mapped-domain edge cache layer, not the page cache itself), look at the browser's network tab for 500 responses, and read the error message in the response body.

### GraphQL Issues

- **403 Forbidden:** Missing or invalid CSRF token. Ensure you're reading the `csrftoken` cookie and sending it as `X-CSRFToken` header.
- **Queries return null:** Check field names against the GraphQL schema. Use the interactive explorer at `https://{store}.29next.store/api/graphql/` (GraphiQL).

### Cache Issues

If changes aren't appearing:
1. Page-cache turnover is per-edge and non-atomic on any domain. After a push, consecutive
   fetches of the same URL can alternate between old and new responses for
   several minutes. Sample repeatedly; never judge cache turnover from one fetch.
2. Make cookie-less requests against the `.29next.store` network domain so a
   preview-session cookie does not select another theme.
3. Confirm the preview URL contains the intended `preview_theme` ID when
   verifying an unpublished theme.
4. Assert on the exact template-specific DOM marker or changed HTML string,
   not general appearance.
5. For asset changes, request the asset URL found in the served HTML and confirm an exact changed CSS or JavaScript token. When the platform serves the built file byte-for-byte, compare the downloaded and local file checksums.
6. Hard-refresh the browser (Cmd+Shift+R).
7. Exercise the affected behavior and compare desktop/mobile screenshots before diagnosing a propagation problem. Repeated fetches and DOM markers supplement these screenshots; they do not replace them.

---

## Supported File Types

ntk recognizes these extensions:

- **Templates:** `.html`
- **Config:** `.json`
- **Styles:** `.css`, `.scss`
- **Scripts:** `.js`
- **Media:** `.woff2`, `.gif`, `.ico`, `.png`, `.jpg`, `.jpeg`, `.svg`, `.eot`, `.ttf`, `.woff`, `.webp`, `.mp4`, `.webm`, `.mp3`, `.pdf`

Theme Kit 1.2.0 ignores files outside its accepted path and extension patterns
when `ntk push` builds the upload list. It does not validate those files or
report per-file status, so review the printed upload count and verify the
remote result.
