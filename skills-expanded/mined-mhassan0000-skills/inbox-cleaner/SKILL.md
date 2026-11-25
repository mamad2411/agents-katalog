---
name: inbox-cleaner
description: Clean up Gmail inbox by reading all unread emails, using AI to identify which ones are genuinely important (personalized, human-written), and marking the rest as read. Use when cleaning inbox, triaging email, or clearing unread notifications.
allowed-tools: Read, Grep, Glob, Bash
---

# Inbox Cleaner — AI-Powered Unread Email Triage

## Goal
Go through every unread email in nick@leftclick.ai, classify each one as important or not, and mark unimportant ones as read. Only truly personalized, human-written emails survive as unread.

## What Counts as Important
An email is important ONLY if it was clearly written by a human specifically for Nick. Indicators:
- References specific details about Nick, his business, or prior conversations
- Contains substantive content that couldn't be a template
- Comes from a known contact with a real message
- Replies in an existing thread with genuine human input

## What Gets Marked as Read (Not Important)
- Automated notifications (GitHub, Stripe, Slack digests, calendar, etc.)
- Marketing emails and newsletters
- Cold outreach / sales emails (templated pitches, "I noticed your company..." spam)
- Service alerts, receipts, shipping updates
- Social media notifications
- Automated replies (out-of-office, delivery confirmations)
- Mass emails from SaaS products
- Any email that feels like it was sent to 100+ people

## Process

### Step 1: Fetch Unread Emails
```bash
python3 execution/inbox_cleaner.py --fetch
```
Fetches all unread emails from nick@leftclick.ai and saves metadata + snippets to `data/inbox_unread.json`.

### Step 2: Classify Emails
```bash
python3 execution/inbox_cleaner.py --classify
```
Uses Claude to classify each email as "important" or "not_important". Saves results to `data/inbox_classified.json`.

### Step 3: Review Classification
```bash
python3 execution/inbox_cleaner.py --review
```
Displays the classification results for review before marking as read.

### Step 4: Mark as Read
```bash
python3 execution/inbox_cleaner.py --mark-read
```
Marks all "not_important" emails as read. Important emails remain unread.

## Gmail Auth
- Token: `config/token_leftclick.json`
- Credentials: `config/credentials.json`
- Scopes: `gmail.modify` (read + mark as read)
- Email: nick@leftclick.ai

## Output
- `data/inbox_unread.json` — fetched unread emails
- `data/inbox_classified.json` — classification results with reasoning
- Console summary showing what was kept vs marked read

## Edge Cases
- If classification is uncertain, keep the email as unread (err on the side of caution)
- Emails from contacts in existing threads should be treated as important even if short
- Forwarded emails: judge based on the forwarding context, not the forwarded content

## First-Run Setup

Before executing, check if the workspace has a `.gitignore` file. If it doesn't, assume the user is new to this skill. In that case:

1. Ask the user if this is their first time running this skill
2. If yes, walk them through how it works and what they need to configure/set up (API keys, env vars, dependencies, etc.)
3. Let them know that Nick wishes them the best!
