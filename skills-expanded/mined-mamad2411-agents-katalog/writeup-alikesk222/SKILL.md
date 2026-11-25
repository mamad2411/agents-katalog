<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-alikesk222
description: CTF writeups and security challenges by alikesk222.
---

# Writeups by alikesk222

Source repository: `/repos/alikesk222`

## Repository Index

- recon-toolkit/README.md

## Writeup Content


### File: recon-toolkit/README.md

# recon-toolkit

> Passive reconnaissance toolkit for bug bounty hunters and pentesters.

Fast, async CLI tool that combines **subdomain enumeration**, **port scanning**, and **Shodan intelligence** into a single workflow — with clean terminal output and a self-contained HTML report.

---

## Features

- **Subdomain Enumeration** — Certificate transparency (crt.sh) + async DNS brute-force
- **Port Scanner** — Async TCP scanner with service detection (common / top1000 / custom ranges)
- **Shodan Integration** — IP intelligence, open services, and CVE lookup via Shodan API
- **HTML Report** — Dark-themed, self-contained report generated after full scans
- **Rich Terminal UI** — Progress bars, tables, and colored output via Rich

---

## Install

```bash
# Clone the repo
git clone https://github.com/yourusername/recon-toolkit.git
cd recon-toolkit

# Install (Python 3.11+)
pip install -e .
```

Or install directly:

```bash
pip install git+https://github.com/yourusername/recon-toolkit.git
```

---

## Usage

### Subdomain Enumeration

```bash
# Basic scan (crt.sh + default wordlist)
recon subdomains example.com

# Custom wordlist + more threads
recon subdomains example.com -w /path/to/wordlist.txt -t 100

# Save results to file
recon subdomains example.com -o subdomains.txt

# Skip crt.sh (faster, brute-force only)
recon subdomains example.com --no-crt
```

### Port Scan

```bash
# Common ports (default)
recon portscan example.com

# Top 1000 ports
recon portscan example.com -p top1000

# Custom port range
recon portscan example.com -p 1-10000

# Specific ports
recon portscan example.com -p 80,443,8080,8443

# All ports (slow)
recon portscan example.com -p all
```

### Shodan Lookup

```bash
# Using flag
recon shodan 8.8.8.8 -k YOUR_SHODAN_API_KEY

# Using environment variable (recommended)
export SHODAN_API_KEY=your_key_here
recon shodan example.com
```

### Full Recon (Recommended)

Runs all modules and generates an HTML report:

```bash
recon full example.com -o report.html

# With Shodan
recon full example.com -k YOUR_SHODAN_KEY -o report.html

# Custom wordlist + more threads
recon full example.com -w wordlist.txt -t 100 -p top1000 -o report.html
```

---

## Example Output

```
>> Certificate Transparency (crt.sh)
   Found 42 subdomains via crt.sh

>> DNS Brute-Force (180 words, 50 threads)
   Scanning... ████████████████████ 180/180 [0:00:08]
   Found 7 subdomains via brute-force

╭─────────────────────────────────────────╮
│  Subdomains found for example.com       │
├────┬────────────────────────────────────┤
│  # │ Subdomain                          │
├────┼────────────────────────────────────┤
│  1 │ api.example.com                    │
│  2 │ blog.example.com                   │
│  3 │ dev.example.com                    │
│  4 │ mail.example.com                   │
│ .. │ ...                                │
╰────┴────────────────────────────────────╯
Total: 49 subdomains found
```

---

## Shodan API Key

Get a free API key at [shodan.io](https://shodan.io). Free tier supports basic host lookups.

Set it as an environment variable to avoid passing it every time:

```bash
export SHODAN_API_KEY=your_key_here   # Linux/macOS
set SHODAN_API_KEY=your_key_here      # Windows CMD
$env:SHODAN_API_KEY="your_key_here"   # PowerShell
```

---

## Requirements

- Python 3.11+
- See [requirements.txt](requirements.txt)

---

## Legal Notice

This tool is intended for **authorized security testing only**. Only use it against targets you own or have explicit written permission to test. Unauthorized scanning may be illegal in your jurisdiction.

---

## License

[MIT](LICENSE)

