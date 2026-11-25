---
name: workspace-bridge-init
description: "This skill should be used when the user asks to 'initialize workspace bridge', 'set up workspace sync', 'connect workspace to Google', 'workspace-bridge-init', 'migrate workspace to Google', or wants to create a new bidirectional sync between their account workspace and Google Sheets/Docs. Interactive wizard that creates Google resources and configures sync."
user-invocable: true
---

# Workspace Bridge Init

Interactive wizard that sets up bidirectional sync between an account workspace and Google Workspace. Creates shared Drive folder, Sheets for structured data, Docs for narrative content, and writes the config file.

## Prerequisites

1. Run `/google-auth` first — migration requires a valid ADC token with Drive, Sheets, and Docs scopes.
2. Must be run from an account workspace root directory.

## Interactive Wizard Flow

Follow these steps in order, asking the user at each decision point:

### Step 1: Detect workspace content

Scan the workspace directory for known file patterns:
- `tracker.md` — Account tracker with items, owners, statuses
- `customer-qa.md` — Customer Q&A log
- `risk-register.md` or README.md with "## Risk Register" section
- `research/index.md` — Research status tracker
- `docs/org-intelligence.md` — Org intelligence document

Report what you find: "I found these files in your workspace: tracker.md, customer-qa.md, ..."

### Step 2: Ask what to sync

Present the user with options based on what exists (and what can be scaffolded from templates):

**Available sync items:**
- `tracker` — Account tracker (multi-tab sheet: Active, Completed, Parking Lot, Workstreams)
- `customer_qa` — Customer Q&A sheet
- `risk_register` — Risk register sheet
- `research_status` — Research status (multi-tab sheet: Active, Complete, Next Refresh)
- `org_intelligence` — Org intelligence Google Doc
- `account_brief` — Auto-generated Account Brief (publish-only)

For files that don't exist, the wizard can scaffold them from templates.

### Step 3: Gather account details

Ask the user:
1. **Account name** (e.g., "Acme Corp") — used for naming Google resources
2. **Team emails** (comma-separated) — who to share the Drive folder with

### Step 4: Ask about customization (optional)

"Do you want to customize workstream names? Default workstreams are: Deployment, Migration, Security, Integration, Training, Support, Renewal, Platform. You can change these later in `.workspace-bridge.json`."

Most users should accept defaults and customize later.

### Step 5: Run the migration script

```bash
RESOURCES_DIR="$(cd "$(dirname "$0")/../../workspace-bridge-init/resources" && pwd)"
python3 "$RESOURCES_DIR/migrate.py" \
    --workspace "$PWD" \
    --folder-name "{Account} Account Team" \
    --share-with "email1@databricks.com,email2@databricks.com" \
    --items "tracker,customer_qa,risk_register,research_status,org_intelligence,account_brief"
```

Add `--workstreams "Custom1,Custom2,Custom3"` if the user specified custom workstreams.

The script:
1. Creates Google Drive folder + Meeting Notes subfolder
2. Shares folder with team
3. For each selected item: migrates existing file or scaffolds from template
4. Writes `.workspace-bridge.json` config
5. Adds sync headers to local markdown files

### Step 6: Verify resources

After migration completes, confirm:
- [ ] `.workspace-bridge.json` exists in workspace root
- [ ] Google Drive folder is accessible (open the URL printed by the script)
- [ ] All sheets have data (spot-check tracker Active tab)
- [ ] Team members received sharing notifications

### Step 7: Update CLAUDE.md session protocol

Add to the workspace CLAUDE.md:

```
- workspace-bridge auto-syncs on session start/stop. Use `/workspace-bridge status` to check sync state.
- Meeting notes: use `/workspace-bridge meeting "Topic"` to create shared Google Docs.
```

## Migration from Personal Plugin

If you previously used the personal version of workspace-bridge:
1. Remove it: `rm -rf ~/.claude/plugins/cache/personal/fe-workspace-bridge/`
2. Your existing `.workspace-bridge.json` is fully compatible — no changes needed
3. The marketplace plugin will take over automatically

## Re-running

The migration script is safe to re-run but will create duplicate resources. If you need to re-initialize:
1. Delete `.workspace-bridge.json`
2. Remove sync headers from local files
3. Optionally delete the Google Drive folder
4. Run init again
