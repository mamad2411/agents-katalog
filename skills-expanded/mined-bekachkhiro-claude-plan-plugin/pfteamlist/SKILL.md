---
name: pfTeamList
description: List team members for the current PlanFlow project
---

# PlanFlow Team List

Display team members, their roles, and current activity for the linked cloud project.

## Usage

```bash
/pfTeamList                 # List all team members
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

const t = JSON.parse(readFile(`locales/${language}.json`))
```

## Step 1: Validate Authentication

If not authenticated:
```
❌ {t.commands.sync.notAuthenticated}

Run: /pfLogin
```

## Step 2: Validate Project Link

If no project is linked:
```
❌ {t.commands.sync.notLinked}

Run: /pfCloudLink <project-id>
```

## Step 3: Fetch Team Members

**API Call:**
```bash
curl -s \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Accept: application/json" \
  "https://api.planflow.tools/projects/{PROJECT_ID}/team"
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "projectId": "uuid",
    "projectName": "My Project",
    "members": [
      {
        "id": "uuid",
        "email": "john@company.com",
        "name": "John Doe",
        "role": "owner",
        "status": "online",
        "currentTask": {
          "taskId": "T2.1",
          "name": "API endpoints"
        },
        "lastSeen": null
      },
      {
        "id": "uuid",
        "email": "jane@company.com",
        "name": "Jane Smith",
        "role": "admin",
        "status": "online",
        "currentTask": {
          "taskId": "T3.5",
          "name": "Dashboard"
        },
        "lastSeen": null
      },
      {
        "id": "uuid",
        "email": "bob@company.com",
        "name": "Bob Wilson",
        "role": "editor",
        "status": "offline",
        "currentTask": null,
        "lastSeen": "2026-02-01T10:30:00Z"
      }
    ],
    "pendingInvites": [
      {
        "email": "alice@company.com",
        "role": "editor",
        "invitedAt": "2026-02-01T09:00:00Z"
      }
    ]
  }
}
```

## Step 4: Display Team Members

**Pseudo-code:**
```javascript
function formatRole(role) {
  const roleMap = {
    "owner": "Owner",
    "admin": "Admin",
    "editor": "Editor",
    "viewer": "Viewer"
  }
  return roleMap[role] || role
}

function formatStatus(member) {
  if (member.status === "online") {
    return "🟢"
  }
  return "🔴"
}

function formatLastSeen(timestamp) {
  if (!timestamp) return ""
  const now = new Date()
  const then = new Date(timestamp)
  const diffMinutes = Math.floor((now - then) / 60000)

  if (diffMinutes < 60) {
    return `${diffMinutes} min ago`
  }
  const diffHours = Math.floor(diffMinutes / 60)
  if (diffHours < 24) {
    return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
  }
  const diffDays = Math.floor(diffHours / 24)
  return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`
}

let output = ""
output += `👥 ${t.commands.team.title}\n\n`
output += `📁 Project: ${data.projectName}\n\n`

for (const member of data.members) {
  const statusIcon = formatStatus(member)
  const role = formatRole(member.role)

  output += `  ${statusIcon} ${member.name} (${role})`
  output += `      ${member.email}\n`

  if (member.status === "online" && member.currentTask) {
    output += `     ${t.commands.team.workingOn}: ${member.currentTask.taskId} - ${member.currentTask.name}\n`
  } else if (member.status === "offline") {
    output += `     ${t.commands.team.lastSeen}: ${formatLastSeen(member.lastSeen)}\n`
  }
  output += "\n"
}

// Show pending invites if any
if (data.pendingInvites && data.pendingInvites.length > 0) {
  output += `\n📨 ${t.commands.team.pendingInvites} (${data.pendingInvites.length})\n`
  for (const invite of data.pendingInvites) {
    output += `  ⏳ ${invite.email} (${formatRole(invite.role)})\n`
  }
}

output += "\n"
output += `💡 ${t.commands.team.commands}:\n`
output += `  /pfTeamInvite <email>        ${t.commands.team.inviteHint}\n`
output += `  /pfTeamRole <email> <role>   ${t.commands.team.roleHint}\n`
output += `  /pfTeamRemove <email>        ${t.commands.team.removeHint}\n`
```

**Example Output:**
```
👥 Team Members

📁 Project: Planflow Plugin

  🟢 John Doe (Owner)      john@company.com
     Working on: T2.1 - API endpoints

  🟢 Jane Smith (Admin)    jane@company.com
     Working on: T3.5 - Dashboard

  🔴 Bob Wilson (Editor)   bob@company.com
     Last seen: 2 hours ago

📨 Pending Invites (1)
  ⏳ alice@company.com (Editor)

💡 Commands:
  /pfTeamInvite <email>        Invite a team member
  /pfTeamRole <email> <role>   Change member role
  /pfTeamRemove <email>        Remove from team
```

**Georgian Example Output:**
```
👥 გუნდის წევრები

📁 პროექტი: Planflow Plugin

  🟢 John Doe (მფლობელი)      john@company.com
     მუშაობს: T2.1 - API endpoints

  🟢 Jane Smith (ადმინი)    jane@company.com
     მუშაობს: T3.5 - Dashboard

  🔴 Bob Wilson (რედაქტორი)   bob@company.com
     ბოლოს ნანახი: 2 საათის წინ

📨 მოლოდინში მყოფი მოწვევები (1)
  ⏳ alice@company.com (რედაქტორი)

💡 ბრძანებები:
  /pfTeamInvite <email>        მოიწვიე გუნდის წევრი
  /pfTeamRole <email> <role>   შეცვალე წევრის როლი
  /pfTeamRemove <email>        წაშალე გუნდიდან
```

## Step 5: Handle Empty Team

If only the owner exists (no team members):

```
👥 Team Members

📁 Project: Planflow Plugin

  🟢 You (Owner)      your@email.com

ℹ️ You're the only team member.

💡 To invite collaborators:
  /pfTeamInvite <email>
  /pfTeamInvite <email> admin    (with role)
```

## Error Handling

**Network Error:**
```
❌ Network error. Could not fetch team information.

Please check your connection and try again.
```

**API Error (401 Unauthorized):**
```
❌ Authentication failed. Your session may have expired.

Run: /pfLogin
```

**API Error (403 Forbidden):**
```
❌ You don't have permission to view team members.

Only project members can view the team list.
```

**API Error (404 Not Found):**
```
❌ Project not found on cloud.

The linked project may have been deleted.
Run: /pfCloudList to see available projects.
```

## Translation Keys Required

Add these to `locales/en.json` and `locales/ka.json`:

**English:**
```json
{
  "commands": {
    "team": {
      "title": "Team Members",
      "project": "Project",
      "workingOn": "Working on",
      "lastSeen": "Last seen",
      "pendingInvites": "Pending Invites",
      "commands": "Commands",
      "inviteHint": "Invite a team member",
      "roleHint": "Change member role",
      "removeHint": "Remove from team",
      "onlyYou": "You're the only team member.",
      "invitePrompt": "To invite collaborators:",
      "noPermission": "You don't have permission to view team members.",
      "projectNotFound": "Project not found on cloud.",
      "roles": {
        "owner": "Owner",
        "admin": "Admin",
        "editor": "Editor",
        "viewer": "Viewer"
      }
    }
  }
}
```

**Georgian:**
```json
{
  "commands": {
    "team": {
      "title": "გუნდის წევრები",
      "project": "პროექტი",
      "workingOn": "მუშაობს",
      "lastSeen": "ბოლოს ნანახი",
      "pendingInvites": "მოლოდინში მყოფი მოწვევები",
      "commands": "ბრძანებები",
      "inviteHint": "მოიწვიე გუნდის წევრი",
      "roleHint": "შეცვალე წევრის როლი",
      "removeHint": "წაშალე გუნდიდან",
      "onlyYou": "შენ ხარ ერთადერთი გუნდის წევრი.",
      "invitePrompt": "კოლაბორატორების მოსაწვევად:",
      "noPermission": "შენ არ გაქვს უფლება გუნდის წევრების სანახავად.",
      "projectNotFound": "პროექტი ვერ მოიძებნა ქლაუდში.",
      "roles": {
        "owner": "მფლობელი",
        "admin": "ადმინი",
        "editor": "რედაქტორი",
        "viewer": "მაყურებელი"
      }
    }
  }
}
```

## Bash Implementation

**Full Implementation:**
```bash
#!/bin/bash

# Load config
API_URL="https://api.planflow.tools"
TOKEN="$API_TOKEN"
PROJECT_ID="$PROJECT_ID"

# Fetch team members
RESPONSE=$(curl -s -w "\n%{http_code}" \
  --connect-timeout 5 \
  --max-time 10 \
  -X GET \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  "${API_URL}/projects/${PROJECT_ID}/team")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "👥 Team Members"
  echo ""
  # Parse and display (Claude will format the JSON response)
else
  echo "❌ Failed to fetch team (HTTP $HTTP_CODE)"
fi
```

## Notes

- This command requires the project to be linked to a cloud project
- Team member statuses are real-time when the platform supports WebSocket connections
- The "Working on" field shows the task the member is currently assigned to with IN_PROGRESS status
- Pending invites are shown separately from active members
