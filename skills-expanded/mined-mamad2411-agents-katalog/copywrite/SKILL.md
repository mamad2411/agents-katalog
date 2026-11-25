---
name: copywrite
description: >
  Write full email copy from an Atomic Emails campaign storyboard. Takes storyboard
  synopses and produces complete, send-ready email copy with subject lines, preheaders,
  body content, and properly structured CTAs. Use when the user has a campaign storyboard (from
  atomic-emails-storyboard) and needs to write the actual emails.
  Triggers: "write the emails", "draft email copy", "atomic emails copywriter",
  "turn this storyboard into emails", "write email #3", "create the campaign copy",
  or when continuing from the atomic-emails-storyboard skill output. This is Step 3 of 3
  in the Atomic Emails skill chain.
allowed-tools: Read, Write, WebFetch, AskUserQuestion
---

# Atomic Emails Copywriter

Write full email copy from a campaign storyboard. Each email follows the atomic principle: one idea, focused and customer-centric.

## Overview

This skill covers Step 5 of the Atomic Emails method: writing the actual emails from storyboard synopses.

## Workflow

### 1. Accept input

Accept a campaign storyboard (from the storyboard skill) or individual email briefs. Minimum required per email: title, synopsis, email type, primary CTA, and key resource.

Also accept (if available): the discovery brief from the research phase, for tone and copywriting material.

### 2. Write each email

For each storyboard row, follow this process:

1. **Use the synopsis as outline.** The synopsis defines the email's one idea and purpose.
2. **Pull content from the referenced resource.** If a URL is provided, fetch it to grab relevant content.
3. **Grab catchy phrases** from available copywriting material (founding story, customer quotes, homepage copy).
4. **Edit for email format.** Make it shorter, clearer, and catchier than the source material. Email is not documentation.
5. **Shape the CTAs** following the hierarchy in [references/cta-hierarchy.md](references/cta-hierarchy.md).
6. **Write the subject line and preheader.** Subject line: clear, specific, benefit-oriented. Preheader: complement (don't repeat) the subject.
7. **Customer-hat check.** Re-read from the customer's perspective. Is it clean, cohesive, and does it evoke the right emotion?

### 3. Email structure

Every email follows this structure:

```
Subject: [Subject line]
Preheader: [Inbox preview text]

[Greeting — e.g. "Hey {{first_name | default: 'there'}}," ]

[Opening — 1–2 sentences that hook the reader. Connect to their problem or goal.]

[Body — The core content. Keep it focused on the one idea. Include actual useful content, not just a teaser. 3–8 short paragraphs.]

[Primary CTA — Button or prominent link.]

[Optional: Secondary CTA — Inline link offering an alternative path.]

[Sign-off]

[Optional: P.S. — Reminder of a different important action.]
```

### 4. Output

Organize each campaign into a separate folder using the name of the campaign. Within each folder, save each email as a separate `.md` file named `[01]-[Email Title].md`, `[02]-[Email Title].md`, etc.

## Quality Criteria

Review every email against these criteria from [references/email-quality-checklist.md](references/email-quality-checklist.md):

- **Focused:** One idea per email. If you're covering two topics, split them.
- **Strategic:** Serves at least one of the four strategic purposes (critical for adoption, increases satisfaction, increases perceived value, delights).
- **Clear CTA:** Primary CTA is obvious and actionable.
- **Customer-centric:** Passes at least 2–3 of the qualifying questions.
- **Appropriate length:** Focused doesn't mean short. Include enough content for the reader to get value from the email itself, not just the CTA.
- **Human tone:** Write as a person, not a brand. Use "I" not "we" where appropriate. No corporate jargon.

## Guidelines

- Each email should take 20–40 minutes of equivalent human effort. Don't overthink — a single email won't solve everything.
- Be realistic: no user is waiting for your email to make their day. It's one touchpoint in a bigger system.
- Use merge tags for personalization: `{{user.first_name}}`, `{{company.name}}`, etc. Ask the user what merge tags their platform supports.
- When the user asks to write "all emails," produce them sequentially and present for review after each batch of 3–5.
