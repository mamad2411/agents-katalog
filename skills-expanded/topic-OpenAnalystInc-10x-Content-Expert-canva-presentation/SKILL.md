---
name: canva-presentation
description: |
  Work with Canva presentations, slideshows, and multi-page documents. Use this skill when
  user wants to create, edit, or manage presentations. Handles slide operations like
  adding/removing slides, reordering, editing individual slides, and bulk updates.
  Follows 3-mode workflow: PLAN, CLARIFY, IMPLEMENT for safe operations.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
---

# Canva Presentation Skill

> **QUICK REFERENCE**
> - **Scripts location**: `scripts/` (NOT `skills/canva-presentation/scripts/` - those don't exist)
> - **Auth check**: `.venv\Scripts\python.exe scripts/auth_check.py`
> - **List designs**: `.venv\Scripts\python.exe scripts/list_designs.py`
> - **Export**: `.venv\Scripts\python.exe scripts/export_design.py --id "ID" --format pptx`
> - **API client**: `scripts/canva_client.py` (import: `from canva_client import get_client`)
> - **Sample script**: `scripts/samples/sample_canva_operations.py`
>
> **WARNING**: Commands below referencing `skills/canva-presentation/scripts/*.py` are WRONG paths.
> Write custom Python using `canva_client.py`. See `scripts/samples/sample_canva_operations.py`.

Specialized skill for working with Canva presentations, slideshows, and multi-page documents.

## Scope of This Skill

**This skill handles:**
- Presentations (16:9, 4:3)
- Slideshows
- Pitch Decks
- Multi-page Documents
- Whiteboards with multiple frames
- Any design with multiple pages/slides

**Operations supported:**
- View all slides in a presentation
- Edit individual slide content
- Add new slides
- Remove slides
- Reorder slides
- Duplicate slides
- Apply consistent styling across slides
- Export to PPTX or PDF

## 3-Mode Workflow

### MODE 1: PLAN

1. **Load Presentation Structure**
   ```python
   # Get presentation overview
   python skills/canva-presentation/scripts/get_presentation.py \
     --id "DESIGN_ID" \
     --include-thumbnails
   ```

2. **Document Slide Analysis**
   ```
   ## Presentation Analysis: "[Name]"

   ### Overview
   - Total Slides: 15
   - Dimensions: 1920x1080 (16:9)
   - Created: 2024-01-15
   - Last Modified: 2024-02-20

   ### Slide Breakdown
   | # | Title | Elements | Notes |
   |---|-------|----------|-------|
   | 1 | Cover Slide | Logo, Title, Subtitle | |
   | 2 | Agenda | 5 bullet points | |
   | 3 | Introduction | Text, Image | |
   ...

   ### Proposed Changes
   1. Update slide 3 headline
   2. Add new slide after slide 5
   3. Remove slide 12
   4. Reorder slides 8-10
   ```

### MODE 2: CLARIFY

Critical questions for presentations:

1. **Slide Identification**
   - "Which slide number? Or can you describe it?"
   - "Slide 5 has title 'Q3 Results' - is this the one?"

2. **Content Changes**
   - "What should the new text say?"
   - "Should I maintain the current bullet format?"

3. **Structural Changes**
   - "Where should the new slide be inserted?"
   - "This will shift all subsequent slide numbers. Proceed?"

4. **Bulk Operations**
   - "Apply this change to all 15 slides or specific ones?"
   - "Should I update the master template instead?"

### MODE 3: IMPLEMENT

```python
# Get slide details
python skills/canva-presentation/scripts/get_slide.py \
  --design "DESIGN_ID" \
  --slide 3

# Update slide content
python skills/canva-presentation/scripts/update_slide.py \
  --design "DESIGN_ID" \
  --slide 3 \
  --element "headline" \
  --text "New Headline"

# Add new slide
python skills/canva-presentation/scripts/add_slide.py \
  --design "DESIGN_ID" \
  --position 6 \
  --template "blank"

# Remove slide
python skills/canva-presentation/scripts/remove_slide.py \
  --design "DESIGN_ID" \
  --slide 12

# Reorder slides
python skills/canva-presentation/scripts/reorder_slides.py \
  --design "DESIGN_ID" \
  --order "1,2,3,4,5,8,9,10,6,7,11,12,13,14,15"

# Duplicate slide
python skills/canva-presentation/scripts/duplicate_slide.py \
  --design "DESIGN_ID" \
  --slide 5 \
  --position 6
```

## Available Scripts

### Analysis Scripts
- `get_presentation.py` - Full presentation overview
- `get_slide.py` - Detailed info for one slide
- `analyze_structure.py` - Template and master analysis
- `extract_all_text.py` - Get all text from all slides
- `compare_slides.py` - Find similar/duplicate slides

### Edit Scripts
- `update_slide.py` - Modify slide content
- `add_slide.py` - Insert new slide
- `remove_slide.py` - Delete a slide
- `duplicate_slide.py` - Copy a slide
- `reorder_slides.py` - Change slide order
- `batch_update.py` - Apply changes to multiple slides
- `update_master.py` - Modify master template

### Creation Scripts
- `create_presentation.py` - New presentation
- `create_from_template.py` - From Canva template

## Slide Types

Common slide layouts:
- **Title Slide**: Main title and subtitle
- **Title + Content**: Header with body text
- **Two Column**: Side-by-side content
- **Image + Text**: Split layout
- **Full Image**: Background image
- **Quote**: Featured quote
- **Chart/Graph**: Data visualization
- **Comparison**: Two items side by side
- **Timeline**: Sequential events
- **Team**: Profile cards
- **Thank You**: Closing slide

## Presentation Dimensions

| Type | Dimensions | Aspect Ratio |
|------|------------|--------------|
| Widescreen | 1920x1080 | 16:9 |
| Standard | 1024x768 | 4:3 |
| Portrait | 1080x1920 | 9:16 |
| Square | 1080x1080 | 1:1 |
| A4 | 595x842 | ~1:1.4 |
| Letter | 612x792 | ~1:1.3 |

## Bulk Operations

For changes across multiple slides:

```python
# Update all headlines
python skills/canva-presentation/scripts/batch_update.py \
  --design "DESIGN_ID" \
  --element-type "headline" \
  --font "Montserrat" \
  --slides "all"

# Update footer on specific slides
python skills/canva-presentation/scripts/batch_update.py \
  --design "DESIGN_ID" \
  --element-type "footer" \
  --text "Confidential" \
  --slides "2,3,4,5,6,7,8"

# Apply color scheme
python skills/canva-presentation/scripts/batch_update.py \
  --design "DESIGN_ID" \
  --primary-color "#2E86AB" \
  --secondary-color "#F4D35E" \
  --slides "all"
```

## Safety Guidelines

1. **Confirm slide numbers** - Always verify which slide before editing
2. **Document before removal** - List slide content before deleting
3. **Backup for reorder** - Note original order before reordering
4. **Test on copy first** - For major restructuring
5. **Check dependencies** - Some slides may reference others

## Example Interactions

### "Show me the slides in my pitch deck"
```
[PLAN]
- Retrieve presentation structure
- Generate slide overview with titles

[CLARIFY]
- None needed for read-only operation

[IMPLEMENT]
- Display slide list with thumbnails
```

### "Update the Q3 numbers on slide 7"
```
[PLAN]
- Get slide 7 details
- Identify numeric elements
- Document current values

[CLARIFY]
- "Slide 7 shows: Revenue $1.2M, Growth 15%"
- "What are the new numbers?"

[IMPLEMENT]
- Update specified values
- Verify formatting maintained
```

### "Add a new slide about our team after the intro"
```
[PLAN]
- Identify intro slide (slide 2)
- New team slide will be slide 3
- All subsequent slides shift by 1

[CLARIFY]
- "Should I use a team template?"
- "What team info should be included?"
- "This will renumber slides 3→4, 4→5, etc."

[IMPLEMENT]
- Insert slide at position 3
- Add content as specified
- Confirm new structure
```

## Export Options

For presentations:
- **PDF** - Static document
- **PPTX** - Editable PowerPoint
- **PNG/JPG** - Individual slide images
- **Video** - Animated slideshow (if applicable)

Use `canva-export` skill for actual export operations.

## Output Files

- `output/presentations/` - Presentation data
- `output/slide_thumbnails/` - Slide images
- `output/logs/presentation_edits.json` - Change history
