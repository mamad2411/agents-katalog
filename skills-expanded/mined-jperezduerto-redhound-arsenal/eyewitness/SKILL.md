---
name: eyewitness
description: >
  Operate and interpret EyeWitness — a web, RDP, and VNC screenshot tool for rapid visual triage of
  large attack surfaces. Use when conducting external or internal network assessments, processing nmap
  or Nessus output to quickly identify high-value web services, or building target triage workflows
  for large scope engagements. Covers installation (Docker, pip, source), input modes (file, nmap XML,
  Nessus XML), protocol support (HTTP/HTTPS, RDP, VNC), report generation, active scanning, and
  integration with recon pipelines.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/RedSiege/EyeWitness
  stars: '5.3k'
  language: Python
---

# eyewitness Agent Skill

## When to Use This Skill

Use this skill when:
- You have a list of URLs or IPs from recon and need rapid visual triage
- Processing nmap XML or Nessus .nessus output to screenshot all discovered web services
- Identifying login panels, admin interfaces, or custom web apps on a large target range
- Taking RDP or VNC screenshots of discovered remote-access services
- Generating an HTML report of all services for client deliverables or internal triage
- The user asks about web service enumeration or visual reconnaissance

## What EyeWitness Does

EyeWitness takes screenshots of web applications (HTTP/HTTPS), RDP services, and VNC servers, then
generates a categorized HTML report with headers, server banners, and page titles. It is the primary
tool for visual triage of large scopes — after running nmap against a /16 or pulling services from
a Nessus scan, EyeWitness lets an assessor visually scan hundreds of services in minutes rather than
manually browsing each one.

## Installation

### Method 1 — Docker (recommended, avoids dependency hell)

```bash
# Pull and run — mounts local directory for output
docker pull ghcr.io/redsiege/eyewitness:latest

# Create alias for convenience
alias eyewitness='docker run --rm -it \
  -v $(pwd):/tmp/EyeWitness \
  ghcr.io/redsiege/eyewitness:latest'

# Run against a URL file
eyewitness --web -f /tmp/EyeWitness/urls.txt -d /tmp/EyeWitness/output
```

### Method 2 — Python setup (Kali / Debian)

```bash
# Kali ships EyeWitness — just update
sudo apt update && sudo apt install eyewitness -y

# Or install from source
git clone https://github.com/RedSiege/EyeWitness.git
cd EyeWitness/Python
sudo ./setup/setup.sh   # Installs chromium, pip deps automatically
pip3 install -r requirements.txt
```

### Method 3 — pip only (if Chromium already present)

```bash
pip3 install eyewitness
# Requires Chromium or Chrome in PATH for web screenshots
```

### Verify Installation

```bash
python3 EyeWitness.py --help
# or if installed via apt:
eyewitness --help
```

## Core Concepts

### How EyeWitness Takes Screenshots

EyeWitness drives a headless Chromium instance via Selenium or directly via the Chrome DevTools
Protocol to render each web page and save a PNG screenshot. For RDP it uses `rdesktop` or `xfreerdp`,
and for VNC it uses `vncdotool`. Each target is processed with a configurable timeout, and failures
are captured in the report as error entries rather than silently dropped.

### Output Structure

```
output/
├── report.html        — Main HTML report with all screenshots, sorted by category
├── open_ports.csv     — CSV of all targets and response data
├── screens/           — Individual PNG screenshots
│   ├── http_10_0_0_1_80.png
│   └── https_app_example_com_443.png
├── source/            — Saved page source (HTML) for each target
└── headers/           — Raw HTTP response headers for each target
```

The HTML report auto-categorizes targets into groups: default credentials found, clusters of similar
pages, error pages, and unique-looking apps — making it easy to prioritize.

## CLI Reference

### Protocol Modes

```bash
# Web (HTTP/HTTPS) — most common mode
eyewitness --web -f urls.txt -d ./output

# RDP — screenshots Windows remote desktop services
eyewitness --rdp -f hosts.txt -d ./output

# VNC — screenshots VNC servers (no auth or known ports)
eyewitness --vnc -f hosts.txt -d ./output

# All protocols at once (slow but comprehensive)
eyewitness --web --rdp --vnc -f targets.txt -d ./output
```

### Input Sources

```bash
# From a flat file (one URL or host per line)
eyewitness --web -f urls.txt -d ./output

# From nmap XML output
eyewitness --web --nmap-xml nmap_scan.xml -d ./output

# From Nessus .nessus export
eyewitness --web --nessus-xml nessus_export.nessus -d ./output

# From a single URL (quick test)
eyewitness --web --single https://10.10.10.1 -d ./output

# urls.txt format — one entry per line, protocol required for web
cat urls.txt
# https://192.168.1.1
# http://192.168.1.100:8080
# https://app.example.com
```

### Output and Reporting

```bash
# Specify output directory (auto-created)
eyewitness --web -f urls.txt -d /tmp/ew_$(date +%Y%m%d)

# Set a custom report title
eyewitness --web -f urls.txt -d ./output --title "Engagement - Acme Corp"

# Skip report creation (screenshots only)
eyewitness --web -f urls.txt -d ./output --no-prompt

# Cycle through report without prompting
eyewitness --web -f urls.txt -d ./output --no-prompt
```

### Timing and Performance

```bash
# Set per-target timeout in seconds (default: 7)
eyewitness --web -f urls.txt -d ./output --timeout 15

# Set number of threads (default: 10)
eyewitness --web -f urls.txt -d ./output --threads 20

# Delay between requests (seconds) — reduces detection risk
eyewitness --web -f urls.txt -d ./output --delay 2

# Retry failed targets N times
eyewitness --web -f urls.txt -d ./output --max-retries 3
```

### HTTP Options

```bash
# Custom user agent
eyewitness --web -f urls.txt -d ./output \
  --user-agent "Mozilla/5.0 (compatible; Googlebot/2.1)"

# Proxy through Burp Suite
eyewitness --web -f urls.txt -d ./output \
  --proxy-ip 127.0.0.1 --proxy-port 8080

# Socks proxy
eyewitness --web -f urls.txt -d ./output \
  --proxy-ip 127.0.0.1 --proxy-port 1080 --proxy-type socks5

# Ignore SSL certificate errors (required for self-signed certs)
eyewitness --web -f urls.txt -d ./output --no-dns

# Set custom HTTP header (e.g., for authenticated internal apps)
eyewitness --web -f urls.txt -d ./output \
  --add-http-headers "Authorization: Bearer TOKEN"
```

### Resolution and Rendering

```bash
# Set browser viewport resolution (default 1920x1080)
eyewitness --web -f urls.txt -d ./output --resolution 1280x720

# Wait additional time after page load for JS rendering (seconds)
eyewitness --web -f urls.txt -d ./output --jitter 3

# Active scan — attempt default credential login on discovered login pages
eyewitness --web -f urls.txt -d ./output --active-scan
```

### Active Scanning

```bash
# Active scan attempts default credentials on recognized login portals
# (Cisco, F5, Juniper, Palo Alto, various web apps)
eyewitness --web -f urls.txt -d ./output --active-scan

# Active scan with custom credential file
eyewitness --web -f urls.txt -d ./output --active-scan \
  --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
```

## Common Workflows

### Workflow 1 — nmap to EyeWitness Pipeline

```bash
# Step 1 — Full port scan with service detection, save XML
nmap -sV -p 80,443,8000,8080,8443,8888,9000,9090,9443 \
  --open -oX nmap_web.xml 192.168.1.0/24

# Step 2 — Feed nmap XML directly to EyeWitness
eyewitness --web --nmap-xml nmap_web.xml -d ./ew_output --timeout 10 --threads 20

# Step 3 — Open HTML report
firefox ./ew_output/report.html
```

### Workflow 2 — Nessus Integration

```bash
# Export scan from Nessus as .nessus format
# Then process with EyeWitness
eyewitness --web --nessus-xml acme_scan.nessus -d ./ew_nessus_output

# Also grab RDP services found by Nessus
eyewitness --rdp --nessus-xml acme_scan.nessus -d ./ew_rdp_output
```

### Workflow 3 — Large External Scope Triage

```bash
# Step 1 — Generate URL list from subdomain recon
cat subdomains.txt | httpx -ports 80,443,8080,8443 -o live_urls.txt

# Step 2 — Screenshot all live URLs
eyewitness --web -f live_urls.txt -d ./external_ew \
  --timeout 15 --threads 25 --no-prompt

# Step 3 — Review report, note interesting targets
# Focus on: login pages, custom apps, admin panels, default creds found
```

### Workflow 4 — Internal Network RDP + Web

```bash
# After pivoting into internal network via Ligolo-ng / chisel
eyewitness --web --rdp -f internal_hosts.txt -d ./internal_ew \
  --timeout 20 --threads 10 --delay 1

# RDP targets file format (host:port)
cat internal_hosts.txt
# 10.10.10.5:3389
# 10.10.10.6:3389
# 10.10.10.10:80
# https://10.10.10.20:8443
```

## Advanced Techniques

### Combining with httpx for Pre-filtering

```bash
# Use httpx to filter live hosts first, then EyeWitness for screenshots
# This avoids EyeWitness wasting time on dead hosts
cat all_targets.txt | httpx -silent -o live.txt
eyewitness --web -f live.txt -d ./output --timeout 8
```

### Splitting Large URL Lists

```bash
# Split 5000-URL list into chunks of 500 for parallel runs
split -l 500 urls.txt chunk_
for chunk in chunk_*; do
  eyewitness --web -f "$chunk" -d "./output_${chunk}" \
    --no-prompt --timeout 10 --threads 15 &
done
wait
```

### Post-processing Report Data

```bash
# Extract all unique page titles from report for quick review
grep -oP '(?<=<title>).*?(?=</title>)' ./output/source/*.html | sort -u

# Find targets returning 200 OK vs others
grep "200 OK" ./output/open_ports.csv | cut -d',' -f1
```

### Screenshot via Proxy for WAF Bypass Testing

```bash
# Route EyeWitness through Burp to capture all requests
eyewitness --web -f urls.txt -d ./burp_routed \
  --proxy-ip 127.0.0.1 --proxy-port 8080 \
  --no-prompt --timeout 20
```

## Integration with Other Tools

### With Amass / subfinder

```bash
amass enum -passive -d example.com -o subs.txt
cat subs.txt | httpx -o live_subs.txt
eyewitness --web -f live_subs.txt -d ./subdomain_screenshots
```

### With Nmap Service Scripts

```bash
nmap -p 80,443 --script http-title,http-headers -oX nmap_http.xml 10.0.0.0/24
eyewitness --web --nmap-xml nmap_http.xml -d ./output
```

### With Metasploit

After EyeWitness identifies interesting login panels, pivot to Metasploit auxiliary scanners:
```
use auxiliary/scanner/http/tomcat_mgr_login
use auxiliary/scanner/http/jboss_vulnscan
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `Chromium not found` | Chromium not installed | `apt install chromium-browser` or `setup.sh` |
| All screenshots blank | Headless rendering issue | `--resolution 1280x720`, check Xvfb |
| SSL errors | Self-signed certs rejected | Chromium ignores SSL by default; check proxy settings |
| Slow performance | Too many threads, slow hosts | Reduce `--threads`, increase `--timeout` |
| Docker volume issues | Wrong mount path | Use absolute path in `-v $(pwd):/tmp/EyeWitness` |
| nmap XML not parsed | nmap run without `-oX` | Re-run nmap with `-oX output.xml` flag |
| RDP screenshots grey | Target requires NLA | EyeWitness cannot bypass NLA; note target for manual testing |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
