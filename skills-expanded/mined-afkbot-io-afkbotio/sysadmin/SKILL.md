---
name: sysadmin
description: "System administration via `bash.exec` for host inspection, package management, and service control. Use when tasks mention apt, dnf, yum, brew, package install or update, nginx setup, systemctl, or service status."
triggers:
  - apt update
  - apt install
  - dnf install
  - yum install
  - brew install
  - package install
  - package update
  - update packages
  - service status
  - systemctl
  - install nginx
  - обнови пакеты
  - установи nginx
  - установи пакет
tool_names:
  - bash.exec
preferred_tool_order:
  - bash.exec
execution_mode: executable
---
# sysadmin

Use this skill for package-manager and service-management tasks that should run through `bash.exec`.

## Workflow
1. Read `# Trusted Runtime Notes` first for OS, distro, shell, package managers, root state, and service manager.
2. If package manager or service manager is still unclear, inspect with one safe shell command before mutating the system.
3. Choose the right package manager for the detected host instead of assuming `apt`.
4. Run one bounded command at a time and check the result before the next command.
5. For commands that may prompt for confirmation, start `bash.exec` with `yield_time_ms` and keep reusing the returned `session_id` with `chars` until the command exits.
6. After installs or service changes, verify with a status or version check.

## Good probes
- `cat /etc/os-release 2>/dev/null || uname -a`
- `command -v apt || command -v dnf || command -v yum || command -v brew || true`
- `command -v systemctl || true`
- `id -u`

## Good execution patterns
- update package indexes: `sudo apt update`
- install nginx on Debian or Ubuntu: `sudo apt install -y nginx`
- check service status: `systemctl status nginx --no-pager`
- reload service after config change: `sudo systemctl reload nginx`

## Rules
- Do not hardcode `apt` when trusted runtime facts or inspection show another package manager.
- Prefer verification after every mutating step.
- Avoid long destructive command chains when one smaller command can prove the next step.
- If `bash.exec` returns a live `session_id`, do not finalize yet; continue the same shell session with `chars` or empty polls until it exits.
- Runtime routes the correct skill automatically; do not send `skill_name`.
