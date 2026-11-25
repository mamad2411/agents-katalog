---
name: aapanel
description: Operate aaPanel / BT Panel hosting servers through the free, open-source aapanel-mcp MCP server — 282 tools for websites, databases, SSL, FTP, files, firewall, cron jobs, Docker, projects, logs, monitoring, server optimization, and security (hardening, WAF, virus scan, CVE scan), with a built-in safety guard on destructive actions. What you need: an aaPanel server with the API interface enabled (Settings → API Interface → copy token) and the aapanel-mcp MCP server installed (pip install aapanel-mcp or uvx aapanel-mcp). A servers.yaml config template is included in this skill. Use when the user mentions aaPanel, their hosting panel, or VPS/server administration — deploying a site, issuing SSL, managing databases or cron, a slow or full server, or hardening/securing a panel.
---

# aaPanel Server Management

Drive aaPanel hosting panels through the **aapanel-mcp** MCP server: 282 tools across 20 modules (system, sites, databases, FTP, files, firewall, crontab, SSL, panel config, plugins, Docker, projects, logs, SSH, terminal, backups, monitoring, deployment, optimization, security).

## Setup (one-time)

1. **Install the MCP server**: `pip install aapanel-mcp` (or run without installing: `uvx aapanel-mcp`). Standalone binaries are available on the [GitHub releases](https://github.com/nipunanirmal/aapanel-mcp/releases/latest) page.
2. **Get the API token**: in the aaPanel web UI go to **Settings → API Interface**, enable it, and copy the token.
3. **Configure panels** in `~/.aapanel-mcp/servers.yaml`:

   ```yaml
   servers:
     - name: "prod-01"
       host: "http://YOUR_SERVER_IP:8888"
       token: "YOUR_API_TOKEN"
       verify_ssl: false
       timeout: 30

   global:
     default_server: "prod-01"
   ```

   Config search order: `AAPANEL_CONFIG_PATH` env var → `./config/servers.yaml` → `~/.aapanel-mcp/servers.yaml`. A ready-made template is included in this skill package as `servers.yaml.example` — copy it to `servers.yaml` and fill in your panel details.

4. **Register the MCP server** in the client (Windsurf, Cursor, Claude Desktop, etc.):

   ```json
   {
     "mcpServers": {
       "aapanel": {
         "command": "aapanel-mcp",
         "env": { "AAPANEL_CONFIG_PATH": "/path/to/servers.yaml" }
       }
     }
   }
   ```

   If not installed globally, use `"command": "uvx"` with `"args": ["aapanel-mcp"]`.

## Tool conventions

- Tool names follow `<module>_<action>`: `site_create`, `database_list`, `ssl_apply_letsencrypt`, `firewall_add_port`, `crontab_create`, `docker_container_list`, `cve_scan_list`, ...
- Every tool accepts an optional `server` parameter to target a specific configured panel; omit it to use the default.
- Destructive tools accept a `confirmed` boolean — see Safety below.
- Responses are pretty-printed JSON. Errors read `Error: <msg> | Endpoint: <ep> | Type: <type>`.

## Safety guard — read before any destructive action

The guard is enforced inside the MCP server at the API-client level; no tool can bypass it.

**Permanently blocked (never allowed, even with confirmation):**
- Deleting files under `/www/server/*`, `/www/wwwroot`, `/www/backup`, `/www/database`, `/root`, `/etc`, `/boot`, `/proc`, `/sys`, `/dev`, `/var/lib/mysql|docker|redis|postgresql`
- Dropping system databases: `mysql`, `information_schema`, `performance_schema`, `sys`, `postgres`, `template0`, `template1`

**Requires explicit user confirmation in chat** (only pass `confirmed=true` after the user agrees): deleting sites, databases, backups, files (outside protected paths), FTP users, firewall rules, cron jobs, SSL certs; stopping sites/containers; uninstalling plugins/software; killing processes; restarting the server or panel; closing the panel; disabling SSH password auth; log/session cleanup.

Never set `confirmed=true` on your own initiative. Show the user exactly what will be deleted or stopped, get an explicit yes, then proceed. A blocked call returns `BLOCKED: ...` or `CONFIRMATION REQUIRED: ...` instead of executing.

## Workflows

### "My server is slow" / health check
1. `system_get_status` — CPU, memory, disk, network, load in one call
2. `abnormal_check_all` — anomaly scan across MySQL, PHP, CPU, memory, disk
3. High CPU → `cpu_get_high_cpu_processes`, then `process_list`; `process_kill` only with confirmation
4. Memory pressure → `memory_get_info`; offer `system_release_memory` or `system_clear_all_cache` (both need confirmation)
5. Disk full → `storage_get_disk_info` → `storage_get_dir_size` on suspects → clean site/panel logs (`system_clear_site_logs`, confirmation required)

### Deploy a website
1. `site_create` — `webname` (comma-separated domains), `path` (aaPanel convention: `/www/wwwroot/<domain>`), `type_id` (0=PHP, 1=proxy, 2=static), `version` (PHP version, e.g. `83` for 8.3)
2. Needs a database → `database_create`, then `database_set_access` (keep `127.0.0.1` for sites on the same host)
3. SSL → `ssl_apply_letsencrypt` (domain must already resolve to the server), then `site_force_https`
4. Verify → `site_get_ssl`, `site_get_traffic_stats`

### SSL management
- Inventory: `ssl_get_list`, per-site: `site_get_ssl`
- Issue/renew: `ssl_apply_letsencrypt`, `ssl_renew`
- Removing a cert needs confirmation (`ssl_delete_cert`)

### Security audit / hardening
1. `security_baseline_scan` → `security_baseline_get_result` → repair items with `security_baseline_repair` (or `security_baseline_repair_all`)
2. SSH: `harden_get_ssh_config` → prefer key auth (`harden_set_ssh_key_auth`). Disabling password auth (`harden_disable_ssh_password`) is destructive — verify key login works first and confirm with the user
3. Panel access: `harden_set_ip_whitelist`, `harden_set_admin_path`, `harden_set_basic_auth`, `harden_set_two_step_auth`
4. Malware/CVE: `virus_scan_safe_detect`, `cve_scan_list` (progress via `cve_get_scan_progress`)
5. Alerts: `alert_get_warning`, `alert_set_warning`

### Emergency security response (e.g. "patch this CVE now")
When the user forwards a vulnerability alert (e.g. actively-exploited PHP RCE), don't just patch the obvious thing — inventory everything:
1. Verify the advisory (web search): affected versions, fixed versions, interim mitigations
2. Inventory ALL runtimes of the affected component: `php_get_config` per version + `terminal_execute_command` for distro packages, LiteSpeed, and every Docker container (containers bundle their own runtimes)
3. Map vulnerable → fixed; flag EOL runtimes that need an app/image upgrade instead of a patch
4. Back up configs (`/www/server/php/<v>/etc`, vhosts) and ask the user to take a provider snapshot before in-place updates
5. Update: panel PHP via `/www/server/panel/install/php.sh update <major>` — patch the pinned version in the script first and add a php.net source fallback (vendor mirrors lag release day); Docker: rebuild with `--pull` on updated bases or pull patched app images
6. Restart the serving process — old workers keep running vulnerable code until restarted
7. VERIFY the version actually served: temp `<?php echo PHP_VERSION; ?>` file requested through the live domain, then delete it — `php -v` alone proves nothing about FPM
8. Sweep for compromise: webshell patterns in webroots, new cron entries, SSH keys, odd listeners
9. Report per-runtime: before → after, and what was skipped plus why (EOL, vendor repo lag)

### Backups
- On demand: `site_backup`, `database_backup`; list via `site_get_backup_list`, `database_get_backups`, `backup_list`
- Scheduled: `crontab_create` (backup job type); deleting a cron job needs confirmation

### Multi-server fleets
All tools accept `server="<name>"` matching a `servers.yaml` entry. When touching an unfamiliar panel, start with `system_get_system_version` to check the aaPanel version.

## Optional modules (fail gracefully when absent)

| Tools | Requires |
|-------|----------|
| `waf_*` | btwaf (Web Application Firewall) plugin |
| `docker_*` | Docker runtime on the panel host |
| `service_get_memcached_status`, `service_get_redis_status` | Memcached / Redis installed |
| `virus_scan_web`, `virus_scan_get_web_result` | webbasicscanning module |
| `terminal_execute_command` | aaPanel Terminal Bridge plugin — check `terminal_bridge_status`; `terminal_install_bridge` downloads a release ZIP only after a second call with `confirmed=true` |

## Troubleshooting

- **404 or unexpected response after an aaPanel update** — endpoint drift. Check the version (`system_get_system_version`). v8-only routes automatically fall back to legacy v1 endpoints; if a tool still fails, the endpoint mapping in `aapanel_mcp/tools/*.py` may need updating (see the Contributing section of the repo README).
- **"No configuration file found"** — set `AAPANEL_CONFIG_PATH` or create `~/.aapanel-mcp/servers.yaml`.
- **`Server 'x' not found`** — name mismatch with `servers.yaml`; the error lists available names.
- **Connection refused / timeout** — wrong host/port, the API interface is disabled (enable under Settings → API Interface), or a firewall blocks the API port.
- **Self-signed panel certificate** — keep `verify_ssl: false` (the default).
- **Compatibility** — tested against aaPanel 8.0.7 and 8.0.4; 7.x untested.

## Reference

- Repository: https://github.com/nipunanirmal/aapanel-mcp
- PyPI: https://pypi.org/project/aapanel-mcp/ — `pip install aapanel-mcp` / `uvx aapanel-mcp`
- Full tool catalog by module: README in the repository
