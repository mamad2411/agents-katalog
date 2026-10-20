---
name: test-strategy-designer
description: "Test strategy analyzer: classifies tests into Unit/Integration/E2E, builds the test pyramid profile (ideal 60/30/10), identifies untested modules, detects overly expensive tests, and recommends optimization priority. Read-only. Audience: Senior. Trigger: /test-strategy"
trigger: /test-strategy
---

## What this is for

A green test suite says nothing about strategy. You can have 100% line coverage
with end-to-end tests that take 40 minutes, or you can have a 60/30/10 pyramid
that catches regressions in seconds. This skill scans every test file,
classifies it by framework + setup pattern, builds the pyramid distribution,
and finds untested modules + tests whose cost exceeds their value.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/strategy-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each finding:

### Step 5

- **Pyramid health**: compare distribution to ideal 60/30/10 (unit/integration/e2e).

### Step 6

If unit count < 50% or e2e > 20%, flag as unhealthy.

### Step 7

- **Untested modules**: are any of these core domain modules? Are they

### Step 8

excluded by policy or genuinely at risk?

### Step 9

- **Expensive tests**: e2e tests that assert < 3 things or integration tests

### Step 10

with low assertion-to-setup ratio. Which can be rewritten as unit tests?

### Step 11

- **Mock complexity**: tests with 4+ mocks signal tight coupling. Which can

### Step 12

be refactored to reduce mocking?

### Step 13

5. Write `test-strategy-report.md` to the working directory.

## Usage

```
/test-strategy                           # interactive
/test-strategy <dir>                     # scan project
/test-strategy -help                     # show usage
```

Returns JSON with `unitTests[]`, `integrationTests[]`, `e2eTests[]`,
`testPyramid{unit, integration, e2e, total}`, `untestedModules[]`,
`assertionStats{}`, `mockComplexity{}`.
