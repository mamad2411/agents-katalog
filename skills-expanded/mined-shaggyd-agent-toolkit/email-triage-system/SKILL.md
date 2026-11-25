---
name: email-triage-system
description: Two-layer Gmail triage system — zero-LLM noise archiving (Janitor) + LLM-powered daily review (Reviewer) — keeps your inbox clean with minimal config
version: 1.0.0
author: Dustin Chadwick (@ShaggyD)
tags: [gmail, triage, inbox-zero, janitor, review, productivity]
---

# Email Triage System

A two-layer email triage pipeline that separates noise from signal with zero ongoing cognitive load.

**Layer 1 — The Janitor** is a zero-LLM-cost CLI cron job that batch-archives known noise (promos, social, newsletters, notifications) every 15 minutes using Gmail API pattern matching. It builds a growing noise-sender database and logs summaries.

**Layer 2 — The Reviewer** is an agent profile that reads the Janitor's logs once daily, applies LLM reasoning to the remaining non-bulk email, and surfaces a clean triage summary with categories and escalations.

**Key constraint:** Zero new OAuth setup — reuse your existing Gmail API token. No LLM calls for the Janitor. Existing label conventions are the source of truth for noise classification.

---

## Architecture

```
┌─────────────────────────────┐
│         Gmail Inbox         │
│  (noise + real email)       │
└──────────┬──────────────────┘
           │  poll every 15 min
           ▼
┌─────────────────────────────┐
│  Layer 1: The Janitor (CLI) │  ← zero LLM cost
│  Pattern matching engine    │
│  Noise-sender database      │
│  Safe-sender allowlist      │
│  Batch archive via API      │
└──────────┬──────────────────┘
           │  structured JSON logs
           ▼
┌─────────────────────────────┐
│  Layer 2: The Reviewer      │  ← LLM-powered, daily
│  (Agent profile)            │
│  Reads Janitor logs         │
│  Fetches remaining inbox    │
│  LLM categorization         │
│  Action items & escalations │
└──────────┬──────────────────┘
           │  structured daily brief
           ▼
┌─────────────────────────────┐
│     Daily Triage Brief      │
│  (terminal, Discord, chat)  │
└─────────────────────────────┘
```

---

## Layer 1: The Janitor (CLI Tool)

### How It Works

1. Scans your Gmail inbox every N minutes (configurable, default 15) via cron
2. Matches emails by sender address + subject-line keywords against a noise-sender database
3. Batch-archives matched emails using Gmail API `modify()` with `removeLabelIds: ['INBOX']` + optional category label
4. Skips emails from safe-sender allowlist
5. Logs structured JSON to a configurable log directory
6. Supports `--dry-run` for safe validation

### Setup

#### 1. Prerequisites

```bash
# Python 3.10+
python --version

# Gmail API credentials
# You need a Google Cloud project with Gmail API enabled
# and OAuth 2.0 credentials (Desktop Application type)
# saved at a known path (default: ~/.google/gmail-token.json)
```

#### 2. Gmail API Authentication

Follow the setup in `references/gmail-api-setup.md` to:
- Create a Google Cloud project
- Enable the Gmail API
- Configure the OAuth consent screen
- Download credentials and generate a refresh token

#### 3. Configuration

Copy the template configuration:

```bash
mkdir -p ~/.config/email-janitor
cp templates/config.yaml ~/.config/email-janitor/config.yaml
cp templates/noise-senders.yaml ~/.config/email-janitor/noise-senders.yaml
cp templates/safe-senders.yaml ~/.config/email-janitor/safe-senders.yaml
```

Edit `config.yaml` to set your:
- Gmail credentials path
- Noise-sender database path
- Safe-sender path
- Log directory
- Check interval (used by cron, not by the tool itself)

#### 4. Cron Setup

Add a 15-minute cron entry:

```bash
crontab -e
# Add:
*/15 * * * * cd /path/to/email-janitor && python janitor.py >> ~/.config/email-janitor/logs/cron.log 2>&1
```

### Usage

```bash
# Normal run — archives noise
python janitor.py

# Dry run — shows what would be archived, no mutations
python janitor.py --dry-run

# Custom config path
python janitor.py --config ~/.config/email-janitor/config.yaml

# Custom credential path
python janitor.py --creds /path/to/gmail-token.json
```

### Configuration Reference

**`config.yaml`:**
```yaml
# Gmail API
credentials_path: ~/.google/gmail-token.json
# Use existing token file — the tool handles token refresh

# Noise-sender database
noise_db_path: ~/.config/email-janitor/noise-senders.yaml

# Safe-sender allowlist
safe_senders_path: ~/.config/email-janitor/safe-senders.yaml

# Logging
log_dir: ~/.config/email-janitor/logs
log_format: jsonl  # jsonl or text

# Labels
# The Janitor applies existing labels before removing from INBOX.
# Set to false to archive without labeling.
apply_labels: true

# Behavior
batch_size: 50        # Gmail API batch size
rate_limit_rps: 5     # Requests per second (respect Gmail quota)
```

**`noise-senders.yaml`:** See the template in `templates/noise-senders.yaml`. Categories include:
- `promotions` — marketing, promos, deals, flash sales
- `newsletters` — regular digests, newsletter platforms
- `social` — social platform notifications
- `services` — transactional/account emails (accounting, cloud, dev tools)
- `security` — security alerts (detected but NOT archived, logged for Reviewer)

**`safe-senders.yaml`:** List of email addresses or domains that are NEVER touched. Support glob patterns.

### Output Format (JSONL)

Each run produces a JSONL file with one line per batch operation:

```json
{"timestamp": "2026-05-23T10:15:00Z", "total_processed": 42, "archived": 38, "skipped_safe": 3, "security_logged": 1, "categories": {"promotions": 12, "newsletters": 15, "social": 8, "services": 3}, "errors": [], "duration_seconds": 4.2}
```

---

## Layer 2: The Reviewer (Agent Profile)

### How It Works

1. Runs once daily (configurable schedule)
2. Reads the latest Janitor log to see what was archived
3. Fetches remaining inbox emails (those NOT caught by Janitor)
4. Applies LLM reasoning to categorize each email into one of four categories:
   - `action_required` — needs a response or task
   - `important_read` — worth reading carefully
   - `worth_flagging` — notable but not urgent
   - `fyi` — informational, no action needed
5. Respects the same safe-sender allowlist
6. Produces a structured review JSON and a human-readable markdown brief

### Setup

#### 1. Create an Agent Profile

This skill works with any agent platform. For Hermes Agent:

```bash
# Create profile directory
mkdir -p ~/.hermes/profiles/email-reviewer/
# Copy SOUL.md from templates
cp templates/reviewer-soul.md ~/.hermes/profiles/email-reviewer/SOUL.md
```

#### 2. Configure the Cron

```bash
# Daily at 06:00
0 6 * * * cd /path/to/email-reviewer && python reviewer.py >> ~/.config/email-janitor/logs/reviewer-cron.log 2>&1
```

### Output

**Structured review JSON:**
```json
{
  "date": "2026-05-23",
  "total_reviewed": 8,
  "categories": {
    "action_required": 2,
    "important_read": 3,
    "worth_flagging": 1,
    "fyi": 2
  },
  "action_items": [
    {"subject": "Q3 Budget Approval Needed", "from": "finance@company.com", "suggested_reply": "Will review and approve by EOD"}
  ],
  "escalations": [
    {"subject": "Security Alert: New Login", "from": "security@cloudflare.com", "priority": "high"}
  ],
  "safe_sender_emails": 1,
  "janitor_log_ref": "2026-05-23T10-15-00.jsonl"
}
```

**Human-readable brief (markdown):**
```markdown
## Daily Email Triage — 2026-05-23

### Action Required (2)
- **Q3 Budget Approval Needed** — finance@company.com
  → Suggested: Will review and approve by EOD
- **Client Meeting Confirmation** — alice@clientco.com
  → Suggested: Confirmed, see you Tuesday at 2pm

### Important (3)
- Platform migration status update from engineering
- New feature proposal from product team
- Weekly analytics digest

### Worth Flagging (1)
- Conference CFP deadline extension

### Escalations ⚠️
- **Security Alert: New Login** — from Colorado IP (approved device)

### Stats
- 38 emails archived by Janitor
- 8 emails reviewed
- 2 require action
```

---

## Noise-Sender Categories

### promotions
Sender domains matching known marketing platforms OR subject contains promo keywords (`sale`, `discount`, `offer ends`, `coupon`, `% off`, `flash sale`, `limited time`).

Common platforms: sendgrid.net, mailchimp.com, constantcontact.com, hubspot.com, klaviyo.com, braze.com, iterable.com

### newsletters
Regular digests from content platforms and newsletter services.

Common platforms: substack.com, medium.com, ghost.io, convertkit.com, buttondown.email, beehiiv.com
Content platforms: youtube.com, reddit.com, pinterest.com

### social
Notifications from social platforms.

Platforms: twitter.com, x.com, linkedin.com, facebook.com, instagram.com, tiktok.com, threads.net, discord.com, slack.com

### services
Transactional/account emails from cloud platforms, dev tools, productivity apps, and finance services.

Examples: aws.*, gcp.*, vercel.com, github.com (non-security), notion.so, stripe.com

### security
Security alerts — detected but NOT archived. Passed through to the Reviewer for prioritization.

Patterns: security@, alert@, alerts@ for major platforms. Subject lines containing `security alert`, `new sign-in`, `password changed`, `2FA`, `verification code`.

---

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|-------------|
| **Noise capture rate** | >=90% of known-category noise within interval | Spot-check inbox vs logs over 7 days |
| **False-positive rate** | <1% of archived emails | Manual audit of first 500 archived emails |
| **Cron reliability** | 100% of scheduled runs execute without error over 30 days | Cron log + Janitor log integrity check |
| **Zero LLM cost (Janitor)** | $0.00 in API spend | Billing + token usage report |
| **Review coverage** | 100% of non-bulk inbox emails reviewed each cycle | Count in review JSON vs inbox diff |
| **Brief readiness** | Brief is actionable without re-reading source emails | User satisfaction |

---

## Files

| File | Purpose |
|------|---------|
| `janitor.py` | Zero-LLM Gmail noise archiving CLI script |
| `SKILL.md` | This document |
| `README.md` | Quick-start guide |
| `templates/config.yaml` | Janitor configuration template |
| `templates/noise-senders.yaml` | Noise-sender database with seed patterns |
| `templates/safe-senders.yaml` | Safe-sender allowlist template |
| `templates/reviewer-soul.md` | Agent profile SOUL.md template for Reviewer |
| `references/gmail-api-setup.md` | Gmail API OAuth setup guide |
| `references/label-conventions.md` | Label hierarchy conventions |
| `references/troubleshooting.md` | Common issues and fixes |

---

## Requirements

- Python 3.10+
- Gmail API enabled Google Cloud project
- OAuth 2.0 credentials for Desktop Application
- Cron (Linux/macOS) or Task Scheduler (Windows)

## License

MIT — use freely, adapt openly, attribute where meaningful.

---

*Maintained by Dustin "Dusty" Chadwick (@ShaggyD)*
