---
name: brand-protection
description: Scan for typosquats and lookalike registrations around a brand, assess each domain individually, surface unconfirmed defensive candidates, and offer monitoring. Not for single-domain analysis (use domain-analyze), general discovery, or keyword trends.
---

# Brand Protection

Scan the domain landscape around a brand, evaluate each similar registration individually, and surface unconfirmed defensive candidates.

**Registration is not infringement.** A domain matching a typosquat pattern is a structural similarity, not proof of abuse. Many such domains are legitimate (common words, unrelated businesses, the brand's own portfolio). This skill surfaces domains worth reviewing. It does not determine legality or intent. Use neutral language ("registered variant", "matches pattern") throughout.

## Tools

**Core:** `typosquat` (requires full domain), `nrds`, `tld_check`, `monitor`, `preferences`, `usage`

**Supporting (per-domain, conditional):** `whois`, `dns`, `available`, `bulk_available`

**Needs from the host:**

- URL threat check: DomainKits does not provide one. If the user has connected a threat-check tool, ask once whether to use it in this scan; if none is connected or the user declines, mark the threat check Unavailable.
- Web fetch, only for page tracking and only under the fetch rule below.

**Fetch rule.** If the user has connected a threat-check tool, ask once whether to run it before fetching any domain's pages in this task, and never fetch a domain it flags. Without a check, tell the user the domain's safety is unverified and fetch only with their go-ahead. Fetch read-only: no form submissions, no credential input, no file downloads.

## Input

- Domain (e.g. `acmebank.com`): prefix = brand term, domain used directly for `typosquat`.
- Keyword only (e.g. `acme`): use for `nrds` and `tld_check`. Ask user to confirm primary domain before calling `typosquat`. Do not guess.

## Evidence rules

- A `typosquat` variant that comes with a registration date is confirmed registered. One without a date has unknown status: not "available", and not confirmed registered. For unknown-status variants worth investigating, call `whois` or `available` to resolve.
- The cross-TLD count is a current count, not a time series. It cannot prove bulk registration alone.
- A "possibly available" result from `tld_check` is not confirmed availability. Verify with `available` or `bulk_available` before recommending defensive registration.
- WHOIS privacy is neutral, not a risk signal.
- Registrar data comes from `whois`, not from `nrds`.
- `nrds` results are paged; the first page is not the full dataset. State the total found and how many pages were checked. Do not present one page as the complete picture.
- Mutation type (omission, transposition, etc.) is a fact from `typosquat`. Visual similarity to the brand is a model judgment, not tool output. Classify it as inference, not fact.
- A threat-check hit is a detection signal, not a legal conclusion; a flagged domain may be benign (false positive, shared hosting, stale blocklist). A clean result is not confirmed safe (coverage gaps, new threats, evasion). Report hits with the specific threat types returned.

## Workflow

One tool failing marks that section Unavailable. Continue with the rest.

### Phase 1: Surface scan (parallel)

1. **Typosquat.** Call `typosquat` with the primary domain. Collect variants with a registration date (confirmed registered). Note variants without a date but with a high cross-TLD count as unknown-status for possible follow-up.

2. **Recent registrations.** Call `nrds` for the brand keyword anywhere in the name, newest first, and report paging as the evidence rules require. Note any clusters of registrations on the same date as context (date clustering alone is weak evidence).

3. **Cross-TLD footprint.** Call `tld_check` with brand prefix for per-TLD registration status.

### Phase 2: Per-domain evaluation

Typosquat can return hundreds of variants. Before any lookups, determine budget.

**Step 1: Check quota.** Call `usage` first and read the remaining daily quota and per-minute rate for each tool used in this phase (`whois`, `dns`, `available`, plus `bulk_available` if defensive candidates need verification). A tool with no daily cap counts as uncapped. The investigation budget is the smaller of the remaining `whois` and `dns` quotas (the two mandatory per-domain tools), or 10 when both are uncapped. Cap at 10 without user confirmation.

**Step 2: Triage.** Select confirmed-registered variants by priority: recent registration date, high cross-TLD count, close mutation type (e.g. single-character omission or homoglyph substitution are closer mutations than TLD-swap). Visual similarity is an inference, not a fact; label it accordingly. State total found. Limit selection to the budget from Step 1.

**Step 3: Resolve unknowns (within budget).** For unknown-status variants that look high-priority, call `whois` or `available` to determine registration status. These calls count against the same budget. Only resolve unknowns if budget remains after reserving slots for confirmed-registered variants.

- If a call is rate-limited (error response), stop further calls for that tool. Report what was completed and list remaining domains as not investigated.
- State the quota situation in the report. If the user wants deeper coverage, mention that higher tiers allow more lookups.

For each selected domain:

1. **WHOIS.** Call `whois`. Extract registration date, registrar, expiry, nameservers. Report as facts.
2. **DNS.** Call `dns`. Extract A/AAAA/CNAME records, MX, NS. Report as facts. DNS alone cannot reliably distinguish parking pages from active sites (a domain with no A record may have AAAA or CNAME; parking IPs are not enumerated here). Treat DNS as context, not classification.
3. **Threat check.** If the user agreed to use a connected threat-check tool, check the variant and report its threat types as detection signals (see the evidence rules). Otherwise mark the threat check Unavailable in the report and continue.
4. **Assessment.** Note mutation type as fact. Note visual similarity as inference. Note registration timing as fact. Note threat-check hits as detection signals. Do not infer intent.

### Phase 3: Report and next steps

**Report structure:**

1. **Summary.** Variants scanned, confirmed registered, investigated, defensive candidates. One paragraph.
2. **Registered variants.** Per-domain data: mutation type, registration date, registrar (from whois), nameservers, DNS records, threat-check result (if checked). Neutral framing. These are domains worth monitoring, not confirmed infringers.
3. **Recent registrations.** NRDs containing brand term from `nrds`, with dates. State the total found and pages checked.
4. **Unconfirmed defensive candidates.** TLDs where `tld_check` reported the name as possibly available. Ranked by importance (.com/.net/.org first). Availability is unconfirmed; offer to verify with `available`/`bulk_available`.
5. **Not investigated.** How many variants were skipped, why (quota, unknown status, lower priority).
6. **Unavailable evidence.** Any tools that failed or returned errors during the scan. State which section is affected and what data is missing.

**Monitoring offer.** After the report, offer to set up `monitor` on registered variants the user wants to track.

- Monitoring needs a registered DomainKits account. Check the tier in the `usage` response (call `usage` if it was not called). For a guest, the report is the full deliverable: mention that a registered account unlocks monitoring, and do not call `preferences`.
- For a registered user, check memory status with `preferences`, and work out the remaining monitor slots from the tier's monitor limit in `usage` and the monitors already set. If no slots remain, do not offer monitoring; say the slots are full and mention upgrade options.
- If memory is not enabled, ask the user before turning it on with `preferences`. Only proceed with their consent.
- Create monitors with `monitor`, checking WHOIS and DNS by default, with a short note on why each domain is watched. Offer only as many domains as slots remain. If the user selects more, add up to the limit and list the rest as "not added, monitor slots full".
- Page tracking requires separate user consent. Before enabling it, explain that the AI client will fetch the page content and store a text snapshot. Page fetches follow the fetch rule above.
- Monitors run when checked, not in the background.

## Limitations

- Typosquat covers the mutation types the tool generates, not every possible lookalike.
- This skill evaluates domains individually. It does not attribute domains to any person or organization.
- Visual similarity is a model inference, not a measured value. Different models may assess it differently.
