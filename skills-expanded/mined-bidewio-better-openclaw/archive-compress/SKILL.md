---
name: archive-compress
description: "Create and extract archives (tar, zip, gzip) in the shared volume at {{SHARED_VOLUME}}."
metadata:
  openclaw:
    emoji: "🗜️"
---

# Archive & Compress

Work with archives in the shared volume at `{{SHARED_VOLUME}}`.

## Create Archives

```bash
# tar.gz
tar -czf {{SHARED_VOLUME}}/output/archive.tar.gz -C {{SHARED_VOLUME}}/input .

# zip
zip -r {{SHARED_VOLUME}}/output/archive.zip {{SHARED_VOLUME}}/input/
```

## Extract

```bash
tar -xzf {{SHARED_VOLUME}}/input/archive.tar.gz -C {{SHARED_VOLUME}}/output/
unzip {{SHARED_VOLUME}}/input/archive.zip -d {{SHARED_VOLUME}}/output/
```

## Tips for AI Agents

- Use `tar -tf` or `unzip -l` to list contents without extracting.
- `gzip` for single files, `tar` for directories.
