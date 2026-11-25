---
name: root-path-discovery-security-audit
description: >
  Use on an already-authorized server/SSH/cPanel/local env to auto-discover
  the filesystem/document root and audit for path/permission/privilege
  misconfigurations. Security assessment only, not authentication bypass.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  category: engineering
  domain: security-audit
  updated: 2026-09-13
  tags: [security, audit, server, permissions, wordpress, hardening]
---
# Root Path Discovery & Security Audit

## Objective

Given an already authorized server, SSH shell, cPanel shell, or local server environment, automatically discover the likely filesystem/document root and identify whether the server exposes dangerous path or privilege misconfigurations.

The goal is security assessment, not authentication bypass.

---

## Workflow

### 1. Environment Discovery

Inspect the current authorized environment:

```bash
pwd
whoami
id
echo "$HOME"
uname -a
```

Determine:

* current user
* current privilege level
* home directory
* operating system
* available shell
* available web-server software

---

### 2. Root / Document-Root Discovery

Search common locations for web roots.

Potential locations include:

```text
/home/*/public_html
/home/*/www
/home/*/htdocs
/var/www
/var/www/html
/srv/www
/opt/*
```

Do NOT assume one location.

Use filesystem discovery to identify directories containing indicators such as:

```text
index.php
index.html
wp-config.php
wp-admin/
wp-content/
wp-includes/
.htaccess
```

Example:

```bash
find /home /var/www /srv -type f \
  \( -name "wp-config.php" -o -name "index.php" -o -name "index.html" \) \
  2>/dev/null
```

---

### 3. Determine Likely Website Root

Rank discovered paths using evidence.

Higher confidence:

1. Web-server configuration points to the directory.
2. Domain configuration points to the directory.
3. WordPress `siteurl`/`home` matches the target domain.
4. Directory contains the active application.
5. File ownership matches the website account.

Never modify a path until confidence is high.

---

### 4. Security Checks

Once the root is identified, check for common security problems:

#### Dangerous permissions

```bash
find TARGET -type f -perm -0002 -ls 2>/dev/null
find TARGET -type d -perm -0002 -ls 2>/dev/null
```

Look for:

* world-writable files
* world-writable directories
* unexpected executable permissions
* incorrect ownership

#### Sensitive files

Check for exposed:

```text
.env
.git/
.git/config
backup files
database dumps
*.sql
*.zip
*.tar.gz
*.bak
config backups
debug logs
```

Do NOT print secrets found inside them.

---

### 5. Web Configuration Audit

Check accessible configuration for:

* directory listing
* exposed backup files
* exposed `.git`
* debug mode
* insecure file permissions
* publicly accessible configuration files
* incorrect document root
* unexpected symbolic links

Report findings without exploiting them.

---

### 6. Privilege Assessment

Determine whether the current authorized user has excessive privileges.

Check:

```bash
id
groups
sudo -l
```

Only inspect privileges available to the currently authorized account.

Do NOT attempt privilege escalation.

---

### 7. WordPress Detection

If WordPress is found:

```bash
wp core version
wp theme list
wp plugin list
```

Check for:

* outdated components
* writable plugin/theme directories
* suspicious PHP files
* exposed configuration
* insecure permissions

Do not automatically exploit vulnerabilities.

---

## Output

Return a concise security report:

```text
=== ROOT DISCOVERY ===

Current User:
Privilege Level:
Home Directory:
Likely Document Root:
Confidence:

=== SECURITY FINDINGS ===

[CRITICAL]
...

[HIGH]
...

[MEDIUM]
...

[LOW]
...

=== RECOMMENDATIONS ===

1. ...
2. ...
3. ...
```

For every finding provide:

```text
Finding
Evidence
Risk
Recommended Fix
```

---

## Important Boundary

This skill may:

* discover filesystem paths
* identify likely document roots
* inspect permissions
* inspect authorized configuration
* detect exposed files
* audit privilege configuration
* report security weaknesses

This skill must NOT:

* guess passwords
* brute-force credentials
* bypass authentication
* steal credentials
* hijack sessions
* exploit another person's server
* escalate privileges
* access accounts outside the authorized environment

The objective is:

**Discover → Assess → Report → Recommend Fix**

not:

**Guess credentials → Bypass security → Gain unauthorized access**

## Purpose
Discover the filesystem/document root on an authorized server and audit path/permission misconfigurations.

## When to use
Only on authorized servers (SSH/cPanel/local) the user owns or may test.

## Inputs
Authorized access and scope.

## Edge cases and failure handling
- No authorization -> stop.
- Sensitive files found -> report paths, never print secrets.

## Validation
- Findings list path, issue, severity, fix.
