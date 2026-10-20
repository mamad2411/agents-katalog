---
name: defect-prevention
description: Move from finding defects to preventing them — defect causal analysis, design checklists, lint/test gates, coding patterns, and process changes that eliminate recurring classes. Use when defect analysis shows recurring root causes.
source: self
date_added: 2026-05-01
---

# Defect Prevention

Detection has a ceiling; prevention compounds. This skill turns the output of defect analysis into design rules, lint/test gates, and process changes that eliminate **classes** of defects — not individual instances.

## Stack Baseline (2026)

| Concern | Default |
| --- | --- |
| Methods | DCA (Defect Causal Analysis), 5 whys, fishbone, ODC trends, Poka-Yoke |
| Code-time gates | ESLint/Biome, ruff, golangci-lint, ktlint, detekt, Sonar; security: Semgrep, CodeQL |
| Test gates | Mutation testing (Stryker/PIT), property-based, contract tests |
| Design gates | Architecture review, threat model, ADR template, design checklists |
| Process | PR template forcing checks; release readiness checklist; pre-merge contract verification |
| Metrics | Defect injection rate per phase, recurrence rate, prevention ROI |

## When to Use

- Same class of defect keeps appearing across releases.
- Post-incident: ensure the failure mode cannot recur.
- High-risk areas (auth, billing, data integrity) need belt-and-suspenders.
- Maturity step from reactive QA to engineering excellence.

## DCA Workflow

1. **Cluster defects by ODC type / root cause** (use defect-analysis output).
2. **Pick the dominant class** (e.g., "off-by-one in pagination").
3. **5 whys** to root cause; **fishbone** to surface contributing systemic factors (people, process, tooling, environment).
4. **Design preventive measures across phases**:
   - Code-time: lint rule, type, assertion
   - Test-time: mutation test, property-based test, contract test
   - Review-time: PR template question, design checklist
   - Build/release-time: gate or guardrail
5. **Pick the cheapest place to prevent** — earlier phases are cheaper but require sharper rules.
6. **Implement, measure recurrence**, tune.

## Worked Example — Off-by-one in pagination

| Where | Prevention |
| --- | --- |
| Code | Type-safe `Cursor<T>` with `next/prev`; forbid raw integer offsets via lint rule |
| Test | Property-based: `pages(N).flat() === all` and `last(page).next === first(page+1)` |
| Review | PR template asks: "Boundary cases tested? off-by-one for empty / single / last page?" |
| CI | Stryker mutation test on pagination module ≥ 85% score |
| Runbook | Pagination cookbook with a worked example |

After 1 quarter: 0 pagination defects (was 7/quarter).

## Poka-Yoke (Mistake-Proofing) Patterns

- **Make wrong code look wrong**: distinct types for `EmailAddress` vs. `string`; `OrderId` vs. `RefundId`.
- **Forbid dangerous patterns**: lint rule banning raw SQL string interpolation.
- **Replace with safer primitive**: `parseInt` → schema-validated DTO; `setTimeout` → typed scheduler.
- **Default to safe**: opt-in to side effects (`dryRun: true` default); idempotency keys required.
- **Visible state**: feature flags surfaced in UI footer in non-prod.

## Code Gates Library

### Custom ESLint rule (no raw offset)

```ts
// rules/no-raw-pagination-offset.ts
export default {
  create(ctx) {
    return {
      Property(node) {
        if (node.key.name === 'offset' && node.value.type === 'Literal') {
          ctx.report({ node, message: 'Use Cursor<T> instead of raw offset.' });
        }
      },
    };
  },
};
```

### Property-based test as gate

```ts
import fc from 'fast-check';
test('all pages partition the dataset', () => {
  fc.assert(fc.property(
    fc.array(fc.integer(), { minLength: 0, maxLength: 1000 }),
    fc.integer({ min: 1, max: 100 }),
    (data, size) => {
      const pages = paginate(data, size);
      expect(pages.flat()).toEqual(data);
      expect(pages.every(p => p.length <= size)).toBe(true);
    }));
});
```

### CodeQL custom query (security/data integrity)

```ql
import javascript
from CallExpr c
where c.getCalleeName() = "exec" and c.getAnArgument().getStringValue().regexpMatch(".*\\$\\{.*")
select c, "Possible string interpolation into shell — use array form."
```

## Process Patterns

- **PR template** with checkboxes derived from the most common defect classes ("Off-by-one verified? Idempotency considered? Deletes are soft? Logging avoids PII?").
- **ADR template** with explicit *Consequences* and *Mitigations*.
- **Threat model required** for any change to auth, billing, data export.
- **Release readiness gate** verifies a sample of these checks were run.

## Metrics

- **Defect recurrence rate**: same root cause appearing again — target ↓ over time.
- **Prevention ROI**: defects prevented (estimated) × avg cost vs. effort to implement gate.
- **Phase-injected → phase-found gap closing** (more caught earlier).
- **% PRs blocked by new gate** — should drop after a learning curve.

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| Endless detection investments | Convert findings into prevention; compound returns |
| Lint rule rolled out big-bang | Stage: warn → CI fail; codemod where possible |
| Vague "be careful" actions | Convert to a rule, type, or test |
| Prevention without measurement | Track recurrence; revert if no improvement |
| Over-engineering | Choose the cheapest layer that holds; don't gate every PR |
| Tribal mitigations | Write to KB; codify; auto-enforce |
| Blaming individuals | DCA targets systems, not people |

## Output Format

```
Prevention initiative — Off-by-one pagination
Driver: 7 defects in Q1; 4 reached prod
Root cause: raw integer offsets, no boundary tests
Measures:
  - Type-safe Cursor<T>; lint rule banning raw offsets (warn → fail)
  - Property-based test in shared lib (mandatory)
  - PR template question
  - Cookbook page
Owner: @platform   ETA: 2026-05-30
KPIs: recurrence Q2 ≤ 1; mutation score ≥ 85% on lib/pagination
Status @ Q2: 0 recurrences ✅; lint blocked 14 PRs (resolved by author)
```

## References

- *Defect Causal Analysis* — D. Card
- IBM ODC research — *Orthogonal Defect Classification*
- *Poka-Yoke* — S. Shingo
- Google Engineering Practices — *How to do a code review*
- M. Fowler — *Refactoring* (smells = recurring defects)
- ISO 25010 quality model
