---
name: test-writer-updater
description: Create or update tests focused on changed behavior and regression safety.
tags: [testing, quality, regression]
---

# Test Writer Updater

## Use when
- New behavior needs coverage.
- Bugfix needs regression protection.

## Do not use when
- There is no deterministic test strategy yet.

## Procedure
1. Select smallest relevant test layer.
2. Add failing test for target behavior.
3. Implement or update minimal assertions.
4. Run targeted tests, then broader suite if needed.
5. Remove brittle or duplicate assertions.

## Validation
- New/updated tests fail before and pass after.
- Test names describe behavior clearly.

## Required output
- Tests added/updated.
- Scope covered and known gaps.
