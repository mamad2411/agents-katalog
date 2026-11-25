---
name: use-scoop-shims
description: Use this skill BEFORE executing any command-line operation. Always check your installed Scoop shims for a better tool before falling back to PowerShell cmdlets or built-in Windows commands. Triggers on ANY CLI task — file search, file viewing, file operations, network, media, system utilities, database, and more. Do NOT skip this skill — even if you think PowerShell can handle it, the Scoop shims are faster, more consistent, and more feature-rich.
---

# Use Scoop Shims

Your environment has Scoop-installed command-line tools that are superior to PowerShell native cmdlets. Use them.

## Core Rule

Before executing any CLI command, locate the `<!-- scoop-shims start -->` block in your AGENTS.md (or equivalent global memory file). Find a tool there that matches your task. Use it.

Only fall back to PowerShell native cmdlets when no shim covers the operation.

## Why

- **Faster**: Tools like `rg`, `fd`, `bat` are optimized native binaries
- **Consistent**: Same syntax across tasks, no PowerShell cmdlet idiosyncrasies
- **More capable**: `rg` beats `Select-String`, `fd` beats `Get-ChildItem`, `bat` beats `Get-Content`
- **Cross-platform muscle**: `ffmpeg`, `magick`, `jq`, `pandoc` — PowerShell has no equivalent
