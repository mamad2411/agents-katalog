---
name: spiderfoot-automation
description: SpiderFoot 4.0 OSINT automation — one email/domain/username/phone/IP
  seed → full digital footprint map. 231 modules (Shodan, HIBP, VirusTotal, breach
  DBs, SOCMINT, DNS, dark web, etc.) running in parallel. CLI scan + HX2 Web GUI +
  fallback playbook. Authorized OSINT/research use.
version: 1.0.0
category: red-teaming
license: MIT
metadata:
  hermes_origin: import
tags:
- OSINT
- spiderfoot
- intelligence
- reconnaissance
- email
- domain
- SOCMINT
- breach
- HIBP
- Shodan
- darkweb
related_skills:
- security-orchestrator
- username-scanner
---

# SpiderFoot OSINT — One Seed → Full Digital Footprint

## What This Skill Does

Feed SpiderFoot a single seed (email / domain / username / phone / IP / Bitcoin address / hostname) and it returns a correlated digital footprint map: linked accounts, breach history, leaked credentials, phone numbers, public photos, hidden connections, DNS/Subdomain structure, dark web mentions, etc.

**Installed at** `~/tools/spiderfoot/` (SpiderFoot 4.0.0, 231 modules)
**Python venv** `~/tools/spiderfoot-venv/` (Python 3.11)

## Quickstart — CLI Single-Shot Scan

```bash
# Activate environment (always required first)
source ~/tools/spiderfoot-venv/bin/activate
cd ~/tools/spiderfoot

# Email → full investigation scan, JSON output
python3 ./sf.py -s "target@example.com" -u investigate -o json -n -q \
  > ~/osint-reports/spiderfoot_$(date +%Y%m%d_%H%M%S).json

# Domain → all-modules scan
python3 ./sf.py -s "example.com" -u all -o json -n -q > report.json

# Username → passive footprint (no active probing)
python3 ./sf.py -s "target_username" -u passive -o json -n -q > report.json

# Phone → investigation
python3 ./sf.py -s "+886912345678" -u investigate -o json -n -q > report.json

# IP → all modules
python3 ./sf.py -s "1.2.3.4" -u all -o json -n -q > report.json
```

## Use Case Modes (`-u` flag)

| Mode | Behavior | When to use |
|---|---|---|
| `passive` | Only modules that don't actively contact target | Stealth recon |
| `footprint` | Passive + modules that perform lookup but not active probe | Mid-level investigation |
| `investigate` | Footprint + active probing of target | Full active scan |
| `all` | Every module, including potentially intrusive ones | Aggressive scan |

## Output Formats

- `tab` (default): Human-readable tabular
- `csv`: Delimited (use `-D` for custom delimiter)
- `json`: Machine-readable (preferred for agent processing)

## Helper — `sfo.py` Wrapper Script

`scripts/sfo.py` wraps `sf.py` with sensible defaults + JSON normalization + report directory management:

```bash
# One-shot email scan with normalized JSON output
~/tools/spiderfoot/scripts/sfo.py scan -s target@example.com -u investigate -o ~/osint-reports/

# List all event types of interest for email OSINT
~/tools/spiderfoot/scripts/sfo.py event-types --category email

# Show which modules are API-key-required
~/tools/spiderfoot/scripts/sfo.py modules --filter api-key
```

See `scripts/sfo.py` for full reference.

## HX2 (Web GUI) Mode

SpiderFox 4 ships a CherryPy-based web UI (HX2) for visual scan management:

```bash
# Start HX2 web UI on localhost 5001
source ~/tools/spiderfoot-venv/bin/activate
cd ~/tools/spiderfoot
python3 ./sf.py -l 127.0.0.1:5001 &

# Access http://127.0.0.1:5001
# - New Scan → enter target → select use case → Start Scan
# - Watch results stream in real-time (JS-refreshed)
# - Export as JSON / CSV / GEXF (graph) / HTML

# Stop HX2
pkill -f "sf.py -l"
```

**HX2 vs CLI trade-off**: HX2 is interactive (good for visual exploration + graph export), CLI is scriptable (good for agent automation + JSON post-processing). Both share the same 231 modules.

## API Keys — Configuration

Many modules need API keys. Without keys, SpiderFoot still runs ~120 passive modules (WHOIS, DNS, crt.sh, public breach check, public SOCMINT) but skips HIBP/Shodan/VirusTotal/DeHashed/C99/etc.

### Setup

```bash
# Edit the SpiderFoot config file
$EDITOR ~/tools/spiderfoot/spiderfoot.cfg
```

Keys to add (most valuable first, in `[main]` section):

| Key | Env Var in cfg | Module | What it unlocks |
|---|---|---|---|
| HaveIBeenPwned | `haveibeenpwned_api_key` | sfp_haveibeenpwned | Email→breach list |
| Shodan | `shodan_api_key` | sfp_shodan | IP/device/inet recon |
| VirusTotal | `virustotal_api_key` | sfp_virustotal | Domain/IP/URL reputation |
| DeHashed | `dehashed_api_key` + `dehashed_email` | sfp_dehashed | Breach credentials (email/pass) |
| Hunter.io | `hunter_api_key` | sfp_hunter | Email pattern discovery |
| BinaryEdge | `binaryedge_api_key` | sfp_binaryedge | Breach + passive DNS |
| FullContact | `fullcontact_api_key` | sfp_fullcontact | Person enrichment |
| C99 | `c99_api_key` | sfp_c99 | Geo/proxy/phone lookup |
| EmailRep | `emailrep_api_key` | sfp_emailrep | Email reputation score |
| Leak-Lookup | `citadel_api_key` | sfp_citadel | Breach DB search |
| GreyNoise | `greynoise_api_key` | sfp_greynoise | IP noise filtering |
| Pulsedive | `pulsedive_api_key` | sfp_pulsedive | Threat intel |

See `references/api-keys-full.md` for full list + how to obtain each key.

### OPSEC Note

Never commit `spiderfoot.cfg` with keys. Add it to `.gitignore` (already in SpiderFoot's default).

## Event Types for Email OSINT

SpiderFoot emits ~150 event types. For email-seed scans, focus on:

- `EMAILADDR` — emails discovered
- `ACCOUNT_EXTERNAL_OWNED` — accounts on external sites
- `ACCOUNT_EXTERNAL_OWNED_COMPROMISED` — hacked accounts
- `PASSWORD` — leaked passwords (from breach modules)
- `DATA_BREACH` — breach events affecting the email
- `PROVIDER_DNS` — DNS provider of associated domains
- `PHONE_NUMBER` — discovered phone numbers
- `USERNAME` — usernames derived from email
- `SOCIAL_MEDIA` — social profiles
- `GEOIP` — geolocation of associated IPs
- `AFFILIATE_EMAILADDR` — emails of associates
- `RAW_DATA_RIR` — RIR WHOIS data

Filter scan output:
```bash
# Only show breach + account + password events
python3 ./sf.py -s "target@example.com" -u investigate -o json \
  -t "EMAILADDR,ACCOUNT_EXTERNAL_OWNED,ACCOUNT_EXTERNAL_OWNED_COMPROMISED,PASSWORD,DATA_BREACH"
```

## Fallback Pipeline (No API Keys)

If no API keys configured, `scripts/sfo.py` automatically falls back to a parallel pipeline using:
- Hunter.io public page (no key required, limited)
- crt.sh (passive subdomain)
- Wayback Machine (historical URLs)
- username-scanner (840+ platforms username check via email local-part)
- Sherlock + Maigret (3000+ platforms)
- h8mail (public breach dump search)
- GHunt (Google account OSINT for Gmail addresses)
- holehe (100+ services account presence check)
- theHarvester (email enumeration from search engines)
- Yahoo TW search (CJK real-person — see `references/api-keys-full.md`)

Fallback command:
```bash
~/tools/spiderfoot/scripts/sfo.py fallback -s "target@example.com" -o ~/osint-reports/
```

## Methodology — Seed → Full Map (5 Phases)

### Phase 1: Seed Triage
- Detect seed type (email/domain/username/phone/IP/BTC)
- If email: extract local-part as candidate username, domain for subdomain recon
- If username: prepare 5 handle variants (lowercase, original case, with numbers, etc.)
- If phone: normalize to E.164 via `phonenumbers` lib
- If domain: pre-resolve A/MX/NS/TXT for validation

### Phase 2: Parallel Run
```bash
# SpiderFoot primary scan
python3 ./sf.py -s "$SEED" -u investigate -o json -n -q > "$REPORT.json" &

# Parallel fallback pipeline (no key dep) for cross-validation
~/tools/spiderfoot/scripts/sfo.py fallback -s "$SEED" -o ~/osint-reports/ &

# username-scanner + Maigret cross-platform username scan (if email local-part available)
username_scanner "$USERNAME" --profile full --format json --output ~/osint-reports/ae/ &
maigret "$USERNAME" --json --output ~/osint-reports/maigret/ &

wait
```

### Phase 3: Process + Correlate
```bash
# Normalize SpiderFoot JSON → entity-keyed dict
~/tools/spiderfoot/scripts/sfo.py normalize -i "$REPORT.json" -o "$REPORT.entities.json"

# Merge with fallback results
~/tools/spiderfoot/scripts/sfo.py merge \
  -i "$REPORT.entities.json" ~/osint-reports/fallback.json \
  -o "$REPORT.merged.json"
```

### Phase 4: Analysis
- Build entity graph: email ↔ username ↔ accounts ↔ breaches ↔ IPs ↔ domains
- Score confidence: High (multiple sources agree), Medium (single source), Low (inferred)
- Pivot identification: which secondary entities reveal new investigation paths (e.g., discovered username reveals Reddit → pastebin → leaked password)

### Phase 5: Report
- Markdown timeline report (see `references/report-template.md`)
- GEXF entity graph (from HX2 export or `scripts/build_gexf.py`)
- Critical findings table (breaches, leaked passwords, full-name disclosures)

## Pitfalls

- **API key reliance**: SpiderFoot's "200+ modules" marketing is misleading — without API keys at least 50% of the valuable modules (HIBP, Shodan, VT, DeHashed) silently skip. Always cross-validate with fallback pipeline.
- **HIBP rate limit**: Free tier is 10 req/min via API key; aggressive scans may stall. Use `-max-threads 5` to throttle.
- **Module stale references**: Some modules (sfp_git, sfp_pastebin) regularly break due to upstream API changes. Always test with `python3 ./sf.py -m sfp_X -s test@example.com -o json` before relying on.
- **Email misattribution**: `EMAILADDR` events include emails discovered *in any data about the target* (e.g., WHOIS of an associated domain). Not all emails belong to the seed person. Cross-reference with `ACCOUNT_EXTERNAL_OWNED` for true attribution.
- **Username guessing from email local-part is noisy**: `john.doe@example.com` → "john.doe", "johndoe", "jdoe" — these are guesses, not confirmations. Mark as "candidate username" until username-scanner/maigret/sherlock confirm 200 status.
- **macOS Python 3.9 system Python breaks SpiderFoot**: Always use the installed venv at `~/tools/spiderfoot-venv/` (Python 3.11). Never try `brew install spiderfoot` — it doesn't exist; manually clone + venv.
- **HX2 background start without `&` blocks the agent**: Always background with `&` or use `<session_id> ← terminal(background=true)` and keep PID.
- **No OPSEC on entity enrichment**: Each module API call logs your IP. For sensitive investigations, route SpiderFoot via Tor (set `socks_proxy = socks5://127.0.0.1:9050` in `spiderfoot.cfg`) — but not all modules honor SOCKS.
- **CherryPy version pins**: `requirements.txt` pins `CherryPy>=18.8.0,<19`. If a later CherryPy is installed for another package, HX2 web UI may break. Keep `spiderfoot-venv` isolated.
- **SpiderFoot v4 + macOS fd limit**: SpiderFoot 4.x runs ~200 modules in concurrent subprocesses and needs ~10K file descriptors. The macOS default `ulimit -n` is 256 — silently kills most modules with "Too many open files" errors. Always raise: `ulimit -n 10240` before launching, or use `sfo.py wrapper` which does it automatically.
- **SpiderFoot v4 CLI stdout is NOT the authoritative event source**: v4 CLI runs the scan in a subprocess; events go to `~/.spiderfoot/spiderfoot.db` SQLite. stdout is a JSON-array stream that can be cut short by pipe deadlock or closed before flush. Always read events from SQLite post-scan. The `sfo.py` wrapper does this automatically.

## Username Disambiguation — Critical Real-World Pattern

**The `yuanhan@mail.tca.org.tw` investigation revealed a universal OSINT trap:**

Common usernames (`yuanhan`, `john`, `admin`, `alex`, `chen`, `wang`, `lee`, `kim`, `smith`, `test`, `demo`, etc.) are **shared by many different people** across platforms. A single username seed like `yuanhan` resolves to **multiple distinct real-world identities**:

| Platform | Displayed Identity | Likely Distinct Person |
|---|---|---|
| GitHub (`github.com/yuanhan`) | **袁晗 / Han Yuan** — 上海財經大學助理教授, 經濟學博士 | Person A |
| GitLab (`gitlab.com/yuanhan`) | **Henry Lee** | Person B |
| Behance (`behance.net/yuanhan`) | **YUAN HAN in USA** (designer) | Person C |
| SoundCloud (`soundcloud.com/yuanhan`) | Located **Shanghai** | Person D |
| Telegram (`t.me/yuanhan`) | No identifying info | Unknown |
| TCA Innoserve Awards | `yuanhan@mail.tca.org.tw` — 專案承辦人, 電話 #879 | Person E (target) |

**Key insight**: `yuanhan` is a common romanization for 袁瀚 / 源瀚 / 苑涵 / 遠涵 / 元瀚… — **at least 4-5 different people** actively use this handle. The 110 "high-confidence" accounts from username-scanner are a **collage of multiple identities**, not one person.

### Disambiguation Protocol (Add to Your Workflow)

1. **Treat username hits as "candidate profiles", not confirmed identities**
   - Every `ACCOUNT_EXTERNAL_OWNED` hit from a common username is a *hypothesis*, not a fact.

2. **Require cross-platform attribute correlation for confirmation**
   - Same avatar hash (Gravatar) across GitHub + GitLab + Behance?
   - Same bio snippet ("PhD Economics, Arizona") on LinkedIn + GitHub + personal site?
   - Same email in public commits (GitHub) matching the seed email?
   - Same location (Shanghai / Taipei / USA) declared consistently?

3. **Use "anchor attributes" to cluster profiles into personas**
   - Anchor = rare, specific attribute (personal site URL, ORCID, unique email, published paper DOI, ORCID)
   - Cluster all profiles sharing ≥1 anchor → persona
   - Profiles with zero anchors → "unattributed candidate"

4. **Document attribution confidence per profile**
   - **Confirmed**: ≥2 independent anchors match seed
   - **Probable**: 1 anchor + consistent bio/location
   - **Candidate**: Username match only, no anchors
   - **Different person**: Conflicting anchors (different PhD university, different name, different country)

5. **In reports, always separate "seed-attributed" vs "username-candidate" findings**
   - Seed-attributed: breach events for `yuanhan@mail.tca.org.tw`, TCA contact page listing
   - Username-candidate: 110 username-scanner accounts (flag as "requires disambiguation")

### Practical Disambiguation Steps for This Case

```bash
# 1. Check GitHub profile README/bio for TCA / Taipei / Taiwan mention
# → github.com/yuanhan README has NO TCA reference, only Shanghai/US academic

# 2. Check Gravatar hash consistency
# → github.com/yuanhan avatar ≠ gitlab.com/yuanhan avatar

# 3. Search ORCID / Google Scholar for "yuanhan" + "TCA" / "Taipei Computer Association"
# → zero hits

# 4. Search Taiwan thesis systems (TDR/NDLTD) for advisor email yuanhan@mail.tca.org.tw
# → zero hits (different academic domain)

# 5. Conclusion: GitHub/GitLab/Behance yuanhan = NOT the TCA coordinator
```

---

## Real-World Investigation Patterns (Template)

### Pattern A: Corporate/Org Email → Staff Identity
```bash
# 1. SpiderFoot on email (passive + breach + accounts)
sfo.py scan -s "target@org.tw" -u investigate -o ~/osint-reports/

# 2. Extract org domain, scan subdomains + contact pages
sfo.py scan -s "org.tw" -u passive -o ~/osint-reports/

# 3. Search org contact pages for email + name pairing
#    → grep "target@org.tw" on org.tw/about, org.tw/contact, org.tw/staff, org.tw/project-X
#    → Often "Ms. Chen | target@org.tw | ext 1234" appears on project pages

# 4. Cross-ref with LinkedIn: site:linkedin.com "target@org.tw" OR "Org Name" "target"
#    → If org has LinkedIn page, check "People" tab for matching name

# 5. Disambiguate username from email local-part
#    → If email is "jchen@org.tw", check if "jchen" on GitHub = same person
#    → Apply Disambiguation Protocol above
```

### Pattern B: Username-Only Seed (No Email)
```bash
# 1. username-scanner + Maigret + Sherlock (parallel) for breadth
username_scanner "username" --profile full --format json -o ~/osint/ae/
maigret "username" --json -o ~/osint/maigret/

# 2. Cluster results by anchor attributes
#    → Extract: display_name, bio, location, website, avatar_url from each hit
#    → Group by (avatar_hash, website, email_in_bio, ORCID, unique_phrase)

# 3. For each cluster, search "display_name" + "location" on LinkedIn/Facebook
#    → Confirm or split clusters

# 4. Report: "Cluster A (23 profiles) → likely Person X; Cluster B (11 profiles) → likely Person Y; 47 unclustered candidates"
```

### Pattern C: Breach-Only Investigation (No API Keys)
```bash
# 1. sfp_citadel (Leak-Lookup free) + LeakCheck.io public API + holehe
#    → Gives breach list without HIBP/DeHashed keys

# 2. If breach found → search breach name + "pastebin" / "git" / "dump"
#    → Sometimes breach dumps contain full name / phone / address for the email

# 3. If password hash leaked → check if reused on other services (credential stuffing simulation, authorized only)
```

---

## Verification Checklist (Updated)

Before declaring scan complete:
- [ ] `sf.py -V` exits 0 with version `4.0.0`
- [ ] At least 1 non-empty event type in output JSON (not just module errors)
- [ ] If breach/leak expected but `PASSWORD` events = 0, check HIBP/DeHashed keys in cfg
- [ ] If `ACCOUNT_EXTERNAL_OWNED` = 0, cross-check with username-pivot scan
- [ ] Run `scripts/sfo.py normalize` — exit 0, non-empty `entities.json`
- [ ] Run `merge` step — combined entity count > sum of individual / 2 (no zero overlap means pipeline broken)
- [ ] **NEW**: If common username used, apply Disambiguation Protocol — document which hits are seed-attributed vs username-candidates
- [ ] **NEW**: Report separates "seed-attributed findings" from "username-candidate profiles" with confidence labels

---

## Integration with Existing osint Skill

This skill is a **specialized module** under the `osint` umbrella. For OSINT methodology framework, see `osint` skill. For SpiderFoot-specific automation + wrapper scripts, this skill. For parallel-multi-source search discipline, see `parallel-intel-gathering`.

Cross-reference table:
| Need | Use |
|---|---|
| Full OSINT methodology (planning → reporting) | `osint` skill |
| SpiderFoot execution (CLI/HX2/wrapper) | this skill |
| Multi-engine parallel search (Shodan + Bing + Yandex) | `parallel-intel-gathering` |
| Username scanning quality (840+ platforms, ML detection) | `username-scanner` skill |
| CJK real-person OSINT (Chinese names that scanners miss) | `references/api-keys-full.md` |

---

*Last updated: 2026-07-21 — Lessons integrated from `yuanhan@mail.tca.org.tw` investigation (TCA Innoserve Awards coordinator disambiguation vs GitHub/Behance/GitLab/SoundCloud identity collision).*
