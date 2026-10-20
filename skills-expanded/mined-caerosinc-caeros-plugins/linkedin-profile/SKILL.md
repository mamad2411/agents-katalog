---
name: linkedin-profile
description: Read the user's LinkedIn profile and edit profile sections (skills, positions, education, certifications, publications, languages) where the connected app has LinkedIn partner access. Use for "what does my LinkedIn say", profile audits, or updating profile sections.
---

# LinkedIn Profile

Read the `linkedin` skill first. Profile data is personal data — never
include it in anything shared or published without explicit confirmation.

## Reading the profile

1. Fetch with the profile tool. The standard API returns basic OpenID
   fields: name, headline, picture, email. It does **not** return the full
   public profile (experience, education, skills) unless the connected app
   is partner-approved — say so when the user expects more.
2. For a profile audit, combine what the API returns with what the user
   pastes or tells you; do not scrape LinkedIn.

## Editing profile sections (partner-gated)

The server ships tools for editing skills, positions, education,
certifications, publications, and languages. They call partner-gated
LinkedIn APIs:

- Try the tool once. On 403/"access denied", **do not retry or loop** — the
  connected app lacks that LinkedIn product. Say so and fall back to
  drafting the content for the user to paste into LinkedIn themselves.
- When editing does work: show the exact before/after for the section and
  confirm before writing. Profile edits are visible to the user's network
  immediately.

## Useful workflows

- **Headline/About rewrite**: ask for the current text (or fetch what's
  available), draft 2-3 options tuned to the user's goal (recruiting,
  selling, thought leadership), let them pick, then update or hand off the
  text.
- **Consistency check**: compare the LinkedIn headline/title against what
  the user's CRM or site says they do, and flag drift.
