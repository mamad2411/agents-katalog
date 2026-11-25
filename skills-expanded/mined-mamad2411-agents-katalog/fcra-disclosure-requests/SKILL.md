---
name: fcra-disclosure-requests
version: 1.0.0
description: Request free consumer file disclosures from background-check agencies under FCRA §609/§1681g, track submissions, and follow up on responses.
metadata:
  hermes:
    triggers:
      - user wants to see what background check companies have on them
      - user mentions FCRA, consumer disclosure, background check file, or "what do they have on me"
      - user lists background check vendors like HireRight, First Advantage, Checkr, Sterling
      - user wants to dispute or review background check data
      - user asks for a "system update" on background check requests
    related_skills:
      - hermes-legal-watchdog
      - reputation-campaign
      - osint-person
---

# FCRA Consumer Disclosure Requests

Use this skill when the user wants to request, review, or dispute the information held by consumer reporting agencies (background check companies) under the Fair Credit Reporting Act.

## Purpose

The FCRA gives consumers the right to request a copy of their file from a consumer reporting agency. For background-check agencies, this is typically called a **Section 609 disclosure** or **consumer file disclosure**. The goal is to learn what data the agency holds and correct inaccuracies before they affect employment, housing, or other decisions.

This skill covers the full repeatable workflow: vendor discovery → information gathering → drafting → approval → submission → tracking → follow-up.

## When to Use

- User asks to "pull my background check" or "see what they have on me"
- User references specific vendors: HireRight, First Advantage, Sterling, Checkr, Accurate Background, GIS, Cisive, DISA
- User wants to dispute a background check result
- User asks for a status update on prior disclosure requests
- User is preparing for a job search and wants to clean up records

## Required Information Before Submitting

Collect and confirm these before drafting any request:

| Field | Example |
|-------|---------|
| Full legal name | the operator Michael Backus |
| SSN (full or last-4 depending on vendor) | 083-76-8990 |
| Date of birth | 11/03/1989 |
| Current address | 89 Saratoga Rd, Scotia, NY 12302 |
| Previous addresses (last 7 years) | if user has lived at current address < 6 months |
| Email | <your-email>@gmail.com |
| Phone | 518-817-6493 |
| Government-issued ID number | NY State non-driver ID or driver's license number |

**Critical:** Do not fabricate the ID number. If the user shared it in a prior message or image, retrieve it. If the image/file is missing, ask the user before filling any form that requires it. Never guess.

## Core Vendor Playbook

| Vendor | Online | Email | Phone | Mail | Notes |
|--------|--------|-------|-------|------|-------|
| **HireRight** | [ows01.hireright.com/consumer_request/entry](https://ows01.hireright.com/consumer_request/entry?entry=create_consumer_request) | — | 1-866-521-6995 | 14002 E. 21st St, Suite 1200, Tulsa, OK 74134 | Form is fastest; requires driver's license/non-driver ID number |
| **First Advantage** | [fadv.com/candidates/](https://fadv.com/candidates/) | consumer.documents@fadv.com | 800-845-6004 | P.O. Box 105292, Atlanta, GA 30348-5292 | Free once per 12 months |
| **Sterling** | Redirects to FAdv | consumer.documents@fadv.com | 800-845-6004 | Same as FAdv | Sterling acquired by First Advantage; mention both names |
| **Checkr** | candidate.checkr.com/login (requires active check) | disclosure@checkr.com | (415) 857-8749 | 1 Letterman Dr, Bldg D, Suite D2400, San Francisco, CA 94129 | Use email/portal if no active check link |
| **Accurate Background** | Site often times out | consumer@accuratebackground.com | 800-784-3911 | 2951 Red Hill Ave, Costa Mesa, CA 92626 | Fall back to phone if web/email fail |
| **GIS** | None found | — | 866-265-4917 | 14002 E. 21st St, Suite 1200, Tulsa, OK 74134 | Same address as HireRight; mail certified |
| **Cisive** | None found | Not publicly listed | 888-575-9959 | Call for consumer disclosure address | Phone-first vendor |
| **DISA** | None found | Not publicly listed | 800-222-3131 | Call for compliance address | Phone-first vendor |

See `references/vendor-contacts.md` for the full contact bank and submission templates.

## Workflow

1. **Confirm the active thread/topic.** If the user says "this thread" or asks for a "system update," retrieve the relevant session history before acting. Do not assume the current working project is the topic.
2. **Search session history** for prior background-check work to avoid false claims or duplicated effort.
3. **Collect or verify PII.** Ask for missing fields. Never fabricate.
4. **Research any vendors** not yet documented.
5. **Draft requests** for all vendors (email text, mail letter, online form fields).
6. **Save drafts** to a markdown file in the user's home directory.
7. **Report back and request explicit approval** before submitting anything live.
8. **After approval, submit in this order:**
   - Online forms first (HireRight, First Advantage portal)
   - Email submissions next
   - Certified mail letters for vendors with no online/email path
   - Phone calls for Cisive/DISA to obtain addresses/processes
9. **Create a tracker** with vendor, method, date/time, confirmation number, and follow-up date.
10. **Follow up** in 7–14 days if no response, then dispute inaccuracies.

## Pitfalls

- **Do not claim submissions were made unless you actually completed them.** A prior session falsely told the user requests were submitted when only a markdown file was saved. Always verify and be explicit about what was done vs. drafted.
- **Do not submit without explicit user approval** for live actions involving PII.
- **Do not guess the ID number.** Ask if it is missing.
- **Watch for vendor consolidation.** Sterling now routes through First Advantage. Do not treat them as fully separate submission paths unless the user insists.
- **Browser automation may fail.** HireRight's form uses JavaScript navigation. If Playwright/MCP tools are unstable, fall back to manually guiding the user through the form or drafting the request for them to submit.
- **Phone-first vendors need human calls.** Agents cannot reliably call Cisive or DISA; prepare the script and hand it to the user.

## Tooling Notes

- If the native `browser_*` tools fail with CDP errors, check whether a project-scoped MCP server is configured (e.g., `playwright-mcp`). Use `tool_search` and `tool_describe` to invoke MCP tools with their fully qualified names (e.g., `mcp__playwright_mcp__browser_navigate`).
- Use `session_search` before assuming context from prior turns.

## References

- `references/vendor-contacts.md` — full vendor contact list and draft request templates
- `references/session-2026-07-12-notes.md` — detailed notes from the first execution run

## Expected Timeframes

- Online/email submissions: confirmation usually immediate to 24 hours
- HireRight reports: ~3 business days for specific-company reports; up to 15 calendar days for other requests
- Mail delivery: 5–7 business days
- Overall response window: allow 2–4 weeks before following up
