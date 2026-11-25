---
name: consumer-data-privacy-rights
description: >-
  Proactive enforcement of CCPA/CPRA data privacy rights — identify every service
  holding personal data, submit Data Subject Access Requests (DSAR) for copies,
  demand deletion, track compliance, and escalate noncompliance to regulatory
  authorities. Covers ALL service categories (subscriptions, hotels, cloud tools,
  financial services, social media, etc.) — not just people-search data brokers.
version: 1.0.0
author: Hermes Agent (Counsel)
metadata:
  hermes:
    tags: [legal, privacy, ccpa, cpra, data-rights, dsar, compliance, consumer-protection]
    triggers:
      - ccpa
      - cpra
      - data rights
      - privacy request
      - dsar
      - right to know
      - right to delete
      - data subject access
      - opt out sale
      - data deletion
      - privacy compliance
      - consumer privacy
    related_skills:
      - hermes-legal-watchdog
      - fcra-consumer-disclosure
      - fcra-disclosure-requests
---

# Consumer Data Privacy Rights Enforcement

## When to Use This Skill

Activate when the user says one of:
- "Send CCPA requests to [services]"
- "Request my data from [company]"
- "I want all my data deleted from [service]"
- "Track my privacy requests"
- "Set up a data privacy pipeline"
- Any mention of CCPA, CPRA, DSAR, Right to Know, Right to Delete, data subject access request

This covers **all services** that hold personal data — subscriptions, hotels, airlines, cloud tools, financial accounts, social media, e-commerce, streaming, healthcare, etc. Not limited to data brokers/people-search sites (those are covered by `hermes-legal-watchdog` reputation management).

## Prioritization Strategy

Not all services should be hit with the same approach. Order matters.

| Priority | Category | Strategy | Rationale |
|----------|----------|----------|-----------|
| 🥇 | **Google** (Gmail, Drive, Photos, YouTube, Location History) | BACKUP FIRST via Google Takeout. Download all archives. Verify completeness. THEN submit DSAR + Deletion. | Google is the single largest data profile. Once deleted, some data (search history, location timeline) is irrecoverable. |
| 🥇 | **Amazon & Apple** | Same as Google — backup purchases, iCloud content, device data first. | Purchase history, iCloud content may be lost on deletion. |
| 🥇 | **Credit Bureaus** (Equifax, Experian, TransUnion, LexisNexis, Innovis, ChexSystems) | FREEZE credit FIRST at every bureau. Then submit DSAR. Then pursue deletion. | Freezing prevents new accounts while you're in the process. The bureaus can also flag your file for identity verification on re-requests. |
| 🥇 | **Data Brokers** (1,000+) | Direct to combined DSAR + Deletion. No backup needed — their data is third-hand anyway. | Batch these for volume efficiency. Most have web opt-out forms. |
| 🥇 | **People Search Sites** (Spokeo, Whitepages, BeenVerified, etc.) | Direct opt-out via their webforms, then DSAR + Deletion. | These have dedicated opt-out flows that are faster than formal DSAR. |
| 🥈 | **Social Media** (Discord, Reddit, X, LinkedIn) | Backup content (export chats, posts) first if valuable. Then DSAR + Delete. | Social platforms have export tools analogous to Google Takeout. |
| 🥉 | **Streaming/SaaS subscriptions** (Spotify, Netflix, GitHub, etc.) | Cancel first if no longer needed. Then DSAR + Delete. | Reduces noise — no point requesting data from a service you're still using. |

## Legal Framework

The California Consumer Privacy Act (CCPA, Cal. Civ. Code § 1798.100 et seq.) as amended by the California Privacy Rights Act (CPRA) grants California residents:

| Right | Statute | Description | Deadline for Business |
|-------|---------|-------------|---------------------|
| Right to Know (DSAR) | § 1798.110 | Full disclosure of all personal information collected, used, disclosed, or sold | 45 days (+45 day extension) |
| Right to Delete | § 1798.105 | Deletion of all personal information | 45 days |
| Right to Opt-Out | § 1798.120 | Opt-out of sale/sharing of personal information | 15 days |
| Right to Correct | § 1798.106 | Correction of inaccurate personal information | Reasonable time |
| Right to Non-Discrimination | § 1798.125 | No retaliation for exercising rights | Ongoing |

**Jurisdiction:** Applies to any for-profit business that collects California residents' personal data and meets one of: >$25M annual revenue, buys/sells personal data of 100K+ residents, or derives 50%+ revenue from selling personal data. This covers most companies the operator interacts with.

## Core Workflow

### Phase 1 — Service Discovery

Build a comprehensive inventory of every service holding personal data.

**Discovery sources (in order of yield):**
1. **Email inbox** — Search Gmail for welcome emails, receipts, invoices, monthly statements, subscription renewals
2. **Password manager** — Export all saved credentials
3. **Bank/credit card statements** — Scan 12+ months for recurring charges and merchant names
4. **Phone apps** — List all installed apps (each likely has an account)
5. **Browser data** — Saved passwords, autofill entries, browsing history
6. **Direct prompts** — Ask the user about new services periodically

**Categories to track:**
- Social Media & Communication (Discord, Telegram, X, Reddit, GitHub, LinkedIn)
- Cloud & Productivity (Google Workspace, Microsoft, Notion, Obsidian, Linear)
- AI & Development Tools (OpenAI, Anthropic, OpenRouter, FAL.ai, HuggingFace, HuggingFace)
- Financial & Payment (Banks, credit cards, PayPal, Stripe, Coinbase, brokerages)
- Email & Marketing (Mailchimp, ConvertKit, Postiz, Airtable)
- Business & CRM (Twenty CRM, Gumroad, ChocoData)
- Travel & Hospitality (Airbnb, Booking.com, hotel chains, airlines, Uber, car rental)
- E-Commerce & Retail (Amazon, Apple, Walmart, Target)
- Streaming & Entertainment (Spotify, Netflix, Apple Music)
- Healthcare & Insurance (Health insurance, pharmacy, doctors)
- Telecom & Utilities (Phone carrier, ISP, electric/gas)
- Government (DMV, IRS, SSA, county records)

### Phase 2 — Request Preparation & Submission

**Use the COMBINED request (DSAR + Deletion) as the default** — one letter that first asks for all data, then requests deletion upon receipt. This is the most efficient approach.

**Request types:**
1. **Combined DSAR + Deletion** — Preferred: request data copy, then deletion in same letter
2. **Standalone DSAR** — When you only want the data copy first
3. **Standalone Deletion** — When you already know what data they have
4. **Opt-Out of Sale/Share** — For ad-supported services that sell data
5. **Correction** — If data received has errors
6. **Follow-Up/Demand** — For noncompliant businesses past statutory deadlines

**Submission methods (preference order):**
1. Privacy portal / web form (fastest, best routing)
2. Email to privacy@[company].com
3. Email to legal@[company].com
4. Certified mail return receipt (for high-value targets or noncompliant businesses)

**Always save:**
- Copy of the request text
- Screenshot of web form confirmation
- Date sent, method used
- Contact address/email used

### Phase 3 — Response Handling

| Timeline | Action |
|----------|--------|
| Within 10 days | Company must acknowledge receipt |
| Within 45 days | Company must provide data OR confirm deletion |
| Up to 90 days | With 45-day extension (company must notify you) |

**When data is received:**
- Save all data files to the service's correspondence folder
- Review for: accuracy, surprising data, unauthorized third-party sharing
- Catalog findings — what categories of data do they hold?
- Follow up with deletion request if not already sent

**When company is noncompliant:**
- No ack within 15 days → send FOLLOW-UP demand letter via certified mail
- No data within 45 days → send demand letter threatening CPPA complaint
- No data within 60 days → file CPPA complaint
- 90+ days → escalate to user for litigation consideration

### Phase 4 — Deletion

After receiving and reviewing the data, pursue deletion:
- If combined request was used, deletion was already requested in Part II
- If standalone DSAR was used, send deletion request now
- Company has 45 days to confirm deletion
- If refused, check for legitimate exemptions (legal retention obligations)
- If exemption seems dubious, escalate via demand letter → CPPA complaint

### Phase 5 — Ongoing Maintenance

**Weekly:** Check for overdue responses, send follow-ups, identify new services from user's recent activity.

**Monthly:** Full scan of email + bank statements for new services, check for CCPA/CPRA regulatory changes, produce status brief.

**Quarterly (90-Day Re-Request Cycle):** This is the critical step most people miss. Companies can re-collect your data after deletion through new purchases, cookies, third-party data feeds, or data onboarding. Run a full re-request cycle every 90 days.

The 90-day cycle works as follows:
1. **Check previous deletion confirmations** — pull every service where deletion was confirmed
2. **Generate re-request letters** for all of them, referencing the prior deletion and requesting affirmation that data remains deleted
3. **Send** — submit the re-request letters. These are shorter than initial DSARs: "You confirmed deletion on [date]. Please confirm my data remains deleted. If you've re-collected any, state the source and legal basis."
4. **Log the cycle** — the cycle number, date, and service list should be timestamped in a dedicated log
5. **Produce cycle report** — what was re-requested, due dates for responses

**Automation is essential here.** With 1,000+ services, manual re-requesting is not viable. Use the Automation Pipeline section below.

### Phase 6 — Full Rebuild (Annual)

Once per year:
- Repeat the full discovery process — you may have signed up for new services
- Re-run the data broker source aggregation (new brokers register/emerge constantly)
- Verify a sample set of 10-20 services are still honoring deletion by submitting a fresh DSAR
- Update all letter templates for regulatory changes

## Data Broker Source Aggregation

For the data broker segment of your registry, you can build a comprehensive master list from multiple open-source datasets rather than compiling from scratch.

### Available Open-Source Broker Datasets

| Source | Count | Format | Description |
|--------|-------|--------|-------------|
| **Optery** | ~960 | CSV (GitHub) | Open-source data broker directory with opt-out guides, tier ratings, and descriptions |
| **PersProtect** | ~500 | CSV (GitHub) | U.S. data broker opt-out list with opt-out links and categories |
| **OptOutRights Foundation** | ~1,000 | CSV (GitHub) | Broker directory with compliance scores, coverage data, and risk ratings |

All three are under open licenses. Download URLs (current as of mid-2026):
- Optery: `https://raw.githubusercontent.com/optery/optery-data-brokers-directory/master/data/data-brokers.csv`
- PersProtect: `https://raw.githubusercontent.com/Persprotect/data-broker-opt-out-list/main/data-brokers.csv`
- OptOutRights: `https://raw.githubusercontent.com/OptOutRights/brokerdirectory/refs/heads/main/data/brokers.csv`

### Deduplication Approach

Each dataset has different naming conventions, so deduplication requires two keys:

1. **Domain key** — Extract the root domain from the `website` field. This is the most reliable match (e.g., `acxiom.com` matches in all three sources).
2. **Normalized name** — Lowercase, strip corporate suffixes (`inc`, `llc`, `corp`, `ltd`, `technologies`, `solutions`), strip non-alphanumeric characters, collapse whitespace.

Priority order for field merging when conflicts arise:
1. Opt-out URL: prefer the most specific/direct URL
2. Privacy email: prefer the dedicated privacy@ address
3. Description: prefer the longest / most informative

### Merged Dataset

After deduplication, a typical merge yields ~1,800 unique brokers. The `scripts/privacy-pipeline.py` script (see Automation Pipeline below) includes the merge/dedup logic. This reference file (`references/data-broker-source-aggregation.md`) has the full Python merge script.

### Category Breakdown of Merged Brokers

| Category | Typical Count | Examples |
|----------|--------------|----------|
| People Search Sites | ~380 | Spokeo, Whitepages, BeenVerified, TruthFinder, Intelius |
| Marketing Data Brokers | ~280 | Acxiom, Epsilon, Oracle/BlueKai, LiveRamp, Criteo |
| B2B Lead Generation | ~130 | ZoomInfo, Apollo, Seamless, Lusha, Clearbit |
| Business Search | ~70 | Crunchbase, Dun & Bradstreet, DataFox |
| Profile Data Brokers | ~45 | FullContact, Pipl, PeekYou |
| Credit & Financial | ~25 | Equifax, Experian, TransUnion, LexisNexis, ChexSystems |
| Phone Directory | ~35 | 411.com, AnyWho, Whitepages (reverse) |
| Background Check | ~20 | Checkr, GoodHire, HireRight, First Advantage |

The remaining ~850 fall under "Unknown/Misc" and need manual categorization.

## Email + Addressing Strategy

For tracking which service each request goes to, use **email + addressing** — a Gmail feature where `you+tag@gmail.com` routes to your inbox but creates a unique address per service.

**Pattern:** `[base]+[company-short]@gmail.com`

Example: `youraccount2+equifax@gmail.com`, `youraccount2+acxiom@gmail.com`

This is invaluable for:
- **Reply tracking** — responses to `+equifax` go into their own folder/filter
- **Proof of submission** — each email has a unique address proving it was sent to that specific company
- **Bounce detection** — if `+chexsystems` bounces, you know that company's email system rejected it
- **Automated filtering** — set up Gmail filters to auto-label/categorize responses by tag

## Personal Info Config Pattern

Never hardcode personal information (name, address, phone, DOB, email) in scripts. Use a separate YAML config file that scripts load:

```yaml
# personal_config.yaml
personal_info:
  full_name: "the operator M Backus"
  email_base: "<your-email>@gmail.com"
  phone: "[PHONE NUMBER]"
  address: "89 Saratoga Rd"
  city_state_zip: "your city, NY 12302"
  dob: "11/03/1989"
```

Scripts read this config and auto-fill letters, using the base email to generate +addressed addresses per company. This:
- Keeps sensitive info out of script code
- Makes it trivial to regenerate all letters after an address/phone change
- Allows the same pipeline to be reused for different people by swapping the config

## Manual Targets (Not in Any Broker Dataset)

Several critical financial/identity services are **not** listed in any of the three open-source broker datasets (Optery, PersProtect, OptOutRights). These must be added manually:

| Service | Contact | What They Hold |
|---------|---------|---------------|
| **ChexSystems** | consumerdept@chexsystems.com | Banking history — closed accounts, bounced checks |
| **Early Warning Services (Zelle)** | privacy@earlywarning.com | Shared banking intel among major US banks |
| **TeleCheck** | privacy@fisglobal.com | Check writing verification history |
| **Certegy** | privacy@certegy.com | Check verification services |
| **MIB Group** | privacy@mib.com | Medical underwriting data for life/health insurance |
| **Milliman IntelliScript** | privacy@milliman.com | Prescription drug history used by insurers |
| **Verisk / ISO** | privacy@verisk.com | Insurance claims history (CLUE reports) |
| **CoreLogic** | privacy@corelogic.com | Property records, rental history, credit risk |
| **ARIS** | privacy@aris.com | Tenant screening and rental history |

See `references/manual-financial-targets.md` for full contact details and FCRA disclosure instructions for these.

## Batch Generation (Mail-Merge) Approach

Generating letters one-at-a-time is too slow for 1,800+ brokers. Use a mail-merge pattern instead:

1. **Config:** `personal_config.yaml` — personal info (name, address, DOB, email base)
2. **Dataset:** `merged_brokers.csv` — 1,800+ brokers with names, types, websites, privacy emails, opt-out URLs
3. **Batch script:** Reads config + CSV, generates filled-in letters for all or a subset

```bash
# Generate all 1,837 letters at once
python3 batch_generate.py --priority all

# Or by priority tier
python3 batch_generate.py --priority credit    # Credit bureaus
python3 batch_generate.py --priority people    # People search sites
python3 batch_generate.py --priority marketing # Marketing/B2B
```

Each letter is saved to `services/[company-name]/001-combined-request.txt` with:
- [FILL IN] replaced with actual personal info
- Email + addressed (`base+company@...`)
- CCPA/CPRA statutory citations
- 10-day acknowledgment and 45-day response deadlines
- Non-compliance penalty notice

The full batch-generator script is saved as `scripts/batch-generate.py` in this skill.

## Pre-Commit Verification Pattern

When batch-generating letters or updating pipeline scripts, run a quick verification before committing:

```bash
# Verify all scripts parse correctly
python3 -c "
import ast, os, yaml
for f in ['batch_generate.py', 'privacy_pipeline.py', 're_request_cycle.py']:
    with open(f) as fh: ast.parse(fh.read())
    print(f'OK: {f}')
# Verify config loads
with open('personal_config.yaml') as fh: yaml.safe_load(fh)
print('OK: personal_config.yaml')
# Verify CSV is readable
import csv
with open('merged_brokers.csv') as fh: rows = list(csv.DictReader(fh))
print(f'OK: merged_brokers.csv ({len(rows)} records)')
# Spot-check a generated letter
with open('services/equifax/001-combined-request.txt') as fh:
    txt = fh.read()
    assert 'the operator M Backus' in txt
    assert '+equifax@gmail.com' in txt
print('OK: sample letter content correct')
"
```

This catches syntax errors, missing config fields, CSV parse failures, and content generation bugs before they get committed.

## Pre-Commit Verification Pattern

Before committing any batch of generated letters or pipeline updates, run a quick structural verification:

```bash
# Verify all scripts parse correctly
python3 -c "
import ast, os, yaml
for f in ['batch_generate.py', 'listener.py', 'auto_responder.py',
          'execute_all.py', 'sync_registry.py', 'privacy_pipeline.py',
          're_request_cycle.py']:
    with open(f) as fh: ast.parse(fh.read())
    print(f'OK: {f}')
# Verify config loads
with open('personal_config.yaml') as fh: yaml.safe_load(fh)
print('OK: personal_config.yaml')
# Verify CSV is readable
import csv
with open('merged_brokers.csv') as fh: rows = list(csv.DictReader(fh))
print(f'OK: merged_brokers.csv ({len(rows)} records)')
# Spot-check a generated letter
with open('services/equifax/001-combined-request.txt') as fh:
    txt = fh.read()
    assert 'the operator M Backus' in txt
    assert '+equifax@gmail.com' in txt
print('OK: sample letter content correct')
"
```

This catches syntax errors, missing config fields, CSV parse failures, and content generation bugs before they get committed. Run it as the last step before `git add` and `git commit`.

## Automation Pipeline

With 1,000+ services, manual tracking is not viable. Use a CLI automation engine.

### Core Script: `privacy-pipeline.py`

This script (saved as `scripts/privacy-pipeline.py` in this skill) provides:

```bash
python3 privacy_pipeline.py status              # Show current stats
python3 privacy_pipeline.py search "acxiom"      # Search brokers by name
python3 privacy_pipeline.py generate --service N  # Generate DSAR letter for broker N
python3 privacy_pipeline.py send --service N      # Mark as sent
python3 privacy_pipeline.py receive --service N   # Mark data received
python3 privacy_pipeline.py delete --service N    # Mark deletion confirmed
python3 privacy_pipeline.py next-batch 5          # Next 5 brokers to process
python3 privacy_pipeline.py report                # Generate full status report
python3 privacy_pipeline.py help                  # Show all commands
```

### Batch Generator: `batch-generate.py`

For mass letter generation using mail-merge from config + CSV:

```bash
python3 batch_generate.py --priority credit     # 11 credit bureau letters
python3 batch_generate.py --priority people     # 25 people search letters
python3 batch_generate.py --priority marketing  # 26 marketing/B2B letters
python3 batch_generate.py --priority all        # ALL 1,837 brokers
python3 batch_generate.py --service "Acxiom"    # Single service
```

The batch generator reads `personal_config.yaml` for PI and `merged_brokers.csv` for broker data, uses email + addressing, and fills in every field of the letter including statutory citations and deadlines.

### 90-Day Re-Request Script: `re-request-cycle.py`

```bash
python3 re_request_cycle.py --dry-run   # Preview without sending
python3 re_request_cycle.py             # Execute the 90-day cycle
```

### Automated Inbox Monitoring (`listener.py`)

An IMAP inbox scanner that polls Gmail for CCPA/CPRA response emails. Runs every 30 minutes via cron.

```bash
python3 listener.py --once      # Single scan
python3 listener.py --daemon    # Continuous polling (every 30min)
```

**What it does:**
1. Connects to Gmail IMAP (requires App Password)
2. Searches for emails from known broker domains (1,800+ in the merged catalog)
3. Also catches CCPA-related keywords (privacy, DSAR, deletion, opt-out)
4. Classifies each response:
   - `ACKNOWLEDGMENT` — company acknowledged receipt
   - `DATA_RECEIVED` — data package arrived
   - `DELETION_CONFIRMED` — company confirmed deletion
   - `BOUNCE` — email bounced (update contact info)
   - `NEEDS_ATTENTION` — identity verification or denial
   - `FOLLOWUP_NEEDED` — time-sensitive second notice
   - `UNKNOWN` — needs manual review
5. Logs all matches to `logs/listener-YYYY-MM-DD.csv`
6. Generates an alert summary for urgent items

**Setup:**
1. Enable 2FA on Google account
2. Generate an App Password at https://myaccount.google.com/apppasswords
3. Copy `.env.template` to `.env` and fill in the password
4. The cron job `ccpa-inbox-listener` handles the rest

**Secrets pattern:** Never put the app password in script code. Use a `.env` file (gitignored) with `.env.template` as the committed placeholder:

```
EMAIL_ADDRESS=<your-email>@gmail.com
EMAIL_PASSWORD=YOUR_16_CHAR_APP_PASSWORD_HERE
```

### Auto-Responder (`auto_responder.py`)

A deadline-aware follow-up engine that monitors the statutory timeline and sends escalation emails when companies miss deadlines.

```bash
python3 auto_responder.py --check      # Check overdue deadlines
python3 auto_responder.py --send       # Send pending follow-up emails
python3 auto_responder.py --report     # Generate escalation report
```

**Timeline it enforces:**

| Day | Threshold | Action |
|-----|-----------|--------|
| 10 | No acknowledgment | Send follow-up demand |
| 45 | No data received | Send data-demand follow-up |
| 60 | No deletion | Mark as CPPA complaint candidate |
| 90 | Still noncompliant | File CPPA complaint |

It reads the action log, determines which services are overdue, generates the appropriate follow-up letter, and sends it via SMTP (Gmail). All actions are logged for audit trail.

### Bulk Execution & Registry Sync

**`execute_all.py`** — After generating letters, this script marks all of them as SENT in the action log, populates TRACKER.md with submission dates and 45-day deadlines, and updates REGISTRY.md statuses.

```bash
python3 execute_all.py
```

**`sync_registry.py`** — Reconciles REGISTRY.md with the action log. Adds new service categories for data broker targets, updates quick stats, and flags any gaps.

```bash
python3 sync_registry.py
```

### Cron Schedule for Automation

Set up three cron jobs covering the full lifecycle:

| Job | Schedule | Purpose |
|-----|----------|---------|
| `ccpa-inbox-listener` | **Every 30 minutes** | Polls Gmail for CCPA responses, classifies, alerts on urgent items |
| `ccpa-auto-responder-daily` | **Daily at 10AM** | Checks statutory deadlines, sends follow-up emails for overdue services |
| `legal-data-privacy-weekly` | **Monday at 9AM** | Full pipeline review with EXECUTION authority — sends follow-ups, generates status brief, commits pipeline state |

The weekly cron is the most important: it has full execution authority and should be configured to take action, not just report. It runs the auto-responder check, processes any overdue items, generates a brief, and commits the pipeline state to git.

Example cron creation:
```bash
hermes cron create --name ccpa-inbox-listener --schedule "30m" --prompt "..." --workdir /path/to/data-privacy
hermes cron create --name ccpa-auto-responder-daily --schedule "0 10 * * *" --prompt "..."
hermes cron create --name legal-data-privacy-weekly --schedule "0 9 * * 1" --prompt "..." --workdir /path/to/data-privacy
```
## Filing Complaints

When a business refuses to comply, file with:

| Authority | Jurisdiction | Link |
|-----------|-------------|------|
| California Privacy Protection Agency | State (CCPA/CPRA) | privacy@cppa.ca.gov |
| California Attorney General | State (CCPA) | oag.ca.gov (web form) |
| Federal Trade Commission | Federal (Section 5) | reportfraud.ftc.gov |

### Skill Linked Files

This skill includes:
- `references/ccpa-letter-templates.md` — 6 ready-to-send CCPA/CPRA letter templates
- `references/service-category-checklist.md` — Discovery checklist for all service categories
- `references/data-broker-source-aggregation.md` — How to download, merge, and deduplicate broker datasets from 3 open sources into a master list of ~1,800 brokers
- `scripts/privacy-pipeline.py` — CLI automation engine for pipeline management (generate, send, track, report, re-request)

## Documentation Standards

Everything must be saved for potential litigation:

**File structure per service:**
```
services/[service-name]/
├── 001-dsar-request.txt
├── 002-company-response.md
├── 003-deletion-confirmation.md
├── evidence/
│   ├── privacy-portal-confirmation.png
│   └── response-email.pdf
└── findings.md
```

**Master registry structure:**
A living table tracking all services with fields:
- Service name, category, data held
- CCPA status (🔴 Not Started → 🟡 DSAR Sent → 🟢 Data Received → 🔵 Deletion Requested → ✅ Confirmed → ⚠️ Dispute)
- Dates: DSAR sent, data received, deletion requested, deletion confirmed
- Notes (interesting findings, data value, litigation potential)

## Per-Service Correspondence Directory

When setting up this pipeline, create:
```
counsel-lead/data-privacy/
├── REGISTRY.md          # Master inventory with status tracking
├── TEMPLATES.md         # 6 CCPA/CPRA letter templates
├── TRACKER.md           # Submission log + enforcement timeline
├── PROCESS.md           # Full SOP (this document's extended version)
└── services/            # Per-service correspondence folders
    └── [service-name]/
```

## Key Deadlines

| Deadline | What's Due | Starts From |
|----------|-----------|-------------|
| 10 calendar days | Business acknowledges request | Request date |
| 45 calendar days | Business provides data/confirms deletion | Request date |
| 90 calendar days | Absolute maximum with extension | Request date |
| 12 months | Cooldown before next free request | Previous request |

## Escalation Path

| Event | Action |
|-------|--------|
| Company refuses DSAR | Send follow-up demand letter → CPPA complaint |
| Company refuses deletion | Send follow-up demand letter → CPPA complaint |
| Interesting/surprising data found | Catalog findings for potential litigation value |
| Company willfully violates CCPA | Document pattern, consult legal counsel |
| Data breach discovered | Immediate notification to user and affected parties |

## Pitfalls

- **Combined requests are preferred** — sending DSAR and deletion separately doubles the timeline. The combined request gives the business 45 days to provide data AND confirm deletion.
- **Identity verification** — companies will ask for identity verification. Respond promptly to avoid the 45-day clock being paused.
- **12-month window** — companies can deny a second request within 12 months. Make the first request count.
- **Extension trap** — businesses can extend by 45 days only if they notify you AND state the reason. If they don't notify you, the original 45-day clock runs.
- **Data broker vs. general service** — people-search sites (MyLife, Spokeo, etc.) have their own opt-out flow covered by the `hermes-legal-watchdog` reputation management skill. This skill covers the broader set of consumer-facing services.
- **HIPAA overlay** — healthcare providers may claim HIPAA preempts CCPA for medical records. Accept the exemption but document it; you can still pursue non-medical data.
- **Email deliverability** — privacy@ emails can bounce or go to spam. Always save a copy in the outbox and set a calendar reminder to follow up if no ack in 10 days.
- **Data broker re-collection** — data brokers can re-acquire your data from public records, data exchanges, or partner feeds even after deletion. This is why the 90-day re-request cycle exists. Treat deletion as a recurring maintenance task, not a one-time event.
- **Credit freeze before action** — if you submit deletion requests to credit bureaus without freezing first, they may still process new account applications during the processing window. Always freeze first, then DSAR, then delete.
- **Google is a multi-month process** — Takeout archives can take days to prepare, and full data deletion from Google can take 2-3 months. Start the Takeout export well before any external deadline.
