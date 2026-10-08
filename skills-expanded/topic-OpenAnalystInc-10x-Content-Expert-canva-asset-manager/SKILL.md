---
name: canva-asset-manager
description: |
  Upload and manage assets (images, videos, audio) in your Canva account. Use this skill
  when user wants to upload files to Canva, manage their asset library, or work with
  uploaded media. Handles image, video, and audio uploads. Follows 3-mode workflow.
  For organizing uploaded assets use canva-folder-organizer.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# Canva Asset Manager Skill

> **QUICK REFERENCE**
> - **Scripts location**: `scripts/` (NOT `skills/canva-asset-manager/scripts/` - those don't exist)
> - **Auth check**: `.venv\Scripts\python.exe scripts/auth_check.py`
> - **API client**: `scripts/canva_client.py` (import: `from canva_client import get_client`)
> - **Sample script**: `scripts/samples/sample_canva_operations.py`
>
> **WARNING**: Commands below referencing `skills/canva-asset-manager/scripts/*.py` are WRONG paths.
> Write custom Python using `canva_client.py`. See `scripts/samples/sample_canva_operations.py`.

Upload and manage media assets in your Canva account.

## Scope of This Skill

**This skill handles:**
- Upload images to Canva
- Upload videos to Canva
- Upload audio files to Canva
- Manage uploaded assets (rename, delete)
- View asset library
- Add tags to assets
- URL-based uploads

**NOT handled by this skill:**
- Using assets in designs → Use `canva-image-editor`
- Organizing into folders → Use `canva-folder-organizer`
- Exporting designs → Use `canva-export`

## Supported File Types

### Images
| Format | Max Size | Notes |
|--------|----------|-------|
| PNG | 25MB | Supports transparency |
| JPG/JPEG | 25MB | Best for photos |
| SVG | 3MB | Vector graphics |
| GIF | 25MB | Static or animated |
| WebP | 25MB | Modern format |
| HEIC | 25MB | Apple format |

### Videos
| Format | Max Size | Notes |
|--------|----------|-------|
| MP4 | 1GB | Most common |
| MOV | 1GB | Apple format |
| WebM | 1GB | Web format |
| M4V | 1GB | Apple format |

### Audio
| Format | Max Size | Notes |
|--------|----------|-------|
| MP3 | 250MB | Most common |
| WAV | 250MB | High quality |
| M4A | 250MB | Apple format |
| OGG | 250MB | Open format |

## 3-Mode Workflow

### MODE 1: PLAN

1. **Identify Upload Requirements**
   ```python
   # Check what files need uploading
   # Verify file types and sizes
   # Determine upload destination
   ```

2. **Document Upload Plan**
   ```
   ## Asset Upload Plan

   ### Files to Upload
   | File | Type | Size | Status |
   |------|------|------|--------|
   | hero-image.png | PNG | 2.1MB | Ready ✓ |
   | promo-video.mp4 | MP4 | 45MB | Ready ✓ |
   | logo.svg | SVG | 120KB | Ready ✓ |

   ### Upload Destination
   - Folder: Uploads (default) or specific folder

   ### Naming Convention
   - Keep original names OR
   - Rename to: project_asset_date format

   ### Tags to Apply
   - "Project Alpha"
   - "2024"
   - "Marketing"
   ```

### MODE 2: CLARIFY

Upload-specific questions:

1. **File Verification**
   - "Upload all 5 images or select specific ones?"
   - "File 'large-video.mp4' is 500MB. This may take time. Proceed?"

2. **Naming**
   - "Keep original filenames or rename?"
   - "Use a naming pattern like 'project_001'?"

3. **Organization**
   - "Upload to default Uploads folder or specific folder?"
   - "Create a new folder for these uploads?"

4. **Tagging**
   - "Add any tags for easy searching later?"
   - "Apply project name as tag?"

### MODE 3: IMPLEMENT

```python
# Upload single file
python skills/canva-asset-manager/scripts/upload_asset.py \
  --file "path/to/image.png" \
  --name "Custom Name" \
  --tags "tag1,tag2"

# Upload multiple files
python skills/canva-asset-manager/scripts/batch_upload.py \
  --folder "input/images/" \
  --pattern "*.png" \
  --tags "batch-upload"

# Upload from URL
python skills/canva-asset-manager/scripts/upload_from_url.py \
  --url "https://example.com/image.png" \
  --name "Downloaded Image"

# Update asset metadata
python skills/canva-asset-manager/scripts/update_asset.py \
  --id "ASSET_ID" \
  --name "New Name" \
  --tags "new-tag,another-tag"

# Delete asset
python skills/canva-asset-manager/scripts/delete_asset.py \
  --id "ASSET_ID" \
  --confirm true
```

## Available Scripts

### Upload Scripts
- `upload_asset.py` - Upload single file
- `batch_upload.py` - Upload multiple files
- `upload_from_url.py` - Upload from URL
- `check_upload_status.py` - Check async upload progress

### Management Scripts
- `list_assets.py` - List uploaded assets
- `get_asset.py` - Get asset details
- `update_asset.py` - Update name/tags
- `delete_asset.py` - Delete asset
- `search_assets.py` - Search by name/tag

### Utility Scripts
- `validate_files.py` - Check file compatibility
- `resize_before_upload.py` - Resize large images
- `convert_format.py` - Convert to supported format

## Upload Process

Canva uploads are **asynchronous**:

```python
# Step 1: Initiate upload
job_id = start_upload(file_path, metadata)

# Step 2: Upload file data
upload_file_data(job_id, file_bytes)

# Step 3: Poll for completion
while True:
    status = check_status(job_id)
    if status == "completed":
        asset_id = get_asset_id(job_id)
        break
    elif status == "failed":
        handle_error()
        break
    time.sleep(2)
```

The scripts handle this automatically.

## Batch Upload

For uploading multiple files:

```python
# Upload all PNGs from a folder
python skills/canva-asset-manager/scripts/batch_upload.py \
  --folder "input/images/" \
  --pattern "*.png" \
  --naming "original" \
  --tags "project-x,batch-2024"

# Upload with custom naming
python skills/canva-asset-manager/scripts/batch_upload.py \
  --folder "input/images/" \
  --pattern "*.jpg" \
  --naming "prefix" \
  --prefix "campaign_" \
  --tags "marketing"

# Upload specific files from list
python skills/canva-asset-manager/scripts/batch_upload.py \
  --files "file1.png,file2.jpg,file3.svg" \
  --tags "selected-uploads"
```

## URL Upload

Upload directly from URLs:

```python
# Single URL
python skills/canva-asset-manager/scripts/upload_from_url.py \
  --url "https://example.com/image.png" \
  --name "External Image"

# Multiple URLs from file
python skills/canva-asset-manager/scripts/batch_url_upload.py \
  --urls-file "input/urls.txt" \
  --tags "from-web"
```

**Note:** URL uploads have a 100MB limit.

## Asset Management

### Viewing Assets
```python
# List all uploaded assets
python skills/canva-asset-manager/scripts/list_assets.py

# Get specific asset details
python skills/canva-asset-manager/scripts/get_asset.py --id "ASSET_ID"

# Search by name
python skills/canva-asset-manager/scripts/search_assets.py --query "logo"

# Search by tag
python skills/canva-asset-manager/scripts/search_assets.py --tag "marketing"
```

### Updating Assets
```python
# Rename asset
python skills/canva-asset-manager/scripts/update_asset.py \
  --id "ASSET_ID" \
  --name "Better Name"

# Add tags
python skills/canva-asset-manager/scripts/update_asset.py \
  --id "ASSET_ID" \
  --tags "new-tag,another-tag" \
  --mode "add"

# Replace tags
python skills/canva-asset-manager/scripts/update_asset.py \
  --id "ASSET_ID" \
  --tags "only-this-tag" \
  --mode "replace"
```

### Deleting Assets
```python
# Delete single asset
python skills/canva-asset-manager/scripts/delete_asset.py \
  --id "ASSET_ID" \
  --confirm true

# Bulk delete by tag
python skills/canva-asset-manager/scripts/bulk_delete.py \
  --tag "temp-uploads" \
  --confirm true
```

## Input Folder

The `input/` folder is for files to upload:

```
input/
├── images/          # Images to upload
│   ├── hero.png
│   ├── banner.jpg
│   └── icons/
├── videos/          # Videos to upload
│   └── promo.mp4
├── audio/           # Audio to upload
│   └── background.mp3
└── urls.txt         # URLs for URL-based upload
```

## File Validation

Before uploading, validate files:

```python
python skills/canva-asset-manager/scripts/validate_files.py \
  --folder "input/images/"

# Output:
# Validation Results:
# ✓ hero.png - Valid (PNG, 2.1MB)
# ✓ banner.jpg - Valid (JPEG, 1.5MB)
# ✗ huge.png - Too large (30MB > 25MB limit)
# ✗ document.pdf - Unsupported format
```

## Resize Before Upload

For images that are too large:

```python
python skills/canva-asset-manager/scripts/resize_before_upload.py \
  --file "input/huge-image.png" \
  --max-size 25 \      # MB
  --output "input/resized/"
```

## Safety Guidelines

1. **Validate before upload** - Check file types and sizes
2. **Use meaningful names** - Makes assets easier to find
3. **Tag consistently** - Develop a tagging strategy
4. **Don't upload duplicates** - Check existing assets first
5. **Large files take time** - Be patient with video uploads

## Example Interactions

### "Upload my logo to Canva"
```
[PLAN]
- File: logo.png (500KB)
- Format: PNG ✓
- Size: Valid ✓

[CLARIFY]
- "Upload with name 'logo' or custom name?"
- "Add any tags?"

[IMPLEMENT]
- Upload file
- Return asset ID
- "Uploaded successfully: Asset ID xxx"
```

### "Upload all images from my folder"
```
[PLAN]
- Folder: input/campaign/
- Found: 12 images (8 PNG, 4 JPG)
- Total size: 15MB

[CLARIFY]
- "Upload all 12 images?"
- "Use original names or rename?"
- "Apply tags to all?"

[IMPLEMENT]
- Upload in batches
- Report progress
- List all asset IDs
```

### "Upload this video for my reel"
```
[PLAN]
- File: promo.mp4 (120MB)
- Format: MP4 ✓
- Duration: 30 seconds

[CLARIFY]
- "Video is 120MB, upload may take 1-2 minutes."
- "Any specific name for this video?"

[IMPLEMENT]
- Upload video
- Monitor progress
- Return asset ID when complete
```

## Rate Limits

Asset API limits:
- Upload initiation: 30 requests/user
- Status checks: 180 requests/user
- Updates: 30 requests/user

For bulk uploads, implement delays between requests.

## Output Files

Upload logs saved to:
- `output/uploads/upload_log.json` - All upload operations
- `output/uploads/assets.json` - Uploaded asset IDs and details
- `output/uploads/errors.json` - Failed uploads
