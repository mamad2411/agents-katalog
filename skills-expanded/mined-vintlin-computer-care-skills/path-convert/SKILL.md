---
name: path-convert
description: Use for path conversion when a user sends a Windows UNC path, macOS smb:// URL, /Volumes path, mounted share path, or asks to convert, normalize, open, or list a file-system path across Windows and macOS.
---

# Path Convert

## Overview

Handle file-system paths as data first. Preserve path components exactly, convert syntax only when the target platform is clear, and avoid inventing server/share mappings.

## Core Rules

1. **Identify** the input path type:
   - Windows UNC: `\\server\share\folder` or `\server\share\folder`
   - Windows local: `C:\Users\name\folder`
   - macOS SMB URL: `smb://server/share/folder`
   - macOS mounted volume: `/Volumes/share/folder` (contains only the mounted share name — do not infer a server name from it)
   - macOS local: `/Users/name/folder`

2. **Convert** only the path syntax by default. Preserve every directory/file component exactly unless the user explicitly gives a rename, replacement, or business mapping rule. Do not silently decode, rename, or translate folder names — the only exception is URL percent-decoding in `smb://` paths.

3. **Prefer** `smb://server/share/folder` as the macOS output for Windows UNC network paths (Finder opens it directly).

4. **Prefer** `\\server\share\folder` as the Windows output for `smb://` paths.

5. **Open** a path:
   - macOS: `open <path-or-smb-url>` in Finder.
   - Windows: `explorer <path>` in File Explorer.
   - If the current environment is not the target OS, provide the command the user should run — never claim a path was opened on the wrong OS.

6. **List** files:
   - List only files by default.
   - Use `--include-dirs` only when the user wants directories shown with files.
   - Use `--dirs-only` only when the user wants directories without files.
   - For `smb://` or UNC paths, listing requires the share to be mounted locally first; otherwise explain the mount requirement. Never claim `smb://` or UNC contents were listed before mounting.

7. **Constraints**:
   - Do not treat a Windows drive path as a real macOS mount unless the user confirms the mount layout.
   - Do not use for URL routing, shell glob expansion, application-specific import paths, or business-specific folder rewrites unless the user provides the mapping rule.

## Quick Reference

| Input | macOS form | Windows form |
| --- | --- | --- |
| `\\server\share\dir` | `smb://server/share/dir` | `\\server\share\dir` |
| `smb://server/share/dir` | `smb://server/share/dir` | `\\server\share\dir` |
| `/Volumes/share/dir` | `/Volumes/share/dir` | placeholder UNC without server |
| `C:\Users\name` | `/Volumes/C/Users/name` placeholder | `C:\Users\name` |

## Tool

Use `scripts/path_tool.py` for deterministic conversion, opening, and listing:

```bash
python3 scripts/path_tool.py convert --to mac '\\server\share\folder'
python3 scripts/path_tool.py convert --to windows 'smb://server/share/folder'
python3 scripts/path_tool.py open --to mac '\\server\share\folder'
python3 scripts/path_tool.py open --to windows 'smb://server/share/folder' --print-command
python3 scripts/path_tool.py list '/Volumes/share/folder'
python3 scripts/path_tool.py list --include-dirs '/Volumes/share/folder'
python3 scripts/path_tool.py list --dirs-only '/Volumes/share/folder'
```

The script prints the converted path. `open` also opens it when the host OS supports the requested file manager. `list` prints one absolute path per line and preserves visible path components without resolving symlinks.

## Response

- **Simple conversion**: answer with only the converted path unless explanation is requested.
- **Open requests**: state whether it was opened or provide the exact command to run.
- **List requests**: return matching paths, or summarize if output is too long.
- **Business rewrites**: ask for the mapping rule — only syntax conversion is safe without one.
