---
name: pfCloudNew
description: Create a new cloud project in PlanFlow
---

# PlanFlow Cloud New

Create a new cloud project in PlanFlow.

## Usage

```bash
/pfCloudNew                 # Create from local plan (uses plan name)
/pfCloudNew "Project Name"  # Create with custom name
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
const apiUrl = cloudConfig.apiUrl || "https://api.planflow.tools"

const t = JSON.parse(readFile(`locales/${language}.json`))
```

## Step 1: Parse Arguments

```javascript
const projectName = commandArgs.trim().replace(/^["']|["']$/g, '') || null
```

## Step 2: Validate Authentication

If not authenticated:
```
❌ {t.commands.sync.notAuthenticated}

Run: /pfLogin
```

## Step 3: Check for PROJECT_PLAN.md

1. Check if PROJECT_PLAN.md exists
2. Extract project name from plan (or use argument)

**If no PROJECT_PLAN.md:**
```
❌ {t.commands.cloud.noPlan}

Run: /planNew to create a plan first.
```

## Step 4: Create Project

**API Call:**
```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {TOKEN}" \
  -d '{"name": "Project Name"}' \
  "https://api.planflow.tools/projects"
```

## Step 5: Link and Push

1. Link to new project (save projectId to config)
2. Push current plan

**Success:**
```
✅ {t.commands.cloud.created}

  Project: My New Project
  ID: xyz789

📤 Pushing local plan to cloud...

✅ {t.commands.sync.pushSuccess}

💡 Your project is now synced!
   View at: https://app.planflow.tools/projects/xyz789
```

## Error Handling

**API Error:**
```
❌ Failed to create project. Please try again.
```
