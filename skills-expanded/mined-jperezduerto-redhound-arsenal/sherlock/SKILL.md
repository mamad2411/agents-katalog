---
name: sherlock
description: >
  Build, extend, and operate Sherlock — an OSINT tool for hunting usernames across
  social networks and online platforms. Use when the user asks about Sherlock, OSINT
  username enumeration, social media footprinting, account discovery across platforms,
  or building a digital profile of a target. Covers installation, single and bulk
  username searches, output formats (text, CSV, XLSX), filtering by site, proxy and
  Tor support, NSFW site inclusion, false positive mitigation, and integration with
  theHarvester and SpiderFoot for comprehensive OSINT investigations.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/sherlock-project/sherlock
---

# sherlock Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to discover all social media and online accounts tied to a username
- Conducting OSINT reconnaissance on an individual during an authorized engagement
- Building a digital profile: social presence, interests, location leakage, personal details
- Performing bulk username lookups for a list of targets
- The user asks about correlating usernames across platforms or finding account pivots
- Integrating username discovery with other OSINT tools (theHarvester, SpiderFoot, Maltego)

## What Sherlock Does

Sherlock is one of the most widely used OSINT tools for username-based account discovery,
with 62k+ GitHub stars. Given a username, it probes hundreds of social network, forum, and
platform URLs concurrently to determine if an account exists. It identifies profiles on
platforms ranging from mainstream (Twitter/X, Instagram, GitHub, Reddit) to niche gaming,
adult, developer, and regional platforms. Sherlock is written in Python and is
straightforward to automate and integrate into larger OSINT pipelines.

## Installation

```bash
# pip (Python 3.7+)
pip3 install sherlock-project

# From source (recommended for latest site list)
git clone https://github.com/sherlock-project/sherlock.git
cd sherlock
pip3 install -r requirements.txt

# Docker
docker pull sherlock/sherlock
docker run --rm sherlock/sherlock username_to_search

# Docker with output volume
docker run --rm -v /tmp/sherlock:/opt/sherlock/results sherlock/sherlock \
  --output /opt/sherlock/results/results.txt username_to_search

# Verify
sherlock --version
# or from source:
python3 sherlock/sherlock.py --help
```

## Basic Usage

```bash
# Search a single username
sherlock johndoe

# Equivalent from source install
python3 sherlock/sherlock.py johndoe

# Multiple usernames at once
sherlock johndoe jane.doe john_doe_1987

# Output is printed to terminal; found accounts shown in green/white, not-found in red
```

## Output Options

```bash
# Save to text file (default: {username}.txt in current directory)
sherlock johndoe --output /tmp/johndoe_results.txt

# Or let sherlock create default file
sherlock johndoe                    # Creates ./johndoe.txt automatically
cat johndoe.txt                     # One URL per line for found accounts

# CSV output
sherlock johndoe --csv
# Creates: ./johndoe.csv
# Columns: username, name, url_home, url_main, url_subdomains, tags, ...

# XLSX output
sherlock johndoe --xlsx
# Creates: ./johndoe.xlsx

# Specify output directory for all formats
sherlock johndoe --folderoutput /tmp/osint_results/

# Multiple usernames, all to same folder
sherlock johndoe jdoe1987 john.doe --folderoutput /tmp/osint_results/
# Creates: /tmp/osint_results/johndoe.txt, jdoe1987.txt, john.doe.txt
```

## Filtering Results

### Print Only Found Accounts

```bash
# Only display accounts that exist (suppress "Not Found" noise)
sherlock johndoe --print-found

# Print found only AND suppress "Checking..." status lines
sherlock johndoe --print-found --print-all
```

### Filter by Site

```bash
# Search only specific site(s)
sherlock johndoe --site Twitter
sherlock johndoe --site GitHub --site GitLab --site Bitbucket

# Site names are case-sensitive and match the site keys in data.json
# List all supported sites:
sherlock --list-all   # Prints all site names from data.json
```

### Tags-Based Filtering

```bash
# Filter by category tag (social, gaming, news, etc.)
# Tags are defined in data.json per site
# No direct CLI flag — filter post-hoc by parsing CSV output:
sherlock johndoe --csv
grep "gaming" johndoe.csv
```

## Timeout and Performance

```bash
# Set connection timeout per site (seconds, default 60)
sherlock johndoe --timeout 10

# Control number of parallel threads (default auto)
# Sherlock uses asyncio internally — no explicit thread count flag needed
# For slower/unstable networks, increase timeout rather than reduce parallelism

# Benchmark speed against full site list
time sherlock testuser --print-found
```

## Proxy and Tor Support

```bash
# Route through HTTP/HTTPS proxy
sherlock johndoe --proxy http://127.0.0.1:8080
sherlock johndoe --proxy https://proxy.example.com:3128

# SOCKS5 proxy
sherlock johndoe --proxy socks5://127.0.0.1:9050

# Route through Tor (must have Tor service running on :9050)
sherlock johndoe --tor
# Equivalent to --proxy socks5://127.0.0.1:9050

# Tor with unique circuit per search (slower but more anonymous)
sherlock johndoe --unique-tor
# Requests a new Tor circuit for each site check

# Verify Tor is working before bulk search
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/api/ip
```

## NSFW Site Support

```bash
# Include adult content platforms in search
sherlock johndoe --nsfw

# NSFW + print found only
sherlock johndoe --nsfw --print-found

# NSFW sites include: OnlyFans-adjacent platforms, adult forums, etc.
# Use only in authorized investigations targeting adult platform footprints
```

## Bulk Username Search

```bash
# Multiple usernames from command line
sherlock user1 user2 user3 user4

# From a file (one username per line) using xargs
cat usernames.txt | xargs sherlock --folderoutput /tmp/results/

# Shell loop with logging
while read username; do
    echo "[*] Searching: $username"
    sherlock "$username" --print-found --output "/tmp/results/${username}.txt"
    sleep 2  # Rate-limit between searches
done < usernames.txt

# Parallel bulk search with GNU parallel
cat usernames.txt | parallel -j 4 \
  "sherlock {} --print-found --output /tmp/results/{}.txt"

# Process results: aggregate all found accounts
cat /tmp/results/*.txt | sort -u > /tmp/all_found_accounts.txt
```

## Interpreting Results and False Positives

### Understanding Output

Sherlock checks whether an HTTP response for a constructed URL indicates an account exists.
Detection methods per site (defined in `data.json`):

- `message`: Checks for presence/absence of a specific string in the response body
- `status_code`: Checks for a specific HTTP status code (200 = exists, 404 = not found)
- `response_url`: Checks if the final URL after redirects matches expected pattern

### Common False Positive Scenarios

```
1. Generic usernames (admin, info, test, user123) — many platforms have these as defaults
2. Username collision — different people using the same handle on unrelated platforms
3. Reserved/deleted accounts — platform returns 200 for any username (site misconfiguration)
4. Squatted accounts — blank accounts registered by others to block the name
```

### Verification Workflow

```bash
# Step 1: Run sherlock with --print-found
sherlock targetname --print-found --csv

# Step 2: For each found URL, visit manually and cross-reference:
# - Profile photo consistency
# - Bio/description keywords matching target
# - Friend/follower network overlap
# - Post content, language, location tags

# Step 3: Rate confidence:
# HIGH: Photo match + location + mutual connections
# MEDIUM: Username + bio keywords match
# LOW: Username match only (common name)

# Step 4: Extract pivot data from confirmed profiles:
# - Email addresses (in bios or contact sections)
# - Alternative usernames mentioned in posts
# - Location data from posts/check-ins
# - Linked accounts (explicit cross-platform links)
```

### Checking data.json for Site Reliability

```bash
# data.json marks problematic sites with errorType: response_url_false_positive
# Review site detection method before trusting results:
python3 -c "
import json
with open('sherlock/resources/data.json') as f:
    data = json.load(f)
for site, info in data.items():
    if info.get('errorType') in ['message', 'status_code']:
        print(f'{site}: {info[\"errorType\"]}')
"
```

## OSINT Investigation Workflow

### Phase 1: Username Discovery

```bash
# Identify username variants from initial intel (email, LinkedIn, etc.)
# johndoe@gmail.com → try: johndoe, john.doe, jdoe, johndoe1987, j_doe

# Run sherlock against all variants
sherlock johndoe john.doe jdoe johndoe1987 --print-found \
  --nsfw --folderoutput /tmp/phase1/ --csv
```

### Phase 2: Profile Correlation

```bash
# Aggregate found URLs
cat /tmp/phase1/*.txt | sort -u > /tmp/all_profiles.txt

# Count presence per platform
awk -F'/' '{print $3}' /tmp/all_profiles.txt | sort | uniq -c | sort -rn

# Extract profile URLs for manual review
grep -E "linkedin|twitter|instagram|github|facebook" /tmp/all_profiles.txt
```

### Phase 3: Email Enumeration (theHarvester)

```bash
# Use theHarvester to find email addresses associated with the target's domain
theHarvester -d targetdomain.com -b google,linkedin,twitter -l 500 \
  -f /tmp/harvester_results

# Cross-reference emails found with sherlock usernames
# email prefix from harvester → test as sherlock input
grep -oP '[a-zA-Z0-9._%+-]+(?=@)' /tmp/harvester_results.html | sort -u | \
  xargs sherlock --print-found --folderoutput /tmp/email_pivot/
```

### Phase 4: Automated OSINT Pipeline (SpiderFoot)

```bash
# SpiderFoot can incorporate sherlock results via module:
# sfcli.py -s "johndoe" -m sfp_accounts -o tab

# Or use SpiderFoot's web UI:
# python3 sf.py -l 127.0.0.1:5001
# Navigate to: New Scan → Target: johndoe → Module: Account Finder
```

### Phase 5: Metadata Extraction from Profiles

```bash
# For each confirmed profile, extract metadata:
# - GitHub: repos, contributions, gists, email in commits
curl -s "https://api.github.com/users/johndoe" | jq '{name, email, location, blog, created_at}'
curl -s "https://api.github.com/users/johndoe/repos" | jq '.[].name'

# - Twitter/X: use snscrape or twint for historical posts
# - Reddit: use pushshift or the Reddit API for comment history
# - LinkedIn: use linkedin2username for employee enumeration
```

## Integration with Other Tools

| Tool | Use Case |
|------|----------|
| theHarvester | Find emails/names → pivot to sherlock username search |
| SpiderFoot | Automated OSINT orchestration including account discovery |
| Maltego | Visualize sherlock results as entity graphs |
| Holehe | Check if email is registered on sites (complements sherlock) |
| social-analyzer | Deeper profile analysis and sentiment scoring |
| maigret | Extended sherlock-compatible tool with more sites and profile enrichment |
| GHunt | Deep Google account OSINT (cross-reference Google profiles found) |

```bash
# maigret (sherlock-compatible, more sites, better reporting)
pip3 install maigret
maigret johndoe --html --folderoutput /tmp/maigret_report/

# holehe (email-based account check — complements username search)
pip3 install holehe
holehe johndoe@gmail.com

# social-analyzer
pip3 install social-analyzer
social-analyzer --username johndoe --metadata --extract --filter good
```

## Automating Periodic Monitoring

```bash
#!/bin/bash
# monitor_username.sh — alert on new account appearances
USERNAME="$1"
PREV_FILE="/tmp/sherlock_prev_${USERNAME}.txt"
CURR_FILE="/tmp/sherlock_curr_${USERNAME}.txt"

sherlock "$USERNAME" --print-found --output "$CURR_FILE" --timeout 15

if [ -f "$PREV_FILE" ]; then
    NEW=$(comm -13 <(sort "$PREV_FILE") <(sort "$CURR_FILE"))
    if [ -n "$NEW" ]; then
        echo "[!] New accounts found for $USERNAME:"
        echo "$NEW"
        # Add email/Slack notification here
    fi
fi
cp "$CURR_FILE" "$PREV_FILE"
```

## Troubleshooting

**Connection errors / timeouts for many sites:**
```bash
# Increase timeout
sherlock johndoe --timeout 30

# Check network connectivity
curl -s --max-time 5 https://twitter.com > /dev/null && echo "OK"

# Try with Tor if rate-limited
sherlock johndoe --tor --unique-tor
```

**Too many false positives:**
```bash
# Use --print-found and manually verify each URL
# Focus on platforms with `status_code` detection (more reliable than `message`)
# Cross-reference photo, bio, and activity

# Exclude unreliable sites
sherlock johndoe --print-found | grep -v "livelib\|flipboard"
```

**sherlock command not found after pip install:**
```bash
# Ensure pip bin directory is in PATH
export PATH="$HOME/.local/bin:$PATH"
# Or run as module:
python3 -m sherlock johndoe
```

**Rate limiting / 429 responses:**
```bash
# Route through Tor with unique circuit per request
sherlock johndoe --unique-tor --timeout 20
# Or introduce delays in bulk search scripts (sleep between calls)
```

**Missing sites / outdated data.json:**
```bash
# Update from source
cd sherlock && git pull
pip3 install -r requirements.txt --upgrade
# Or: pip3 install sherlock-project --upgrade
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
