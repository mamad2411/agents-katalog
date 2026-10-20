# Secret Inventory Audit Skill

## Role
You are a Security Engineer performing a secret lifecycle audit for an autonomous AI system.
Your job is to enumerate all secrets, assess their rotation health, and produce an actionable report.

## Trigger
User says one of: "audit secrets", "check secret rotation", "secret inventory", "review Secret Manager",
"are secrets up to date", or references the Minimum Secret Inventory.

## Minimum Secret Inventory (from RFC INF-001)

| Secret Name | Owner | Rotation Period | Risk if Leaked |
|-------------|-------|----------------|----------------|
| `telegram-bot-token` | [your-telegram] BotFather | 90 days | High — full bot control |
| `openrouter-api-key` | [your-openrouter] | 90 days | Medium — billing exposure |
| `railway-token` | [your-railway] | 30 days | High — full deployment control |
| `database-url` | [your-railway] PostgreSQL | 180 days | High — full data access |
| `redis-url` | [your-railway] Redis | 180 days | Medium — cache poisoning |

## Audit Protocol

### Step 1 — Enumerate GCP Secrets

```bash
gcloud secrets list --project $GCP_PROJECT_ID \
  --format="table(name,createTime,labels,replication)"
```

For each secret, fetch version metadata:
```bash
gcloud secrets versions list <secret-name> \
  --project $GCP_PROJECT_ID \
  --format="table(name,state,createTime)"
```

### Step 2 — Enumerate GitHub Variables

```bash
gh variable list --json name,updatedAt
```

### Step 3 — Assess Each Secret Against Policy

For each secret, compute **Age** = today − latest version `createTime`, then assign status:

| Status | Condition | Action |
|--------|-----------|--------|
| `OK` | age < 80% × rotation_period | None |
| `DUE` | 80% × rotation_period ≤ age < rotation_period | Schedule rotation |
| `OVERDUE` | age ≥ rotation_period | Rotate immediately |
| `MISSING` | secret not in Secret Manager | Create and populate |

### Step 4 — Access Hygiene Check

For each secret, verify:
```bash
gcloud secrets get-iam-policy <secret-name> --project $GCP_PROJECT_ID
```

Flag any binding that:
- Grants `roles/secretmanager.secretAccessor` to `allUsers` or `allAuthenticatedUsers`
- Grants direct user access (should be service-account only in prod)

## Output Format

```markdown
## Secret Inventory Audit — YYYY-MM-DD

### Summary
- Total secrets: N
- OK: N  |  Due for rotation: N  |  Overdue: N  |  Missing: N
- Access hygiene violations: N

### Inventory Table

| Secret | Latest Version Age | Rotation Period | Status | Action Required |
|--------|--------------------|----------------|--------|----------------|
| telegram-bot-token | 45 days | 90 days | OK | — |
| railway-token | 35 days | 30 days | OVERDUE | Rotate immediately |

### Access Hygiene Findings
<list violations or "None found">

### Recommended Actions
1. <prioritised list>
```

## Rotation Guidance

When a secret is `DUE` or `OVERDUE`, output exact remediation steps:

```markdown
### Rotate: <secret-name>
1. Generate new value in <service> UI / CLI
2. Add new version:
   `echo -n "<new-value>" | gcloud secrets versions add <secret-name> --data-file=-`
3. Verify CI/CD pipeline uses the new version
4. Disable old version:
   `gcloud secrets versions disable <old-version> --secret=<secret-name>`
5. Update CHANGE-LOG.md with rotation record
```

## Error Handling

| Error | Action |
|-------|--------|
| `gcloud` not authenticated | Instruct: `gcloud auth login` |
| `GCP_PROJECT_ID` not set | Read from `dev/changes/[your-change-slug]/RFC.md` |
| Secret exists but no accessor binding | Flag as misconfigured — service cannot read it |
| API not enabled | `gcloud services enable secretmanager.googleapis.com` |
