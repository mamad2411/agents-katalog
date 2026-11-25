---
name: service-deployment-and-monitoring
description: Service deployment, auto-healing monitoring, and port management for Charles's Hostinger server. Covers Traefik Docker routing, systemd port reservation, Docker-in-Docker patterns, health checks, and alerting.
category: devops
---

# Service Deployment and Monitoring

**Deploy, monitor, and maintain services on Charles's Hostinger server.**

## What This Skill Does

This skill Service deployment, auto-healing monitoring, and port management for Charles's Hostinger server. Covers Traefik Docker routing, systemd port reservation, Docker-in-Docker patterns, health checks, and alerting.

## Server Environment

- **Server IP:** set `CHARLES_HOST_IP` in the environment before using IP-based commands.
- **Firewall:** UFW active — ports 22, 80, 443, 3000, 7000 already open
- **Traefik:** `/docker/traefik/docker-compose.yml` + `/docker/traefik/traefik.yml`, runs in host network mode
- **Traefik network:** `traefik-net` (bridge)
- **Let's Encrypt email:** realdealmeetup@gmail.com

## Umbrella Sections

- **[§1 Traefik Docker Deploy](#section-1-traefik-docker-deploy)** — Deploy Docker apps behind Traefik with SSL, DNS, and firewall
- **[§2 systemd Port Reservation](#section-2-systemd-port-reservation)** — Lock a port to a Node/Vite service with systemd auto-restart
- **[§3 Service Health Monitoring](#section-3-service-health-monitoring)** — Auto-healing cron jobs with Telegram alerts
- **[§4 Docker-in-Docker Patterns](#section-4-docker-in-docker-patterns)** — Running Docker inside containers, container-down detection, port checks
- **[§5 filebrowser Deploy](#section-5-filebrowser-deploy)** — Deploy filebrowser with Cloudflare tunnel HTTPS

---

## §1 Traefik Docker Deploy

**Deploy Docker apps behind Traefik reverse proxy with automatic SSL certificates.**

### Deployment Steps

1. **Check Docker is available:**
   `docker --version`

2. **Stop/remove any previous version of the container:**
   `docker rm -f <container_name> 2>/dev/null || true`

3. **Verify the domain has DNS:**
   `dig +short <domain>` or `host <domain> 8.8.8.8`
   If no DNS record exists, use sslip.io as fallback:
   - Format: `http://IP-WITH-DASHES.sslip.io` (derive it from `$CHARLES_HOST_IP`)

4. **Create data directory with correct permissions:**
   `mkdir -p /root/<app_name>/data`
   `chown -R 1000:1000 /root/<app_name>`  (common for apps that run as non-root)

5. **Launch behind Traefik:**
   ```bash
   docker run -d \
     --name <container_name> \
     --restart unless-stopped \
     --network traefik-net \
     -e APPLICATION_URL=https://<domain> \
     --label "traefik.enable=true" \
     --label "traefik.http.routers.<name>.rule=Host(\`<domain>\`)" \
     --label "traefik.http.routers.<name>.entrypoints=websecure" \
     --label "traefik.http.routers.<name>.tls.certresolver=letsencrypt" \
     --label "traefik.http.services.<name>.loadbalancer.server.port=<internal_port>" \
     -v /root/<app_name>/data:/app/data \
     <image_name>
   ```

   For HTTP-only (no TLS), also add:
   ```
   --label "traefik.http.routers.<name>-insecure.rule=Host(\`<domain>\`)" \
   --label "traefik.http.routers.<name>-insecure.entrypoints=web" \
   ```

6. **Verify the container is healthy:**
   `docker ps --filter name=<container_name> --format '{{.Status}}'`
   Should show "Up X seconds" (not "Restarting")

7. **Check Traefik logs for SSL certificate issuance:**
   `docker logs traefik 2>&1 | grep -i <domain> | tail -5`
   Wait up to 60 seconds for the certificate to be obtained.

8. **Test from the server:**
   `curl -sk https://<domain> | head -5`
   `curl -sL http://<domain> | head -5`

### Troubleshooting

**Container is restart-looping:**
- **Wrong UID:** Many apps run as non-root (UID 1000). Check: `docker run --rm <image> id`. Fix perms: `chown -R 1000:1000 /root/<app>`.
- **Missing dirs/files:** Some apps need specific subdirectories pre-created. Check `docker logs <container>`.
- **Stale config files:** Remove old config files from previous attempts.

**SSL certificate fails (400 DNS error):**
- Domain has no DNS A record pointing to `$CHARLES_HOST_IP`.
- Fix: add DNS record at registrar, or use sslip.io.
- Note: Let's Encrypt may rate-limit retries. HTTP fallback works immediately.
- **here.now is NOT an option for HTTPS** — it only hosts static files.

**Port not accessible from outside:**
- Traefik handles all external traffic via ports 80/443 — apps behind Traefik do NOT need host port mapping (`-p`).
- **SIMPLEST APPROACH when Traefik/DNS is problematic:** Use an already-open port (7000) with direct IP access, e.g. `http://$CHARLES_HOST_IP:7000`.
- **HTTPS tunnel fallback:** Use localtunnel:
  `lt --port <app_port> --local-host localhost --subdomain <unique-name>`

**Verify Traefik is routing correctly:**
- `docker network inspect traefik-net --format '{{range .Containers}}{{.Name}} {{end}}'`
- Test from Inside Traefik: `docker exec traefik wget -qO- http://<container_name>:<port> | head -5`
  Note: hostname-based DNS won't work from Traefik container. Use container name or `curl -H "Host: <domain>" http://<container_ip>:<port>`.

---

## §2 systemd Port Reservation

**Lock a port permanently to a Node/Vite service using systemd — prevents any other process from stealing it, auto-restarts on crash, survives reboots.**

### Key Lessons

### DO NOT use systemd socket activation (.socket unit)
The instinct to use a `.socket` unit to "pre-bind" the port sounds right but FAILS with Vite/Node.
Reason: systemd holds the socket fd and passes it via fd inheritance — but Vite does its own `listen()` call and sees the port as already in use, then tries to fall back to another port.
Result: Vite logs "Port 3001 is in use, trying another one..." and binds to a random port instead.

### Correct approach: service-only with --strictPort + ExecStartPre guard
- Use a plain `.service` unit (no `.socket` unit)
- Pass `--strictPort` to Vite so it errors out instead of silently switching ports
- Add `ExecStartPre` to fail fast if something else somehow grabs the port before startup
- Set `Restart=always` + `StartLimitIntervalSec=0` for infinite auto-restart

### Step-by-Step

1. **Kill any existing background process on the port:**
```bash
pkill -f "vite.*PORT" 2>/dev/null
pkill -f "pnpm.*dev" 2>/dev/null
sleep 2
ss -tlnp | grep PORT && echo "still running" || echo "port free"
```

2. **Write the service file:**
```bash
cat > /etc/systemd/system/MY-SERVICE.service << 'EOF'
[Unit]
Description=My Service UI (port PORT)
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/app
Environment=PORT=PORT
Environment=NODE_OPTIONS=--max-old-space-size=2048

# Fail fast if anything else is on PORT before we start
ExecStartPre=/bin/bash -c '! ss -tlnp | grep -q ":PORT " || (echo "PORT already in use" >&2; exit 1)'

# --strictPort: Vite errors out instead of silently falling back
ExecStart=/usr/bin/pnpm dev --port PORT --strictPort

Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=MY-SERVICE

[Install]
WantedBy=multi-user.target
EOF
```

Replace `MY-SERVICE`, `PORT`, and `/path/to/app` with real values.

3. **Enable and start:**
```bash
systemctl daemon-reload
systemctl enable MY-SERVICE.service
systemctl start MY-SERVICE.service
```

4. **Verify:**
```bash
# Service status
systemctl status MY-SERVICE.service --no-pager

# Port actually bound
ss -tlnp | grep PORT

# Prove no other process can bind it
python3 -c "
import socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.bind(('0.0.0.0', PORT))
    print('WARNING: port was bindable!')
except OSError as e:
    print(f'Port protected: {e}')
finally:
    s.close()
"
```
Expected: `Port protected: [Errno 98] Address already in use`

### Hermes Workspace Specific Values
- Service name: `hermes-workspace`
- Port: `3001`
- WorkingDirectory: `/root/.openclaw/workspace/hermes-workspace`
- ExecStart: `/usr/bin/pnpm dev --port 3001 --strictPort`
- Service file: `/etc/systemd/system/hermes-workspace.service`

### Pitfalls
- **Don't create a .socket unit alongside the .service** — it will pre-bind the port and break Vite
- **pnpm's dev script may hardcode --port 3000** — passing `--port 3001` on CLI overrides it
- **StartLimitIntervalSec=0** is required for truly infinite restarts
- **ExecStartPre grep pattern** — use `:PORT ` (with trailing space) to avoid matching port 30010, 30011, etc.

### Useful Commands
```bash
# View live logs
journalctl -u hermes-workspace.service -f

# Restart manually
systemctl restart hermes-workspace.service

# Check port ownership
ss -tlnp | grep 3001
```

---

## §3 Service Health Monitoring

**Auto-healing cron jobs with Telegram alerts — detects zombie processes, connection losses, memory leaks, auto-restarts failed services.**

### Use When
- You need to monitor critical processes/services and auto-restart them if they fail
- You want automatic recovery without manual intervention
- You need periodic health checks with alerting on failures

### Setup

#### 1. Create the health check script
Template: `~/.hermes/bin/service-health-check.sh`
Key checks:
- Process running check: `pgrep -f "service_name" | head -1`
- Zombie detection: `kill -0 $PID 2>/dev/null`
- Recent activity: `stat -c %Y logfile` vs `date +%s`
- Connection status: `grep "Connected\|Disconnected" logfile`
- Memory usage: `ps -p $PID -o %mem=`

#### 2. Create the alert script (optional)
Template: `~/.hermes/bin/service-restart-alert.sh`
- Sends Telegram message on restart
- Requires `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` env vars

#### 3. Set up cron job
```
cronjob action=create name="service-health-check" schedule="*/5 * * * *" prompt="..."
```
Runs every 5 minutes automatically.

### Key Commands

**Check if service is running:**
```bash
pgrep -f "service_name"
```

**Restart service:**
```bash
pkill -f "old_process"
sleep 2
nohup /path/to/service &
```

**View health logs:**
```bash
tail -f ~/.hermes/logs/health-check.log
```

**Test health check manually:**
```bash
bash ~/.hermes/bin/gateway-health-check.sh
echo $?  # 0 = healthy, 1 = restarted/failed
```

### Pitfalls
- **False positives on idle services:** Don't restart just because there's no activity. Check actual connection status or process state.
- **Cascading restarts:** If restart fails repeatedly, add a cooldown timer or max restart count.
- **Missing credentials:** Telegram alerts require `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
- **Duplicate poller trap (CRITICAL):** If your gateway script spawns a new Telegram poller every time it sees a stale log → 409 conflict loop. Always check if the primary daemon is already running before spawning a new one.

---

## §4 Docker-in-Docker Patterns

**Running Docker commands inside containers, container-down detection, port checks via /proc/net/tcp.**

### Key Constraint
NO host-level `pkill`, `pgrep`, or process management allowed. All checks and restarts go through `docker exec`.

### Port check inside container
```bash
# /proc/net/tcp uses little-endian hex for ports
# e.g. port 18789 = 0x4965
docker exec "$CONTAINER" grep -qi "4965" /proc/net/tcp /proc/net/tcp6 2>/dev/null
```

### Restart inside container
```bash
docker exec -d "$CONTAINER" sh -c "myservice run --port 18789 >> /tmp/service.log 2>&1"
```

### Container-down detection (escalate immediately, don't retry)
```bash
RUNNING=$(docker inspect --format '{{.State.Running}}' "$CONTAINER" 2>/dev/null)
if [ "$RUNNING" != "true" ]; then
    send_telegram "Container is DOWN. Run: docker start $CONTAINER"
    exit 1
fi
```

### Retry loop pattern (3 attempts, verify after each)
```bash
attempt=1
while [ $attempt -le 3 ]; do
    docker exec -d "$CONTAINER" sh -c "service run >> /tmp/service.log 2>&1"
    sleep 8  # wait for startup
    if port_is_up; then
        send_telegram "Service recovered on attempt $attempt"
        exit 0
    fi
    attempt=$((attempt + 1))
    [ $attempt -le 3 ] && sleep 10
done
send_telegram "All 3 restart attempts failed -- manual intervention required"
exit 1
```

### Telegram alerts — reuse Hermes credentials
```bash
token=$(grep '^TELEGRAM_BOT_TOKEN=.*' "$HOME/.hermes/.env" | cut -d= -f2-)
chat_id=$(grep '^TELEGRAM_CHAT_ID=.*' "$HOME/.hermes/.env" | cut -d= -f2-)
curl -s -X POST "https://api.telegram.org/bot${token}/sendMessage" \
    -d "chat_id=${chat_id}" -d "text=${msg}" -d "parse_mode=Markdown" > /dev/null 2>&1
```

### Real-world example
`/root/openclawcharles/ops/openclaw-gateway-watchdog.sh`
Monitors OpenClaw gateway (port 18789) inside container `openclaw-mm3f-openclaw-1`.
Runs every 2 minutes via root crontab.

### Pitfalls
- **Silent failure trap:** `docker exec -d` fires and forgets. Always re-check the port after sleeping.
- **Container vs process:** Two separate failure modes. If the container is down, `docker exec` will fail — detect this first.
- **Port hex conversion:** `/proc/net/tcp` stores port in little-endian hex. `printf '%04X\n' 18789` gives `4965`.
- **POST_RESTART_WAIT:** Give the process 8-10 seconds to bind the port before checking.

---

## §5 Filebrowser Deploy

**Deploy filebrowser (web-based file manager) with HTTPS via Cloudflare tunnel.**

### Steps

1. **Pull the image:**
```bash
docker pull filebrowser/filebrowser:latest
```

2. **Create config with low password requirements:**
```bash
mkdir -p /root/filebrowser
cat > /root/filebrowser/settings.json << 'EOF'
{
  "port": 80,
  "baseURL": "",
  "address": "0.0.0.0",
  "log": "stdout",
  "database": "/database/filebrowser.db",
  "root": "/srv"
}
EOF
```

3. **Initialize database and create admin user (3-step process):**
```bash
docker volume create fb-data

# Init the database
docker run --rm -v fb-data:/database -v /root/filebrowser/settings.json:/config/settings.json \
  filebrowser/filebrowser:latest config init --config /config/settings.json --database /database/filebrowser.db

# Lower minimum password length to 4
docker run --rm -v fb-data:/database -v /root/filebrowser/settings.json:/config/settings.json \
  filebrowser/filebrowser:latest config set --config /config/settings.json --database /database/filebrowser.db --minimumPasswordLength 4

# Create admin user (password must NOT be a dictionary word — "admin" is banned)
docker run --rm -v fb-data:/database -v /root/filebrowser/settings.json:/config/settings.json \
  filebrowser/filebrowser:latest users add admin Admin123456 --config /config/settings.json --database /database/filebrowser.db --perm.admin
```

4. **Launch container:**
```bash
docker rm -f filebrowser 2>/dev/null || true
docker run -d \
  --name filebrowser \
  --restart unless-stopped \
  -p 7000:80 \
  -v fb-data:/database \
  -v /:/srv \
  filebrowser/filebrowser:latest
```

5. **Verify login:**
```bash
curl -s -X POST http://localhost:7000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin123456"}'
# Should return a JWT token on success
```

6. **Set up HTTPS via Cloudflare quick tunnel:**
```bash
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared
nohup cloudflared tunnel --url http://localhost:7000 > /tmp/cloudflared.log 2>&1 &
sleep 6
grep "https://" /tmp/cloudflared.log | head -1
```

### Password Reset / User Management
If you need to change a user's password after the container is already running:

```bash
docker stop filebrowser
docker run --rm -v fb-data:/database -v /root/filebrowser/settings.json:/config/settings.json \
  filebrowser/filebrowser:latest users update admin \
  --config /config/settings.json --database /database/filebrowser.db --password "NewPass123!"
docker start filebrowser
```

### Pitfalls
- `minimumPasswordLength` is 12 by default in the container's `/config/settings.json` — you must mount your own config
- The quick setup flags (`--username admin --password admin`) create wrong password hashes — use the 3-step init flow
- "admin" as a password fails the **dictionary check** — use `Admin123456` or similar
- The `gtsteffaniak/filebrowser` Docker image does NOT exist — use `filebrowser/filebrowser`
- Named volumes (`fb-data`) avoid bind-mount permission issues that corrupt the SQLite database
- Localtunnel (`lt`) is unreliable on this server — use `cloudflared` instead


---

## §6 Webhook Subscriptions

**Event-driven agent runs via webhooks — GitHub, GitLab, Stripe, CI/CD, monitoring tools all trigger Hermes agent runs by POSTing to a URL.**

### Setup (Required First)

Check if webhook platform is enabled:
```bash
hermes webhook list
```

If not enabled:
```bash
hermes gateway setup
```
Follow the prompts to enable webhooks, set the port, and set a global HMAC secret.

### Create a subscription
```bash
hermes webhook subscribe <name>   --prompt "Prompt template with {payload.fields}"   --events "event1,event2"   --description "What this does"   --skills "skill1,skill2"   --deliver telegram   --deliver-chat-id "12345"
```

### Common Patterns

**GitHub new issues:**
```bash
hermes webhook subscribe github-issues   --events "issues"   --prompt "New GitHub issue #{issue.number}: {issue.title}"   --deliver telegram --deliver-chat-id "-100123456789"
```

**Stripe payment events:**
```bash
hermes webhook subscribe stripe-payments   --events "payment_intent.succeeded,payment_intent.payment_failed"   --prompt "Payment {data.object.status}: {data.object.amount} cents"   --deliver telegram --deliver-chat-id "-100123456789"
```

**Direct delivery (no LLM, zero cost):**
Use `--deliver-only` for notifications that should forward verbatim:
```bash
hermes webhook subscribe alerts   --deliver telegram --deliver-chat-id "123456789"   --deliver-only   --prompt "Alert: {alert.name}"
```

### Troubleshooting
1. Is the gateway running? `systemctl --user status hermes-gateway`
2. Is the webhook server listening? `curl http://localhost:8644/health`
3. Signature mismatch? Verify the secret matches in `hermes webhook list`
4. Wrong event type? Use `hermes webhook test <name>` to verify

---

## §7 Docker Management

**Manage Docker containers, images, volumes, networks, and Compose stacks — lifecycle ops, debugging, cleanup, and Dockerfile optimization.**

### Quick Reference

| Task | Command |
|------|---------|
| Run container (background) | `docker run -d --name NAME IMAGE` |
| Stop + remove | `docker stop NAME && docker rm NAME` |
| View logs (follow) | `docker logs --tail 50 -f NAME` |
| Shell into container | `docker exec -it NAME /bin/sh` |
| List all containers | `docker ps -a` |
| Build image | `docker build -t TAG .` |
| Compose up | `docker compose up -d` |
| Disk usage | `docker system df` |

### Container Operations

```bash
# With environment variables
docker run -d -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=mydb --name db postgres:16

# With persistent data (named volume)
docker run -d -v pgdata:/var/lib/postgresql/data --name db postgres:16

# With resource limits and restart policy
docker run -d --memory=512m --cpus=1.5 --restart=unless-stopped --name app my-app
```

### Docker Compose

```yaml
services:
  api:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  pgdata:
```

### Debugging Third-Party Images

Third-party images often have undocumented assumptions. When a fresh container crash-loops:

1. Check logs: `docker logs NAME 2>&1 | tail -30`
2. Find the container's internal user: `docker run --rm IMAGE id`
3. Fix host permissions: `chown -R UID:GID /host/path`
4. Pre-create app-specific subdirectories the app expects
5. Test interactively: `docker run --rm -it --entrypoint /bin/sh IMAGE`

### Pitfalls
- **Container exits immediately** → Main process finished or crashed. Check `docker logs NAME`
- **"port is already allocated"** → `docker ps` or `lsof -i :PORT`
- **"no space left on device"** → `docker system df` then targeted prune
- **Can't connect to container** → App binds to 127.0.0.1 inside container. Must bind to `0.0.0.0`
- **Traefik returns 404** → Container needs `--network traefik-net` and proper labels

---

## §8 Skill-to-Web-App

**Wrap an existing Hermes skill as a public-facing website deployed on Vercel.**

### When to Use
- User wants to expose an existing skill to the public via a web interface
- The skill involves image upload, form input, and report generation
- Need a self-contained, no-login, instant-value web app

### Architecture
Single Next.js app with:
- **Frontend**: React page with image upload + form inputs
- **API Route** (`/app/api/xxx/route.js`): Edge runtime, handles all skill logic
- **Results page**: Inline component displaying the generated report
- **Deploy**: Vercel

### Step-by-Step

1. Create project:
```bash
mkdir -p my-web-app/app/api/xxx
```

2. **package.json** (Next.js 15, React 18):
```json
{
  "name": "my-web-app",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^15.1.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  }
}
```

3. **Build all files BEFORE npm install** — write all source files first, then run `npm install`

4. **API route (edge runtime):**
```js
export const runtime = 'edge'
export async function POST(request) {
  const formData = await request.formData()
  const image = formData.get('image')
  const bytes = await image.arrayBuffer()
  const base64 = Buffer.from(bytes).toString('base64')
  // Call AI, external APIs, calculate, return JSON
}
```

5. **Deploy to Vercel:**
```bash
cd my-web-app && npm install
VERCEL_TOKEN=... vercel --token "$VERCEL_TOKEN" --name my-web-app --confirm
```

### Pitfalls

**DO NOT over-investigate before building** — start building.

**Terminal REDACTS secret values** — if you grep a secret and try to use it in a Python string, you get `***` instead of the real value. Write a Python script to read the secret directly from source files.

**Edge runtime limitations:**
- No Node.js-only modules (fs, path) — use edge-compatible alternatives
- No `require()` — use ESM only
- `Buffer.from()` for encoding is available in edge

**Verified working models (April 2026):**
- `google/gemini-2.0-flash-001` — Vision + fast, free tier
- `google/gemini-2.0-flash-lite-001` — cheaper, no vision
- `anthropic/claude-sonnet-4-6-20250514` — high quality

**Avoid:** `google/gemini-2.5-flash:free` does NOT exist on OpenRouter.
