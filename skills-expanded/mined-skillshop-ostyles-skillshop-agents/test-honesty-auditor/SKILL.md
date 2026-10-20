---
name: test-honesty-auditor
description: "Test honesty auditor: statically detects 6 categories of tests-that-cannot-fail (zero-assertion tests, tautological assertions, tests that assert on their own mocks, try-around-assert swallowing, rotting disabled/skipped tests, ambiguous disabled-state). Auto-bucketizes each test, then LLM judges which actually pin down behavior vs. which pass by accident. Risk-tiered report with proposed minimal fixes. Read-only. Audience: Both. Trigger: /test-honesty"
trigger: /test-honesty
---

## What this is for

A green test suite means nothing if the tests cannot fail. This skill audits
test files for the failure modes that turn coverage into theater: tests
without assertions, tautological assertions (`expect(true).toBe(true)`), tests
that assert on mocks they themselves just configured (proving the mock, not
the code), try/catch swallowing assertion errors, and disabled/skipped tests
that have not been touched since months.

The collector is a fast static scan; the LLM is what judges for each
candidate whether the test could ever fail and what it actually pins down.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/test-scan.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each suspicious test:

### Step 5

- Read the `body` (600 chars of test source).

### Step 6

- Could this test ever fail? If yes, what behavior does it pin down?

### Step 7

- Classify: `honest` / `cannot-fail` / `tests-the-mock` / `tautological`

### Step 8

/ `rotting-skip` / `try-around-assert`.

### Step 9

5. Confidence: `proven` (clearly cannot fail), `likely` (suspicious context),

### Step 10

`suspected` (judgment call).

### Step 11

6. Propose a minimal fix per finding.

### Step 12

7. Write `test-honesty-report.md` to the working directory.

## Usage

```
/test-honesty                         # interactive, prompts for directory
/test-honesty <dir>                   # scan project test directories
/test-honesty -help                   # show usage
```

Returns JSON with `tests[]` per test case:
`{file, line, name, runner, assertionCount, disabled, tryAroundAssert,
tautologySuspicion, disabledSinceDays?, body}` plus summary counts.

## Report Format

`test-honesty-report.md` with:
- Executive summary (total tests, % honest vs cannot-fail, oldest skip)
- Critical findings (proven cannot-fail - the green tick is theater)
- Medium findings (suspicious mock-assertion, swallowing assertion errors)
- Low findings (tautologies, very short tests with no clear intent)
- Skip age histogram (skip markers older than 30 / 90 / 365 days)
- False positives (dismissed with reason)
- Open questions (suspected, needs human review)
