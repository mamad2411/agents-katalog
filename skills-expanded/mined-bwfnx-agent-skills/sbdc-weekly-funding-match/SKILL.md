---
name: sbdc-weekly-funding-match
description: Weekly funding opportunity to SBDC client matching packet
---

> **Schedule:** Weekly funding opportunity
> **Needs:** Gmail, Google Calendar, Drive, team drive
> **Helper scripts (yours, not included):** none

# Weekly SBDC Funding Opportunity Match

## Objective

Create a weekly funding-opportunity-to-client match packet for {{USER}} using the University of Maryland / SBDC Google account. The packet should identify new funding opportunities, match them to recently active SBDC clients, and produce outreach drafts {{USER}} can review and send.

This workflow is based on `sbdc-advising/wiki/funding-opportunity-matching.md`.

## Account And Data Boundaries

- Use {{USER}}'s University of Maryland / SBDC Gmail, Calendar, and Drive context.
- Do not use `{{YOUR_EMAIL}}` or FNX Pearl data unless explicitly relevant to an SBDC client and already present in SBDC context.
- Do not send emails automatically.
- Do not create or edit client files automatically.
- Do not overclaim eligibility. Use "may be a fit" when key facts are missing.
- Treat client information and funding-readiness notes as sensitive advising data.
- Prioritize Maryland/local opportunities before national opportunities.

## Inputs To Review

### Gmail Funding Sources

Search SBDC/UMD Gmail for the last 60 days:

- Label: `Funding Opportunities`, if present
- Keywords: grant, funding, accelerator, prize, competition, award, pitch, TEDCO, SBA, SBIR, STTR, FAST, MIPS, Catalyst, Equitech, CDFI, loan fund

For weekly mode, clearly distinguish:

- New opportunities received in the last 7 days
- Carry-forward opportunities still actionable from the prior 60 days

### Recent Client Activity

Search SBDC/UMD Calendar and Drive:

- Calendar lookback: last 60 days
- Drive lookback: recently modified/viewed client materials from the last 90 days when relevant
- Meeting keywords: SBDC, Intro, Triage, Follow-Up, Strategy, Business Assistance, eCenter, MIC

Extract:

- Client/business name
- Contact if available
- Last activity date
- Sector
- Geography
- Business stage
- Readiness signals: business plan, pitch deck, financial projections, traction, capability statement, SAM/MBE status, loan package, prior grant activity
- Missing facts that would affect eligibility

### Local SBDC Wiki Reference

Use local articles to interpret funding fit:

- `sbdc-advising/wiki/funding-opportunity-matching.md`
- `sbdc-advising/wiki/financing-alternatives.md`
- `sbdc-advising/wiki/local-lending-programs.md`
- `sbdc-advising/wiki/sba-loan-programs.md`
- `sbdc-advising/wiki/sbir-sttr-grants.md`
- `sbdc-advising/wiki/specialized-programs.md`
- `sbdc-advising/wiki/tech-team-innovation.md`
- `sbdc-advising/wiki/manufacturing-resources.md`

## Match Scoring

Score each client-opportunity pair from 0 to 100:

| Factor | Points |
|--------|--------|
| Eligibility fit: geography, entity type, stage, founder requirements, size | 0-40 |
| Strategic alignment: sector, mission, product/service relevance | 0-25 |
| Readiness signals: plan, deck, traction, financials, cap statement, application capacity | 0-25 |
| Urgency/actionability: deadline proximity, clarity, next step available | 0-10 |

Flag matches as:

- `New`
- `Carry Forward`
- `Needs Verification`
- `Low Priority`
- `Internal Only`
- `Draft Ready`

Use `Conditional` when the client may fit but a critical fact is missing.

## Geographic Priority

Rank opportunities in this order:

1. City/county opportunities in Maryland
2. Maryland statewide
3. DMV regional with clear Maryland eligibility
4. National with strong fit for active clients
5. International or out-of-region only when unusually strong

Tag each opportunity:

- Local
- Maryland Statewide
- DMV Regional
- National
- International

## Output Destination

This section was missing until 2026-08-11. Its absence — not the analysis — caused every
defect this task has produced: a duplicate `... (1).md` on 2026-08-10 and a 15-byte
`__PLACEHOLDER__` HTML stub on 2026-08-06. Do not drop it.

**Write exactly one file, to exactly this path, with exactly this name:**

```
{{TEAM_DRIVE}}/outputs/SBDC Funding Match Packet - Week of YYYY-MM-DD (DRAFT).md
```

`YYYY-MM-DD` is the **Monday** the packet covers, not the day it runs.

### The four rules that prevent the historical bugs

1. **Never use the Google Drive API to write this file.** `create_file` cannot update in
   place — it makes a second file with the same title and Drive's desktop client renames one
   to `foo (1).md`. That is exactly what happened on 2026-08-10. Write through the mounted
   team drive filesystem instead. The Drive API is fine for **read-only discovery**.
2. **Markdown only. Never write an `.html` file to `outputs/`.** The styled, interactive
   version stays a chat artifact and is not persisted to disk. The 2026-08-06 run created an
   empty `.html` stub it then could not fill, because the Drive API has no update-in-place
   tool. There is no HTML render step in this task and there should not be one.
3. **If the target filename already exists, overwrite it in place.** Do not append a suffix,
   a counter, or a timestamp. If a same-week `(1)`, `(2)`, or `-v2` twin already exists on
   disk, stop and report it in Internal Notes rather than adding a third — the two twins may
   contain *different* research, and the later file is not reliably the better one.
4. **Verify the write before reporting success.** Read the file back and confirm it is at
   least 5,000 bytes and its first line begins `# Weekly SBDC Funding Match`. A real packet
   runs 19–22 KB. If the read-back fails or comes in short, say so plainly in the run summary;
   do not report a successful run. Nothing else in this task would have caught a 15-byte file.

## Output Format

Use this exact structure.

```
# Weekly SBDC Funding Match - Week of YYYY-MM-DD

## Executive Snapshot
- New Maryland/local opportunities:
- Top client matches:
- Outreach drafts ready:
- Items needing eligibility verification:
- Deadlines inside 14 days:

## New Opportunities This Week

| Priority | Opportunity | Funder | Deadline | Amount | Geography | Sector/Stage | Source | Notes |
|----------|-------------|--------|----------|--------|-----------|--------------|--------|-------|

## Carry-Forward Opportunities Still Worth Attention

| Opportunity | Deadline | Why still relevant | Recommended action |
|-------------|----------|--------------------|--------------------|

## Recently Active Clients Reviewed

| Client | Last activity | Sector | Geography | Readiness signals | Missing facts |
|--------|---------------|--------|-----------|-------------------|---------------|

## Client-Opportunity Match Table

| Score | Status | Client | Opportunity | Rationale | Risks / missing info | Recommended action |
|-------|--------|--------|-------------|-----------|----------------------|--------------------|

## Reach-Out Checklist

| Priority | Client | Opportunity | Outreach goal | Required verification | Action this week | Status |
|----------|--------|-------------|---------------|-----------------------|------------------|--------|

## Outreach Drafts

### [Client] - [Opportunity]
Subject:

[Warm, concise draft. Be honest about uncertainty. Include one concrete CTA.]

## Internal Notes For {{USER}}
- [Judgment call or pattern worth noticing]
```

## Outreach Voice

Drafts should sound like {{USER}}:

- Direct and warm
- Plain language
- Specific resource handoff
- No corporate filler
- Data-before-opinions
- Questions that move toward a decision

Example posture:

"This may be worth a look because..." rather than "You are eligible."

## Early Exit

If no new or carry-forward funding opportunities are found, output a brief packet:

```
# Weekly SBDC Funding Match - Week of YYYY-MM-DD

No actionable funding opportunities found in the searched SBDC/UMD Gmail window.

## Client Watchlist
- [Any recently active clients who are funding-ready and should stay on the radar.]
```

## Portability Notes

When installing this in another ChatGPT Enterprise instance:

- Connect the University of Maryland Google Calendar, Gmail, and Drive connectors.
- Make sure Gmail labels/search permissions include SBDC funding newsletters and program correspondence.
- Paste this file as the scheduled task instruction.
- Keep the task as a draft/report generator unless {{USER}} explicitly authorizes sending emails.
