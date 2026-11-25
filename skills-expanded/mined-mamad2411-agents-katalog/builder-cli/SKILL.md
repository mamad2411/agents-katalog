---
name: builder-cli
description: "CLI detection and proactive usage patterns for Builder. Use when CLI operations are detected or when suggesting manual configuration. Triggers on: CLI detection, service configuration, deployment commands, secret management."
---

# Builder CLI Detection & Proactive Usage

> Load this skill when: detecting available CLIs, configuring services, managing deployments, or about to suggest manual dashboard configuration.

---

## CLI Detection (with Persistence for Compaction Resilience)

> ⚠️ **CLI state survives context compaction.** This is critical for long PRD sessions.

### Step 1: Check for Persisted CLI State

```bash
# Check if we already have CLI state from a previous detection
CLI_STATE=$(jq -r '.availableCLIs // empty' docs/builder-config.json 2>/dev/null)
CLI_DETECTED_AT=$(echo "$CLI_STATE" | jq -r '.vercel.detectedAt // .gh.detectedAt // empty' 2>/dev/null)
```

### Step 2: Reuse Fresh State (<24h)

If CLI state exists and is fresh (<24h):
- Skip re-detection
- Log: "Restored CLI state from previous session"
- Continue to workflow

### Step 3: Detect CLIs (If No State or Stale)

```bash
# Run in parallel for speed
which vercel && vercel whoami 2>/dev/null
which supabase && supabase projects list 2>/dev/null | head -1
which aws && aws sts get-caller-identity 2>/dev/null | jq -r '.Account'
which gh && gh auth status 2>/dev/null | head -1
which netlify && netlify status 2>/dev/null | head -1
which fly && fly auth whoami 2>/dev/null
which railway && railway whoami 2>/dev/null
which wrangler && wrangler whoami 2>/dev/null
```

### Step 4: Persist to builder-config.json (CRITICAL)

```bash
# Read existing config, add/update availableCLIs, write back
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
jq --arg ts "$TIMESTAMP" '.availableCLIs = {
  "vercel": { "installed": true, "authenticated": true, "user": "team-name", "detectedAt": $ts },
  "supabase": { "installed": true, "authenticated": true, "detectedAt": $ts },
  "gh": { "installed": true, "authenticated": true, "user": "username", "detectedAt": $ts },
  "aws": { "installed": false, "authenticated": false },
  "netlify": { "installed": false, "authenticated": false },
  "fly": { "installed": false, "authenticated": false },
  "railway": { "installed": false, "authenticated": false },
  "wrangler": { "installed": false, "authenticated": false }
}' docs/builder-config.json > docs/builder-config.json.tmp && mv docs/builder-config.json.tmp docs/builder-config.json
```

### Step 5: Show in Dashboard

Show only authenticated CLIs:
```
CLIs: vercel ✓ | supabase ✓ | gh ✓
```

---

## CLI Capabilities Reference

| CLI | Capabilities |
|-----|--------------|
| `vercel` | Deploy, env vars, domains, logs, rollback |
| `supabase` | DB migrations, edge functions, secrets, logs |
| `aws` | S3, Lambda, CloudFormation, SSM params, secrets |
| `gh` | PRs, issues, releases, actions, secrets |
| `netlify` | Deploy, env vars, functions, forms |
| `fly` | Deploy, secrets, logs, scaling |
| `railway` | Deploy, env vars, logs |
| `wrangler` | Workers, KV, R2, secrets |

---

## Proactive CLI Usage (CRITICAL)

> ⛔ **NEVER tell the user to manually configure a service when you have CLI access.**
>
> Before ANY instruction like "Go to [service] dashboard and configure...", check `availableCLIs` in `builder-config.json`. If the CLI is authenticated, **use it directly**.
>
> **Failure behavior:** If you find yourself about to write "Go to Vercel dashboard" or "Configure in Supabase console" — STOP. Check if CLI can do it.

### CLI Replacement Table

| Instead of telling user... | Check CLI | Use command instead |
|---------------------------|-----------|---------------------|
| "Go to Vercel → Domains → Add domain" | `vercel` | `vercel domains add [domain]` |
| "Go to Vercel → Settings → Environment Variables" | `vercel` | `vercel env add [NAME]` / `vercel env ls` |
| "Go to Vercel → Settings → Git → Production Branch" | `vercel` | `vercel project [name] --prod-branch [branch]` |
| "Deploy to Vercel" | `vercel` | `vercel deploy` / `vercel --prod` |
| "Check Vercel deployment status" | `vercel` | `vercel ls` / `vercel inspect [url]` |
| "View Vercel logs" | `vercel` | `vercel logs [deployment]` |
| "Go to Supabase dashboard → SQL Editor" | `supabase` | `supabase db diff` / `supabase db push` |
| "Configure Supabase secrets" | `supabase` | `supabase secrets set [NAME]=[VALUE]` |
| "Check Supabase migration status" | `supabase` | `supabase db status` / `supabase migration list` |
| "Add GitHub secret in Settings" | `gh` | `gh secret set [NAME]` |
| "Create GitHub release" | `gh` | `gh release create [tag]` |
| "Check PR status/checks" | `gh` | `gh pr checks` / `gh pr view` |
| "View GitHub Actions logs" | `gh` | `gh run view [run-id] --log` |
| "Deploy to Netlify" | `netlify` | `netlify deploy` / `netlify deploy --prod` |
| "Configure Netlify env vars" | `netlify` | `netlify env:set [NAME] [VALUE]` |
| "Deploy to Fly.io" | `fly` | `fly deploy` |
| "Set Fly secrets" | `fly` | `fly secrets set [NAME]=[VALUE]` |
| "Deploy to Railway" | `railway` | `railway up` |
| "Set Railway env vars" | `railway` | `railway variables set [NAME]=[VALUE]` |
| "Deploy Cloudflare Worker" | `wrangler` | `wrangler deploy` |
| "Set Cloudflare secrets" | `wrangler` | `wrangler secret put [NAME]` |

### Decision Flow

```
About to tell user to configure something manually?
    │
    ▼
Read availableCLIs from docs/builder-config.json
    │
    ▼
Is the relevant CLI authenticated?
    │
    ├─── YES ──► Use the CLI command directly. Show output.
    │
    └─── NO ──► OK to tell user to configure manually.
                Include: "Tip: Install [cli] to automate this in future"
```

---

## Common CLI Patterns

| Scenario | CLI Solution |
|----------|--------------|
| Setting up staging/preview environments | `vercel env add`, `supabase link` |
| Domain configuration | `vercel domains`, `netlify domains` |
| Checking deployment health | `vercel ls`, `fly status`, `railway status` |
| Debugging deployment failures | `vercel logs`, `fly logs`, `railway logs` |
| Database migrations | `supabase db push`, `supabase migration up` |
| Secret management | `gh secret set`, `fly secrets set`, `vercel env add` |

---

## After CLI Usage

After using any CLI command:

1. **Verify success:** Check exit code is 0
2. **Show output:** Display relevant output to user
3. **Fallback path:** If command fails, THEN suggest manual dashboard approach

```
✅ Command successful: vercel env add API_KEY
   Value set in Production environment

---

❌ Command failed: vercel env add API_KEY
   Error: Not logged in to Vercel team "acme"
   
   Fallback: Go to Vercel dashboard → Settings → Environment Variables → Add API_KEY
   Tip: Run `vercel login` to enable CLI access
```
