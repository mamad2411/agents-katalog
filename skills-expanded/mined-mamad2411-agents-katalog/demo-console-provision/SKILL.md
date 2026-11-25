---
name: demo-console-provision
description: "Add one or more FRR routers to the running ContainerLab demo topology and wire up web consoles (ttyd + nginx + dashboard HTML) without disrupting existing consoles. Use when the user asks to add new routers to the demo lab and wants them accessible from the console dashboard."
version: 1.0.0
license: Apache-2.0
author: netclaw
tags: [demo, console, containerlab, ttyd, nginx]
mcp_servers: []
---

# Demo Console Provision

Add new FRR routers to a running ContainerLab demo and wire them into the web console dashboard — all without disrupting existing consoles or services.

## When to Use

- User asks to add one or more new routers to the demo lab
- User wants new routers accessible from the console dashboard like the existing ones
- User wants to expand the topology live without tearing anything down

## What This Skill Does

For each new router requested:

1. **Deploy the router into the running ContainerLab topology** (via `clab deploy` with `--reconfigure`)
2. **Create a ttyd wrapper script** at `/usr/local/bin/router-<name>.sh`
3. **Launch a ttyd process** on the next available port (starting from 7688)
4. **Add an nginx location block** to `/etc/nginx/sites-available/console`
5. **Add a card to the HTML dashboard** at `/var/www/console/index.html`
6. **Reload nginx gracefully** — zero disruption to existing WebSocket sessions

## Port Allocation

Existing port assignments (DO NOT reuse):

| Port | Service |
|------|---------|
| 7681 | P1 |
| 7682 | P2 |
| 7683 | P3 |
| 7684 | P4 |
| 7685 | RR1 |
| 7686 | PE1 |
| 7687 | OpenClaw TUI |

New routers start at **7688** and increment. To find the next free port, check what ttyd processes are running:

```bash
ss -tlnp | grep ttyd | awk '{print $4}' | grep -oP '\d+$' | sort -n | tail -1
```

If no ttyd is running above 7687, start at 7688. Otherwise, use max + 1.

## Procedure

### Step 1: Determine Next Available Ports

```bash
LAST_PORT=$(ss -tlnp | grep ttyd | awk '{print $4}' | grep -oP '\d+$' | sort -n | tail -1)
NEXT_PORT=$((LAST_PORT + 1))
```

If multiple routers are requested, allocate sequential ports: NEXT_PORT, NEXT_PORT+1, etc.

**Before using a port, verify it's actually free:**

```bash
# Kill any zombie process on the target port
sudo fuser -k $NEXT_PORT/tcp 2>/dev/null || true
sleep 1
ss -tlnp | grep :$NEXT_PORT && echo "ERROR: port still in use" || echo "OK: port free"
```

### Step 2: Update ContainerLab Topology

Edit `/home/ubuntu/netclaw-demo/lab/netclaw-demo/netclaw-demo.clab.yml` to add the new node(s) and link(s), then reconfigure:

```bash
sudo clab deploy -t /home/ubuntu/netclaw-demo/lab/netclaw-demo/netclaw-demo.clab.yml --reconfigure
```

The `--reconfigure` flag adds new nodes without destroying existing ones.

Each new node needs:
- A `configs/<name>/daemons` file (copy from an existing node like p1)
- A `configs/<name>/frr.conf` file (can be minimal/blank initially)
- An entry under `topology.nodes` in the clab YAML
- Link entries under `topology.links` connecting it to the fabric

### Step 3: Create ttyd Wrapper Scripts

For each new router (e.g., `pe2`):

```bash
cat > /usr/local/bin/router-pe2.sh <<'EOF'
#!/bin/bash
while true; do
  if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "clab-netclaw-demo-pe2"; then
    docker exec -it clab-netclaw-demo-pe2 vtysh
  else
    echo "Router PE2 is not running yet. Waiting..."
    sleep 5
  fi
done
EOF
chmod +x /usr/local/bin/router-pe2.sh
```

### Step 4: Launch ttyd Instances

First, verify the port is actually free. If something is bound to it, kill it:

```bash
# Check if port is in use and kill the occupying process
fuser -k 7688/tcp 2>/dev/null || true
sleep 1
```

Then launch ttyd as a **systemd transient service** (more reliable than nohup in an agent shell context):

```bash
sudo systemd-run --unit=ttyd-pe2 --remain-after-exit -- ttyd -p 7688 -W /usr/local/bin/router-pe2.sh
```

**Why systemd-run instead of nohup?** When the agent runs shell commands, nohup processes can still get killed if the parent shell session is cleaned up or if stdout/stderr pipes break. `systemd-run` creates a proper background service that survives independently.

If `systemd-run` is not available or fails, fall back to:

```bash
nohup ttyd -p 7688 -W /usr/local/bin/router-pe2.sh > /var/log/ttyd-pe2.log 2>&1 &
disown
sleep 2
# Verify it's actually running
ss -tlnp | grep :7688 || echo "ERROR: ttyd failed to bind port 7688"
```

**Always verify the port is listening after launch.** If it's not, check `/var/log/ttyd-pe2.log` for errors.

### Step 5: Add Nginx Location Blocks

Append to `/etc/nginx/sites-available/console` inside the `server {}` block, before the closing brace:

```nginx
location /pe2/ { set $auth_ok 0; if ($cookie_demo_sess = "valid") { set $auth_ok 1; } if ($arg_token) { set $auth_ok 1; } if ($auth_ok = 0) { return 401; } proxy_pass http://127.0.0.1:7688/; proxy_http_version 1.1; proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection "upgrade"; proxy_set_header Host $host; }
```

Then reload:
```bash
nginx -t && sudo systemctl reload nginx
```

### Step 6: Update HTML Dashboard

Insert a new card into the `.grid` div in `/var/www/console/index.html`:

```html
<div class="card"><h3>PE2</h3><p>PE Router</p><a class="btn" href="/pe2/" target="_blank">Open Console</a></div>
```

Insert BEFORE the TUI card (so TUI stays last).

## Handling Multiple Routers

When the user asks for multiple routers at once, repeat Steps 3-6 for each router with incrementing ports. Batch all nginx location blocks into a single edit and do one `nginx -t && systemctl reload nginx` at the end.

Example — adding PE2, PE3, and CE1:

| Router | Port | Path | Role |
|--------|------|------|------|
| PE2 | 7688 | /pe2/ | PE Router |
| PE3 | 7689 | /pe3/ | PE Router |
| CE1 | 7690 | /ce1/ | CE Router |

## Important Rules

1. **Never kill existing ttyd processes** — each runs independently on its own port
2. **Never replace the nginx config wholesale** — only append location blocks
3. **Always run `nginx -t` before reload** — abort if syntax check fails
4. **Use `systemctl reload` not `restart`** — reload is graceful, restart drops connections
5. **Container naming convention** — containers are always `clab-netclaw-demo-<name>`
6. **The TUI card must remain last** in the HTML dashboard grid
7. **FRR daemons file** — must enable zebra, bgpd, ospfd at minimum (copy from existing node)
8. **No ITSM gating** — this is a lab/demo operation, no CR required

## Verification

After provisioning, confirm:

```bash
# Container is running
docker ps --format '{{.Names}}' | grep clab-netclaw-demo-<name>

# ttyd is listening
ss -tlnp | grep :<port>

# Nginx routes correctly
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:7680/<name>/

# Dashboard HTML has the card
grep -q "<name>" /var/www/console/index.html
```

## Rollback

To remove a console without affecting others:

```bash
# Kill the specific ttyd
pkill -f "ttyd -p <port>"

# Remove the nginx location block (edit the file)
# Reload nginx
sudo systemctl reload nginx

# Remove the HTML card
# Remove the wrapper script
rm -f /usr/local/bin/router-<name>.sh
```

To remove the router from ContainerLab entirely:
```bash
sudo clab destroy -t /home/ubuntu/netclaw-demo/lab/netclaw-demo/netclaw-demo.clab.yml --node-filter <name>
```
