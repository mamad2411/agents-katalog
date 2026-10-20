---
name: test-coverage-analysis
version: "1.0"
description: >
  Test coverage analysis, gap identification, and coverage configuration for Python and JavaScript.
  PROACTIVELY activate for: (1) Analyzing coverage reports, (2) Identifying critical coverage gaps,
  (3) Configuring coverage tools, (4) Setting up CI/CD coverage checks, (5) Branch coverage analysis.
  Triggers: "coverage", "uncovered", "pytest-cov", "istanbul", "c8", "coverage report", "coverage gap"
core-integration:
  techniques:
    primary: ["exhaustive_edge_case_enumeration"]
    secondary: ["completeness_verification"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Test Coverage Analysis Skill

## Metadata (Tier 1)

**Keywords**: coverage, uncovered, pytest-cov, istanbul, c8, coverage report

**File Patterns**: coverage.xml, lcov.info, coverage.json

**Modes**: testing_frontend, testing_backend

---

## Instructions (Tier 2)

### Python Coverage (coverage.py)

```bash
# Generate coverage
pytest --cov=src --cov-report=html --cov-report=term

# Configuration
[tool.coverage.run]
source = ["src"]
branch = true  # Enable branch coverage
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

### JavaScript/TypeScript Coverage

```bash
# Jest
npm test -- --coverage

# Vitest
vitest --coverage

# Configuration (vitest.config.ts)
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: {
        lines: 70,
        branches: 70,
        functions: 70,
        statements: 70
      }
    }
  }
});
```

### Coverage Gap Analysis

**Critical Gaps** (must cover):
1. Error handlers (try/except, catch blocks)
2. Boundary conditions (null, empty, max values)
3. Complex conditionals (nested if/else)
4. Security-sensitive code

**Example Gap Analysis**:
```
File: src/auth.py
Coverage: 45%

Uncovered Lines:
- 45-52: Password reset token generation (CRITICAL)
- 78-85: Email sending error handler (HIGH)
- 120-125: Edge case: empty email (MEDIUM)

Priority: Fix CRITICAL gaps first
```

### Branch Coverage

```python
def process(value):
    if value > 0:
        return "positive"  # Branch 1
    else:
        return "non-positive"  # Branch 2

# Need 2 tests to cover both branches
test_process_positive()  # Covers branch 1
test_process_zero()      # Covers branch 2
```

### Coverage in CI/CD

```yaml
# GitHub Actions
- name: Test with coverage
  run: pytest --cov=src --cov-report=json

- name: Check threshold
  run: |
    python scripts/coverage_validator.py
```

### Anti-Patterns

- Chasing 100% coverage without quality tests
- Ignoring branch coverage (only line coverage)
- Not testing error paths
- Excluding important files from coverage
