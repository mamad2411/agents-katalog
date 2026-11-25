---
name: canva-folder-organizer
description: |
  Organize and manage folders in your Canva account. Use this skill when user wants to
  create folders, move designs between folders, rename folders, or organize their
  Canva project structure. Follows 3-mode workflow to prevent accidental moves or deletions.
  For viewing folder contents use canva-explorer first.
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

# Canva Folder Organizer Skill

> **QUICK REFERENCE**
> - **Scripts location**: `scripts/` (NOT `skills/canva-folder-organizer/scripts/` - those don't exist)
> - **List folders**: `.venv\Scripts\python.exe scripts/list_folders.py`
> - **List designs**: `.venv\Scripts\python.exe scripts/list_designs.py`
> - **API client**: `scripts/canva_client.py` (import: `from canva_client import get_client`)
> - **Sample script**: `scripts/samples/sample_canva_operations.py`
>
> **WARNING**: Commands below referencing `skills/canva-*/scripts/*.py` are WRONG paths.
> Write custom Python using `canva_client.py`. See `scripts/samples/sample_canva_operations.py`.

Manage and organize your Canva folder structure and move items between folders.

## Scope of This Skill

**This skill handles:**
- Create new folders
- Rename folders
- Delete folders
- Move designs between folders
- Move assets between folders
- Organize folder hierarchy
- Bulk organization operations

**NOT handled by this skill:**
- Viewing folder contents → Use `canva-explorer`
- Editing designs → Use `canva-image-editor`, `canva-presentation`
- Uploading assets → Use `canva-asset-manager`
- Exporting → Use `canva-export`

## Folder Structure in Canva

```
Canva Account
├── Projects (root)
│   ├── Folder 1
│   │   ├── Subfolder A
│   │   └── Subfolder B
│   └── Folder 2
├── Uploads (uploads)
│   └── [Uploaded assets]
└── Trash
    └── [Deleted items]
```

### Special Folder IDs
- `root` - Top level Projects folder
- `uploads` - User's Uploads folder

## 3-Mode Workflow

### MODE 1: PLAN

1. **Map Current Structure**
   ```python
   # Get current folder structure
   python skills/canva-explorer/scripts/list_folders.py --depth 5
   ```

2. **Identify Changes Needed**
   ```
   ## Folder Organization Plan

   ### Current Structure
   Projects/
   ├── Marketing (12 items)
   ├── Sales (8 items)
   ├── Random (45 items) ← Needs organization
   └── Old Stuff (20 items)

   ### Proposed Changes

   1. CREATE: "Marketing/2024-Q1"
   2. CREATE: "Marketing/2024-Q2"
   3. MOVE: 15 designs from "Random" → "Marketing/2024-Q1"
   4. RENAME: "Old Stuff" → "Archive-2023"
   5. DELETE: Empty folder "Untitled"

   ### Items to Move
   | Design | From | To |
   |--------|------|-----|
   | "Jan Campaign" | Random | Marketing/2024-Q1 |
   | "Feb Promo" | Random | Marketing/2024-Q1 |
   ...

   ### Safety Notes
   - "Random" will have 30 items remaining after move
   - Delete operation for "Untitled" is safe (empty)
   ```

### MODE 2: CLARIFY

Folder-specific questions:

1. **Create Operations**
   - "Where should the new folder be created? (root or inside another folder)"
   - "What should the folder be named?"

2. **Move Operations**
   - "I found 15 items matching 'Marketing'. Move all of them?"
   - "Some items have similar names - should I list them for review?"

3. **Delete Operations**
   - "This folder contains 5 items. They will be moved to Trash. Proceed?"
   - "This is permanent after 30 days in Trash. Confirm deletion?"

4. **Bulk Operations**
   - "Organize all 45 items in 'Random' or specific ones?"
   - "Should I auto-categorize based on design type?"

### MODE 3: IMPLEMENT

```python
# Create folder
python skills/canva-folder-organizer/scripts/create_folder.py \
  --name "2024-Q1" \
  --parent "MARKETING_FOLDER_ID"

# Rename folder
python skills/canva-folder-organizer/scripts/rename_folder.py \
  --folder "FOLDER_ID" \
  --new-name "Archive-2023"

# Move single item
python skills/canva-folder-organizer/scripts/move_item.py \
  --item "DESIGN_ID" \
  --to-folder "TARGET_FOLDER_ID"

# Move multiple items
python skills/canva-folder-organizer/scripts/move_items.py \
  --items "ID1,ID2,ID3" \
  --to-folder "TARGET_FOLDER_ID"

# Delete folder
python skills/canva-folder-organizer/scripts/delete_folder.py \
  --folder "FOLDER_ID" \
  --confirm true
```

## Available Scripts

### Folder Management
- `create_folder.py` - Create new folder
- `rename_folder.py` - Rename existing folder
- `delete_folder.py` - Delete folder (moves to trash)
- `get_folder_info.py` - Get folder details

### Item Movement
- `move_item.py` - Move single item
- `move_items.py` - Move multiple items
- `move_by_type.py` - Move items by design type
- `move_by_date.py` - Move items by creation date

### Organization Helpers
- `auto_organize.py` - Suggest organization structure
- `find_duplicates.py` - Find duplicate designs
- `find_empty_folders.py` - List empty folders
- `flatten_folder.py` - Move all subfolder contents up

## Organization Strategies

### By Project
```
Projects/
├── Project Alpha/
│   ├── Designs/
│   ├── Assets/
│   └── Exports/
├── Project Beta/
│   ├── Designs/
│   ├── Assets/
│   └── Exports/
```

### By Date
```
Projects/
├── 2024/
│   ├── Q1/
│   ├── Q2/
│   ├── Q3/
│   └── Q4/
├── 2023/
│   └── Archive/
```

### By Type
```
Projects/
├── Social Media/
│   ├── Instagram/
│   ├── Facebook/
│   └── LinkedIn/
├── Presentations/
├── Marketing Materials/
└── Brand Assets/
```

### By Client
```
Projects/
├── Client A/
│   ├── Active/
│   └── Completed/
├── Client B/
│   ├── Active/
│   └── Completed/
└── Internal/
```

## Bulk Organization

### Auto-Organize by Type
```python
# Analyze folder and suggest organization
python skills/canva-folder-organizer/scripts/auto_organize.py \
  --folder "RANDOM_FOLDER_ID" \
  --strategy "by-type" \
  --dry-run true  # Preview only

# Output:
# Would create:
#   - Social Media/ (25 items)
#   - Presentations/ (10 items)
#   - Documents/ (5 items)
#   - Other/ (5 items)
```

### Auto-Organize by Date
```python
python skills/canva-folder-organizer/scripts/auto_organize.py \
  --folder "FOLDER_ID" \
  --strategy "by-date" \
  --granularity "month" \
  --dry-run true

# Output:
# Would create:
#   - 2024-01/ (15 items)
#   - 2024-02/ (12 items)
#   - 2024-03/ (18 items)
```

### Clean Up Empty Folders
```python
# Find empty folders
python skills/canva-folder-organizer/scripts/find_empty_folders.py

# Output:
# Empty folders found:
#   - Untitled (ID: xxx)
#   - Old Campaign (ID: yyy)
#   - Test (ID: zzz)

# Delete all empty folders
python skills/canva-folder-organizer/scripts/delete_empty_folders.py \
  --confirm true
```

## Safety Guidelines

1. **Always preview first** - Use `--dry-run` for bulk operations
2. **Confirm moves** - Especially for large numbers of items
3. **Document before delete** - List folder contents before deletion
4. **Check dependencies** - Some folders may have shared items
5. **Trash is recoverable** - Deleted items go to Trash for 30 days

## Example Interactions

### "Create a new folder for Q1 marketing"
```
[PLAN]
- Will create folder named "Q1 Marketing"
- Location: Inside "Marketing" folder (or root)

[CLARIFY]
- "Create inside Marketing folder or at root level?"
- "Should I create subfolders too? (Designs, Assets, etc.)"

[IMPLEMENT]
- Create folder at specified location
- Return new folder ID
```

### "Move all Instagram posts to Social Media folder"
```
[PLAN]
- Search for Instagram post type designs
- Found: 23 Instagram posts
- Target: Social Media folder

[CLARIFY]
- "Found 23 Instagram posts. Move all to Social Media folder?"
- "Should I create an 'Instagram' subfolder?"

[IMPLEMENT]
- Move items in batches
- Report progress
- Confirm completion
```

### "Organize my messy 'Random' folder"
```
[PLAN]
- Analyze "Random" folder contents
- 45 items: 20 social posts, 10 presentations, 15 misc

[CLARIFY]
- "I suggest organizing by type:"
  - Social Media/ (20 items)
  - Presentations/ (10 items)
  - Miscellaneous/ (15 items)
- "Approve this organization?"

[IMPLEMENT]
- Create subfolders
- Move items to appropriate folders
- Report final structure
```

## Rate Limits

Folder operations have rate limits:
- Create/Update: 20 requests/user
- Move operations: 100 requests/user
- List operations: 100 requests/user

For large moves, implement delays between requests.

## Output Files

Operations are logged to:
- `output/folders/operations.json` - All folder operations
- `output/folders/moves.json` - Item movement history
- `output/folders/structure.json` - Current folder structure
