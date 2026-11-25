---
name: verification-loop
description: Continuous validation through verification checkpoints, assertion quality, property-based testing, invariant checking, CI/CD validation, and automated feedback loops.
origin: AI Dev Kit
disable-model-invocation: false
---

# Verification Loop

Continuous validation methodology for ensuring code correctness throughout the development lifecycle. Covers verification checkpoints, assertion quality, property-based testing, invariant checking, CI/CD integration, and automated feedback loops. Use this skill when building robust verification infrastructure or establishing validation standards.

## When to Use

- Implementing verification infrastructure for critical systems
- Writing property-based tests for complex algorithms
- Setting up invariant checks for data pipelines
- Establishing verification gates in CI/CD pipelines
- Building feedback loops for automated code quality
- Designing assertion strategies for complex business logic
- Validating system behavior across edge cases

## Core Concepts

### The Verification Pyramid

```
         ┌─────────────────┐
         │   Formal Proof   │  ← Mathematical guarantees (rare)
        ├───────────────────┤
        │ Property-Based    │  ← Universal invariants
       ├────────────────────┤
       │ Integration Tests   │  ← Component interactions
      ├──────────────────────┤
      │ Unit Tests            │  ← Individual function correctness
     ├────────────────────────┤
     │ Type Checking + Lint    │  ← Static analysis (fast, cheap)
    └──────────────────────────┘
```

Each layer catches different classes of bugs. Verification is strongest when all layers are active.

### Verification Checkpoints

Insert verification at strategic points in the codebase:

```python
# contracts.py — Design by Contract pattern
from functools import wraps
from typing import Callable, Any

def requires(condition: Callable) -> Callable:
    """Precondition decorator — validate inputs before execution."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Bind arguments for predicate evaluation
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            if not condition(**bound.arguments):
                raise ValueError(
                    f"Precondition violated in {func.__name__}: "
                    f"{condition.__name__}({dict(bound.arguments)})"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

def ensures(condition: Callable) -> Callable:
    """Postcondition decorator — validate outputs after execution."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            if not condition(result, **bound.arguments):
                raise ValueError(
                    f"Postcondition violated in {func.__name__}: "
                    f"result={result}, args={dict(bound.arguments)}"
                )
            return result
        return wrapper
    return decorator

# Usage
def non_empty_list(lst):
    return len(lst) > 0

def result_is_sorted(result, lst):
    return result == sorted(lst)

@requires(non_empty_list)
@ensures(result_is_sorted)
def sort_list(lst: list) -> list:
    return sorted(lst)

sort_list([3, 1, 2])  # ✓ Returns [1, 2, 3]
sort_list([])          # ✗ Raises ValueError: Precondition violated
```

### Property-Based Testing

Instead of individual examples, test universal properties that must hold for all inputs.

**Python with Hypothesis:**

```python
from hypothesis import given, strategies as st, settings
from hypothesis.errors import InvalidArgument

# Property: reversing a list twice returns the original
@given(st.lists(st.integers()))
def test_reverse_twice_is_identity(lst):
    reversed_once = lst[::-1]
    reversed_twice = reversed_once[::-1]
    assert reversed_twice == lst

# Property: sorted list length equals original length
@given(st.lists(st.integers()))
def test_sort_preserves_length(lst):
    assert len(sorted(lst)) == len(lst)

# Property: sorted list is non-decreasing
@given(st.lists(st.integers()))
def test_sort_produces_ordered_list(lst):
    result = sorted(lst)
    for i in range(len(result) - 1):
        assert result[i] <= result[i + 1]

# Property: all elements in sorted output exist in input
@given(st.lists(st.integers()))
def test_sort_permutes_elements(lst):
    result = sorted(lst)
    assert sorted(lst) == sorted(result)  # Same multiset

# Complex property: JSON round-trip
import json
from hypothesis import given, strategies as st

@given(st.recursive(
    st.one_of(st.integers(), st.floats(allow_nan=False), st.text(), st.booleans()),
    st.lists,
    st.dictionaries,
    max_leaves=10
))
def test_json_roundtrip(data):
    """Any JSON-serializable value round-trips through dumps/loads."""
    serialized = json.dumps(data)
    deserialized = json.loads(serialized)
    assert deserialized == data
```

**TypeScript with fast-check:**

```typescript
import { fc, assert, property } from 'fast-check'

// Property: string reversal is involutive
test('reverse(reverse(s)) === s', () => {
  fc.assert(
    property(fc.string(), (s: string) => {
      const reverse = (str: string) => str.split('').reverse().join('')
      return reverse(reverse(s)) === s
    })
  )
})

// Property: array concat is associative
test('(a ++ b) ++ c === a ++ (b ++ c)', () => {
  fc.assert(
    property(
      fc.array(fc.integer()),
      fc.array(fc.integer()),
      fc.array(fc.integer()),
      (a, b, c) => {
        const concat = (x: number[], y: number[]) => [...x, ...y]
        const left = concat(concat(a, b), c)
        const right = concat(a, concat(b, c))
        expect(left).toEqual(right)
      }
    )
  )
})

// Property: binary search returns correct index or -1
test('binary search finds element or returns -1', () => {
  fc.assert(
    property(
      fc.array(fc.integer()).map(arr => [...new Set(arr)].sort((a, b) => a - b)),
      fc.integer(),
      (sortedArr: number[], target: number) => {
        function binarySearch(arr: number[], target: number): number {
          let lo = 0, hi = arr.length - 1
          while (lo <= hi) {
            const mid = Math.floor((lo + hi) / 2)
            if (arr[mid] === target) return mid
            if (arr[mid] < target) lo = mid + 1
            else hi = mid - 1
          }
          return -1
        }

        const idx = binarySearch(sortedArr, target)
        if (idx === -1) {
          expect(sortedArr).not.toContain(target)
        } else {
          expect(sortedArr[idx]).toBe(target)
        }
      }
    )
  )
})
```

### Invariant Checking

Invariants are conditions that must always be true at a specific point in execution.

```python
# invariants.py — Data pipeline invariants
from dataclasses import dataclass
from typing import Any

class InvariantViolation(Exception):
    pass

@dataclass
class UserRecord:
    id: str
    email: str
    created_at: str
    status: str  # 'active', 'suspended', 'deleted'

class UserPipeline:
    """Pipeline with invariant checks at each stage."""

    VALID_STATUSES = {'active', 'suspended', 'deleted'}

    def _check_invariant(self, condition: bool, message: str):
        if not condition:
            raise InvariantViolation(message)

    def validate_input(self, record: UserRecord):
        """Stage 1: Validate raw input."""
        self._check_invariant(record.id is not None, "User ID cannot be None")
        self._check_invariant('@' in record.email, f"Invalid email: {record.email}")
        self._check_invariant(
            record.status in self.VALID_STATUSES,
            f"Invalid status: {record.status}"
        )

    def transform(self, record: UserRecord) -> dict:
        """Stage 2: Transform record."""
        result = {
            "user_id": record.id,
            "email": record.email.lower().strip(),
            "created_at": record.created_at,
            "is_active": record.status == 'active',
        }

        # Post-transform invariant
        self._check_invariant(
            result["email"] == result["email"].lower().strip(),
            "Email was not properly normalized"
        )
        self._check_invariant(
            isinstance(result["is_active"], bool),
            "is_active must be boolean"
        )

        return result

    def process_batch(self, records: list[UserRecord]) -> list[dict]:
        results = []
        for record in records:
            self.validate_input(record)
            transformed = self.transform(record)
            results.append(transformed)

        # Batch-level invariant
        self._check_invariant(
            len(results) == len(records),
            f"Output count ({len(results)}) != input count ({len(records)})"
        )

        # All IDs unique invariant
        output_ids = [r["user_id"] for r in results]
        self._check_invariant(
            len(output_ids) == len(set(output_ids)),
            "Duplicate user IDs in output"
        )

        return results
```

### Assertion Quality

Good assertions are specific, independent, and meaningful:

```python
# BAD: Vague assertion — what are we checking?
assert result is not None

# GOOD: Specific assertion with context
assert result is not None, "get_user() returned None for existing user_id"

# BAD: Overly broad — hides which condition failed
assert user.status == "active" and user.email_verified and user.plan != "free"

# GOOD: Separate, named assertions
assert user.status == "active", f"Expected active, got {user.status}"
assert user.email_verified, f"User {user.id} email not verified"
assert user.plan != "free", f"User {user.id} on free plan, expected paid"
```

**Python with descriptive assertions:**

```python
def test_payment_processing():
    """Payment flow produces correct ledger entries."""
    result = process_payment(order_id="ord_123", amount=99.99, currency="USD")

    # Structural assertions
    assert isinstance(result, PaymentResult)
    assert result.status == "completed"
    assert result.transaction_id.startswith("txn_")

    # Value assertions
    assert result.amount == 99.99
    assert result.currency == "USD"
    assert result.fee == 2.99  # 3% processing fee

    # Side-effect assertions
    ledger_entry = db.ledger.get(result.transaction_id)
    assert ledger_entry is not None, "No ledger entry created"
    assert ledger_entry.debit == 99.99
    assert ledger_entry.credit == 97.00  # Amount minus fee

    # Temporal assertion
    assert ledger_entry.created_at > order.created_at
```

## Verification in CI/CD

### Gate Configuration

```yaml
# .github/workflows/verification.yml
name: Verification Gates
on:
  pull_request:
    branches: [main]

jobs:
  static-analysis:
    name: Static Analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install mypy ruff bandit
      - run: mypy app/ --strict
      - run: ruff check .
      - run: bandit -r app/ -f json -o bandit-report.json
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: bandit-report
          path: bandit-report.json

  unit-tests:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest --cov=app --cov-fail-under=80 --cov-report=xml
      - uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml

  property-tests:
    name: Property-Based Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/properties/ -v --hypothesis-seed=0
        # Fixed seed for reproducibility in CI

  integration-tests:
    name: Integration Tests
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - run: pytest tests/integration/ -v
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test

  verification-gate:
    name: Verification Gate
    needs: [static-analysis, unit-tests, property-tests, integration-tests]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Check all gates passed
        run: |
          if [[ "${{ needs.static-analysis.result }}" != "success" ]] ||
             [[ "${{ needs.unit-tests.result }}" != "success" ]] ||
             [[ "${{ needs.property-tests.result }}" != "success" ]] ||
             [[ "${{ needs.integration-tests.result }}" != "success" ]]; then
            echo "Verification gate failed"
            exit 1
          fi
          echo "All verification gates passed ✓"
```

### Feedback Loop Automation

```python
# scripts/verification_feedback.py
"""
Automated feedback loop: when verification fails,
generate a diagnostic report and suggest fixes.
"""
import json
import subprocess
from pathlib import Path

def run_verification():
    """Run full verification suite and collect results."""
    results = {
        "lint": run_command("ruff check . --output-format json"),
        "types": run_command("mypy app/ --no-error-summary"),
        "unit": run_command("pytest tests/unit/ -v --tb=short"),
        "properties": run_command("pytest tests/properties/ -v --tb=short"),
        "security": run_command("bandit -r app/ -f json"),
    }
    return results

def analyze_failures(results: dict) -> list[dict]:
    """Analyze verification failures and generate suggestions."""
    issues = []

    if results["lint"]["returncode"] != 0:
        issues.append({
            "category": "lint",
            "severity": "warning",
            "message": "Linting violations detected",
            "suggestion": "Run `ruff check . --fix` to auto-fix",
        })

    if results["types"]["returncode"] != 0:
        error_count = results["types"]["stderr"].count("error:")
        issues.append({
            "category": "types",
            "severity": "error",
            "message": f"{error_count} type errors found",
            "suggestion": "Check mypy output for specific type mismatches",
        })

    if results["security"]["returncode"] != 0:
        security_data = json.loads(results["security"]["stdout"])
        high_severity = [r for r in security_data.get("results", []) if r["issue_severity"] == "HIGH"]
        if high_severity:
            issues.append({
                "category": "security",
                "severity": "critical",
                "message": f"{len(high_severity)} high-severity security issues",
                "suggestion": "Review bandit report and fix security violations",
            })

    return issues

def generate_feedback_report(issues: list[dict]) -> str:
    """Format issues as actionable feedback."""
    report = "# Verification Feedback Report\n\n"

    for issue in sorted(issues, key=lambda x: {"critical": 0, "error": 1, "warning": 2}[x["severity"]]):
        icon = {"critical": "🚨", "error": "❌", "warning": "⚠️"}[issue["severity"]]
        report += f"{icon} **[{issue['category'].upper()}]** {issue['message']}\n"
        report += f"   → {issue['suggestion']}\n\n"

    return report
```

## Continuous Verification Checklist

### Pre-Commit

- [ ] Type checker passes with zero errors
- [ ] Linter has no violations (or approved noqa)
- [ ] Unit tests pass (fast, < 30 seconds)
- [ ] No new security warnings from SAST

### Pre-Merge

- [ ] Property-based tests pass (reproduce with fixed seed)
- [ ] Integration tests pass against test database
- [ ] Coverage meets threshold (≥80% line, ≥70% branch)
- [ ] Invariant checks added for new business logic
- [ ] Pre/post conditions documented for complex functions

### Post-Merge

- [ ] E2E smoke tests pass in staging
- [ ] Performance benchmarks within 5% of baseline
- [ ] Security scan shows no new critical vulnerabilities
- [ ] Monitoring alerts configured for new endpoints

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `assert False` without message | No context on why it failed | Always include descriptive message |
| Asserting implementation details | Tests break on refactor | Assert observable behavior |
| Single assertion per test function | One failure hides others | Multiple focused assertions OK |
| No property-based testing | Edge cases missed by examples | Use Hypothesis/fast-check |
| Verification only in CI | Slow feedback loop | Run quick checks pre-commit |
| Ignoring invariant violations | Data corruption goes undetected | Fail fast with clear errors |
| Flaky property test seeds | Non-reproducible failures | Fix seed in CI, randomize locally |

## Best Practices

1. **Verify at every layer** — static analysis, unit, property, integration, E2E
2. **Use design by contract** — preconditions, postconditions, invariants
3. **Property-test complex logic** — simple logic can use examples
4. **Fixed seeds in CI** — reproducibility is more important than randomness
5. **Fail fast, fail loud** — early invariant checks with descriptive errors
6. **Automate the feedback loop** — verification results should trigger suggested fixes
7. **Track verification metrics** — pass rate, time to feedback, flaky test count
8. **Don't verify the obvious** — focus on business logic, not language guarantees
9. **Make verification cheap** — pre-commit checks should complete in seconds
10. **Document invariants** — they're part of the interface contract

## Success Metrics

- [ ] All verification gates pass on every PR
- [ ] Property-based tests cover complex algorithms and data transformations
- [ ] Invariants documented for all critical business logic
- [ ] Pre-commit hooks complete in under 10 seconds
- [ ] Full verification suite completes in under 15 minutes
- [ ] Zero false-positive failures in verification pipeline
- [ ] Feedback report generated automatically on failure

---

**Remember:** Verification isn't a phase — it's a continuous discipline. Every line of code should be verified at the appropriate level of rigor.
