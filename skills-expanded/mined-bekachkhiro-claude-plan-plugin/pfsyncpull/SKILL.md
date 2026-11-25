---
name: pfSyncPull
description: Pull plan from PlanFlow cloud to local PROJECT_PLAN.md
---

# PlanFlow Sync Pull

Pull plan from PlanFlow cloud to local PROJECT_PLAN.md.

## Usage

```bash
/pfSyncPull                 # Pull cloud → local
/pfSyncPull --force         # Overwrite local without confirmation
```

## Step 0: Load Configuration

```javascript
function getConfig() {
  const localConfigPath = "./.plan-config.json"
  let localConfig = {}
  if (fileExists(localConfigPath)) {
    try { localConfig = JSON.parse(readFile(localConfigPath)) } catch {}
  }

  const globalConfigPath = expandPath("~/.config/claude/plan-plugin-config.json")
  let globalConfig = {}
  if (fileExists(globalConfigPath)) {
    try { globalConfig = JSON.parse(readFile(globalConfigPath)) } catch {}
  }

  return { ...globalConfig, ...localConfig }
}

const config = getConfig()
const language = config.language || "en"
const cloudConfig = config.cloud || {}
const isAuthenticated = !!cloudConfig.apiToken
const projectId = cloudConfig.projectId
const apiUrl = cloudConfig.apiUrl || "https://api.planflow.tools"

const t = JSON.parse(readFile(`locales/${language}.json`))
```

## Step 1: Parse Arguments

```javascript
const args = commandArgs.trim().split(/\s+/)
const forceFlag = args.includes("--force")
```

## Step 2: Validate Prerequisites

**Not authenticated:**
```
❌ {t.commands.sync.notAuthenticated}

Run: /pfLogin
```

**Not linked to project:**
```
❌ {t.commands.sync.notLinked}

Run: /pfCloudLink
```

## Step 3: Pull from Cloud

1. GET plan from API
2. Show diff if local exists (unless --force)
3. Write to PROJECT_PLAN.md

**API Call:**
```bash
curl -s \
  -H "Authorization: Bearer {TOKEN}" \
  "https://api.planflow.tools/projects/{PROJECT_ID}/plan"
```

**If local exists and differs (without --force):**
```
⚠️ {t.commands.sync.localChanges}

{t.commands.sync.diff}
  - Task T1.1: IN_PROGRESS → DONE (local)
  + Task T1.2: Added description (cloud)

{t.commands.sync.confirmPull}
```

Use AskUserQuestion to confirm.

**Success:**
```
✅ {t.commands.sync.pullSuccess}

  {t.commands.sync.downloaded} PROJECT_PLAN.md
  {t.commands.sync.from} My Project
  {t.commands.sync.at} 2024-01-15 14:30:00
```

## Error Handling

**Network Error:**
```
❌ Network error. Please check your connection.
```
