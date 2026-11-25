---
name: deploy-vercel-cloudflare
description: Deploy to Vercel and bind a Cloudflare subdomain. Use when the user wants to deploy a project, set up a custom domain, or any combination of deployment and DNS steps.
---

# Deploy to Vercel + Cloudflare Domain

Deploy a project to Vercel and configure a custom domain via Cloudflare DNS.

## Prerequisites

Verify CLI tools are authenticated before starting:

```bash
gh auth status        # GitHub CLI
vercel whoami         # Vercel CLI (if expired: vercel login --github)
```

If any tool is not logged in, run the corresponding login command first.

## Supported Domains

| Domain | Cloudflare API Token Env Var |
|--------|------------------------------|
| `xzd.me` | `CLOUDFLARE_API_TOKEN_XZD_ME` |
| `synaix-lab.com` | `CLOUDFLARE_API_TOKEN_SYNAIX_LAB_COM` |

Run `source ~/.zshrc` if the env var is not available in the current shell.

## Workflow

### Step 1: Determine Subdomain

The user MUST specify or approve a subdomain before proceeding.

If the user hasn't specified one, suggest based on the project/directory name under both domains:

```
Suggested subdomains:
- <name>.xzd.me
- <name>.synaix-lab.com

Which one would you like? Or specify your own.
```

**Do NOT proceed until the user explicitly confirms.**

From the confirmed subdomain (e.g., `example.synaix-lab.com`):
- **Vercel project name** = first segment (e.g., `example`)
- **Root domain** = base domain (e.g., `synaix-lab.com`)
- **Cloudflare API token** = corresponding env var

### Step 2: Push to GitHub (if needed)

Skip if the repo is already on GitHub.

```bash
git add -A
git commit -m "feat: initial commit"
gh repo create <repo-name> --private --source=. --push --description "<description>"
```

### Step 3: Deploy to Vercel

The Vercel project name MUST match the first segment of the subdomain (e.g., `example.xzd.me` → project name `example`).

```bash
# Remove existing .vercel config if creating a new project
rm -rf .vercel

# Deploy with explicit project name
vercel deploy --name <subdomain-first-segment> -y --no-wait --scope xuzuodongs-projects
```

If the project already exists and the user just wants to redeploy:
```bash
vercel deploy -y --no-wait --scope xuzuodongs-projects
```

### Step 4: Bind Cloudflare Subdomain

#### 4a. Add custom domain to Vercel project

```bash
vercel domains add <full-subdomain> --scope xuzuodongs-projects
```

#### 4b. Create CNAME record in Cloudflare

```bash
# 1. Ensure env var is available
source ~/.zshrc

# 2. Get zone ID (replace TOKEN_VAR and ROOT_DOMAIN)
ZONE_ID=$(curl -s "https://api.cloudflare.com/client/v4/zones?name=<root-domain>" \
  -H "Authorization: Bearer $<TOKEN_VAR>" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data['result'][0]['id'])
")

# 3. Create CNAME record (DNS only, not proxied)
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $<TOKEN_VAR>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CNAME",
    "name": "<subdomain-prefix>",
    "content": "cname.vercel-dns.com",
    "ttl": 1,
    "proxied": false
  }'
```

**Important**: Set `proxied: false` (DNS only / grey cloud) to let Vercel handle SSL.

#### 4c. Verify

```bash
dig <full-subdomain> CNAME +short
# Should return: cname.vercel-dns.com.
```

### Step 5: Report Results

Show the user:
- Vercel project name and dashboard URL
- Custom domain
- Deployment status (`vercel inspect <url> --scope xuzuodongs-projects`)
- Remind about environment variables if the build fails

## Partial Execution

The user may only need a subset of steps. Each step is independent — skip steps that are already done or not requested:

- "Deploy to Vercel" → Steps 3 only
- "Add a domain" → Step 4 only
- "Create and push to GitHub" → Step 2 only
- "Full setup" → All steps

## Error Handling

- If `vercel whoami` fails → ask user to run `vercel login`
- If Cloudflare API token env var is empty → run `source ~/.zshrc` and retry; if still empty, ask user to set it
- If DNS record creation returns auth error → token may lack DNS write permissions
- If Vercel project name is taken → ask user for alternative subdomain
