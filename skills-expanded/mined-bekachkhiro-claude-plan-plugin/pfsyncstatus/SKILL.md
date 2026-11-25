---
name: pfSyncStatus
description: Show synchronization status between local and PlanFlow cloud
---

# PlanFlow Sync Status

Show synchronization status between local PROJECT_PLAN.md and PlanFlow cloud.

## Usage

```bash
/pfSyncStatus
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

## Step 1: Validate Prerequisites

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

## Step 2: Show Sync Status

Show comparison between local and cloud:

```
📊 {t.commands.sync.status}

  {t.commands.sync.localFile} PROJECT_PLAN.md (modified 5 min ago)
  {t.commands.sync.cloudProject} My Project (synced 2 hours ago)
  {t.commands.sync.syncStatus} {t.commands.sync.localAhead}

  {t.commands.sync.changes}
    • 2 tasks completed locally
    • 1 task description changed

  💡 Run: /pfSyncPush
```

## Error Handling

**Network Error:**
```
❌ Network error. Please check your connection.
```
