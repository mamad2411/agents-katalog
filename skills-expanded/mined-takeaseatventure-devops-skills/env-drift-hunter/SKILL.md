---
name: env-drift-hunter
description: Detect environment variable drift across .env files before deploy. Use when a user has multiple .env files (.env, .env.local, .env.staging, .env.production), when debugging "works on my machine" config issues, or when setting up a new environment. Scans 12 languages (Node, Python, Ruby, Go, Rust, Java, PHP, Docker, shell, YAML, TOML, JS/TS) to find where env vars are actually used and flags missing/extra/changed values across environments.
---

# env-drift-hunter

## When to use this skill

- A user has two or more `.env` files and wants to compare them.
- A user is debugging "works locally, breaks in prod" — almost always env drift.
- A user is deploying to a new environment and needs to verify all required vars are set.
- A user is onboarding a new developer and wants to generate a `.env.example`.
- A user asks "what environment variables does this project actually use?"

Environment drift is the #1 cause of "works on my machine" failures. A variable
that's set in `.env.local` but missing in `.env.production` — or worse, set to a
different value — causes silent failures, wrong API endpoints, and 3am pages.

## How env drift happens

```
.env.local           .env.staging         .env.production
─────────────        ─────────────        ─────────────────
DATABASE_URL=...     DATABASE_URL=...     DATABASE_URL=...     ✓ same
REDIS_URL=...        REDIS_URL=...        (missing)           ✗ MISSING in prod
LOG_LEVEL=debug      LOG_LEVEL=info       LOG_LEVEL=warn      ~ CHANGED
API_KEY=dev_xxx      API_KEY=stg_xxx      (missing)           ✗ MISSING in prod
STRIPE_KEY=          STRIPE_KEY=sk_...    STRIPE_KEY=sk_live  ~ CHANGED
NEW_FEATURE_FLAG=1   (missing)           (missing)           ✗ ONLY in local
```

The dangerous ones are **missing in prod** (the app crashes) and **changed** (the app
points to the wrong service). Extra-in-local is less dangerous but causes confusion.

## How to hunt drift

### Step 1: Find all .env files

```bash
# All env files in the project (excluding node_modules, .git)
find . -name ".env*" -not -path "*/node_modules/*" -not -path "*/.git/*" | sort
```

Common patterns: `.env`, `.env.local`, `.env.development`, `.env.staging`,
`.env.production`, `.env.test`, `.env.example`, `.env.defaults`.

### Step 2: Parse and compare

For each `.env` file, extract the variable names and values. Compare them:

- **Missing**: present in one file but not another → potential crash in the missing env.
- **Extra**: present only in one file → may be a stale var or a new var not yet deployed.
- **Changed**: same name, different value → verify this is intentional (e.g. different
  API endpoints per environment is normal; different LOG_LEVEL might be a mistake).

**Parsing rules:**
- `KEY=VALUE` — standard
- `KEY="VALUE"` / `KEY='VALUE'` — quoted values (strip quotes)
- `export KEY=VALUE` — shell-style (strip `export`)
- `# comment` — ignore (but note commented-out vars, they may be intentionally disabled)
- Empty value `KEY=` is different from missing `KEY` — an empty value means "explicitly
  set to nothing", missing means "not set at all."

### Step 3: Find what the code actually uses (12-language scan)

Don't just compare files — find which env vars the codebase actually references. A var
in `.env` that no code reads is dead config. A var that code reads but isn't in `.env`
will crash at runtime.

**Language-specific env var reference patterns:**

| Language | Pattern | Example |
|----------|---------|---------|
| Node.js | `process.env.KEY` | `process.env.DATABASE_URL` |
| Python | `os.environ['KEY']` / `os.getenv('KEY')` | `os.getenv('API_KEY')` |
| Ruby | `ENV['KEY']` | `ENV['STRIPE_SECRET']` |
| Go | `os.Getenv("KEY")` | `os.Getenv("PORT")` |
| Rust | `env::var("KEY")` / `env!("KEY")` | `env::var("DATABASE_URL")` |
| Java | `System.getenv("KEY")` | `System.getenv("JWT_SECRET")` |
| PHP | `getenv('KEY')` / `$_ENV['KEY']` | `getenv('API_KEY')` |
| Dockerfile | `ENV KEY=value` / `ARG KEY` | `ENV NODE_ENV=production` |
| Shell | `$KEY` / `${KEY}` | `${DATABASE_URL}` |
| YAML/CI | `${{ secrets.KEY }}` / `${KEY}` | `${{ secrets.DOCKER_PASSWORD }}` |
| TOML | in `[env]` or inline | `database_url = "..."` |
| JS/TS (Vite) | `import.meta.env.KEY` / `VITE_KEY` | `import.meta.env.VITE_API_URL` |

**Regex for finding all env var references across a codebase:**
```
process\.env\.([A-Z_][A-Z0-9_]*)
os\.(?:environ|getenv)\(?['"]([A-Z_][A-Z0-9_]*)['"]\)?
ENV\[(['"]?[A-Z_][A-Z0-9_]*)['"]?\]
os\.Getenv\("([A-Z_][A-Z0-9_]*)"\)
env(?:!)?::var\("([A-Z_][A-Z0-9_]*)"\)
System\.getenv\("([A-Z_][A-Z0-9_]*)"\)
getenv\(['"]([A-Z_][A-Z0-9_]*)['"]\)
\$\{?\{([A-Z_][A-Z0-9_]*)\}?
```

### Step 4: Generate the drift report

Present the results as a clear diff table:

```
Variable              .env.local     .env.staging   .env.production    Status
───────────────────── ────────────── ────────────── ────────────────── ────────
DATABASE_URL          ✓ postgres://… ✓ postgres://… ✓ postgres://…     ✓ same
REDIS_URL             ✓ redis://…    ✓ redis://…    ✗ MISSING          ⚠️ MISSING
LOG_LEVEL             = debug        = info         = warn             ~ changed
API_KEY               ✓ dev_xxx      ✓ stg_xxx      ✗ MISSING          ⚠️ MISSING
SENTRY_DSN            ✗ missing      ✗ missing      ✓ https://…        ◯ prod-only
NEW_FEATURE_FLAG      = 1            ✗ missing      ✗ missing          ◯ local-only
DEPRECATED_VAR        ✓ (commented)  ✓ old_value    ✓ old_value        💀 dead code

Code references found but not in ANY .env file:
  → JWT_SECRET (used in src/auth.js:42)
  → SMTP_PASSWORD (used in src/email.js:18)

In .env files but no code reference found:
  → LEGACY_API_KEY (dead config, safe to remove)
```

## Common pitfalls to flag

1. **Secrets in `.env.example`**: `.env.example` should have placeholder values
   (`STRIPE_KEY=sk_test_xxx`), never real secrets. If you see a real-looking key,
   flag it — it may have been committed by mistake.

2. **Production secrets in local `.env`**: if `.env.local` contains `sk_live_...`
   (live Stripe key) or a production database URL, that's a security risk. Developers
   should use test/sandbox keys locally.

3. **Commented-out vars**: `# DATABASE_URL=...` means the var is disabled. This is
   different from the var being absent. Commented vars may indicate a feature that was
   toggled off and forgotten.

4. **`.env` committed to git**: check `.gitignore`. If `.env` is NOT in `.gitignore`,
   real secrets may be in git history. Run `git log --all -- .env` to check.

5. **Empty vs missing**: `KEY=` (empty string) behaves differently from the key being
   entirely absent. Code like `if (process.env.FEATURE_FLAG)` will be falsy for empty
   string, but `process.env.FEATURE_FLAG ?? 'default'` will use empty string not default.

## Generating `.env.example`

When generating a `.env.example` from a real `.env`:

1. Copy all variable **names**, keep the structure.
2. Replace all **values** with descriptive placeholders: `DATABASE_URL=postgres://user:pass@host:5432/db`
3. Detect **sensitive keys** by name pattern: `*KEY*`, `*SECRET*`, `*PASSWORD*`, `*TOKEN*`, `*CREDENTIAL*`
   and add a comment: `# Keep this secret — never commit the real value`
4. Add type hints as comments: `# boolean: set to "true" or "false"`
5. Group related vars: database, cache, auth, feature-flags.
