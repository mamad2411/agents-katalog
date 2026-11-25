---
name: cewl
description: >
  Build, extend, and operate CeWL — a custom wordlist generator that spiders websites and
  extracts unique words for use in password attacks. Use when the user needs to create
  target-specific wordlists from web content, extract email addresses or metadata from sites,
  or build a password attack pipeline using CeWL → rules → hashcat/john/hydra. Covers
  installation, depth control, word filtering, email extraction, metadata parsing, proxy
  and authentication options, and full password attack methodology integration.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/digininja/CeWL
  stars: '2.7k'
---

# cewl Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs target-specific wordlists built from a company's website
- Performing password spraying against Active Directory or web apps where employees write content
- Extracting email addresses from a web target for phishing or username enumeration
- Harvesting metadata (author names, software) from documents linked on a site
- Building a wordlist → rules → cracker pipeline for a password audit

## What CeWL Does

CeWL (Custom Word List generator) is a Ruby application that spiders a given URL to a specified depth and returns a list of words found on the site. These words are useful as password candidates because real employees write company-specific jargon, product names, and internal terms that generic wordlists miss. CeWL is maintained by Robin Wood (digininja) and has ~2.7k GitHub stars.

## Installation

### Kali Linux / Debian (apt — recommended)
```bash
sudo apt update && sudo apt install -y cewl
cewl --version
```

### Ruby Gem (latest version)
```bash
# Requires Ruby >= 2.5
gem install cewl
# Or install from source
git clone https://github.com/digininja/CeWL.git /opt/cewl
cd /opt/cewl
bundle install
ruby cewl.rb --help
```

### Dependency Check
```bash
gem list | grep -E "nokogiri|spider|mime|mini_exiftool"
# If missing: bundle install inside /opt/cewl
```

## Core Concepts

### Spidering
CeWL fetches the target URL and follows links up to the specified depth (`-d`). It stays within the same domain by default, preventing drift to external sites. Every word on visited pages is extracted, deduplicated, and optionally filtered by minimum length.

### Word Extraction Rules
- HTML tags, attributes, and JavaScript are stripped; only visible text content is kept
- Numbers-only strings are excluded by default
- Words are case-sensitive unless `--lowercase` is used
- Duplicate words are removed (each word appears once)

### Email and Metadata Extraction
- `--email` extracts `mailto:` addresses and `@`-format strings found in text
- `--meta` reads metadata from linked documents (PDF, DOCX, XLSX, PPTX) using ExifTool

## CLI Reference

### Basic Usage
```bash
# Simple wordlist from a URL, output to stdout
cewl https://www.target.com

# Save to file
cewl https://www.target.com -w /tmp/target_words.txt

# Specify depth (default: 2; 0 = current page only)
cewl https://www.target.com -d 3 -w /tmp/words_deep.txt

# Minimum word length (default: 3)
cewl https://www.target.com -m 6 -w /tmp/words_6plus.txt

# Count word occurrences (outputs "word, count" format)
cewl https://www.target.com -c -w /tmp/words_counted.txt
```

### Depth and Scope
```bash
# Depth 0: only the single page given
cewl https://www.target.com/about -d 0 -w /tmp/about_only.txt

# Depth 1: target page + all directly linked pages
cewl https://www.target.com -d 1 -m 5 -w /tmp/d1.txt

# Depth 4: aggressive spidering (slower, more coverage)
cewl https://www.target.com -d 4 -m 4 -w /tmp/d4_words.txt

# Offsite links: follow links to external domains
cewl https://www.target.com --offsite -d 2 -w /tmp/offsite.txt
```

### Email Extraction
```bash
# Extract emails to stdout (alongside wordlist)
cewl https://www.target.com -e

# Save emails to a separate file
cewl https://www.target.com -e --email_file /tmp/emails.txt -w /tmp/words.txt

# Emails + wordlist in one run
cewl https://www.target.com -d 3 -m 5 \
  -e --email_file /tmp/emails.txt \
  -w /tmp/words.txt
```

### Metadata Extraction
```bash
# Extract metadata from linked documents (PDF, DOCX, etc.)
# Requires: exiftool (sudo apt install libimage-exiftool-perl)
cewl https://www.target.com --meta -w /tmp/words.txt

# Save metadata to separate file
cewl https://www.target.com --meta --meta_file /tmp/meta.txt -w /tmp/words.txt

# Full run: words + emails + metadata
cewl https://www.target.com -d 3 -m 4 \
  -e --email_file /tmp/emails.txt \
  --meta --meta_file /tmp/meta.txt \
  -w /tmp/full_wordlist.txt
```

### Case and Formatting
```bash
# Lowercase all words (deduplicated after lowercasing)
cewl https://www.target.com --lowercase -w /tmp/lower.txt

# Convert to uppercase post-processing
cewl https://www.target.com -w - | tr '[:lower:]' '[:upper:]' > /tmp/upper.txt

# Remove words shorter than N after CeWL (additional filter)
cewl https://www.target.com -m 3 -w - | awk 'length >= 8' > /tmp/min8.txt
```

### Authentication
```bash
# HTTP Basic authentication
cewl https://intranet.target.com \
  --auth_type basic \
  --auth_user admin \
  --auth_pass password123 \
  -w /tmp/intranet_words.txt

# HTTP Digest authentication
cewl https://intranet.target.com \
  --auth_type digest \
  --auth_user jsmith \
  --auth_pass Summer2024! \
  -d 2 -m 5 -w /tmp/digest_words.txt

# Cookie-based authentication (supply session cookie)
cewl https://app.target.com/dashboard \
  --header "Cookie: session=abc123; PHPSESSID=xyz" \
  -w /tmp/auth_words.txt
```

### Proxy Support
```bash
# HTTP proxy (Burp Suite for inspection)
cewl https://www.target.com \
  --proxy_host 127.0.0.1 \
  --proxy_port 8080 \
  -w /tmp/words.txt

# Proxy with credentials
cewl https://www.target.com \
  --proxy_host proxy.corp.com \
  --proxy_port 3128 \
  --proxy_username user \
  --proxy_password pass \
  -w /tmp/words.txt
```

### User-Agent Customization
```bash
# Custom user-agent string (bypass WAF or appear as Googlebot)
cewl https://www.target.com \
  --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -w /tmp/words.txt

cewl https://www.target.com \
  --user-agent "Googlebot/2.1 (+http://www.google.com/bot.html)" \
  -w /tmp/words.txt
```

### Additional Options
```bash
# Follow redirects (default: yes)
cewl https://www.target.com --no_follow_redirect -w /tmp/words.txt

# Verbose output (shows pages visited)
cewl https://www.target.com -v -w /tmp/words.txt

# Debug output
cewl https://www.target.com --debug -w /tmp/words.txt

# Rate limiting (add delay between requests, in seconds)
cewl https://www.target.com --rate-limit 1 -w /tmp/words.txt

# Include numbers in wordlist
cewl https://www.target.com --with-numbers -w /tmp/words_nums.txt
```

## Common Workflows

### Standard Password List Build
```bash
# 1. Spider target with good coverage
cewl https://www.target.com -d 3 -m 5 --lowercase \
  -e --email_file /tmp/target_emails.txt \
  -w /tmp/cewl_raw.txt

# 2. Check word count
wc -l /tmp/cewl_raw.txt

# 3. Sort and deduplicate
sort -u /tmp/cewl_raw.txt -o /tmp/cewl_sorted.txt
```

### CeWL → Rules → Hashcat Pipeline
```bash
# 1. Generate wordlist
cewl https://www.target.com -d 3 -m 5 -w /tmp/cewl.txt

# 2. Apply hashcat rules to expand (capitalize, add numbers, symbols)
hashcat -a 0 -m 1000 /tmp/ntlm_hashes.txt /tmp/cewl.txt \
  -r /usr/share/hashcat/rules/best64.rule \
  -r /usr/share/hashcat/rules/toggles1.rule \
  --status --status-timer=30

# 3. Additional rules: append years and common suffixes
hashcat -a 0 -m 1000 /tmp/ntlm_hashes.txt /tmp/cewl.txt \
  -r /usr/share/hashcat/rules/d3ad0ne.rule \
  -o /tmp/cracked.txt
```

### CeWL → John the Ripper
```bash
# Generate wordlist
cewl https://www.target.com -d 2 -m 6 -w /tmp/cewl.txt

# Run john with rules
john --wordlist=/tmp/cewl.txt \
  --rules=best64 \
  --format=NT \
  /tmp/hashes.txt

# Show cracked passwords
john --show /tmp/hashes.txt
```

### CeWL → Hydra (Online Attack)
```bash
# 1. Build wordlist
cewl https://www.target.com -d 3 -m 6 --lowercase -w /tmp/cewl.txt

# 2. Use emails as usernames, CeWL words as passwords
# Extract just usernames from emails
cut -d@ -f1 /tmp/emails.txt > /tmp/usernames.txt

# 3. Spray against OWA/Office 365
hydra -L /tmp/usernames.txt -P /tmp/cewl.txt \
  https-post-form \
  "https://mail.target.com/owa/auth.owa:username=^USER^&password=^PASS^:failed" \
  -t 1 -w 3 -V

# 4. Spray against SMB
hydra -L /tmp/usernames.txt -P /tmp/cewl.txt \
  smb://10.10.10.5 -t 1 -W 5
```

### Intranet Portal Wordlist
```bash
# Spider internal wiki/portal with credentials
cewl https://wiki.internal.corp \
  --auth_type basic \
  --auth_user pentest \
  --auth_pass Temp1234! \
  -d 4 -m 4 \
  --meta --meta_file /tmp/meta_authors.txt \
  -e --email_file /tmp/internal_emails.txt \
  -w /tmp/internal_words.txt

# Authors from metadata = likely usernames
cat /tmp/meta_authors.txt
```

## Advanced Techniques

### Merging Multiple CeWL Runs
```bash
# Spider multiple targets (blog, main site, careers page)
for url in \
  "https://www.target.com" \
  "https://blog.target.com" \
  "https://careers.target.com"; do
    cewl "$url" -d 2 -m 5 --lowercase -w /tmp/cewl_$(date +%s).txt
done

# Merge and deduplicate
cat /tmp/cewl_*.txt | sort -u > /tmp/master_wordlist.txt
wc -l /tmp/master_wordlist.txt
```

### Post-Processing with Python
```python
#!/usr/bin/env python3
# Expand CeWL wordlist with common password patterns
words = open('/tmp/cewl.txt').read().splitlines()
output = []
for w in words:
    output.append(w)
    output.append(w.capitalize())
    output.append(w + '1')
    output.append(w + '123')
    output.append(w + '2024')
    output.append(w + '!')
    output.append(w[0].upper() + w[1:] + '!')
with open('/tmp/cewl_expanded.txt', 'w') as f:
    f.write('\n'.join(set(output)))
print(f"Generated {len(set(output))} candidates")
```

### Combining with Crunch for Hybrid Lists
```bash
# CeWL base words + Crunch numeric suffixes
cewl https://www.target.com -d 2 -m 6 -w /tmp/base.txt
# Append 4-digit year to each word
while read word; do
  crunch 4 4 1234567890 | while read num; do echo "${word}${num}"; done
done < /tmp/base.txt > /tmp/hybrid.txt
```

## Integration with Other Tools

| Tool | Integration |
|------|-------------|
| Hashcat | Primary cracker; use CeWL words with `-a 0` + rules |
| John the Ripper | `--wordlist=cewl.txt --rules=best64` |
| Hydra | `-P cewl.txt` for online password spraying |
| Medusa | `-P cewl.txt` for multi-protocol online attacks |
| Burp Suite | Proxy CeWL through Burp to inspect/modify requests |
| SpiderFoot | OSINT to find additional subdomains; CeWL each subdomain |
| Crunch | Generate numeric/symbol suffixes to append to CeWL words |
| Metasploit | `auxiliary/scanner/smb/smb_login` with CeWL wordlist |

## Troubleshooting

**SSL certificate errors**
```bash
# Ignore SSL verification
cewl https://self-signed.target.com --no-verify-ssl -w /tmp/words.txt
```

**Too few words generated**
- Lower `-m` to 3 or 4
- Increase `-d` depth
- Add `--offsite` if relevant content is on subdomains
- Try specific content pages: `/blog`, `/news`, `/about`
- The site may be JavaScript-heavy (CeWL cannot render JS) — use `wget --mirror` first and run CeWL on local files

**JavaScript-rendered sites**
```bash
# Download rendered HTML with a headless browser first
chromium --headless --dump-dom https://www.target.com > /tmp/rendered.html
# Serve locally and point CeWL at it
python3 -m http.server 8888 --directory /tmp &
cewl http://127.0.0.1:8888/rendered.html -d 0 -w /tmp/words.txt
```

**ExifTool missing for --meta**
```bash
sudo apt install libimage-exiftool-perl -y
exiftool --version
```

**Rate-limited by WAF**
```bash
cewl https://www.target.com --rate-limit 2 \
  --user-agent "Mozilla/5.0 (compatible; Googlebot/2.1)" \
  -w /tmp/words.txt
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
