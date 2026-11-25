---
name: pfLogout
description: PlanFlow Logout
---

# PlanFlow Logout

Clear PlanFlow credentials and disconnect from cloud.

**IMPORTANT:** This is ONLY for PlanFlow (planflow.tools) - NOT for Claude or Claude Code logout.

## Usage

```bash
/pfLogout                   # Clear credentials
```

## Step 0: Load Configuration

```javascript
function getConfig() {
  const globalConfigPath = expandPath("~/.config/claude/plan-plugin-config.json")
  if (fileExists(globalConfigPath)) {
    try {
      return JSON.parse(readFile(globalConfigPath))
    } catch (error) {}
  }
  return { "language": "en" }
}

const config = getConfig()
const language = config.language || "en"
const cloudConfig = config.cloud || {}
const isAuthenticated = !!cloudConfig.apiToken

const t = JSON.parse(readFile(`locales/${language}.json`))
```

## Step 1: Check Auth Status

If not authenticated:
```
ℹ️ {t.commands.logout.notLoggedIn}
```

## Step 2: Clear Credentials

Remove from global config (`~/.config/claude/plan-plugin-config.json`):
- `cloud.apiToken`
- `cloud.userId`
- `cloud.userEmail`

Keep other settings like `language` and `cloud.apiUrl`.

## Step 3: Show Success

```
✅ {t.commands.logout.success}

{t.commands.logout.cleared}
```
