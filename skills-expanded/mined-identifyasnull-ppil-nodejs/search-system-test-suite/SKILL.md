---
name: "search-system-test-suite"
description: "Use when extending or validating the companions search-system test suite, fixtures, or regression docs."
intent: >-
  Provide a site-local workflow for building and maintaining the companions search-system comprehensive test suite: cover ranking, filtering, state tokens, breadcrumbs, fixtures, and regression documentation without drifting from the search contract.
type: workflow
best_for:
  - "Creating or extending search-system regression tests"
  - "Maintaining mock ads and search config fixtures"
  - "Documenting search-suite behavior and running instructions"
  - "Validating state token, breadcrumb, and ranking contracts"
scenarios:
  - "search ranking logic changes and needs coverage"
  - "state token or breadcrumb behavior regressed"
  - "search fixtures or docs need to match current search semantics"
---

# Search System Test Suite

## Purpose

Use this skill when the companions search system needs regression coverage for ranking, filtering, state-token persistence, breadcrumbs, or fixture-based search behavior.

## Overview

This test suite provides end-to-end coverage for the companions search system across two test files and shared fixtures:

1. `sites/companions/tests/search-system.comprehensive.test.js`
2. `sites/companions/tests/search-system.location-and-language.test.js`

Supporting artifacts:

- `sites/companions/tests/fixtures/mock-ads.json`
- `sites/companions/tests/fixtures/search-config.json`
- `sites/companions/tests/SEARCH_SYSTEM_TESTS.md`

The suite covers ranking, filtering, input parsing, state-token round trips, breadcrumb filtering, hierarchical location handling, language persistence, and deterministic ordering.

## Core Rules

- Keep the suite aligned to the search contract, not to incidental UI behavior.
- Treat the 7-field state token as the source of truth for pagination and breadcrumb continuity.
- Keep breadcrumb filtering at the search endpoint contract boundary.
- Use fixtures that cover both exact-match and edge-case ranking scenarios.
- Update docs whenever the suite shape or coverage claims change.

## Test Suite Scope

This workflow is centered on these artifacts:

- `sites/companions/tests/search-system.comprehensive.test.js`
- `sites/companions/tests/fixtures/mock-ads.json`
- `sites/companions/tests/fixtures/search-config.json`
- `sites/companions/tests/SEARCH_SYSTEM_TESTS.md`

## Coverage Areas

1. Exclusive criteria filtering and AND logic
2. Optional criteria ranking and match percentage calculations
3. Text query parsing and selector merging
4. Voice input handling and menu integration
5. State token round-trip behavior across pagination
6. Breadcrumb filtering and coin-count consistency
7. Deterministic result ordering and regression stability

### Detailed Scenarios

- Exclusive criteria never rank; they filter the result set.
- Optional criteria never filter; they rank by match percentage.
- State tokens preserve `selector`, `rawSelector`, `queryDerivedSelector`, `query`, `breadcrumb_criteria`, `queryDiagnostics`, and `lang`.
- Breadcrumbs are filtered once at the search endpoint and consumed from token state during listing.
- Location hierarchy supports Country → State → City → Suburb matching.
- Language-aware parsing and voice input preserve the original query and selected locale.

## Key Formulas

### Match Percentage

```javascript
const matchedProperties = count of properties where ad[prop] === selector[prop]
const totalProperties = count of properties in selector
matchPercent = (matchedProperties / totalProperties) * 100
```

### Deterministic Sorting

```javascript
sort by: matchPercent descending, then id ascending
```

### Exclusive vs Optional

```javascript
Exclusive: if (ad[category] !== selector[category]) return false;
Optional: matchPercent = calculateMatchPercentage(ad, selector);
```

## Quick Start

1. Update or add fixtures that model the behavior under test.
2. Keep ranking formulas and selector assumptions in sync with search config.
3. Add or extend tests for the changed search behavior.
4. Update the test documentation if the suite shape changes.
5. Run the search test suite and confirm regressions are covered.

## Test Coverage Summary

### search-system.comprehensive.test.js

- Exclusive criteria: category and gender filtering
- Optional criteria: ranking and match percentage
- Text query parsing and selector merging
- Voice-to-text processing
- Dialog criteria integration
- State token round-trips
- Breadcrumb filtering
- Result ranking and ordering
- End-to-end integration
- Pagination state consistency

### search-system.location-and-language.test.js

- Hierarchical location criteria
- Language parameter state persistence
- Language-specific query parsing
- Voice input with language selection
- Language persistence and breadcrumb labels
- Location + language integration

## Running the Tests

```bash
# Main search regression suite
npm test -- search-system.comprehensive.test.js

# Location and language suite
npm test -- search-system.location-and-language.test.js

# Specific suite
npm test -- search-system.comprehensive.test.js --testNamePattern="Exclusive Criteria"

# Coverage
npm test -- search-system*.test.js --coverage
```

## Regression Prevention

These tests catch regressions in:

- Breadcrumb filtering showing all criteria instead of user-selected criteria
- Exclusive criteria starting to rank instead of filter
- Match percentage calculation errors
- Result ordering becoming non-deterministic
- State token losing fields
- Menu selections being lost
- Pagination breaking result consistency

## Validation Checklist

- The test suite covers ranking, filtering, state, and breadcrumb behavior.
- Fixture data matches the current search contract.
- Coverage assertions and docs reflect the current suite shape.
- Regression tests fail for the bug before the fix and pass after.

## Common Failure Modes

- Fixture search properties drift from the current search config.
- Tests validate only the happy path and miss pagination or token round trips.
- Breadcrumb assertions rebuild state instead of validating token output.
- Test documentation claims coverage that the actual suite no longer provides.

## Anti-Patterns

- Hardcoding fixture behavior that no longer matches search config.
- Testing only happy-path ranking and skipping pagination or state-token cases.
- Rebuilding breadcrumbs in tests instead of validating the search contract.
- Letting docs drift from the actual fixture/test set.

## References

- `memories/repo/search-system-test-suite-created.md`
- `memories/repo/location-language-implementation.md`