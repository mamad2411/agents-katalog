---
name: build-a-prospect-list
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 30min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Build a targeted prospect list from approved sources for lawful sales outreach or research.

## Preconditions

- A defined ideal customer profile, territory, segment, or campaign target.
- Access to approved CRM, data provider, event, or account research tools.
- Outreach consent and suppression-list rules for the target market.

## Steps

1. **Define list criteria.** Specify industry, company size, geography, technology, buying role, trigger, and exclusions. → *Expect:* list scope is narrow enough to search.
2. **Select approved sources.** Use CRM reports, data providers, event scans, website leads, or public business directories allowed by policy. → *Expect:* the data source is permitted.
3. **Search and filter accounts.** Apply company-level filters and remove customers, competitors, partners, and poor-fit accounts. → *Expect:* target accounts match the campaign criteria.
4. **Identify contacts.** Find relevant business roles and verified work contact details from approved sources. → *Expect:* each prospect has a role-based reason for inclusion.
5. **Check suppression and ownership.** Remove opt-outs, do-not-contact records, active opportunities owned by others, and restricted accounts. → *Expect:* the list is eligible for use.
6. **Import or save the list.** [BRANCH: Salesforce | HubSpot | generic] create a Campaign or report in Salesforce; create a list in HubSpot; in another CRM, save the segment or import with source labels. → *Expect:* prospects are grouped in the CRM or approved tool.
7. **Add source and purpose labels.** Tag list source, campaign, date, owner, and intended use. → *Expect:* list provenance is visible.
8. **Review sample quality.** Inspect a small sample for fit, duplicates, consent status, and bad data. → *Expect:* obvious quality problems are found before outreach.

## Decision points

- If the source is scraped, purchased, or unclear → do not use it without legal or policy approval.
- If a prospect is already assigned → coordinate with the owner before adding to outreach.
- If the market requires opt-in → build a research list only or obtain consent first.

## Failure modes & recovery

- **F1 Poor fit:** detect many irrelevant titles or companies in sample review → tighten criteria and rebuild.
- **F2 Suppressed contact included:** detect opt-out or do-not-contact status → remove immediately and update the list filter.
- **F3 Duplicate prospects:** detect repeated emails or CRM records → dedupe before assigning or enrolling.

## Verification

The saved prospect list contains target-fit records from approved sources, excludes suppressed and owned-conflict records, and includes source and purpose labels.

## Variations

- Account-based list: build accounts first, then select only buying-committee roles.
- Event list: use registration or badge-scan consent fields as the source of truth.
- Expansion list: start from existing customer accounts and coordinate with account owners.

## Safety & privacy

Medium outreach and privacy risk. Follow CAN-SPAM, GDPR, opt-in, opt-out, suppression, data-source, and company frequency rules before using the list for contact.
