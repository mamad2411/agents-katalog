---
name: canva-export
description: |
  Export Canva designs to various formats (PDF, PNG, JPG, PPTX, MP4, GIF). Use this skill
  when user wants to download, export, or save their designs. Handles single and bulk
  exports with format options. Follows 3-mode workflow for confirmation.
  For editing designs use other specialized skills (canva-image-editor, canva-presentation).
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
---

# Canva Export Skill

> **QUICK REFERENCE**
> - **Export script**: `.venv\Scripts\python.exe scripts/export_design.py --id "DESIGN_ID" --format pdf`
> - **Auth check**: `.venv\Scripts\python.exe scripts/auth_check.py`
> - **List designs first**: `.venv\Scripts\python.exe scripts/list_designs.py`
> - **Sample script**: `scripts/samples/sample_canva_operations.py`
> - **Output**: `output/exports/` or `output/pdf/`, `output/pptx/`
>
> **WARNING**: Commands below referencing `skills/canva-export/scripts/*.py` are WRONG paths.
> Use: `scripts/export_design.py`. For custom operations, see `scripts/samples/sample_canva_operations.py`.

Export Canva designs to various file formats for download and use.

## Scope of This Skill

**This skill handles:**
- Export to PDF
- Export to PNG/JPG
- Export to PPTX (PowerPoint)
- Export to MP4 (video)
- Export to GIF
- Single design exports
- Bulk/batch exports
- Export with options (quality, pages, etc.)

**NOT handled by this skill:**
- Editing designs → Use `canva-image-editor`, `canva-presentation`, or `canva-video`
- Uploading assets → Use `canva-asset-manager`
- Browsing designs → Use `canva-explorer`

## Export Formats

| Format | Best For | Supports |
|--------|----------|----------|
| **PDF** | Documents, Print | Multi-page, High quality |
| **PNG** | Web, Transparency | Single/Multi-page, Lossless |
| **JPG** | Photos, Social | Single/Multi-page, Compressed |
| **PPTX** | Presentations | Multi-page, Editable |
| **MP4** | Videos | Animation, Audio |
| **GIF** | Animations | No audio, Looping |
| **SVG** | Vector graphics | Scalable, Limited support |

## 3-Mode Workflow

### MODE 1: PLAN

1. **Identify Export Target**
   ```python
   # Get design info
   python skills/canva-explorer/scripts/get_design.py --id "DESIGN_ID"

   # Check available export formats
   python skills/canva-export/scripts/get_export_formats.py --id "DESIGN_ID"
   ```

2. **Document Export Plan**
   ```
   ## Export Plan

   ### Design(s) to Export
   - "Q4 Report" (15 pages, Presentation)
   - Design ID: abc123

   ### Export Details
   - Format: PDF
   - Quality: High
   - Pages: All (1-15)
   - Estimated Size: ~5MB

   ### Output Location
   - File: output/exports/Q4_Report.pdf
   ```

### MODE 2: CLARIFY

Export-specific questions:

1. **Format Selection**
   - "What format do you need? (PDF, PNG, PPTX, etc.)"
   - "For presentations, PDF or editable PPTX?"

2. **Quality Options**
   - "Standard or high quality?"
   - "Compression level for images?"

3. **Page Selection**
   - "Export all 15 pages or specific ones?"
   - "Each page as separate file or combined?"

4. **Bulk Export**
   - "Export all 10 designs in the folder?"
   - "Same format for all, or different per design?"

### MODE 3: IMPLEMENT

```python
# Single design export
python skills/canva-export/scripts/export_design.py \
  --id "DESIGN_ID" \
  --format pdf \
  --quality high \
  --output "output/exports/"

# Export specific pages
python skills/canva-export/scripts/export_design.py \
  --id "DESIGN_ID" \
  --format png \
  --pages "1,3,5" \
  --output "output/exports/"

# Batch export
python skills/canva-export/scripts/batch_export.py \
  --designs "ID1,ID2,ID3" \
  --format pdf \
  --output "output/exports/"

# Export folder contents
python skills/canva-export/scripts/export_folder.py \
  --folder "FOLDER_ID" \
  --format png \
  --output "output/exports/"
```

## Available Scripts

### Export Scripts
- `export_design.py` - Export single design
- `batch_export.py` - Export multiple designs
- `export_folder.py` - Export all designs in folder
- `get_export_formats.py` - Check available formats
- `check_export_status.py` - Monitor async export

### Utility Scripts
- `download_export.py` - Download completed export
- `convert_format.py` - Convert between formats locally
- `compress_export.py` - Reduce file size

## Export Options

### PDF Options
```python
python skills/canva-export/scripts/export_design.py \
  --id "DESIGN_ID" \
  --format pdf \
  --quality high \           # standard, high
  --pages all \              # all, or "1,2,3"
  --flatten true \           # Flatten for print
  --output "output/"
```

### PNG/JPG Options
```python
python skills/canva-export/scripts/export_design.py \
  --id "DESIGN_ID" \
  --format png \
  --quality high \           # standard, high
  --transparent true \       # PNG only
  --scale 2 \                # 1x, 2x, 4x
  --pages all \
  --output "output/"
```

### PPTX Options
```python
python skills/canva-export/scripts/export_design.py \
  --id "DESIGN_ID" \
  --format pptx \
  --output "output/"
```

### MP4 Options
```python
python skills/canva-export/scripts/export_design.py \
  --id "DESIGN_ID" \
  --format mp4 \
  --quality 1080p \          # 720p, 1080p, 4k
  --fps 30 \                 # Frame rate
  --output "output/"
```

### GIF Options
```python
python skills/canva-export/scripts/export_design.py \
  --id "DESIGN_ID" \
  --format gif \
  --quality standard \
  --loop true \
  --output "output/"
```

## Batch Export

For exporting multiple designs:

```python
# Export by design IDs
python skills/canva-export/scripts/batch_export.py \
  --designs "id1,id2,id3,id4" \
  --format pdf \
  --naming "original" \      # original, numbered, custom
  --output "output/batch/"

# Export all in folder
python skills/canva-export/scripts/export_folder.py \
  --folder "FOLDER_ID" \
  --format png \
  --output "output/batch/"

# Export with different formats
python skills/canva-export/scripts/batch_export.py \
  --designs "id1:pdf,id2:png,id3:pptx" \
  --output "output/batch/"
```

## Export Process

Canva exports are **asynchronous**:

1. **Initiate Export** - Request export, get job ID
2. **Poll Status** - Check if export is ready
3. **Download** - Get file from temporary URL

```python
# The export script handles this automatically
# For manual control:

# Step 1: Start export
job_id = start_export(design_id, format)

# Step 2: Wait for completion
status = check_status(job_id)  # "in_progress", "completed", "failed"

# Step 3: Download when ready
download_url = get_download_url(job_id)  # Valid for 24 hours
```

## File Naming

Output files are named:
- `{design_name}.{format}` - Default
- `{design_name}_page{N}.{format}` - Multi-page individual
- `{design_name}_{timestamp}.{format}` - With timestamp

## Rate Limits

Export API limits:
- 20 export requests per user (then wait)
- 120 status checks per user
- Downloads have 24-hour validity

For large batch exports, implement delays between requests.

## Safety Guidelines

1. **Verify design before export** - Ensure correct design
2. **Check available formats** - Not all formats work for all designs
3. **Monitor export status** - Large files take time
4. **Download promptly** - URLs expire in 24 hours
5. **Check disk space** - Large exports need room

## Example Interactions

### "Export my presentation as PDF"
```
[PLAN]
- Design: "Q4 Report" (15 pages)
- Format: PDF
- Output: output/exports/Q4_Report.pdf

[CLARIFY]
- "Export all 15 pages?"
- "High or standard quality?"

[IMPLEMENT]
- Start export job
- Monitor completion
- Download file
- "Exported to: output/exports/Q4_Report.pdf (2.3MB)"
```

### "Export all designs in my Marketing folder"
```
[PLAN]
- Folder: "Marketing" (8 designs)
- List: Instagram_Post_1, Instagram_Post_2, ...

[CLARIFY]
- "Export all 8 designs?"
- "What format for each? (PDF, PNG, JPG)"
- "Same format for all?"

[IMPLEMENT]
- Batch export with delays
- Report progress (1/8, 2/8, ...)
- List all output files
```

## Output Location

All exports saved to:
- `output/exports/` - Single exports
- `output/batch/` - Batch exports
- `output/logs/export_log.json` - Export history

## Troubleshooting

### Export Stuck "In Progress"
- Large files take longer
- Check status after 5 minutes
- Retry if still stuck

### Format Not Available
- Not all formats work for all design types
- Videos can't export as PDF
- Check `get_export_formats.py` first

### Download Failed
- URL may have expired (24 hour limit)
- Re-export if needed
- Check network connectivity
