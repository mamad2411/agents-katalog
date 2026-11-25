---
name: local-pptx-editor
description: |
  Edit PowerPoint (PPTX) files locally without Canva API. Use this skill when user provides
  a PPTX file and wants to modify slides, update text, change images, or restructure content.
  Maintains original formatting, themes, animations, and layout. Does NOT require Canva.
  Output goes to output/ folder. Use for: "edit this presentation", "update slide 5", "change PPT text".
---

# Local PPTX Editor Skill

> **QUICK REFERENCE**
> - **Utility script**: `scripts/local/pptx_utils.py`
> - **Sample script**: `scripts/samples/sample_pptx_edit.py`
> - **Safe copy**: `scripts/local/safe_copy.py`
> - **Output folder**: `output/pptx/`
> - **Working folder**: `output/working/`
> - **Run with**: `.venv\Scripts\python.exe scripts/samples/sample_pptx_edit.py`
> - **3-Step workflow**: (1) Copy from `input/` to `output/working/` → (2) Edit the copy → (3) Save to `output/pptx/`
> - **Python**: ALWAYS use `.venv\Scripts\python.exe` (never bare `python`)

Edit and manipulate PowerPoint files locally without requiring Canva API.

## CRITICAL: Never Modify Original Files

1. **ALWAYS** copy the original to `output/working/` first
2. **ALL** edits happen on the copy
3. **SAVE** results to `output/pptx/`
4. **ORIGINAL** file remains untouched

## When to Use This Skill

Use this skill when:
- User provides a PPTX/PPT file and wants modifications
- Need to update slide content while maintaining design
- Need to add/remove/reorder slides
- Need to modify speaker notes
- **User has NOT explicitly asked to use Canva**

## Capabilities

### Read Operations
- Extract all text from slides
- Extract images from presentation
- Get slide layouts and themes
- Analyze slide structure
- Extract speaker notes

### Write Operations
- Modify text on any slide
- Replace images
- Add/delete/reorder slides
- Update speaker notes
- Bulk text replacement

### Conversion
- PPTX to PDF
- PPTX to images (one per slide)

## Running Python Scripts (Virtual Environment)

**IMPORTANT**: Always use the virtual environment Python:

```bash
# Windows
.venv\Scripts\python.exe scripts/local/script_name.py

# macOS/Linux
.venv/bin/python scripts/local/script_name.py
```

## Workflow

### Step 1: Create Safe Copy
```bash
.venv\Scripts\python.exe scripts/local/safe_copy.py --source "input/presentation.pptx"
```

### Step 2: Analyze
```bash
.venv\Scripts\python.exe scripts/local/pptx_utils.py "output/working/presentation_copy.pptx"
```

### Step 3: Make Modifications

Use the pptx_utils.py functions to:
- Replace text while preserving formatting
- Update specific slides
- Reorder slides

### Step 4: Save Result
Save to `output/pptx/presentation_modified.pptx`

## 3-Mode Workflow

### MODE 1: PLAN
- Analyze presentation structure
- List all slides with content summary
- Document proposed changes

### MODE 2: CLARIFY
- Confirm which slides to modify
- Verify text replacements
- Check formatting requirements

### MODE 3: IMPLEMENT
- Create working copy
- Apply modifications
- Save to output folder

## Maintaining Format Integrity

### Preservation Rules
1. **Theme & Master Slides** - Never modify unless requested
2. **Layouts** - Maintain placeholder positions
3. **Animations** - Keep existing animations
4. **Text Formatting** - Same font size, color, style

### Word Count Management
- Track original word count per slide
- Warn if new content differs significantly
- Suggest adjustments to maintain layout

## Research Capabilities

This skill can:
- Search for PowerPoint best practices
- Look up python-pptx documentation
- Research presentation design principles
- Find solutions to formatting challenges

## Available Scripts

- `pptx_utils.py` - Core PPTX analysis and manipulation
- `safe_copy.py` - Create working copies safely

## Todo List Tracking (REQUIRED)

**ALWAYS use TodoWrite** to track progress:

```json
[
  {"content": "Create safe working copy", "status": "in_progress", "activeForm": "Creating safe copy"},
  {"content": "Analyze presentation structure", "status": "pending", "activeForm": "Analyzing slides"},
  {"content": "Apply modifications", "status": "pending", "activeForm": "Applying changes"},
  {"content": "Save to output/pptx/", "status": "pending", "activeForm": "Saving result"}
]
```

## Output Location

- `output/pptx/` - Modified presentations
- `output/working/` - Working copies
