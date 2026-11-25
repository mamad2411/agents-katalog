---
name: ProjectOrganizer
description: Organize folder structures, cleanup projects, create templates. USE WHEN organize, clean up, structure folder, reorganize, naming convention.
---

# ProjectOrganizer

Audit, clean, and organize project folder structures.

---

## Trigger Phrases

- "organize this folder"
- "clean up the structure"
- "help me reorganize"
- "what do we have here"
- "list everything"
- "create a template"
- "apply naming convention"

---

## Workflow Routing

| Trigger | Workflow |
|---------|----------|
| "organize", "clean up" | `Workflows/Audit.md` |
| "list", "what do we have" | `Workflows/Inventory.md` |
| "create template" | `Workflows/CreateTemplate.md` |
| "archive", "move old" | `Workflows/Archive.md` |

---

## Standard Folder Structures

### Project Folder (Agency/Client Work)
```
project-name/
├── README.md           # Project overview
├── SPEC.md             # Requirements/spec
├── meeting/            # Meeting transcripts & notes
│   └── YYYY-MM-DD-topic.md
├── assets/             # Raw inputs from client
├── output/             # Deliverables
├── _internal/          # Internal notes (not shared)
└── archive/            # Old versions
```

### Event Folder
```
event-YYYY-MM-DD-name/
├── README.md           # Event overview
├── slides/             # Presentation files
├── scripts/            # Speaking scripts
├── data/               # Attendee data, responses
├── assets/             # Images, media
└── follow-up/          # Post-event materials
```

### Guild/Organization Folder
```
guild-name/
├── README.md           # Overview
├── 1-events/           # Event folders
├── 2-community/        # Community resources
├── 3-vibe-ops/         # Operations
│   ├── projects/       # Active projects
│   └── deals/          # Pipeline tracking
├── 4-agency/           # Client work
│   └── projects/       # Client folders
└── archive/            # Completed/old
```

---

## Naming Conventions

### Folders
- **Projects:** `clientcode-project-name` (e.g., `roland001-personal-brand`)
- **Events:** `YYYY-MM-DD-event-name` (e.g., `2026-01-16-cc-workshop`)
- **General:** `lowercase-with-dashes`

### Files
- **Docs:** `TitleCase.md` or `lowercase-with-dashes.md`
- **Data:** `YYYY-MM-DD-description.ext`
- **Versions:** `filename-v1.ext`, `filename-v2.ext`

### Prefix Conventions
- `_internal/` - Not for sharing
- `_archive/` - Old versions
- `_temp/` - Temporary files (delete later)

---

## Audit Process

### Step 1: Inventory
List all contents with:
- File/folder count
- Types of content
- Last modified dates
- Size (if relevant)

### Step 2: Identify Issues
- [ ] Inconsistent naming
- [ ] Duplicates
- [ ] Orphaned files
- [ ] Missing structure
- [ ] Old/stale content

### Step 3: Propose Changes
Present reorganization plan:
- What to rename
- What to move
- What to archive
- What to delete
- New folders to create

### Step 4: Execute (with approval)
- Create new structure
- Move files
- Rename as needed
- Archive old content

---

## Quick Commands

### `list`
Show folder contents with context

### `audit`
Full structure analysis with recommendations

### `apply-naming`
Fix naming to match conventions

### `create-structure`
Create standard folder structure

### `archive-old`
Move old content to archive

---

## Integration

- **MeetingProcessor:** Ensure meeting outputs go to correct folders
- **FounderOps:** Set up new project folders properly
- **DailyUpdate:** Track organization tasks

---

## Example

**Request:** "organize the my-project folder"

**Output:**
```markdown
## Folder Audit: my-project

### Current State
- 4 main directories
- 12 project subfolders
- Mixed naming conventions
- Some orphaned files in root

### Issues Found
1. ❌ `16jan-cc-event` should be `1-events/2026-01-16-cc-workshop`
2. ❌ `vibe-ops` should be `3-vibe-ops`
3. ❌ Loose files in root: `notes.md`, `todo.txt`
4. ❌ Duplicate: `proposal.md` and `proposal-v2.md`

### Proposed Changes
1. Move event folder to events directory
2. Rename vibe-ops with prefix
3. Move loose files to appropriate locations
4. Archive old proposal, keep v2

### Execute?
[y/n]
```
