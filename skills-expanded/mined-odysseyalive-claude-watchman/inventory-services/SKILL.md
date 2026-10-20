---
name: inventory-services
description: "OBSERVE: inventory what is installed and how it serves — web server, database, php-fpm — so other skills know what surface exists to check."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# inventory-services (Grammar / Observe)

Establishes *what is running*. A factual inventory of the service surface, so the
other skills (security headers, CORS, log inspection) know what exists to examine.
Read-only.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## When to use

Early in every `/watchman audit` / `/watchman inventory`, before the skills that
depend on knowing which web server or database is present.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher —
   `bash lib/wm <function> [args…]` — which sources the libs (`lib/journal.sh`,
   `lib/distro.sh`, `lib/profile.sh`) under bash internally; never `source lib/…` directly
   (dontAsk refuses a dot-source). Initialize with `bash lib/wm journal_init`; resolve
   family/profile via `bash lib/wm watchman_family` / `bash lib/wm watchman_profile`.
2. **Web server.** Enumerate EVERY web server present with `bash lib/wm webserver_detect` —
   it scans the `/etc` config roots and packages across nginx, apache (apache2 /
   httpd), **Caddy, lighttpd, and OpenLiteSpeed**, so niche/non-default builds are
   not missed. For each, record: its config root, whether the resolved unit is
   active/enabled (`bash lib/wm service_status` / `bash lib/wm service_enabled`), and the directories that
   actually hold its logs via `bash lib/wm webserver_log_paths` (parsed from the config —
   custom `access_log`/`CustomLog` targets and per-vhost logs included — never a
   bare `/var/log` assumption). These resolvers are family-blind: on `darwin` they cover the
   Homebrew prefixes (`<brew_prefix>/etc/nginx`, macOS's `/etc/apache2`) and read service
   state via `brew services`, exactly as they use `/etc` + `systemctl` on Linux. This
   inventory is what tells inspect-logs and the security-header/CORS checks exactly which
   server, config, and log paths exist.
3. **Database.** Detect mariadb/mysql, postgresql similarly via `bash lib/wm pkg_is_installed`
   and `bash lib/wm service_status`.
4. **App runtime.** Detect php-fpm (and its version) and any obvious app server.
5. **Journal an inventory finding** per discovered service:
   `category=config`, `severity=info`, `risk_tier=safe`,
   `check_id=service_<name>`, `target=<bare unit name>` — the unit WITHOUT the
   `.service` suffix (`nginx`, never `nginx.service`), so the fingerprint is identical
   every run; a suffix that comes and goes run-to-run duplicates the finding instead
   of folding it. Title/detail describe version and enabled/active state. These `info`
   rows are context, not alarms.
6. **Profile sanity-check (mismatch finding).** Compare the discovered surface against
   the active `profile`. The dangerous direction is a **`workstation` profile that is
   actually serving the public** — because the server-only checks are then *silently
   skipped*. Detect it: if `profile == workstation` AND any inventoried web server /
   database is **listening on a non-loopback address**:
   - **Linux:** `ss -H -tln | awk '{print $4}'`
   - **macOS:** `netstat -an 2>/dev/null | awk '/LISTEN/{print $4}'`
   A loopback bind (`127.*` / `[::1]` / `::1.`) does NOT count. Journal exactly ONE
   finding:
   `category=config`, `severity=medium`, `risk_tier=manual`,
   `check_id=profile_mismatch_public_service`, `target=` (leave empty — keeps the
   fingerprint stable).
   - **title:** `Profile is 'workstation' but public-facing services are present`
   - **detail:** name the offending listeners and state the server-profile checks are not running.
   - **remediation:** `Re-run 'bash install.sh --profile server' or set WATCHMAN_PROFILE=server in config/watchman.conf then 'watchman preflight'. If intentional, mark this finding 'ignored'.`
   Do **not** flag the reverse (server profile on a quiet machine). Never change the
   profile yourself — `risk_tier=manual`.
7. **Stay family-blind.** Never call `apt`/`pacman`/`dnf`/`brew` directly — only the
   `pkg_*` and `service_*` resolvers.
<!-- /origin -->

## Grounding

All claude-watchman functions below are reached via `bash lib/wm <function>` — the
dispatcher sources these libs internally; never `source lib/…` directly.

- `lib/distro.sh` — `webserver_detect` / `webserver_config_roots` / `webserver_log_paths`
  (config-derived web-server + log discovery), `service_status`, `service_enabled`, `pkg_is_installed`.
- `lib/journal.sh` — `journal_upsert`.
- `net_connections` resolver (`ss -H -tln`) — listener addresses for the profile check.
- `lib/profile.sh` — `profile` (the active profile being sanity-checked).
- `manifest.json` — declared permissions.
