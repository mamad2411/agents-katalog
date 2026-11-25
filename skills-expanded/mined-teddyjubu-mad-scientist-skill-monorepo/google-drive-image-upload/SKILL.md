---
name: google-drive-image-upload
description: google-drive-image-upload lets the user automatically upload generated images to Charles's Google Drive folder for permanent backup, which is useful when they want to preserve visual assets, keep a centralized media library, or ensure important images are never lost if local storage or Telegram messages get cleared.
---

## What This Skill Does

This skill google-drive-image-upload lets the user automatically upload generated images to Charles's Google Drive folder for permanent backup, which is useful when they want to preserve visual assets, keep a centralized media library, or ensure important images are never lost if local storage or Telegram messages get cleared.

## Google Drive Image Upload

After generating any image output for Charles, upload a copy to his Google Drive folder.

### Target Folder
- Folder URL: https://drive.google.com/drive/u/1/folders/1ssT8OozmF9U69B8wz6vY30fMVK9TOWv1
- Folder ID: `1ssT8OozmF9U69B8wz6vY30fMVK9TOWv1`

### Setup (One Time)
1. OAuth client secret is stored on server
2. User must click the auth URL and return the authorization code
3. Exchange code for refresh token, save to `~/.config/googledrive/token.json`
4. Use `google-api-python-client` or `rclone` for uploads

### Upload Command (once auth is set up)
```python
# Use google-api-python-client with service account or OAuth
# Upload to folder ID: 1ssT8OozmF9U69B8wz6vY30fMVK9TOWv1
```

### IMPORTANT
- "gog" CLI is NOT installed on Hermes — it existed in OpenClaw but did not migrate
- Do NOT tell Charles to use "gog" — use python API or rclone instead
- Always auto-upload images to Drive AS WELL AS sending to Telegram

### Pending
- OAuth token exchange still needs user authorization (auth URL provided, awaiting code return)