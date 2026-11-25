---
name: tender-source-onboarding
description: Onboards a new tender source (portal, RSS, API, bulk file) through the project's legal, rate-limit, fixture and parser gates. Use when adding a tender channel or repairing one that broke. Triggers - add a new source, new portal, scraper for, this source broke, RSS feed, onboard a channel.
---

# Tender Source Onboarding

*Example domain skill — see `examples/domain-pack/README.md`.*

At 100+ channels, every source written "slightly differently" becomes
unmaintainable. Every source passes the same eight gates; a source that skips
one does not go live.

## Gate 0 — Source card

`docs/sources/<slug>.md` is created first. No card, no code. It records: type,
country and language, access mode, whether an official API exists, robots and
terms status with the date checked, rate limit, identifying user agent, update
frequency, the field that serves as `external_id`, whether classification codes
are supplied, personal-data risk, expected accuracy band, and owner.

## The eight gates

1. **Legal** — official API or open data before scraping; terms and robots
   checked; blocked means stop, and an exception requires an ADR.
   (`security-and-threat-modeling`)
2. **Discovery** — ten varied real responses saved as fixtures, including one
   long, one with missing fields, one with attachments.
3. **Field map** — source field → canonical field, with the transformation.
   Unmappable fields stay in the raw payload; they are never invented.
4. **Parser** — written test-first against fixtures
   (`test-driven-development`). Parsing only: no business rule, no I/O.
5. **Idempotent ingest** — raw payload always stored before normalization;
   re-running a fetch creates nothing new.
6. **Resilience** — bounded retries with jitter, per-source rate limit, partial
   failure tolerated and recorded (`distributed-systems-and-resilience`).
7. **Measurement** — first 50 notices checked by hand; field completeness and
   observed accuracy written into the card. Below the project's thresholds, the
   source stays inactive.
8. **Monitoring** — daily counts per source; parse failure above the threshold
   over a rolling window marks the source degraded and notifies the owner.

## When a source breaks

Portal markup changes are routine. Capture a new fixture, diff it against the
old, write the failing test, fix the parser — and keep the **old fixture test
green**, because historical payloads must still parse.

## Exit checklist

- [ ] Source card complete, including the legal check and its date
- [ ] Ten varied fixtures committed
- [ ] Parser is pure and covered by fixture tests
- [ ] Ingest is idempotent; raw payload retained
- [ ] Rate limit and retry policy enforced in code, matching the card
- [ ] Manual accuracy sample recorded
- [ ] Monitoring and degraded threshold wired up
