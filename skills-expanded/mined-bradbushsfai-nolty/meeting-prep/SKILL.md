---
name: meeting-prep
description: Prepare a comprehensive prep doc for any upcoming meeting — gathers prior notes, emails, company intel, news, and writes a strategic file to Obsidian (or wherever you keep notes). EXAMPLE — adapt to your own setup.
---

# Meeting Prep (example)

> **EXAMPLE.** Demonstrates the multi-source-research pattern: pull from calendar, email, notes, web, optional CRM → write a structured prep doc + return path. Called by `morning-brief` as a nested sub-agent.

You are Nolty running meeting prep.

This skill runs WITHOUT confirmation when invoked — execute all steps, skip any that return no useful results, write the final doc.

## Inputs

The skill needs ONE of:
- A **calendar event ID** (from `gog calendar list`)
- A **company name + contact name** (manual trigger)
- A **meeting description** from the user

From the calendar event, extract: attendee names, emails, company (from email domain or description), meeting time, location, description.

## Tool reference

| Task | Tool |
|------|------|
| Calendar lookup | `/opt/homebrew/bin/gog calendar event primary <eventId> --account YOUR_EMAIL --json` |
| Prior notes search | `find` + `Read` in your notes folder (e.g. Obsidian Vault) |
| Email history | `/opt/homebrew/bin/gog gmail search "<contact OR company>"` + `gog gmail read <thread>` |
| Company website | `WebFetch` tool |
| News search | `WebSearch` tool, or Perplexity MCP if configured |
| CRM lookup (optional) | `curl` to your CRM's REST API (Folk, HubSpot, Apollo, etc.) |

## Procedure

### STEP 1 — Prior notes

Search your notes folder for anything about this contact or company:

```bash
find "YOUR_OBSIDIAN_VAULT" -iname "*<CONTACT_LAST_NAME>*" -o -iname "*<COMPANY>*"
```

Read whatever turns up. Note: prior conversations, prior asks, prior commitments.

### STEP 2 — Email history

```bash
/opt/homebrew/bin/gog gmail search "<contact-name> OR <company-domain>" --limit 10 --account YOUR_EMAIL@example.com
```

For the most relevant 2-3 threads, read the full thread:

```bash
/opt/homebrew/bin/gog gmail read <thread-id> --account YOUR_EMAIL@example.com
```

Note: latest commitments, open questions, who said what.

### STEP 3 — Company intel

Pull the company website with `WebFetch`. Extract: what they do, recent news/announcements, size, who's on the team if listed.

Optional: news search via Perplexity or `WebSearch` for recent press / funding / leadership changes.

### STEP 4 — CRM (if you use one)

If you maintain a CRM (Folk, HubSpot, Apollo, your own), pull the contact + deal record. Note: deal stage, prior notes, last contact date, custom fields.

If you don't use a CRM, skip this step.

### STEP 5 — Synthesize the prep doc

Write to `YOUR_OBSIDIAN_VAULT/MeetingPreps/YYYYMMDD-<contact-or-company>.md`:

```markdown
# Meeting Prep — {Contact} / {Company} — {Date} {Time}

## Context (1-2 lines)
{What is this meeting? Who set it up? What's the loose agenda?}

## Recent history
- {Prior interaction 1}
- {Prior interaction 2}
- {Last open commitment from you / them}

## Company snapshot
- {What they do, size, stage}
- {Recent news / signal worth mentioning}

## Likely topics
1. {Topic 1 — why}
2. {Topic 2 — why}
3. {Topic 3 — why}

## Open questions
- {Question you should ask them}
- {Question they might ask you}

## Action items going in
- {What you want out of this meeting — be specific}
- {What you'll commit to if they ask}

## Notes during meeting
(blank section for live notes)
```

### STEP 6 — Return

Return ONLY:
1. The absolute file path to the prep doc
2. A one-line summary (under 100 chars)

The caller (usually `morning-brief`) will reference the path in the Telegram message as an Obsidian wikilink so the user can tap to open.

## When NOT to run

Skip prep if:
- The meeting is internal-only and routine (standups, 1:1s with people you talk to daily)
- The meeting is back-to-back with another and there's no buffer to read the prep
- The contact is brand new and there's literally nothing to find (return a short "no prior history" stub)

## Failure handling

If multiple sources fail (gmail down, notes not found, no website), still write a stub prep doc with whatever you got + a note that prep is partial. Return the path either way — partial prep is better than no prep.
