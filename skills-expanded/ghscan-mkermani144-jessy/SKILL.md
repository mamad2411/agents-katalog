---
name: wellfound
description: Wellfound URL patterns and page semantics for jessy job scanning. Use whenever interacting with wellfound.com job, role, location, or company pages to read startup job listings and details.
user-invocable: false
---

# Wellfound platform skill (jessy)

DOM extraction goes through the Claude Chrome extension (`claude --chrome`).
Ask the page in natural terms ("visible job rows", "job detail header",
"About the job") rather than relying on fixed selectors.

## When this loads

Triggered when the active tab URL contains `wellfound.com/jobs`,
`wellfound.com/role`, `wellfound.com/location`, or `wellfound.com/remote`
and jessy is scanning, scoring, or extracting jobs.

## URL patterns

| Pattern                         | Page kind      |
|---------------------------------|----------------|
| `wellfound.com/jobs`            | Search / jobs  |
| `wellfound.com/role/<slug>`     | Role listing   |
| `wellfound.com/role/r/<slug>`   | Remote role    |
| `wellfound.com/location/<slug>` | Location list  |
| `wellfound.com/jobs/<id>-...`   | Detail page    |

Canonical job URL is the detail URL:
`https://wellfound.com/jobs/<id>-<slug>`. Strip query params and fragments.

## Page semantics — lists

- Lists are grouped by company. One company card can contain multiple jobs.
- Company block usually has company name, one-line summary, employee band,
  hiring badges, and funding/stage badges.
- Each job row has: title, employment type, salary/equity when visible,
  location / remote policy, experience, posted time, save/apply controls.
- Job links often open a full detail page instead of a side rail.
- Lists usually lazy-load more rows. Keep scrolling/loading until no new
  visible job rows appear, the scan hits an attempted row, or the run cap is
  reached.

## Page semantics — detail

- Header: title, company, salary/equity, location/remote policy,
  experience, employment type, reposted/posted time.
- Sidebar/details: remote policy, company location, visa sponsorship,
  preferred timezones, relocation, hiring contact.
- Body: `About the job`, often with markdown-style headings.
- Company section: summary, employee band, industry/stage/funding tags,
  perks, founders/team links.

## Requirement headings (extract -> `req_hard`)

Match headings / lead-in phrases, case-insensitive:

- "Requirements"
- "Qualifications"
- "What we're looking for"
- "What you bring"
- "You have"
- "We're looking for"
- "Experience"
- "Skills"

Use nearby bullets/lines until the next heading.

## Nice-to-have headings (extract -> `req_nice`)

- "Nice to have"
- "Bonus"
- "Preferred"
- "Plus"
- "Bonus points"
- "Extra credit"

Split mixed required/preferred lists when visible.

## Boundary / skip rules

- Title prefilter: drop cards whose title matches any global
  `skip_title_keywords` entry.
- Attempt boundary: if a canonical URL exists in Jessy's attempted state,
  stop lower/older jobs for that list/feed.
- Ignore Wellfound `Save`, `Apply`, and any viewed-like UI state.

## Auth + access

Public pages expose enough for many jobs. If the page requires login or blocks
detail text, return `auth_wall` and stop that card. Do not attempt to log in.
