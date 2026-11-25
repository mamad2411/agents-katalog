---
name: gabito-terminal
description: Replaces a failing or noisy shell command with a short Python script run from .gabitotl/tmp/. Trigger: before shell work, scripts or any remote operation; a shell command fails or its output is mangled; or the task is log, file, JSON, API or report analysis.
license: Apache-2.0
metadata:
  author: gabitotl
  version: "1.0"
---

# Gabito terminal: Python instead of fighting the shell

## When to use

- A shell command failed and the cause looks like quoting, escaping or line breaks.
- The command is multiline, deeply quoted, or relies on PowerShell/cmd escaping.
- The output is mangled, truncated or too noisy to read.
- Any remote operation (SSH, remote hosts, file transfer, authenticated sessions): see Remote operations below.
- The task is analysis: logs, file discovery, text processing, JSON/YAML/XML, API calls, reports, diagnostics.

## When NOT to use

- A simple one-line command that works. Keep it as it is.
- The task needs a real interactive tool (editor, REPL, pager).
- Python is missing. Say so and fall back to the simplest single-line command.

## Noisy commands: use `gabitotl run`

For any command with long output (tests, builds, linters, installs) run `gabitotl run -- <command> [args...]`
instead of the bare command. It prints the exit code, the failures and the last lines, and saves the full output to
`.gabitotl/tmp/run-<time>.log`. Read that log only when the digest is not enough, and then by targeted search
(`rg -n "pattern" <log>`), never whole.

## Procedure

1. Do not retry the same command. After the first failure, switch to a script.
2. Write a short script to `.gabitotl/tmp/<purpose>.py` (the folder is git-ignored).
3. Run it with `python3` (or `python` on Windows) and read its output.
4. Delete the script when you are done.

Python is the default for analysis on every OS (logs, file discovery, text processing, JSON/YAML/XML,
API calls, reports, diagnostics). Use PowerShell only for Windows-specific work (services, Active
Directory, networking, native cmdlets); avoid PowerShell one-liners and long pipelines when Python can
do it. Simple one-line commands that work stay as they are.

## Rules

- Use `pathlib` for paths. Never build paths by string concatenation.
- Use `subprocess.run([...], capture_output=True, text=True)` with an argument list, never `shell=True`.
- Print compact results: counts, the first matches, a short summary. Never dump whole files.
- Never print, log or hardcode secrets, tokens or passwords.
- Keep scripts small and single-purpose. One script, one question.

## Remote operations

Local permission does not authorize remote work. Before using SSH, remote hosts, file transfer or any
authenticated session, get the user's explicit OK for the destination, the operation and the credential
to use. Never discover or reuse ambient SSH agents, sockets or sessions. If anything is unclear, ask and
stay local.

## Template: search files for a pattern

```python
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
pattern = re.compile(sys.argv[2] if len(sys.argv) > 2 else "TODO")
skip = {".git", "node_modules", ".venv", "__pycache__"}
hits = 0
for path in root.rglob("*"):
    if not path.is_file() or skip & set(path.parts):
        continue
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        continue
    for number, line in enumerate(lines, 1):
        if pattern.search(line):
            hits += 1
            if hits <= 50:
                print(f"{path}:{number}: {line.strip()[:120]}")
print(f"{hits} match(es)")
```

## Template: extract fields from JSON

```python
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
fields = sys.argv[2:] or ["name"]
items = data if isinstance(data, list) else [data]
for item in items[:50]:
    print({f: item.get(f) for f in fields})
print(f"{len(items)} item(s)")
```
