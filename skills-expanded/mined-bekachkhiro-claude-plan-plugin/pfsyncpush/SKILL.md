---
name: pfSyncPush
description: Push local PROJECT_PLAN.md to PlanFlow cloud
---

# PlanFlow Sync Push

Push local PROJECT_PLAN.md to PlanFlow cloud.

## Usage

```bash
/pfSyncPush                 # Push local → cloud
/pfSyncPush --force         # Overwrite cloud without confirmation
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

## Step 3: Push to Cloud

**IMPORTANT: Follow these steps exactly!**

1. Read PROJECT_PLAN.md using the Read tool
2. Create JSON payload using Bash with jq
3. Make API call and parse response
4. Show task count from response
5. Update lastSyncedAt in config

**Step 3a: Create JSON payload**
```bash
cat PROJECT_PLAN.md > /tmp/plan_content.txt
jq -n --rawfile plan /tmp/plan_content.txt '{"plan": $plan}' > /tmp/payload.json
```

**Step 3b: Make API call**
```bash
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {TOKEN}" \
  -d @/tmp/payload.json \
  "https://api.planflow.tools/projects/{PROJECT_ID}/plan")

# Separate body and status code
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

echo "HTTP Status: $HTTP_CODE"
echo "Response: $BODY"
```

**Step 3c: Parse response - CRITICAL!**

**IMPORTANT**: You MUST parse the JSON response to extract and display the task count!

The API returns:
```json
{
  "success": true,
  "data": {
    "projectId": "uuid",
    "projectName": "My Project",
    "tasksCount": 15,
    "completedCount": 3,
    "progress": 20
  }
}
```

**Use jq or manual parsing to extract values:**
```bash
# Extract values from response
TASKS_COUNT=$(echo "$BODY" | jq -r '.data.tasksCount')
COMPLETED_COUNT=$(echo "$BODY" | jq -r '.data.completedCount')
PROGRESS=$(echo "$BODY" | jq -r '.data.progress')
PROJECT_NAME=$(echo "$BODY" | jq -r '.data.projectName')

echo "Tasks: $TASKS_COUNT, Completed: $COMPLETED_COUNT, Progress: $PROGRESS%"
```

**You MUST extract and display:**
- `tasksCount` - Number of tasks parsed from the plan
- `completedCount` - Number of completed tasks
- `progress` - Progress percentage (0-100)

**Success output (MUST show task count):**
```
✅ {t.commands.sync.pushSuccess}

📊 Sync Details:
   Project: {projectName}
   Tasks synced: {tasksCount}
   Completed: {completedCount}
   Progress: {progress}%

🕐 Synced at: {timestamp}
```

**If tasksCount is 0 or null:**
```
⚠️ Warning: No tasks were parsed from the plan.

This could mean:
- The plan format is not recognized
- Tasks should use format: #### T1.1: Task Name
- Or table format: | T1.1 | Task Name | Low | TODO | - |

Run /planNext to verify your plan format.
```

## Step 4: Update Local Config

After successful sync, update `.plan-config.json` with the sync timestamp:

```javascript
// Read current config
const configPath = "./.plan-config.json"
let config = {}
if (fileExists(configPath)) {
  config = JSON.parse(readFile(configPath))
}

// Update lastSyncedAt
if (!config.cloud) config.cloud = {}
config.cloud.lastSyncedAt = new Date().toISOString()

// Write back
writeFile(configPath, JSON.stringify(config, null, 2))
```

## Error Handling

**No PROJECT_PLAN.md:**
```
❌ {t.commands.sync.noPlan}

Run: /planNew to create a plan first.
```

**HTTP 401 - Unauthorized:**
```
❌ Authentication failed. Your token may have expired.

Run: /pfLogin to re-authenticate.
```

**HTTP 404 - Project not found:**
```
❌ Project not found on cloud.

The linked project may have been deleted.
Run: /pfCloudLink to link a different project.
```

**Network Error:**
```
❌ Network error. Please check your connection.
```
