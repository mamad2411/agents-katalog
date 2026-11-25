---
name: pfCloudList
description: List all cloud projects in your PlanFlow account
---

# PlanFlow Cloud List

List all cloud projects in your PlanFlow account.

## Usage

```bash
/pfCloudList
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

## Step 1: Validate Authentication

If not authenticated:
```
❌ {t.commands.sync.notAuthenticated}

Run: /pfLogin
```

## Step 2: List Projects

**API Call:**
```bash
curl -s \
  -H "Authorization: Bearer {TOKEN}" \
  "https://api.planflow.tools/projects"
```

**Output:**
```
📁 {t.commands.cloud.listProjects}

  ID        Name              Tasks    Progress
  ────────  ────────────────  ───────  ──────────
  abc123    E-commerce App    24/45    53%
  def456    Mobile API        12/18    67%
  ghi789    Dashboard         8/12     75%

  ✓ Current: abc123 (E-commerce App)

💡 Commands:
  /pfCloudLink <id>     Link to a project
  /pfCloudUnlink        Disconnect current
  /pfCloudNew           Create new project
```

## Error Handling

**Network Error:**
```
❌ Network error. Please check your connection.
```
