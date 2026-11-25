---
name: authorized-server-root-discovery
description: >
  Use when user grants access to cPanel/SSH/hosting file manager/authenticated
  server env and asks to find site root, WordPress install, or deploy/edit files
  directly. Auto-discovers doc root, domain, WP install, then edits/deploys.
  Never bypasses auth, never guesses credentials.
license: MIT + Commons Clause
metadata:
  version: 1.0.0
  category: engineering
  domain: server-administration
  updated: 2026-09-13
  tags: [server, cpanel, ssh, wordpress, deployment, sysadmin]
---
# Authorized Server Root Discovery & Direct Deployment

## Purpose

Operate as an authorized server/web administrator.

The user may provide access to a cPanel server, SSH session, hosting file manager, or an authenticated server environment. Your job is to automatically identify the correct website account, document root, WordPress installation, and relevant files, then perform the requested operation directly.

**Important:** Never bypass authentication, guess passwords, brute-force credentials, exploit authentication weaknesses, or access accounts/sites that are not already authorized.

---

## Operating Rules

1. Work ONLY inside the server/account/environment currently authorized by the user.
2. Do not attempt password guessing or credential brute forcing.
3. Do not bypass cPanel, SSH, FTP, WordPress, or hosting authentication.
4. Do not modify unrelated domains, accounts, databases, or directories.
5. Before making destructive changes, create a backup when practical.
6. Prefer the minimum required change.
7. Preserve existing website functionality.
8. Do not expose passwords, API keys, tokens, cookies, or private credentials in logs or responses.
9. If multiple domains/accounts are discovered, identify the correct one from the user's requested domain rather than choosing randomly.
10. If the requested target cannot be confidently identified, stop before modifying files.

---

# Phase 1 — Discover Authorized Environment

First determine what access is currently available.

Check for:

* SSH
* cPanel shell
* hosting file manager
* WordPress filesystem
* WP-CLI
* PHP
* MySQL/MariaDB
* web-server configuration
* home directory
* public_html
* addon-domain directories
* subdomain directories

Do NOT attempt authentication bypass.

---

# Phase 2 — Discover Hosting Root

Automatically inspect the authorized filesystem.

Typical locations may include:

```text
/home/USERNAME/
/home/USERNAME/public_html/
/home/USERNAME/domains/
/var/www/
/var/www/html/
```

But NEVER assume these paths.

Discover them from the actual environment.

Useful discovery methods:

```bash
pwd
whoami
id
echo "$HOME"
find "$HOME" -maxdepth 3 -type f -name wp-config.php 2>/dev/null
find "$HOME" -maxdepth 4 -type d -name public_html 2>/dev/null
```

If WP-CLI is available:

```bash
wp --info
wp core is-installed
wp option get home
wp option get siteurl
```

---

# Phase 3 — Identify Correct Website

When the user provides a domain such as:

```text
example.com
```

find the corresponding website root.

Check:

* cPanel domain configuration
* addon-domain configuration
* Apache/Nginx virtual-host configuration when accessible
* WordPress `home` and `siteurl`
* `wp-config.php`
* directory names
* document roots

Confirm that the discovered directory actually belongs to the requested domain.

Example verification:

```bash
grep -E "DB_NAME|DB_USER|DB_HOST" wp-config.php
```

Never display credential values.

---

# Phase 4 — WordPress Detection

Once a candidate root is found, verify:

```text
wp-admin/
wp-content/
wp-includes/
wp-config.php
index.php
```

If WordPress is detected, determine:

* active theme
* plugins
* WordPress version
* PHP version
* site URL
* home URL
* upload directory
* relevant theme/plugin files

Use WP-CLI where available.

Example:

```bash
wp core version
wp theme list
wp plugin list
wp option get home
wp option get siteurl
```

---

# Phase 5 — Find Relevant Files

Before editing, search the discovered website root for the requested functionality.

Examples:

```bash
find . -type f
grep -R "target text" . --exclude-dir=node_modules --exclude-dir=.git
```

For WordPress themes:

```text
wp-content/themes/
```

For plugins:

```text
wp-content/plugins/
```

Determine which file actually controls the requested behavior before changing anything.

---

# Phase 6 — Backup Before Modification

For important modifications:

```bash
cp FILE FILE.backup-TIMESTAMP
```

For larger changes, create an appropriate archive outside the active deployment path.

Never overwrite an unrelated backup directory.

If the user explicitly specifies a directory that must not be touched, treat it as immutable.

---

# Phase 7 — Make the Change Directly

After identifying the correct target:

1. Edit the required file(s).
2. Preserve existing functionality.
3. Do not rewrite unrelated code.
4. Do not change design/content unless requested.
5. Maintain existing permissions.
6. Validate syntax.

For PHP:

```bash
php -l FILE.php
```

For WordPress:

```bash
wp core is-installed
wp theme list
wp plugin list
```

---

# Phase 8 — Verify

After modification:

* verify file exists
* verify permissions
* verify syntax
* verify WordPress loads
* verify requested functionality
* check for PHP errors
* check relevant logs when accessible

If browser automation is available, use it to visually verify the website.

For responsive work, test:

```text
Desktop
Tablet
Mobile
```

Do not modify desktop behavior when the request is specifically responsive-only.

---

# Phase 9 — Direct Deployment

If the user asks to deploy/overwrite:

1. Confirm the target root.
2. Confirm the domain.
3. Backup the existing target when appropriate.
4. Copy/overwrite only the required files.
5. Verify ownership and permissions.
6. Test the website.
7. Report exactly what was changed.

Never deploy into an uncertain directory.

---

# Safety Boundary

The following are NOT allowed:

```text
Password guessing
Root password guessing
cPanel password brute force
SSH brute force
Credential stuffing
Authentication bypass
Session hijacking
Unauthorized privilege escalation
Accessing another customer's hosting account
Circumventing hosting-provider security
```

If authentication is missing, report:

> Authentication is required. I can continue once an authorized SSH/cPanel/server session or valid credentials are provided.

Do not attempt to discover or guess credentials.

---

# Response Style

Operate directly and efficiently.

Before modification, briefly report:

```text
Target domain:
Detected account:
Detected document root:
WordPress:
Target files:
Backup:
```

After completion:

```text
Completed:
- ...
- ...
- ...

Verified:
- ...
```

Do not provide unnecessary narration while executing.

The primary objective is:

**Discover → Verify → Backup → Modify → Validate → Deploy → Test**

Always prioritize correct target identification over speed.
