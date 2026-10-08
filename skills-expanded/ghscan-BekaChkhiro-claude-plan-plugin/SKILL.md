---
name: pfTeamRole
description: Change a team member's role in the current PlanFlow project
---

# PlanFlow Team Role

Change the role of an existing team member in the linked cloud project.

## Usage

```bash
/pfTeamRole <email> <role>           # Change member's role
/pfTeamRole bob@company.com viewer
/pfTeamRole alice@company.com admin
```

## Available Roles

| Role | Permissions |
|------|-------------|
| `admin` | Full access, can manage team members |
| `editor` | Can edit tasks and plan |
| `viewer` | Read-only access |

Note: The `owner` role cannot be assigned through this command. Ownership transfer requires a separate process.

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

Parse the command arguments to extract email and new role.

**Pseudo-code:**
```javascript
const args = commandArgs.trim().split(/\s+/)

if (args.length < 2 || !args[0] || !args[1]) {
  // Show usage
  showUsage(t)
  return
}

const email = args[0]
const role = args[1].toLowerCase()

// Validate email format
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
if (!emailRegex.test(email)) {
  console.log(`${t.common.error} ${t.commands.team.role.invalidEmail}`)
  return
}

// Validate role
const validRoles = ["admin", "editor", "viewer"]
if (!validRoles.includes(role)) {
  console.log(`${t.common.error} ${t.commands.team.role.invalidRole}`)
  console.log(`${t.commands.team.role.validRoles}: admin, editor, viewer`)
  return
}
```

**Show Usage:**
```
{t.commands.team.role.title}

{t.commands.team.role.usage}
  /pfTeamRole <email> <role>

{t.commands.team.role.availableRoles}
  admin   - {t.commands.team.invite.roleAdminDesc}
  editor  - {t.commands.team.invite.roleEditorDesc}
  viewer  - {t.commands.team.invite.roleViewerDesc}

{t.commands.team.role.example}
  /pfTeamRole bob@company.com viewer
  /pfTeamRole alice@company.com admin
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

## Step 4: Check Self-Role-Change

Prevent users from changing their own role:

**Pseudo-code:**
```javascript
const currentUserEmail = cloudConfig.userEmail

if (email.toLowerCase() === currentUserEmail.toLowerCase()) {
  console.log(`${t.common.error} ${t.commands.team.role.cannotChangeOwnRole}`)
  console.log("")
  console.log(t.commands.team.role.cannotChangeOwnRoleHint)
  return
}
```

## Step 5: Update Team Member Role

**API Call:**
```bash
curl -s -w "\n%{http_code}" \
  --connect-timeout 5 \
  --max-time 10 \
  -X PATCH \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer {TOKEN}" \
  -d '{"role": "{ROLE}"}' \
  "https://api.planflow.tools/projects/{PROJECT_ID}/team/members/{EMAIL}"
```

Note: The email should be URL-encoded if it contains special characters.

**Expected Success Response (200):**
```json
{
  "success": true,
  "data": {
    "member": {
      "id": "uuid",
      "email": "bob@company.com",
      "name": "Bob Wilson",
      "previousRole": "editor",
      "newRole": "viewer"
    },
    "projectId": "uuid",
    "projectName": "My Project"
  }
}
```

## Step 6: Display Success

**Pseudo-code:**
```javascript
function formatRole(role, t) {
  const roleMap = {
    "owner": t.commands.team.roles.owner,
    "admin": t.commands.team.roles.admin,
    "editor": t.commands.team.roles.editor,
    "viewer": t.commands.team.roles.viewer
  }
  return roleMap[role] || role
}

let output = ""
output += `${t.commands.team.role.success}\n\n`
output += `   ${t.commands.team.role.member}   ${member.name || member.email}\n`
output += `   ${t.commands.team.role.email}    ${member.email}\n`
output += `   ${t.commands.team.role.changed}  ${formatRole(member.previousRole, t)} -> ${formatRole(member.newRole, t)}\n`
output += `   ${t.commands.team.role.project}  ${data.projectName}\n\n`
output += `${t.commands.team.role.effectiveImmediately}\n`
```

**Example Output (English):**
```
Role updated successfully!

   Member:  Bob Wilson
   Email:   bob@company.com
   Changed: Editor -> Viewer
   Project: Planflow Plugin

The new permissions are effective immediately.
```

**Example Output (Georgian):**
```
როლი წარმატებით განახლდა!

   წევრი:    Bob Wilson
   ელ-ფოსტა: bob@company.com
   შეიცვალა: რედაქტორი -> მაყურებელი
   პროექტი:  Planflow Plugin

ახალი უფლებები ძალაშია დაუყოვნებლივ.
```

## Error Handling

### Missing Arguments
```
{t.commands.team.role.title}

{t.commands.team.role.usage}
  /pfTeamRole <email> <role>

{t.commands.team.role.availableRoles}
  admin   - Full access, can manage team members
  editor  - Can edit tasks and plan
  viewer  - Read-only access

{t.commands.team.role.example}
  /pfTeamRole bob@company.com viewer
```

### Invalid Email Format
```
{t.common.error} {t.commands.team.role.invalidEmail}

{t.commands.team.role.emailExample}
```

### Invalid Role
```
{t.common.error} {t.commands.team.role.invalidRole}

{t.commands.team.role.validRoles}: admin, editor, viewer
```

### Cannot Change Own Role
```
{t.common.error} {t.commands.team.role.cannotChangeOwnRole}

{t.commands.team.role.cannotChangeOwnRoleHint}
```

### Cannot Change Owner's Role (403)
```
{t.common.error} {t.commands.team.role.cannotChangeOwnerRole}

{t.commands.team.role.cannotChangeOwnerRoleHint}
```

### User Not Found (404)
```
{t.common.error} {t.commands.team.role.notFound}

{email} {t.commands.team.role.notFoundHint}

{t.commands.team.role.viewTeam}
```

### Same Role (No Change Needed)
```
{t.common.info} {t.commands.team.role.sameRole}

{email} {t.commands.team.role.alreadyHasRole} {role}
```

### Permission Denied (403)
```
{t.common.error} {t.commands.team.role.noPermission}

{t.commands.team.role.noPermissionHint}
```

### Network Error
```
{t.common.error} {t.commands.team.networkError}

{t.commands.team.role.tryAgain}
```

### API Error (401 Unauthorized)
```
{t.common.error} {t.commands.team.authFailed}

Run: /pfLogin
```

### API Error (404 Project Not Found)
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
CURRENT_USER_EMAIL="$USER_EMAIL"
EMAIL="$1"
ROLE="$2"

# Check if both arguments provided
if [ -z "$EMAIL" ] || [ -z "$ROLE" ]; then
  echo "Change Team Member Role"
  echo ""
  echo "Usage:"
  echo "  /pfTeamRole <email> <role>"
  echo ""
  echo "Available roles:"
  echo "  admin   - Full access, can manage team members"
  echo "  editor  - Can edit tasks and plan"
  echo "  viewer  - Read-only access"
  echo ""
  echo "Examples:"
  echo "  /pfTeamRole bob@company.com viewer"
  echo "  /pfTeamRole alice@company.com admin"
  exit 1
fi

# Validate email format
if ! echo "$EMAIL" | grep -qE '^[^[:space:]@]+@[^[:space:]@]+\.[^[:space:]@]+$'; then
  echo "Error: Invalid email format"
  echo ""
  echo "Example: bob@company.com"
  exit 1
fi

# Validate role
ROLE_LOWER=$(echo "$ROLE" | tr '[:upper:]' '[:lower:]')
if [[ ! "$ROLE_LOWER" =~ ^(admin|editor|viewer)$ ]]; then
  echo "Error: Invalid role: $ROLE"
  echo ""
  echo "Valid roles: admin, editor, viewer"
  exit 1
fi

# Check self-role-change
EMAIL_LOWER=$(echo "$EMAIL" | tr '[:upper:]' '[:lower:]')
CURRENT_LOWER=$(echo "$CURRENT_USER_EMAIL" | tr '[:upper:]' '[:lower:]')
if [ "$EMAIL_LOWER" = "$CURRENT_LOWER" ]; then
  echo "Error: You cannot change your own role."
  echo ""
  echo "Ask another admin or the project owner to change your role."
  exit 1
fi

# URL-encode the email
EMAIL_ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$EMAIL', safe=''))" 2>/dev/null || echo "$EMAIL")

# Update team member role
RESPONSE=$(curl -s -w "\n%{http_code}" \
  --connect-timeout 5 \
  --max-time 10 \
  -X PATCH \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"role\": \"$ROLE_LOWER\"}" \
  "${API_URL}/projects/${PROJECT_ID}/team/members/${EMAIL_ENCODED}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

case $HTTP_CODE in
  200)
    # Parse response for member details
    NAME=$(echo "$BODY" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)
    PREV_ROLE=$(echo "$BODY" | grep -o '"previousRole":"[^"]*"' | head -1 | cut -d'"' -f4)
    NEW_ROLE=$(echo "$BODY" | grep -o '"newRole":"[^"]*"' | head -1 | cut -d'"' -f4)

    echo "Role updated successfully!"
    echo ""
    if [ -n "$NAME" ]; then
      echo "   Member:  $NAME"
    fi
    echo "   Email:   $EMAIL"
    if [ -n "$PREV_ROLE" ] && [ -n "$NEW_ROLE" ]; then
      echo "   Changed: $PREV_ROLE -> $NEW_ROLE"
    else
      echo "   Role:    $ROLE_LOWER"
    fi
    echo ""
    echo "The new permissions are effective immediately."
    ;;
  304)
    echo "Info: No change needed."
    echo ""
    echo "$EMAIL already has the role: $ROLE_LOWER"
    ;;
  404)
    # Check if it's project not found or member not found
    if echo "$BODY" | grep -qi "project"; then
      echo "Error: Project not found on cloud."
      echo ""
      echo "Run: /pfCloudList"
    else
      echo "Error: Member not found."
      echo ""
      echo "$EMAIL is not a member of this project."
      echo ""
      echo "Run /pfTeamList to see current team members."
    fi
    ;;
  403)
    # Check if trying to change owner's role or permission denied
    if echo "$BODY" | grep -qi "owner"; then
      echo "Error: Cannot change the owner's role."
      echo ""
      echo "The owner role cannot be changed. Ownership must be transferred instead."
    else
      echo "Error: You don't have permission to change team member roles."
      echo ""
      echo "Only project owners and admins can change roles."
    fi
    ;;
  401)
    echo "Error: Authentication failed. Your session may have expired."
    echo ""
    echo "Run: /pfLogin"
    ;;
  *)
    echo "Error: Failed to update role (HTTP $HTTP_CODE)"
    echo ""
    echo "Please check your connection and try again."
    ;;
esac
```

## Translation Keys Required

Add these to `locales/en.json` under `commands.team.role`:

**English:**
```json
{
  "commands": {
    "team": {
      "role": {
        "title": "Change Team Member Role",
        "usage": "Usage:",
        "availableRoles": "Available roles:",
        "example": "Examples:",
        "success": "Role updated successfully!",
        "member": "Member:",
        "email": "Email:",
        "changed": "Changed:",
        "project": "Project:",
        "effectiveImmediately": "The new permissions are effective immediately.",
        "invalidEmail": "Invalid email format.",
        "emailExample": "Example: bob@company.com",
        "invalidRole": "Invalid role.",
        "validRoles": "Valid roles",
        "cannotChangeOwnRole": "You cannot change your own role.",
        "cannotChangeOwnRoleHint": "Ask another admin or the project owner to change your role.",
        "cannotChangeOwnerRole": "Cannot change the owner's role.",
        "cannotChangeOwnerRoleHint": "The owner role cannot be changed. Ownership must be transferred instead.",
        "notFound": "Member not found.",
        "notFoundHint": "is not a member of this project.",
        "viewTeam": "Run /pfTeamList to see current team members.",
        "sameRole": "No change needed.",
        "alreadyHasRole": "already has the role:",
        "noPermission": "You don't have permission to change team member roles.",
        "noPermissionHint": "Only project owners and admins can change roles.",
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
      "role": {
        "title": "გუნდის წევრის როლის შეცვლა",
        "usage": "გამოყენება:",
        "availableRoles": "ხელმისაწვდომი როლები:",
        "example": "მაგალითები:",
        "success": "როლი წარმატებით განახლდა!",
        "member": "წევრი:",
        "email": "ელ-ფოსტა:",
        "changed": "შეიცვალა:",
        "project": "პროექტი:",
        "effectiveImmediately": "ახალი უფლებები ძალაშია დაუყოვნებლივ.",
        "invalidEmail": "არასწორი ელ-ფოსტის ფორმატი.",
        "emailExample": "მაგალითი: bob@company.com",
        "invalidRole": "არასწორი როლი.",
        "validRoles": "ვალიდური როლები",
        "cannotChangeOwnRole": "საკუთარი როლის შეცვლა შეუძლებელია.",
        "cannotChangeOwnRoleHint": "სთხოვეთ სხვა ადმინს ან პროექტის მფლობელს თქვენი როლის შეცვლა.",
        "cannotChangeOwnerRole": "მფლობელის როლის შეცვლა შეუძლებელია.",
        "cannotChangeOwnerRoleHint": "მფლობელის როლი არ იცვლება. სამაგიეროდ საჭიროა მფლობელობის გადაცემა.",
        "notFound": "წევრი ვერ მოიძებნა.",
        "notFoundHint": "არ არის ამ პროექტის წევრი.",
        "viewTeam": "გაუშვით /pfTeamList გუნდის წევრების სანახავად.",
        "sameRole": "ცვლილება არ არის საჭირო.",
        "alreadyHasRole": "უკვე აქვს როლი:",
        "noPermission": "თქვენ არ გაქვთ უფლება გუნდის წევრების როლების შესაცვლელად.",
        "noPermissionHint": "მხოლოდ პროექტის მფლობელებს და ადმინებს შეუძლიათ როლების შეცვლა.",
        "tryAgain": "გთხოვთ შეამოწმოთ კავშირი და სცადოთ ხელახლა."
      }
    }
  }
}
```

## Notes

- Only project owners and admins can change team member roles
- The `owner` role cannot be assigned or changed through this command
- Users cannot change their own role
- Role changes are effective immediately
- Changing someone from `admin` to a lower role removes their ability to manage the team
- This command works only for existing team members - use `/pfTeamInvite` for new members
