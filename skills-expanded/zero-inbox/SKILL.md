# Zero Inbox - Triage Skill

```yaml
name: zero-inbox
description: >
  Triages unanswered Slack messages and unread emails. Fetches messages,
  filters for what needs a response, routes to domain-specific skills,
  and drafts replies. Goal: get to inbox zero efficiently.
triggers:
  - zero inbox
  - triage my inbox
  - check my messages
  - what needs my attention
```

---

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Slack | Read DMs and channel mentions, send replies |
| Gmail | Read unread emails, draft replies |

## Slack Triage Routine

### Step 1: Fetch Incoming Messages
Fetch all DMs and channel mentions from the last 10 days.
- Use the Slack MCP to read channels and DMs
- Focus on messages that mention the user or are direct messages to them
- Capture: sender, channel, timestamp, message content, thread context

### Step 2: Fetch Sent Messages
Fetch the user's own sent messages from the same time period.
- This is needed to identify which conversations are already handled
- Also fetch messages sent by designated proxies (e.g., co-CAO, EA) who may have replied on the user's behalf

### Step 3: Filter Unanswered
Compare incoming vs sent. A message is "unanswered" if:
- It was directed at the user (DM or @mention)
- Neither the user nor a designated proxy replied in that thread
- It contains a question, request, or action item (not just a reaction or FYI)
- It is not from a bot or automated notification

Skip messages that are:
- Already answered by the user or a proxy
- Pure informational (no response needed)
- From bots or integrations (unless they require action)
- Older than 10 days (flag these separately as "stale")

### Step 4: Present for Review
Present unanswered messages grouped by priority:

```
## Needs Response (X messages)

### High Priority
[Messages from important contacts, time-sensitive items, blockers]

### Normal Priority
[Standard questions, requests, follow-ups]

### Low Priority / FYI
[Nice-to-respond but not urgent]

### Stale (over 10 days)
[Messages that may need a "sorry for the delay" if still relevant]
```

For each message, show:
- Sender and channel
- Message preview (first 2 lines)
- Suggested action: reply / acknowledge / delegate / skip

### Step 5: Draft Replies
For each message the user wants to respond to:
- Load the email-writer skill for tone and formatting
- Read the full thread for context
- Draft a reply that matches the sender's energy and language
- Present the draft for user review before sending

---

## Email Triage Routine

### Step 1: Fetch Unread Emails
Fetch unread emails from the inbox.
- Use the email MCP (Gmail, Outlook, etc.)
- Capture: sender, subject, date, preview, labels/folders
- Sort by date (newest first)

### Step 2: Detect Domain
For each email, determine which domain it belongs to:

| Signal | Domain | Route To |
|--------|--------|----------|
| From a candidate, job board, or contains resume | HR | hr-screening skill |
| From a prospect, contains pricing/demo request | Sales | head-of-sales skill |
| From an existing customer, support request | Customer Success | customer-success skill |
| From an investor, board member, or financial | Finance | investor-update skill |
| From a partner, agency, or collaboration request | Partnerships | manual review |
| Internal team communication | Internal | reply directly |
| Newsletter, marketing, automated | Noise | archive or skip |
| Unknown or ambiguous | Other | present to user for routing |

### Step 3: Call Domain Skill
Route each email to the appropriate domain skill for handling:
- HR emails: load hr-screening skill for candidate evaluation
- Sales emails: load head-of-sales skill for pipeline management
- CS emails: load customer-success skill for follow-up drafting
- For all domains: the skill handles context gathering and draft creation

### Step 4: Act
For each email, take the appropriate action:

| Action | When |
|--------|------|
| **Draft reply** | The email needs a response. Draft via email-writer skill. |
| **Archive** | Newsletter, notification, or FYI that needs no action. |
| **Flag for user** | Requires a decision only the user can make. |
| **Delegate** | Can be handled by someone else. Note who and why. |
| **Snooze** | Not urgent, but needs attention later. Suggest a date. |

### Step 5: Summary
Present a summary at the end:

```
## Inbox Triage Complete

- Emails processed: [X]
- Replies drafted: [X] (awaiting your review)
- Archived: [X]
- Flagged for you: [X]
- Delegated: [X]
- Snoozed: [X]

### Drafts Ready for Review
[List each draft with recipient and one-line summary]

### Needs Your Decision
[List items that require user input]
```

---

## Domain Routing Map

| Domain | Skill | Trigger Signals |
|--------|-------|----------------|
| HR / Recruiting | `hr-screening` | Candidate names, job applications, interview scheduling, resume attachments |
| Sales / Pipeline | `head-of-sales` | Pricing questions, demo requests, prospect domains, CRM contacts |
| Customer Success | `customer-success` | Existing customer domains, support tickets, feature requests, renewal mentions |
| Finance / Investors | `investor-update` | Investor names, board meeting, financial reports, fundraising |
| Product / Engineering | `product-manager` | Bug reports, feature requests from internal team, GitHub notifications |
| Content / Marketing | `cmo` | Press inquiries, collaboration requests, podcast invites |
| Partnerships | Manual review | Agency outreach, co-marketing proposals, integration requests |
| Internal | `email-writer` | Team members, internal tools, calendar invites |
| Noise | Auto-archive | Newsletters, marketing blasts, automated notifications |

---

## Guardrails

1. **Never send a reply without user approval.** Always present drafts for review first.
2. **Never archive emails that might need a response.** When in doubt, flag for user.
3. **Never share email content across domains.** A customer email doesn't go to the sales skill.
4. **Respect language.** Match the language of the incoming message in replies.
5. **Flag sensitive items.** Legal threats, escalations, or anything unusual gets flagged immediately, not auto-drafted.
6. **Don't draft for strangers.** If the sender is unknown and the email looks suspicious, flag it rather than drafting a reply.
7. **Time-sensitive items first.** If something has a deadline within 24 hours, surface it at the top regardless of domain.
8. **Track patterns.** If the same type of email keeps coming in (e.g., repeated support questions), note it in `_insights.md` as a potential process improvement.

## Self-improvement

After the CAO reviews an inbox triage batch:

1. If the CAO overrides a classification (e.g. moves an email from "archive" to "urgent"), note the pattern in `admin/_insights.md`
2. If she changes a draft reply before sending, diff what was drafted vs what she sent - update the `email-writer` skill if the pattern is voice-related
3. If the routing table is wrong (e.g. a domain was assigned to the wrong agent), update the Domain Routing Map section
4. If new email patterns emerge (e.g. a new type of inbound that needs its own category), add them to the classification guide
