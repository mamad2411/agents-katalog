---
name: spiderfoot
description: >
  Build, extend, and operate SpiderFoot — an OSINT automation platform with 200+ modules
  for passive and active reconnaissance. Use when the user needs automated intelligence
  gathering on IP addresses, domains, email addresses, phone numbers, usernames, subnets,
  or ASNs. Covers installation, web UI and CLI operation, scan types, module configuration,
  API key setup, correlation engine, data visualization, export formats, and OSINT
  investigation methodology for penetration testing and threat intelligence engagements.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/smicallef/spiderfoot
  stars: '13.8k'
---

# spiderfoot Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs passive or active OSINT on a target entity (domain, IP, email, person)
- Conducting pre-engagement reconnaissance on corporate infrastructure
- Building a comprehensive intelligence picture from open sources
- Correlating data across breach databases, DNS records, WHOIS, social media, and threat feeds
- The user needs to export OSINT findings into reports (HTML, CSV, JSON)

## What SpiderFoot Does

SpiderFoot is an open-source OSINT automation framework with 200+ modules that query APIs, DNS, WHOIS, web services, social platforms, threat intelligence feeds, and breach databases. It accepts multiple target types, correlates findings across modules, and presents results in a searchable web UI or CSV/JSON exports. The hosted version is SpiderFoot HX. The project has ~13.8k GitHub stars.

## Installation

### pip (Python 3.7+)
```bash
pip3 install spiderfoot
spiderfoot -l 127.0.0.1:5001
# Or run CLI: spiderfoot -s TARGET -t DOMAIN -m all
```

### From Source (recommended for latest modules)
```bash
git clone https://github.com/smicallef/spiderfoot.git /opt/spiderfoot
cd /opt/spiderfoot
pip3 install -r requirements.txt
python3 ./sf.py -l 127.0.0.1:5001
```

### Kali Linux
```bash
sudo apt update && sudo apt install -y spiderfoot
spiderfoot -l 127.0.0.1:5001
```

### Docker
```bash
docker pull smicallef/spiderfoot
docker run -p 5001:5001 smicallef/spiderfoot -l 0.0.0.0:5001
# Persist data
docker run -p 5001:5001 \
  -v /opt/sf-data:/home/spiderfoot/.spiderfoot \
  smicallef/spiderfoot -l 0.0.0.0:5001
```

### Dependency Verification
```bash
python3 -c "import spiderfoot; print('OK')"
# Or check CLI
python3 /opt/spiderfoot/sf.py --help
```

## Core Concepts

### Target Types
| Type | Example | Notes |
|------|---------|-------|
| DOMAIN | `example.com` | Passive + active DNS, subdomains |
| IP_ADDRESS | `93.184.216.34` | Geolocation, PTR, threat intel |
| EMAILADDR | `user@example.com` | Breach databases, social |
| PHONE | `+14155552671` | Carrier lookup, social profiles |
| USERNAME | `johndoe` | Social media enumeration |
| NETBLOCK | `93.184.216.0/24` | IP range sweeping |
| ASN | `AS15133` | BGP data, IP allocation |
| INTERNET_NAME | `sub.example.com` | Specific hostname |
| URL | `https://example.com/app` | Web content analysis |

### Scan Modes
| Mode | Description | Intensity |
|------|-------------|-----------|
| All | Every enabled module | High (active + passive) |
| Passive | No direct contact with target | Low (DNS, WHOIS, APIs) |
| Investigate | Threat intel, breach, reputation | Medium |
| Footprint | Network mapping, infrastructure | Medium-High |

### Module Categories
```
dns/         - DNS enumeration (zone transfers, bruteforce, records)
whois/       - WHOIS lookups and registrant data
social/      - Social media profile discovery
pwned/       - Breach and credential database lookups
geo/         - Geolocation of IPs
recon/       - General web reconnaissance
malicious/   - Threat intelligence and reputation
leaks/       - Paste sites and data leak detection
network/     - BGP, ASN, traceroute, port scan modules
vulnerabilities/ - CVE and vulnerability lookups
```

## CLI Reference

### Web UI Mode
```bash
# Start on localhost only
python3 sf.py -l 127.0.0.1:5001

# Start accessible on all interfaces (careful on pentest infra)
python3 sf.py -l 0.0.0.0:5001

# Custom data directory
python3 sf.py -l 127.0.0.1:5001 -D /opt/sf-data

# Background service
nohup python3 sf.py -l 127.0.0.1:5001 &>/var/log/spiderfoot.log &
```
Access at: `http://127.0.0.1:5001`

### CLI Scan Mode (sfcli / sf.py)
```bash
# Run scan against a domain, all modules
python3 sf.py -s example.com -t DOMAIN -m all -q

# Passive modules only
python3 sf.py -s example.com -t DOMAIN -m passive -q

# Specific modules (comma-separated)
python3 sf.py -s example.com -t DOMAIN \
  -m sfp_dnsresolve,sfp_dnsdumpster,sfp_shodan,sfp_haveibeenpwned -q

# Save results to file (JSON)
python3 sf.py -s example.com -t DOMAIN -m all \
  -o json -f /tmp/sf_results.json -q

# Save as CSV
python3 sf.py -s example.com -t DOMAIN -m footprint \
  -o csv -f /tmp/sf_results.csv -q

# List all available modules
python3 sf.py -M

# List modules matching a keyword
python3 sf.py -M | grep -i shodan
python3 sf.py -M | grep -i breach
```

### sfcli (Interactive CLI)
```bash
python3 sfcli.py -s 127.0.0.1:5001

# Inside sfcli:
sf> scans               # List all scans
sf> start example.com DOMAIN all     # Start scan
sf> scan list           # List scans with IDs
sf> scan info <scan_id>              # Scan status
sf> scan data <scan_id>              # All results
sf> scan data <scan_id> EMAILADDR    # Filter by data type
sf> scan abort <scan_id>             # Stop scan
sf> scan delete <scan_id>            # Delete scan
sf> exit
```

### Listing and Filtering Results
```bash
# Via sf.py after scan (export modes)
python3 sf.py -s example.com -t DOMAIN -m all -o json | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
emails = [r for r in data if r['type'] == 'EMAILADDR']
for e in emails: print(e['data'])
"
```

## API Key Configuration

SpiderFoot uses API keys for premium/commercial sources. Configure via the Web UI Settings or directly in `~/.spiderfoot/spiderfoot.cfg`.

### High-Value API Keys
```
Shodan          - sfp_shodan         (host intelligence, open ports)
Hunter.io       - sfp_hunter         (email discovery)
HaveIBeenPwned  - sfp_haveibeenpwned (breach lookups)
VirusTotal      - sfp_virustotal     (malware/phishing reputation)
SecurityTrails  - sfp_securitytrails (DNS history, subdomains)
Censys          - sfp_censys         (TLS cert and host data)
GreyNoise       - sfp_greynoise      (IP noise/classification)
Hashes.org      - sfp_hashinfo       (hash lookups)
BuiltWith       - sfp_builtwith      (web technology fingerprint)
Whoisology      - sfp_whoisology     (WHOIS history)
```

### Setting Keys via Web UI
1. Navigate to `http://127.0.0.1:5001` → Settings → Modules
2. Find the module (e.g., `sfp_shodan`)
3. Enter API key in the key field → Save

### Setting Keys via Config File
```bash
# Edit config directly
cat >> ~/.spiderfoot/spiderfoot.cfg <<'EOF'
[sfp_shodan]
api_key = YOUR_SHODAN_KEY
[sfp_virustotal]
api_key = YOUR_VT_KEY
[sfp_hunter]
api_key = YOUR_HUNTER_KEY
EOF
```

## Module Reference — Key Modules

### DNS and Infrastructure
```
sfp_dnsresolve      - Forward/reverse DNS resolution
sfp_dnsbrute        - DNS subdomain bruteforce
sfp_dnsdumpster     - DNSDumpster subdomain discovery
sfp_dnszone         - DNS zone transfer attempts
sfp_ssl             - TLS certificate parsing (CN, SANs)
sfp_censys          - Censys host data
sfp_shodan          - Shodan host and port data
sfp_binaryedge      - BinaryEdge internet scan data
sfp_securitytrails  - Historical DNS and subdomain data
```

### People and Email
```
sfp_hunter          - Hunter.io email discovery
sfp_haveibeenpwned  - Breach database lookup (HIBP)
sfp_emailformat     - Common email format guessing
sfp_github          - GitHub profile and repo data
sfp_linkedin_api    - LinkedIn (via RocketReach or similar)
sfp_twitter         - Twitter/X profile discovery
```

### Threat Intelligence
```
sfp_virustotal      - VirusTotal reputation
sfp_greynoise       - GreyNoise IP classification
sfp_abuseipdb       - AbuseIPDB reputation
sfp_threatminer     - ThreatMiner IOC data
sfp_maltiverse      - Maltiverse threat intelligence
sfp_spamhaus        - Spamhaus DNSBL lookups
```

### Web Reconnaissance
```
sfp_spider          - Web spidering
sfp_builtwith       - Technology detection via BuiltWith
sfp_whatweb         - WhatWeb technology fingerprint
sfp_robots          - robots.txt and sitemap discovery
sfp_googlesearch    - Google dorking for target
sfp_pastebin        - Pastebin content matching
sfp_waybackmachine  - Wayback Machine archive lookup
```

## Correlation Engine

SpiderFoot automatically correlates findings:
- An IP found via DNS is automatically scanned by IP-based modules
- Email addresses feed into breach lookup modules
- Discovered subdomains feed into cert, Shodan, and DNS modules
- The correlation chain can be seen in the Web UI under "Graph" view

### Graph Visualization
- Web UI → Scan → Graph: Force-directed graph of all findings
- Nodes = data entities, Edges = module relationships
- Useful for identifying clusters (e.g., shared hosting, common registrant)

## Export and Reporting

### Web UI Exports
- Navigate to scan → Results → Export (top right)
- Formats: CSV, JSON, GEXF (Gephi graph), Excel

### CLI Exports
```bash
# JSON
python3 sf.py -s example.com -t DOMAIN -m all -o json -f scan.json -q

# CSV
python3 sf.py -s example.com -t DOMAIN -m all -o csv -f scan.csv -q

# Filter specific data types post-scan (from JSON)
python3 - <<'EOF'
import json
data = json.load(open('scan.json'))
types = set(r['type'] for r in data)
print("Available types:", sorted(types))
emails = [r['data'] for r in data if r['type'] == 'EMAILADDR']
print(f"\nEmails ({len(emails)}):")
for e in emails: print(f"  {e}")
EOF
```

### GEXF for Gephi
```bash
# Export GEXF for external graph analysis
python3 sf.py -s example.com -t DOMAIN -m all -o gexf -f scan.gexf -q
# Open scan.gexf in Gephi for advanced visualization
```

## Common Workflows

### Corporate Domain Footprint
```bash
# Full footprint with passive first
python3 sf.py -s target.com -t DOMAIN -m passive -o json -f /tmp/passive.json -q
# Then active
python3 sf.py -s target.com -t DOMAIN -m footprint -o json -f /tmp/active.json -q

# Key questions answered:
# - What subdomains exist?
# - What IPs/hosting providers?
# - What technologies?
# - Any leaked credentials?
```

### Email Breach Investigation
```bash
# Investigate a specific email
python3 sf.py -s target@example.com -t EMAILADDR \
  -m sfp_haveibeenpwned,sfp_hunter,sfp_fullcontact \
  -o json -f /tmp/email_intel.json -q
```

### IP Threat Intelligence
```bash
python3 sf.py -s 93.184.216.34 -t IP_ADDRESS \
  -m sfp_shodan,sfp_greynoise,sfp_abuseipdb,sfp_virustotal \
  -o json -f /tmp/ip_intel.json -q
```

### Username OSINT
```bash
python3 sf.py -s johndoe -t USERNAME \
  -m sfp_github,sfp_twitter,sfp_instagram,sfp_linkedin_api \
  -o json -f /tmp/user_intel.json -q
```

## Advanced Techniques

### Custom Module Development
```python
# /opt/spiderfoot/modules/sfp_custom.py
from spiderfoot import SpiderFootPlugin, SpiderFootEvent

class sfp_custom(SpiderFootPlugin):
    meta = {
        'name': "Custom Module",
        'summary': "Does something custom",
        'flags': [],
        'useCases': ["Passive", "Footprint"],
        'categories': ["Search Engines"],
    }
    opts = {}
    optdescs = {}

    def setup(self, sfc, userOpts={}):
        self.sf = sfc
        self.__dataSource__ = "Custom API"

    def watchedEvents(self):
        return ["DOMAIN_NAME"]

    def producedEvents(self):
        return ["RAW_RIR_DATA"]

    def handleEvent(self, event):
        eventData = event.data
        # Query your custom source
        result = f"Custom result for {eventData}"
        evt = SpiderFootEvent("RAW_RIR_DATA", result, self.__name__, event)
        self.notifyListeners(evt)
```

### Automated Scan + Report Pipeline
```bash
#!/bin/bash
TARGET=$1
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="/opt/sf-reports/${TARGET}_${TIMESTAMP}"
mkdir -p "$OUTPUT_DIR"

python3 /opt/spiderfoot/sf.py \
  -s "$TARGET" -t DOMAIN \
  -m all -q \
  -o json -f "${OUTPUT_DIR}/full.json"

python3 /opt/spiderfoot/sf.py \
  -s "$TARGET" -t DOMAIN \
  -m all -q \
  -o csv -f "${OUTPUT_DIR}/full.csv"

echo "Scan complete: ${OUTPUT_DIR}"
# Extract summary
python3 -c "
import json
data = json.load(open('${OUTPUT_DIR}/full.json'))
types = {}
for r in data:
    types[r['type']] = types.get(r['type'], 0) + 1
for t, c in sorted(types.items(), key=lambda x: -x[1]):
    print(f'{c:4d}  {t}')
"
```

## SpiderFoot HX (Hosted)

SpiderFoot HX at `https://www.spiderfoot.net/hx/` is the commercial hosted version:
- No local installation required
- More API integrations pre-configured
- Collaboration features (shared workspaces)
- REST API for programmatic access
- Costs money but removes API key management burden

## Integration with Other Tools

| Tool | Integration |
|------|-------------|
| Shodan | sfp_shodan module; open ports → Nmap targeted scan |
| theHarvester | Parallel email/subdomain gathering; compare results |
| Maltego | Import SpiderFoot GEXF into Maltego for link analysis |
| Recon-ng | Feed SpiderFoot domains into recon-ng workspaces |
| Amass | SpiderFoot passive → Amass active DNS enumeration |
| Metasploit | Discovered hosts → Metasploit db_import for exploitation |
| BloodHound | SpiderFoot usernames/emails → targeted AD enumeration |

## Troubleshooting

**Web UI not accessible**
```bash
# Check if running
pgrep -a python | grep sf.py
# Check binding
ss -tlnp | grep 5001
# Try different port
python3 sf.py -l 127.0.0.1:5002
```

**Modules returning no data**
- API keys not configured (most modules require keys)
- Rate limited by external service — wait and retry
- Check module log in Web UI under scan → Log tab
- Test module individually: `-m sfp_shodan`

**Scan stuck / hanging**
```bash
# Via sfcli
sf> scan abort <scan_id>
# Or kill and restart
pkill -f sf.py
```

**ImportError on startup**
```bash
cd /opt/spiderfoot && pip3 install -r requirements.txt --upgrade
```

**Database locked**
```bash
# Remove stale lock
rm ~/.spiderfoot/spiderfoot.db-wal ~/.spiderfoot/spiderfoot.db-shm
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
