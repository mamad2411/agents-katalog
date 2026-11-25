---
name: grant-discover
description: >
  Find open funding opportunities that match the organization's profile. This
  skill should be used when the user says "find grants for us", "what grants
  are we eligible for", "search for funding opportunities", "any new grants
  this month", or asks about funding sources for a specific program or project
  idea.
version: 0.1.0
---

# Grant Discovery

Search systematically for open opportunities the organization can plausibly
win, and rank them by fit, not by volume.

Requires the `.grantforge/` profile; if missing, run grant-setup first. Read
`profile/organization.md` before searching — entity type, service area,
program areas, and budget size drive everything.

## Search strategy

Run web searches across these source categories, adapted to the org's
entity type and geography:

1. **Federal**: Grants.gov (search by keyword and eligibility category),
   agency forecast pages for the 2-3 agencies most aligned with the org's
   work (e.g., ED, HHS, NSF, NEA, DOJ, USDA, EPA).
2. **State and local**: the state's grants portal, relevant state agency
   pages, county/city community development and health department pages
   for the service area.
3. **Private foundations**: community foundations serving the org's
   geography, national foundations whose published priorities match the
   org's programs, and funders of peer organizations (search "[peer org]
   received grant" and funder annual reports).
4. **Corporate**: corporate giving programs of major employers in the
   service area, plus national corporate foundations aligned with the
   program area.

Verify every candidate on the funder's own site: deadline still open,
eligibility confirmed, award range stated. Discard anything that cannot
be verified as currently open — stale listings are endemic in grant
databases.

## Filtering and ranking

Apply hard filters first (entity type eligible, geography eligible,
deadline realistically achievable given application complexity). Then
score remaining candidates 1-5 on:

- **Program fit**: does the funder pay for what the org already does?
- **Size fit**: award range appropriate to org budget (an org with a $500k
  budget rarely wins a $5M award, and a $2,500 grant may not repay the
  effort of a 20-page federal application).
- **Winnability**: number of awards, geographic preference, whether the
  funder has funded similar orgs, incumbency patterns.
- **Strategic value**: general operating > program > project restricted;
  multi-year > one-time; funders who renew.

## Deliverable

Produce a ranked opportunity brief (in chat, and save to
`.grantforge/discovery/<date>-opportunities.md`) with one entry per
opportunity: funder, program, deadline, award range, match requirement,
one-paragraph fit rationale, link to the announcement, and a recommended
action (pursue now / watch for next cycle / skip). Cap the list at the
10 best; a short strong list beats a long weak one.

For any opportunity the user wants to pursue, hand off to grant-intake
and add it to `tracker.md` with status `intake`.

Offer to set up a recurring scheduled search (weekly or monthly) using the
same profile-driven criteria, reporting only new opportunities since the
last run.
