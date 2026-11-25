---
name: canva-explorer
description: |
  Explore and discover your Canva account contents. Use this skill when the user wants to
  see what designs, folders, or assets they have. Lists designs with metadata, shows folder
  structure, displays account information. READ-ONLY operations - never modifies anything.
  Perfect for: "What's in my Canva?", "Show my designs", "List my folders", "Find design X".
allowed-tools:
  - Bash
  - Read
  - Write
---

# Canva Explorer Skill

> **QUICK REFERENCE**
> - **Scripts location**: `scripts/` (NOT `skills/*/scripts/` - those paths don't exist)
> - **Auth check**: `.venv\Scripts\python.exe scripts/auth_check.py`
> - **List designs**: `.venv\Scripts\python.exe scripts/list_designs.py`
> - **List folders**: `.venv\Scripts\python.exe scripts/list_folders.py`
> - **Export design**: `.venv\Scripts\python.exe scripts/export_design.py --id "ID" --format pdf`
> - **Sample script**: `scripts/samples/sample_canva_operations.py`
> - **Always use**: `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (Mac/Linux)
>
> **WARNING**: Commands below referencing `skills/canva-explorer/scripts/*.py` are WRONG paths.
> Use the actual scripts: `scripts/auth_check.py`, `scripts/list_designs.py`, `scripts/list_folders.py`.
> For custom operations, write Python using `from canva_client import get_client` (see `scripts/samples/sample_canva_operations.py`).

A **read-only** skill for discovering and browsing your Canva account. This skill NEVER modifies anything - it only retrieves and displays information.

## When to Use This Skill

Use this skill when the user wants to:
- See what designs they have
- Browse their folder structure
- Find a specific design by name
- Get details about a design (pages, dimensions, type)
- View their account information
- List assets in their library
- Search for designs by type or date

## Workflow

### Step 1: Understand the Query
Determine what the user wants to explore:
- All designs? Specific folder? Specific design?
- Need metadata? Just names? Page counts?

### Step 2: Run Discovery Scripts
Execute the appropriate script(s):

```bash
# Get account info and verify connection
python skills/canva-explorer/scripts/auth_check.py

# List all designs
python skills/canva-explorer/scripts/list_designs.py

# List folder structure
python skills/canva-explorer/scripts/list_folders.py

# Get specific design details
python skills/canva-explorer/scripts/get_design.py --id "DESIGN_ID"

# List folder contents
python skills/canva-explorer/scripts/list_folder_contents.py --folder "FOLDER_ID"

# Search designs by name
python skills/canva-explorer/scripts/search_designs.py --query "search term"
```

### Step 3: Present Results Clearly
Format the results in a user-friendly way:

```
## Your Canva Account

### Account Info
- User: [Display Name]
- Team: [Team Name if applicable]

### Designs (Total: X)
| Name | Type | Pages | Created | Last Modified |
|------|------|-------|---------|---------------|
| ... | ... | ... | ... | ... |

### Folders
- Projects (root)
  - Folder 1 (X items)
    - Subfolder A (Y items)
  - Folder 2 (Z items)
```

## Available Scripts

### `auth_check.py`
Verifies API credentials and returns user info.

**Output:**
```json
{
  "user_id": "...",
  "display_name": "...",
  "team_id": "...",
  "capabilities": ["..."]
}
```

### `list_designs.py`
Lists all designs in the account.

**Arguments:**
- `--limit N` - Max number to return (default: 50)
- `--type TYPE` - Filter by design type (presentation, instagram_post, etc.)
- `--sort FIELD` - Sort by field (created_at, modified_at, title)

**Output:** JSON array of design objects

### `list_folders.py`
Returns the folder tree structure.

**Arguments:**
- `--depth N` - How deep to traverse (default: 3)

**Output:** Nested folder structure with item counts

### `get_design.py`
Gets detailed information about a specific design.

**Arguments:**
- `--id DESIGN_ID` - The design ID (required)
- `--include-pages` - Also fetch page thumbnails

**Output:** Complete design metadata including owner, URLs, dimensions

### `list_folder_contents.py`
Lists items within a specific folder.

**Arguments:**
- `--folder FOLDER_ID` - Folder ID ("root" for Projects, "uploads" for Uploads)
- `--type TYPE` - Filter by item type (design, folder, image)

**Output:** Array of items in the folder

### `search_designs.py`
Searches designs by name or metadata.

**Arguments:**
- `--query TEXT` - Search term
- `--type TYPE` - Filter by design type

**Output:** Matching designs

## Design Types in Canva

Common design types you'll encounter:
- `presentation` - Presentations/Slideshows
- `instagram_post` - Instagram Posts
- `instagram_story` - Instagram Stories
- `facebook_post` - Facebook Posts
- `poster` - Posters
- `flyer` - Flyers
- `document` - Documents
- `whiteboard` - Whiteboards
- `video` - Videos
- `logo` - Logos
- `business_card` - Business Cards
- `invitation` - Invitations
- `resume` - Resumes
- `infographic` - Infographics

## Special Folder IDs

- `root` - Top level of Projects
- `uploads` - User's Uploads folder
- `trash` - Deleted items (if accessible)

## Example Interactions

### "What designs do I have?"
```python
# Run: list_designs.py
# Present summary table of all designs
```

### "Show me my presentations"
```python
# Run: list_designs.py --type presentation
# Present only presentation designs
```

### "What's in my 'Marketing' folder?"
```python
# First: list_folders.py to find Marketing folder ID
# Then: list_folder_contents.py --folder MARKETING_ID
```

### "Tell me about my design called 'Annual Report'"
```python
# Run: search_designs.py --query "Annual Report"
# Then: get_design.py --id FOUND_ID --include-pages
# Present detailed info with page thumbnails
```

## Output Location

All exploration results are saved to:
- `output/explorations/` - JSON data files
- `output/logs/` - Operation logs

## Safety Notes

- This skill is **completely safe** - it only reads data
- No designs, folders, or assets are ever modified
- Results are cached locally for quick re-access
- Large accounts may take time to fully enumerate
