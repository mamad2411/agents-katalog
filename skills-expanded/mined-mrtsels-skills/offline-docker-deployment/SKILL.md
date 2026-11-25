---
name: offline-docker-deployment
description: "Prepare and deploy Docker applications to air-gapped/offline servers with no network access. Covers image building, export, transfer (USB), and import on target."
category: devops
---

# Offline Docker Deployment

> 本技能为离线部署类技能的伞,已吸收 `air-gap-deployment`(2026-08 合并)。
> 完整原文见 `references/absorbed-*.md`。


Deploy Docker applications to servers with **no network access**. All images must be prepared on a networked machine, exported as tar files, physically transferred (USB), and loaded on the target.

## Workflow (Mac/Linux → USB → Linux server)

```
Dev machine (has Docker + internet)          Target server (no network)
  ┌─────────────────────┐                    ┌──────────────────────┐
  │ bash deploy.sh      │                    │ sudo bash install.sh │
  │   ├─ pull base img  │                    │   ├─ load .tar img  │
  │   ├─ build app img  │   USB drive        │   ├─ docker compose  │
  │   └─ save → .tar    │  ───────►          │   └─ up -d          │
  └─────────────────────┘                    └──────────────────────┘
```

# Workflow (macOS → Windows USB via SCP)

When the USB drive is physically connected to a **Windows machine** that has SSH server running:

```
macOS                          Windows (SSH)                    Target server
  ┌─────────────┐  scp zip     ┌─────────────────┐  USB plug   ┌──────────────┐
  │ bash deploy │───────►     │ PowerShell      │────────►     │ /opt/        │
  │  .sh        │              │ ExtractToDirectory              │ install.sh   │
  └─────────────┘              │ delete old dir                 │              │
                               └─────────────────┘              └──────────────┘
```

Steps:
```bash
# 1. On dev machine: build + export
cd /path/to/project && bash deploy.sh

# 2. Compress with Python (handles Chinese filenames correctly)
#    Use Python's zipfile, NOT the `zip` command — macOS zip encoding
#    breaks Chinese chars on Windows.
python3 -c "
import zipfile, os
exclude = {'.git', 'backend/target', '.config', '.claude', '.hermes', 'logs', 'references'}
with zipfile.ZipFile('/tmp/project.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk('.'):
        rel = os.path.relpath(root, '.')
        if any(rel == d or rel.startswith(d+'/') for d in exclude): continue
        for f in files:
            zf.write(os.path.join(root, f), 'project/' + os.path.relpath(os.path.join(root, f), '.'))
"

# ⚠️ CRITICAL — docker/images/*.tar MUST be included.
#    These are the offline deployment images (mysql, backend, frontend, etc.).
#    Without them, install.sh cannot start services on the air-gapped server.
#    Excluding them will make the deployment non-functional.

# 3. SCP zip directly to Windows (SMB mount is unreliable — disconnects)
scp /tmp/project.zip user@windows-ip:F:/

# 4. SSH to Windows, delete old dir, unzip
ssh user@windows-ip 'powershell -Command "
  Add-Type -AssemblyName System.IO.Compression.FileSystem;
  if (Test-Path F:\\\project) { Remove-Item F:\\\project -Recurse -Force };
  [System.IO.Compression.ZipFile]::ExtractToDirectory(\"F:\\\project.zip\", \"F:\\\");
"'

# 5. Plug USB into target server, run install
cp -r /media/USB/project /opt/project
cd /opt/project && sudo bash install.sh
```

## Windows dev machine alternative

If the dev machine itself runs Windows, use `deploy-win.ps1` (PowerShell equivalent of `deploy.sh`):

```powershell
# Terminal (PowerShell):
.\deploy-win.ps1

# Then zip the project directory and copy to USB directly:
# Copy-Item C:\project F:\enterprise -Recurse
```

## Step 1 — Prepare images (on networked dev machine)

### Mac/Linux (bash)

```bash
mkdir -p docker/images
docker pull mysql:8.0
docker pull eclipse-temurin:17-jre
docker pull nginx:alpine
docker-compose -f docker/docker-compose.yml build
docker save mysql:8.0              -o docker/images/mysql-8.0.tar
docker save eclipse-temurin:17-jre -o docker/images/eclipse-temurin-17-jre.tar
docker save nginx:alpine           -o docker/images/nginx-alpine.tar
docker save myapp-backend:latest   -o docker/images/enterprise-backend.tar
docker save myapp-frontend:latest  -o docker/images/enterprise-frontend.tar
```

### Windows (PowerShell)

Use `deploy-win.ps1` if available, or:

```powershell
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path "docker\images"
foreach ($img in @("mysql:8.0","eclipse-temurin:17-jre","nginx:alpine")) { docker pull $img }
docker compose -f docker\docker-compose.yml build
docker save mysql:8.0              -o docker\images\mysql-8.0.tar
docker save eclipse-temurin:17-jre -o docker\images\eclipse-temurin-17-jre.tar
docker save nginx:alpine           -o docker\images\nginx-alpine.tar
docker save enterprise-backend:latest  -o docker\images\enterprise-backend.tar
docker save enterprise-frontend:latest -o docker\images\enterprise-frontend.tar
```

## Step 2 — Import and start (on target)

```bash
# install.sh typically does:
for img in docker/images/*.tar; do
  docker load -i "$img"
done
docker compose -f docker/docker-compose.yml up -d

# Post-start: verify seed data
# If database volume is stale (old schema, no seed data), auto-reimport:
docker exec <db-container> mysql -u <user> -p<pass> <db> \
  -e "SELECT 1 FROM sys_user LIMIT 1" 2>/dev/null | grep -q 1 || \
  docker exec -i <db-container> mysql -u <user> -p<pass> <db> < init.sql
```

## Uninstall (full cleanup)

```bash
# 1. Stop containers + delete volumes (including database data)
docker compose -f docker/docker-compose.yml down -v

# 2. Remove Docker images
for img in enterprise-backend:latest enterprise-frontend:latest mysql:8.0; do
  docker rmi -f "$img" 2>/dev/null || true
done

# 3. Remove offline tar files
rm -f docker/images/*.tar

# 4. Clean logs, configs, uploads
rm -rf logs/ uploads/ docker/.env

# 5. If systemd service exists:
systemctl stop enterprise-backend 2>/dev/null || true
systemctl disable enterprise-backend 2>/dev/null || true
rm -f /etc/systemd/system/enterprise-backend.service
systemctl daemon-reload
```

## Interactive AI/API key configuration

When deployment requires runtime configuration (API keys, model selection), provide an interactive setup command:

```bash
cmd_setup() {
  # 1. Prompt for URL with default
  read -p "API URL [default]: " INPUT_URL || true
  URL="${INPUT_URL:-$DEFAULT_URL}"

  # 2. Prompt for API key
  read -p "API Key: " INPUT_KEY || true
  KEY="${INPUT_KEY:-$CURRENT_KEY}"

  # 3. Prompt for model with default
  read -p "Model [default]: " INPUT_MODEL || true
  MODEL="${INPUT_MODEL:-$DEFAULT_MODEL}"

  # 4. Write to .env file
  echo "AI_URL=$URL" >> docker/.env
  echo "AI_KEY=$KEY" >> docker/.env
  echo "AI_MODEL=$MODEL" >> docker/.env

  # 5. Also write to runtime config file for immediate effect
  mkdir -p uploads
  python3 -c "import json; json.dump({'url':'$URL','key':'$KEY','model':'$MODEL'}, open('uploads/config.json','w'))"
}
```

## `read` command safety under `set -euo pipefail`

When adding `read -p` prompts to CLI scripts that run under `set -euo pipefail`, always add `|| true` to every `read` command:

```bash
# WRONG — exits on EOF (piped input, no TTY):
read -p "Enter value: " VAR

# CORRECT — tolerates EOF silently:
read -p "Enter value: " VAR || true
```

Also pre-initialize the variable to prevent `set -u` failures on empty read:

```bash
VAR=""; read -p "Enter value: " VAR || true
```

## Docker extra_hosts and DNS failover

When the target has no DNS, add `extra_hosts` in docker-compose.yml. Multiple IPs for the same hostname are **appended** to `/etc/hosts`, not overwritten:

```yaml
extra_hosts:
  - "api.example.com:1.2.3.4"
  - "api.example.com:5.6.7.8"   # ← both lines appear in /etc/hosts
```

The OS resolver returns IPs in file order. Java's `InetAddress.getAllByName()` returns all addresses, and HTTP clients (RestClient, HttpURLConnection) try each in sequence on connection failure.

**Caveat:** If the first IP accepts the TCP connection but returns wrong data (not a timeout), the client won't retry with the next IP. This is a TCP-level failover, not an application-level one.

## Pitfalls

### docker/images/*.tar is DEPLOYMENT-CRITICAL — never exclude
When creating the deployment zip, `docker/images/*.tar` files are the pre-built Docker images that `install.sh` imports. **If you exclude them, the server will have no images to run and deployment will fail.** The user will not be able to start any service.

Always include `docker/images/` in the zip. Acceptable excludes: `.git`, `backend/target/`, `references/`, `.config/`, `.claude/`, `.hermes/`, `logs/`.

### Chinese filename encoding in zip
When the project contains Chinese-named files (e.g. `references/04-政策研究/`), Windows `Expand-Archive` cmdlet and Windows `tar` may fail with "invalid path characters".

**Use .NET API directly via PowerShell:**
```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory('F:\project.zip', 'F:\')
```

Python's `zipfile` with `ZIP_DEFLATED` on macOS produces UTF-8 entries that work with this .NET method.

### CRLF line endings on Linux target

When `.sh` scripts are transferred via USB from **Windows**, the line endings are often converted to CRLF (`\r\n`). The Linux kernel tolerates `\r` in the shebang line, but **bash** treats `\r` as part of token names — so `set -euo pipefail\r` fails because `pipefail\r` is not a recognized option.

**Fix 1 — Self-healing guard** (recommended for install.sh / CLI scripts):

Insert BEFORE `set -euo pipefail`:
```bash
# CRLF self-heal: Windows USB transfer leaves \r\n line endings
if grep -q $'\r$' "$0"; then
  sed -i 's/\r$//' "$0"
  exec bash "$0" "$@"
fi
```

The guard detects `\r` at end-of-line, strips it with `sed`, then re-executes the clean script via `exec`. Must be placed before any `set -e` or `set -euo pipefail` that would fail on the `\r` suffix.

**Fix 2 — Ad-hoc repair** (for any other .sh files that lack the guard):
```bash
sed -i 's/\r$//' /opt/enterprise/*.sh
```

### Build context path
When `docker-compose.yml` is in a subdirectory (e.g. `docker/`), the build context path must point to the project root (`..`), not the compose file's directory (`.`).

**Wrong** (compose in docker/ subdir):
```yaml
build:
  context: .        # resolves to docker/ — WRONG
```

**Correct:**
```yaml
build:
  context: ..       # resolves to project root — CORRECT
  dockerfile: docker/Dockerfile.backend
```

### Frontend healthcheck in nginx:alpine
The `nginx:alpine` image contains `wget` but it may fail with "Connection refused" when running a healthcheck against `http://localhost/` — even though nginx is running and serving requests correctly. **Use `curl -sf` instead** in HEALTHCHECK:

```dockerfile
# May report unhealthy despite serving correctly:
HEALTHCHECK CMD wget -qO- http://localhost/ || exit 1

# Reliable:
HEALTHCHECK CMD curl -sf http://localhost/ || exit 1
```

`curl` is included in `nginx:alpine` and works reliably for local health checks.

### macOS + colima: DOCKER_HOST not set

On macOS, Docker often runs via colima (socket at `~/.colima/default/docker.sock`), not the default `/var/run/docker.sock`. Running `deploy.sh` or any `docker`/`docker-compose` command without `DOCKER_HOST` set will fail with `failed to connect to the docker API`:

```bash
# Set before running deploy.sh:
export DOCKER_HOST=unix:///Users/me/.colima/default/docker.sock
bash deploy.sh

# Or in a CLI script, auto-detect at startup:
detect_docker_host() {
  if [ -z "${DOCKER_HOST:-}" ]; then
    local colima_sock="$HOME/.colima/default/docker.sock"
    if [ -S "$colima_sock" ]; then
      export DOCKER_HOST="unix://$colima_sock"
    fi
  fi
}
detect_docker_host
```

The `enterprise` CLI template should include this detection at the top, before any docker command.

### PowerShell via SSH: single-line quoting only

When running PowerShell commands through SSH from bash, **multi-line quoted strings silently produce no output**. The backslash-newline continuation inside double-quoted SSH strings does NOT work as expected:

```bash
# BROKEN — produces empty output, command silently fails:
ssh user@host "powershell -Command \"
Add-Type ...;
if (...) { Remove-Item ... };
[ZipFile]::ExtractToDirectory(...);
Write-Host 'done'
\""

# WORKS — single-line, semicolons separate statements:
ssh user@host 'powershell -Command "Add-Type -AssemblyName System.IO.Compression.FileSystem; if (Test-Path F:\\project) { Remove-Item F:\\project -Recurse -Force }; [System.IO.Compression.ZipFile]::ExtractToDirectory(\"F:\\project.zip\", \"F:\\\"); Write-Host DONE"'
```

The single-line format with single-quote bash wrapper (`'...'`) and escaped internal double quotes (`\"`) is the reliable pattern.

### Relative volume paths
Docker image tars are too large for git. Add to `.gitignore`:
```
docker/images/*.tar
```

### Don't assume network or SSH on target
The server may have no network, no DNS, no SSH access. Deployment happens via physical media (USB drive). Never document `scp`, `ssh`, or `curl` commands in deployment instructions without confirming the target's connectivity.

### Verify credentials from source
When documenting passwords, ports, or connection strings in deployment docs, always read the **actual source file** (init.sql, migration files, config files) to verify. Do not copy from memory or other docs that may themselves be wrong.

### Git push through GFW
Pushing to GitHub from China may fail with `SSL_read: sslv3 alert bad record mac`. Workarounds (try in order):
1. Retry with `git -c http.version=HTTP/1.1 push`
2. Use SOCKS5 proxy: `git -c http.proxy=socks5://127.0.0.1:1082 push`
3. Configure persistent proxy: `git config --global http.proxy socks5://127.0.0.1:1082`
