---
name: linkedin-network
description: Work with LinkedIn connections and people search (partner-gated APIs), and sync LinkedIn contacts into the CRM. Use for "who am I connected to", researching a person met on LinkedIn, or logging LinkedIn contacts as CRM people.
---

# LinkedIn Network

Read the `linkedin` skill first. Connection listing and people search call
**partner-gated** LinkedIn APIs: try the tool once, and on 403/"access
denied" stop, say the connected app lacks that LinkedIn product, and use the
fallbacks below. Never loop on a gated endpoint.

## When the network tools work

- List connections and search people by name/company/title per the tool
  schemas.
- Treat results as personal data: summarize, don't dump; and never compile
  contact lists into shared or published artifacts without explicit
  confirmation.

## Fallbacks when gated (the common case)

- The user pastes a profile URL or text: extract name, title, company from
  what they provide.
- Company-level research: use whatever enrichment tools the session has
  (e.g. PDL `enrich-person`/`enrich-company` via the CRM plugin) instead of
  LinkedIn APIs.

## Syncing to the CRM

When the CRM plugin is connected, LinkedIn contacts belong in the CRM
(see `crm-records`):

1. Search the CRM for the person by name/email first — update, don't
   duplicate.
2. Create the person with `name`, `jobTitle`, and set
   `linkedinLink.primaryLinkUrl` to their profile URL; link `companyId`
   (search or create the company, setting its `linkedinLink` too).
3. Log context as a note targeted at the person ("met via LinkedIn,
   discussed X") and a follow-up task if there's a next step.
