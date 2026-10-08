---
name: aaPanel Website-Troubleshoot
description: >
  Diagnose and fix aaPanel website access problems and service start failures.
  Use this skill when users report: site not opening, 403/404/500/502/503 errors,
  blank/white page, database connection errors, nginx or php-fpm start failure,
  service start failed with no specific reason, or any site down / access denied.
  Trigger keywords: site down, website not opening, website unreachable, 502,
  500, 403, 404, blank page, white page, nginx error, php-fpm error, start failed,
  database connection failed, connection refused, too many connections, access
  denied, site unreachable, service unavailable, bad gateway, site anomaly.
---

# aaPanel Website Troubleshoot

> **STOP. Read this document completely before doing anything.**
> **Your FIRST action is always `TodoWrite`** — create the diagnostic task list before running any probe or command.
> Do NOT skip sections. Execute the decision tree in order.
> Never show raw commands, btpython paths, or code blocks to users — report as plain text.

---

## Core Rules

1. **Always run the pre-check first** — never skip the `curl --resolve` loopback verification.
2. **Read before fixing** — diagnose the root cause before executing any repair action.
3. **Max 15 tool calls per task** — if exceeded, summarize findings and stop.
4. **Never let users type commands** — always execute via `RunCommand`.
5. **On error during fix** — report to user, do NOT retry automatically.
6. **Always inspect raw service logs** when a service reports "start failed" — the panel hint is usually too vague to act on.
7. **Forbidden operations**: delete site, drop database, delete files, `rm -rf`, `DROP TABLE/DATABASE`.
8. **Track every diagnosis with TodoWrite** — before starting Step 0, create a todo list of the planned diagnostic steps; set exactly one to `in_progress` while working it, mark `completed` the moment it finishes. Use `TodoRead` to re-check state if interrupted.

---

## Step 0 — Pre-Check (mandatory)

Before any diagnosis, confirm the site actually belongs to this server and the request is reaching it.

1. **First action — create your task list**: call `TodoWrite` to lay out the steps for this case (pre-check → probes → status-code branch → fix). Do this before any other tool call.
2. **Run**: `RunCommand: curl --resolve <domain>:80:127.0.0.1 -sS -o /dev/null -w '%{http_code}\\n' http://<domain>/`
   - Returns the actual HTTP status code reaching the panel's nginx.
3. **List sites**: `SiteList()` → find the matching `id`, `path`, `project_type`.
4. **If the site is not on this panel** (`curl` returns connection error or a different site): report to user that the domain may not be hosted here, do NOT proceed.

> Skip pre-check only if the user explicitly confirms the site is on this server, or provides a `site_id` directly.

---

## Step 1 — Two Probes

These probes are read-only and side-effect free. Create them, test, then **delete them** when done.

### Probe A — Static file (verifies domain binding + nginx + root path)

1. `RunCommand: echo 'aaPanel probe $(date)' > <site_path>/.probe_static.html`
2. `RunCommand: chown www:www <site_path>/.probe_static.html && chmod 644 <site_path>/.probe_static.html`
3. `RunCommand: curl --resolve <domain>:80:127.0.0.1 -sS http://<domain>/.probe_static.html`
4. **Expect**: returns the probe text with HTTP 200.
5. Clean up: `RunCommand: rm -f <site_path>/.probe_static.html`

### Probe B — PHP file (verifies PHP runtime + php-fpm socket)

1. `RunCommand: echo '<?php echo "aaPanel PHP probe ".PHP_VERSION; ?>' > <site_path>/.probe_php.php`
2. `RunCommand: chown www:www <site_path>/.probe_php.php && chmod 644 <site_path>/.probe_php.php`
3. `RunCommand: curl --resolve <domain>:80:127.0.0.1 -sS http://<domain>/.probe_php.php`
4. **Expect**: returns the probe text with the PHP version string.
5. Clean up: `RunCommand: rm -f <site_path>/.probe_php.php`

> Get `site_path` from `SiteList` → matching `path` field. `GetSitesConf([site_id])` returns the **raw vhost config text** (not structured fields) — locate the `root`, `access_log`, and `include enable-php-<ver>.conf;` directives by reading that text to verify the root path.

---

## Step 2 — Status Code Decision Tree

### 403 Forbidden — Permission / Ownership

**Goal**: confirm `www` owns the site directory tree, with 755/644 mode and readable parents.

1. `GetSitesConf([site_id])` → get `root` directory.
2. `RunCommand: ls -la <root>/` and `RunCommand: ls -la <parent_of_root>/` (parent matters).
3. Check:
   - Owner / group = `www:www` on root and all parents
   - Directory mode = `755`
   - File mode = `644`
4. If any are wrong (auto-fix, low risk):
   - `RunCommand: chown -R www:www <root>`
   - `RunCommand: find <root> -type d -exec chmod 755 {} \;`
   - `RunCommand: find <root> -type f -exec chmod 644 {} \;`
5. Re-test with the pre-check curl. If 403 persists, inspect the nginx error log:
   - `Read: /www/wwwlogs/<domain>.error.log` (last 50 lines, look for `directory index of "..." is forbidden` or `access denied`).

### 404 Not Found — Path / Rewrite

**First classify**: is the missing URL expected to be served dynamically (PHP route / framework route) or statically (a real file)?

- **Static 404** (e.g. `/favicon.ico`, `/uploads/foo.jpg`):
  1. `GetSitesConf([site_id])` → check `root` and `access_log` location.
  2. `RunCommand: ls -la <root>/<expected_path>` → file missing? wrong root?
  3. Verify `root` directive in vhost config matches the actual `site_path` from `SiteList`.

- **Dynamic 404** (e.g. `/category/news/`, `/article/123`, `/admin/login`):
  1. `GetSitesConf([site_id])` → look for `include .../rewrite/<domain>.conf;` line.
  2. `Read: /www/server/panel/vhost/rewrite/<domain>.conf` (if exists).
  3. **Common cause**: rewrite rules missing or wrong for the framework (WordPress / ThinkPHP / Laravel / Typecho / etc.).
  4. Fix (high risk — needs panel confirm): edit the rewrite file with `SearchReplace` per the framework's standard rules, then `RunCommand: nginx -t && nginx -s reload`.

### 500 Internal Server Error — Three Branches

Run the pre-check curl to confirm 500. Then check each branch:

#### Branch A — Database

1. Read `GetSitesConf` to find the project root, then look for the framework's DB config:
   - WordPress: `Read: <root>/wp-config.php` → extract `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`.
   - Other frameworks: look for `.env`, `config/database.php`, `application/database.php`, etc.
2. `MysqlTestConnection(db_name=<extracted_name>)` → returns `connected` and `version` on success.
3. If connection fails, the error message is auto-mapped by `mysql_engine.MYSQL_ERROR_MAP` — use that mapping directly:
   - `2002` / `2003` → MySQL is down. Go to **Service Start Failure → MySQL**.
   - `1045` → wrong password. Compare `DB_PASSWORD` in config with `databases` table; if mismatch, report to user (do NOT auto-reset DB password).
   - `1146` → table missing. `MysqlListDatabases` / `MysqlDescribeTable` to confirm, then report.
   - `1040` → too many connections. `MysqlQuery("SHOW GLOBAL STATUS LIKE 'Threads_connected'")` + `GetTopProcesses` to see who is connecting; suggest raising `max_connections` (high risk).

#### Branch B — Code (uncaught exception)

1. Enable PHP error display (high risk — needs confirm, and only if not in production):
   - `Read: /www/server/php/<ver>/etc/php.ini` → check `display_errors` and `error_reporting`.
2. `Read: /www/wwwlogs/<domain>.error.log` (last 100 lines) → look for PHP `Fatal error` / `Parse error` / `Uncaught` lines.
3. Report the file:line and error message to the user. Do NOT auto-edit site code.

#### Branch C — Config (HTTP 200 but blank page)

1. This is the **fastcgi.conf breakage** pattern: status is 200, body is empty, and the site worked before.
2. `Read: /www/server/nginx/conf/fastcgi.conf` → check whether it has been emptied / over-commented.
3. If abnormal, report to user. Fix requires restoring the panel's default `fastcgi.conf` (high risk — needs confirm and original file).

### 502 / 503 Bad Gateway / Service Unavailable — PHP-FPM Environment

1. `RunCommand: ps -ef \| grep php-fpm \| grep -v grep` → is php-fpm running?
2. `ServiceStatus("php-fpm-<ver>")` → confirm install + run state. Identify which version from `GetSitesConf`'s `include enable-php-<ver>.conf;` line.
3. `GetSitesConf([site_id])` → check the vhost actually includes the **same** `enable-php-<ver>.conf` as the running version.
4. `RunCommand: curl -sS http://127.0.0.1/phpfpm_<ver>_status` → check active processes, listen queue, max children.
   - If `listen queue` is non-zero → process pool exhausted. See OOM in **Service Start Failure → php-fpm**.
5. `GetSystemResources()` → if memory free < 200MB, OOM-killer may have hit php-fpm.
6. For **reverse-proxy 502**: `RunCommand: curl -v <upstream_host>` from the panel host → check if the upstream is reachable (firewall / DNS / upstream down).

---

## Step 3 — Service Start Failure

> **Core principle**: when the panel says "start failed" with no useful detail, **always read the raw service log first**. The panel hint is too vague to act on.

### 3.1 nginx

```bash
# 1. Syntax check — gives the exact file:line of any error
/www/server/nginx/sbin/nginx -t
```

Three common failure modes:

| Symptom | Cause | Fix |
|---|---|---|
| `unknown directive "xxx" in /www/server/panel/vhost/nginx/<site>.conf:N` | Site vhost has a typo / unsupported directive | `Read` the line, fix with `SearchReplace` (high risk), then re-run `nginx -t` |
| `bind() to 0.0.0.0:80 failed` / `bind() to [::]:443 failed` | Port occupied | `RunCommand: netstat -tlnp \| grep -E ':80\|:443'` → identify the conflicting process, report to user |
| `host not found in upstream "<name>"` | Upstream DNS unresolved at startup | Verify with `RunCommand: dig +short <name>`; if not resolvable, report to user. Fix: add `resolver` directive to the vhost, or replace with an IP (high risk) |

After the fix, **always** run `nginx -t` again, then `RunCommand: /etc/init.d/nginx restart` (or `ServiceRestart("nginx")`, high risk — needs confirm).

### 3.2 php-fpm

Get the version from the failing site's `enable-php-<ver>.conf` reference, then:

```bash
# 1. Tail the raw php-fpm error log — most informative
tail -n 50 /www/server/php/<ver>/var/log/php-fpm.log
```

| Symptom | Cause | Fix |
|---|---|---|
| `Unable to load dynamic library '<ext>.so'` / `segfault (core dumped)` | A newly installed PHP extension is broken | Bisect: in the panel go to App Store → PHP → Settings → Extensions, uninstall newly added extensions one by one, restarting (`RunCommand: /etc/init.d/php-fpm-<ver> restart`) after each |
| `active (exited)` immediately after start | OOM-killer killed it | `RunCommand: dmesg \| grep -E "php\|oom" \| tail -20` + `GetSystemResources` → reduce `pm.max_children` in `/www/server/php/<ver>/etc/php-fpm.conf` (high risk) |
| `bind() to /tmp/php-cgi-<ver>.sock failed: Address already in use` | Old php-fpm process still alive | `RunCommand: pkill php-fpm && sleep 2 && /etc/init.d/php-fpm-<ver> start` (high risk) |
| `ERROR: [/www/server/php/<ver>/etc/php-fpm.conf:N] unknown parameter` | Manual edit broke a directive | `Read` the line, fix or reset via panel App Store → PHP → Settings → Config → Reset (high risk) |
| `Unable to access php-fpm.sock: Permission denied` | Socket file owner wrong | `RunCommand: ls -la /tmp/php-cgi-<ver>.sock` → if not `www:www`, `RunCommand: chown www:www /tmp/php-cgi-<ver>.sock && chown -R www:www /www/server/php/<ver>/var/log/` (low risk) |

---

## Step 4 — Tool Risk Levels

Tools are gated by their registered `risk_level`, not by what the command does.

| risk_level | Tools | Typical use | Handling |
|---|---|---|---|
| **low** | `Read`, `GetSitesConf`, `GetSitesLogs`, `ServiceStatus`, `GetSystemResources`, `GetTopProcesses`, `MysqlTestConnection`, `MysqlQuery`, `MysqlListDatabases`, `MysqlDescribeTable`, `TodoRead`, `TodoWrite` | read configs/logs, check service state, test DB connection, list DBs/tables, track todos | Execute directly |
| **high** | `RunCommand`, `ServiceRestart`, `SearchReplace`, `Write`, `MysqlExecute` | any shell command (incl. read-only `curl`/`ls`/`netstat`/`ps` and `chown`/`chmod`), restart service, edit nginx/php config, write file, SQL write | Every call goes through the panel confirmation gate |
| **forbidden** | — | delete site, drop database, delete files, `rm -rf`, `DROP TABLE/DATABASE` | Never execute |

- `RunCommand` is `risk_level="high"` as a tool, so **even read-only probes** (`curl`, `ls`, `netstat`) trigger the confirmation gate. Prefer the low-risk read tools (`Read` for logs/configs, `ServiceStatus` for state) to gather facts without confirmation.
- After any config edit (`SearchReplace`/`Write`), **must** run `nginx -t` to validate before reload.

---

## Step 5 — Output Format

When reporting findings to the user, always use **plain natural language** in this shape:

```
Root cause: <one-sentence root cause>

Executed steps:
- <step 1>
- <step 2>
...

Recommendations:
- <prevention or follow-up action>
```

Rules:
- **Never** paste raw shell commands, btpython paths, or config diffs into the user-facing message.
- **Never** ask the user to type commands — if a fix is needed, describe it and let the user confirm.
- If the diagnosis is incomplete (e.g. could not reproduce, logs unclear), say so explicitly. Do NOT fabricate a cause.

---

## Quick Reference — Common Error Codes

These are auto-mapped by `mysql_engine.MYSQL_ERROR_MAP`; the mapping is shown for agent's own reasoning, **do not echo the codes to the user verbatim**.

| SQLSTATE / Code | Friendly Meaning | Next Step |
|---|---|---|
| `2002` / `2003` | Cannot connect to MySQL socket / port | Check `ServiceStatus("mysql")` |
| `1045` | Wrong password for DB user | Compare `wp-config.php` with panel's `databases` table |
| `1146` | Table does not exist | `MysqlListDatabases` + `MysqlDescribeTable` to confirm |
| `1040` | Too many connections | `MysqlQuery("SHOW GLOBAL STATUS LIKE 'Threads_connected'")` + `GetTopProcesses` |
| `1452` | Foreign key constraint fails | Inspect the referenced row, report to user |

---

## Quick Reference — File / Log Paths

| What | Path |
|---|---|
| Nginx vhost config | `/www/server/panel/vhost/nginx/<domain>.conf` |
| Apache vhost config | `/www/server/panel/vhost/apache/<domain>.conf` |
| Rewrite rules | `/www/server/panel/vhost/rewrite/<domain>.conf` |
| Nginx main config | `/www/server/nginx/conf/nginx.conf` |
| Nginx fastcgi config (whitespace-page culprit) | `/www/server/nginx/conf/fastcgi.conf` |
| Site access log | `/www/wwwlogs/<domain>.log` |
| Site error log | `/www/wwwlogs/<domain>.error.log` |
| PHP-FPM error log | `/www/server/php/<ver>/var/log/php-fpm.log` |
| PHP-FPM socket | `/tmp/php-cgi-<ver>.sock` |
| PHP-FPM pool config | `/www/server/php/<ver>/etc/php-fpm.conf` |
| WordPress DB config | `<site_root>/wp-config.php` |
