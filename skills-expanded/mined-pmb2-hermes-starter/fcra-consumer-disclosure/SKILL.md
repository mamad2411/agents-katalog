---
name: fcra-consumer-disclosure
description: Request free FCRA Section 609 consumer disclosure files from background check agencies and track submissions.
title: FCRA Consumer Disclosure Requests
version: 1.0.0
author: pmb2
metadata:
  hermes:
    triggers:
      - User asks to request background check files, consumer reports, or FCRA Section 609 disclosures.
      - User wants to see what data background check companies hold on them.
      - User mentions HireRight, First Advantage, Sterling, Checkr, Accurate, GIS, Cisive, DISA, or "background check companies."
      - User wants to dispute background check data or verify what employers can see.
dependencies:
  - mcp-playwright-mcp (for web-form submissions)
  - himalaya CLI (for email submissions)
  - browser for vendor research
---

# FCRA Consumer Disclosure Requests

Request free copies of consumer files under FCRA Section 609 from major background check / consumer reporting agencies, then track submissions and follow up.

## Core Workflow

1. **Confirm scope and identity.**
   - Ask which vendors if the user has a list; otherwise use the standard set.
   - Gather: full legal name, SSN, DOB, current address, phone, email, and government-issued ID number (driver's license or non-driver ID). Many forms require the ID number.

2. **Research processes first.**
   - For each vendor, find the current consumer disclosure method: web form, email, phone, or mail.
   - Do NOT claim submissions are complete until they are actually submitted.

3. **Draft everything, get approval.**
   - Save a process draft with vendor contact info and submission methods.
   - Prepare email/letter templates with the user's info.
   - Report back and ask for approval before any live submissions.

4. **Execute submissions.**
   - Web forms: use Playwright MCP; fill forms, capture confirmation/case numbers.
   - Email: use Himalaya CLI `message send` with piped raw message.
   - Mail: prepare certified-letter templates with return receipt.

5. **Track and follow up.**
   - Save a master tracker with confirmation numbers, dates, and methods.
   - Follow up in 7–14 days if no response.
   - Dispute inaccuracies when reports arrive.

## Standard Vendor Set

| Vendor | Typical Method | Notes |
|--------|---------------|-------|
| HireRight | Web form | ows01.hireright.com/consumer_request/entry; requires ID number |
| First Advantage | Email / mail | consumer.documents@fadv.com; PO Box 105292, Atlanta, GA 30348-5292 |
| Sterling | Email / mail | Now part of First Advantage; use same contact, mention Sterling |
| Checkr | Email / portal | disclosure@checkr.com; candidate.checkr.com portal |
| Accurate Background | Email / mail | consumer@accuratebackground.com; 2951 Red Hill Ave, Costa Mesa, CA 92626 |
| GIS | Mail / phone | 14002 E. 21st St, Suite 1200, Tulsa, OK 74134; 866-265-4917 |
| DISA | Web form | disa.com/contact/bg-copy/; requires approximate report date |
| Cisive | Phone first | 888-575-9959; ask for consumer disclosure/compliance address |

> Always verify current contact info on the vendor's site before submitting. Vendor processes change, especially after acquisitions.

## Tool Patterns

### Playwright MCP form submission

Tool names follow the pattern `mcp__playwright_mcp__browser_*`. Prefer `browser_fill_form` for multiple fields, then `browser_click` for navigation/submit.

Capture confirmation text and case numbers from the resulting page.

### Himalaya raw email send

```bash
cat /path/to/email.txt | himalaya message send -a ACCOUNT_NAME
```

The raw message must include headers:

```
To: consumer.documents@fadv.com
From: <your-email>@gmail.com
Subject: FCRA Section 609 Consumer Disclosure Request
Content-Type: text/plain; charset=utf-8

Body here...
```

Do NOT pass the message as a quoted argument; pipe it.

## Pitfalls

- **Do not assume current project context.** When a user refers to "our conversation about X" or asks for a status update, search session history for X before reporting on the wrong project.
- **Do not claim submissions are done until verified.** A previous assistant saved a markdown file and falsely claimed requests were submitted; always verify real actions.
- **ID number is required.** HireRight and similar forms require a driver's license or non-driver ID number. Ask for it explicitly if not already provided.
- **DISA form requires an approximate report date.** If the user does not have one, use a recent plausible date and note it.
- **Cisive and similar vendors hide consumer contacts.** A phone call is often required to get the correct mailing address or email.
- **Mail should be certified with return receipt.** This creates a paper trail for FCRA compliance.

## Required Information Checklist

- [ ] Full legal name
- [ ] SSN
- [ ] Date of birth
- [ ] Current address
- [ ] Phone
- [ ] Email
- [ ] Driver's license / non-driver ID number and state
- [ ] Previous addresses (last 7 years) if requested

## Output Artifacts

For each run, save:

- `fcra_submissions_tracker.md` — master tracker with confirmations and next steps.
- `fcra_email_*.txt` — sent email drafts.
- `fcra_letter_*.txt` — certified mail letters.
- `fcra_process_draft.md` — vendor research and process notes.

See `references/vendor-contacts.md` for condensed vendor contact research.
