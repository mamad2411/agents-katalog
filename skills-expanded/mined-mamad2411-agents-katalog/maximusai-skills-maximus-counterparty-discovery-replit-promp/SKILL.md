# Replit Build Prompt: Maximus Counterparty Discovery

Build a production-ready web application named **Maximus Counterparty Discovery**. It accepts a natural-language description of any desired counterparty and performs auditable, source-aware public-web research. The first built-in template is: family office, allocator, CTA, or individual accredited-investor prospect potentially suitable for a managed-futures CTA separately managed account with a $100,000 minimum.

Do not import, seed, or port any prior sample prospect export. Build schemas, logic, connectors, and empty demo records only.

## Product behavior

1. Convert the user's description into a structured search brief: type, geography, minimum capacity, strategy fit, positive signals, exclusions, recency, target count, and approved sources.
2. Create a research plan with source families, query variants, and estimated confidence.
3. Run jobs asynchronously through a queue and show live progress by source. Long searches may pause/resume safely.
4. Store every query and every source visited, including zero-result, blocked, paywalled, rate-limited, and failed searches.
5. Extract candidates, claims, dates, identifiers, citations, and exact evidence snippets.
6. Resolve duplicate identities conservatively. Never merge on name alone.
7. Score fit, capacity, intent, source quality, risk, and identity confidence. Expose score explanations.
8. Require a human review gate before marking a candidate approved for outreach.
9. Export CSV/JSON/XLSX containing candidates, evidence, and full source logs. Include a separate methodology/readme export.

## CTA template discovery paths

Implement configurable modules for:
- Family offices and alternative-investment allocators.
- CTAs/CPOs that allocate to external CTAs, multi-manager programs, sub-advisers, or manager-of-managers products.
- Public bankruptcy, receivership, enforcement, and court records involving failed CTAs/CPOs, looking for lawfully disclosed LPs, creditors, feeder funds, account holders, and counterparties. Treat these only as relationship leads; never target vulnerability.
- Public futures/trading forum and Reddit discussions that indicate manager-selection interest or substantial trading experience. Keep pseudonymous profiles pseudonymous unless independently verified.
- Confirmed property transactions of $5 million or more as a weak liquidity signal; suppress residential street addresses.
- SEC Form 4 filings showing estimated gross open-market stock sales of $5 million or more. Parse transaction codes, direct/indirect ownership, prices, shares, footnotes, option exercises, gifts, withholding, and Rule 10b5-1 references.

## Source architecture

Create adapter interfaces for SEC EDGAR, CFTC releases, NFA BASIC/manual verification, SEC IAPD, FINRA BrokerCheck, CourtListener/RECAP, authorized PACER access, state court portals, public bankruptcy records, company websites, news/search APIs, Reddit's approved API, approved social/search providers, licensed property data, and licensed business-contact providers.

Never bypass CAPTCHAs, login walls, robots controls, rate limits, paywalls, or platform terms. Each adapter must declare terms basis, rate limits, authentication requirements, and permitted data retention.

## Database

Use PostgreSQL/Supabase with tables: users, workspaces, search_briefs, research_jobs, source_adapters, search_queries, source_visits, candidates, candidate_identifiers, evidence, claims, candidate_scores, review_actions, suppression_list, exports, and audit_events.

Use the field definitions from the bundled Counterparty Discovery skill. Model every claim as a claim-to-source relationship, not a loose note.

## Stack

Use TypeScript, Next.js, PostgreSQL/Supabase, background workers with durable queues, Playwright only for permitted public pages, provider APIs where available, Zod validation, row-level security, encrypted secrets, retries with backoff, per-source throttling, structured logging, and tests.

## UI

Pages: New Search, Search Brief Review, Live Research Console, Candidate Table, Candidate Evidence Drawer, Source Coverage Map, Review Queue, Suppression List, Connector Settings, Exports, and Audit Log.

Candidate table columns: name, entity, type, title, fit, capacity, intent, identity confidence, risk, total score, strongest evidence, last verified, and review status. Clicking a score must explain how it was calculated.

## Compliance and privacy

Do not infer or target protected traits. Do not display exact private residence addresses, family-member data, personal routines, private emails, or personal phone numbers. Keep accreditation and suitability as unverified until confirmed. Discovery does not authorize solicitation. Add configurable compliance approval, do-not-contact suppression, data retention, deletion, and export redaction controls.

## Acceptance tests

- A search creates a complete source plan before execution.
- Every candidate claim has at least one source record.
- Every source query is retained even when no candidate is found.
- Duplicate names at different organizations remain separate.
- Form 4 open-market sale math is reproducible and footnotes are retained.
- A property-sale-only lead cannot receive a high capacity or total score.
- A Reddit-only pseudonym cannot be marked identity-verified.
- Exports include candidates, evidence, source log, methodology, timestamps, and caveats.
- No sample prospect data exists in migrations, fixtures, repository history, or demos.
