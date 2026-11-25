---
name: cloudinary-upload
description: Upload local files or images to the project's Cloudinary CDN (cloud "cyeam") via the official `cld` CLI, replicating the /admin/upload behavior. Converts images to webp on storage and uploads into a target folder. Use when the user wants to upload images/files to Cloudinary, batch-upload a directory, or asks "上传图片到cloudinary", "传图", "upload to cloudinary".
---

# Cloudinary Upload (official CLI)

Replicates the `/admin/upload` flow (see `controllers/admin_controller.go` + `util/file_util.go`)
using the official Cloudinary CLI (`cld`). Images are converted to **webp** on storage and
uploaded into a target folder (flat, structure not preserved).

## Prerequisites

1. **Official CLI (`cld`) is installed automatically on first use** if missing (via `pip3 install --user cloudinary-cli`).
2. **Credentials via `CLOUDINARY_URL`** (do NOT hardcode secrets):
   ```bash
   export CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
   ```
   For this project the cloud name is `cyeam`. Get the key/secret from the constants in
   `controllers/admin_controller.go` or ask the user, then export the URL above before running.
   Verify with: `cld config` (should show the cyeam cloud).

## Upload single / multiple files

```bash
bash .agents/skills/cloudinary-upload/scripts/upload.sh -f uploads file1.png file2.jpg
```

- `-f FOLDER` — target Cloudinary asset folder (default: `uploads`)
- `-r` — keep original format (skip webp conversion)

Each file is uploaded with `public_id` = filename without extension, `overwrite=True`
(same as the existing backend). Images get `format=webp`; non-images are left as-is.

## Upload a directory (flat)

```bash
bash .agents/skills/cloudinary-upload/scripts/upload-dir.sh -f blog-images ./my-images
```

Uploads every top-level file in the directory into the one target folder. Folder structure is
NOT preserved (per project preference for a flat target). Add `-r` to skip webp conversion.

## What the scripts do

| Behavior | How |
|----------|-----|
| webp conversion | `format=webp` upload param on images |
| target folder | `folder=<FOLDER>` |
| overwrite | `overwrite=True` (matches existing `/admin/upload`) |
| public_id | filename without extension |
| non-image files | uploaded unchanged |

The underlying command is:
```bash
cld uploader upload <path> public_id=<name> asset_folder=<folder> overwrite=True format=webp
```

## Common mistakes

- **Missing `CLOUDINARY_URL`** → scripts exit with an error. Export it first.
- **Preserving directory structure** → use `cld upload_dir <dir> -f <folder>` directly instead;
  these scripts intentionally flatten.
- **Converting non-images** → webp conversion only applies to image extensions; other files
  upload untouched.
