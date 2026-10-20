---
name: anonymous-dark-web-search
description: "Set up and operate anonymous dark web and Telegram search pipelines through Tor — SOCKS5 proxy, dark web search engines (Ahmia, OnionLand), Telegram MTProto search (Telethon), cron sweeps, and circuit rotation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, dark-web, tor, telegram, osint, anonymization, socks5, mtproto, telethon]
    triggers: [dark-web, deep-web, tor, anonymous-search, telegram-search, onion-search, hidden-service, .onion, socks5, circuit-rotation, darkweb-spider, sweep-darkweb]
    related_skills: [osint-threat, cyber-intel-workflow, osint-recon]
---

# Anonymous Dark Web & Telegram Search

Build and operate a fully anonymized search pipeline for dark web (.onion services) and Telegram content. All traffic routes through Tor SOCKS5 — no clearnet requests from your real IP.

## Architecture

```
User request
    │
    ▼
deep_spider.py / tg_searcher.py
    │
    ▼  socks5h://127.0.0.1:9050
Tor SOCKS5 proxy (tor.exe)
    │
    ├── Ahmia.fi (clearnet .onion indexer)
    ├── OnionLand.io (clearnet .onion indexer)
    ├── Telegram MTProto API (Telethon)
    └── .onion hidden services (Torch, etc.)
```

## Prerequisites

### Tor Installation

**Windows (chocolatey):**
```bash
choco install tor -y
# Tor binary: C:\ProgramData\chocolatey\bin\tor.exe
# Expert bundle: C:\ProgramData\chocolatey\lib\tor\tools\tor\tor.exe
```

**Linux:**
```bash
sudo apt install tor
```

**macOS:**
```bash
brew install tor
```

### Python Dependencies
```bash
pip install telethon pysocks stem requests
```

## Setup

### 1. Tor Configuration

Create `torrc`:
```
SOCKSPort 127.0.0.1:9050
ControlPort 127.0.0.1:9051
DataDirectory ~/deep-spider/tor_data
Log notice file ~/deep-spider/tor.log
CookieAuthentication 1
```

**CRITICAL:** Do NOT add `DNSPort` or `AutomapHostsOnResolve` — these can cause permission-denied errors on Windows (port 5353 binding fails). The SOCKS5 proxy handles DNS resolution through Tor automatically when using `socks5h://` (see "socks5h vs socks5" pitfall below).

### 2. Start Tor

**Background (recommended for sweeps):**
```bash
tor -f ~/deep-spider/torrc &
```

**Windows via cmd:**
```bash
cmd.exe /c "C:\ProgramData\chocolatey\bin\tor.exe -f C:\Users\<user>\deep-spider\torrc"
```

### 3. Verify Anonymity

```python
import requests
resp = requests.get("https://check.torproject.org/api/ip",
                    proxies={"http": "socks5h://127.0.0.1:9050",
                             "https": "socks5h://127.0.0.1:9050"},
                    timeout=15)
data = resp.json()
# data["IsTor"] must be True
# data["IP"] is your exit node
```

## Project Structure

```
~/deep-spider/
├── deep_spider.py          # Main spider CLI (dark web + Telegram + surface)
├── tg_searcher.py          # Telegram MTProto search via Telethon
├── cron_sweep_runner.py    # Self-contained cron pipeline (auto-starts Tor)
├── torrc                   # Tor configuration
├── tor_start.bat           # Windows Tor launcher
├── tor_bg.log              # Tor background process log
├── tg_session              # Telegram session file (created on auth)
└── results/                # All sweep output saved as JSON
    ├── darkweb_<keywords>_<timestamp>.json
    ├── sweep_<phase>_<keywords>_<timestamp>.json
    └── tg_mtproto_<keywords>_<timestamp>.json
```

## Dark Web Search

### Working Sources (via Tor)

| Source | Type | Reliability |
|--------|------|-------------|
| Ahmia.fi | Clearnet .onion indexer | Excellent — always works through Tor |
| OnionLand.io | Clearnet .onion indexer | Good — returns results with Wayback links |
| Torch (.onion) | Native .onion search | Variable — many Torch .onion addresses are stale |
| DarkEye / Excavator | Clearnet indexes | Often unreachable through Tor exit nodes |

### CLI Usage

```bash
cd ~/deep-spider

# Quick dark web search
python deep_spider.py darkweb --keywords "credentials dump,breach data,marketplace" --limit 50

# Full sweep with rotation
python deep_spider.py sweep --keywords "breach data,marketplace,stealer logs" --limit 100

# Rotate Tor circuit
python deep_spider.py new-identity
```

### Keyword Strategy

Group by target type for better results:

- **Breach/credential:** `breached data leaked database,credentials dump stealer logs,ransomware leak marketplace`
- **Financial:** `credit card dumps,paypal hacked,bank account login,fullz ssn dob,cvv shop`
- **Market access:** `darknet market,carding forum,harmony market,versus market`

## Telegram Search

### Method 1: MTProto API (Recommended)

Uses `telethon` to search Telegram's native API through Tor. Does NOT need clearnet scraping.

**Setup:**
1. Get API credentials at **my.telegram.org/apps** (free, instant)
2. Create a Telegram account with a burner number (Google Voice works)
3. Set environment variables:
   ```
   TG_API_ID=<your_api_id>
   TG_API_HASH=<your_api_hash>
   ```

**Usage:**
```bash
# First run — authenticates with phone + code, saves session
python tg_searcher.py --keywords "stealer logs,data leak,marketplace"

# Search only channels/groups
python tg_searcher.py --keywords "breach,marketplace" --channels-only
```

The session is saved to `~/deep-spider/tg_session` — subsequent runs don't need re-auth.

**Error handling:** If authentication fails, delete `tg_session` and re-run for fresh auth. Two-factor auth prompts for password on stdin.

### Method 2: Web Search (Limited)

Clearnet Telegram search sites (TGStat, Telemetr) **block most Tor exit nodes**. Only use this when MTProto is unavailable and you're on a non-Tor connection:

```bash
python deep_spider.py telegram --keywords "data leak marketplace"
```

## Cron Pipeline

### Setup

Copy the runner script to the Hermes scripts directory:
```bash
cp ~/deep-spider/cron_sweep_runner.py ~/.hermes/scripts/deep_spider_sweep.py
```

### Create Cron Job

```bash
# Daily at 5 AM ET
hermes cron create "0 5 * * *" \
  --name deep-spider-sweep \
  --script deep_spider_sweep.py \
  --prompt "Run the Deep Spider dark web sweep and report results."
```

The script:
1. Checks if Tor is running (starts it if not)
2. Verifies the exit node via check.torproject.org
3. Runs Phase 1 (breach/credential keywords through Ahmia + OnionLand)
4. Rotates Tor circuit
5. Runs Phase 2 (financial intel keywords)
6. Lists all result files with sizes
7. Outputs a summary (delivered via cron)

## Pitfalls

### socks5h vs socks5

**CRITICAL:** Use `socks5h://` (not `socks5://`) for the proxy URL. The 'h' suffix tells the library to resolve hostnames THROUGH the SOCKS proxy. Without it, `.onion` addresses fail with `getaddrinfo failed` because the system DNS can't resolve them.

```python
# CORRECT — resolves .onion through Tor
TOR_PROXY = "socks5h://127.0.0.1:9050"

# WRONG — resolves DNS locally, breaks .onion
TOR_PROXY = "socks5://127.0.0.1:9050"
```

### Python requests proxy + socket monkeypatching

Do NOT monkey-patch `socket.socket = socks.socksocket` when using `requests` with proxy dicts. The monkey-patch intercepts ALL socket connections including local ones. Use one approach:
- **Recommended:** Just `requests.Session.proxies` with `socks5h://` 
- OR just the monkey-patch with `rdns=True`, but not both

### .onion search engines are unreliable

Torch, DarkSearch, and other .onion-native search engines frequently go offline or change addresses. Ahmia.fi (clearnet) is the most reliable. OnionLand is a good secondary. Build fallback chains rather than depending on any single .onion engine.

### Telegram clearnet sites block Tor exit nodes

TGStat, Telemetr, tgstat.com, and similar sites return 403 for Tor exit traffic. Do not rely on them through Tor. Use Telethon MTProto instead, which connects via Telegram's own protocol and doesn't care about the IP.

### Telegram authentication

On first Telethon run, the script prompts for phone number and then a verification code. If you're running via cron or headless, pre-authenticate by running `tg_searcher.py` interactively once to create the session file, then subsequent runs use the saved session.

### Tor on Windows

- Tor binary is at `C:\ProgramData\chocolatey\bin\tor.exe` (via chocolatey)
- Must use `cmd.exe /c` to launch from git-bash (the .exe doesn't run directly in MSYS)
- `CREATENO WINDOW` flag keeps it from popping a console window
- Check if Tor is running: `curl --socks5-hostname 127.0.0.1:9050 -s --max-time 10 https://check.torproject.org/api/ip`

### Circuit rotation takes time

After sending `NEWNYM`, wait at least 3-5 seconds before the next request. Tor's new circuit establishment isn't instant. The `deep_spider.py new-identity` command handles this.

### DNS port 5353 conflicts

On Windows, adding `DNSPort 127.0.0.1:5353` to torrc will fail with "Permission denied" because something already binds that port. **Don't use it.** The `socks5h://` proxy scheme handles DNS through Tor without needing a separate DNS port.

## Saved Results Format

All results are JSON with this structure:
```json
{
  "source": "darkweb",
  "keyword": "breach data",
  "timestamp": "20260710_123456",
  "count": 24,
  "results": [
    {
      "url": "http://juhanurmihxlp77nkq...onion",
      "title": "...",
      "snippet": "",
      "source_engine": "ahmia",
      "keyword": "breach data"
    }
  ]
}
```

## Verification Checklist

- [ ] Tor installed and SOCKS5 port 9050 listening
- [ ] `check.torproject.org/api/ip` returns `{"IsTor": true}`
- [ ] Ahmia.fi returns results through Tor (`deep_spider.py darkweb --keywords "test"`)
- [ ] Telegram API credentials obtained (my.telegram.org)
- [ ] Telegram session authenticated (run `tg_searcher.py` interactively)
- [ ] Cron job created with `hermes cron create`
- [ ] Tor auto-starts on cron run (test via `cron_sweep_runner.py`)
- [ ] Circuit rotation verified (`new-identity` changes exit IP)
