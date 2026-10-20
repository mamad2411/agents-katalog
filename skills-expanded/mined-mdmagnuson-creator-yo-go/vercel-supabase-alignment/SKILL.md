---
name: vercel-supabase-alignment
description: "Verify that Vercel environment variables point to the correct Supabase project for each environment to prevent staging/production cross-wiring. Triggers on: vercel supabase check, environment alignment, env var check, supabase environment."
---

# Vercel-Supabase Environment Alignment Check

## Purpose

Verify that Vercel environment variables point to the correct Supabase project for each environment. This prevents the common issue where staging deployments accidentally connect to production databases (or vice versa).

## Triggers

Load this skill when:

- Database schema error in a deployed app (e.g., "column does not exist")
- User mentions "wrong database", "env vars", "schema mismatch"
- After applying migrations that don't take effect on a deployed environment
- User reports an issue in a specific app environment (e.g., "error in Helm Dev")
- Discrepancy between local migration state and deployed app behavior

## Prerequisites

- `vercel` CLI installed and authenticated (`vercel whoami` succeeds)
- `supabase` CLI installed (optional, for local link verification)
- Project has `environments` configured in `docs/project.json` with `database` objects

## Environment Detection

### Step 1: Identify the Environment from User Context

When the user reports an issue, map their context to an environment:

| User Says | Likely Environment | Look Up |
|-----------|-------------------|---------|
| "Helm Dev", "dev app", "staging app" | staging | `environments.staging.desktop.appName` |
| "Helm", "prod app", "production app" | production | `environments.production.desktop.appName` |
| "localhost", "local", "my machine" | development | `environments.development` |
| API URL like `*-api.vercel.app` | staging | `environments.staging.apiUrl` |
| API URL like `api.example.com` | production | `environments.production.apiUrl` |

**Detection algorithm:**

```bash
# Read project.json to get environment config
PROJECT_JSON=$(cat docs/project.json)

# Try to match user context to environment
# 1. Check desktop app names
# 2. Check API URLs
# 3. Check branch names
# 4. Ask user if ambiguous
```

### Step 2: Look Up Expected Database

Once environment is identified, read expected database from `project.json`:

```bash
# For staging:
jq -r '.environments.staging.database.projectRef' docs/project.json
jq -r '.environments.staging.database.projectName' docs/project.json

# For production:
jq -r '.environments.production.database.projectRef' docs/project.json
jq -r '.environments.production.database.projectName' docs/project.json
```

## Vercel Environment Check

### Step 3: Get Vercel Environment Variables

```bash
# List all env vars for the Vercel project
vercel env ls

# Get specific Supabase-related vars by environment
# Note: Vercel uses "production", "preview", "development"

# For Preview (typically maps to staging):
vercel env pull .env.preview --environment=preview --yes 2>/dev/null
grep -E "SUPABASE|DATABASE" .env.preview

# For Production:
vercel env pull .env.production --environment=production --yes 2>/dev/null
grep -E "SUPABASE|DATABASE" .env.production

# Clean up
rm -f .env.preview .env.production
```

### Step 4: Extract Supabase Project Ref from URL

Supabase URLs contain the project ref:

```
https://[PROJECT_REF].supabase.co
```

**Parse the project ref:**

```bash
# Extract project ref from SUPABASE_URL or NEXT_PUBLIC_SUPABASE_URL
SUPABASE_URL=$(grep SUPABASE_URL .env.preview | cut -d= -f2)
ACTUAL_REF=$(echo "$SUPABASE_URL" | sed -E 's|https://([^.]+)\.supabase\.co.*|\1|')
echo "Actual project ref: $ACTUAL_REF"
```

### Step 5: Compare Expected vs Actual

```bash
EXPECTED_REF=$(jq -r '.environments.staging.database.projectRef' docs/project.json)
ACTUAL_REF="[extracted from Vercel env]"

if [ "$EXPECTED_REF" != "$ACTUAL_REF" ]; then
  echo "⚠️ MISMATCH DETECTED"
  echo "Expected: $EXPECTED_REF"
  echo "Actual: $ACTUAL_REF"
fi
```

## Common Issues and Fixes

### Issue: Vercel "Production" Environment Used for Main Branch

**Problem:** Vercel defaults `main` branch deployments to use "Production" environment variables, but the project uses `main` for staging and `production` branch for actual production.

**Detection:**

```bash
# Check Vercel project settings
vercel inspect --scope [team] | grep -A5 "Production Branch"
```

**Fix options:**

1. **Change Vercel production branch** (recommended):
   ```bash
   # In Vercel dashboard: Settings → Git → Production Branch → "production"
   # Or via API/CLI if supported
   ```

2. **Use Preview for main branch:**
   Configure main branch deployments to use Preview env vars.

3. **Create explicit environment mapping:**
   Use Vercel's branch-specific env vars feature.

### Issue: Local Supabase Link Points to Wrong Project

**Problem:** `supabase link` was run against production instead of staging.

**Detection:**

```bash
# Check which project is linked locally
cat supabase/.temp/project-ref 2>/dev/null || supabase status
```

**Fix:**

```bash
# Re-link to correct project
supabase link --project-ref [CORRECT_PROJECT_REF]
```

### Issue: Migration Applied to Wrong Database

**Problem:** Migration ran successfully but app still shows "column not found".

**Diagnosis:**

1. Verify migration was applied to expected database:
   ```bash
   # Check which database the migration was applied to
   supabase db remote status
   ```

2. Compare with app's actual database:
   ```bash
   # Get app's database from Vercel env
   vercel env pull .env.check --environment=preview --yes
   grep SUPABASE_URL .env.check
   ```

3. If different, apply migration to correct database:
   ```bash
   # Switch to correct project and apply
   supabase link --project-ref [CORRECT_REF]
   supabase db push
   ```

## Diagnostic Report Format

When running alignment check, output this report:

```
═══════════════════════════════════════════════════════════════════════
                  ENVIRONMENT ALIGNMENT CHECK
═══════════════════════════════════════════════════════════════════════

PROJECT: [Project Name]
CHECK TIME: [Timestamp]

ENVIRONMENT MAPPING (from project.json)
───────────────────────────────────────────────────────────────────────
  Environment    Branch       Database Project      Desktop App
  ─────────────  ───────────  ──────────────────    ───────────
  staging        main         Helm (rvuy...)        Helm Dev
  production     production   helm-prod (hiuh...)   Helm

VERCEL ENVIRONMENT VARIABLES
───────────────────────────────────────────────────────────────────────
  Vercel Env    SUPABASE_URL Project Ref    Expected    Status
  ──────────    ───────────────────────     ────────    ──────
  preview       rvuylmblhafnryfdlnkj        rvuy...     ✅ MATCH
  production    hiuhimcmmqdeeyhvdkrb        hiuh...     ✅ MATCH

LOCAL SUPABASE LINK
───────────────────────────────────────────────────────────────────────
  Linked to: rvuylmblhafnryfdlnkj (Helm - staging)  ✅ CORRECT

VERCEL BRANCH CONFIGURATION
───────────────────────────────────────────────────────────────────────
  Production Branch: production  ✅ CORRECT
  
  Branch → Env Mapping:
    main branch → Preview env vars
    production branch → Production env vars

RESULT: ✅ All environments aligned correctly
═══════════════════════════════════════════════════════════════════════
```

Or if issues found:

```
═══════════════════════════════════════════════════════════════════════
                  ENVIRONMENT ALIGNMENT CHECK
═══════════════════════════════════════════════════════════════════════

...

RESULT: ❌ MISALIGNMENT DETECTED

Issues Found:
  1. ⚠️ Vercel preview env points to PRODUCTION database
     Expected: rvuylmblhafnryfdlnkj (staging)
     Actual: hiuhimcmmqdeeyhvdkrb (production)
     
     FIX: Update SUPABASE_URL in Vercel Preview environment:
     vercel env rm SUPABASE_URL preview
     vercel env add SUPABASE_URL preview
     → Enter: https://rvuylmblhafnryfdlnkj.supabase.co

  2. ⚠️ Vercel production branch is set to 'main'
     Expected: 'production'
     
     FIX: Go to Vercel Dashboard → Settings → Git → Production Branch
     Change from 'main' to 'production'

═══════════════════════════════════════════════════════════════════════
```

## Integration with Builder Error Diagnosis

When Builder encounters a database error:

1. **Identify environment** from user's error context
2. **Load this skill** to run alignment check
3. **If misalignment found**, report the issue and fix instructions
4. **If aligned**, the issue is likely a genuine missing migration

This prevents the common mistake of applying migrations to the wrong database.

## Preventive Checks

### Pre-Migration Check

Before running `supabase db push` or migration commands:

```bash
# Verify we're pushing to the intended environment
LINKED_REF=$(cat supabase/.temp/project-ref 2>/dev/null)
STAGING_REF=$(jq -r '.environments.staging.database.projectRef' docs/project.json)
PROD_REF=$(jq -r '.environments.production.database.projectRef' docs/project.json)

if [ "$LINKED_REF" = "$PROD_REF" ]; then
  echo "⚠️ WARNING: About to push migrations to PRODUCTION database"
  echo "Press Ctrl+C to cancel, or Enter to continue"
  read
fi
```

### Post-Deployment Check

After deploying to Vercel, verify the deployment uses correct env vars:

```bash
# Get the deployment URL
DEPLOY_URL=$(vercel ls --json | jq -r '.[0].url')

# Check which database it's using (if app exposes this info)
# Or verify by testing a known staging-only vs prod-only data point
```
