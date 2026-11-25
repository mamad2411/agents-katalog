# API Client Skill

You are an HTTP client handler for PlanFlow cloud API communication. Your role is to make authenticated API requests and handle responses.

## Objective

Provide a reusable HTTP client for all cloud-related commands to communicate with `api.planflow.tools`.

## When to Use

This skill is invoked internally by:
- `/login` - Token verification
- `/logout` - (No API call, just config)
- `/whoami` - Get user info
- `/sync` - Push/pull project plans
- `/cloud` - List/manage cloud projects

**This is NOT a user-invocable skill.** It's a utility skill used by other commands.

## Configuration

### Base URL

Read from config hierarchy:

```javascript
function getApiUrl() {
  const config = getConfig()  // From Step 0 pattern
  return config.cloud?.apiUrl || "https://api.planflow.tools"
}
```

### Authentication Token

Read from config:

```javascript
function getApiToken() {
  const config = getConfig()
  return config.cloud?.apiToken || null
}
```

## Core Functions

### Function: makeRequest

Makes an authenticated HTTP request to the PlanFlow API.

**Parameters:**
- `method` - HTTP method (GET, POST, PUT, DELETE)
- `endpoint` - API endpoint path (e.g., "/projects")
- `data` - Optional request body (for POST/PUT)
- `requiresAuth` - Whether to include Bearer token (default: true)

**Pseudo-code:**
```javascript
function makeRequest(method, endpoint, data = null, requiresAuth = true) {
  const baseUrl = getApiUrl()
  const token = getApiToken()
  const url = `${baseUrl}${endpoint}`

  // Build curl command
  let curlCmd = `curl -s -w "\\n%{http_code}" -X ${method}`
  curlCmd += ` -H "Content-Type: application/json"`
  curlCmd += ` -H "Accept: application/json"`

  if (requiresAuth && token) {
    curlCmd += ` -H "Authorization: Bearer ${token}"`
  }

  if (data && (method === "POST" || method === "PUT")) {
    // Escape data for shell
    const escapedData = JSON.stringify(data).replace(/'/g, "'\\''")
    curlCmd += ` -d '${escapedData}'`
  }

  curlCmd += ` "${url}"`

  // Execute and parse response
  const output = bash(curlCmd)
  const lines = output.trim().split("\n")
  const statusCode = parseInt(lines.pop())
  const body = lines.join("\n")

  return {
    status: statusCode,
    body: body ? JSON.parse(body) : null,
    ok: statusCode >= 200 && statusCode < 300
  }
}
```

**Bash Implementation:**

```bash
# Variables (set before calling)
API_URL="https://api.planflow.tools"
API_TOKEN="pf_xxx..."
ENDPOINT="/projects"
METHOD="GET"
DATA=""  # JSON string for POST/PUT

# Build and execute curl
RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X "$METHOD" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  ${DATA:+-d "$DATA"} \
  "${API_URL}${ENDPOINT}")

# Parse response
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Check success
if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "Success: $BODY"
else
  echo "Error ($HTTP_CODE): $BODY"
fi
```

## API Endpoints

### Authentication Endpoints

#### POST /api-tokens/verify

Verify that an API token is valid.

**Request:**
```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  "${API_URL}/api-tokens/verify"
```

**Success Response (200):**
```json
{
  "valid": true,
  "token": {
    "id": "uuid",
    "name": "My CLI Token",
    "createdAt": "2026-01-15T10:00:00Z",
    "lastUsedAt": "2026-01-31T14:30:00Z"
  },
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Error Response (401):**
```json
{
  "error": "Invalid or expired token",
  "code": "INVALID_TOKEN"
}
```

---

#### GET /auth/me

Get current authenticated user information.

**Request:**
```bash
curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "${API_URL}/auth/me"
```

**Success Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2026-01-01T00:00:00Z",
  "stats": {
    "projectCount": 5,
    "totalTasks": 127,
    "completedTasks": 89
  }
}
```

---

### Project Endpoints

#### GET /projects

List all projects for the authenticated user.

**Request:**
```bash
curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "${API_URL}/projects"
```

**Success Response (200):**
```json
{
  "projects": [
    {
      "id": "abc123",
      "name": "E-commerce App",
      "createdAt": "2026-01-10T00:00:00Z",
      "updatedAt": "2026-01-31T12:00:00Z",
      "stats": {
        "totalTasks": 45,
        "completedTasks": 24,
        "progress": 53
      }
    },
    {
      "id": "def456",
      "name": "Mobile API",
      "createdAt": "2026-01-20T00:00:00Z",
      "updatedAt": "2026-01-30T09:00:00Z",
      "stats": {
        "totalTasks": 18,
        "completedTasks": 12,
        "progress": 67
      }
    }
  ],
  "total": 2
}
```

---

#### POST /projects

Create a new project.

**Request:**
```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "My New Project", "description": "Optional description"}' \
  "${API_URL}/projects"
```

**Success Response (201):**
```json
{
  "id": "ghi789",
  "name": "My New Project",
  "description": "Optional description",
  "createdAt": "2026-01-31T15:00:00Z",
  "updatedAt": "2026-01-31T15:00:00Z",
  "stats": {
    "totalTasks": 0,
    "completedTasks": 0,
    "progress": 0
  }
}
```

---

#### GET /projects/:id

Get project details.

**Request:**
```bash
curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "${API_URL}/projects/${PROJECT_ID}"
```

**Success Response (200):**
```json
{
  "id": "abc123",
  "name": "E-commerce App",
  "description": "Full-stack e-commerce platform",
  "createdAt": "2026-01-10T00:00:00Z",
  "updatedAt": "2026-01-31T12:00:00Z",
  "stats": {
    "totalTasks": 45,
    "completedTasks": 24,
    "inProgressTasks": 3,
    "blockedTasks": 1,
    "progress": 53
  },
  "phases": [
    {"number": 1, "name": "Foundation", "progress": 100},
    {"number": 2, "name": "Core Features", "progress": 60},
    {"number": 3, "name": "Advanced", "progress": 0}
  ]
}
```

**Error Response (404):**
```json
{
  "error": "Project not found",
  "code": "PROJECT_NOT_FOUND"
}
```

---

#### GET /projects/:id/plan

Get the PROJECT_PLAN.md content for a project.

**Request:**
```bash
curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "${API_URL}/projects/${PROJECT_ID}/plan"
```

**Success Response (200):**
```json
{
  "content": "# Project Name\n\n## Overview\n...",
  "updatedAt": "2026-01-31T12:00:00Z",
  "hash": "sha256:abc123..."
}
```

---

#### PUT /projects/:id/plan

Update/upload PROJECT_PLAN.md content.

**Request:**
```bash
curl -s -X PUT \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"content": "# Project Name\n\n## Overview\n..."}' \
  "${API_URL}/projects/${PROJECT_ID}/plan"
```

**Success Response (200):**
```json
{
  "success": true,
  "updatedAt": "2026-01-31T15:30:00Z",
  "hash": "sha256:def456...",
  "stats": {
    "totalTasks": 16,
    "completedTasks": 5,
    "progress": 31
  }
}
```

**Conflict Response (409):**
```json
{
  "error": "Plan has been modified on the server",
  "code": "CONFLICT",
  "serverHash": "sha256:xyz789...",
  "serverUpdatedAt": "2026-01-31T15:00:00Z"
}
```

---

#### GET /projects/:id/tasks

Get parsed task list from a project.

**Request:**
```bash
curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "${API_URL}/projects/${PROJECT_ID}/tasks"
```

**Success Response (200):**
```json
{
  "tasks": [
    {
      "id": "T1.1",
      "name": "Project Setup",
      "status": "DONE",
      "complexity": "Low",
      "phase": 1,
      "dependencies": []
    },
    {
      "id": "T1.2",
      "name": "Database Setup",
      "status": "IN_PROGRESS",
      "complexity": "Medium",
      "phase": 1,
      "dependencies": ["T1.1"]
    }
  ],
  "total": 16,
  "stats": {
    "done": 5,
    "inProgress": 1,
    "blocked": 0,
    "todo": 10
  }
}
```

---

#### PUT /projects/:id/tasks

Bulk update task statuses.

**Request:**
```bash
curl -s -X PUT \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "updates": [
      {"id": "T1.2", "status": "DONE"},
      {"id": "T1.3", "status": "IN_PROGRESS"}
    ]
  }' \
  "${API_URL}/projects/${PROJECT_ID}/tasks"
```

**Success Response (200):**
```json
{
  "success": true,
  "updated": 2,
  "stats": {
    "done": 6,
    "inProgress": 1,
    "blocked": 0,
    "todo": 9,
    "progress": 37
  }
}
```

---

#### PATCH /projects/:id/tasks/:taskId

Update a single task's status (used by hybrid sync).

**Request:**
```bash
curl -s -X PATCH \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status": "DONE"}' \
  "${API_URL}/projects/${PROJECT_ID}/tasks/${TASK_ID}"
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "projectId": "abc123",
    "projectName": "My Project",
    "task": {
      "id": "uuid",
      "taskId": "T1.1",
      "name": "Project Setup",
      "status": "DONE",
      "complexity": "Low",
      "dependencies": [],
      "updatedAt": "2026-02-01T12:00:00Z",
      "updatedBy": "user@example.com"
    }
  }
}
```

---

#### GET /projects/:id/tasks/:taskId

Get a single task's current state (used for pull-before-push).

**Request:**
```bash
curl -s -X GET \
  -H "Authorization: Bearer $TOKEN" \
  "${API_URL}/projects/${PROJECT_ID}/tasks/${TASK_ID}"
```

**Success Response (200):**
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "uuid",
      "taskId": "T1.1",
      "name": "Project Setup",
      "status": "IN_PROGRESS",
      "complexity": "Low",
      "dependencies": [],
      "createdAt": "2026-01-15T10:00:00Z",
      "updatedAt": "2026-01-31T14:30:00Z",
      "updatedBy": "teammate@example.com"
    }
  }
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": "Task not found",
  "code": "TASK_NOT_FOUND"
}
```

---

## Task Comparison Helpers (v1.3.0)

These helper functions support the hybrid sync pull-before-push pattern.

### Function: compareTaskStates

Compares local and cloud task states to determine sync action.

**Pseudo-code:**
```javascript
/**
 * Compare local and cloud task states
 * @param {Object} params - Comparison parameters
 * @param {string} params.taskId - Task identifier (e.g., "T1.1")
 * @param {string} params.localStatus - New local status (DONE, IN_PROGRESS, BLOCKED)
 * @param {string} params.localUpdatedAt - Local update timestamp (ISO 8601)
 * @param {string} params.localUpdatedBy - Local update source ("local")
 * @param {string} params.cloudStatus - Current cloud status
 * @param {string} params.cloudUpdatedAt - Cloud update timestamp (ISO 8601)
 * @param {string} params.cloudUpdatedBy - Who updated on cloud (email or "system")
 * @param {string} params.lastSyncedAt - Last successful sync timestamp (ISO 8601)
 * @returns {Object} Comparison result
 */
function compareTaskStates(params) {
  const {
    taskId,
    localStatus,
    localUpdatedAt,
    localUpdatedBy,
    cloudStatus,
    cloudUpdatedAt,
    cloudUpdatedBy,
    lastSyncedAt
  } = params

  // Normalize statuses for comparison
  const normalizedLocal = normalizeStatus(localStatus)
  const normalizedCloud = normalizeStatus(cloudStatus)

  // Case 1: Same status - no conflict, no need to push
  if (normalizedLocal === normalizedCloud) {
    return {
      result: "NO_CONFLICT",
      reason: "same_status",
      action: "skip",
      message: `Both local and cloud have status: ${normalizedLocal}`
    }
  }

  // Case 2: No lastSyncedAt - first sync, local takes precedence
  if (!lastSyncedAt) {
    return {
      result: "NO_CONFLICT",
      reason: "first_sync",
      action: "push",
      message: "First sync - pushing local changes"
    }
  }

  // Case 3: Cloud hasn't changed since last sync - safe to push
  const lastSyncTime = new Date(lastSyncedAt).getTime()
  const cloudUpdateTime = new Date(cloudUpdatedAt).getTime()

  if (cloudUpdateTime <= lastSyncTime) {
    return {
      result: "NO_CONFLICT",
      reason: "cloud_unchanged",
      action: "push",
      message: "Cloud unchanged since last sync - safe to push"
    }
  }

  // Case 4: Cloud changed after our last sync - CONFLICT
  return {
    result: "CONFLICT",
    reason: "concurrent_modification",
    action: "resolve",
    taskId,
    local: {
      status: normalizedLocal,
      updatedAt: localUpdatedAt,
      updatedBy: localUpdatedBy
    },
    cloud: {
      status: normalizedCloud,
      updatedAt: cloudUpdatedAt,
      updatedBy: cloudUpdatedBy
    },
    message: `Conflict: local=${normalizedLocal}, cloud=${normalizedCloud}`
  }
}

/**
 * Normalize status string for comparison
 */
function normalizeStatus(status) {
  if (!status) return "TODO"
  const normalized = status.toUpperCase().trim()

  // Handle status with emoji suffixes
  if (normalized.includes("DONE") || normalized.includes("✅")) return "DONE"
  if (normalized.includes("IN_PROGRESS") || normalized.includes("🔄")) return "IN_PROGRESS"
  if (normalized.includes("BLOCKED") || normalized.includes("🚫")) return "BLOCKED"
  if (normalized.includes("TODO")) return "TODO"

  return normalized
}
```

---

### Function: shouldPullBeforePush

Determines if pull-before-push is needed based on config.

**Pseudo-code:**
```javascript
/**
 * Check if hybrid sync (pull-before-push) is enabled
 * @param {Object} config - Merged config object
 * @returns {boolean} Whether to use hybrid sync
 */
function shouldPullBeforePush(config) {
  const cloudConfig = config.cloud || {}

  // Check authentication
  if (!cloudConfig.apiToken) return false

  // Check project link
  if (!cloudConfig.projectId) return false

  // Check storage mode
  const storageMode = cloudConfig.storageMode || "local"

  return storageMode === "hybrid"
}
```

---

### Function: getCloudTaskState

Fetches current task state from cloud.

**Pseudo-code:**
```javascript
/**
 * Fetch task state from cloud
 * @param {string} projectId - Cloud project ID
 * @param {string} taskId - Task ID (e.g., "T1.1")
 * @param {string} apiToken - API authentication token
 * @param {string} apiUrl - API base URL
 * @returns {Object} Task state or error
 */
async function getCloudTaskState(projectId, taskId, apiToken, apiUrl) {
  const url = `${apiUrl}/projects/${projectId}/tasks/${taskId}`

  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Accept": "application/json",
      "Authorization": `Bearer ${apiToken}`
    }
  })

  if (response.status === 404) {
    return {
      found: false,
      isNew: true,
      message: "Task not found on cloud"
    }
  }

  if (!response.ok) {
    return {
      found: false,
      error: true,
      status: response.status,
      message: `Failed to fetch task: HTTP ${response.status}`
    }
  }

  const data = await response.json()
  return {
    found: true,
    task: data.data.task,
    status: data.data.task.status,
    updatedAt: data.data.task.updatedAt,
    updatedBy: data.data.task.updatedBy
  }
}
```

**Bash Implementation:**
```bash
get_cloud_task_state() {
  local PROJECT_ID="$1"
  local TASK_ID="$2"
  local API_TOKEN="$3"
  local API_URL="${4:-https://api.planflow.tools}"

  RESPONSE=$(curl -s -w "\n%{http_code}" \
    --connect-timeout 5 \
    --max-time 10 \
    -X GET \
    -H "Accept: application/json" \
    -H "Authorization: Bearer $API_TOKEN" \
    "${API_URL}/projects/${PROJECT_ID}/tasks/${TASK_ID}")

  HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
  BODY=$(echo "$RESPONSE" | sed '$d')

  if [ "$HTTP_CODE" -eq 404 ]; then
    echo '{"found": false, "isNew": true}'
  elif [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    # Parse and return task data
    echo "$BODY" | jq '{found: true, task: .data.task}'
  else
    echo "{\"found\": false, \"error\": true, \"status\": $HTTP_CODE}"
  fi
}
```

---

### Function: updateCloudTaskStatus

Updates a single task's status on cloud.

**Pseudo-code:**
```javascript
/**
 * Update task status on cloud
 * @param {string} projectId - Cloud project ID
 * @param {string} taskId - Task ID (e.g., "T1.1")
 * @param {string} newStatus - New status (DONE, IN_PROGRESS, BLOCKED, TODO)
 * @param {string} apiToken - API authentication token
 * @param {string} apiUrl - API base URL
 * @returns {Object} Update result
 */
async function updateCloudTaskStatus(projectId, taskId, newStatus, apiToken, apiUrl) {
  const url = `${apiUrl}/projects/${projectId}/tasks/${taskId}`

  const response = await fetch(url, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
      "Authorization": `Bearer ${apiToken}`
    },
    body: JSON.stringify({ status: newStatus })
  })

  if (!response.ok) {
    return {
      success: false,
      status: response.status,
      message: `Failed to update task: HTTP ${response.status}`
    }
  }

  const data = await response.json()
  return {
    success: true,
    task: data.data.task,
    updatedAt: data.data.task.updatedAt
  }
}
```

**Bash Implementation:**
```bash
update_cloud_task_status() {
  local PROJECT_ID="$1"
  local TASK_ID="$2"
  local NEW_STATUS="$3"
  local API_TOKEN="$4"
  local API_URL="${5:-https://api.planflow.tools}"

  RESPONSE=$(curl -s -w "\n%{http_code}" \
    --connect-timeout 5 \
    --max-time 10 \
    -X PATCH \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -H "Authorization: Bearer $API_TOKEN" \
    -d "{\"status\": \"$NEW_STATUS\"}" \
    "${API_URL}/projects/${PROJECT_ID}/tasks/${TASK_ID}")

  HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
  BODY=$(echo "$RESPONSE" | sed '$d')

  if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo '{"success": true}'
    echo "$BODY" | jq '.data.task.updatedAt' 2>/dev/null
  else
    echo "{\"success\": false, \"status\": $HTTP_CODE}"
  fi
}
```

---

### Comparison Result Actions

| Result | Reason | Action | Description |
|--------|--------|--------|-------------|
| NO_CONFLICT | same_status | skip | Both have same status, no sync needed |
| NO_CONFLICT | first_sync | push | First sync ever, push local |
| NO_CONFLICT | cloud_unchanged | push | Cloud hasn't changed, safe to push |
| AUTO_MERGE | convergent_change | push | Different paths to same result |
| CONFLICT | concurrent_modification | resolve | Both changed differently, needs user |

---

### Integration Example

**Complete hybrid sync flow in a command:**

```javascript
async function hybridSyncTask(taskId, newStatus, config, t) {
  const cloudConfig = config.cloud || {}
  const { apiToken, projectId, lastSyncedAt } = cloudConfig
  const apiUrl = cloudConfig.apiUrl || "https://api.planflow.tools"

  // Step 1: Pull cloud state
  console.log(t.hybridPulling)
  const cloudState = await getCloudTaskState(projectId, taskId, apiToken, apiUrl)

  // Step 2: Handle new task case
  if (!cloudState.found && cloudState.isNew) {
    console.log(t.hybridTaskNew)
    return await updateCloudTaskStatus(projectId, taskId, newStatus, apiToken, apiUrl)
  }

  // Step 3: Handle pull error
  if (!cloudState.found && cloudState.error) {
    console.log(t.hybridPullFailed)
    return { success: false, localOnly: true }
  }

  // Step 4: Compare states
  const comparison = compareTaskStates({
    taskId,
    localStatus: newStatus,
    localUpdatedAt: new Date().toISOString(),
    localUpdatedBy: "local",
    cloudStatus: cloudState.status,
    cloudUpdatedAt: cloudState.updatedAt,
    cloudUpdatedBy: cloudState.updatedBy,
    lastSyncedAt
  })

  // Step 5: Handle based on comparison
  if (comparison.result === "CONFLICT") {
    console.log(t.hybridConflict)
    return { success: false, conflict: comparison }
  }

  if (comparison.action === "skip") {
    console.log(t.hybridNoConflict)
    return { success: true, skipped: true }
  }

  // Step 6: Push changes
  console.log(t.hybridPushing)
  const result = await updateCloudTaskStatus(projectId, taskId, newStatus, apiToken, apiUrl)

  if (result.success) {
    // Update lastSyncedAt
    config.cloud.lastSyncedAt = result.updatedAt
    console.log(t.hybridSyncSuccess)
  }

  return result
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Parse response body |
| 201 | Created | Parse response body |
| 400 | Bad Request | Show validation error |
| 401 | Unauthorized | Token invalid/expired, prompt re-login |
| 403 | Forbidden | No permission, show message |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Sync conflict, show resolution options |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | Show generic error, retry later |
| 502/503 | Service Unavailable | Server down, retry later |

### Error Response Format

All errors follow this format:

```json
{
  "error": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": {}  // Optional additional info
}
```

### Error Parsing Function

**Pseudo-code:**
```javascript
function parseError(response, translations) {
  const t = translations

  if (response.status === 401) {
    return {
      message: t.errors.unauthorized,
      action: t.errors.pleaseLogin,
      code: "UNAUTHORIZED"
    }
  }

  if (response.status === 404) {
    return {
      message: t.errors.notFound,
      action: null,
      code: "NOT_FOUND"
    }
  }

  if (response.status === 409) {
    return {
      message: t.errors.conflict,
      action: t.errors.resolveConflict,
      code: "CONFLICT",
      details: response.body
    }
  }

  if (response.status === 429) {
    const retryAfter = response.body?.retryAfter || 60
    return {
      message: t.errors.rateLimited,
      action: `${t.errors.waitSeconds.replace("{seconds}", retryAfter)}`,
      code: "RATE_LIMITED"
    }
  }

  if (response.status >= 500) {
    return {
      message: t.errors.serverError,
      action: t.errors.tryLater,
      code: "SERVER_ERROR"
    }
  }

  // Generic error
  return {
    message: response.body?.error || t.errors.unknown,
    action: null,
    code: response.body?.code || "UNKNOWN"
  }
}
```

### User-Friendly Error Messages

**Pseudo-code for displaying errors:**
```javascript
function displayError(error, t) {
  let output = `${t.common.error} ${error.message}\n`

  if (error.action) {
    output += `\n💡 ${error.action}\n`
  }

  if (error.code === "UNAUTHORIZED") {
    output += `\n${t.errors.runLogin}\n`
    output += `   /login\n`
  }

  if (error.code === "CONFLICT") {
    output += `\n${t.errors.conflictOptions}\n`
    output += `   /sync push --force   ${t.errors.overwriteCloud}\n`
    output += `   /sync pull --force   ${t.errors.overwriteLocal}\n`
  }

  return output
}
```

**Example output (English):**
```
❌ Error: Invalid or expired token

💡 Please log in again to continue.

   /login
```

**Example output (Georgian):**
```
❌ შეცდომა: არასწორი ან ვადაგასული ტოკენი

💡 გთხოვთ ხელახლა შეხვიდეთ გასაგრძელებლად.

   /login
```

---

## Retry Logic

### Transient Failure Handling

For network errors and 5xx responses, implement retry with exponential backoff.

**Pseudo-code:**
```javascript
async function makeRequestWithRetry(method, endpoint, data, options = {}) {
  const maxRetries = options.maxRetries || 3
  const baseDelay = options.baseDelay || 1000  // 1 second

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await makeRequest(method, endpoint, data)

      // Success or client error (4xx) - don't retry
      if (response.ok || (response.status >= 400 && response.status < 500)) {
        return response
      }

      // Server error (5xx) - retry
      if (attempt < maxRetries) {
        const delay = baseDelay * Math.pow(2, attempt - 1)
        console.log(`Retry ${attempt}/${maxRetries} in ${delay}ms...`)
        await sleep(delay)
      }
    } catch (networkError) {
      // Network error - retry
      if (attempt < maxRetries) {
        const delay = baseDelay * Math.pow(2, attempt - 1)
        console.log(`Network error. Retry ${attempt}/${maxRetries} in ${delay}ms...`)
        await sleep(delay)
      } else {
        return {
          status: 0,
          body: { error: "Network error", code: "NETWORK_ERROR" },
          ok: false
        }
      }
    }
  }

  return {
    status: 503,
    body: { error: "Service unavailable after retries", code: "MAX_RETRIES" },
    ok: false
  }
}
```

**Bash Implementation with Retry:**

```bash
#!/bin/bash
# retry_request.sh

MAX_RETRIES=3
RETRY_DELAY=1

make_request_with_retry() {
  local method="$1"
  local endpoint="$2"
  local data="$3"

  for ((attempt=1; attempt<=MAX_RETRIES; attempt++)); do
    RESPONSE=$(curl -s -w "\n%{http_code}" \
      --connect-timeout 10 \
      --max-time 30 \
      -X "$method" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $API_TOKEN" \
      ${data:+-d "$data"} \
      "${API_URL}${endpoint}" 2>/dev/null)

    CURL_EXIT=$?

    # Network error
    if [ $CURL_EXIT -ne 0 ]; then
      if [ $attempt -lt $MAX_RETRIES ]; then
        echo "Network error. Retrying in ${RETRY_DELAY}s..." >&2
        sleep $RETRY_DELAY
        RETRY_DELAY=$((RETRY_DELAY * 2))
        continue
      else
        echo '{"error": "Network error", "code": "NETWORK_ERROR"}'
        return 1
      fi
    fi

    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | sed '$d')

    # Success or client error - don't retry
    if [ "$HTTP_CODE" -lt 500 ]; then
      echo "$BODY"
      return 0
    fi

    # Server error - retry
    if [ $attempt -lt $MAX_RETRIES ]; then
      echo "Server error ($HTTP_CODE). Retrying in ${RETRY_DELAY}s..." >&2
      sleep $RETRY_DELAY
      RETRY_DELAY=$((RETRY_DELAY * 2))
    fi
  done

  echo '{"error": "Service unavailable", "code": "MAX_RETRIES"}'
  return 1
}
```

---

## Network Connectivity Check

Before making API calls, optionally check connectivity:

**Bash:**
```bash
check_connectivity() {
  if ! curl -s --connect-timeout 5 "${API_URL}/health" > /dev/null 2>&1; then
    echo "Cannot connect to PlanFlow API"
    echo "Please check your internet connection"
    return 1
  fi
  return 0
}
```

---

## Request/Response Logging (Debug Mode)

When `debug: true` in config, log requests:

**Pseudo-code:**
```javascript
function logRequest(method, endpoint, data) {
  if (!config.debug) return

  console.log(`→ ${method} ${endpoint}`)
  if (data) {
    console.log(`  Body: ${JSON.stringify(data, null, 2)}`)
  }
}

function logResponse(response) {
  if (!config.debug) return

  console.log(`← ${response.status}`)
  if (response.body) {
    console.log(`  Body: ${JSON.stringify(response.body, null, 2)}`)
  }
}
```

---

## Usage Examples

### Example 1: Verify Token

```javascript
// In /login command
const response = makeRequest("POST", "/api-tokens/verify", null, true)

if (response.ok) {
  const user = response.body.user
  saveCredentials({
    apiToken: token,
    userId: user.id,
    userEmail: user.email
  })
  showSuccess(`Logged in as ${user.name}`)
} else {
  const error = parseError(response, t)
  showError(error)
}
```

### Example 2: List Projects

```javascript
// In /cloud list command
const response = makeRequest("GET", "/projects")

if (response.ok) {
  const projects = response.body.projects
  displayProjectList(projects)
} else {
  const error = parseError(response, t)
  showError(error)
}
```

### Example 3: Push Plan

```javascript
// In /sync push command
const planContent = readFile("PROJECT_PLAN.md")
const projectId = config.cloud.projectId

const response = makeRequest("PUT", `/projects/${projectId}/plan`, {
  content: planContent
})

if (response.ok) {
  updateConfig({ lastSyncedAt: response.body.updatedAt })
  showSuccess("Plan synced to cloud")
} else if (response.status === 409) {
  showConflictResolution(response.body)
} else {
  const error = parseError(response, t)
  showError(error)
}
```

---

## Security Notes

1. **Token Storage**: Tokens are stored in plain text in config files (standard for CLI tools)
2. **Token Masking**: Never log or display full token - show only first 8 characters
3. **HTTPS Only**: Always use HTTPS for API communication
4. **Token Scope**: API tokens should have limited scope (read/write projects only)
5. **No Secrets in Commands**: Never pass tokens as command line arguments (visible in process list)

**Token Masking Example:**
```javascript
function maskToken(token) {
  if (!token) return "none"
  return token.substring(0, 8) + "..." + token.substring(token.length - 4)
}

// Output: "pf_abc12...xyz9"
```

---

## Integration Notes

### For Command Authors

When using this skill in your command:

1. **Load config first** (Step 0 pattern)
2. **Check authentication** before making requests:
   ```javascript
   const token = getApiToken()
   if (!token) {
     showError(t.errors.notLoggedIn)
     showHint("/login")
     return
   }
   ```
3. **Handle all error cases** gracefully
4. **Update lastSyncedAt** after successful sync operations
5. **Show progress** for long operations

### Common Patterns

**Check if authenticated:**
```javascript
function isAuthenticated() {
  const config = getConfig()
  return !!config.cloud?.apiToken
}
```

**Get current project link:**
```javascript
function getLinkedProjectId() {
  const config = getConfig()
  return config.cloud?.projectId || null
}
```

**Check if project is linked:**
```javascript
function isProjectLinked() {
  return !!getLinkedProjectId()
}
```

---

## Important Notes

1. **This is an internal skill** - not user-invocable
2. **Always handle network errors** - users may be offline
3. **Respect rate limits** - implement backoff
4. **Keep responses fast** - use timeouts
5. **Be secure** - never expose tokens
6. **Be helpful** - provide actionable error messages

This skill provides the foundation for all cloud communication in the plugin.
