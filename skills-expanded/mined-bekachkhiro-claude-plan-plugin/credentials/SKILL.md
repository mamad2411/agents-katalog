# Credential Storage Utility Skill

You are a credential management handler for PlanFlow cloud authentication. Your role is to securely store, retrieve, and clear authentication tokens.

## Objective

Provide a reusable credential management utility for all cloud-related commands to handle token storage and retrieval.

## When to Use

This skill is invoked internally by:
- `/login` - Save credentials after successful authentication
- `/logout` - Clear stored credentials
- `/whoami` - Read credentials to display user info
- `/sync` - Check if authenticated before syncing
- `/cloud` - Check if authenticated before cloud operations

**This is NOT a user-invocable skill.** It's a utility skill used by other commands.

## Storage Locations

Credentials are stored in JSON config files with a hierarchical priority system:

| Priority | Location | Purpose |
|----------|----------|---------|
| 1 (Highest) | `./.plan-config.json` | Project-specific credentials |
| 2 (Default) | `~/.config/claude/plan-plugin-config.json` | Global user credentials |

### Storage Structure

Credentials are stored in the `cloud` section of the config:

```json
{
  "language": "en",
  "cloud": {
    "apiUrl": "https://api.planflow.tools",
    "apiToken": "pf_abc123...",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "userEmail": "user@example.com",
    "userName": "John Doe",
    "tokenName": "My CLI Token",
    "projectId": "abc123",
    "lastSyncedAt": "2026-01-31T15:00:00Z",
    "autoSync": false
  }
}
```

---

## Core Functions

### Function: getConfig

Reads configuration with hierarchical priority (local → global → defaults).

**Pseudo-code:**
```javascript
function getConfig() {
  let config = {}

  // Try local config first (highest priority)
  const localPath = "./.plan-config.json"
  if (fileExists(localPath)) {
    try {
      const localConfig = JSON.parse(readFile(localPath))
      config = { ...config, ...localConfig }
    } catch (error) {
      // Invalid JSON, skip
    }
  }

  // Fall back to global config
  const globalPath = expandPath("~/.config/claude/plan-plugin-config.json")
  if (fileExists(globalPath)) {
    try {
      const globalConfig = JSON.parse(readFile(globalPath))
      // Merge: local overrides global
      config = { ...globalConfig, ...config }
    } catch (error) {
      // Invalid JSON, skip
    }
  }

  // Apply defaults
  return {
    language: "en",
    cloud: {
      apiUrl: "https://api.planflow.tools",
      autoSync: false,
      ...config.cloud
    },
    ...config
  }
}
```

**Bash Implementation:**
```bash
get_config() {
  local LOCAL_CONFIG="./.plan-config.json"
  local GLOBAL_CONFIG="${HOME}/.config/claude/plan-plugin-config.json"

  # Check local first
  if [ -f "$LOCAL_CONFIG" ]; then
    cat "$LOCAL_CONFIG" 2>/dev/null
    return 0
  fi

  # Fall back to global
  if [ -f "$GLOBAL_CONFIG" ]; then
    cat "$GLOBAL_CONFIG" 2>/dev/null
    return 0
  fi

  # Return defaults
  echo '{"language": "en", "cloud": {"apiUrl": "https://api.planflow.tools"}}'
}
```

---

### Function: saveCredentials

Saves authentication credentials to config file.

**Parameters:**
- `credentials` - Object containing token, user info, etc.
- `scope` - Where to save: "local" or "global" (default: "global")

**Pseudo-code:**
```javascript
function saveCredentials(credentials, scope = "global") {
  // Determine target file
  const targetPath = scope === "local"
    ? "./.plan-config.json"
    : expandPath("~/.config/claude/plan-plugin-config.json")

  // Ensure directory exists (for global)
  if (scope === "global") {
    const configDir = expandPath("~/.config/claude")
    if (!directoryExists(configDir)) {
      createDirectory(configDir, { recursive: true })
    }
  }

  // Read existing config or create new
  let config = {}
  if (fileExists(targetPath)) {
    try {
      config = JSON.parse(readFile(targetPath))
    } catch (error) {
      // Invalid JSON, start fresh
      config = {}
    }
  }

  // Merge credentials into cloud section
  config.cloud = {
    ...config.cloud,
    apiToken: credentials.apiToken,
    userId: credentials.userId,
    userEmail: credentials.userEmail,
    userName: credentials.userName,
    tokenName: credentials.tokenName,
    savedAt: new Date().toISOString()
  }

  // Write back
  writeFile(targetPath, JSON.stringify(config, null, 2))

  return {
    success: true,
    path: targetPath,
    scope: scope
  }
}
```

**Bash Implementation:**
```bash
save_credentials() {
  local TOKEN="$1"
  local USER_ID="$2"
  local USER_EMAIL="$3"
  local USER_NAME="$4"
  local TOKEN_NAME="$5"
  local SCOPE="${6:-global}"

  if [ "$SCOPE" = "local" ]; then
    TARGET_PATH="./.plan-config.json"
  else
    TARGET_PATH="${HOME}/.config/claude/plan-plugin-config.json"
    # Ensure directory exists
    mkdir -p "${HOME}/.config/claude"
  fi

  # Read existing or create new
  if [ -f "$TARGET_PATH" ]; then
    EXISTING=$(cat "$TARGET_PATH" 2>/dev/null || echo '{}')
  else
    EXISTING='{}'
  fi

  # Update with jq (or manual JSON manipulation)
  UPDATED=$(echo "$EXISTING" | jq --arg token "$TOKEN" \
    --arg userId "$USER_ID" \
    --arg email "$USER_EMAIL" \
    --arg name "$USER_NAME" \
    --arg tokenName "$TOKEN_NAME" \
    --arg savedAt "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    '.cloud.apiToken = $token |
     .cloud.userId = $userId |
     .cloud.userEmail = $email |
     .cloud.userName = $name |
     .cloud.tokenName = $tokenName |
     .cloud.savedAt = $savedAt')

  echo "$UPDATED" > "$TARGET_PATH"
  echo "Credentials saved to $TARGET_PATH"
}
```

**Without jq (Pure Bash/Read-Edit):**

For Claude, use the Read and Edit tools:
1. Read the target config file
2. Parse the JSON content
3. Update the cloud section with new credentials
4. Write back using Edit or Write tool

---

### Function: getCredentials

Retrieves stored credentials from config.

**Pseudo-code:**
```javascript
function getCredentials() {
  const config = getConfig()

  if (!config.cloud?.apiToken) {
    return null
  }

  return {
    apiToken: config.cloud.apiToken,
    userId: config.cloud.userId,
    userEmail: config.cloud.userEmail,
    userName: config.cloud.userName,
    tokenName: config.cloud.tokenName,
    apiUrl: config.cloud.apiUrl || "https://api.planflow.tools",
    projectId: config.cloud.projectId,
    lastSyncedAt: config.cloud.lastSyncedAt,
    autoSync: config.cloud.autoSync || false
  }
}
```

**Bash Implementation:**
```bash
get_credentials() {
  local CONFIG=$(get_config)

  # Extract token (check if exists)
  local TOKEN=$(echo "$CONFIG" | jq -r '.cloud.apiToken // empty')

  if [ -z "$TOKEN" ]; then
    echo ""
    return 1
  fi

  # Return full credentials object
  echo "$CONFIG" | jq '.cloud'
}
```

---

### Function: getApiToken

Quick helper to get just the API token.

**Pseudo-code:**
```javascript
function getApiToken() {
  const config = getConfig()
  return config.cloud?.apiToken || null
}
```

**Bash Implementation:**
```bash
get_api_token() {
  local CONFIG=$(get_config)
  echo "$CONFIG" | jq -r '.cloud.apiToken // empty'
}
```

---

### Function: clearCredentials

Removes stored credentials from config.

**Parameters:**
- `scope` - Which config to clear: "local", "global", or "all" (default: "all")

**Pseudo-code:**
```javascript
function clearCredentials(scope = "all") {
  const results = []

  // Clear local config
  if (scope === "local" || scope === "all") {
    const localPath = "./.plan-config.json"
    if (fileExists(localPath)) {
      try {
        const config = JSON.parse(readFile(localPath))
        delete config.cloud?.apiToken
        delete config.cloud?.userId
        delete config.cloud?.userEmail
        delete config.cloud?.userName
        delete config.cloud?.tokenName
        delete config.cloud?.savedAt
        // Keep projectId and other settings
        writeFile(localPath, JSON.stringify(config, null, 2))
        results.push({ scope: "local", cleared: true, path: localPath })
      } catch (error) {
        results.push({ scope: "local", cleared: false, error: error.message })
      }
    }
  }

  // Clear global config
  if (scope === "global" || scope === "all") {
    const globalPath = expandPath("~/.config/claude/plan-plugin-config.json")
    if (fileExists(globalPath)) {
      try {
        const config = JSON.parse(readFile(globalPath))
        delete config.cloud?.apiToken
        delete config.cloud?.userId
        delete config.cloud?.userEmail
        delete config.cloud?.userName
        delete config.cloud?.tokenName
        delete config.cloud?.savedAt
        writeFile(globalPath, JSON.stringify(config, null, 2))
        results.push({ scope: "global", cleared: true, path: globalPath })
      } catch (error) {
        results.push({ scope: "global", cleared: false, error: error.message })
      }
    }
  }

  return results
}
```

**Bash Implementation:**
```bash
clear_credentials() {
  local SCOPE="${1:-all}"
  local LOCAL_CONFIG="./.plan-config.json"
  local GLOBAL_CONFIG="${HOME}/.config/claude/plan-plugin-config.json"

  if [ "$SCOPE" = "local" ] || [ "$SCOPE" = "all" ]; then
    if [ -f "$LOCAL_CONFIG" ]; then
      # Remove auth fields but keep other settings
      local UPDATED=$(cat "$LOCAL_CONFIG" | jq 'del(.cloud.apiToken, .cloud.userId, .cloud.userEmail, .cloud.userName, .cloud.tokenName, .cloud.savedAt)')
      echo "$UPDATED" > "$LOCAL_CONFIG"
      echo "Cleared credentials from local config"
    fi
  fi

  if [ "$SCOPE" = "global" ] || [ "$SCOPE" = "all" ]; then
    if [ -f "$GLOBAL_CONFIG" ]; then
      local UPDATED=$(cat "$GLOBAL_CONFIG" | jq 'del(.cloud.apiToken, .cloud.userId, .cloud.userEmail, .cloud.userName, .cloud.tokenName, .cloud.savedAt)')
      echo "$UPDATED" > "$GLOBAL_CONFIG"
      echo "Cleared credentials from global config"
    fi
  fi
}
```

---

### Function: isAuthenticated

Checks if the user is currently authenticated.

**Pseudo-code:**
```javascript
function isAuthenticated() {
  const token = getApiToken()
  return !!token && token.length > 0
}
```

**Bash Implementation:**
```bash
is_authenticated() {
  local TOKEN=$(get_api_token)
  if [ -n "$TOKEN" ]; then
    return 0  # true
  else
    return 1  # false
  fi
}
```

---

### Function: requireAuth

Helper to check authentication and show error if not authenticated.

**Pseudo-code:**
```javascript
function requireAuth(translations) {
  const t = translations

  if (!isAuthenticated()) {
    return {
      authenticated: false,
      error: t.commands.sync.notAuthenticated,
      hint: "/login"
    }
  }

  return {
    authenticated: true,
    credentials: getCredentials()
  }
}
```

**Usage in commands:**
```javascript
// At the start of any cloud command
const authCheck = requireAuth(t)
if (!authCheck.authenticated) {
  console.log(authCheck.error)
  console.log(`\n💡 Run: ${authCheck.hint}`)
  return
}

// Continue with authenticated operations
const { credentials } = authCheck
// ...
```

---

### Function: getCredentialSource

Determines where credentials are stored (for display purposes).

**Pseudo-code:**
```javascript
function getCredentialSource() {
  const localPath = "./.plan-config.json"
  const globalPath = expandPath("~/.config/claude/plan-plugin-config.json")

  // Check local first
  if (fileExists(localPath)) {
    try {
      const config = JSON.parse(readFile(localPath))
      if (config.cloud?.apiToken) {
        return { source: "local", path: localPath }
      }
    } catch (error) {}
  }

  // Check global
  if (fileExists(globalPath)) {
    try {
      const config = JSON.parse(readFile(globalPath))
      if (config.cloud?.apiToken) {
        return { source: "global", path: globalPath }
      }
    } catch (error) {}
  }

  return { source: null, path: null }
}
```

---

### Function: maskToken

Masks a token for display (security).

**Pseudo-code:**
```javascript
function maskToken(token) {
  if (!token || token.length < 12) {
    return "***"
  }
  // Show prefix and last 4 chars
  const prefix = token.substring(0, 8)
  const suffix = token.substring(token.length - 4)
  return `${prefix}...${suffix}`
}

// Example: "pf_abc12345xyz" → "pf_abc12...xyz"
```

**Bash Implementation:**
```bash
mask_token() {
  local TOKEN="$1"
  if [ ${#TOKEN} -lt 12 ]; then
    echo "***"
    return
  fi
  local PREFIX="${TOKEN:0:8}"
  local SUFFIX="${TOKEN: -4}"
  echo "${PREFIX}...${SUFFIX}"
}
```

---

### Function: updateProjectLink

Updates the linked cloud project ID.

**Parameters:**
- `projectId` - The cloud project ID to link (or null to unlink)
- `scope` - Where to save: "local" or "global" (default: "local")

**Pseudo-code:**
```javascript
function updateProjectLink(projectId, scope = "local") {
  const targetPath = scope === "local"
    ? "./.plan-config.json"
    : expandPath("~/.config/claude/plan-plugin-config.json")

  let config = {}
  if (fileExists(targetPath)) {
    try {
      config = JSON.parse(readFile(targetPath))
    } catch (error) {
      config = {}
    }
  }

  if (!config.cloud) {
    config.cloud = {}
  }

  if (projectId) {
    config.cloud.projectId = projectId
  } else {
    delete config.cloud.projectId
  }

  writeFile(targetPath, JSON.stringify(config, null, 2))

  return {
    success: true,
    projectId: projectId,
    path: targetPath
  }
}
```

---

### Function: updateLastSyncedAt

Updates the last sync timestamp.

**Pseudo-code:**
```javascript
function updateLastSyncedAt(timestamp = new Date().toISOString()) {
  // Prefer updating local config if it exists and has projectId
  const localPath = "./.plan-config.json"
  const globalPath = expandPath("~/.config/claude/plan-plugin-config.json")

  let targetPath = globalPath
  if (fileExists(localPath)) {
    try {
      const localConfig = JSON.parse(readFile(localPath))
      if (localConfig.cloud?.projectId) {
        targetPath = localPath
      }
    } catch (error) {}
  }

  let config = {}
  if (fileExists(targetPath)) {
    try {
      config = JSON.parse(readFile(targetPath))
    } catch (error) {
      config = {}
    }
  }

  if (!config.cloud) {
    config.cloud = {}
  }

  config.cloud.lastSyncedAt = timestamp

  writeFile(targetPath, JSON.stringify(config, null, 2))

  return { success: true, timestamp: timestamp }
}
```

---

## Usage Examples

### Example 1: Login Command

```javascript
// After successful token verification from API
const userInfo = apiResponse.user
const tokenInfo = apiResponse.token

saveCredentials({
  apiToken: inputToken,
  userId: userInfo.id,
  userEmail: userInfo.email,
  userName: userInfo.name,
  tokenName: tokenInfo.name
}, scope)  // "local" or "global" based on --local/--global flag

console.log(t.commands.login.success)
console.log(`  ${t.commands.login.user} ${userInfo.name}`)
console.log(`  ${t.commands.login.email} ${userInfo.email}`)
```

### Example 2: Logout Command

```javascript
// Clear credentials
const results = clearCredentials(scope)

for (const result of results) {
  if (result.cleared) {
    console.log(t.commands.logout.cleared.replace("{scope}", result.scope))
  }
}

console.log(t.commands.logout.success)
```

### Example 3: Whoami Command

```javascript
const credentials = getCredentials()

if (!credentials) {
  console.log(t.commands.whoami.notLoggedIn)
  console.log(t.commands.whoami.loginHint)
  return
}

const source = getCredentialSource()

console.log(t.commands.whoami.title)
console.log(`  ${t.commands.whoami.name} ${credentials.userName}`)
console.log(`  ${t.commands.whoami.email} ${credentials.userEmail}`)
console.log(`  ${t.commands.whoami.userId} ${credentials.userId}`)
console.log(`  ${t.commands.whoami.apiUrl} ${credentials.apiUrl}`)
console.log(`  Token: ${maskToken(credentials.apiToken)}`)
console.log(`  Source: ${source.source} (${source.path})`)
```

### Example 4: Check Auth Before Sync

```javascript
// At start of /sync command
if (!isAuthenticated()) {
  console.log(t.commands.sync.notAuthenticated)
  console.log("\n💡 Run: /login")
  return
}

// Get credentials for API calls
const credentials = getCredentials()
const projectId = credentials.projectId

if (!projectId) {
  console.log(t.commands.sync.notLinked)
  console.log("\n💡 Run: /cloud link")
  return
}

// Continue with sync...
```

---

## Claude Implementation Guide

When implementing credential operations in commands, use the following approach:

### Reading Config Files

Use the **Read** tool to read config files:
```
Read tool: ./.plan-config.json (local)
Read tool: ~/.config/claude/plan-plugin-config.json (global)
```

If the file doesn't exist, the Read tool will return an error - treat this as "no config".

### Writing Config Files

Use the **Write** tool to write updated config:
```
Write tool: target path, JSON content
```

For global config, ensure the directory exists first. You may need to check/create `~/.config/claude/` directory.

### Parsing JSON

Parse the JSON content from the Read tool output:
- Extract the `cloud` section
- Check for `apiToken` to determine authentication status
- Extract user info fields as needed

### Updating JSON

When updating config:
1. Read existing config
2. Parse JSON
3. Modify the `cloud` section
4. Preserve other fields (language, etc.)
5. Write back with proper formatting (2-space indent)

---

## Security Considerations

1. **Plain Text Storage**: Tokens are stored in plain text (standard for CLI tools like gh, aws-cli, etc.)

2. **Token Masking**: Never display full tokens in output - always use `maskToken()`

3. **File Permissions**: Config files should be readable only by the user:
   ```bash
   chmod 600 ~/.config/claude/plan-plugin-config.json
   ```

4. **No Command Line Tokens**: Never pass tokens as command arguments (visible in process list)

5. **Secure Deletion**: When clearing credentials, actually remove the fields, don't just set to empty

---

## Error Handling

### File Not Found
```javascript
// Not an error - just means no credentials stored
if (!fileExists(configPath)) {
  return null  // Not authenticated
}
```

### Invalid JSON
```javascript
try {
  config = JSON.parse(content)
} catch (error) {
  // Log warning, treat as no config
  console.warn("Config file corrupted, will be reset on next save")
  return {}
}
```

### Write Errors
```javascript
try {
  writeFile(path, content)
} catch (error) {
  return {
    success: false,
    error: "Cannot write config file. Check permissions."
  }
}
```

---

## Integration Checklist

When using this skill in commands:

- [ ] Call `isAuthenticated()` before cloud operations
- [ ] Use `requireAuth(t)` for consistent error messages
- [ ] Use `maskToken()` when displaying tokens
- [ ] Update `lastSyncedAt` after successful sync
- [ ] Respect `--local` and `--global` flags for credential scope
- [ ] Handle missing credentials gracefully
- [ ] Show helpful hints when not authenticated

---

## Important Notes

1. **This is an internal skill** - not user-invocable
2. **Hierarchical priority** - local config overrides global
3. **Preserve non-auth fields** - when clearing credentials, keep language, autoSync, etc.
4. **Project linking is separate** - projectId can exist without auth (for /cloud link)
5. **Always mask tokens** - never show full token in any output

This skill provides the foundation for credential management across all cloud commands.
