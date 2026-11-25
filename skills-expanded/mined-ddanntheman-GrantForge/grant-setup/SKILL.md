---
name: grant-setup
description: >
  First-run setup for GrantForge. This skill should be used when the user says
  "set up GrantForge", "set up my organization", "enter my company information",
  "create my org profile", or when any other GrantForge skill runs and no
  .grantforge/ profile exists yet. Conducts a structured interview about the
  organization and builds the persistent profile, answer library, and voice
  profile that every other GrantForge skill depends on.
version: 0.1.0
---

# Grant Setup

Build the organization's persistent GrantForge workspace. Every other skill
in this plugin reads from it, so completeness here pays off on every future
application.

## Prerequisite: a working folder

The profile must persist across sessions, so it lives in a folder on the
user's computer, not in temporary session storage. If no folder is connected,
ask the user to connect one (their grants folder, or wherever they want
GrantForge to live) before proceeding.

## Workspace structure

Create this inside the connected folder:

```
.grantforge/
├── profile/
│   ├── organization.md      # The org dossier
│   ├── voice.md             # Writing voice preferences
│   └── boilerplate/         # Reusable answer library
│       ├── need-statement.md
│       ├── org-capacity.md
│       ├── evaluation-plan.md
│       └── ...
├── grants/                  # One subfolder per application (created by grant-intake)
└── tracker.md               # Pipeline tracker (created by grant-tracker)
```

## The interview

Conduct the interview conversationally, in stages, using multiple-choice
questions where options are predictable and free text where they are not.
Do not ask for everything at once; group related items. If the user uploads
existing documents (annual report, past applications, 990, capability
statement, website URL), extract answers from them first and only ask about
gaps. Offer document upload before starting the question list — past grant
applications are the single richest source.

### Stage 1 — Identity and legal

- Legal name, dba if any, entity type (501(c)(3), government, school
  district, university, for-profit, fiscal sponsorship arrangement)
- EIN, UEI, SAM.gov registration status and expiration, DUNS legacy if known
- Founding year, headquarters, service area (be geographic and specific)
- Website, primary contact for grants

### Stage 2 — Mission and programs

- Mission statement (verbatim)
- Each major program: name, what it does, who it serves, scale (people
  served per year), evidence of effectiveness
- Population served: demographics, geography, need indicators the org
  already tracks

### Stage 3 — Capacity and credibility

- Staff count (FTE), key leadership with 2-3 sentence bios
- Board size and notable expertise
- Annual operating budget for the last completed fiscal year, and current
- Audit status (audited financials? single audit?)
- Accreditations, licenses, memberships

### Stage 4 — Track record

- Past grants won: funder, amount, year, purpose, outcome (as many as the
  user can supply; even five is useful)
- Outcomes and impact metrics the org tracks, with recent numbers
- Any grants declined or returned, and why (informs risk framing)

### Stage 5 — Voice

- Ask for 2-3 writing samples the org is proud of (past proposals, reports,
  website copy). Analyze them for: first-person plural vs. third person,
  formality level, preferred terms for the population served, terms to
  avoid, sentence rhythm.
- Ask directly: any words or framings the org never uses? (e.g., "at-risk"
  vs "systems-impacted")
- Write findings to `profile/voice.md`. If no samples exist, record the
  direct answers and note that the house style applies unmodified.

## Writing the profile

Write `profile/organization.md` with clear headings matching the stages
above. Every fact gets a "last verified" date. Facts the user could not
supply get an explicit `TODO:` marker so future sessions can prompt for
them rather than hallucinate.

Seed `profile/boilerplate/` with any reusable narrative extracted from
uploaded past applications: need statements, organizational capacity
descriptions, evaluation plans, sustainability plans, DEI statements.
Label each file with its source and date. These are raw material for
grant-draft, never to be pasted verbatim without adaptation.

## Updating an existing profile

When a profile already exists and the user asks to update it, show a short
summary of what is on file, ask what changed, and update only those
sections, refreshing the "last verified" dates. After every submitted
application, grant-tracker will suggest harvesting strong answers back
into the boilerplate library.

## Completion

Finish by summarizing what was captured, listing the TODO gaps, and telling
the user what to try next: "give me a grant to respond to" (grant-intake)
or "find grants we qualify for" (grant-discover).
