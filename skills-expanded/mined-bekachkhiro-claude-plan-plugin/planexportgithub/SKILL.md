---
name: planExportGithub
description: Export PROJECT_PLAN.md tasks as GitHub Issues
---

# Plan Export to GitHub Issues

Export PROJECT_PLAN.md tasks as GitHub Issues with labels and dependencies.

## Usage

```bash
/planExportGithub
```

## Step 0: Load Configuration

```javascript
function getConfig() {
  if (fileExists("./.plan-config.json")) {
    try { return JSON.parse(readFile("./.plan-config.json")) } catch {}
  }
  const globalPath = expandPath("~/.config/claude/plan-plugin-config.json")
  if (fileExists(globalPath)) {
    try { return JSON.parse(readFile(globalPath)) } catch {}
  }
  return { "language": "en" }
}

const config = getConfig()
const language = config.language || "en"
const t = JSON.parse(readFile(`locales/${language}.json`))
```

## Step 1: Read PROJECT_PLAN.md

If not found:
```
{t.commands.update.planNotFound}

{t.commands.update.runPlanNew}
```

## Step 2: Check Prerequisites

### Check GitHub CLI
```bash
gh --version
```

If not installed:
```
{t.commands.export.ghNotFound}

{t.commands.export.ghInstall}
{t.commands.export.ghUrl}
```

### Check Authentication
```bash
gh auth status
```

If not authenticated:
```
{t.commands.export.ghNotAuth}

{t.commands.export.ghAuthCommand}
```

### Check Git Repository
```bash
git rev-parse --is-inside-work-tree
```

If not a repo:
```
⚠️ Not a Git repository.

To export to GitHub Issues:
1. Initialize a Git repo: git init
2. Create a GitHub repo: gh repo create
3. Or run this command in an existing Git repo
```

## Step 3: Parse Project Data

Extract from PROJECT_PLAN.md:
- Project name
- All tasks (ID, name, status, complexity, estimate, dependencies, description)
- Phases

## Step 4: Create Labels

Create these labels (if they don't exist):
- `phase-1`, `phase-2`, `phase-3`, `phase-4`
- `complexity-low`, `complexity-medium`, `complexity-high`
- `status-todo`, `status-in-progress`, `status-done`, `status-blocked`
- `plan-plugin`

## Step 5: Create Issues

For each task:

### Issue Title Format
```
[Phase N] TX.Y: Task Name
```

### Issue Body Format
```markdown
## Task Details

**Phase**: [N] - [Phase Name]
**Complexity**: [Low/Medium/High]
**Estimated Effort**: [X] hours
**Status**: [TODO/IN_PROGRESS/DONE/BLOCKED]

## Description

[Full task description from plan]

## Dependencies

[List of dependency task IDs, or "None"]

---

*Exported from PROJECT_PLAN.md*
*Created by plan-plugin*
```

### Create Issue Command
```bash
gh issue create \
  --title "[Phase 1] T1.1: Project Setup" \
  --body "$(cat <<'EOF'
[Issue body content here]
EOF
)" \
  --label "phase-1,complexity-low,status-todo,plan-plugin"
```

## Step 6: Show Progress

```
Creating GitHub Issues...

✅ Created: [Phase 1] T1.1: Project Setup (#1)
✅ Created: [Phase 1] T1.2: Database Setup (#2)
...

📊 Export Summary:
• Total Issues Created: 18

🏷️ Labels Created:
• phase-1, phase-2, phase-3, phase-4
• complexity-low, complexity-medium, complexity-high

🔗 View all issues:
   gh issue list --label plan-plugin

Or visit:
   https://github.com/user/repo/issues
```

## Error Handling

```
❌ Error: gh command failed

[Error message from gh CLI]

Possible solutions:
1. Authenticate: gh auth login
2. Check repo access: gh repo view
3. Verify network connection
```
