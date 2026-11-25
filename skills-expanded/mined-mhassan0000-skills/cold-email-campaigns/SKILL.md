---
name: cold-email-campaigns
description: Create cold email campaigns in Instantly from a client description and offers. Use when setting up outreach campaigns, cold email sequences, or automated email marketing.
allowed-tools: Read, Grep, Glob, Bash
---

# Cold Email Campaign Creator — Instantly Integration

## Goal
Take a client description and a few words about their offers, then create 3 cold email campaigns in Instantly. The script finds the 3 closest existing campaigns in your Instantly account, then minimally rewrites them for the new brand (5-10 word changes per email).

## Inputs
- **Client name**: The business name
- **Client description**: What they do, who they serve, their value proposition
- **Offers** (optional): Up to 3 distinct offers. If not provided, generates them from the description.
- **Target audience** (optional): Who we're emailing
- **Social proof** (optional): Credentials, results, experience to mention

## Process

### Step 1: Fetch Source Campaigns
The script fetches all existing campaigns from Instantly (via v2 API), then uses Claude to pick the 3 closest analogues based on offer structure, industry, and specificity.

### Step 2: Fetch Sequences
Full email sequences are pulled from the 3 selected source campaigns.

### Step 3: Minimal Rewrite
Claude rewrites each source campaign with **5-10 word changes only**:
- Swap brand name, industry noun, offer noun
- Keep same sentence structure, paragraph count, tone, and pacing
- Do NOT add new sentences, rephrase, or get creative

### Step 4: Run
```bash
python3 execution/instantly_create_campaigns.py \
  --client_name "ClientName" \
  --client_description "What the client does..." \
  --offers "Free audit|Demo session|Revenue share" \
  --target_audience "Agency owners, service businesses" \
  --social_proof "Built AI systems generating $1M+ in revenue"
```

### Step 5: Review (Dry Run)
```bash
python3 execution/instantly_create_campaigns.py \
  --client_name "Test" \
  --client_description "Test company" \
  --offers "Free thing" \
  --dry_run
```

## Campaign Structure
Each campaign (3 total) has exactly 2 steps:

**Email 1 (2 A/B variants):**
- Icebreaker
- Who you are + what you do (1-2 sentences)
- Clear offer with specifics
- Soft CTA

**Email 2 (follow-up, day 3):**
- 2-3 sentences max
- Restate the offer
- Low-pressure ask

## Hard Rules
- **No links or URLs in cold emails** — they get flagged as spam. Never use `{{web_site}}` or any URL variable.
- **Every email must state the offer** — no vague "would love to chat" without saying what you're offering.
- **Minimal rewrites only** — find-and-replace industry nouns, don't rewrite sentences.
- **Preserve source HTML** — keep `<p>`, `<div>`, `<br />` tags exactly as they are from the source.
- **2 steps only** — opener + 1 follow-up. No breakup emails.

## Available Variables
From Instantly's lead data:
- `{{firstName}}`, `{{lastName}}`, `{{email}}`
- `{{companyName}}`, `{{casualCompanyName}}`
- `{{icebreaker}}` — AI-generated opener
- `{{sendingAccountFirstName}}` — sender's name

## Environment
Requires in `.env`:
```
INSTANTLY_API_KEY=your_api_key
ANTHROPIC_API_KEY=your_anthropic_key
```

Both keys are always required (even for dry runs, since source campaigns are fetched from Instantly).

## Edge Cases
- **No offers provided**: Generates 3 distinct offers from client description
- **API rate limits**: Handled with retry after 30s
- **Missing API key**: Exits early with helpful error
- **Source campaign has 3+ steps**: Drops everything after step 2
- **Source campaign has links/URLs**: Claude removes them during rewrite

## First-Run Setup

Before executing, check if the workspace has a `.gitignore` file. If it doesn't, assume the user is new to this skill. In that case:

1. Ask the user if this is their first time running this skill
2. If yes, walk them through how it works and what they need to configure/set up (API keys, env vars, dependencies, etc.)
3. Let them know that Nick wishes them the best!
