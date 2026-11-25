---
name: error-guessing
description: Apply experience-based error guessing and defect taxonomies to design tests for likely failure modes — beyond what specs and EP/BVA cover. Use when augmenting black-box techniques on risky areas.
source: self
date_added: 2026-05-01
---

# Error Guessing

Spec-based techniques (EP, BVA, Decision Tables) don't catch what the spec doesn't say. Error guessing leverages experience, defect taxonomies, and historical bug patterns to predict where bugs hide and design targeted tests.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Spec | ISTQB CTFL 4.0 §4.4.1 (experience-based testing) |
| Taxonomies | IEEE 1044 (defect classification), Beizer's Bug Taxonomy, OWASP Top 10 |
| Pairing | Exploratory testing, fault injection, mutation testing |
| Knowledge sources | Defect history, postmortems, escaped-defect logs, PR comments, on-call incidents |

## When to Use

- Risk-based testing on critical features (payments, auth, data integrity).
- Augmenting EP/BVA after systematic coverage is in place.
- Onboarding new testers — cataloging "where bugs always live here".
- Pre-release "bug bash" sessions.

## Source Material

1. **Past defect database**: cluster bugs by component, type, root cause. Extract patterns.
2. **Postmortems**: incidents reveal real failure modes (race conditions, retry storms, cache poisoning).
3. **On-call logs**: recurring 3am pages indicate fragile code paths.
4. **PR review comments**: "what about when X is null?" — the reviewer is error-guessing.
5. **Generic taxonomies**: data type limits, encoding, concurrency, time, resource exhaustion.

## Universal Error Guess Catalog

| Category | Try |
| --- | --- |
| Numbers | 0, -1, MAX, MIN, MAX+1, NaN, Infinity, very small float, negative zero |
| Strings | empty, whitespace, very long, Unicode (emoji 🤖, RTL ‏, combining marks, NFC vs NFD), control chars, SQL/HTML/JSON injection samples |
| Dates/times | epoch 0, year 1970/2000/2038/9999, Feb 29, DST forward/back, midnight in non-UTC TZ, 23:59:60 leap second |
| Collections | empty, single, max-size, duplicates, unsorted, with nulls |
| Files | empty, 1 byte, very large, binary in text field, wrong encoding, name with spaces/Unicode, max path length |
| Network | timeout, partial response, 5xx, redirect loop, slow stream, IPv6, double-submit |
| Concurrency | duplicate request, out-of-order events, retry after success, two writers, expired lock |
| Auth | expired token, refresh during request, role downgrade mid-session, CSRF, missing CORS header |
| Idempotency | duplicate POST, replayed webhook, restart mid-write |
| State | back button, refresh, browser back-then-forward, multiple tabs, offline → online |
| I18n | locale flip mid-flow, RTL layout, currency precision (JPY 0 decimals, BHD 3) |
| Limits | rate-limit boundary, quota-just-exceeded, plan downgrade |
| Errors | error → retry → error → success path; partial failure surfaces partial UI |

## Method

1. **Pick the feature** and its risk profile.
2. **Pull patterns** from defect history for similar features.
3. **Brainstorm** with the universal catalog and team experience (45-min bug-bash style).
4. **Triage** guesses by likelihood × impact; keep top 10–20.
5. **Convert into automated or charter-based tests**; tag `@error-guess` for tracking.
6. **Feed back hits** to the org-wide pattern library.

## Code

```ts
test.describe('error-guessing — checkout', () => {
  test('double-submit yields one order', async ({ page, apiClient }) => {
    await page.goto('/checkout');
    const place = page.getByRole('button', { name: 'Place order' });
    await Promise.all([place.click(), place.click()]);
    const orders = await apiClient.orders.list();
    expect(orders.length).toBe(1);
  });

  test('back button after success does not re-submit', async ({ page }) => {
    await page.goto('/checkout');
    await page.getByRole('button', { name: 'Place order' }).click();
    await page.waitForURL('**/orders/*');
    await page.goBack();
    await expect(page.getByText('Order already placed')).toBeVisible();
  });
});
```

## Bug-Bash Charter Template

```
Charter: Find error-handling defects in /checkout
Tester(s): Alex, Sam
Time-box: 60 min
Approach:
  - apply universal catalog: numbers, strings, dates, network, concurrency, idempotency
  - target known fragile areas: 3rd-party tax service, address autocomplete
Logging: append to bug-bash.md; tag @error-guess
Stop conditions: time elapsed OR session yields > 5 high-severity defects
```

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Treating EG as substitute for systematic coverage | Use it as **complement** to EP/BVA/Decision Tables |
| Random guesses with no record | Catalog and reuse — patterns recur across features |
| Senior-only knowledge | Capture in the team's pattern library; pair sessions |
| One-off bug-bash before launch | Routine, time-boxed, monthly |
| Hits never converted to automated tests | Promote significant guesses into the regression suite |

## Output Format

```
Feature: Checkout
Top guesses (10) prioritized by likelihood×impact:
  1. Double-click "Place order" → duplicate charge   [auto'd ✅]
  2. Address autocomplete returns 0 → silent crash   [auto'd ✅]
  3. Tax service 504 → order placed without tax line [charter ⏳]
  ...
Patterns harvested: 3 new (double-submit, back-after-success, 3p timeout)
```

## References

- ISTQB CTFL Syllabus 4.0 — Experience-based techniques
- B. Beizer — *Software Testing Techniques* (bug taxonomy)
- IEEE 1044 — Standard Classification for Software Anomalies
- J. Bach — *Heuristic Test Strategy Model*
- Cem Kaner — *Lessons Learned in Software Testing*
