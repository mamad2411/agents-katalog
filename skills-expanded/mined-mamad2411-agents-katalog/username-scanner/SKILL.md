---
name: username-scanner
description: AI-OSINT username scanner — scan 840+ platforms with ML-blended detection.
  Find accounts across social media, forums, dev platforms, and more. Supports Tor/proxy,
  advanced scan levels, JSON/CSV/HTML/MD export, Playwright fallback, and ML retraining.
version: 1.0.0
category: red-teaming
license: MIT
metadata:
  hermes_origin: import
tags:
- OSINT
- username-scanner
- social-media
- reconnaissance
- account-discovery
- username-scanner
related_skills:
- security-orchestrator
- pentest-workflow
- browser-automation-security
---

# Username Scanner — AI-Powered OSINT Username Scanner

## When to Load This Skill

Load this skill when you need to:
- Find a username across 840+ social media platforms and websites
- Check if a target has accounts on specific platforms
- Perform SOCMINT (Social Media Intelligence) username enumeration
- Discover additional accounts linked to a known username
- Validate account existence as part of an OSINT investigation

## Tool: username_scanner

**Package**: `username-scanner` v2.1.0 (PyPI)  
**Binary**: `username_scanner` (installed in Hermes venv)  
**Python path**: `~/.hermes/hermes-agent/venv/bin/username_scanner`  
**Source**: https://github.com/arxhr007/username_scanner

### Key Capabilities

| Feature | Detail |
|:--------|:-------|
| Platforms | 840+ (social media, dev, forums, streaming, etc.) |
| Detection | ML + heuristic blended (25-dim feature vector) |
| Scan levels | basic / intermediate / advanced (prefix/suffix variations) |
| Proxy | HTTP, SOCKS4, SOCKS5, Tor (`--tor`) |
| Export | JSON, CSV, HTML, Markdown (`--format all`) |
| Playwright | JS-heavy page fallback (`--playwright`, needs `[browser]` extra) |
| Profiles | quick / full / aggressive (non-interactive) |
| ML retrain | `username_scanner train collect` → `username_scanner train fit` |
| Self-check | `username_scanner selfcheck` validates detection accuracy |

## Quick Commands

```bash
# ── Basic scan ──
username_scanner username
```

> **⚠️ Common mistake**: `--profile` only accepts **`quick`**, **`full`**, **`aggressive`**. Don't pass `basic`/`standard`/`intermediate` — argparse error: `invalid choice: 'basic'`. The default (no flag) uses `quick`. To get all 820+ sites use `full`. (verified 2026-06-30)
# ── Multiple usernames ──
username_scanner username1 username2

# ── Advanced scan (prefix/suffix variations like _username, username_) ──
username_scanner username -l advanced

# ── Non-interactive profiles ──
username_scanner username --profile quick      # fast, fewer sites (~30s via Tor, ~20s direct)
username_scanner username --profile full       # all sites, default settings
username_scanner username --profile aggressive # more retries, slower but thorough

# ── Target specific platforms ──
username_scanner username --site github,reddit,gitlab

# ── Exclude platforms ──
username_scanner username --exclude-site pornhub,onlyfans

# ── Skip NSFW sites ──
username_scanner username --no-nsfw

# ── Through Tor ──
username_scanner username --tor

# ── Through SOCKS5 proxy ──
username_scanner username --proxy socks5://127.0.0.1:1080

# ── Export all formats ──
username_scanner username --format all --output ./results

# ── Plain text output (for scripting/parsing) ──
username_scanner username --plain

# ── Read/display previous scan results ──
username_scanner -r results/username_advanced_20260611_120000.json

# ── Heuristics only (no ML) ──
username_scanner username --no-ml

# ── Validate detection accuracy ──
username_scanner selfcheck
```

## Detection Method

Each response is converted into a 25-dimensional feature vector:
- HTTP status buckets
- Username placement (path / title / meta)
- Error and profile keywords
- DOM structure (images, forms, profile/error CSS classes)
- Response timing
- Redirect counts
- Per-site fingerprint matches

Two judges vote:
1. **Heuristic engine** — weighted scoring over features
2. **ML model** — logistic regression trained on labeled real + fake scans

Blended probability → **Found / Maybe / Not Found** with confidence %. If model file missing, falls back to heuristics silently.

## OSINT Workflow Integration

### Step 1: Username Discovery
```bash
# Start with basic scan
username_scanner target_user --profile full --format json --output ./osint_results
```

### Step 2: Enrich with Advanced Variations
```bash
# Check username variations (common patterns)
username_scanner target_user -l advanced --format all --output ./osint_results_advanced
```

### Step 3: Combine with Other OSINT Tools
```bash
# Parallel workflow:
# Terminal 1: username_scanner for social media footprint
username_scanner target_user --profile full --format all --output ./osint/

# Terminal 2: Sherlock for cross-validation
sherlock target_user --output ./osint/sherlock/

# Terminal 3: Maigret for deeper non-English platforms
maigret target_user --all-sites --html
```

### Step 4: Analyze Results
```bash
# Read JSON results for programmatic analysis
cat ./osint/target_user_full_*.json | python3 -c "
import sys, json
data = json.load(sys.stdin)
found = [r for r in data.get('results', []) if r.get('status') == 'Found']
maybe = [r for r in data.get('results', []) if r.get('status') == 'Maybe']
print(f'Found: {len(found)} | Maybe: {len(maybe)}')
for r in sorted(found, key=lambda x: x.get('confidence', 0), reverse=True)[:20]:
    print(f\"  {r['site']}: {r['url']} ({r.get('confidence', '?')}%)\")
"
```

### Step 5: Generate Report
```bash
# HTML report for presentation
username_scanner target_user --profile full --format html --output ./osint_report/

# Markdown for documentation
username_scanner target_user --profile full --format md --output ./osint_report/
```

## Configuration

Default config locations (CLI flags override):
1. `./config.json` (cwd)
2. `~/.config/username_scanner/config.json` (Linux/macOS)
3. `%LOCALAPPDATA%\username_scanner` (Windows)

Example config:
```json
{
  "concurrent": 50,
  "timeout": 10.0,
  "retries": 2,
  "rate_limit_delay": 0.2,
  "output_dir": "results",
  "output_formats": ["json", "csv", "html", "md"],
  "use_playwright": false,
  "proxy": null,
  "use_ml": true,
  "exclude_nsfw": false,
  "level": "basic"
}
```

## ML Model Retraining

```bash
# Install training extras
pip install "username-scanner[train]"

# Step 1: Collect ground truth
username_scanner train collect --out dataset.csv --negatives 4

# Step 2: Train model
username_scanner train fit --data dataset.csv --out model.json

# Step 3: Use custom model
username_scanner username --model model.json
```

## Running from Hermes Terminal

**IMPORTANT**: Always use the full venv path to avoid Python version mismatch:
```bash
~/.hermes/hermes-agent/venv/bin/username_scanner username --profile full --format all --output /tmp/username_scanner_results
```

Or activate venv first:
```bash
source ~/.hermes/hermes-agent/venv/bin/activate
username_scanner username --profile full
```

## Comparison with Other Username Scanners

| Tool | Platforms | ML Detection | Speed | Export | Notes |
|:-----|:----------|:-------------|:------|:-------|:------|
| **Username Scanner** | 840+ | ✅ ML+heuristic | Fast (async) | JSON/CSV/HTML/MD | Best detection quality |
| Sherlock | 300+ | ❌ Status code | Medium | TXT/CSV/JSON | Most known, simple |
| Maigret | 2500+ | ❌ Pattern match | Slow | PDF/HTML/JSON | Deepest coverage |
| WhatsMyName | 500+ | ❌ API check | Medium | Web/JSON | Curated list |

---

## ⚠️ Critical: Reading JSON Output (Schema Gotcha)

The README and examples online suggest a flat `{results: [...]}` schema. **The actual output is nested.** Quick Commands' `--format json` produces:

```json
{
  "scan_summary": {"base_username": "...", "scan_level": "...", "total_variations": 1, ...},
  "variations": {
    "<username>": {
      "scan_info": {"username": "...", "sites_scanned": 820, "found": 99, "maybe": 146, "high_confidence_matches": 4},
      "sites": {
        "<platform_name>": {
          "status": "Found" | "Maybe" | "Not Found",
          "code": 200,
          "url": "https://...",
          "final_url": "https://...",
          "confidence": 86,           // integer percent (sometimes 0-1, normalize)
          "ai_analysis": {
            "probability": 0.86,     // ← REAL confidence signal — float 0-1
            "score": 24.0,           // raw heuristic score
            "method": "ml+heuristic",
            "features": {...25-dim feature vector...},
            "signals": {"title": "...", "meta_samples": [...], "url_analysis": {...}, "dom": {...}}
          }
        }
      }
    }
  }
}
```

**Two confidence numbers exist — use `ai_analysis.probability` (float 0-1), not `confidence` (sometimes integer, sometimes missing).**

See `references/json-schema-and-parsing.md` for a working parser that handles both confidence shapes, filters false positives, and ranks real hits.

---

## ⚠️ Critical: "Found" Counts Are Inflated by False Positives

The tool reports `Found: 99` per variant scan — **most are false positives**. ML marks a username "Found" when its probability is barely above the threshold, and many platforms (Telegram, Roblox, Habbo, Civitai, Snapchat, Steam, OurDJTalk, Chatujme.cz, random forum blogs) return 200 with the username in the path even for non-existent profiles.

**Filtering recipe (real workflow from 2026-06-30 Taiwan OSINT run):**

| Filter | Effect |
|:---|:---|
| `status == "Found"` raw | 99-295 hits per variant — mostly noise |
| + `ai_analysis.probability >= 0.75` | Drops to 9-74 — still mixed |
| + `signals.title` contains username OR non-default page | Drops to 5-15 — meaningful |
| + cross-variant: same `final_url` returns Found for 2+ variants | Drops to 0-3 — **real accounts** |

**Cross-variant check is the strongest signal** — if username `zhaohongzhong` AND `zhao_hongzhong` both return Found on the same platform URL, it's almost certainly a real account, not a path-prefix artifact.

**Don't trust "high_confidence_matches" alone** — the tool reports e.g. `high_confidence_matches: 4` per variant, but these are the same 4 platforms every time (Telegram / Snapchat / Roblox-style path conventions). Cross-checking against the username is your job.

---

## Workflow: Chinese-Name Cross-Script OSINT (Taiwan/PRC names)

For Chinese-name targets (`張三`, `王大明`), the username scanner alone finds nothing because:
- Most Chinese users have no English username at all
- The few who do picked it years ago on a whim — you don't know the script
- Tools like Sherlock/Username Scanner are ASCII-only

**Parallel 4-leg workflow:**

| Leg | Tool | What it finds |
|:---|:---|:---|
| 1. English username variants via Username Scanner | `username_scanner` over Tor | Catches ASCII accounts (rare for Chinese names but worth 5 min) |
| 2. Pinyin variants | `username_scanner hongzhong zhaohongzhong hzzhao ...` | Same as leg 1 with different romanization |
| 3. Chinese search engines (Playwright) | Brave Search → Yahoo TW → Baidu | The killer for Taiwan/PRC names — finds school websites, news, papers |
| 4. Domain-specific databases (Playwright) | Google Scholar, Airiti, 華藝, 教育部, TDR | Verifies the identity ("this 趙鴻中 wrote a 2010 thesis on 歐陽脩序跋文 → therefore school X") |

**Variant generator for Chinese names** (e.g., `趙鴻中`):

```python
# Pinyin combinations (concatenated, with separators, with surname last)
base_variants = [
    "zhaohongzhong",        # full concat
    "hongzhongzhao",        # surname-last (Western order)
    "zhao_hongzhong",       # surname_underscore
    "hongzhong_zhao",       # reversed underscore
    "zhao.hongzhong",       # dotted
    "zhaohz",               # surname + given initial
    "hzzhao",               # initials + surname
    "hhzhao",               # initials variant
    "hongzhong",            # given name only (teachers often use this)
    "prof_zhaohz",          # academic prefix
]
# Run Username Scanner with --no-nsfw --profile quick for each (~30s each via Tor)
# Then de-dup by URL across variants
```

**Critical OPSEC note for Chinese-name targets:** This person is almost certainly identifiable in 1-2 public databases. Always default to `--tor` even if the user doesn't explicitly request it — schools, government sites, and breach datasets that will return hits are exactly the ones you don't want logging your scan from a Taiwan/home IP.

**Yahoo TW is the killer for Taiwan names** — Google/Bing/DuckDuckGo all return captcha for bot UA, but `tw.search.yahoo.com` is wide open to curl AND gives richer results than Google Scholar for Chinese academic names.

---

## Workflow: Parallel OSINT (3-track)

For any non-trivial SOCMINT target, run all three in parallel:

```bash
# Track 1: Username Scanner via Tor (background)
~/.hermes/hermes-agent/venv/bin/username_scanner <username> --no-nsfw --tor --profile quick \
    --format json --output /tmp/osint/username_scanner/ &

# Track 2: Username Scanner via Tor with variations (background)
for v in variant1 variant2 variant3; do
    ~/.hermes/hermes-agent/venv/bin/username_scanner "$v" --no-nsfw --tor --profile quick \
        --format json --output /tmp/osint/username_scanner/ &
done

# Track 3: Playwright subagent for Google Scholar / Yahoo TW / school sites
# (delegate_task with parallel-intel or playwright-browser skill loaded)

# Track 4: Web search engines (Brave Search is the only reliable JS-render-free one)
curl -sL -A "Mozilla/5.0 ..." "https://search.brave.com/search?q=%22<name>%22" | grep -oE 'href="[^"]*"' | sort -u
```

Wait for all tracks. Cross-reference by URL. The track-3 (Playwright) hits usually dominate for real-world names because Tor scans yield too many false positives to triage manually.

---

## Configuration (Tor OPSEC)

Tor must be running BEFORE `username_scanner --tor` will work:

```bash
# One-time install
brew install tor

# Start daemon (auto-starts on boot)
brew services start tor

# Verify
nc -z 127.0.0.1 9050 && echo "TOR_UP" || echo "TOR_DOWN"

# Each scan adds 100-150s latency vs direct connection (820 sites through 3-hop circuit)
# Don't run 6 variants sequentially — parallelize with `&` and wait, or accept ~15 min total
```

**Don't expect `--tor` to bypass Google/Bing/DDG captcha** — those detect Tor exit nodes via IP reputation. Use plain `curl` with a regular UA against Yahoo TW, Brave Search, DuckDuckGo HTML, and SearX instances instead.

---

## Pitfalls

- **OPSEC**: Your IP is visible to every platform scanned. Use `--tor` or `--proxy` for sensitive ops. Tor daemon must be running first (`brew services start tor`).
- **Schema gotcha**: Output is nested `variations.<user>.sites.<platform>.ai_analysis.probability`, NOT a flat results list. See `references/json-schema-and-parsing.md`.
- **False positive flood**: Raw `status == "Found"` returns 99-295 per variant. Filter by `probability >= 0.75` AND cross-variant URL dedup before treating any hit as real.
- **Rate limiting**: Some platforms aggressively rate-limit. Lower `--concurrent` (e.g. `-c 20)` or increase `--rate-limit` if getting blocks.
- **Maybe results**: These are uncertain — verify manually or re-run with `--playwright` for JS-heavy pages.
- **MAC vs Linux paths**: Config file location differs. Use `--config` to specify explicitly.
- **Python path**: Hermes venv Python ≠ system Python. Always use `~/.hermes/hermes-agent/venv/bin/username_scanner`.
- **Tor requirement**: `--tor` requires a running Tor daemon on `socks5://127.0.0.1:9050`. Install with `brew install tor && brew services start tor` on macOS.
- **Playwright extra**: `--playwright` requires `pip install "username-scanner[browser]"` + `python -m playwright install chromium`.
- **Large scans**: Scanning 840+ sites generates significant network traffic. Be mindful of bandwidth and time.
- **NSFW content**: Use `--no-nsfw` to skip adult platforms in professional OSINT reports.
- **Result freshness**: Accounts may have been deleted since the scan. Always verify critical findings manually.
- **Chinese names**: Tool is ASCII-only. Always pair with Playwright subagent + Yahoo TW for any CJK target.
- **Tor doesn't bypass search-engine captcha**: Google/Bing/DDG block Tor exits. Use Yahoo TW / Brave Search / SearX / DDG HTML endpoint for crawler-friendly queries.
- **Confidence column actually present is `confidence`, NOT `ai_analysis.probability`** (2026-06-30 Taiwan OSINT run): the README/schema suggests `ai_analysis.probability` is the canonical signal, but in the **`quick` profile** that ships as default, `ai_analysis` is **either absent or empty** — the only consistently populated confidence field is `info["confidence"]` as a **0-100 integer percent**. Filter as: `status == "Found" AND info["confidence"] >= 70`. If `ai_analysis.probability` IS present (e.g. `full` or `aggressive` profiles), prefer it (float 0-1, threshold 0.7). Write filters defensively:
  ```python
  prob = info.get("ai_analysis", {}).get("probability") or (info.get("confidence", 0) / 100.0)
  ```
