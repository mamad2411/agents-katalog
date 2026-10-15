---
name: verify-complete
description: "Evidence-based completion check before claims persist to persistent state, session notes, or roadmap. Use BEFORE writes that say items are done, BEFORE answering 'how much is done?', or before any multi-item completion claim."
user-invocable: true
---

# Verify Complete — Evidence-Based Completion Check

Prevents overclaiming by requiring code-level evidence for each claimed feature. Run this BEFORE the claim hits a persistence layer (persistent state files, session notes, roadmap tracking) — once it's written, it propagates to future sessions unchallenged.

## When to Use

Pre-claim, not post-claim:

- BEFORE writing to persistent state files (any "Active Now" entry, completion status)
- BEFORE writing session notes that claim items are complete
- BEFORE updating roadmap item status in any tracking system
- BEFORE answering "how much of X is done?" / "is the feature ready?"
- After implementing a multi-item feature checklist
- When reporting status to stakeholders

Even one false "done" claim poisons your persistent state and propagates into future sessions.

**Note**: If your harness has a Stop hook that catches single-turn deploy claims (e.g. "deployed and verified" with no evidence command in the same turn), that handles simple cases. This skill handles the heavier case: multi-item checklists, persistent-state writes, status reports.

## Verification Recipes by Claim Type

Different claims need different evidence. Pick the recipe that matches the claim shape — generic "grep for it" is not enough for deploys, schema changes, or cron triggers.

### Deploy claim ("deployed and verified", "shipped to dev/prod")

```bash
# Verify the live endpoint returns expected content
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://{{your-app}}.example.com/api/health"
```

Pass criteria: HTTP 200 + JSON body. HTML response = auth redirect (auth issue). 5xx = function bundle missing or crashed.

### CI claim ("CI passed", "tests green", "workflow succeeded")

```bash
gh run list --branch <branch> --limit 3 --json databaseId,status,conclusion,name
```

Pass criteria: all recent runs show `status=completed`, `conclusion=success`. In-progress runs do not count — wait or use the Monitor tool.

### Database migration claim ("migration applied", "schema updated")

```bash
npx wrangler d1 execute {{your-d1-db}} --remote \
  --command="SELECT name FROM d1_migrations ORDER BY id DESC LIMIT 5"
```

Pass criteria: the new migration filename appears in the result. Empty result or older names only = migration did not actually apply.

### Worker cron claim ("cron registered", "schedule active", "trigger live")

```bash
# Use your platform's API to verify the schedule registration timestamp
# For Cloudflare Workers, check the CF API schedules endpoint:
ACCT_ID=<cf-account-id>
TOKEN=<oauth-token>
curl -s -H "Authorization: Bearer ${TOKEN}" \
  "https://api.cloudflare.com/client/v4/accounts/${ACCT_ID}/workers/scripts/{{your-worker}}/schedules"
```

Pass criteria: `modified_on` >= the time of your last deploy. If `modified_on` is older than your deploy, the trigger is silently stuck — re-register with PUT [] then PUT [{...}]. The deploy tool's "Deployed triggers" output is NOT proof on its own.

### UI feature claim ("button works", "modal renders", "label updated")

Use chrome-devtools MCP — `new_page` → `navigate_page` → `take_screenshot` of the specific component. HTTP 200 and unit tests don't prove what the user sees. Visual verification is mandatory for any UI label/render change. Note: the same label is often rendered in multiple places (sidebar, page header, document title, tab labels, breadcrumbs) — grep ALL render sites before claiming a label change is done.

### Feature checklist item ("idea N is done", "X of Y features shipped")

```bash
grep -rn "<feature-keyword>" <project>/src/ --include="*.jsx" --include="*.js"
```

Pass criteria: at least one of [file path, JSX render site, state hook, API call]. Help-text-only = `[DOCUMENTED ONLY]`, not `[VERIFIED]`. CSS without JSX = `[PARTIAL]`.

### Schema/code change claim ("alert wires up", "logic updated")

```bash
# Smoke-test the relevant endpoint
curl -s -X POST -H "Authorization: Bearer ${AUTH_TOKEN}" \
  "https://{{your-app}}.example.com/api/{{endpoint}}/run"
# Confirm the action was logged in your audit table
npx wrangler d1 execute {{your-d1-db}} --remote \
  --command="SELECT * FROM audit_log ORDER BY id DESC LIMIT 3"
```

Pass criteria: 200 from the endpoint AND a fresh row in the audit log. 200 alone doesn't prove the action happened — only the audit row does.

### Shared-component scope claim ("affects X projects", "lands in project-a + project-b")

When a change in `shared/` is described as touching multiple projects, verify each project actually *imports* the symbol — being in `shared/` means it's available, not that every project consumes it. Grep for the import before claiming scope:

```bash
# Find every project that imports the shared symbol (replace SymbolName)
grep -rln "import.*SymbolName.*from.*shared\|from '@your-shared.*SymbolName" \
  project-a/src/ project-b/src/ project-c/src/ --include="*.{js,jsx,ts,tsx}" \
  2>/dev/null
```

Pass criteria: at least one import line per project named in the claim. Empty result for a named project = the change has no practical effect there, even though the file lives in `shared/`. Update the claim to match consumer reality before persisting it.

### RBAC / permission claim ("X has access", "role granted")

```bash
npx wrangler d1 execute {{your-d1-db}} --remote \
  --command="SELECT email, role, granted_at FROM user_roles WHERE email='<user>'"
```

Pass criteria: row exists with the expected role. Any KV fallback for auth must also be checked if D1 is empty.

### Multi-item completion ("X of Y items done")

Run Steps 1-6 below. Do not skip Step 1 (listing claims explicitly) — that's where overcounting is caught.

## Steps

### 1. List Claims

Write out each feature being claimed as complete:
```
1. [CLAIMED] Search input in grid view
2. [CLAIMED] Color legend button
3. [CLAIMED] Product filter dropdown
...
```

### 2. Code Verification (Per Feature)

For each claimed feature, provide evidence:

```bash
# Search for the implementation
grep -r "searchText\|search-input\|filterText" project/src/ --include="*.jsx" --include="*.js" -l
```

Evidence categories:
- **Component exists**: File path + key JSX snippet
- **State wired**: useState/useEffect for the feature
- **UI renders**: JSX that produces visible output
- **API connected**: fetch/endpoint call if needed
- **CSS styled**: Relevant class names exist

Mark each as:
- `[VERIFIED]` — code exists, renders, connected
- `[PARTIAL]` — code exists but incomplete (missing CSS, no API, etc.)
- `[NOT FOUND]` — claimed but no code evidence
- `[DOCUMENTED ONLY]` — help text exists but no implementation

### 3. Build Verification

```bash
cd <project> && npm run build
```

Build passing does NOT mean features work — it only means no syntax errors.

### 4. Lint Verification

```bash
cd <project> && npm run lint
```

### 5. Visual Verification (if Playwright available)

Take screenshots of the feature in action. If auth blocks access, note it and verify via code instead.

### 6. Report Honest Status

```
## Feature Verification Report

| # | Feature | Code | Build | Visual | Status |
|---|---------|------|-------|--------|--------|
| 1 | Search  | Found in Dashboard.jsx:45 | PASS | N/A | VERIFIED |
| 2 | Legend  | NOT FOUND | - | - | NOT DONE |
| 3 | Filter  | Found but missing dropdown JSX | PASS | - | PARTIAL |
```

### 7. Correct Persistent State

If any items were previously claimed as done but are NOT VERIFIED:
- Update persistent state files to correct the status
- Update session notes if they contain false claims
- Update roadmap items if they were marked completed

## Anti-Patterns

- NEVER mark something as complete based on memory alone — always grep for code
- NEVER count help documentation as implementation
- NEVER count CSS without corresponding JSX as complete
- NEVER claim "done" without running build at minimum
- NEVER report X/Y completion without evidence for each X item

## Evidence Levels

| Level | Meaning | Required Evidence |
|-------|---------|-------------------|
| Verified | Feature works end-to-end | Code + build + visual or API test |
| Code Complete | Implementation exists | Code + build pass |
| Partial | Some pieces exist | Code exists but gaps identified |
| Not Done | No implementation | Grep returns empty or docs-only |
