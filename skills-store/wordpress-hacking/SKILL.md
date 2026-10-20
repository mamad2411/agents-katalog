---
name: wordpress-hacking
description: |
  Activate this skill whenever the user mentions WordPress, WP, WooCommerce, WP plugin,
  WP theme, wp-admin, wp-content, wp-login, wp-json, wp-includes, xmlrpc, XML-RPC,
  wp-cron, admin-ajax, wp-config, wpscan, WordPress vulnerability, WordPress exploit,
  WordPress enumeration, WordPress brute force, WordPress RCE, WordPress shell upload,
  WordPress backdoor, WordPress privilege escalation, WordPress authentication bypass,
  WordPress REST API, WordPress nonce, WordPress application password,
  plugin vulnerability, theme vulnerability, WooCommerce exploit, WooCommerce injection,
  Wordfence, Sucuri, iThemes Security, All-in-One WP Security, WP security plugin,
  WordPress multisite, WordPress network, WordPress mu-plugins, must-use plugins,
  WordPress file upload, WordPress SQLi, WordPress XSS, WordPress SSRF, WordPress LFI,
  WordPress deserialization, WordPress object injection, WordPress CSRF,
  Elementor, WPBakery, Contact Form 7, Yoast, ACF, Advanced Custom Fields,
  Gravity Forms, WP File Manager, RevSlider, LayerSlider, ThemeGrill,
  WordPress user enumeration, WordPress version detection, WordPress fingerprinting,
  /wp-login.php, /wp-admin/, /wp-content/uploads/, /wp-includes/, /xmlrpc.php,
  readme.html, license.txt, wp-signup.php, wp-activate.php, wp-trackback.php,
  WordPress database, wp_users, wp_options, wp_usermeta, WordPress hash cracking,
  phpass, WordPress password hash, $P$ hash,
  WordPress penetration testing, WordPress security assessment, WordPress audit,
  WordPress attack surface, WordPress hacking methodology.
version: 2.0.0
---

# WordPress Hacking

WordPress powers over 40% of the web. Its attack surface is massive: core engine, 60,000+ public plugins, 10,000+ themes, REST API, XML-RPC, admin-ajax, custom PHP endpoints, WooCommerce storefronts, and multisite networks. A single outdated plugin can give you a shell. Master the enumeration-to-exploitation pipeline and you will pop WordPress sites systematically.

## Triage Workflow

Follow this sequence for every WordPress target. Each step feeds the next.

### Step 1 -- Confirm WordPress and Detect Version

Before running any scanner, confirm the target is WordPress and fingerprint the exact version. This determines which CVEs apply.

```bash
# Quick confirmation — check meta generator, login page, and common paths
curl -sI https://TARGET/ | grep -i 'x-powered-by\|x-redirect-by\|link.*wp-json'
curl -s https://TARGET/ | grep -oP 'content="WordPress \K[0-9.]+'
curl -s https://TARGET/readme.html | head -20
curl -s https://TARGET/feed/ | grep '<generator>'
curl -s https://TARGET/wp-includes/js/wp-emoji-release.min.js | head -1
```

Multiple version detection methods exist because admins disable some but rarely all. See `references/wp-enum.md` for the full fingerprinting matrix.

Record findings immediately:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add \
  "https://TARGET" info-leak "wp-version" INFO \
  "WordPress X.Y.Z detected via meta generator"

node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add \
  "TARGET" tech-stack "cms" "wordpress-X.Y.Z" --source "version-detection"
```

### Step 2 -- Security Plugin Detection

Before aggressive scanning, identify security plugins that will block or log you. This dictates your OPSEC profile.

```bash
# Check for common security plugin signatures
curl -s https://TARGET/ | grep -iE 'wordfence|sucuri|ithemes-security|better-wp-security|all-in-one-wp-security|shield-security|bulletproof'
curl -sI https://TARGET/wp-login.php | grep -i 'x-sucuri\|x-waf'
curl -s https://TARGET/wp-content/plugins/ 2>/dev/null | grep -oP 'href="[^"]*"' | grep -iE 'wordfence|sucuri|ithemes|bulletproof|shield|cerber'
```

| Security Plugin | Detection Signature | Impact on Testing |
|----------------|---------------------|-------------------|
| Wordfence | `wordfence` in source, `/wp-content/plugins/wordfence/` | Rate limiting, IP blocking, live traffic view, login lockout |
| Sucuri | `X-Sucuri-ID` header, Sucuri WAF CloudProxy | CDN/WAF layer, request filtering, GeoIP blocking |
| iThemes Security | `better-wp-security` plugin dir | Brute force protection, 404 lockout, file change detection |
| WP Cerber | `wp-cerber` plugin dir | Aggressive rate limiting, custom login URL, IP subnet blocking |
| Shield Security | `wp-simple-firewall` plugin dir | Bot detection, comment/form SPAM, 2FA enforcement |

Log detected defenses:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/target-intel.js add \
  "TARGET" defense "security-plugin" "wordfence-active" --source "fingerprinting"
```

### Step 3 -- User Enumeration

Enumerate WordPress users to build a target list for brute force and social engineering. Multiple methods exist because admins block some but not all.

```bash
# WPScan user enumeration
wpscan --url https://TARGET --enumerate u --disable-tls-checks

# Manual methods (when wpscan is blocked)
# Author archives — IDs 1-50
for i in $(seq 1 50); do curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" "https://TARGET/?author=$i"; done

# REST API
curl -s https://TARGET/wp-json/wp/v2/users | jq '.[].slug'
curl -s 'https://TARGET/?rest_route=/wp/v2/users' | jq '.[].slug'

# oEmbed
curl -s "https://TARGET/wp-json/oembed/1.0/embed?url=https://TARGET/" | jq '.author_name'

# Login error oracle
curl -s -d 'log=admin&pwd=wrong&wp-submit=Log+In' https://TARGET/wp-login.php | grep -oP 'Error.*?<'
```

See `references/wp-enum.md` for all enumeration vectors.

### Step 4 -- Plugin and Theme Enumeration

Plugins are the primary attack surface. Enumerate aggressively.

```bash
# WPScan — aggressive plugin detection (tests ~100k slugs)
wpscan --url https://TARGET --enumerate ap --plugins-detection aggressive --disable-tls-checks

# WPScan — vulnerable plugins only (faster)
wpscan --url https://TARGET --enumerate vp --disable-tls-checks

# Theme enumeration
wpscan --url https://TARGET --enumerate at --disable-tls-checks

# Combined comprehensive scan with API token for vulnerability data
wpscan --url https://TARGET --enumerate ap,at,u,cb,dbe \
  --plugins-detection aggressive --api-token YOUR_TOKEN --disable-tls-checks
```

For passive enumeration without wpscan, analyze page source for `/wp-content/plugins/` and `/wp-content/themes/` references. See `references/wp-enum.md`.

### Step 5 -- Vulnerability Mapping

Cross-reference enumerated components against vulnerability databases.

```bash
# WPScan with API token gives CVE data inline
wpscan --url https://TARGET --enumerate vp,vt --api-token YOUR_TOKEN --disable-tls-checks

# Nuclei WordPress templates
nuclei -u https://TARGET -tags wordpress,wp-plugin,wp-theme -severity critical,high
nuclei -u https://TARGET -tags wordpress -severity medium

# Search for specific plugin CVEs
searchsploit wordpress plugin-name
searchsploit wordpress theme-name
```

Log every vulnerability:

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/findings-tracker.js add \
  "https://TARGET/wp-content/plugins/PLUGIN/" rce "PLUGIN-version" CRITICAL \
  "CVE-XXXX-XXXXX: PLUGIN vX.Y.Z RCE via ..."

node ${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js add \
  wpscan "TARGET" "plugin-enumeration" success \
  --notes "Found X plugins, Y vulnerable"
```

### Step 6 -- Exploitation

Exploit discovered vulnerabilities. See `references/wp-exploits.md` for vulnerability class patterns, `references/wp-authentication.md` for auth attacks, and `references/wp-plugin-attacks.md` for plugin-specific exploitation.

### Step 7 -- Post-Exploitation

Once you have access (any level), escalate and persist. See `references/wp-post-exploitation.md` for backdoor techniques, database manipulation, and lateral movement.

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/techniques-tracker.js add \
  manual "TARGET" "wp-post-exploitation" success \
  --notes "Shell uploaded via theme editor, wp-config.php extracted"
```

## Decision Tree

Route your approach based on the target's configuration:

```
WordPress detected
├── REST API enabled (/wp-json/ returns routes)?
│   ├── YES → User enum via /wp-json/wp/v2/users
│   │         Plugin routes via /wp-json/ (custom endpoints)
│   │         WooCommerce API if /wp-json/wc/v3/ exists
│   └── NO  → Author archive enum (/?author=N)
│             Feed-based version detection (/feed/)
│
├── XML-RPC enabled (/xmlrpc.php)?
│   ├── YES → system.multicall brute force
│   │         pingback.ping SSRF
│   │         See references/wp-authentication.md
│   └── NO  → wp-login.php brute force (rate-limited)
│
├── Multisite (wp-signup.php exists)?
│   ├── YES → Enumerate subsites via /wp-sitemap.xml
│   │         Test wp-signup.php for open registration
│   │         Cross-site privilege escalation
│   └── NO  → Standard single-site methodology
│
├── WooCommerce detected?
│   ├── YES → Payment endpoint testing
│   │         Store API enumeration
│   │         Customer data exposure via REST
│   │         See references/wp-plugin-attacks.md
│   └── NO  → Standard plugin attack surface
│
├── Security plugin detected?
│   ├── Wordfence → Reduce request rate, rotate IPs
│   ├── Sucuri WAF → Test WAF bypass rules
│   ├── Cerber → Custom login URL discovery
│   └── None → Aggressive scanning safe
│
└── wp-cron.php accessible?
    ├── YES → Timing oracle for plugins
    │         DoS via cron trigger flooding
    └── NO  → DISABLE_WP_CRON likely set (good opsec by admin)
```

## OPSEC Considerations

### Request Rate Management

| Security Plugin | Safe Rate | Lockout Threshold |
|----------------|-----------|-------------------|
| None | Unlimited | N/A |
| Wordfence Free | 5-10 req/s | 20 login failures / 5 min |
| Wordfence Premium | 2-5 req/s | Configurable, real-time IP blocking |
| Sucuri WAF | 3-5 req/s | Varies by plan |
| WP Cerber | 1-3 req/s | Aggressive, subnet-level blocking |

### Login Brute Force OPSEC

- Prefer XML-RPC `system.multicall` over wp-login.php (fewer requests, harder to rate-limit)
- Batch 500-1000 passwords per multicall request
- Space multicall requests 2-5 seconds apart
- Use wp-login.php only as fallback when xmlrpc.php is disabled
- Watch for lockout indicators: HTTP 403, "Too many failed attempts", `Retry-After` header

### WPScan OPSEC Flags

```bash
# Stealth scan — minimal requests
wpscan --url https://TARGET --enumerate p --plugins-detection passive \
  --request-timeout 30 --throttle 2000 --random-user-agent --disable-tls-checks

# Paranoid — Tor routing
wpscan --url https://TARGET --enumerate p --plugins-detection passive \
  --proxy socks5://127.0.0.1:9050 --random-user-agent --disable-tls-checks
```

### wp-cron Timing

`wp-cron.php` runs on page load by default. During stealth scans, avoid triggering it by not hitting the front page repeatedly. If `DISABLE_WP_CRON` is set (visible via timing behavior), the admin uses a real cron job — this means less noise from your requests.

## Hexstrike MCP Tool Integration

Load tools via `ToolSearch`:

| Tool | Load Command | WordPress Use |
|------|-------------|---------------|
| WPScan | `select:mcp__hexstrike-ai__wpscan_analyze` | Primary WP scanner — version, plugins, themes, users, vulns |
| Nuclei | `select:mcp__hexstrike-ai__nuclei_scan` | WordPress-tagged templates, CVE validation |
| Katana | `select:mcp__hexstrike-ai__katana_crawl` | Custom endpoint discovery in themes/plugins |
| Feroxbuster | `select:mcp__hexstrike-ai__feroxbuster_scan` | Directory/file brute force in wp-content |
| HTTP Repeater | `select:mcp__hexstrike-ai__http_repeater` | Manual XML-RPC, REST API, exploit requests |
| HTTP Intruder | `select:mcp__hexstrike-ai__http_intruder` | admin-ajax action fuzzing, parameter brute force |
| Hydra | `select:mcp__hexstrike-ai__hydra_attack` | wp-login.php brute force |
| SQLMap | `select:mcp__hexstrike-ai__sqlmap_scan` | SQL injection in plugin parameters |

## WordPress File Structure

```
/                           # Web root
├── wp-admin/               # Admin dashboard (requires auth)
│   ├── admin-ajax.php      # AJAX handler — key attack surface
│   ├── includes/           # Admin includes
│   ├── theme-editor.php    # Theme file editor (post-auth RCE)
│   └── plugin-editor.php   # Plugin file editor (post-auth RCE)
├── wp-content/             # User content — primary attack surface
│   ├── plugins/            # All plugins (active and inactive)
│   ├── themes/             # All themes
│   ├── uploads/            # Media uploads (year/month dirs)
│   │   └── YYYY/MM/        # Upload directories
│   ├── mu-plugins/         # Must-use plugins (auto-loaded, no activation needed)
│   ├── upgrade/            # Temp upgrade directory
│   └── cache/              # Cache directory (if caching plugin)
├── wp-includes/            # Core WordPress engine
│   ├── version.php         # Core version number
│   ├── class-wp-*.php      # Core classes
│   └── js/                 # Core JavaScript
├── wp-config.php           # Database creds, auth keys, debug settings
├── wp-login.php            # Login form
├── wp-cron.php             # Pseudo-cron system
├── xmlrpc.php              # XML-RPC API
├── wp-json/                # REST API (virtual directory)
├── wp-signup.php           # Multisite registration
├── readme.html             # Version disclosure
├── license.txt             # License file
├── wp-trackback.php        # Trackback endpoint
└── .htaccess / web.config  # Rewrite rules, directory protection
```

## References

| Reference | Coverage |
|-----------|----------|
| `references/wp-enum.md` | Version fingerprinting matrix, user enumeration (7 methods), plugin/theme enumeration (passive + active), configuration file discovery, WooCommerce enumeration |
| `references/wp-exploits.md` | Vulnerability classes by component, CVE exploitation patterns, admin-ajax attacks, REST API exploitation, file upload bypass, SQL injection patterns |
| `references/wp-authentication.md` | XML-RPC brute force, wp-login attacks, application passwords, REST API authentication, cookie structure, nonce exploitation, 2FA bypass |
| `references/wp-plugin-attacks.md` | Top vulnerable plugins with CVEs, file upload exploitation, LFI/RFI through plugins, SQLi in plugin parameters, deserialization/object injection, WooCommerce attacks |
| `references/wp-post-exploitation.md` | Backdoor insertion (theme editor, mu-plugins, wp-config), database manipulation, user creation, persistent access, wp-config.php secrets extraction, lateral movement |
