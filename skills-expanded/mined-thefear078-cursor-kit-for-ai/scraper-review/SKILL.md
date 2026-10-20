---
name: scraper-review
description: MUST USE for Playwright/HTTP scraper audits — blocking, ethics/TOS, retries, selectors, silent breakage detection. Triggers on scraper PR, CAPTCHA walls, or "parser returns empty."
---

# Scraper Review

Scrapers fail **silently** when sites change. Review for legal/ethical bounds, resilient selectors, observability, and polite rate limits — treat like production batch jobs (`pipeline-review`).

## When This Skill Applies

- New scraper or parser module
- Zero results without error
- IP bans, CAPTCHA, 403 spikes
- Moving from BeautifulSoup to Playwright
- Scheduled cron scraper maintenance

## Severity Model

| Level | Signal | Gate |
|-------|--------|------|
| **R0** | Credentials in repo; scraping PII without legal basis; DDoS-rate requests | Stop |
| **R1** | No empty-result alert; brittle single CSS selector | Fix before schedule |
| **R2** | No retry backoff; missing user-agent policy | Sprint |
| **R3** | Logging noise | Optional |

Cross-ref: `api-integration` when official API exists; `workflow-design` for orchestration; `proxy-rotation` template.

## Phase 0 — Prefer Official API

Ask: Is there documented API/webhook? Scraping is **last resort** — document why API insufficient.

## Phase 1 — Politeness & Compliance

- [ ] robots.txt reviewed — not legal sole defense but signal
- [ ] Rate limit ≤ site tolerance (default ≤1 req/s same host unless documented)
- [ ] Identify bot contact in User-Agent
- [ ] Terms of service risk acknowledged in doc
- [ ] No bypass of paywalls/login without authorization

## Phase 2 — Technical Resilience

### HTTP layer

- Session with retries: exponential backoff, retry idempotent GET only
- Timeout connect/read; circuit breaker after N failures
- Cache `ETag`/`If-Modified-Since` when supported

### Browser layer (Playwright 2025–2026)

- [ ] `page.locator` with role/text over brittle CSS
- [ ] Wait for network idle or specific response — not fixed `sleep`
- [ ] Screenshot on failure to object storage (no PII in shared bucket)
- [ ] Headless fingerprint — expect bot detection; plan API or partnership

```bash
npx playwright test tests/scraper.spec.ts --reporter=list
python -m pytest tests/test_parser.py -q
```

## Phase 3 — Data Contract

- Schema for parsed output; validate with pydantic/Zod
- **Empty allowed?** If not — fail job and alert
- Row count vs historical baseline (`data-quality` anomaly)

```python
if len(rows) == 0:
    raise ScrapeEmptyError(url)
```

## Phase 4 — Monitoring

- Metric: `scrape_success`, `rows_extracted`, `duration`, `http_status`
- Alert: zero rows, error rate >10%, latency 3× baseline
- Golden HTML fixtures in repo for unit tests — detect selector drift in CI

## Phase 5 — Structure

```text
scraper/
  fetch.py       # HTTP
  parse.py       # pure functions
  run.py         # CLI entry
  fixtures/
tests/
```

Parse functions pure — feed fixture HTML.

## Output Template

```markdown
## Scraper Review: [target/site]

**Verdict:** ✅ / 🔶 / ❌ | **Legal note:** ...

### Fetch strategy
- HTTP / Playwright
- Rate:

### Fragility
| Selector | Risk | Alternative |

### Findings
| ID | Sev | Issue | Fix |

### Monitoring
- Alerts:

### Tests
- Fixture coverage:
```

## Anti-Patterns

- **Infinite retry** on 404 — ban loop
- **Scrape in request path** of user API — async queue
- **One giant sleep(5)** everywhere
- **No diff detection** — store hash of normalized output
- **Personal account cookies** in git

## Cross-References

| Skill | Use when |
|-------|----------|
| `pipeline-review` | Airflow schedule |
| `secrets-audit` | leaked cookies |
| `playwright-automation` integrations |

## Cursor Kit Templates

- `scraper`, `parser`, `proxy-rotation`

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

