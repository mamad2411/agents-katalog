---

name: systemd-port-reservation
description: Lock a specific port to a long-running Node/Vite service using systemd — prevents any other process from stealing it, auto-restarts on crash, survives reboots.
version: 1.0.0
metadata:
  hermes:
    tags: [systemd, port, vite, node, devops, auto-restart, linux]

---
Use this when you need a port permanently owned by a specific service on a Linux VPS — no other process can accidentally grab it, and the service auto-restarts on crash or reboot.

## What This Skill Does

This skill Lock a specific port to a long-running Node/Vite service using systemd — prevents any other process from stealing it, auto-restarts on crash, survives reboots.

## Key Lessons Learned (Trial and Error)

### DO NOT use systemd socket activation (.socket unit)
The instinct to use a `.socket` unit to "pre-bind" the port sounds right but FAILS with Vite/Node.
Reason: systemd holds the socket fd and passes it via fd inheritance — but Vite does its own `listen()` call and sees the port as already in use, then tries to fall back to another port.
Result: Vite logs "Port 3001 is in use, trying another one..." and binds to a random port instead.

### Correct approach: service-only with --strictPort + ExecStartPre guard

- Use a plain `.service` unit (no `.socket` unit)
- Pass `--strictPort` to Vite so it errors out instead of silently switching ports
- Add `ExecStartPre` to fail fast if something else somehow grabs the port before startup
- Set `Restart=always` + `StartLimitIntervalSec=0` for infinite auto-restart

## Step-by-Step

### 1. Kill any existing background process on the port

```bash
pkill -f "vite.*PORT" 2>/dev/null
pkill -f "pnpm.*dev" 2>/dev/null
sleep 2
ss -tlnp | grep PORT && echo "still running" || echo "port free"
```

### 2. Write the service file

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

### 3. Enable and start

```bash
systemctl daemon-reload
systemctl enable MY-SERVICE.service
systemctl start MY-SERVICE.service
```

### 4. Verify

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

## Hermes Workspace Specific Values

- Service name: `hermes-workspace`
- Port: `3001`
- WorkingDirectory: `/root/.openclaw/workspace/hermes-workspace`
- ExecStart: `/usr/bin/pnpm dev --port 3001 --strictPort`
- Service file: `/etc/systemd/system/hermes-workspace.service`

## Pitfalls

- **Don't create a .socket unit alongside the .service** — it will pre-bind the port and break Vite
- **pnpm's dev script may hardcode --port 3000 in package.json** — passing `--port 3001` on the CLI overrides it; `--strictPort` ensures no silent fallback
- **StartLimitIntervalSec=0** is required for truly infinite restarts — without it systemd stops retrying after a burst of failures
- **ExecStartPre grep pattern** — use `:PORT ` (with trailing space) to avoid matching port 30010, 30011, etc.

## Useful Commands

```bash
# View live logs
journalctl -u hermes-workspace.service -f

# Restart manually
systemctl restart hermes-workspace.service

# Check port ownership
ss -tlnp | grep 3001
```
