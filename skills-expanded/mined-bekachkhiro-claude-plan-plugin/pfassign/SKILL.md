---
name: pfAssign
description: Assign a task to a team member in the current PlanFlow project
---

# PlanFlow Task Assignment

Assign a task to a team member or yourself in the linked cloud project.

## Usage

```bash
/pfAssign <task-id> <email|me>        # Assign task to team member or self
/pfAssign T2.1 jane@company.com       # Assign to specific member
/pfAssign T2.1 me                     # Assign to yourself
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

  // Merge configs: local overrides global, cloud sections are merged
  return {
    ...globalConfig,
    ...localConfig,
    cloud: {
      ...(globalConfig.cloud || {}),
      ...(localConfig.cloud || {})
    }
  }
}

const config = getConfig()
const language = config.language || "en"
const cloudConfig = config.cloud || {}
const isAuthenticated = !!cloudConfig.apiToken
const projectId = cloudConfig.projectId
const apiUrl = cloudConfig.apiUrl || "https://api.planflow.tools"
const userEmail = cloudConfig.userEmail

const t = JSON.parse(readFile(`locales/${language}.json`))
```

## Step 1: Parse Arguments

Parse the command arguments to extract task ID and assignee.

**Pseudo-code:**
```javascript
const args = commandArgs.trim().split(/\s+/)

if (args.length < 2) {
  // Show usage
  showUsage(t)
  return
}

const taskId = args[0].toUpperCase()  // e.g., T2.1
let assignee = args[1]

// Validate task ID format
const taskIdRegex = /^T\d+\.\d+$/
if (!taskIdRegex.test(taskId)) {
  console.log(`${t.common.error} ${t.commands.assign.invalidTaskId}`)
  console.log(t.commands.assign.taskIdExample)
  return
}

// Handle "me" keyword
if (assignee.toLowerCase() === "me") {
  assignee = userEmail
}

// Validate email format (unless it was "me")
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
if (!emailRegex.test(assignee)) {
  console.log(`${t.common.error} ${t.commands.assign.invalidEmail}`)
  console.log(t.commands.assign.emailExample)
  return
}
```

**Show Usage:**
```
📋 {t.commands.assign.title}

{t.commands.assign.usage}
  /pfAssign <task-id> <email>    {t.commands.assign.usageEmail}
  /pfAssign <task-id> me         {t.commands.assign.usageMe}

{t.commands.assign.example}
  /pfAssign T2.1 jane@company.com
  /pfAssign T2.1 me
```

## Step 2: Validate Authentication

If not authenticated:
```
{t.common.error} {t.commands.sync.notAuthenticated}

Run: /pfLogin
```

## Step 3: Validate Project Link

If no project is linked:
```
{t.common.error} {t.commands.sync.notLinked}

Run: /pfCloudLink <project-id>
```

## Step 4: Assign Task

**API Call:**
```bash
curl -s -w "\n%{http_code}" \
  --connect-timeout 5 \
  --max-time 10 \
  -X PATCH \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer {TOKEN}" \
  -d '{"assignee": "{EMAIL}"}' \
  "https://api.planflow.tools/projects/{PROJECT_ID}/tasks/{TASK_ID}/assign"
```

**Expected Success Response (200):**
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "uuid",
      "taskId": "T2.1",
      "name": "Implement login API",
      "status": "TODO",
      "assignee": {
        "id": "uuid",
        "name": "Jane Smith",
        "email": "jane@company.com"
      },
      "assignedAt": "2026-02-02T12:00:00Z",
      "assignedBy": {
        "id": "uuid",
        "name": "John Doe",
        "email": "john@company.com"
      }
    },
    "projectName": "My Project"
  }
}
```

## Step 5: Display Success

**Pseudo-code:**
```javascript
let output = ""
output += `${t.commands.assign.success}\n\n`
output += `   ${t.commands.assign.task}     ${task.taskId}: ${task.name}\n`
output += `   ${t.commands.assign.assignedTo} ${task.assignee.name} (${task.assignee.email})\n`
output += `   ${t.commands.assign.project}  ${projectName}\n\n`

if (assignee === userEmail) {
  output += `${t.commands.assign.selfAssignHint}\n`
  output += `   /planUpdate ${task.taskId} start\n`
} else {
  output += `${t.commands.assign.notifyHint}\n`
}
```

**Example Output (English):**
```
Task assigned!

   Task:        T2.1: Implement login API
   Assigned to: Jane Smith (jane@company.com)
   Project:     Planflow Plugin

They'll be notified of this assignment.
```

**Example Output (Georgian):**
```
ამოცანა მინიჭებულია!

   ამოცანა:      T2.1: Implement login API
   მინიჭებულია:  Jane Smith (jane@company.com)
   პროექტი:      Planflow Plugin

მათ მიიღებენ შეტყობინებას ამ მინიჭების შესახებ.
```

**Self-Assignment Output (English):**
```
Task assigned!

   Task:        T2.1: Implement login API
   Assigned to: You (john@company.com)
   Project:     Planflow Plugin

Ready to start working? Run:
   /planUpdate T2.1 start
```

## Step 6: Update Local PROJECT_PLAN.md (Optional)

If the task exists in the local PROJECT_PLAN.md, optionally update it with the assignee info.

**Pseudo-code:**
```javascript
// Check if PROJECT_PLAN.md exists
if (fileExists("PROJECT_PLAN.md")) {
  const planContent = readFile("PROJECT_PLAN.md")

  // Find the task section
  const taskPattern = new RegExp(`#### ${taskId}:`)
  if (taskPattern.test(planContent)) {
    // Add or update assignee line after status
    // This is optional - the cloud is the source of truth for assignments
  }
}
```

## Error Handling

### Invalid Task ID Format
```
{t.common.error} {t.commands.assign.invalidTaskId}

{t.commands.assign.taskIdExample}
```

### Invalid Email Format
```
{t.common.error} {t.commands.assign.invalidEmail}

{t.commands.assign.emailExample}
```

### Task Not Found (404)
```
{t.common.error} {t.commands.assign.taskNotFound}

Task ID: {taskId}

{t.commands.assign.checkTaskId}
```

### User Not Team Member (404)
```
{t.common.error} {t.commands.assign.userNotMember}

{email} {t.commands.assign.notMemberHint}

{t.commands.assign.inviteFirst}
  /pfTeamInvite {email}
```

### Permission Denied (403)
```
{t.common.error} {t.commands.assign.noPermission}

{t.commands.assign.noPermissionHint}
```

### Already Assigned (409)
```
{t.common.warning} {t.commands.assign.alreadyAssigned}

Task {taskId} is already assigned to {currentAssignee}.

{t.commands.assign.reassignHint}
  /pfUnassign {taskId}
  /pfAssign {taskId} {newEmail}
```

### Network Error
```
{t.common.error} {t.commands.team.networkError}

{t.commands.assign.tryAgain}
```

### API Error (401 Unauthorized)
```
{t.common.error} {t.commands.team.authFailed}

Run: /pfLogin
```

## Bash Implementation

**Full Implementation:**
```bash
#!/bin/bash

# Load config (Claude will read from config files)
API_URL="https://api.planflow.tools"
TOKEN="$API_TOKEN"
PROJECT_ID="$PROJECT_ID"
USER_EMAIL="$USER_EMAIL"
TASK_ID="$1"
ASSIGNEE="$2"

# Validate task ID format
if ! echo "$TASK_ID" | grep -qE '^T[0-9]+\.[0-9]+$'; then
  echo " Error: Invalid task ID format"
  echo ""
  echo "Task ID should be like: T1.1, T2.3, T10.5"
  exit 1
fi

# Handle "me" keyword
if [ "$(echo "$ASSIGNEE" | tr '[:upper:]' '[:lower:]')" = "me" ]; then
  ASSIGNEE="$USER_EMAIL"
fi

# Validate email format
if ! echo "$ASSIGNEE" | grep -qE '^[^[:space:]@]+@[^[:space:]@]+\.[^[:space:]@]+$'; then
  echo " Error: Invalid email format"
  echo ""
  echo "Example: jane@company.com or use 'me'"
  exit 1
fi

# Assign task
RESPONSE=$(curl -s -w "\n%{http_code}" \
  --connect-timeout 5 \
  --max-time 10 \
  -X PATCH \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"assignee\": \"$ASSIGNEE\"}" \
  "${API_URL}/projects/${PROJECT_ID}/tasks/${TASK_ID}/assign")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

case $HTTP_CODE in
  200)
    # Parse response
    TASK_NAME=$(echo "$BODY" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)
    ASSIGNEE_NAME=$(echo "$BODY" | grep -o '"assignee":{[^}]*"name":"[^"]*"' | grep -o '"name":"[^"]*"' | cut -d'"' -f4)

    echo " Task assigned!"
    echo ""
    echo "   Task:        $TASK_ID: $TASK_NAME"
    echo "   Assigned to: $ASSIGNEE_NAME ($ASSIGNEE)"
    echo ""

    if [ "$ASSIGNEE" = "$USER_EMAIL" ]; then
      echo " Ready to start working? Run:"
      echo "   /planUpdate $TASK_ID start"
    else
      echo " They'll be notified of this assignment."
    fi
    ;;
  404)
    # Check if task or user not found
    if echo "$BODY" | grep -q "task"; then
      echo " Task not found: $TASK_ID"
      echo ""
      echo "Make sure the task exists in the cloud project."
      echo "Run /pfSyncPush to sync your local tasks first."
    else
      echo " User not found: $ASSIGNEE"
      echo ""
      echo "This user is not a team member."
      echo "Invite them first:"
      echo "   /pfTeamInvite $ASSIGNEE"
    fi
    ;;
  409)
    CURRENT_ASSIGNEE=$(echo "$BODY" | grep -o '"email":"[^"]*"' | head -1 | cut -d'"' -f4)
    echo " Task $TASK_ID is already assigned to $CURRENT_ASSIGNEE"
    echo ""
    echo "To reassign, first unassign:"
    echo "   /pfUnassign $TASK_ID"
    echo "   /pfAssign $TASK_ID $ASSIGNEE"
    ;;
  403)
    echo " You don't have permission to assign tasks."
    echo ""
    echo "Only editors and above can assign tasks."
    ;;
  401)
    echo " Authentication failed. Your session may have expired."
    echo ""
    echo "Run: /pfLogin"
    ;;
  *)
    echo " Failed to assign task (HTTP $HTTP_CODE)"
    echo ""
    echo "Please try again later."
    ;;
esac
```

## Translation Keys Required

Add these to `locales/en.json` under `commands.assign`:

**English:**
```json
{
  "commands": {
    "assign": {
      "title": "Task Assignment",
      "usage": "Usage:",
      "usageEmail": "Assign to team member by email",
      "usageMe": "Assign to yourself",
      "example": "Examples:",
      "success": "Task assigned!",
      "task": "Task:",
      "assignedTo": "Assigned to:",
      "project": "Project:",
      "selfAssignHint": "Ready to start working? Run:",
      "notifyHint": "They'll be notified of this assignment.",
      "invalidTaskId": "Invalid task ID format.",
      "taskIdExample": "Task ID should be like: T1.1, T2.3, T10.5",
      "invalidEmail": "Invalid email format.",
      "emailExample": "Example: jane@company.com or use 'me'",
      "taskNotFound": "Task not found.",
      "checkTaskId": "Make sure the task exists. Run /pfSyncPush to sync your local tasks.",
      "userNotMember": "User is not a team member.",
      "notMemberHint": "is not part of this project.",
      "inviteFirst": "Invite them first:",
      "noPermission": "You don't have permission to assign tasks.",
      "noPermissionHint": "Only editors and above can assign tasks.",
      "alreadyAssigned": "Task is already assigned.",
      "reassignHint": "To reassign:",
      "tryAgain": "Please check your connection and try again."
    }
  }
}
```

**Georgian:**
```json
{
  "commands": {
    "assign": {
      "title": "ამოცანის მინიჭება",
      "usage": "გამოყენება:",
      "usageEmail": "მინიჭება გუნდის წევრისთვის ელ-ფოსტით",
      "usageMe": "მინიჭება საკუთარ თავზე",
      "example": "მაგალითები:",
      "success": "ამოცანა მინიჭებულია!",
      "task": "ამოცანა:",
      "assignedTo": "მინიჭებულია:",
      "project": "პროექტი:",
      "selfAssignHint": "მზად ხართ მუშაობის დასაწყებად? გაუშვით:",
      "notifyHint": "მათ მიიღებენ შეტყობინებას ამ მინიჭების შესახებ.",
      "invalidTaskId": "არასწორი ამოცანის ID ფორმატი.",
      "taskIdExample": "ამოცანის ID უნდა იყოს: T1.1, T2.3, T10.5",
      "invalidEmail": "არასწორი ელ-ფოსტის ფორმატი.",
      "emailExample": "მაგალითი: jane@company.com ან 'me'",
      "taskNotFound": "ამოცანა ვერ მოიძებნა.",
      "checkTaskId": "დარწმუნდით რომ ამოცანა არსებობს. გაუშვით /pfSyncPush ლოკალური ამოცანების სასინქრონიზაციოდ.",
      "userNotMember": "მომხმარებელი არ არის გუნდის წევრი.",
      "notMemberHint": "არ არის ამ პროექტის ნაწილი.",
      "inviteFirst": "ჯერ მოიწვიეთ:",
      "noPermission": "თქვენ არ გაქვთ უფლება ამოცანების მინიჭების.",
      "noPermissionHint": "მხოლოდ რედაქტორებს და ზემოთ შეუძლიათ ამოცანების მინიჭება.",
      "alreadyAssigned": "ამოცანა უკვე მინიჭებულია.",
      "reassignHint": "ხელახლა მინიჭებისთვის:",
      "tryAgain": "გთხოვთ შეამოწმოთ კავშირი და სცადოთ ხელახლა."
    }
  }
}
```

## Notes

- The "me" keyword is case-insensitive (Me, ME, me all work)
- Task IDs are case-insensitive but will be normalized to uppercase (t2.1 → T2.1)
- Only team members can be assigned tasks (use /pfTeamInvite first)
- A task can only have one assignee at a time
- To change assignee, use /pfUnassign first then /pfAssign
- Assignment notifications are sent via email (if enabled in user settings)
- Assigning to yourself shows a prompt to start working on the task
