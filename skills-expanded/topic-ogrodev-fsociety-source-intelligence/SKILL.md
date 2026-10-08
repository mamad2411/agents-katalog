---
name: source-intelligence
description: |
  This skill should be used when the user mentions "Google dork", "search operator", "inurl:", "filetype:", "intitle:", "site:", "intext:", "dork pattern", "breach forum", "BreachForums", "Exploit.in", "XSS.is", "RaidForums", "forum intelligence", "forum navigation", "seller credibility", "paste site", "Pastebin", "Ghostbin", "paste search", "paste monitoring", "Telegram leak", "Telegram channel", "Discord leak", "channel monitoring", "GitHub secrets", "GitHub scanning", "gitleaks", "trufflehog", "GitLab secrets", "committed credentials", "connection string leak", ".env file leak", "source discovery", "OSINT sources", "leak source", "intelligence gathering", "combolist", "combo list", "credential dump search", or discusses constructing search operator queries to find leaked data, navigating breach forums to locate target-specific listings, scanning paste sites for credentials or PII, monitoring Telegram/Discord channels for fresh leak announcements, scanning GitHub/GitLab repositories for committed secrets and connection strings, or evaluating the credibility of data sellers on underground forums. Always use this skill when the task involves discovering where target data has been leaked or exposed across web and underground sources — for instance, "find if anyone has posted their database on a forum" or "check GitHub for leaked connection strings" or "search paste sites for their credentials" should trigger this skill. It routes source intelligence through hunt-engine.js dork, github, and forum subcommands and logs discoveries via source-tracker.js.
---

# Source Intelligence

Discover where target data has been leaked, exposed, or sold across search engines, code repositories, paste sites, breach forums, and messaging platforms. The goal is to build a complete map of available intelligence sources before any direct acquisition attempt.

## Workflow

Source intelligence follows a structured collection process across five source categories. Work through each category systematically — skipping categories means missed intelligence.

```
SCOPE → DORK → CODE → PASTE → FORUM → CHAT → LOG → ROUTE
  │       │      │       │       │       │      │      │
  │       │      │       │       │       │      │      ├─ classified source → data-acquisition / cross-plugin-pipeline
  │       │      │       │       │       │      └─ source-tracker.js add + classify
  │       │      │       │       │       └─ Telegram/Discord channel monitoring
  │       │      │       │       └─ BreachForums, Exploit.in, XSS.is, dark web
  │       │      │       └─ Pastebin, paste.ee, Rentry, Ghostbin
  │       │      └─ GitHub/GitLab: hunt-engine.js github + gitleaks/trufflehog
  │       └─ Google/Brave dorks: hunt-engine.js dork
  └─ verify target is in-scope for the active engagement
```

---

## Phase 1: Scope Verification

Before generating any queries:

1. Check `engagement.json` or the active campaign scope — confirm the target domain, brand name, and email patterns are authorized
2. Define search identifiers: primary domain (`corp.com`), brand name (`Acme Corp`), email pattern (`@corp.com`), product names, subsidiary domains
3. Check the active hunt profile — it determines which source categories are accessible

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-profile.js show
```

| Profile | Dorks | Code | Paste | Forums | Chat |
|---------|-------|------|-------|--------|------|
| `surface` | Yes | Yes | Yes (via dorks) | No | No |
| `deep` | Yes | Yes | Yes (direct) | Yes (registered accounts) | Yes (joined channels) |
| `dark` | Yes | Yes | Yes (direct + Tor) | Yes (+ .onion forums) | Yes (+ hidden groups) |
| `ghost` | Yes (paced) | Yes (paced) | Yes (Tor only) | Yes (single-threaded, max delays) | Yes (read-only) |

---

## Phase 2: Google/Brave Dork Execution

Generate dork queries targeting the five discovery categories:

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-engine.js dork <target> [--category exposed-db|credentials|dumps|configs|admin-panels]
```

Without `--category`, generates queries for all categories. Execute each generated query via Brave Search MCP tool.

### Dork Categories

| Category | What It Finds | Priority |
|----------|---------------|----------|
| `credentials` | SQL dumps with passwords, paste site credential leaks, CSV/TXT with username:password | **Highest** — direct credential access |
| `dumps` | Directory listings with database dumps, BSON/JSONL data files, breach references | High — raw data files |
| `configs` | `.env` files with DB passwords, YAML/JSON configs with connection strings, Java properties with JDBC URLs | High — infrastructure credentials |
| `exposed-db` | phpMyAdmin panels, Elasticsearch `_cat/indices`, Kibana dashboards, CouchDB Futon, Adminer | Medium — routes to exposed-databases skill |
| `admin-panels` | Login panels, Grafana, Jenkins, RabbitMQ management interfaces | Lower — indirect value, may reveal infrastructure |

### Execution Strategy

1. Start with `credentials` and `dumps` categories — these have the highest ROI for source discovery
2. Execute one dork at a time — search engines rate-limit automated queries
3. For each result page, check pages 2-3 as well — important results are often buried
4. Use `after:YYYY-MM-DD` date filter to surface recent leaks
5. If a result is deleted, try `cache:` operator or Wayback Machine to recover content
6. Archive paste/ephemeral content immediately before it disappears

### Custom Dork Construction

When the generated dorks are not specific enough, build custom queries by combining operators:

**Target-specific credential hunt:**
```
("@DOMAIN" OR "BRAND") ("password" OR "senha" OR "pwd") (filetype:sql OR filetype:csv OR filetype:txt) -site:DOMAIN
```

**Infrastructure exposure sweep:**
```
("BRAND" OR "DOMAIN") (filetype:env OR filetype:conf OR filetype:yml OR filetype:ini) ("password" OR "secret" OR "key")
```

**Broad leak search:**
```
("@DOMAIN" "password") OR ("DOMAIN" "dump" filetype:sql) OR (site:pastebin.com "@DOMAIN")
```

See `references/dork-patterns.md` for the complete operator reference, paste site dorks, Brazilian-specific patterns, and advanced combination strategies.

---

## Phase 3: GitHub/GitLab Code Scanning

Scan public code repositories for committed secrets, connection strings, configuration files, and database dumps.

### Query Generation

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-engine.js github <target> [--type secrets|configs|dumps|env-files]
```

Without `--type`, generates queries for all types. Execute via GitHub code search or GitHub MCP tool.

### Three-Layer Scanning Approach

**Layer 1 — Hunt engine queries (fast, broad)**
Run the generated queries against GitHub code search. This catches currently-visible secrets in public repositories.

**Layer 2 — gitleaks (deep, per-repo)**
After identifying target repositories from Layer 1 or from the target's GitHub organization, scan each with gitleaks for pattern-matched secrets:
```bash
gitleaks detect --source /path/to/cloned/repo --report-format json --report-path gitleaks-report.json
```

**Layer 3 — trufflehog (org-wide, verified)**
For organization-level scanning with verification of found secrets:
```bash
trufflehog github --org target-corp --only-verified --json
```

### What to Look For

| Finding Type | Operational Value | Next Step |
|--------------|-------------------|-----------|
| MongoDB/Redis/Elasticsearch connection string with credentials | **Critical** — direct database access | Probe the endpoint, route to data-acquisition |
| AWS/GCP/Azure credentials | **Critical** — cloud infrastructure access | Route to cross-plugin-pipeline (elliot handoff) |
| `.env` file with `DB_PASSWORD` | **High** — credential for known infrastructure | Match against discovered exposed databases |
| SQL dump file committed to repo | **High** — data already extracted | Download and register as acquisition |
| API keys (Stripe, Twilio, SendGrid) | **Medium** — secondary access | Log for potential lateral movement |
| Hardcoded passwords in application code | **Medium** — may reveal password patterns | Test against target services |

### Commit History Mining

Secrets deleted from current branches remain in git history. After cloning a target repository:
```bash
git log --all -S "password" --oneline
git log --all -S "mongodb://" --oneline
git log --all -S "DB_PASSWORD" --oneline
```

Recover the secret from the specific commit:
```bash
git show <commit-hash>:<file-path>
```

See `references/github-scanning.md` for the full GitHub/GitLab search operator reference, gitleaks/trufflehog usage, self-hosted GitLab recon, and commit history mining techniques.

---

## Phase 4: Paste Site Surveillance

Paste sites are primary distribution channels for leaked credentials, database samples, and configuration dumps.

### Target Paste Sites

| Site | Indexed by Google | Direct Search | Longevity |
|------|-------------------|---------------|-----------|
| Pastebin | Yes | API (paid) | Varies (can be removed) |
| paste.ee | Yes | No API | Usually persistent |
| Rentry | Partially | No API | Persistent |
| Ghostbin | No longer active | N/A | Defunct — check archives |
| dpaste | Yes | No API | Time-limited |
| PrivateBin | No (encrypted) | No | Requires link |

### Search Approach

**Via dorks (surface profile):**
```
site:pastebin.com "@corp.com"
site:pastebin.com "corp.com" "password"
site:paste.ee "@corp.com"
site:rentry.co "corp.com"
```

**Via Pastebin API (deep profile, paid):**
The Pastebin scraping API (`https://psbdmp.ws/api/`) enables real-time monitoring of new pastes matching keywords. Requires a paid account.

### Paste Assessment

For each relevant paste found:

1. **Archive immediately** — pastes disappear without warning. Save the raw content before analysis
2. **Identify data type**: credentials (email:password), database samples (SQL INSERT, JSON records), configuration dumps (.env content), combolists (user:pass format)
3. **Assess volume**: is this a sample (< 100 records) suggesting a larger dataset exists, or a full dump?
4. **Check freshness**: paste creation date, dates in the data itself, email domain activity
5. **Cross-reference**: do email addresses match the target's known patterns? Do credentials work against known services?

### Logging Paste Sources

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/source-tracker.js add paste "https://pastebin.com/XXXXX" "Credential dump: ~500 email:password pairs for @corp.com, MD5 hashed" \
  --data-types email,password \
  --records 500
```

Then classify:
```
node ${CLAUDE_PLUGIN_ROOT}/scripts/source-tracker.js classify <id> \
  --credibility medium \
  --freshness 2025-01 \
  --access-method open
```

---

## Phase 5: Breach Forum Intelligence

Navigate underground forums to find target-specific database listings, credential dumps, and data sales.

### Forum Search Queries

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-engine.js forum <target> [--forum breachforums|leakbase|raidforums]
```

### Search Order

For each forum, execute searches in this order:

1. Primary domain: `corp.com`
2. Brand name: `Acme Corp`
3. Email pattern: `@corp.com`
4. Product names (if different from brand)
5. Country + industry: `brazil banking` (catches industry-wide dumps)

### Thread Evaluation

When you find a relevant thread, extract:

| Field | What to Note |
|-------|-------------|
| **Post date** | Freshness — recent posts mean data may still be available |
| **Sample** | Is a preview file or pastebin sample provided? |
| **Record count** | Claimed number of records — verify against sample |
| **Fields listed** | email, password, CPF, phone, address, etc. |
| **Price** | Free = widely circulated. Paid = potentially exclusive |
| **Source claim** | "hacked from X" vs "scraped from Y" — affects credibility |
| **Seller reputation** | Post count, account age, vouches, rep score |

### Credibility Assessment

**High credibility (act on it):** Account age > 6 months, 50+ posts, verified sales history, sample validates against known data.

**Medium credibility (verify first):** Account age 1-6 months, 10-50 posts, plausible description but limited vouches.

**Low credibility / scam indicators:** New account, no vouches, refuses sample, requests payment outside escrow, "exclusive" data found on multiple forums, sequential test data in sample.

See `references/forum-navigation.md` for the full credibility framework, sample validation techniques, field mapping to the pipeline schema, and operational security guidelines.

---

## Phase 6: Chat Platform Monitoring

Telegram and Discord are primary channels for rapid leak distribution, often surfacing data before it appears on forums or paste sites.

### Telegram Intelligence

**Discovery:** Find breach-focused channels by searching in Telegram's global search, checking forum threads for Telegram links, and monitoring known aggregator channels.

**Monitoring approach:**
- Join target-relevant channels using an operational identity (never personal accounts)
- Search channel history for: target domain, brand name, email pattern
- Monitor for new posts matching target keywords
- Download and archive shared files immediately — they are frequently removed

**Source types on Telegram:**
- Full database dumps shared as files (.sql, .csv, .json, .txt)
- Combolists (email:password format)
- Sample previews with links to paid full dumps
- Announcements of new breaches
- Resold/reshared data from other platforms

### Discord Intelligence

**Discovery:** Breach-focused Discord servers are found through forum invites, Telegram cross-posts, and Google dorks (`site:discord.gg "leak" OR "breach" OR "database"`).

**Monitoring approach:**
- Similar to Telegram but servers are more frequently shut down
- Focus on #leaks, #databases, #freeleaks, #combolists channels
- Bot-posted content often includes automated breach aggregation

### Logging Chat Sources

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/source-tracker.js add telegram "t.me/channel_name/12345" "Database dump announcement: corp.com, ~2M records, posted 2025-03-15" \
  --data-types email,password,phone \
  --records 2000000
```

---

## Phase 7: Log and Classify All Discoveries

Every source discovered across any channel gets logged in the source tracker. Never skip logging — even negative results (no data found on a specific forum) are valuable to prevent re-searching.

### Logging Command

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/source-tracker.js add <source_type> <url_or_identifier> "<description>" \
  [--service <type>] \
  [--access-method open|login|purchase|exploit] \
  [--data-types email,password,name,phone,cpf] \
  [--records <estimated-count>]
```

Source types: `paste`, `forum`, `telegram`, `github`, `exposed-db`, `darkweb`

### Classification

After logging, classify each source:
```
node ${CLAUDE_PLUGIN_ROOT}/scripts/source-tracker.js classify <id> \
  --credibility high|medium|low|unknown \
  --freshness <YYYY-MM> \
  --access-method open|login|purchase|exploit
```

### Routing Classified Sources

| Access Method | Route | Action |
|---------------|-------|--------|
| `open` (paste, public repo, free forum post) | **data-acquisition skill** | Download/dump the data directly |
| `login` (forum account required, Telegram join required) | **data-acquisition skill** | Access with operational accounts, then acquire |
| `purchase` (paid forum listing, paid API) | **Operator decision** | Present the listing details, cost, and credibility assessment — operator decides |
| `exploit` (credential found but target is protected) | **cross-plugin-pipeline skill** | Generate elliot handoff with discovered credentials and target intel |

---

## OPSEC Considerations

| Profile | Dork Execution | Code Scanning | Forum/Chat Access | Timing |
|---------|---------------|---------------|-------------------|--------|
| `surface` | Direct via Brave Search | GitHub API, public repos only | No forums, no Telegram | Immediate |
| `deep` | Direct via Brave Search | GitHub/GitLab + cloning + gitleaks | Forums with registered accounts, joined Telegram channels | 1-5s between queries |
| `dark` | Via Tor if available | + self-hosted GitLab recon | + .onion forums, new accounts via Tor | 3-10s between queries |
| `ghost` | Via Tor only, single query at a time | Paced scanning, single repo at a time | Read-only on all platforms, max delays | 10-60s random delays |

On `deep`/`dark`/`ghost` profiles:
- Use separate operational identities for each platform
- Never cross-reference target identifiers between platforms in the same session
- Rotate search patterns to avoid detection by platform monitoring

---

## Handling Failures

| Problem | Response |
|---------|----------|
| **Search engine rate limit** | Switch to a different search engine (Brave to DuckDuckGo) or pause and retry after 5-10 minutes |
| **Forum account banned/restricted** | Switch to an alternative account or different forum. Log the ban as a blocker in session state |
| **Paste content deleted** | Check `cache:` operator, Wayback Machine, or paste archive services (`psbdmp.ws`) |
| **GitHub search returns no results** | Try broader search terms, check if the org uses a different name, search for employee usernames instead |
| **Telegram channel shut down** | Check for mirror channels, search for the channel name on forums for archived content |
| **gitleaks/trufflehog not installed** | `node ${CLAUDE_PLUGIN_ROOT}/scripts/tool-checker.js check gitleaks` — install via `/ty-install` |
| **Found credentials but unsure if valid** | Log as credibility `unknown`, note in description — never test credentials against live services without explicit authorization |

---

## Additional Resources

- **`references/dork-patterns.md`** — Google/Brave search operator reference, paste site dorks, database dump file dorks, configuration file dorks, open directory dorks, Brazilian-specific patterns, combination strategies, and execution tips
- **`references/github-scanning.md`** — GitHub/GitLab search operators, high-value search patterns (connection strings, cloud credentials, API keys), commit history mining, gitleaks and trufflehog usage, GitLab-specific notes, and source logging
- **`references/forum-navigation.md`** — Forum landscape (active and defunct platforms), navigation strategy, thread evaluation, seller credibility assessment framework, sample validation techniques, field mapping to pipeline schema, and operational security
- **`references/paste-and-chat-monitoring.md`** — Paste site enumeration (Pastebin, paste.ee, Rentry, dpaste), paste assessment methodology, Telegram channel discovery and monitoring, Discord server intelligence, archival strategies, and OPSEC for chat platforms
