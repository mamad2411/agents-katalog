---
name: pfCloudLink
description: Link local directory to a PlanFlow cloud project
---

# PlanFlow Cloud Link

Link local directory to a PlanFlow cloud project.

## Usage

```bash
/pfCloudLink                # Interactive project selection
/pfCloudLink <project-id>   # Link to specific project
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

## Step 1: Parse Arguments

```javascript
const projectIdArg = commandArgs.trim()  // project ID if provided
```

## Step 2: Validate Authentication

If not authenticated:
```
❌ {t.commands.sync.notAuthenticated}

Run: /pfLogin
```

## Step 3: Select Project

**If no ID provided:**
Show project list and use AskUserQuestion to select:
```javascript
AskUserQuestion({
  questions: [{
    question: t.commands.cloud.selectProject,
    header: "Project",
    multiSelect: false,
    options: projects.map(p => ({
      label: p.name,
      description: `ID: ${p.id} | ${p.tasksDone}/${p.tasksTotal} tasks`
    }))
  }]
})
```

**If ID provided:**
Verify project exists via API call.

## Step 4: Save Link

**Save to local config (`.plan-config.json`):**
```json
{
  "cloud": {
    "projectId": "selected-uuid"
  }
}
```

**Success:**
```
✅ {t.commands.cloud.linked}

  Project: E-commerce App
  ID: abc123

💡 Run /pfSyncPull to download the plan
   or /pfSyncPush to upload your local plan
```

## Error Handling

**Project not found:**
```
❌ Project not found: {id}

Run: /pfCloudList to see available projects.
```

**Already linked:**
```
⚠️ Already linked to: {projectName}

Run: /pfCloudUnlink first to switch projects.
```
