---
name: pfLogin
description: PlanFlow Login
---

# PlanFlow Login

Authenticate with PlanFlow project management service.

**IMPORTANT:** This is ONLY for PlanFlow (planflow.tools) - NOT for Claude or Claude Code authentication.

## Usage

```bash
/pfLogin                    # Interactive - prompts for token
/pfLogin pf_abc123...       # Direct token input
```

## Step 0: Load Configuration

```javascript
function getConfig() {
  const localConfigPath = "./.plan-config.json"
  if (fileExists(localConfigPath)) {
    try {
      return JSON.parse(readFile(localConfigPath))
    } catch (error) {}
  }
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

## Step 1: Check Current Auth Status

If already authenticated, show message and exit:
```
⚠️ Already logged in as {email}

To switch accounts, run /pfLogout first.
```

## Step 2: Get Token

If token provided as argument, use it.
Otherwise, ask user:
```
{t.commands.login.enterToken}

Get your token at: https://planflow.tools/settings/api-tokens
```

## Step 3: Validate Token

**API Call:**
```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"token": "{TOKEN}"}' \
  "https://api.planflow.tools/api-tokens/verify"
```

**IMPORTANT:** The token must be passed in the **request body** as JSON, NOT in the Authorization header!

**Success Response (HTTP 200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "tokenName": "My CLI Token"
  }
}
```

**Error Response (HTTP 401):**
```json
{
  "success": false,
  "error": "Invalid API token"
}
```

## Step 4: Save Credentials

Save to global config (`~/.config/claude/plan-plugin-config.json`):

**IMPORTANT:**
- Create the directory if it doesn't exist: `mkdir -p ~/.config/claude`
- Use the Write tool to save the config file

```json
{
  "language": "en",
  "cloud": {
    "apiUrl": "https://api.planflow.tools",
    "apiToken": "pf_xxx...",
    "savedAt": "2026-02-02T12:00:00Z",
    "verified": true,
    "userId": "uuid-from-response",
    "userEmail": "email-from-response",
    "userName": "name-from-response"
  }
}
```

## Step 5: Show Success

After successful verification, extract user info from response:
- `response.data.user.name` - User's name
- `response.data.user.email` - User's email
- `response.data.user.id` - User's ID
- `response.data.tokenName` - Token name (note: it's `tokenName`, not `token.name`)

Then show:
```
✅ {t.commands.login.success}

  {t.commands.login.user} {response.data.user.name}
  {t.commands.login.email} {response.data.user.email}
  {t.commands.login.token} {response.data.tokenName}

{t.commands.login.nowYouCan}
  • /pfSyncPush - Push local to cloud
  • /pfSyncPull - Pull from cloud
  • /pfCloudList - List your projects
```

## Error Handling

**Invalid Token:**
```
❌ {t.commands.login.invalidToken}

Get a new token at: https://planflow.tools/settings/api-tokens
```

**Network Error:**
```
❌ Network error. Please check your connection.
```
