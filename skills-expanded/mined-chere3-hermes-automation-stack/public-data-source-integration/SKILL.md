---
name: public-data-source-integration
description: Connect, harden, and verify public catalogs, feeds, aggregators, and read-only discovery sources without fabricating coverage or bypassing access controls.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [integrations, public-data, feeds, scraping, reliability, testing]
---

# Public Data Source Integration

Use this skill when expanding an unattended monitor or ingestion pipeline across public APIs, RSS feeds, SSR pages, ATS/catalog endpoints, or browser-rendered public sources.

## User-facing operating style

When the user asks to keep expanding coverage, continue doing concrete integration and verification work rather than repeatedly stopping with long progress summaries. Report brief milestones only when they explain a course correction, a blocker requiring user action, or a newly discovered data-quality risk. Do not present search queries, watchdogs, or blocked pages as equivalent to a working connector.

## Coverage states

Classify each source precisely:

- **Connected:** unattended retrieval was executed successfully, normalized records were produced, and the result passed the pipeline's filters and deduplication.
- **Degraded:** a legitimate fallback exists but a required enrichment/session/channel is temporarily unavailable. Degraded output must fail closed when missing data affects eligibility or safety.
- **Watchdog only:** the source is empty, broken, or blocked, but a low-impact check can detect recovery.
- **Prepared, not active:** implementation exists but awaits a user-controlled prerequisite such as account authorization or alert creation.
- **Not connected:** no reliable unattended path exists. Never disguise this as coverage.

## Integration workflow

1. **Inventory before building**
   - Search the codebase for existing providers, parsers, tests, and commented configuration examples.
   - Probe the official source and likely public feed directly.
   - Prefer an existing tested provider over new code.
2. **Choose the least fragile official channel**
   - Prefer, in order: documented/public API, official RSS, ATS public endpoint, SSR/embedded structured data, browser-rendered public DOM, official email alert.
   - Do not bypass login, CAPTCHA, Cloudflare, or access controls. Use a prepared official-alert/session path instead.
3. **Pin trust boundaries**
   - Require HTTPS and exact or narrowly patterned trusted hosts.
   - Disable or validate redirects where an endpoint could become an SSRF pivot.
   - Bound pagination, query combinations, page sizes, retries, and concurrency.
   - Keep ephemeral cookies/CSRF tokens in memory and preserve repeated `Set-Cookie` headers as an ordered list.
4. **Use TDD at the provider seam**
   - Build a fixture that captures pagination, duplicate IDs, unsafe URLs, malformed rows, missing locations, and transient enrichment failure.
   - Run RED, implement the smallest fix, then GREEN.
   - Follow with a live, low-volume probe against the official source.
5. **Normalize conservatively**
   - Prefer stable job/resource IDs and canonical URLs over tracking links.
   - Deduplicate within a source and globally.
   - Never infer eligibility from absent location data.
   - Infer location from titles only with narrow, explicit patterns; otherwise emit an explicit unconfirmed marker that filters reject.
6. **Fail closed on enrichment loss**
   - If a secondary lookup supplies geography, price, identity, or eligibility, do not fall back to a broad value such as `Remote`, `Available`, or `In stock` when that lookup fails.
   - Emit `Eligibility unconfirmed` (or the domain equivalent) and reject it until the enrichment succeeds.
7. **Verify production behavior**
   - Run focused provider tests, configuration validation, formatting/diff checks, and a real production scan.
   - Run a second consecutive scan to test cross-run deduplication.
   - Investigate any new records from the second run: they may be true upstream rotation, pagination drift, or a degraded-enrichment regression.
   - Programmatically re-evaluate the pending output against the current policy and remove historical records that now fail corrected rules.
8. **Scale without destabilizing existing sources**
   - Add sources in bounded batches.
   - If expansion causes timeouts, lower concurrency before blindly increasing timeouts.
   - Distinguish source failures from optional enrichment failures and preserve accurate health reporting.

## Geographic and eligibility filtering

- A home-region match may override another listed blocked region only when the role genuinely includes the home region.
- A generic `Remote` may be allowed by policy, but `Remote - California`, `Remote - Denmark`, or similar explicit foreign geography must not pass merely because the word `Remote` appears.
- Treat geographic allow markers separately from work-model markers.
- Preserve `Anywhere`, `LATAM`, and explicit home-country markers according to user policy.
- Block non-open requisitions such as `Not an Active Opening` and `Building Talent Pipeline` when the pipeline is intended for actionable jobs.

## Verification checklist

- Official endpoint executed successfully.
- Provider fixture tests pass.
- Host, protocol, redirect, and pagination boundaries are enforced.
- Multiple cookies are preserved without lossy header collapsing when required.
- Missing critical enrichment fails closed.
- Production scan succeeds at sustainable concurrency.
- Consecutive scan does not re-add the same records.
- Current pending records all satisfy current filters.
- Blocked or account-dependent sources are labeled honestly.

## Community implementation and reverse-engineering research

When surveying unofficial clients, device protocols, or community integrations:

1. Search multiple registries and channels rather than relying on repository-name search alone: GitHub repositories, package registries (PyPI/npm), upstream framework integrations, and protocol documentation embedded in source.
2. Verify claims against source files and release metadata. Repository descriptions and README badges are discovery aids, not proof of supported models, UUIDs, payload layouts, maintenance, or license.
3. Separate three evidence layers explicitly:
   - raw passive broadcasts or public responses;
   - active/local request-response or connected-device data;
   - retained, app-synchronized, or cloud history.
4. Distinguish directly measured fields from derived labels. Do not relabel timer sectors, status flags, or proprietary classifier inputs as physical measurements without evidence.
5. For maintenance, report both latest release and latest substantive source activity where available; a recently touched repository can still have an old published package.
6. Treat model-family IDs as protocol identifiers unless evidence maps them to retail model names. State the exact hardware and firmware on which richer behavior was verified.
7. If a requested exporter does not exist, identify the nearest working path and state its output limitations instead of presenting a synchronization script as a general export tool.

## References

- `references/community-protocol-research.md` — provenance, evidence grading, registry/source inspection, live-vs-history distinctions, and reporting structure for reverse-engineered community ecosystems.
- `references/consumer-device-api-availability-research.md` — evidence ladder and reporting format for determining whether a connected-device manufacturer offers a public/partner API, while separating app metrics, privacy exports, and unofficial integrations.
- `references/job-catalog-and-ats-patterns.md` — concrete patterns for ATS migrations, ephemeral public sessions, remote-location filtering, enrichment failure, and live verification.
- `references/official-career-feed-discovery.md` — provenance-first stale-portal audits, Greenhouse/Ashby/Teamtailor discovery patterns, SSR and WordPress feed pitfalls, regional relevance checks, and the recommended result table.
- `references/market-news-event-lens.md` — public candle/news integration, event-to-session alignment, degraded-source semantics, chart-density controls, and end-to-end verification for market event-study dashboards.
