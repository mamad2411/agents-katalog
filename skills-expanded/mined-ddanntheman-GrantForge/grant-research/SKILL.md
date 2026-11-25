---
name: grant-research
description: >
  Gather the evidence base and funder intelligence for a grant application.
  This skill should be used when the user says "research this grant", "find
  statistics for our need statement", "research the funder", "who has this
  foundation funded before", "find citations to support X", or after
  grant-intake completes and drafting is about to begin.
version: 0.1.0
---

# Grant Research

Build two research files inside the grant workspace before drafting starts:
the evidence base that substantiates the narrative, and the funder
intelligence that shapes how the narrative is framed. Weak applications
assert; winning applications prove.

Requires a grant workspace from grant-intake (or create one if the user is
researching ahead of a specific opportunity).

## Part 1 — Evidence base (`research/evidence.md`)

Read the requirements matrix to identify what must be proven: typically
the need (problem severity in the service area), the intervention's
effectiveness, and the org's capacity to deliver.

**Need data.** Search for the most local, most recent data available, in
this order of preference: the org's own tracked data (from the profile),
then county/city-level government data, then state, then national. Standard
sources by domain: Census/ACS (demographics, poverty), BLS (employment),
CDC WONDER and county health rankings (health), NCES and state report cards
(education), HUD and NLIHC (housing), FBI UCR and local dashboards (safety),
Feeding America Map the Meal Gap (food security). Record for every statistic:
the figure, year, geography, source name, and a working URL. Verify each URL
resolves before recording it.

**Intervention evidence.** Search for peer-reviewed studies, meta-analyses,
and clearinghouse ratings (What Works Clearinghouse, Blueprints,
evidence-based registries relevant to the domain) supporting the program
model. Prefer studies of the same model; otherwise the closest analog,
stated honestly as an analog.

**Rules.** Never fabricate or approximate a statistic. If the data does not
exist at the needed geography, say so and recommend the honest fallback
(state-level data plus local qualitative evidence). Flag any statistic older
than five years. Every entry gets a full citation in the format the funder
requires (or a consistent format if unspecified).

## Part 2 — Funder intelligence (`research/funder.md`)

**Foundations.** Pull the funder's 990-PF/990 (ProPublica Nonprofit
Explorer, Candid) for the last 2-3 years: total giving, grant count,
typical award size, and — most useful — the actual grantee list. Identify
grantees similar to the org (size, geography, program). Read the funder's
website, annual report, and any president's letter for stated strategy and
vocabulary. Note board members and staff with any connection to the org's
network.

**Government funders.** Find prior award lists (USASpending.gov for federal;
agency press releases), technical assistance webinars and their recorded
Q&A, and any published reviewer guidance. Identify what past winners had in
common. Note the program officer's name and the Q&A contact.

**Corporate.** Giving priorities, employee presence in the service area,
recent local sponsorships, and who signs off (foundation staff vs. local
branch).

**Synthesis.** End the file with a half-page "how to win this funder"
memo: their vocabulary to mirror, priorities to lead with, award-size
positioning, and any relationship route worth activating before submission.

## Handoff

Summarize both files in chat: the three strongest evidence points, the
biggest evidence gap, and the funder-alignment angle. grant-draft consumes
these files directly; nothing in a draft may cite a source that is not in
`research/evidence.md`.
