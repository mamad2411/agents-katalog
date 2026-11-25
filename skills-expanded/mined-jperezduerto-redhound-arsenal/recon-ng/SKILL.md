---
name: recon-ng
description: >
  Build, extend, and operate Recon-ng — a web reconnaissance framework with a modular
  architecture for OSINT gathering and passive reconnaissance. Use when the user needs to
  enumerate domains, discover hosts and contacts, harvest credentials, or produce structured
  OSINT reports. Covers installation, workspace management, marketplace, module loading and
  configuration, API key management, database queries, reporting modules, and OSINT
  methodology integration for penetration testing and intelligence-gathering engagements.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/lanmaster53/recon-ng
  stars: '5.8k'
---

# recon-ng Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs a structured, database-backed OSINT framework
- Enumerating domains, subdomains, hosts, contacts, and credentials
- Building repeatable recon workflows with a persistent workspace database
- Generating formatted OSINT reports (HTML, CSV, JSON, pushpin maps)
- The user asks how to integrate API keys (Shodan, Bing, VirusTotal, etc.) into recon

## What Recon-ng Does

Recon-ng is a full-featured reconnaissance framework modeled after Metasploit's console interface. It provides a modular architecture where each module performs a discrete OSINT task and populates a SQLite database with structured results (hosts, contacts, credentials, locations, ports, vulnerabilities). Data flows between modules via the shared database. The project has ~5.8k GitHub stars.

## Installation

### Kali Linux (apt)
```bash
sudo apt update && sudo apt install -y recon-ng
recon-ng --version
```

### From Source (recommended for latest modules)
```bash
git clone https://github.com/lanmaster53/recon-ng.git /opt/recon-ng
cd /opt/recon-ng
pip3 install -r REQUIREMENTS
python3 recon-ng --help
```

### pip
```bash
pip3 install recon-ng
```

### Dependency Check
```bash
python3 -c "import requests, lxml, mechanize; print('OK')"
# Module-specific deps installed via marketplace on first use
```

## Core Concepts

### Architecture
- **Workspace**: Isolated SQLite database containing all gathered data for an engagement
- **Marketplace**: Online module repository — modules are installed on demand
- **Modules**: Self-contained Python scripts that query APIs, DNS, web, and databases
- **Tables**: Hosts, Contacts, Credentials, Locations, Ports, Vulnerabilities, Pushpins, Profiles

### Data Flow
```
Domains table  →  recon/domains-hosts modules  →  Hosts table
Hosts table    →  recon/hosts-ports modules    →  Ports table
Contacts table →  recon/contacts-credentials   →  Credentials table
Hosts table    →  reporting/html               →  HTML Report
```

### Module Naming Convention
```
category/input_table-output_table/module_name
Examples:
  recon/domains-hosts/brute_hosts      # Domains → Hosts via bruteforce
  recon/domains-hosts/google_site_web  # Domains → Hosts via Google
  recon/hosts-ports/shodan_ip          # Hosts → Ports via Shodan
  recon/contacts-credentials/hibp      # Contacts → Credentials via HIBP
  reporting/html                       # Output HTML report
```

## CLI Reference

### Launching Recon-ng
```bash
# Start with default workspace
recon-ng

# Start with or create named workspace
recon-ng -w target_engagement

# Non-interactive (run script of commands)
recon-ng -r /opt/scripts/recon_script.rc

# Debug mode
recon-ng --debug
```

### Workspace Management
```
[recon-ng] > workspaces list              # List all workspaces
[recon-ng] > workspaces create acme       # Create workspace
[recon-ng] > workspaces select acme       # Switch workspace
[recon-ng] > workspaces remove old_ws     # Delete workspace
```

Each workspace gets its own SQLite database at `~/.recon-ng/workspaces/<name>/data.db`.

### Database Operations
```
# View tables and counts
[recon-ng][acme] > show domains
[recon-ng][acme] > show hosts
[recon-ng][acme] > show contacts
[recon-ng][acme] > show credentials
[recon-ng][acme] > show ports
[recon-ng][acme] > show locations
[recon-ng][acme] > show vulnerabilities
[recon-ng][acme] > show profiles

# Add seed data manually
[recon-ng][acme] > db insert domains
domain (TEXT): acme.com
notes (TEXT): 

[recon-ng][acme] > db insert hosts
ip_address (TEXT): 93.184.216.34
host (TEXT): www.acme.com
notes (TEXT): 

[recon-ng][acme] > db insert contacts
first_name (TEXT): John
last_name (TEXT): Smith
email (TEXT): jsmith@acme.com
title (TEXT): IT Manager

# Query with SQL
[recon-ng][acme] > db query SELECT * FROM hosts WHERE host LIKE '%.acme.com'
[recon-ng][acme] > db query SELECT email FROM contacts WHERE email IS NOT NULL
[recon-ng][acme] > db query SELECT host, ip_address FROM hosts ORDER BY host
```

### Marketplace
```
# Search for modules
[recon-ng][acme] > marketplace search
[recon-ng][acme] > marketplace search shodan
[recon-ng][acme] > marketplace search domains-hosts
[recon-ng][acme] > marketplace search credentials

# View module details
[recon-ng][acme] > marketplace info recon/domains-hosts/brute_hosts

# Install a module
[recon-ng][acme] > marketplace install recon/domains-hosts/brute_hosts

# Install all modules (takes time, installs all dependencies)
[recon-ng][acme] > marketplace install all

# Remove a module
[recon-ng][acme] > marketplace remove recon/domains-hosts/brute_hosts

# Check for updates
[recon-ng][acme] > marketplace refresh
```

### Module Usage
```
# Load a module
[recon-ng][acme] > modules load recon/domains-hosts/brute_hosts

# Short-form (partial match)
[recon-ng][acme] > modules load brute_hosts

# View module info
[recon-ng][acme][brute_hosts] > info

# View and set options
[recon-ng][acme][brute_hosts] > options list
[recon-ng][acme][brute_hosts] > options set SOURCE acme.com
[recon-ng][acme][brute_hosts] > options set WORDLIST /opt/wordlists/subdomains.txt
[recon-ng][acme][brute_hosts] > options set NAMESERVERS 8.8.8.8,1.1.1.1

# Run the module
[recon-ng][acme][brute_hosts] > run

# Go back to main menu
[recon-ng][acme][brute_hosts] > back
```

## API Key Management

```
# List all configured keys
[recon-ng][acme] > keys list

# Add an API key
[recon-ng][acme] > keys add shodan_api <YOUR_KEY>
[recon-ng][acme] > keys add bing_api <YOUR_KEY>
[recon-ng][acme] > keys add virustotal_api <YOUR_KEY>
[recon-ng][acme] > keys add hibp_api <YOUR_KEY>
[recon-ng][acme] > keys add censys_api <CENSYS_API_ID>
[recon-ng][acme] > keys add censys_secret <CENSYS_SECRET>
[recon-ng][acme] > keys add hunter_api <YOUR_KEY>
[recon-ng][acme] > keys add hunterio_api <YOUR_KEY>
[recon-ng][acme] > keys add securitytrails_api <YOUR_KEY>

# Remove a key
[recon-ng][acme] > keys remove shodan_api
```

Keys persist globally across all workspaces in `~/.recon-ng/keys.db`.

## Module Reference — Domains to Hosts

### Subdomain Discovery
```
recon/domains-hosts/brute_hosts            # DNS bruteforce
recon/domains-hosts/google_site_web        # Google: site:domain.com
recon/domains-hosts/bing_domain_web        # Bing: domain:domain.com (needs key)
recon/domains-hosts/certificate_transparency  # crt.sh certificate logs
recon/domains-hosts/dnsdumpster            # DNSDumpster
recon/domains-hosts/hackertarget           # HackerTarget DNS lookup
recon/domains-hosts/shodan_hostname        # Shodan hostname search (needs key)
recon/domains-hosts/threatminer            # ThreatMiner
recon/domains-hosts/virustotal            # VirusTotal passive DNS (needs key)
recon/domains-hosts/netcraft              # Netcraft subdomain data
```

### Domain Intelligence
```
recon/domains-contacts/whois_pocs          # WHOIS POC contacts
recon/domains-contacts/pgp_search          # PGP keyserver email extraction
recon/domains-contacts/hunter_io           # Hunter.io email discovery (needs key)
recon/domains-credentials/pwnedlist        # Credential leaks by domain
recon/domains-vulnerabilities/xssed        # XSS vulnerability history
```

## Module Reference — Hosts to Ports and Credentials

### Host Enumeration
```
recon/hosts-hosts/resolve                  # DNS forward lookup
recon/hosts-hosts/reverse_resolve          # PTR record lookup
recon/hosts-hosts/ssltools                 # SSL cert analysis
recon/hosts-ports/shodan_ip               # Shodan port data (needs key)
recon/hosts-ports/binaryedge              # BinaryEdge port data
recon/hosts-hosts/ipinfodb                # IP geolocation
recon/hosts-locations/maxmind              # MaxMind geolocation
```

### Credentials
```
recon/contacts-credentials/hibp            # HaveIBeenPwned (needs key)
recon/credentials-credentials/credential_recovery  # Format credentials
```

## Reporting Modules

### HTML Report
```
[recon-ng][acme] > modules load reporting/html
[recon-ng][acme][html] > options set FILENAME /tmp/acme_recon.html
[recon-ng][acme][html] > options set CREATOR "Red Team Operator"
[recon-ng][acme][html] > options set CUSTOMER "Acme Corp"
[recon-ng][acme][html] > run
# Opens /tmp/acme_recon.html — summary of all DB tables with counts
```

### CSV Export
```
[recon-ng][acme] > modules load reporting/csv
[recon-ng][acme][csv] > options set TABLE hosts
[recon-ng][acme][csv] > options set FILENAME /tmp/acme_hosts.csv
[recon-ng][acme][csv] > run

# Tables: hosts, contacts, credentials, ports, locations, vulnerabilities
```

### JSON Export
```
[recon-ng][acme] > modules load reporting/json
[recon-ng][acme][json] > options set FILENAME /tmp/acme_data.json
[recon-ng][acme][json] > run
```

### Pushpin (Geolocation Map)
```
[recon-ng][acme] > modules load reporting/pushpin
[recon-ng][acme][pushpin] > options set FILENAME /tmp/acme_map.html
[recon-ng][acme][pushpin] > options set LATITUDE 37.4220
[recon-ng][acme][pushpin] > options set LONGITUDE -122.0841
[recon-ng][acme][pushpin] > run
```

### List (Quick Text Report)
```
[recon-ng][acme] > modules load reporting/list
[recon-ng][acme][list] > options set COLUMN host
[recon-ng][acme][list] > options set TABLE hosts
[recon-ng][acme][list] > options set FILENAME /tmp/hostlist.txt
[recon-ng][acme][list] > run
```

## Common Workflows

### Full Domain OSINT Workflow
```
[recon-ng] > workspaces create acme_corp
[recon-ng][acme_corp] > db insert domains
domain (TEXT): acmecorp.com

# Subdomain discovery (multiple sources)
[recon-ng][acme_corp] > modules load recon/domains-hosts/certificate_transparency
[recon-ng][acme_corp][certificate_transparency] > run
[recon-ng][acme_corp][certificate_transparency] > back

[recon-ng][acme_corp] > modules load recon/domains-hosts/hackertarget
[recon-ng][acme_corp][hackertarget] > run
[recon-ng][acme_corp][hackertarget] > back

[recon-ng][acme_corp] > modules load recon/domains-hosts/google_site_web
[recon-ng][acme_corp][google_site_web] > run
[recon-ng][acme_corp][google_site_web] > back

# Resolve all discovered hosts
[recon-ng][acme_corp] > modules load recon/hosts-hosts/resolve
[recon-ng][acme_corp][resolve] > run
[recon-ng][acme_corp][resolve] > back

# Port data via Shodan
[recon-ng][acme_corp] > modules load recon/hosts-ports/shodan_ip
[recon-ng][acme_corp][shodan_ip] > run
[recon-ng][acme_corp][shodan_ip] > back

# Email harvest
[recon-ng][acme_corp] > modules load recon/domains-contacts/hunter_io
[recon-ng][acme_corp][hunter_io] > run
[recon-ng][acme_corp][hunter_io] > back

# Check breaches
[recon-ng][acme_corp] > modules load recon/contacts-credentials/hibp
[recon-ng][acme_corp][hibp] > run
[recon-ng][acme_corp][hibp] > back

# Report
[recon-ng][acme_corp] > modules load reporting/html
[recon-ng][acme_corp][html] > options set FILENAME /tmp/acme_report.html
[recon-ng][acme_corp][html] > run
```

### Resource Script Automation
```bash
# Create a recon-ng resource script
cat > /opt/scripts/domain_recon.rc <<'EOF'
workspaces select default
db insert domains
acmecorp.com

modules load recon/domains-hosts/certificate_transparency
run
back

modules load recon/domains-hosts/hackertarget
run
back

modules load recon/hosts-hosts/resolve
run
back

modules load reporting/csv
options set TABLE hosts
options set FILENAME /tmp/hosts.csv
run
back
EOF

recon-ng -w acme -r /opt/scripts/domain_recon.rc
```

### Checking Results
```bash
# Query the workspace database directly
sqlite3 ~/.recon-ng/workspaces/acme_corp/data.db \
  "SELECT host, ip_address FROM hosts ORDER BY host;" | head -50

sqlite3 ~/.recon-ng/workspaces/acme_corp/data.db \
  "SELECT email FROM contacts WHERE email IS NOT NULL;" | sort -u

sqlite3 ~/.recon-ng/workspaces/acme_corp/data.db \
  "SELECT username, password, hash FROM credentials;"
```

## Advanced Techniques

### Custom Module Development
```python
# /opt/recon-ng/modules/recon/domains-hosts/custom_source.py
from recon.core.module import BaseModule

class Module(BaseModule):
    meta = {
        'name': 'Custom Source',
        'author': 'operator',
        'description': 'Custom domain-to-host module',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
    }
    
    def module_run(self, domains):
        for domain in domains:
            # Your custom logic here
            results = self.request(f'https://api.example.com/hosts/{domain}')
            for host in results.json().get('hosts', []):
                self.add_hosts(host)
```

### Bulk Domain Seeding
```python
import sqlite3

db_path = '/root/.recon-ng/workspaces/acme_corp/data.db'
domains = ['acmecorp.com', 'acme.io', 'acme-internal.com']

conn = sqlite3.connect(db_path)
c = conn.cursor()
for domain in domains:
    try:
        c.execute("INSERT INTO domains (domain) VALUES (?)", (domain,))
    except sqlite3.IntegrityError:
        pass  # Already exists
conn.commit()
conn.close()
print(f"Inserted {len(domains)} domains")
```

### Exporting for BloodHound / Other Tools
```bash
# Export hosts as target list for nmap
sqlite3 ~/.recon-ng/workspaces/acme_corp/data.db \
  "SELECT ip_address FROM hosts WHERE ip_address IS NOT NULL" \
  > /tmp/targets_for_nmap.txt

nmap -iL /tmp/targets_for_nmap.txt -sV -p 80,443,8080 -oX /tmp/nmap_out.xml

# Export emails for password spray
sqlite3 ~/.recon-ng/workspaces/acme_corp/data.db \
  "SELECT email FROM contacts WHERE email IS NOT NULL" \
  > /tmp/emails.txt
```

## Integration with Other Tools

| Tool | Integration |
|------|-------------|
| SpiderFoot | Parallel OSINT — feed SpiderFoot domains into recon-ng |
| Shodan | sfp_shodan in SpiderFoot vs recon/hosts-ports/shodan_ip |
| theHarvester | Compare email and subdomain results |
| Amass | Feed amass passive output domains into recon-ng DB |
| Nmap | Export recon-ng hosts → Nmap target list for active scanning |
| BloodHound | Email addresses from contacts → AD username enumeration |
| Metasploit | `db_import` Nmap XML that was built from recon-ng host list |
| CeWL | Spider corporate site → wordlist for password spray |

## Troubleshooting

**Module not found after marketplace install**
```bash
# Refresh module list
[recon-ng] > marketplace refresh
# Or reinstall
[recon-ng] > marketplace remove recon/domains-hosts/brute_hosts
[recon-ng] > marketplace install recon/domains-hosts/brute_hosts
```

**API key errors**
```
# Verify key is set
[recon-ng] > keys list | grep shodan
# Re-add key
[recon-ng] > keys remove shodan_api
[recon-ng] > keys add shodan_api YOUR_KEY
```

**Module returns no results**
- SOURCE may not be set correctly: `options list` → verify SOURCE value
- API key may be invalid or rate-limited
- Some modules require data in the DB first (e.g., hosts table must have entries before running hosts→ports module)
- Verify the module query: `info` → shows the SQL query used to pull SOURCE data

**Permission errors on install**
```bash
sudo chown -R $USER ~/.recon-ng/
pip3 install --user <package>
```

**Database locked**
```bash
# Close all recon-ng instances
pkill -f recon-ng
# Remove WAL files
rm ~/.recon-ng/workspaces/*/data.db-wal
rm ~/.recon-ng/workspaces/*/data.db-shm
```

**Slow module execution (Google)**
- Google rate-limits after many requests; use Bing API or other sources
- Add delay: some modules have a `DELAY` option — `options set DELAY 2`
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
