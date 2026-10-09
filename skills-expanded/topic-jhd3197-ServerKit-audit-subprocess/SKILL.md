---
name: audit-subprocess
description: Scan backend services for subprocess bugs — missing sudo, missing exception handling on distro-specific commands, raw subprocess calls bypassing system utilities, and container/environment assumptions that break in LXC or restricted environments. Reports issues with file, line, and fix.
argument-hint: "[file-or-directory]"
---

Audit subprocess calls in ServerKit backend services for recurring bug patterns.
Scope: **${ARGUMENTS:-backend/app/services/}**

## What to Scan For

### Pattern 1: Missing `sudo` on privileged commands

Search for `subprocess.run()` calls that invoke commands requiring root but lack `sudo`:

- **`systemctl`** (start, stop, restart, enable, disable, daemon-reload) — ALL require sudo
- **`firewall-cmd`** (--state, --get-default-zone, --list-services, --list-ports, --list-rich-rules, --get-zones, --zone=*, --add-*, --remove-*, --reload) — ALL require sudo
- **`ufw`** (status, enable, disable, allow, deny, delete) — ALL require sudo
- **`iptables`** / **`ip6tables`** — ALL require sudo
- **`nginx`** (-s reload, -t) — ALL require sudo
- **`certbot`** — ALL require sudo
- **`freshclam`** — requires sudo

For each match, check if the command list starts with `'sudo'`. If not, flag it.

**Ignore**: Commands that legitimately don't need sudo (git, python, pip, npm, node, which, cat, ls, grep, df, free, uptime, whoami, hostname, lsb_release).

### Pattern 2: Missing exception handling on distro-specific commands

Search for `subprocess.run()` calls that use distro-specific package managers without `try/except FileNotFoundError`:

- **`dpkg`** — Debian/Ubuntu only, doesn't exist on RHEL/Fedora/CentOS
- **`apt`** / **`apt-get`** — Debian/Ubuntu only
- **`rpm`** — RHEL family only, doesn't exist on Debian
- **`dnf`** / **`yum`** — RHEL family only

For each match, check if it's wrapped in a `try/except` that catches `FileNotFoundError` (or a broad `Exception` on the immediate call). If not, flag it.

**Acceptable**: If the call is guarded by `os.path.exists('/usr/bin/<cmd>')` before the subprocess call, that's fine — don't flag it.

### Pattern 3: Raw subprocess calls that should use system utilities

The project provides centralized utilities in `app/utils/system.py`. Flag direct subprocess calls that bypass them:

- **`subprocess.run(['sudo', 'systemctl', ...])`** → should use `ServiceControl.start/stop/restart/reload/enable/disable/daemon_reload()`
- **`subprocess.run(['systemctl', 'is-active', ...])`** → should use `ServiceControl.is_active()`
- **`subprocess.run(['systemctl', 'is-enabled', ...])`** → should use `ServiceControl.is_enabled()`
- **`subprocess.run(['dpkg', ...])`** or **`subprocess.run(['rpm', ...])`** for package checks → should use `PackageManager.is_installed()`
- **`os.path.exists('/usr/bin/apt')`** or similar distro detection → should use `PackageManager.detect()`
- **`for path in ['/usr/bin/X', '/usr/sbin/X']: if os.path.exists(path)`** binary search → should use `is_command_available()`
- **`subprocess.run(['sudo', 'apt-get', 'install', ...])`** or **`['sudo', 'dnf', 'install', ...]`** → should use `PackageManager.install()`
- **`subprocess.run(['sudo', <privileged-cmd>, ...])`** for other privileged commands → should use `run_privileged()`

**Acceptable exceptions** (do NOT flag these):
- Docker CLI calls in `docker_service.py` (uses Docker socket)
- Git CLI calls (no privilege needed)
- Python/pip in venvs (per-app, no root)
- MySQL/PostgreSQL CLI (auth via socket/password)
- WP-CLI (`sudo -u www-data` pattern)
- Read-only commands (`clamscan`, `fail2ban-client status`, `uname`, `which`, `ssh-keygen`, etc.)

### Pattern 4: Container/environment assumptions

Code that assumes bare-metal or KVM and breaks inside LXC containers, Docker, or restricted environments. Search for these patterns:

#### 4a. Unguarded `/proc` and `/sys` reads

- **`open('/proc/cpuinfo')`** or similar `/proc/` reads without `try/except (FileNotFoundError, PermissionError)`
- **`open('/sys/class/...')`** or `/sys/` reads — often restricted in unprivileged containers
- **`/proc/meminfo`**, **`/proc/net/`**, **`/proc/diskstats`** — may be empty or permission-denied

Flag if the read is NOT wrapped in a try/except that handles `FileNotFoundError` or `PermissionError`.

#### 4b. `psutil` calls that fail in containers

- **`psutil.disk_io_counters()`** — returns `None` when `/proc/diskstats` is unavailable
- **`psutil.disk_partitions()`** — returns container-internal mounts, not host disks
- **`psutil.sensors_temperatures()`** — fails without `/sys/class/thermal/`
- **`psutil.sensors_fans()`** — same issue
- **`psutil.net_io_counters(pernic=True)`** — may show veth interfaces only

Flag if the return value is used without a `None` / empty check. For example, `psutil.disk_io_counters().read_bytes` will crash if the call returns `None`.

#### 4c. Docker socket assumptions

- **`subprocess.run(['docker', ...])`** without checking if Docker is installed/running first
- Direct access to **`/var/run/docker.sock`** without verifying the socket exists
- Any Docker operation that doesn't handle `FileNotFoundError` or `ConnectionError`

Flag if there's no pre-check (e.g., `is_docker_installed()`) or no try/except around the call.

**Acceptable**: Calls inside `docker_service.py` that are already gated behind `is_docker_installed()` at the API layer.

#### 4d. Firewall/network commands without capability checks

- **`firewall-cmd`**, **`ufw`**, **`iptables`** — require `CAP_NET_ADMIN` which is dropped in unprivileged LXC
- These commands fail silently or with cryptic errors when capabilities are missing

Flag if the subprocess call doesn't handle the failure case (no try/except, or no check of `returncode`).

#### 4e. Hardcoded device paths

- **`/dev/`** references (e.g., `/dev/sda`, `/dev/null` is fine) — block devices don't exist in containers
- **`/dev/fuse`** — FUSE device, unavailable in unprivileged LXC

Flag hardcoded `/dev/` paths (except `/dev/null`, `/dev/stdin`, `/dev/stdout`, `/dev/stderr`, `/dev/urandom`, `/dev/random`).

**Acceptable**: Paths discovered dynamically from `psutil` or `lsblk` output.

## How to Audit

1. Use **Grep** to find all `subprocess.run(` calls in the target scope
2. For each match, read the surrounding context (5-10 lines) to check:
   - Is `sudo` present for privileged commands?
   - Is there a `try/except FileNotFoundError` for distro-specific commands?
   - Is there an `os.path.exists()` guard?
   - Is there a system utility (`ServiceControl`, `PackageManager`, `run_privileged`, `is_command_available`) that should be used instead?
3. Also search for `os.path.exists('/usr/bin/apt')` and similar distro-detection patterns
4. Search for `open('/proc/` and `open('/sys/` — check for missing error handling
5. Search for `psutil.disk_io_counters`, `psutil.disk_partitions`, `psutil.sensors_` — check return values are guarded against `None`
6. Search for `/dev/` string literals — flag hardcoded device paths (except standard ones)
7. Search for `docker` subprocess calls outside `docker_service.py` — check for availability guards
8. For firewall commands, check that `returncode` is inspected or the call is wrapped in try/except
9. Collect all violations

## Report Format

For each issue found, report:

```
[PATTERN] file_path:line_number
  Command: ['systemctl', 'restart', ...]
  Fix: Add 'sudo' as first element
```

or for Pattern 3:

```
[PATTERN 3] file_path:line_number
  Command: subprocess.run(['sudo', 'systemctl', 'restart', service], ...)
  Fix: Use ServiceControl.restart(service)
```

Then provide a summary:

```
## Summary
- Files scanned: X
- Total subprocess calls: X
- Missing sudo: X instances across Y files
- Missing exception handling: X instances across Y files
- Should use system utilities: X instances across Y files
- Container/environment assumptions: X instances across Y files
- Clean: X calls
```

If issues are found, ask the user if they want you to fix them automatically.
If no issues are found, confirm the codebase is clean for these patterns.
