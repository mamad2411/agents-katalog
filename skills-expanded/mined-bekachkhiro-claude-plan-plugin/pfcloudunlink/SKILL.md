---
name: pfCloudUnlink
description: Disconnect from current PlanFlow cloud project
---

# PlanFlow Cloud Unlink

Disconnect from current PlanFlow cloud project.

## Usage

```bash
/pfCloudUnlink
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

  return { ...globalConfig, ...localConfig, _localConfig: localConfig, _globalConfig: globalConfig }
}

const config = getConfig()
const language = config.language || "en"
const cloudConfig = config.cloud || {}
const isAuthenticated = !!cloudConfig.apiToken
const currentProjectId = cloudConfig.projectId
const apiUrl = cloudConfig.apiUrl || "https://api.planflow.tools"

const t = JSON.parse(readFile(`locales/${language}.json`))
```

## Step 1: Check if Linked

**If not linked:**
```
ℹ️ Not currently linked to any cloud project.

Run: /pfCloudLink to link to a project.
```

## Step 2: Remove Link

**Remove from local config:**
Remove `cloud.projectId` from `.plan-config.json`

**Output:**
```
✅ {t.commands.cloud.unlinked}

Local PROJECT_PLAN.md is now independent.

💡 Run /pfCloudLink to link to a different project.
```
