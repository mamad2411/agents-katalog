---
name: pfWhoami
description: PlanFlow Who Am I
---

# PlanFlow Who Am I

Display current PlanFlow user information and connection status.

## Usage

```bash
/pfWhoami                   # Show current user info
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
const apiUrl = cloudConfig.apiUrl || "https://api.planflow.tools"

const t = JSON.parse(readFile(`locales/${language}.json`))
```

## Step 1: Check Auth Status

If not authenticated:
```
❌ {t.commands.whoami.notLoggedIn}

Run: /pfLogin
```

## Step 2: Get User Info from API

**API Call:**
```bash
curl -s \
  -H "Authorization: Bearer {TOKEN}" \
  "https://api.planflow.tools/auth/me"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "projectCount": 5
  }
}
```

## Step 3: Display Info

```
👤 {t.commands.whoami.title}

  {t.commands.whoami.name} John Doe
  {t.commands.whoami.email} user@example.com
  {t.commands.whoami.userId} uuid
  {t.commands.whoami.apiUrl} https://api.planflow.tools
  {t.commands.whoami.status} ✅ {t.commands.whoami.connected}

📊 {t.commands.whoami.cloudStats}
  {t.commands.whoami.projects} 5
```

## Error Handling

**Token Expired:**
```
❌ Session expired. Please login again.

Run: /pfLogin
```
