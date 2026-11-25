---
name: canva-manager
description: |
  Comprehensive Canva API integration skill for managing designs, folders, assets, and exports.
  Uses a 3-mode workflow: PLAN (analyze what needs to be done), CLARIFY (ask user questions),
  and IMPLEMENT (execute changes via Python scripts). Ensures safe operations by always
  confirming changes before execution. Use this skill when the user wants to work with their
  Canva account, manage designs, organize folders, upload assets, or export designs.
---

# Canva Manager Skill

> **QUICK REFERENCE**
> - **Scripts location**: `scripts/` (NOT `skills/*/scripts/` - those paths don't exist)
> - **Auth check**: `.venv\Scripts\python.exe scripts/auth_check.py`
> - **List designs**: `.venv\Scripts\python.exe scripts/list_designs.py`
> - **List folders**: `.venv\Scripts\python.exe scripts/list_folders.py`
> - **Export design**: `.venv\Scripts\python.exe scripts/export_design.py --id "ID" --format pdf`
> - **API client**: `scripts/canva_client.py` (import: `from canva_client import get_client`)
> - **Sample script**: `scripts/samples/sample_canva_operations.py`
> - **Always use**: `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (Mac/Linux)
>
> **WARNING**: Commands below referencing `skills/canva-*/scripts/*.py` are WRONG paths.
> Use actual scripts in `scripts/` folder. For custom operations, see `scripts/samples/sample_canva_operations.py`.

A comprehensive skill for managing Canva designs, folders, and assets through the Canva Connect API. This skill operates in a **3-mode workflow** to ensure safe and accurate operations on your Canva account.

## Overview

This skill provides full control over your Canva account including:
- **Designs**: List, view, create, export, and manage designs (Instagram posts, Presentations, Documents, etc.)
- **Folders**: Create, organize, move items, and manage your project structure
- **Assets**: Upload images, videos, and other media to your Canva library
- **Exports**: Export designs to various formats (PDF, PNG, JPG, PPTX, MP4, GIF)

## 3-Mode Workflow

**CRITICAL: Always follow this workflow. Never skip to implementation without completing Plan and Clarify modes.**

### Mode 1: PLAN

Before making ANY changes to Canva, you MUST:

1. **Analyze the Request**
   - What exactly does the user want to accomplish?
   - Which Canva resources are involved (designs, folders, assets)?
   - What API operations will be needed?

2. **Gather Current State**
   - Run the discovery scripts to understand current Canva account state
   - List relevant designs, folders, or assets
   - Identify exactly which items will be affected

3. **Create Detailed Plan**
   - Document every action that will be taken
   - List which designs/folders/assets will be modified
   - Specify the exact changes (names, exports, moves, etc.)
   - Identify potential risks or irreversible actions

4. **Present Plan to User**
   Format the plan clearly:
   ```
   ## Canva Operation Plan

   ### Objective
   [What we're trying to accomplish]

   ### Current State
   - Found X designs in folder Y
   - Design "ABC" has 5 pages
   - etc.

   ### Proposed Actions
   1. [Action 1 - specific details]
   2. [Action 2 - specific details]

   ### Potential Risks
   - [Any irreversible actions]
   - [Rate limit considerations]

   ### What Will NOT Be Changed
   - [Explicitly list unaffected items]
   ```

### Mode 2: CLARIFY

After presenting the plan, you MUST ask clarifying questions:

1. **Required Questions**
   - "Does this plan accurately reflect what you want to do?"
   - "Are there any items I should exclude from this operation?"
   - "Should I proceed with all X items or just specific ones?"

2. **Context-Specific Questions**
   - For exports: "What format and quality do you prefer?"
   - For folder operations: "Should I create backups first?"
   - For design modifications: "Should I work on copies instead of originals?"
   - For bulk operations: "Do you want me to process all at once or in batches?"

3. **Confirmation Requirements**
   - Get explicit "yes" or confirmation before proceeding
   - If user has concerns, return to PLAN mode with modifications
   - Never assume silence means approval

### Mode 3: IMPLEMENT

Only after explicit user approval:

1. **Pre-Implementation Checks**
   - Verify credentials are valid (run auth check script)
   - Confirm API rate limits are sufficient
   - Double-check target items match the plan

2. **Execute with Logging**
   - Run the appropriate Python scripts
   - Log every API call and response
   - Save results to the output folder

3. **Report Results**
   - Show exactly what was changed
   - Provide links/IDs of affected items
   - Note any errors or partial completions

## Environment Setup

Before using this skill, ensure the `.env` file is configured:

```bash
# Required - Get from https://www.canva.com/developers/
CANVA_CLIENT_ID=your_client_id
CANVA_CLIENT_SECRET=your_client_secret

# OAuth tokens (obtained after authorization)
CANVA_ACCESS_TOKEN=your_access_token
CANVA_REFRESH_TOKEN=your_refresh_token

# Optional
CANVA_REDIRECT_URI=http://127.0.0.1:3001/oauth/redirect
```

## Running Python Scripts (Virtual Environment)

**IMPORTANT**: Always use the virtual environment Python:

```bash
# Windows
.venv\Scripts\python.exe scripts/script_name.py

# macOS/Linux
.venv/bin/python scripts/script_name.py
```

## Available Scripts

All scripts are in `scripts/`:

### Discovery Scripts (Safe - Read Only)
- `auth_check.py` - Verify credentials and get user info
- `list_designs.py` - List all designs with metadata
- `list_folders.py` - List folder structure
- `get_design_details.py` - Get detailed info about a specific design
- `list_folder_contents.py` - List items in a specific folder

### Action Scripts (Require Confirmation)
- `export_design.py` - Export a design to specified format
- `create_folder.py` - Create a new folder
- `move_items.py` - Move items between folders
- `upload_asset.py` - Upload an image/video to Canva
- `create_design.py` - Create a new blank design
- `batch_export.py` - Export multiple designs at once

## API Rate Limits

Be aware of Canva API rate limits:
- List operations: 100 requests/user
- Create/Update operations: 20-30 requests/user
- Export operations: 20 requests/user

For bulk operations, implement delays between requests.

## Usage Examples

### Example 1: Explore Canva Account
```
User: "Show me what's in my Canva account"

[PLAN MODE]
1. Will run auth_check.py to verify connection
2. Will run list_designs.py to get all designs
3. Will run list_folders.py to get folder structure
4. Will present summary of account contents

[CLARIFY MODE]
"I'll list your designs and folders. Do you want me to also show:
- Detailed page counts for each design?
- Asset library contents?
- Recent activity?"

[IMPLEMENT MODE]
*Run scripts and present organized results*
```

### Example 2: Export Presentation
```
User: "Export my presentation called 'Q4 Report' as PDF"

[PLAN MODE]
1. Search for design named "Q4 Report"
2. Found: Design ID xyz123, 15 pages, Presentation type
3. Will export as PDF format
4. Will save to output folder

[CLARIFY MODE]
"I found 'Q4 Report' (15 pages). Confirming:
- Export format: PDF
- Include all 15 pages?
- Save location: ./output/Q4_Report.pdf
Proceed?"

[IMPLEMENT MODE]
*Export and provide download link*
```

### Example 3: Organize Folder
```
User: "Move all my Instagram posts to a folder called 'Social Media 2024'"

[PLAN MODE]
1. List all designs with type "Instagram Post"
2. Found: 23 Instagram post designs
3. Check if folder "Social Media 2024" exists
4. Create folder if needed, then move all 23 designs

[CLARIFY MODE]
"I found 23 Instagram post designs. Here are the first 5:
- 'Summer Sale Post' (created Jan 15)
- 'New Product Launch' (created Jan 20)
...
Should I move ALL 23, or would you like to review the full list first?"

[IMPLEMENT MODE]
*Create folder and move items with progress updates*
```

## Safety Guidelines

1. **Never modify without confirmation** - Always get explicit approval
2. **Prefer copies over originals** - For risky operations, suggest working on copies
3. **Batch operations need extra care** - Show sample of items before bulk changes
4. **Export originals before deletion** - If user wants to delete, export first
5. **Log everything** - All operations are logged to output folder
6. **Rate limit awareness** - Don't exceed API limits; implement delays

## Troubleshooting

### Authentication Issues
```bash
python scripts/auth_check.py
```
If this fails, re-run OAuth flow or refresh tokens.

### Design Not Found
- Check exact spelling and case
- Try listing all designs to find the correct name
- Designs may be in trash or shared with you

### Export Failures
- Some formats require Canva Pro
- Very large designs may timeout
- Check design isn't corrupted

## Resources

- [Canva Connect API Docs](https://www.canva.dev/docs/connect/)
- [Canva Developer Portal](https://www.canva.com/developers/)
- [API Rate Limits](https://www.canva.dev/docs/connect/rate-limits/)

## Todo List Tracking (REQUIRED)

**ALWAYS use TodoWrite** to track progress for Canva operations:

```json
[
  {"content": "Check API authentication", "status": "in_progress", "activeForm": "Checking authentication"},
  {"content": "List user's designs", "status": "pending", "activeForm": "Listing designs"},
  {"content": "Export requested design", "status": "pending", "activeForm": "Exporting design"},
  {"content": "Confirm completion", "status": "pending", "activeForm": "Confirming completion"}
]
```

This gives users visibility into progress and ensures all steps are completed.

## File Outputs

All outputs are saved to the `output/` folder:
- Exported files (PDFs, images, etc.)
- Operation logs with timestamps
- JSON responses from API calls
