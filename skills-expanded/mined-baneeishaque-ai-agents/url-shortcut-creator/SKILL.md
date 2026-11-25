---
name: url-shortcut-creator
description: Create cross-platform HTML redirect shortcut files for any URL — works on macOS, Windows, and Linux by double-click.
category: File-Utilities
---

# URL Shortcut Creator Skill (v1)

This is a **base** skill. It creates a self-contained `.html` file that
redirects to a target URL when opened in any browser. Double-clicking the file
on macOS, Windows, or Linux opens the URL. Domain-agnostic — usable by any
workflow needing a clickable bookmark file.

***

## 1. Scope & Intent

- **In scope**: Create an `.html` file with a `meta http-equiv="refresh"` redirect to any URL.
- **Out of scope**:
    - Native OS shortcut formats (`.url` for Windows, `.webloc` for macOS) —
      the HTML format is the universal cross-platform fallback.
    - Opening the browser or managing bookmarks.
    - URL validation beyond basic format checks.

***

## 2. Environment & Dependencies

### 2.1 Runtime

- **Python 3.12+** — scripts use `argparse`, `os`, `sys`. Verify:

  ```bash
  python3 --version
  ```

No external libraries required.

***

## 3. Protocol

### 3.1 Step 1 — Create Shortcut

```bash
python3 .agents/skills/url-shortcut-creator/scripts/create-url-shortcut.py \
  --url "<target-url>" \
  --name "<filename-without-extension>" \
  [--output-dir "<path>"]
```

The script:

1. Creates a valid `.html` file with meta-refresh redirect to the target URL.
2. Prints the absolute path of the created file to stdout.
3. Exits 0 on success.

#### 3.1.1 Arguments

| Argument       | Required | Description                                           |
|----------------|----------|-------------------------------------------------------|
| `--url`        | Yes      | Target URL (e.g. `https://youtu.be/abc123`)           |
| `--name`       | Yes      | Filename without extension (e.g. `my-video`)          |
| `--output-dir` | No       | Output directory (default: current working directory) |

#### 3.1.2 Output

The script prints the absolute path of the created `.html` file:

```text
/Users/user/Desktop/my-video.html
```

***

## 4. Edge Cases

- **URL contains special characters**: The script emits the URL directly into
  HTML attribute values. URLs containing `"` (double quotes) would break the
  HTML. The script does not validate for this — the caller MUST ensure the URL
  is well-formed.
- **Output directory does not exist**: The script creates it via `os.makedirs`.
- **File already exists**: The script overwrites without warning. The caller SHOULD check or use a unique name.

***

## 5. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
| --- | --- |
| [`youtube-video-upload`](../youtube-video-upload/SKILL.md) | Calls `scripts/create-url-shortcut.py` after upload to create clickable `.html` shortcut |
