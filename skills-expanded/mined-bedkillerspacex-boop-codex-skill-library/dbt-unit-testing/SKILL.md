---
name: dbt-unit-testing
description: >
  Write dbt unit tests for owned models using dbt native unit_tests (and/or
  established unit-test packages): mock inputs, assert output rows, and run
  fast PR checks without full warehouse refreshes. Use when validating
  transformation logic in isolation — pair with dbt-tests-and-docs for data
  tests on real relations.
---

# dbt Unit Testing

## Scope And Authorization

- **In scope:** dbt projects you develop; warehouse usage for unit tests should be minimal/ephemeral.
- **Out of scope:** Treating unit tests as a substitute for integration tests on production data quality.
- Prefer unit tests for conditional logic, date spine edge cases, and SCD quirks.
- Pair with `dbt-tests-and-docs` and `code-quality-standards`.

## When To Use

- Complex `case when`, window functions, or multi-`ref` transformations.
- Regression-proofing bug fixes with tiny fixtures.
- PR CI that should not build entire DAGs.
- Onboarding developers to model expected outputs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| uniqueness/freshness on real tables | `dbt-tests-and-docs` |
| Lineage/exposures | `dbt-exposures-lineage` |
| Full warehouse reconciliation | data QA skills |
| SQL style only | `sql-style-conventions` |
| Implementation quality baseline | `code-quality-standards` |

## Unit vs data tests

| | Unit tests | Data tests |
| --- | --- | --- |
| Inputs | Mocked rows | Real relations |
| Speed | Fast | Depends on data size |
| Purpose | Logic correctness | Data contract/quality |
| When | Every PR on logic | CI/scheduled on warehouses |

## Workflow

### 1. Confirm dbt version and approach

```bash
dbt --version
# Native unit tests available in modern dbt Core — check project dbt_version
```

If on older dbt, use team-approved package (e.g. historical `dbt_unit_testing` patterns) consistently.

### 2. Identify pure transformation under test

Prefer models with clear inputs/outputs. Extract hard logic into intermediate models if monolith SQL resists testing.

### 3. Author native unit test (illustrative YAML)

```yaml
# models/marts/schema.yml  (syntax may vary slightly by dbt version — consult current docs)
unit_tests:
  - name: test_fct_orders_cancelled_zero_revenue
    model: fct_orders
    given:
      - input: ref('stg_orders')
        rows:
          - {order_id: 1, status: cancelled, amount: 50}
          - {order_id: 2, status: paid, amount: 50}
    expect:
      rows:
        - {order_id: 1, order_total: 0}
        - {order_id: 2, order_total: 50}
```

Adapt to your dbt version’s exact `unit_tests` schema (rows as dict/list formats differ by release).

### 4. Run unit tests

```bash
dbt test --select "test_type:unit" 
# or
dbt test --select fct_orders,test_type:unit
```

Ensure CI job installs the same dbt version as local.

### 5. Fixture design tips

| Tip | Why |
| --- | --- |
| Minimal rows | Clarity |
| Named edge cases | DST boundaries, nulls, duplicates |
| Stable expected output | Sort expectations if order undefined |
| Mock all refs | Avoid accidental warehouse reads |
| One behavior per test | Easier failures |

### 6. Combine with data tests

1. Unit test encodes business rule.
2. Data test ensures warehouse still satisfies grain after load.
3. Do not drop data tests because unit tests pass.

### 7. Verify CI

```yaml
# Conceptual
- run: dbt deps
- run: dbt test --select "test_type:unit"
- run: dbt build --select state:modified+  # integration path separately
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Edge-case logic | Re-testing `select *` only |
| Fixtures | Tiny explicit rows | 10k-row CSV mocks |
| CI | Unit always; slim data tests | Only full prod refresh nightly |
| Version | Pinned dbt | YAML syntax drift across versions |
| Failures | Clear name per rule | One mega fixture |

## Output Checklist

- [ ] dbt version supports chosen unit method
- [ ] Critical logic models identified
- [ ] Unit tests for edge cases added
- [ ] Commands documented for developers
- [ ] CI runs unit tests on PR
- [ ] Data tests still present on marts
- [ ] Fixtures minimal and readable
- [ ] Expected rows deterministic
- [ ] Owners know how to update tests with model changes
- [ ] Residual untested paths ticketed

## Rules

- Unit tests mock logic; they do not prove pipeline freshness or volume.
- Keep fixtures human-readable.
- Focus on **dbt unit testing** of transformation logic.
