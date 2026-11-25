# Google Drive Skill

Interact with Google Drive across multiple Google accounts. Search files, upload documents and videos, create folders, and organize your Drive.

## Features

- **Multi-account support** - Use different profiles for business and personal accounts
- **File search** - Find files by name, type, date, and more
- **Standard upload** - Upload documents, images, and regular files
- **Large file upload** - Resumable uploads for videos and large files with progress tracking
- **Folder management** - Create folders and organize uploads
- **List contents** - Browse folder contents

## Profiles

| Profile | Account | Usage |
|---------|---------|-------|
| `default` | Primary account | `--profile default` |

Add more profiles in `~/.claude/integrations/google/credentials/` as `token.<profile>.json`.

## Quick Start

```bash
# Search for files
uv run .claude/skills/google-drive/scripts/search.py --query "name contains 'invoice'"

# Upload a file to business account
uv run .claude/skills/google-drive/scripts/upload.py --file report.pdf --profile default

# Upload a video to personal account (with progress)
uv run .claude/skills/google-drive/scripts/upload_large.py --file video.mp4 --profile youtube

# Create a folder
uv run .claude/skills/google-drive/scripts/create_folder.py --name "Client Deliverables"

# List folder contents
uv run .claude/skills/google-drive/scripts/list.py
```

## Scripts

| Script | Purpose | Example |
|--------|---------|---------|
| [search.py](scripts/search.py) | Search files | `--query "mimeType='application/pdf'"` |
| [upload.py](scripts/upload.py) | Standard upload | `--file document.pdf --folder-id <id>` |
| [upload_large.py](scripts/upload_large.py) | Large file upload | `--file video.mp4 --profile youtube` |
| [create_folder.py](scripts/create_folder.py) | Create folder | `--name "Projects" --parent-id <id>` |
| [list.py](scripts/list.py) | List folder | `--folder-id <id> --format json` |

## Search Query Examples

```
name contains 'report'              Files with 'report' in name
mimeType = 'application/pdf'        PDF files only
mimeType contains 'video'           Video files
modifiedTime > '2024-01-01T00:00:00'  Modified after date
trashed = false                     Exclude trashed files
'me' in owners                      Files you own
```

Combine with `and`/`or`:
```
name contains 'invoice' and mimeType contains 'pdf'
```

See [Drive search parameters](https://developers.google.com/drive/api/guides/search-files).

## Setup

Google OAuth setup is done once via the plugin README — it covers Drive automatically.

If Drive access is missing, add the scope:

```bash
uv run ~/.claude/plugins/cache/riccardovandra/cc-plugin-productivity-suite/integrations/google/scripts/oauth_setup.py --add-scope drive
```

## Module

The [drive_client.py](modules/drive_client.py) module provides a Python API:

```python
from drive_client import DriveClient

# Initialize with profile
client = DriveClient(profile='default')

# Search
files = client.search("name contains 'contract'")

# Upload
result = client.upload('document.pdf', folder_id='<folder_id>')

# Large upload with progress
def show_progress(pct): print(f"{pct}%")
result = client.upload_large('video.mp4', progress_callback=show_progress)

# Create folder
folder = client.create_folder('Client Work', parent_id='<parent_id>')

# List contents
items = client.list_folder('<folder_id>')
```

## Output Styles

This skill works with any output style. No specific recommendation.
