---
name: leak-hunting
description: |
  This skill should be used when the user mentions "hunt leaks", "find breaches", "credential leaks", "data leak", "breach database", "hunt dumps", "leak finder", "leak hunting", "discover leaks", "breached credentials", "combo list", "combolist", "credential dump", "paste site", "pastebin leak", "breach forums", "BreachForums", "Exploit.in", "RaidForums", "Telegram leaks", "leak channel", "h8mail", "dehashed", "LeakCheck", "IntelX", "Intelligence X", "breach correlation", "credential reuse", "credential stuffing list", "breach data", "leaked passwords", "leaked emails", "data broker", "have i been pwned", "HIBP", "combo cloud", "stealer logs", "infostealer", "redline stealer", "raccoon stealer", "leak search", or discusses systematically searching for breached credentials, hunting leaked data across paste sites and forums, correlating breach records across multiple sources, assessing credential reuse exposure, navigating dark web forums for data listings, monitoring Telegram leak channels, using breach search APIs, or building target dossiers from leaked data. Always use this skill when the task involves finding already-breached or already-leaked data about a target — as distinct from discovering live exposed databases (which is the exposed-databases skill). For example, "check if their credentials were in any breaches" or "search for leaks of corp.com emails" should trigger this skill.
version: 2.0.0
---

# Leak Hunting

Systematically discover breached credentials, leaked databases, and dumped data related to a target across paste sites, breach forums, dark web markets, Telegram channels, GitHub repos, and breach search APIs. This skill covers *already-leaked data* — for finding live exposed databases, see the exposed-databases skill.

## Workflow

Leak hunting follows five phases. Each phase feeds the next — do not skip triage or you will waste time acquiring junk data.

```
RECON → HUNT → VALIDATE → TRIAGE → ACQUIRE/HANDOFF
  |        |        |         |           |
  |        |        |         |           +-- open → data-acquisition skill
  |        |        |         |           +-- protected → cross-plugin-pipeline (elliot handoff)
  |        |        |         +-- credibility + freshness + value scoring
  |        |        +-- sample check, domain match, format plausibility
  |        +-- hunt-engine.js (dork, github, forum) + APIs (h8mail, IntelX, HIBP)
  +-- map target surface: domains, emails, brands, subsidiaries
```

---

## Phase 1: Target Reconnaissance

Before generating any queries, map the target's digital footprint to maximize hunt coverage.

### Define the Attack Surface

| Element | How to Find | Example |
|---------|------------|---------|
| Primary domains | Engagement scope, whois, DNS | `corp.com`, `corp.com.br` |
| Email patterns | LinkedIn, public org charts, known breach headers | `first.last@corp.com`, `flast@corp.com` |
| Brand keywords | Company name, products, internal projects, acquisitions | `CorpTech`, `CorpPay`, `Project Atlas` |
| Employee emails | TheHarvester, LinkedIn scraping, prior breach samples | `jane.doe@corp.com` |
| Subsidiaries | CNPJ/corporate registries, SEC filings, crunchbase | `sub.corp.com`, `acquired-co.com` |

### Configure Hunt Profile

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-profile.js show
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-profile.js set <profile>
```

The profile controls which source categories are permitted and what timing delays to apply. See OPSEC section below.

---

## Phase 2: Hunt Execution

Execute queries across all source categories, ordered by ROI (signal quality per time invested).

### Execution Order

| Priority | Source | Tool / Method | Profile Requirement |
|----------|--------|--------------|---------------------|
| 1 | Breach search APIs (h8mail, HIBP, IntelX) | CLI / MCP / API | `surface`+ |
| 2 | GitHub secret search | `hunt-engine.js github` | `surface`+ |
| 3 | Google dorks (paste sites, indexed dumps) | `hunt-engine.js dork` | `surface`+ |
| 4 | Breach forums (BreachForums, Exploit.in) | `hunt-engine.js forum` + manual | `deep`+ |
| 5 | Telegram leak channels | Manual channel search | `deep`+ |
| 6 | Dark web markets (.onion) | Tor Browser, manual | `dark`+ |
| 7 | Stealer log markets (Russian Market, Genesis) | Tor Browser, manual | `dark`+ |

### Breach Search APIs

**h8mail** (aggregated breach search):
```bash
h8mail -t target@corp.com -q domain --all
h8mail -t corp.com -q domain --all -o dumps/h8mail-corp.csv
```
Searches HIBP, LeakCheck, Snusbase, and other APIs. Configure API keys in `~/.h8mail/h8mail_config.ini`.

**Intelligence X** (full-text breach search):
```bash
# Via API
curl -s "https://2.intelx.io/intelligent/search" \
  -H "x-key: $INTELX_API_KEY" \
  -d '{"term":"corp.com","maxresults":100,"media":0,"sort":2,"terminate":[]}'
```

**Have I Been Pwned** (breach membership check):
```bash
# Check single email
curl -s "https://haveibeenpwned.com/api/v3/breachedaccount/user@corp.com" \
  -H "hibp-api-key: $HIBP_API_KEY" \
  -H "user-agent: tyrell-hunter"
```
Returns list of breaches the email appears in — use to identify which breach databases to hunt for.

### Query Generation

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-engine.js dork <target> --category leaks
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-engine.js github <target> --type secrets
node ${CLAUDE_PLUGIN_ROOT}/scripts/hunt-engine.js forum <target>
```

Execute generated queries via MCP tools (Brave Search, Shodan MCP, GitHub search). Do not manually construct queries — the engine optimizes them per source type.

### GitHub Secret Hunting

Beyond `hunt-engine.js`, use dedicated tools for deeper coverage:

```bash
# gitleaks — scan a cloned repo
gitleaks detect --source /path/to/cloned-repo --report-format json --report-path dumps/gitleaks-report.json

# trufflehog — scan GitHub org
trufflehog github --org=target-org --json > dumps/trufflehog-results.jsonl
```

Look for: database connection strings (`mongodb://`, `redis://`, `mysql://`, `postgres://`, JDBC URLs), API keys, AWS credentials, `.env` files, `config.yml` with plaintext passwords.

---

## Phase 3: Validation

Every result must be validated before acquisition. This prevents wasting time and storage on fake, synthetic, or irrelevant data.

### Quick Validation Checklist

1. **Domain match**: Do email addresses in the sample match the target's known domains?
2. **Format plausibility**: Realistic data distributions — mixed names, varied passwords, correct phone/CPF formats
3. **Volume consistency**: Claimed record count plausible for the target's size (a 50-person startup won't have 10M records)
4. **Date plausibility**: Breach date consistent with company history and known breach events
5. **Cross-reference**: Check if this data appears in known public breaches (may be recycled old data)

### Red Flags (Fake / Scam Data)

| Signal | Meaning |
|--------|---------|
| Sequential IDs (1,2,3,4...) with no gaps | Likely generated, not real data |
| All records share the same password hash | Test/seed data |
| Seller has <10 forum posts, claims exclusive fresh data | Probable scam |
| Preview shows only 3-5 records for a "multi-million" dump | Insufficient proof |
| Email domains don't match target at all | Wrong target or fabricated |
| All passwords are plaintext and suspiciously simple | May be a combo list, not a real breach |
| Offered "free" on a known scam channel | Bait for malware or phishing |

### Stealer Log Validation

Stealer logs (from Redline, Raccoon, Vidar, etc.) require extra validation:

- **URL field**: Should contain target's login URL (e.g., `https://portal.corp.com/login`)
- **Timestamp**: Recent timestamps (< 6 months) indicate active infection
- **Machine info**: Hostname, OS, installed software — confirms real infected endpoint
- **Cookie data**: Session cookies may still be valid for account takeover

---

## Phase 4: Source Logging and Classification

Every discovered source gets logged immediately upon discovery — before full validation. Classification happens after validation.

### Log the Source

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/source-tracker.js add <type> <url-or-identifier> "<description>" \
  --data-types email,password,name \
  --records <estimated-count>
```

Source types: `forum`, `paste`, `darkweb`, `telegram`, `github`, `api-result`, `stealer-log`

### Classify After Validation

```
node ${CLAUDE_PLUGIN_ROOT}/scripts/source-tracker.js classify <id> \
  --credibility <high|medium|low|unknown> \
  --freshness <YYYY-MM> \
  --access-method <open|login|purchase|exploit>
```

### Credibility Decision Tree

```
Sample validated against known real accounts?
  YES → credibility: high
  NO  → Seller has 50+ posts and forum vouches?
          YES → credibility: medium
          NO  → Sample format plausible and domain matches?
                  YES → credibility: low
                  NO  → credibility: unknown (or scam → mark dead)
```

---

## Phase 5: Triage and Route

After logging and classifying, route each source to the appropriate next step.

| Access Status | Credibility | Route | Action |
|--------------|-------------|-------|--------|
| Open (direct download) | High/Medium | **data-acquisition skill** | Download, convert, register in acquisition tracker |
| Open (direct download) | Low/Unknown | **Validate first** | Pull sample, re-assess before full acquisition |
| Login required (forum account) | High/Medium | **Manual acquisition** | Use operational identity to download |
| Purchase required | High | **Handoff** | Log in handoff tracker, flag for operator decision |
| Purchase required | Medium/Low | **Skip** | Not worth the investment without higher confidence |
| Exploit required | Any | **cross-plugin-pipeline** | Generate elliot handoff package |
| Dead / 404 | Any | **Close** | `source-tracker.js update <id> status stale` |

### Acquisition Routing

For open sources, proceed directly to the data-acquisition skill:
```
node ${CLAUDE_PLUGIN_ROOT}/scripts/source-tracker.js update <id> status acquired
```

For protected sources requiring elliot:
```
node ${CLAUDE_PLUGIN_ROOT}/scripts/handoff-builder.js create <source-id> \
  --tech-stack "<platform details>" \
  --defenses "<auth type, WAF, etc.>"
```

---

## OPSEC Considerations

The active hunt profile determines which sources you can access and how:

| Profile | Allowed Sources | Timing | Identity |
|---------|----------------|--------|----------|
| `surface` | Public APIs, Google dorks, GitHub, paste sites | Immediate | Operator's own API keys |
| `deep` | + Breach forums, Telegram, paid APIs | 1-5s delays | Operational identity (burner accounts) |
| `dark` | + .onion markets, stealer log shops | 3-10s delays, through Tor | Clean identity, dedicated Tor circuit |
| `ghost` | Same as dark, max anonymity | 10-60s random delays, single-threaded | Fresh identity per session, no API keys tied to real infra |

**Critical**: On `dark` and `ghost` profiles, never access .onion sources from non-Tor infrastructure. Never use real email addresses for forum registration. Never reuse forum identities across engagements.

---

## Handling Failures

| Problem | Response |
|---------|----------|
| h8mail returns no results | Check API key configuration. Try IntelX or manual HIBP lookup. Target may not appear in indexed breaches. |
| Forum post is deleted | Check web archives (Wayback Machine). Search for the same dump on other forums — dumps are often cross-posted. |
| Paste site returns 404 | Paste was removed. Check Google cache or Wayback Machine. Search for the same content hash on other paste sites. |
| Telegram channel is private | Note the channel name and log as `protected`. Check if the channel was previously public (cached previews). |
| Breach data is encrypted/password-protected | Log as `protected`. Check if the password was posted in a separate forum thread or channel message. |
| API rate limit hit | Rotate to a different API. Space out requests. On `ghost` profile, wait and retry after the cooldown period. |
| Suspected honeypot data | Suspiciously perfect data seeded to track downloaders. Mark credibility as `unknown`, do not acquire without operator approval. |

---

## Additional Resources

- **`references/methodology.md`** — Deep reconnaissance methodology: attack surface mapping, query optimization, multi-source correlation, chain of custody, and the complete leak hunting decision framework
- **`references/source-types.md`** — Per-source-type hunting playbooks: indicators, access patterns, credibility matrices, tool commands, and operational notes for each source category
- **`references/paste-and-forum-hunting.md`** — Paste site monitoring, breach forum navigation, Telegram channel discovery, stealer log markets, and dark web marketplace tradecraft
- **`references/breach-correlation.md`** — Correlating findings across multiple breaches: credential reuse analysis, identity pivoting, timeline reconstruction, and building target dossiers from fragmented leak data
