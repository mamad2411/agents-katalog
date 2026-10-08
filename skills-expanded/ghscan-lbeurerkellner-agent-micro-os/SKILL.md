---
name: create-cap
description: "Create a cap CLI tool (.cap.py or .cap.js). Use when the user wants to write a new cap tool, add a cap script, author a capability-bound CLI, configure access/network/dependencies for a cap script, or install a tool into ~/.cap/tools/."
argument-hint: "Describe what the tool should do"
---

# Create a Cap Tool

`cap` runs `.cap.py` / `.cap.js` scripts inside capability-bound Docker containers.

Each script declares exactly what it needs — dependencies, filesystem access, network — and Docker enforces those limits.

## When to Use
- User wants to write a new `cap` tool or script
- User asks how to configure access, network, or dependencies for a cap script
- User wants to install a tool so it's runnable by name (e.g. `cap markitdown`)

---

## Anatomy of a Cap Script

```python
#!/bin/cap
# ---
# name: my-tool
# description: One-line description shown by 'cap list'
# dependencies: ['pypi:requests', 'npm:lodash']
# platform: linux/amd64
# access: ['data/**', '$@']
# network: ['api.example.com', '*.github.com']
# ---

import requests
# … script body
```

### JavaScript variant
```js
#!/bin/cap
// ---
// name: my-tool
// description: One-line description
// dependencies: ['npm:axios']
// access: ['$@']
// network: disable
// ---
const axios = require('axios');
```

---

## Frontmatter Fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `name` | string | filename stem | Tool name; used for Docker image tag and `cap list` display |
| `description` | string | `""` | Shown by `cap list` |
| `dependencies` | list | `[]` | `pypi:<pkg>` or `npm:<pkg>` |
| `platform` | string | host arch | Docker `--platform`, e.g. `linux/amd64` |
| `access` | list | `[]` | Filesystem globs to mount (see below) |
| `network` | value | `['*']` | Network policy (see below) |

### `access` — Filesystem Access

Globs are matched relative to the **working directory** and copied into `/workspace/` inside the container.

| Pattern | Meaning |
|---------|---------|
| `'data/**'` | All files under `data/`, read-write |
| `'config.json:ro'` | Single file, read-only |
| `'$@'` | Expand CLI path arguments (remapped to `/workspace/<rel>`) |
| `'$@:ro'` | CLI path args, read-only |

After the container exits, modified `:rw` files are written back; `:ro` changes are discarded.

### `network` — Outbound Network Policy

| Value | Effect |
|-------|--------|
| `'*'` (default, or omit) | Unrestricted network access |
| `disable` | `--network none`; no outbound traffic |
| `['host.com', '*.api.com']` | HTTPS-intercepting proxy allowlist; unmatched hosts get HTTP 403 |

Allowlist entries support fnmatch globs (`*.example.com`) and regex (`re:.*\.api\.com`).
When an allowlist is active, a mitmproxy CA is auto-generated at `~/.cap/proxy/` and injected into the container's trust store.

---

## Running a Tool

```bash
# Run a script directly
cap my-tool.cap.py arg1 arg2

# Run by name (looks up ~/.cap/tools/<name>[.cap.py|.cap.js])
cap my-tool arg1 arg2

# Force rebuild of Docker images
cap --build my-tool.cap.py

# List all installed tools
cap list
```

---

## Installing a Tool

Place the file in `~/.cap/tools/` so it's runnable by name:

```bash
# Install
cp my-tool.cap.py ~/.cap/tools/my-tool.cap.py

# Now run anywhere by name
cap my-tool input.pdf
```

`cap list` reads `~/.cap/tools/` and prints `name — description` for every tool.

---

## Step-by-Step: Creating a New Tool

1. **Identify the task** — what should the tool do? What inputs does it need?

2. **Choose the language** — Python (`.cap.py`) for most tasks; JavaScript (`.cap.js`) for Node-heavy work.

3. **Draft the frontmatter**
   - `name:` — short, lowercase, hyphenated
   - `description:` — one sentence, shown in `cap list`
   - `dependencies:` — list `pypi:` or `npm:` packages needed
   - `access:` — use `['$@']` if the tool operates on files passed as arguments; add explicit globs for fixed paths; append `:ro` for read-only
   - `network:` — use `disable` if no outbound calls needed; list specific domains if known; omit or use `'*'` only if truly unrestricted

4. **Write the script body** — standard Python or Node.js. CLI args arrive in `sys.argv` / `process.argv`. Files from `access` globs are at `/workspace/<rel>`.

5. **Test locally**
   ```bash
   cap ./my-tool.cap.py [args]
   ```

6. **Install** (optional)
   ```bash
   cp my-tool.cap.py ~/.cap/tools/
   cap my-tool [args]
   ```

---

## Examples

### Convert a file to Markdown
```python
#!/bin/cap
# ---
# name: markitdown
# description: Convert a file to markdown using Microsoft MarkItDown.
# dependencies: ['pypi:markitdown[pdf,youtube-transcription]']
# platform: linux/amd64
# network: ['*']
# access: ['$@']
# ---
import sys
from markitdown import MarkItDown

if len(sys.argv) < 2:
    print("Usage: markitdown <file>", file=sys.stderr)
    sys.exit(1)

result = MarkItDown().convert(sys.argv[1])
print(result.text_content)
```

### Sandboxed vim (read-write, no network)
```python
#!/bin/cap
# ---
# name: vim
# description: Edit files with vim in a sandboxed container.
# dependencies: []
# network: disable
# access: ['$@:rw']
# ---
import os, sys
args = sys.argv[1:] or ["."]
os.execvp("vim", ["vim"] + args)
```

---

## Key Constraints

- Scripts must be **self-contained** — all imports must come from `dependencies`
- `/workspace/` is the only writable path inside the container (when `access` is set)
- The container is ephemeral; state does not persist between runs unless written back via `:rw` access
- Docker must be running; cap manages image builds and caching automatically
