---
name: product-updates-digest
description: "Generate a weekly digest of Databricks project-updates@ mailing list emails. Reads all project update emails from the past week, categorizes features by maturity stage (GA/Preview/Beta/Private Preview/Coming Soon), identifies SA action items and customer opportunities, and sends a concise digest email. Use when the user says 'project updates', 'product updates digest', 'what shipped this week', 'feature updates', 'weekly product digest', or wants a summary of Databricks product changes."
user-invocable: true
---

# Product Updates Digest

Reads project-updates@databricks.com emails from the past week, categorizes features by maturity stage (GA, Public Preview, Beta, Private Preview, Coming Soon), identifies SA action items and customer opportunities, and sends a formatted digest email with clickable Gmail links to the original update threads.

## Quick Start

```
"Summarize this week's project updates and send me a digest"
"What Databricks features shipped this week? Email me a digest"
"Create a product updates digest for the last 2 weeks and send to my team"
"Generate a weekly product digest and include opportunities for Acme Corp"
```

## Prerequisites

- **Google Auth** — run `/google-auth` first (Gmail read + send scopes)

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `recipients` | **Yes** | — | One or more email addresses to send the digest to |
| `accounts` | No | — | Customer account names for opportunity matching (e.g., "Acme Corp, BigBank") |
| `mailing_list` | No | `project-updates.databricks.com` | Mailing list address to search |
| `lookback_days` | No | `7` | Number of days to look back for emails |

## Workflow

### Step 1: Authenticate with Google

Run the Google Auth skill to ensure Gmail access:

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py status
```

If not authenticated:

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py login
```

### Step 2: Search Gmail for Project-Updates Emails

Use the Gmail skill's `gmail_builder.py` to search for mailing list emails within the lookback window.

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_builder.py \
  search --query "list:project-updates.databricks.com newer_than:7d" --max-results 100
```

If more than 100 results, paginate using the `nextPageToken` returned by the API until all messages are collected.

For each message returned, record:
- **Message ID** — needed for reading content and building Gmail hyperlinks
- **Thread ID** — for grouping originals vs. replies
- **Subject** — the email subject line
- **Date** — when the email was sent

**Distinguishing originals from replies:**
- Replies have subjects prefixed with `Re:` or `Fwd:`
- Within a thread, the first message (earliest date) is the original
- Track both, but only originals appear in the "Original Emails Index" at the bottom of the digest

**Gmail hyperlinks** for each message use this format:
```
https://mail.google.com/mail/u/0/#inbox/{MESSAGE_ID}
```

### Step 3: Read and Extract Content

Read each email to extract its full content:

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_builder.py \
  read-message --message-id "MESSAGE_ID"
```

From each email, extract:
- **Feature name** — the product or feature being announced
- **Status / maturity stage** — GA, Public Preview, Beta, Private Preview, Coming Soon, or Change/Deprecation
- **Timeline** — any dates or version targets mentioned
- **Risks** — breaking changes, migration requirements, deprecation deadlines
- **Key details** — summary of what changed and why it matters

### Step 4: Categorize and Analyze

Group extracted features into the following maturity stages (in this order):

1. **GA (Generally Available)** — production-ready, fully supported, SLA-backed
2. **Public Preview** — available to all customers, not yet production-hardened
3. **Beta** — early-stage, experimental, may change significantly
4. **Private Preview** — gated access, customers must enroll or be nominated
5. **Coming Soon** — announced on a roadmap but not yet available

Additionally identify:

- **Feature Changes / Deprecations** — breaking changes, API removals, migration timelines, behavioral changes that could impact existing workloads
- **SA Action Items** — for each update, assess:
  - Which customers could benefit from this feature?
  - Are there proactive outreach opportunities (e.g., a customer asked for this)?
  - Are there risks to flag (e.g., deprecation affecting a customer's current setup)?

If the user provided `accounts`, match action items against those specific accounts. Otherwise, describe opportunities generically (e.g., "customers using Feature X").

### Step 5: Build HTML Email (Locked Format)

Construct the digest email as HTML. The template below is **locked** — follow it exactly for consistency across weekly digests.

**Overall structure:**

```
┌─────────────────────────────────────────────┐
│  Header bar (#1B3A4B dark blue)             │
│  "Databricks Product Updates Digest"        │
│  Week of {start_date} – {end_date}          │
│  {N} updates from project-updates@          │
├─────────────────────────────────────────────┤
│  TL;DR box (#E3F2FD light blue)             │
│  3-5 bullet executive summary               │
├─────────────────────────────────────────────┤
│  SA Action Items table (#FFEBEE light red)  │
│  Action | Related Feature | Customer Opp    │
│  | Timeline                                 │
├─────────────────────────────────────────────┤
│  GA table (#E8F5E9 green header)            │
├─────────────────────────────────────────────┤
│  Public Preview table (#FFF3E0 orange)      │
├─────────────────────────────────────────────┤
│  Beta table (#E3F2FD blue)                  │
├─────────────────────────────────────────────┤
│  Private Preview table (#F3E5F5 purple)     │
├─────────────────────────────────────────────┤
│  Coming Soon table (#ECEFF1 gray)           │
├─────────────────────────────────────────────┤
│  Changes & Deprecations (#FFF8E1 yellow)    │
│  (only if any exist)                        │
├─────────────────────────────────────────────┤
│  Original Emails Index                      │
│  (subjects hyperlinked to Gmail, originals  │
│   only — no replies)                        │
├─────────────────────────────────────────────┤
│  Footer                                     │
└─────────────────────────────────────────────┘
```

**Section details:**

**Header bar:**
- Background: `#1B3A4B`; text: white; padding: 20px
- Title: "Databricks Product Updates Digest"
- Subtitle: "Week of {Mon date} – {Sun date} · {N} updates from project-updates@"

**TL;DR box:**
- Background: `#E3F2FD`; border-left: 4px solid `#1565C0`; padding: 16px
- 3-5 bullet points summarizing the most impactful updates of the week
- Focus on what matters most to SAs and their customers

**SA Action Items table:**
- Header background: `#FFEBEE` (light red); border: 1px solid `#EF9A9A`
- Columns: **Action** | **Related Feature** | **Customer Opportunity** | **Timeline**
- Each row is a concrete action an SA should take (e.g., "Reach out to customers using Serverless SQL about new auto-scaling behavior")

**Feature tables by maturity stage:**
Each stage gets its own table with a colored header row. Columns: **Feature** | **Summary** | **Key Details** | **Timeline**

| Stage | Header Color | Text |
|-------|-------------|------|
| GA | `#E8F5E9` (green) | `#2E7D32` |
| Public Preview | `#FFF3E0` (orange) | `#E65100` |
| Beta | `#E3F2FD` (blue) | `#1565C0` |
| Private Preview | `#F3E5F5` (purple) | `#6A1B9A` |
| Coming Soon | `#ECEFF1` (gray) | `#37474F` |

**Omit any maturity stage section that has zero items.**

**Changes & Deprecations table:**
- Only include if there are any changes or deprecations
- Header background: `#FFF8E1` (yellow); text: `#F57F17`
- Columns: **Change** | **Impact** | **Migration Deadline** | **Action Required**

**Original Emails Index:**
- List only original emails (not replies/forwards)
- Each entry: date + subject hyperlinked to the Gmail message
- Format: `{date} — <a href="https://mail.google.com/mail/u/0/#inbox/{MESSAGE_ID}">{subject}</a>`
- Sorted by date, newest first

**Footer:**
- Light gray text, small font
- "Generated by Vibe · product-updates-digest skill"

### Step 6: Send Email

Send the HTML digest using `gmail_builder.py`:

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_builder.py \
  send \
  --to "recipient1@databricks.com" \
  --cc "recipient2@databricks.com" \
  --subject "Databricks Product Updates Digest — Week of {date_range}" \
  --html "$(cat /tmp/product_digest.html)"
```

If the HTML is too large for a command-line argument, write it to a temp file and use:

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_builder.py \
  send \
  --to "recipient@databricks.com" \
  --subject "Databricks Product Updates Digest — Week of {date_range}" \
  --html-file /tmp/product_digest.html
```

After sending, confirm to the user:
- Number of updates categorized
- Number of action items identified
- Recipients the digest was sent to
- Link to the sent email in Gmail

## Scheduling

To receive this digest automatically every week, use the `fe-macos-scheduler` plugin:

```
"Schedule the product updates digest to run every Saturday and send to me"
```

This creates a local macOS launchd job that invokes the skill on the configured schedule.

## Tips

- If the mailing list has low volume, increase `lookback_days` to 14 to capture more updates
- Provide `accounts` to get personalized action items matched to your customers
- The digest groups by maturity stage so you can quickly scan what's production-ready vs. experimental
- Original email links let you click through to the full thread for details
