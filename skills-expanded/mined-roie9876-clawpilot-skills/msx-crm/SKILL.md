---
name: "msx-crm"
description: "Query Microsoft Sales Experience (MSX) CRM data — accounts, opportunities, milestones, tasks, and deal teams. Triggers: any mention of 'MSX', 'CRM', 'milestones', 'opportunities', 'deal team', 'pipeline', 'accounts', 'customer milestones', 'sales play', or questions about customer engagement status in Dynamics 365 Sales."
---

# MSX CRM Skill

## Overview

This skill queries the Microsoft Sales Experience (MSX) CRM (Dynamics 365) to retrieve
accounts, opportunities, milestones, tasks, and deal team data. It uses a Node.js
helper script (`run-tool.mjs`) that wraps the CRM OData API.

## CRM URL

https://microsoftsales.crm.dynamics.com

## Platform Compatibility

This skill runs on **macOS, Linux, and Windows**. Detect the OS first and pick the right
command syntax. See `_shared/PLATFORM.md` (skills repo root) for the full reference.

| Action | macOS / Linux (bash) | Windows (PowerShell) |
|--------|----------------------|----------------------|
| Run node script | `node $HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs ...` | `node $HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs ...` |
| Find node | `which node` | `Get-Command node` |
| Home dir | `~` or `$HOME` | `$HOME` |

## Prerequisite Auto-Install

Before running, verify all dependencies are present. Install anything missing automatically.

### Required Sibling Skills

This skill requires sibling skills from the same repository
(`https://github.com/roie9876/clawpilot-skills`):

| Skill | Purpose | Required? |
|-------|---------|-----------|
| `/customer-repo` | Customer engagement folder structure | ⚠️ For customer-scoped queries |

Check if each required skill is installed:

```bash
# macOS / Linux
[ -f "$HOME/.copilot/skills/customer-repo/SKILL.md" ] && echo "✅ installed" || echo "❌ missing"
```

```powershell
# Windows
if (Test-Path "$HOME\.copilot\skills\customer-repo\SKILL.md") { "✅ installed" } else { "❌ missing" }
```

**If ANY required skill is missing**, install all skills from the repository:

1. Clone the repo (skip if already cloned):
   ```bash
   # macOS / Linux
   [ -d "$HOME/customer-skills/.git" ] || git clone https://github.com/roie9876/clawpilot-skills.git "$HOME/customer-skills"
   ```
   ```powershell
   # Windows
   if (-not (Test-Path "$HOME\customer-skills\.git")) {
       git clone https://github.com/roie9876/clawpilot-skills.git "$HOME\customer-skills"
   }
   ```

2. Run the installer (idempotent — safe to re-run):
   ```bash
   # macOS / Linux
   bash "$HOME/customer-skills/scripts/install.sh"
   ```
   ```powershell
   # Windows
   pwsh "$HOME\customer-skills\scripts\install.ps1"
   ```

3. Verify the required skills are now installed. If still missing, stop and report the error.

### Required Tools

| Tool | Check (POSIX) | Check (Windows) | Install (macOS) | Install (Windows) |
|------|---------------|-----------------|-----------------|-------------------|
| Node.js | `node --version` | `Get-Command node` | `brew install node` | `winget install OpenJS.NodeJS` |
| git | `git --version` | `Get-Command git` | Pre-installed | `winget install Git.Git` |
| Azure CLI | `az version` | `az version` | `brew install azure-cli` | `winget install Microsoft.AzureCLI` |

Install any missing tools before proceeding. After installing Node.js, verify: `node --version`.
If `node` is not on `PATH` after Homebrew installation, use the Homebrew binary directly:

```bash
NODE_BIN="$(command -v node || true)"
[ -n "$NODE_BIN" ] || NODE_BIN="$HOME/.homebrew/bin/node"
"$NODE_BIN" --version
```

### CRM Tool Script (`run-tool.mjs`)

The CRM helper script must exist at `$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs`.
It is bundled with this skill; do **not** clone a separate `crm-tools` repo.

```bash
# macOS / Linux
[ -f "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" ] && echo "✅ CRM tools found" || echo "❌ CRM tools missing"
```

```powershell
# Windows
if (Test-Path "$HOME\.copilot\skills\msx-crm\crm-tools\run-tool.mjs") { "✅ CRM tools found" } else { "❌ CRM tools missing" }
```

If missing, reinstall the skills repository so the bundled `crm-tools` folder is linked:

```bash
[ -d "$HOME/customer-skills/.git" ] || git clone https://github.com/roie9876/clawpilot-skills.git "$HOME/customer-skills"
bash "$HOME/customer-skills/scripts/install.sh"
```

```powershell
if (-not (Test-Path "$HOME\customer-skills\.git")) {
    git clone https://github.com/roie9876/clawpilot-skills.git "$HOME\customer-skills"
}
pwsh "$HOME\customer-skills\scripts\install.ps1"
```

### MCAPS-IQ Library

`run-tool.mjs` imports the MSX auth/client code from the MCAPS-IQ library at:

| OS | Required path |
|----|---------------|
| macOS / Linux | `$HOME/.copilot/skills/msx-crm/crm-tools/lib/mcaps-iq/mcp/msx-mcp-server/dist` |
| Windows | `$HOME\.copilot\skills\msx-crm\crm-tools\lib\mcaps-iq\mcp\msx-mcp-server\dist` |

The skill installer clones MCAPS-IQ automatically. Verify it exists:

```bash
[ -f "$HOME/.copilot/skills/msx-crm/crm-tools/lib/mcaps-iq/mcp/msx-mcp-server/dist/auth.js" ] && echo "✅ MCAPS-IQ MSX modules found" || echo "❌ MCAPS-IQ MSX modules missing"
```

```powershell
if (Test-Path "$HOME\.copilot\skills\msx-crm\crm-tools\lib\mcaps-iq\mcp\msx-mcp-server\dist\auth.js") { "✅ MCAPS-IQ MSX modules found" } else { "❌ MCAPS-IQ MSX modules missing" }
```

If MCAPS-IQ is missing but `run-tool.mjs` exists, restore MCAPS-IQ locally or provide an authorized repo URL, then transpile the MSX modules:

```bash
mkdir -p "$HOME/.copilot/skills/msx-crm/crm-tools/lib"
if [ -d "$HOME/MCAPS-IQ" ]; then
    ln -sfn "$HOME/MCAPS-IQ" "$HOME/.copilot/skills/msx-crm/crm-tools/lib/mcaps-iq"
elif [ -n "${MCAPS_IQ_REPO_URL:-}" ]; then
    git clone "$MCAPS_IQ_REPO_URL" "$HOME/.copilot/skills/msx-crm/crm-tools/lib/mcaps-iq"
else
    echo "Place MCAPS-IQ at ~/MCAPS-IQ or set MCAPS_IQ_REPO_URL to an authorized repo URL."
fi
cd "$HOME/.copilot/skills/msx-crm/crm-tools/lib/mcaps-iq/mcp/msx-mcp-server"
esbuild src/auth.ts src/crm.ts src/validation.ts --outdir=dist --format=esm --platform=node --target=node22
```

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.copilot\skills\msx-crm\crm-tools\lib" | Out-Null
if (Test-Path "$HOME\MCAPS-IQ") {
    New-Item -ItemType SymbolicLink -Path "$HOME\.copilot\skills\msx-crm\crm-tools\lib\mcaps-iq" -Target "$HOME\MCAPS-IQ" -Force | Out-Null
} elseif ($env:MCAPS_IQ_REPO_URL) {
    git clone $env:MCAPS_IQ_REPO_URL "$HOME\.copilot\skills\msx-crm\crm-tools\lib\mcaps-iq"
} else {
    "Place MCAPS-IQ at ~/MCAPS-IQ or set MCAPS_IQ_REPO_URL to an authorized repo URL."
}
Set-Location "$HOME\.copilot\skills\msx-crm\crm-tools\lib\mcaps-iq\mcp\msx-mcp-server"
esbuild src/auth.ts src/crm.ts src/validation.ts --outdir=dist --format=esm --platform=node --target=node22
```

### VPN Connection

CRM is only accessible on Microsoft corpnet via VPN.

**macOS / Linux:**
Check if a VPN ensure script exists at `$HOME/Scripts/ensure-vpn.sh`:
```bash
if [ -f "$HOME/Scripts/ensure-vpn.sh" ]; then
    bash "$HOME/Scripts/ensure-vpn.sh"
else
    echo "⚠️ No VPN auto-connect script found. Please connect to Azure VPN manually."
    echo "Check VPN status: scutil --nc list | grep VPN"
fi
```

**Windows:**
There is no automated VPN script for Windows. Ask the user to confirm VPN is connected
via Azure VPN Client before proceeding:
```
⚠️ CRM requires VPN. Please confirm Azure VPN Client is connected before continuing.
```

### M365 Sign-In

Check `m_m365_status`. If not signed in → call `m_m365_sign_in`.

---

## How to Run Tools

After all prerequisites are satisfied:

```bash
# macOS / Linux
NODE_BIN="$(command -v node || true)"
[ -n "$NODE_BIN" ] || NODE_BIN="$HOME/.homebrew/bin/node"
"$NODE_BIN" "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" <tool-name> '<json-params>'
```

```powershell
# Windows
node "$HOME\.copilot\skills\msx-crm\crm-tools\run-tool.mjs" <tool-name> '<json-params>'
```

**Important:** Always run the VPN check before any CRM tool call.

## Available Tools

### 1. `crm_auth_status`
Check if CRM authentication is working.
```bash
node "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" crm_auth_status
```

### 2. `crm_whoami`
Get the current user's CRM identity.
```bash
node "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" crm_whoami
```

### 3. `get_milestones`
Get milestones for a customer, opportunity, or the current user.
Parameters:
- `customerKeyword` (string) — Search accounts by name (e.g., "Aidoc", "Nuvei")
- `opportunityKeyword` (string) — Search opportunities by name
- `opportunityId` (GUID) — Single opportunity ID
- `opportunityIds` (GUID[]) — Multiple opportunity IDs
- `milestoneNumber` (string) — Milestone number lookup
- `milestoneId` (GUID) — Direct milestone lookup
- `ownerId` (GUID) — Filter by owner
- `mine` (boolean) — Get milestones owned by current user
- `statusFilter` ("active") — Only active milestones (Not Started, On Track, In Progress, Blocked, At Risk)
- `keyword` (string) — Filter milestone names
- `includeTasks` (boolean) — Include task data

Examples:
```bash
# Customer milestones
node "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" get_milestones '{"customerKeyword":"Aidoc"}'

# My active milestones
node "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" get_milestones '{"mine":true,"statusFilter":"active"}'
```

### 4. `list_opportunities`
List opportunities for a customer.
Parameters:
- `customerKeyword` (string) — Search accounts by name
- `accountIds` (GUID[]) — Direct account IDs
- `includeCompleted` (boolean) — Include completed/old opportunities

```bash
node "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" list_opportunities '{"customerKeyword":"Aidoc"}'
```

### 5. `get_my_active_opportunities`
Get all active opportunities where the user is owner or deal team member.
Parameters:
- `customerKeyword` (string) — Optional filter by customer name

```bash
node "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" get_my_active_opportunities
```

### 6. `get_milestone_activities`
Get tasks linked to milestones.
Parameters:
- `milestoneId` (GUID) — Single milestone
- `milestoneIds` (GUID[]) — Multiple milestones

```bash
node "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" get_milestone_activities '{"milestoneId":"abc-123..."}'
```

### 7. `find_milestones_needing_tasks`
Find active milestones that have no tasks created yet.
Parameters:
- `customerKeyword` (string)
- `opportunityKeyword` (string)
- `mine` (boolean)

```bash
node "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" find_milestones_needing_tasks '{"mine":true}'
```

### 8. `crm_query`
Raw OData query against any CRM entity set.
Parameters:
- `entitySet` (string, required) — e.g., "accounts", "opportunities", "msp_engagementmilestones", "tasks"
- `filter` (string) — OData $filter expression
- `select` (string) — Comma-separated fields
- `orderby` (string) — OData $orderby expression
- `top` (number) — Max records
- `expand` (string) — OData $expand expression

```bash
node "$HOME/.copilot/skills/msx-crm/crm-tools/run-tool.mjs" crm_query '{"entitySet":"accounts","filter":"contains(name,'\''Aidoc'\'')","select":"accountid,name,msp_tpid","top":10}'
```

### 9. `crm_get_record`
Get a single record by entity set and ID.
Parameters:
- `entitySet` (string, required)
- `id` (GUID, required)
- `select` (string) — Comma-separated fields

### 10. `list_accounts_by_tpid`
Find accounts by TPID.
Parameters:
- `tpid` (string, required)

### 11. `create_task`
Create a new task linked to a milestone.
Parameters:
- `subject` (string, required) — Task title
- `description` (string) — Task description
- `regardingobjectid` (GUID, required) — Milestone ID to link the task to
- `msp_taskcategory` (number) — Activity category (see category codes below)
- `scheduledend` (string) — Due date (ISO format)
- `statuscode` (number) — Status: 2=Not Started, 3=In Progress, 5=Completed
- `statecode` (number) — State: 0=Open, 1=Completed, 2=Canceled

### 12. `update_task`
Update an existing task.
Parameters:
- `taskId` (GUID, required) — Task ID to update
- Plus any fields from `create_task` to modify

### 13. `delete_task`
Delete a task by ID.
Parameters:
- `taskId` (GUID, required)

## CRM Task Category Codes

| Code | Category |
|------|----------|
| 861980000 | Customer Engagement |
| 861980001 | Workshop |
| 861980002 | Demo |
| 861980004 | Architecture Design Session |
| 861980005 | PoC/Pilot |
| 861980006 | Blocker Escalation |
| 861980008 | Briefing |
| 861980012 | Internal |

## Formatted Value Pattern

CRM returns lookup display names as `field@OData.Community.Display.V1.FormattedValue`.
When presenting data, always check for these formatted values to show human-readable
names instead of GUIDs.

## Error Handling

- If you get "IP address is blocked" → VPN dropped mid-call. Re-run VPN check and retry.
- If you get auth errors → Run `az login` or check Azure CLI session.
- Always wrap calls in try/catch and surface useful error messages.

## Output Formatting

When presenting CRM data to the user:
- Use tables for lists of milestones/opportunities
- Show status with emoji indicators: ✅ Completed, 🟢 On Track, 🔴 At Risk/Lost, ❌ Cancelled, ⏸️ Not Started, 🔄 In Progress, ⚠️ Blocked
- Include relevant dates, owners, and opportunity names
- Summarize counts at the end
