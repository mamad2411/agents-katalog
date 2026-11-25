---
name: antigravity-coding-agent
description: Delegate complex coding or full-stack application builds to Antigravity CLI (agy) as an autonomous headless worker.
---

# Antigravity Coding Agent

Use when asked to build a full-stack web application, complex microservice, or multi-file programming project on the homelab, delegating the implementation to Antigravity CLI (`agy`) instead of generating the entire codebase inline in chat.

## Procedure

### 1. Isolate Project Directory and Assets
Create a dedicated project directory to keep dependencies and builds fully self-contained, initialize Git, and trust the directory in `~/.gemini/trustedFolders.json`:
```bash
mkdir -p /home/user/<project_name>/data
cd /home/user/<project_name> && git init
python3 -c "
import json, os
p = os.path.expanduser('~/.gemini/trustedFolders.json')
d = json.load(open(p)) if os.path.exists(p) else {}
d['/home/user/<project_name>'] = 'TRUST_FOLDER'
with open(p, 'w') as f:
    json.dump(d, f, indent=2)
"
```
Trusting the path prevents headless CLI runs from stalling on interactive workspace confirmation.
Copy or link any required databases, dumps, schemas, or raw datasets into `/home/user/<project_name>/data/` so the worker has direct local access without reaching into external session workspaces.

### 2. Audit Homelab Environment and Ports
Check active network ports and PM2 services before writing specifications to prevent runtime port collisions:
```bash
ss -tuln | grep -E ':(3000|3001|3010|3200|3306|3400|3600|5001|5678|8081|8082|8085|8888)\b'
pm2 status
```
Assign a verified free port (e.g., 3600) and a distinct PM2 process name (e.g., `<project_name>`).

### 3. Write Specification Prompt
Save the complete requirements into `/home/user/<project_name>/PROMPT.md` to prevent shell quoting truncation and argument splitting:
Include:
- Target architecture: distinguish web services from native desktop applications. For local workstation tools or apps requested "like VirtualBox", mandate a native GUI (PyQt6/PySide6) with a `.desktop` launcher and local filesystem pickers (`QFileDialog`), not a web service, browser interface, or network upload flow.
- Local paths to all datasets and SQLite/MySQL database files.
- For web services: exact port assignment, host binding (`0.0.0.0:<port>`), and PM2 process management requirements (`pm2 start ... --name <project_name>`).
- Explicit visual theme (light vs dark mode) based on the user's preference rather than assuming a default palette.
- Style constraints (e.g., strict prohibition of emojis across code, UI, and logs).
- Relational grouping integrity: mandate grouping records strictly by foreign keys or entity IDs (such as household UUIDs), never by surname string matching, because common surnames conflate unrelated individuals.
- Map tiles and geospatial services: avoid third-party tile layers that require API keys or inject watermark errors (e.g. CartoDB, Mapbox); use OpenStreetMap or host local pre-downloaded tiles under `public/tiles/{z}/{x}/{y}.png` with OSM fallback.
- Mobile-first UI specifications: when building frontends, mandate a fixed bottom navigation bar for mobile (`<= 768px`), bottom sheets for slide-out drawers, card views instead of horizontal table scrolling, and touch-scrolling filter chips.
- Interactive state & filter contracts: require filter reset buttons to explicitly trigger re-renders without early return guards, and test compound role or relationship filters against raw datasets.
- Required modules, views, API routes, and dataset contracts.
- Self-verification steps (e.g., `curl -I http://127.0.0.1:<port>/api/health`).

### 4. Execute Antigravity CLI

#### Option A: Homelab Local Execution (Server)
Run `agy` inside the local project directory using auto-approved permissions mode:
```bash
cd /home/user/<project_name> && /home/user/.local/bin/agy --dangerously-skip-permissions --print "$(cat PROMPT.md)"
```
Use `exec` with `yieldMs` to allow the compilation to proceed in the background without blocking the turn. Scope prompts per component or file rather than passing monolithic multi-file specifications at once, because large generations risk exceeding execution timeouts. Always prefer `--model gemini-3.8-flash-low` for non-interactive `--print` task runs; higher-effort or thinking models buffer without streaming and easily hit subshell execution timeouts.

#### Option B: Workstation Queue Delegation (PC / Notebook)
When instructed to develop or offload builds to the user's PC (`workstation-host`), enqueue the task to the workstation queue API (`workstation-queue` on port 5070):
```bash
pc-task agy "<Task Title>" "$(cat PROMPT.md)" --project "<project_name>" --workdir "/home/user/<project_name>"
```
The workstation runner (`workstation-runner.service`) automatically takes the task via Tailscale, displays native desktop notifications ("Félix está trabajando en tu PC"), activates the tray icon (`AyatanaAppIndicator3`), runs `agy --dangerously-skip-permissions --print` locally on the workstation, and reports results upon completion.

### 5. Monitor Headless Execution
For local execution, track ongoing activity by checking process state, modified files, and CLI execution logs:
```bash
ps aux | grep agy
ls -lt /home/user/<project_name>/ /home/user/<project_name>/public/
tail -n 25 $(ls -t /home/user/.gemini/antigravity-cli/log/cli-*.log | head -n 1)
```

For workstation queue execution, monitor status and fetch logs via CLI:
```bash
pc-task show <task_id>
```
Inspect `Status` (`pending`, `running`, `completed`, `failed`), `Exit Code`, and `Output`. If the task fails with `Authentication required. Please visit the URL to log in` followed by `authentication timed out`, the workstation OAuth token in `~/.gemini/oauth_creds.json` has expired and headless non-interactive mode cannot complete browser callbacks; instruct the user to run `agy` interactively in a terminal on the workstation once to refresh the Google session before re-enqueuing.

### 6. Resume or Extend Existing Projects
When instructed to add features, apply fixes, or adjust authentication/configuration on an existing project, do not restart from scratch. Continue the prior conversation session:

For local homelab execution:
```bash
cd /home/user/<project_name> && /home/user/.local/bin/agy --dangerously-skip-permissions --continue --print "$(cat PROMPT_UPDATE.md)"
```
To quickly resolve the last conversation ID for a workspace without database queries, inspect the active conversation cache:
```bash
python3 -c "import json; print(json.load(open('/home/user/.gemini/antigravity-cli/cache/last_conversations.json')).get('/home/user/<project_name>'))"
```
Or query `conversation_summaries.db` by title, preview, or workspace:
```bash
python3 -c "
import sqlite3
con = sqlite3.connect('/home/user/.gemini/antigravity-cli/conversation_summaries.db')
for r in con.execute('''
    SELECT conversation_id, title, preview, step_count, last_modified_time 
    FROM conversation_summaries 
    WHERE workspace_uris LIKE '%<project_name>%' OR preview LIKE '%<keyword>%' OR title LIKE '%<keyword>%'
    ORDER BY last_modified_time DESC LIMIT 5
''').fetchall():
    print(r)
"
```
Resume the exact conversation using its `<conversation_id>`:
```bash
cd /home/user/<project_name> && /home/user/.local/bin/agy --dangerously-skip-permissions --conversation <conversation_id> --print "$(cat PROMPT_UPDATE.md)"
```

For workstation queue execution, pass the same `--project` and `--workdir`:
```bash
pc-task agy "<Task Title>" "$(cat PROMPT_UPDATE.md)" --project "<project_name>" --workdir "/home/user/<project_name>"
```
The workstation runner automatically resolves and reuses the previous conversation ID from `~/.gemini/antigravity-cli/cache/last_conversations.json` on the PC. To target a specific conversation explicitly, pass `--conversation <conversation_id>`.

### 7. Consolidate and Clean Sessions
Never attempt to merge multiple `.db` conversation files directly; trajectory step indices and token caches will desynchronize and corrupt the session. To consolidate fragmented sessions:
1. Document architecture and design decisions in the project repository's `AGENTS.md` or handoff Markdown file.
2. Archive old `.db` files into a `.tar.gz` backup and remove them from `/home/user/.gemini/antigravity-cli/conversations/`.
3. Delete their entries from `conversation_summaries.db` (`DELETE FROM conversation_summaries WHERE conversation_id IN (...)`).
4. Run a single synchronization prompt with `--conversation <canonical_id>` passing the updated context to anchor the canonical session.

### 8. Verify Deployment and Register Monitoring
For web services and daemons, confirm the application status in PM2 and verify HTTP response:
```bash
pm2 status <project_name>
curl -I http://127.0.0.1:<port>/
curl http://127.0.0.1:<port>/api/health
```
Immediately register the new service in Homelab Monitor using the local CLI to activate automated health checks and WhatsApp incident notifications:
```bash
homelab-monitor add "<Project Name>" "http://127.0.0.1:<port>/health"
```
For external subdomains, pass the full public URL (`https://...`). For raw TCP ports, pass `--type tcp`. Verify registration with `homelab-monitor list`.

For native desktop applications, verify executable PATH presence and desktop launcher registration:
```bash
which <app_name>
desktop-file-validate ~/.local/share/applications/<app_name>.desktop
```
