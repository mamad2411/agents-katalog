---
name: file-manage
description: "Perform file CRUD operations in the shared volume at {{SHARED_VOLUME}}."
metadata:
  openclaw:
    emoji: "📁"
---

# File Management

Manage files in the shared volume at `{{SHARED_VOLUME}}`.

## Operations

```bash
# List files
ls -la {{SHARED_VOLUME}}/

# Create directory
mkdir -p {{SHARED_VOLUME}}/output/reports

# Copy files
cp {{SHARED_VOLUME}}/input/data.csv {{SHARED_VOLUME}}/output/data_backup.csv

# Move/rename files
mv {{SHARED_VOLUME}}/output/temp.txt {{SHARED_VOLUME}}/output/final.txt

# Find files by pattern
find {{SHARED_VOLUME}} -name "*.json" -type f

# Check file size
du -sh {{SHARED_VOLUME}}/input/*
```

## Tips for AI Agents

- Always use absolute paths within the shared volume.
- Use `find` with `-mtime` to locate recently modified files.
- Use `stat` to check file permissions and timestamps.
