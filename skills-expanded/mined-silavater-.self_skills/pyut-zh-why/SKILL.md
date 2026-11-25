---
name: pyut-zh-why
description: Use when Codex is about to read, inspect, quote, summarize, or display text files on Windows/PowerShell that may contain Chinese or CJK text. Prefer Python file reads over PowerShell Get-Content, cat, or type to avoid mojibake.
---

# Pyut Zh Why

When reading file contents that may contain Chinese or CJK text on Windows, use Python first.

Do not use PowerShell `Get-Content`, `cat`, or `type` for the file content.

Use an available Python executable (`python`, `py -3`, or the runtime supplied by the environment). Replace `PYTHON_EXE` with the actual executable:

```powershell
& "PYTHON_EXE" -c "from pathlib import Path; import sys; sys.stdout.reconfigure(encoding='utf-8'); print(Path(sys.argv[1]).read_text(encoding='utf-8-sig', errors='replace'))" "PATH_HERE"
```

For snippets, still slice in Python. Do not pipe the target file text through PowerShell. If Python is unavailable, say the PowerShell output may be unreliable for Chinese text.
