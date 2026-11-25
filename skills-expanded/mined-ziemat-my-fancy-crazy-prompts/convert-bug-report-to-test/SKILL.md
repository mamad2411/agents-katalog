name: convert-bug-report-to-test
description: Turns a bug report into a reproducible failing or regression test in Python. Use this when you need to convert a bug description, incident report, or user complaint into a test that reproduces the issue.

---

# Convert Bug Report to Test

## Purpose

Turn a bug report into a reproducible failing or regression test in Python. This skill converts bug descriptions, incident reports, or user complaints into tests that clearly reproduce the issue and verify the fix.

## Use when

- Converting a bug report into a test
- Creating regression tests after fixing an issue
- Reproducing an intermittent or hard-to-catch bug
- Documenting a bug with an automated test
- Onboarding new developers to understand a bug

## Do not use when

- You're writing tests for new functionality
- The bug report is too vague to reproduce
- You need to design a comprehensive test suite

## Inputs

- Bug report or incident description
- Error messages or stack traces
- Reproduction steps (if available)
- Expected vs actual behavior
- Fixed code (if already fixed)

## Outputs

- Reproducible test case that demonstrates the bug
- Clear test name describing the issue
- Assertions that capture expected vs actual behavior
- Optional: minimal reproduction script

## Method

1. **Extract key information**
   - What was the expected behavior?
   - What was the actual behavior?
   - What input triggered the bug?
   - What was the error message (if any)?

2. **Create minimal reproduction**
   - Strip away unrelated code
   - Focus on the specific failure scenario
   - Make the test self-contained
   - Include all necessary setup

3. **Write the test**
   - Name: `test_<bug_description>_<scenario>`
   - Include the reproduction steps as comments
   - Add assertions for both expected and actual behavior
   - Use `pytest.xfail` if the bug is known and unfixed

4. **Verify the test**
   - Confirm it fails with the buggy code
   - Confirm it passes with the fixed code
   - Ensure it's not flaky or timing-dependent
   - Check that it's not over-specified

5. **Document the bug**
   - Add link to bug tracker or incident report
   - Include context in test comments
   - Note any workarounds or related issues

## Test Structure for Bug Reports

```python
def test_bug_<issue_number>_<description>():
    """
    Reproduce: <brief description>
    Issue: <link to bug tracker>
    Expected: <expected behavior>
    Actual: <buggy behavior before fix>
    
    Steps to reproduce:
    1. ...
    2. ...
    """
    # Test code here
```

## Guardrails

- Don't make the test more complex than necessary to reproduce the bug
- Don't test unrelated functionality
- Don't write a test that only passes because of unrelated changes
- Make sure the test would fail if the bug returns

## Example prompts

```
Convert this bug report to a test:

Bug: User authentication fails when password contains Unicode characters
Error: "UnicodeEncodeError: 'ascii' codec can't encode character"
Steps:
1. Create user with password "pässwörd"
2. Attempt to log in
3. Authentication fails with Unicode error

---

Create a test for this incident:

Incident: Payment webhook handler crashed on duplicate events
Root cause: Handler didn't check for already-processed events
Error: "IntegrityError: UNIQUE constraint failed"
Fix: Added idempotency check before processing

---

Convert this user complaint to a test:

User report: "When I upload a PDF larger than 10MB, the app just spins forever"
Expected: Show error message "File too large"
Actual: Timeout after 30 seconds
Code: File upload handler with 30s timeout
