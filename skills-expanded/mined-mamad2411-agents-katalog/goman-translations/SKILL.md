---
name: goman-translations
description: "Manage app translations with goman.live. Use when: adding translations, adding i18n keys, localizing components, checking translation keys exist, searching translations, updating language content, managing i18n strings, extract hardcoded strings, localize folder, audit missing translations."
argument-hint: "Describe the translation task (e.g., 'localize LoginScreen component', 'add key auth.login.button', 'check missing translations')"
---

# Goman Translations Skill

Translation management for multi-language apps via the goman.live API.

## First-time setup (run once before anything else)

**Check if `.env` exists next to this `SKILL.md` file** (same folder).

If it does NOT exist, tell the user to run this from their project root:

```bash
npx github:bel-frontend/goman-live-skills
```

Then:
> Run the command above to create `.env`, fill in `GOMAN_API_KEY` and `GOMAN_APP_ID` from goman.live dashboard → Settings → API Keys, then ask me to continue.

**Do not run any scripts until `.env` exists and has real credentials.**

## Running scripts

All scripts live in the `scripts/` subfolder of this skill. Always `cd` into it first, then run with `node`:

```bash
cd <path-to-skill>/scripts
node goman-languages.js
```

In one line:

```bash
cd .agents/skills/goman-translations/scripts && node goman-languages.js
```

The scripts auto-load `.env` from the parent skill folder — no need to set env vars manually.

## Available Scripts

| Script | What it does | Example |
|--------|-------------|---------|
| `goman-languages.js` | List active language codes | `node goman-languages.js` |
| `goman-namespaces.js` | List translation namespaces | `node goman-namespaces.js` |
| `goman-get.js <fullKey>` | Get translations for a key | `node goman-get.js auth.login.button` |
| `goman-search.js [opts]` | Search/filter translations | `node goman-search.js --namespace auth.login --query button` |
| `goman-create.js <fullKey> <json> [ctx]` | Add or update translations | `node goman-create.js auth.login.button '{"en":"Log in","be":"Увайсці"}' "Login button"` |
| `goman-delete.js <fullKey>` | ⚠️ Delete a key permanently | `node goman-delete.js auth.login.button` |

All scripts output JSON. Parse with `JSON.parse()` when processing results.

## Key Format

```
namespace.key
```

- Namespace = everything **before** the last dot
- Key = everything **after** the last dot
- Example: `"screens.login.submitButton"` → namespace `"screens.login"`, key `"submitButton"`

⚠️ Every `fullKey` must contain at least one dot.

## Workflows

### 1. Add a Single Translation Key

```
STEP 1: node goman-languages.js          → get valid language codes
STEP 2: node goman-get.js <fullKey>      → check if key already exists
STEP 3: node goman-create.js <fullKey> <json> <context>  → create/update
```

### 2. Localize a Component

```
STEP 1: Receive component code from user
STEP 2: Find ALL hardcoded user-visible strings
        (labels, placeholders, titles, errors, tooltips — skip console.log, URLs, CSS)
STEP 3: node goman-languages.js
STEP 4: Plan keys: namespace = component name, key = descriptive name
        Show plan to user and ask: "Should I proceed?"
STEP 5: After confirmation → node goman-create.js for each key (all languages at once)
STEP 6: Show replacement code snippets:
        Before: <button>Submit</button>
        After:  <button>{t("LoginForm.submitButton")}</button>
```

### 3. Search / Audit Translations

```
STEP 1: node goman-namespaces.js         → understand project structure
STEP 2: node goman-search.js             → filter by namespace or search query
STEP 3: node goman-languages.js          → compare found keys vs active languages
STEP 4: Report missing translations per key
```

### 4. Localize a Folder

```
STEP 1: List files in the folder (ask user if not provided)
STEP 2: For each file: find hardcoded strings
STEP 3: node goman-languages.js
STEP 4: Show full plan across all files, ask confirmation
STEP 5: Batch node goman-create.js calls
STEP 6: Show replacement code for each file
```

## Safety Rules

1. **NEVER** run `goman-delete.js` without explicit user confirmation
2. **ALWAYS** run `goman-languages.js` first — only use language codes it returns
3. **ALWAYS** show what will be affected before destructive actions
4. **ALWAYS** include `context` argument in `goman-create.js` — it helps translators
5. Present results in readable format, never raw JSON

## Detailed Workflows

For complex scenarios, see [workflows.md](./references/workflows.md).
