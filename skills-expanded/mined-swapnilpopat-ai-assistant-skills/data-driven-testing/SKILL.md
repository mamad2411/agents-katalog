---
name: data-driven-testing
description: Run the same test logic across many input/output pairs using parameterized tests, data tables, and external fixtures — without copy-paste. Use for boundary, equivalence, decision-table, and matrix testing.
source: self
date_added: 2026-05-01
---

# Data-Driven Testing

Drive a single test body with N input rows so coverage scales with data, not code. Reduces duplication, makes intent obvious, and keeps assertions precise.

## Stack Baseline (2026)

| Stack | Mechanism |
| --- | --- |
| JUnit 5 | `@ParameterizedTest` + `@CsvSource` / `@MethodSource` / `@CsvFileSource` |
| pytest | `@pytest.mark.parametrize` + `pytest-cases` for complex matrices |
| Vitest / Jest | `it.each` / `describe.each` |
| xUnit (.NET) | `[Theory]` + `[InlineData]` / `[MemberData]` / `[ClassData]` |
| Go | Table-driven tests with subtests `t.Run(name, ...)` |
| Playwright | `test.describe.parallel` + array iteration; `testInfo.project.metadata` |
| Karate / Cucumber | Scenario Outline + Examples table |
| Property-based | jqwik (Java), fast-check (TS), Hypothesis (Python), proptest (Rust) |

## When to Use

- Boundary / equivalence partition coverage.
- Decision-table or business-rule matrices.
- Locale, currency, browser, device matrices.
- Spec-by-example / Gherkin Examples.
- Regression set fed from a CSV or a DB snapshot.

## Patterns

1. **Inline tables** for ≤ ~20 rows — keep them next to the test for readability.
2. **External fixtures** (CSV/JSON/YAML) for large or business-owned data.
3. **Generators** (factories, faker, builders) for randomized data with seed control.
4. **Property-based** for invariants ("for all valid inputs, output satisfies X").
5. **Name each row** so failures point to the offending case (`@DisplayName`, `ids=`, `{name}` template).
6. **Assert structurally** (object equality, JSON schema) instead of repeating field-by-field.

## Code

### JUnit 5

```java
@ParameterizedTest(name = "[{index}] {0} -> {1}")
@CsvFileSource(resources = "/discount-cases.csv", numLinesToSkip = 1)
void discountIsApplied(int qty, BigDecimal expectedTotal) {
    BigDecimal total = pricing.totalFor(qty, BigDecimal.valueOf(10));
    assertThat(total).isEqualByComparingTo(expectedTotal);
}
```

```csv
qty,expectedTotal
1,10.00
9,90.00
10,85.00
50,425.00
```

### pytest

```python
import pytest

CASES = [
    pytest.param("PT1H",  3600, id="one-hour"),
    pytest.param("PT90M", 5400, id="ninety-minutes"),
    pytest.param("P1D",  86400, id="one-day"),
]

@pytest.mark.parametrize("iso, expected_seconds", CASES)
def test_iso8601_to_seconds(iso, expected_seconds):
    assert duration.parse(iso).total_seconds() == expected_seconds
```

### Vitest

```ts
describe.each([
  { input: '',         valid: false, reason: 'empty' },
  { input: 'a@b.co',   valid: true  },
  { input: 'no-at.io', valid: false, reason: 'no @' },
])('isEmail("$input")', ({ input, valid, reason }) => {
  it(`returns ${valid}${reason ? ' (' + reason + ')' : ''}`, () => {
    expect(isEmail(input)).toBe(valid);
  });
});
```

### Property-based (fast-check)

```ts
import fc from 'fast-check';

test('reverse(reverse(xs)) === xs', () => {
  fc.assert(fc.property(fc.array(fc.integer()), xs => {
    expect(reverse(reverse(xs))).toEqual(xs);
  }));
});
```

### Playwright matrix

```ts
const locales = ['en-US', 'de-DE', 'ja-JP'] as const;
for (const locale of locales) {
  test(`pricing renders correctly in ${locale}`, async ({ page }) => {
    await page.goto(`/?locale=${locale}`);
    await expect(page.getByTestId('price')).toMatchSnapshot(`price-${locale}.png`);
  });
}
```

## Fixture Hygiene

- Keep fixtures in `tests/fixtures/<feature>/`. Version with the test code.
- For business-owned tables, mirror to a generated `*.md` so PMs/QA can read in PRs.
- Rotate / regenerate snapshot baselines deliberately, never blindly.
- Never read live production data — anonymize and snapshot first.

## Common Pitfalls

| Pitfall | Fix |
| --- | --- |
| One asserting test, 50 inputs, opaque failure | Name each row; assert per row, not in a loop with shared state |
| External CSV drifts from code expectations | Validate schema in a setup hook; fail loudly on missing columns |
| Random data without seed | Set a fixed seed; print it on failure for reproducibility |
| Mixing setup data into the row table | Keep inputs vs. setup separate; use fixtures for setup |
| Combinatorial explosion (locale × browser × theme × ...) | Use pairwise tools (PICT, Hypothesis `combine`) to cut size |
| "Update snapshots" used as a band-aid | Treat snapshot diffs as real review, not noise |

## Output Format

```
Suite: discount-pricing
  Cases: 24
  Passed: 23
  Failed: 1
    [12] qty=1000 expectedTotal=8000.00 actual=8500.00
        cause: bulk threshold off-by-one
  Coverage: equivalence partitions {1, 2..9, 10..49, 50..99, 100+}: 5/5
```

## References

- JUnit 5 Parameterized Tests: <https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests>
- pytest parametrize: <https://docs.pytest.org/en/stable/how-to/parametrize.html>
- Vitest each: <https://vitest.dev/api/#test-each>
- fast-check (property-based TS): <https://fast-check.dev/>
- Hypothesis (Python): <https://hypothesis.readthedocs.io/>
- ISTQB FL Syllabus 4.0 — black-box techniques
