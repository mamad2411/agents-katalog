---
name: pfTeamInvite
description: Invite a team member to the current PlanFlow project
---

# PlanFlow Team Invite

Send an invitation to add a new team member to the linked cloud project.

## Usage

```bash
/pfTeamInvite <email>                # Invite with default role (editor)
/pfTeamInvite <email> <role>         # Invite with specific role
/pfTeamInvite alice@company.com
/pfTeamInvite alice@company.com admin
```

## Available Roles

| Role | Permissions |
|------|-------------|
| `admin` | Full access, can manage team members |
| `editor` | Can edit tasks and plan (default) |
| `viewer` | Read-only access |

Note: Only the project owner can assign the `admin` role.

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

## Step 1: Parse Arguments

Parse the command arguments to extract email and optional role.

**Pseudo-code:**
```javascript
const args = commandArgs.trim().split(/\s+/)

if (args.length === 0 || !args[0]) {
  // Show usage
  showUsage(t)
  return
}

const email = args[0]
const role = args[1] || "editor"  // Default role

// Validate email format
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
if (!emailRegex.test(email)) {
  console.log(`${t.common.error} ${t.commands.team.invite.invalidEmail}`)
  return
}

// Validate role
const validRoles = ["admin", "editor", "viewer"]
if (!validRoles.includes(role.toLowerCase())) {
  console.log(`${t.common.error} ${t.commands.team.invite.invalidRole}`)
  console.log(`${t.commands.team.invite.validRoles}: admin, editor, viewer`)
  return
}
```

**Show Usage:**
```
📨 {t.commands.team.invite.title}

{t.commands.team.invite.usage}
  /pfTeamInvite <email>           {t.commands.team.invite.usageDefault}
  /pfTeamInvite <email> <role>    {t.commands.team.invite.usageWithRole}

{t.commands.team.invite.availableRoles}
  admin   - {t.commands.team.invite.roleAdminDesc}
  editor  - {t.commands.team.invite.roleEditorDesc}
  viewer  - {t.commands.team.invite.roleViewerDesc}

{t.commands.team.invite.example}
  /pfTeamInvite alice@company.com
  /pfTeamInvite bob@company.com admin
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

## Step 4: Send Invitation

**API Call:**
```bash
curl -s -w "\n%{http_code}" \
  --connect-timeout 5 \
  --max-time 10 \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer {TOKEN}" \
  -d '{"email": "{EMAIL}", "role": "{ROLE}"}' \
  "https://api.planflow.tools/projects/{PROJECT_ID}/team/invitations"
```

**Expected Success Response (201):**
```json
{
  "success": true,
  "data": {
    "invitation": {
      "id": "uuid",
      "email": "alice@company.com",
      "role": "editor",
      "invitedBy": {
        "id": "uuid",
        "name": "John Doe",
        "email": "john@company.com"
      },
      "projectId": "uuid",
      "projectName": "My Project",
      "expiresAt": "2026-02-08T12:00:00Z",
      "createdAt": "2026-02-01T12:00:00Z"
    }
  }
}
```

## Step 5: Display Success

**Pseudo-code:**
```javascript
function formatRole(role, t) {
  const roleMap = {
    "admin": t.commands.team.roles.admin,
    "editor": t.commands.team.roles.editor,
    "viewer": t.commands.team.roles.viewer
  }
  return roleMap[role] || role
}

let output = ""
output += `${t.commands.team.invite.success}\n\n`
output += `   ${t.commands.team.invite.to}   ${invitation.email}\n`
output += `   ${t.commands.team.invite.role} ${formatRole(invitation.role, t)}\n`
output += `   ${t.commands.team.invite.project} ${invitation.projectName}\n\n`
output += `${t.commands.team.invite.emailSent}\n\n`
output += `${t.commands.team.invite.expiresHint}\n`
```

**Example Output (English):**
```
Invitation sent!

   To:      alice@company.com
   Role:    Editor
   Project: Planflow Plugin

They'll receive an email with instructions to join.

The invitation expires in 7 days.
```

**Example Output (Georgian):**
```
მოწვევა გაიგზავნა!

   მიმღები:  alice@company.com
   როლი:     რედაქტორი
   პროექტი:  Planflow Plugin

ისინი მიიღებენ ელ-ფოსტას შეერთების ინსტრუქციებით.

მოწვევის ვადა იწურება 7 დღეში.
```

## Error Handling

### Invalid Email Format
```
{t.common.error} {t.commands.team.invite.invalidEmail}

{t.commands.team.invite.emailExample}
```

### Invalid Role
```
{t.common.error} {t.commands.team.invite.invalidRole}

{t.commands.team.invite.validRoles}: admin, editor, viewer
```

### User Already Member (409 Conflict)
```
{t.common.warning} {t.commands.team.invite.alreadyMember}

{email} {t.commands.team.invite.alreadyMemberHint}
```

### Invitation Already Pending (409 Conflict)
```
{t.common.warning} {t.commands.team.invite.alreadyInvited}

{t.commands.team.invite.pendingInviteHint}
```

### Permission Denied (403 Forbidden)
```
{t.common.error} {t.commands.team.invite.noPermission}

{t.commands.team.invite.noPermissionHint}
```

### Self-Invite Attempt
```
{t.common.error} {t.commands.team.invite.cannotInviteSelf}
```

### Network Error
```
{t.common.error} {t.commands.team.networkError}

{t.commands.team.invite.tryAgain}
```

### API Error (401 Unauthorized)
```
{t.common.error} {t.commands.team.authFailed}

Run: /pfLogin
```

### API Error (404 Not Found)
```
{t.common.error} {t.commands.team.projectNotFound}

Run: /pfCloudList
```

## Bash Implementation

**Full Implementation:**
```bash
#!/bin/bash

# Load config (Claude will read from config files)
API_URL="https://api.planflow.tools"
TOKEN="$API_TOKEN"
PROJECT_ID="$PROJECT_ID"
EMAIL="$1"
ROLE="${2:-editor}"

# Validate email format
if ! echo "$EMAIL" | grep -qE '^[^[:space:]@]+@[^[:space:]@]+\.[^[:space:]@]+$'; then
  echo " Error: Invalid email format"
  echo ""
  echo "Example: alice@company.com"
  exit 1
fi

# Validate role
ROLE_LOWER=$(echo "$ROLE" | tr '[:upper:]' '[:lower:]')
if [[ ! "$ROLE_LOWER" =~ ^(admin|editor|viewer)$ ]]; then
  echo " Error: Invalid role: $ROLE"
  echo ""
  echo "Valid roles: admin, editor, viewer"
  exit 1
fi

# Send invitation
RESPONSE=$(curl -s -w "\n%{http_code}" \
  --connect-timeout 5 \
  --max-time 10 \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"email\": \"$EMAIL\", \"role\": \"$ROLE_LOWER\"}" \
  "${API_URL}/projects/${PROJECT_ID}/team/invitations")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

case $HTTP_CODE in
  201)
    echo " Invitation sent!"
    echo ""
    echo "   To:      $EMAIL"
    echo "   Role:    $ROLE_LOWER"
    echo ""
    echo " They'll receive an email with instructions to join."
    ;;
  409)
    # Check if already member or already invited
    if echo "$BODY" | grep -q "already a member"; then
      echo " $EMAIL is already a team member."
    else
      echo " An invitation is already pending for $EMAIL."
    fi
    ;;
  403)
    echo " You don't have permission to invite team members."
    echo ""
    echo "Only project owners and admins can send invitations."
    ;;
  401)
    echo " Authentication failed. Your session may have expired."
    echo ""
    echo "Run: /pfLogin"
    ;;
  404)
    echo " Project not found on cloud."
    echo ""
    echo "Run: /pfCloudList"
    ;;
  *)
    echo " Failed to send invitation (HTTP $HTTP_CODE)"
    echo ""
    echo "Please try again later."
    ;;
esac
```

## Translation Keys Required

Add these to `locales/en.json` under `commands.team.invite`:

**English:**
```json
{
  "commands": {
    "team": {
      "invite": {
        "title": "Team Invite",
        "usage": "Usage:",
        "usageDefault": "Invite with default role (editor)",
        "usageWithRole": "Invite with specific role",
        "availableRoles": "Available roles:",
        "roleAdminDesc": "Full access, can manage team members",
        "roleEditorDesc": "Can edit tasks and plan (default)",
        "roleViewerDesc": "Read-only access",
        "example": "Examples:",
        "success": "Invitation sent!",
        "to": "To:",
        "role": "Role:",
        "project": "Project:",
        "emailSent": "They'll receive an email with instructions to join.",
        "expiresHint": "The invitation expires in 7 days.",
        "invalidEmail": "Invalid email format.",
        "emailExample": "Example: alice@company.com",
        "invalidRole": "Invalid role.",
        "validRoles": "Valid roles",
        "alreadyMember": "User is already a team member.",
        "alreadyMemberHint": "is already part of this project.",
        "alreadyInvited": "Invitation already pending.",
        "pendingInviteHint": "An invitation has already been sent to this email.",
        "noPermission": "You don't have permission to invite team members.",
        "noPermissionHint": "Only project owners and admins can send invitations.",
        "cannotInviteSelf": "You cannot invite yourself.",
        "tryAgain": "Please check your connection and try again."
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
      "invite": {
        "title": "გუნდში მოწვევა",
        "usage": "გამოყენება:",
        "usageDefault": "მოწვევა ნაგულისხმევი როლით (რედაქტორი)",
        "usageWithRole": "მოწვევა კონკრეტული როლით",
        "availableRoles": "ხელმისაწვდომი როლები:",
        "roleAdminDesc": "სრული წვდომა, შეუძლია გუნდის მართვა",
        "roleEditorDesc": "შეუძლია ამოცანების და გეგმის რედაქტირება (ნაგულისხმევი)",
        "roleViewerDesc": "მხოლოდ წაკითხვის უფლება",
        "example": "მაგალითები:",
        "success": "მოწვევა გაიგზავნა!",
        "to": "მიმღები:",
        "role": "როლი:",
        "project": "პროექტი:",
        "emailSent": "ისინი მიიღებენ ელ-ფოსტას შეერთების ინსტრუქციებით.",
        "expiresHint": "მოწვევის ვადა იწურება 7 დღეში.",
        "invalidEmail": "არასწორი ელ-ფოსტის ფორმატი.",
        "emailExample": "მაგალითი: alice@company.com",
        "invalidRole": "არასწორი როლი.",
        "validRoles": "ვალიდური როლები",
        "alreadyMember": "მომხმარებელი უკვე გუნდის წევრია.",
        "alreadyMemberHint": "უკვე არის ამ პროექტის ნაწილი.",
        "alreadyInvited": "მოწვევა უკვე გაგზავნილია.",
        "pendingInviteHint": "მოწვევა უკვე გაიგზავნა ამ ელ-ფოსტაზე.",
        "noPermission": "შენ არ გაქვს უფლება გუნდის წევრების მოსაწვევად.",
        "noPermissionHint": "მხოლოდ პროექტის მფლობელებს და ადმინებს შეუძლიათ მოწვევების გაგზავნა.",
        "cannotInviteSelf": "საკუთარი თავის მოწვევა შეუძლებელია.",
        "tryAgain": "გთხოვთ შეამოწმოთ კავშირი და სცადოთ ხელახლა."
      }
    }
  }
}
```

## Notes

- Only project owners and admins can invite new team members
- The `owner` role cannot be assigned through invitations
- Invitations expire after 7 days by default
- Users receive an email notification with a link to accept the invitation
- If the invited user doesn't have a PlanFlow account, they'll be prompted to create one
- Pending invitations can be viewed with `/pfTeamList`
- To cancel a pending invitation, use `/pfTeamInvite cancel <email>` (future feature)
