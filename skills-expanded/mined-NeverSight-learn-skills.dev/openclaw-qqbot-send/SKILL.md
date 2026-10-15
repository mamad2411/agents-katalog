---
name: openclaw-qqbot-send-skill
description: Stage and send local media files through OpenClaw QQBot with safe temporary staging and automatic cleanup
triggers:
  - send a file through QQBot
  - how do I send local media with OpenClaw QQBot
  - stage a file for QQBot sending
  - send image/audio/video through QQ bot
  - clean up QQBot staged files
  - how to send local files with qqmedia tags
  - OpenClaw QQBot media relay
  - QQBot file size limit
---

# OpenClaw QQBot Send Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

An OpenClaw skill for safely sending local files, images, audio, video, and other media through QQBot. This skill stages local files into the QQBot media relay directory, sends them with `<qqmedia>...</qqmedia>` tags, and cleans up only the temporary staged copy after sending.

## What It Does

- **Stages local files** into `~/.openclaw/media/qqbot/` with unique filenames
- **Sends media** through QQBot using `<qqmedia>...</qqmedia>` XML tags
- **Cleans up safely** by removing only the staged temporary copy, never the original
- **Enforces 10 MB limit** for file size safety
- **Supports HTTP(S) URLs** directly without staging or cleanup
- **Normalizes extensions** to lowercase for consistency

## Installation

Clone the repository:

```bash
git clone https://github.com/ZJunCher/openclaw-qqbot-send-skill.git
cd openclaw-qqbot-send-skill
```

The skill uses Python's standard library only (no external dependencies required).

## Key Components

### `scripts/stage_media.py`

The core staging and cleanup script with two operations:

1. **Stage**: Copy a local file to `~/.openclaw/media/qqbot/` with a unique name
2. **Cleanup**: Delete the staged temporary copy after sending

### `SKILL.md`

OpenClaw skill definition that tells the AI agent when and how to stage, send, and clean up media files.

## Usage Patterns

### Pattern 1: Send a Local File

```python
import subprocess
import os

# Step 1: Stage the local file
source_file = "/home/user/Pictures/photo.jpg"
result = subprocess.run(
    ["python", "scripts/stage_media.py", source_file],
    capture_output=True,
    text=True,
    check=True
)
staged_path = result.stdout.strip()

# Step 2: Send with QQBot using qqmedia tags
qqbot_message = f"<qqmedia>{staged_path}</qqmedia>"
# ... send qqbot_message through your QQBot integration ...

# Step 3: Clean up the staged copy
subprocess.run(
    ["python", "scripts/stage_media.py", "--cleanup", staged_path],
    check=True
)
```

### Pattern 2: Send an HTTP(S) URL

```python
# No staging or cleanup needed for URLs
url = "https://example.com/image.png"
qqbot_message = f"<qqmedia>{url}</qqmedia>"
# ... send directly through QQBot ...
```

### Pattern 3: Batch Send Multiple Files

```python
import subprocess

files = [
    "/path/to/image1.png",
    "/path/to/video.mp4",
    "/path/to/audio.mp3"
]

staged_files = []

try:
    # Stage all files
    for source in files:
        result = subprocess.run(
            ["python", "scripts/stage_media.py", source],
            capture_output=True,
            text=True,
            check=True
        )
        staged_path = result.stdout.strip()
        staged_files.append(staged_path)
        
        # Send each file
        qqbot_message = f"<qqmedia>{staged_path}</qqmedia>"
        # ... send through QQBot ...
        
finally:
    # Always clean up all staged files
    for staged in staged_files:
        subprocess.run(
            ["python", "scripts/stage_media.py", "--cleanup", staged],
            check=False  # Don't fail if cleanup fails
        )
```

## Command-Line Interface

### Stage a File

```bash
python scripts/stage_media.py <source_path>
```

**Input**: Path to the original file  
**Output**: Absolute path to the staged copy in `~/.openclaw/media/qqbot/`

Example:

```bash
python scripts/stage_media.py "/home/user/document.pdf"
# Output: /home/user/.openclaw/media/qqbot/a1b2c3d4.pdf
```

### Clean Up a Staged File

```bash
python scripts/stage_media.py --cleanup <staged_path>
```

**Input**: The exact path returned by the staging command  
**Output**: Success or error message

Example:

```bash
python scripts/stage_media.py --cleanup "/home/user/.openclaw/media/qqbot/a1b2c3d4.pdf"
```

## Configuration

### File Size Limit

Default: **10 MB**

The script enforces this limit during staging. To modify:

```python
# In scripts/stage_media.py, locate:
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Change to desired size, e.g., 20 MB:
MAX_FILE_SIZE = 20 * 1024 * 1024
```

### Media Relay Directory

Default: `~/.openclaw/media/qqbot/`

The script automatically creates this directory if it doesn't exist. To change the location, modify the `MEDIA_DIR` constant in `scripts/stage_media.py`.

## Safety Rules

### Critical: Only Clean Up Staged Paths

**DO**:
```python
staged = subprocess.run(["python", "scripts/stage_media.py", source], ...).stdout.strip()
subprocess.run(["python", "scripts/stage_media.py", "--cleanup", staged], ...)
```

**DON'T**:
```python
# NEVER clean up the original source
subprocess.run(["python", "scripts/stage_media.py", "--cleanup", source], ...)

# NEVER clean up HTTP(S) URLs
subprocess.run(["python", "scripts/stage_media.py", "--cleanup", url], ...)

# NEVER guess or construct the staged path
subprocess.run(["python", "scripts/stage_media.py", "--cleanup", "~/.openclaw/media/qqbot/file.txt"], ...)
```

### What Gets Deleted

- ✅ **Staged copy** in `~/.openclaw/media/qqbot/`
- ❌ **Original source file** (never touched)

## Troubleshooting

### File Too Large

**Error**: "File size exceeds 10 MB limit"

**Solution**: Reduce file size or increase `MAX_FILE_SIZE` in the script.

### File Not Found

**Error**: "Source file does not exist"

**Solution**: Verify the path is correct and the file exists:

```python
import os
if os.path.exists(source_file):
    # proceed with staging
else:
    print(f"File not found: {source_file}")
```

### Permission Denied

**Error**: "Permission denied" or "Access denied"

**Solution**: Check file permissions and ensure the script has read access to the source file and write access to `~/.openclaw/media/qqbot/`.

### Cleanup Fails After Successful Send

**Best Practice**: Always attempt cleanup even if sending fails:

```python
staged_path = None
try:
    staged_path = stage_file(source)
    send_to_qqbot(staged_path)
except Exception as e:
    print(f"Send failed: {e}")
finally:
    if staged_path:
        try:
            cleanup_file(staged_path)
        except Exception as e:
            print(f"Cleanup failed for {staged_path}: {e}")
            # Log but don't delete manually
```

## Integration Example

Complete flow for OpenClaw QQBot integration:

```python
#!/usr/bin/env python3
import subprocess
import sys
import os

def send_media_to_qqbot(source_path):
    """Stage, send, and clean up media for QQBot."""
    
    # Check if it's a URL
    if source_path.startswith(("http://", "https://")):
        print(f"Sending URL directly: {source_path}")
        qqbot_message = f"<qqmedia>{source_path}</qqmedia>"
        # Send through QQBot API here
        return True
    
    # Check if file exists
    if not os.path.exists(source_path):
        print(f"Error: File not found: {source_path}")
        return False
    
    staged_path = None
    try:
        # Stage the file
        result = subprocess.run(
            ["python", "scripts/stage_media.py", source_path],
            capture_output=True,
            text=True,
            check=True
        )
        staged_path = result.stdout.strip()
        print(f"Staged to: {staged_path}")
        
        # Send through QQBot
        qqbot_message = f"<qqmedia>{staged_path}</qqmedia>"
        print(f"Sending: {qqbot_message}")
        # ... actual QQBot send logic here ...
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Staging failed: {e.stderr}")
        return False
        
    finally:
        # Always clean up the staged file
        if staged_path:
            try:
                subprocess.run(
                    ["python", "scripts/stage_media.py", "--cleanup", staged_path],
                    check=True
                )
                print(f"Cleaned up: {staged_path}")
            except subprocess.CalledProcessError as e:
                print(f"Cleanup failed: {e.stderr}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: send_media.py <file_path_or_url>")
        sys.exit(1)
    
    send_media_to_qqbot(sys.argv[1])
```

## License

MIT License
