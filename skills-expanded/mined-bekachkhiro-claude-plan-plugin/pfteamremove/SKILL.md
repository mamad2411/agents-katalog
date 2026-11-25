---
name: pfTeamRemove
description: Remove a team member from the current PlanFlow project
---

# PlanFlow Team Remove

Remove a team member from the linked cloud project.

## Usage

```bash
/pfTeamRemove <email>                # Remove member by email
/pfTeamRemove bob@company.com
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

## Step 1: Parse Arguments

Parse the command arguments to extract the email of the member to remove.

**Pseudo-code:**
```javascript
const args = commandArgs.trim()

if (!args) {
  // Show usage
  showUsage(t)
  return
}

const email = args.split(/\s+/)[0]

// Validate email format
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
if (!emailRegex.test(email)) {
  console.log(`${t.common.error} ${t.commands.team.remove.invalidEmail}`)
  return
}
```

**Show Usage:**
```
{t.commands.team.remove.title}

{t.commands.team.remove.usage}
  /pfTeamRemove <email>

{t.commands.team.remove.example}
  /pfTeamRemove bob@company.com
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

## Step 4: Check Self-Removal

Prevent users from removing themselves:

**Pseudo-code:**
```javascript
const currentUserEmail = cloudConfig.userEmail

if (email.toLowerCase() === currentUserEmail.toLowerCase()) {
  console.log(`${t.common.error} ${t.commands.team.remove.cannotRemoveSelf}`)
  console.log("")
  console.log(t.commands.team.remove.cannotRemoveSelfHint)
  return
}
```

## Step 5: Remove Team Member

**API Call:**
```bash
curl -s -w "\n%{http_code}" \
  --connect-timeout 5 \
  --max-time 10 \
  -X DELETE \
  -H "Accept: application/json" \
  -H "Authorization: Bearer {TOKEN}" \
  "https://api.planflow.tools/projects/{PROJECT_ID}/team/members/{EMAIL}"
```

Note: The email should be URL-encoded if it contains special characters.

**Expected Success Response (200):**
```json
{
  "success": true,
  "data": {
    "removed": {
      "email": "bob@company.com",
      "name": "Bob Wilson",
      "role": "editor"
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
output += `${t.commands.team.remove.success}\n\n`
output += `   ${t.commands.team.remove.member}  ${removed.name || removed.email}\n`
output += `   ${t.commands.team.remove.email}   ${removed.email}\n`
output += `   ${t.commands.team.remove.role}    ${formatRole(removed.role, t)}\n`
output += `   ${t.commands.team.remove.project} ${data.projectName}\n\n`
output += `${t.commands.team.remove.accessRevoked}\n`
```

**Example Output (English):**
```
Member removed from team.

   Member:  Bob Wilson
   Email:   bob@company.com
   Role:    Editor
   Project: Planflow Plugin

They no longer have access to this project.
```

**Example Output (Georgian):**
```
წევრი წაიშალა გუნდიდან.

   წევრი:    Bob Wilson
   ელ-ფოსტა: bob@company.com
   როლი:     რედაქტორი
   პროექტი:  Planflow Plugin

მას აღარ აქვს წვდომა ამ პროექტზე.
```

## Error Handling

### Invalid Email Format
```
{t.common.error} {t.commands.team.remove.invalidEmail}

{t.commands.team.remove.emailExample}
```

### User Not Found (404)
```
{t.common.error} {t.commands.team.remove.notFound}

{email} {t.commands.team.remove.notFoundHint}

{t.commands.team.remove.viewTeam}
```

### Cannot Remove Self
```
{t.common.error} {t.commands.team.remove.cannotRemoveSelf}

{t.commands.team.remove.cannotRemoveSelfHint}
```

### Cannot Remove Owner (403)
```
{t.common.error} {t.commands.team.remove.cannotRemoveOwner}

{t.commands.team.remove.cannotRemoveOwnerHint}
```

### Permission Denied (403)
```
{t.common.error} {t.commands.team.remove.noPermission}

{t.commands.team.remove.noPermissionHint}
```

### Network Error
```
{t.common.error} {t.commands.team.networkError}

{t.commands.team.remove.tryAgain}
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

# Check if email provided
if [ -z "$EMAIL" ]; then
  echo "Remove Team Member"
  echo ""
  echo "Usage:"
  echo "  /pfTeamRemove <email>"
  echo ""
  echo "Example:"
  echo "  /pfTeamRemove bob@company.com"
  exit 1
fi

# Validate email format
if ! echo "$EMAIL" | grep -qE '^[^[:space:]@]+@[^[:space:]@]+\.[^[:space:]@]+$'; then
  echo "Error: Invalid email format"
  echo ""
  echo "Example: bob@company.com"
  exit 1
fi

# Check self-removal
EMAIL_LOWER=$(echo "$EMAIL" | tr '[:upper:]' '[:lower:]')
CURRENT_LOWER=$(echo "$CURRENT_USER_EMAIL" | tr '[:upper:]' '[:lower:]')
if [ "$EMAIL_LOWER" = "$CURRENT_LOWER" ]; then
  echo "Error: You cannot remove yourself from the team."
  echo ""
  echo "To leave a project, ask the project owner to remove you."
  exit 1
fi

# URL-encode the email
EMAIL_ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$EMAIL', safe=''))" 2>/dev/null || echo "$EMAIL")

# Remove team member
RESPONSE=$(curl -s -w "\n%{http_code}" \
  --connect-timeout 5 \
  --max-time 10 \
  -X DELETE \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  "${API_URL}/projects/${PROJECT_ID}/team/members/${EMAIL_ENCODED}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

case $HTTP_CODE in
  200)
    # Parse response for member details
    NAME=$(echo "$BODY" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)
    ROLE=$(echo "$BODY" | grep -o '"role":"[^"]*"' | head -1 | cut -d'"' -f4)

    echo "Member removed from team."
    echo ""
    if [ -n "$NAME" ]; then
      echo "   Member:  $NAME"
    fi
    echo "   Email:   $EMAIL"
    if [ -n "$ROLE" ]; then
      echo "   Role:    $ROLE"
    fi
    echo ""
    echo "They no longer have access to this project."
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
    # Check if trying to remove owner or permission denied
    if echo "$BODY" | grep -qi "owner"; then
      echo "Error: Cannot remove the project owner."
      echo ""
      echo "Project ownership must be transferred before the owner can be removed."
    else
      echo "Error: You don't have permission to remove team members."
      echo ""
      echo "Only project owners and admins can remove members."
    fi
    ;;
  401)
    echo "Error: Authentication failed. Your session may have expired."
    echo ""
    echo "Run: /pfLogin"
    ;;
  *)
    echo "Error: Failed to remove member (HTTP $HTTP_CODE)"
    echo ""
    echo "Please check your connection and try again."
    ;;
esac
```

## Translation Keys Required

Add these to `locales/en.json` under `commands.team.remove`:

**English:**
```json
{
  "commands": {
    "team": {
      "remove": {
        "title": "Remove Team Member",
        "usage": "Usage:",
        "example": "Example:",
        "success": "Member removed from team.",
        "member": "Member:",
        "email": "Email:",
        "role": "Role:",
        "project": "Project:",
        "accessRevoked": "They no longer have access to this project.",
        "invalidEmail": "Invalid email format.",
        "emailExample": "Example: bob@company.com",
        "notFound": "Member not found.",
        "notFoundHint": "is not a member of this project.",
        "viewTeam": "Run /pfTeamList to see current team members.",
        "cannotRemoveSelf": "You cannot remove yourself from the team.",
        "cannotRemoveSelfHint": "To leave a project, ask the project owner to remove you.",
        "cannotRemoveOwner": "Cannot remove the project owner.",
        "cannotRemoveOwnerHint": "Project ownership must be transferred before the owner can be removed.",
        "noPermission": "You don't have permission to remove team members.",
        "noPermissionHint": "Only project owners and admins can remove members.",
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
      "remove": {
        "title": "გუნდის წევრის წაშლა",
        "usage": "გამოყენება:",
        "example": "მაგალითი:",
        "success": "წევრი წაიშალა გუნდიდან.",
        "member": "წევრი:",
        "email": "ელ-ფოსტა:",
        "role": "როლი:",
        "project": "პროექტი:",
        "accessRevoked": "მას აღარ აქვს წვდომა ამ პროექტზე.",
        "invalidEmail": "არასწორი ელ-ფოსტის ფორმატი.",
        "emailExample": "მაგალითი: bob@company.com",
        "notFound": "წევრი ვერ მოიძებნა.",
        "notFoundHint": "არ არის ამ პროექტის წევრი.",
        "viewTeam": "გაუშვით /pfTeamList გუნდის წევრების სანახავად.",
        "cannotRemoveSelf": "საკუთარი თავის წაშლა შეუძლებელია.",
        "cannotRemoveSelfHint": "პროექტის დასატოვებლად, სთხოვეთ პროექტის მფლობელს თქვენი წაშლა.",
        "cannotRemoveOwner": "პროექტის მფლობელის წაშლა შეუძლებელია.",
        "cannotRemoveOwnerHint": "მფლობელის წაშლამდე საჭიროა მფლობელობის გადაცემა.",
        "noPermission": "თქვენ არ გაქვთ უფლება გუნდის წევრების წასაშლელად.",
        "noPermissionHint": "მხოლოდ პროექტის მფლობელებს და ადმინებს შეუძლიათ წევრების წაშლა.",
        "tryAgain": "გთხოვთ შეამოწმოთ კავშირი და სცადოთ ხელახლა."
      }
    }
  }
}
```

## Notes

- Only project owners and admins can remove team members
- The project owner cannot be removed (ownership must be transferred first)
- Users cannot remove themselves (they must ask an owner/admin)
- Removed members lose all access to the project immediately
- Any tasks assigned to the removed member remain but become unassigned
- Pending invitations can be cancelled with `/pfTeamRemove <email>` as well (removes pending invite)
- This action cannot be undone - to re-add someone, use `/pfTeamInvite`
