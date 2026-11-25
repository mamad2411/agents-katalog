---
name: claude-vision-skill
description: Use when the user shares, pastes, or references an image (local path or URL) and you need to describe, analyze, or recognize its content, especially when the current model cannot read images directly. Run the bundled vision.js helper to convert the image into text.
---

# Vision Helper

The current model may not support native image input. When the user provides an image path or URL, do not rely on viewing the image directly. Instead run the bundled `vision.js` helper (resolve it against this skill's base directory — the directory that contains this SKILL.md, which the loader tells you):

```powershell
node "<base_directory>\vision.js" "<absolute image path>" "<prompt>"
```

For an image URL:

```powershell
node "<base_directory>\vision.js" --url "<image url>" "<prompt>"
```

When the user pastes an image into the chat but no file path or URL is visible:

```powershell
node "<base_directory>\vision.js" --clipboard "<prompt>"
```

`--clipboard` reads the current image from the system clipboard (Windows uses the bundled `clipboard.ps1`; the pasted image is usually still there). If it fails, ask the user to save the image to a file and provide the absolute path.

Fallback rules (automatic):

- If a local path is given but the file does not exist, vision.js automatically falls back to the clipboard.
- If no image path or URL is given at all, vision.js automatically tries the clipboard.
- Pass `--no-fallback` to disable this behavior and fail with an explicit error instead.

Rules:

- Always use the absolute path to `vision.js`.
- Use an absolute image path for local files, or `--url` for remote images.
- Prefer `--clipboard` when the user pasted an image with no accessible path.
- Use Chinese for descriptions unless the user asks otherwise.
- Configuration lives in `.env` next to `vision.js` (`DASHSCOPE_API_KEY`, `VISION_MODEL`, `DASHSCOPE_BASE_URL`). Never print or commit the API key.
- If the API call fails, report the error to the user and ask them to check the key, model, or base URL.
