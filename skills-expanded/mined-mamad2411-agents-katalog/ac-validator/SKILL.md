---
name: ac-validator
description: "Validates Acceptance Criteria quality (specific, testable, user-focused) and verifies AC fulfillment after task completion. Used by dor-validator (quality check) and sprint-executor (verification before task close)."
---

# AC Validator

Двойная роль:
1. **Quality validation** - проверяет что AC написаны правильно (used in DoR)
2. **Fulfillment verification** - проверяет что AC реально выполнены (used after task work)

## Quality validation (DoR phase)

### Quality criteria

Каждое AC должно быть:

#### Specific
- Concrete, не vague
- Bad: "system должна быть быстрой"
- Good: "Operation completes in <500ms for input of size N"

#### Testable
- Clear pass/fail criteria
- Bad: "code is clean"
- Good: "All functions have type annotations"

#### User-focused или behavior-focused
- Описывает observable behavior
- Bad: "Use Redux for state management" (implementation detail)
- Good: "When user clicks save, changes persist across page reload"

#### Independent
- Можно verify without depending on other AC
- Each AC stands alone

#### Negotiable
- Can be discussed before implementation
- Not so prescriptive that no engineering judgment remains

#### Verifiable
- Without subjective interpretation
- "Better UX" - subjective, bad
- "Page loads in 2 seconds" - objective, good

### Quality checks

For each AC:

```python
def validate_ac_quality(ac_text):
    checks = {
        'specific': not contains_vague_terms(ac_text),
        'testable': has_clear_pass_fail(ac_text),
        'user_focused': not is_implementation_detail(ac_text),
        'measurable_if_perf': has_threshold_if_perf(ac_text),
    }
    return checks
```

**Vague terms** flagged:
- "fast", "good", "clean", "better", "nice"
- "should", "could", "might" (vs "must")
- "appropriately", "adequately"

**Implementation details** flagged:
- "Use {framework}"
- "Implement using {pattern}"
- Specific class/function names

### Output (DoR phase)

For each AC: PASS/FAIL with specific issues.

```markdown
## AC Quality Check for T-2

AC 1: "User can register with email"
  ✓ Specific
  ✓ Testable
  ✓ User-focused
  Verdict: PASS

AC 2: "System should be fast"
  ✗ Specific - vague term "fast"
  ✗ Testable - no pass/fail criteria
  Verdict: FAIL
  Suggestion: Specify threshold like "Login completes in <500ms"

AC 3: "Use Redux for state management"
  ✗ User-focused - implementation detail
  Verdict: FAIL
  Suggestion: Reformulate as observable behavior, e.g., "User changes persist across navigation"
```

## Fulfillment verification (post-task phase)

Запускается после executor говорит task complete но перед `/sprint:checkin "task done"`.

### Workflow

For each AC of the task:

#### 1. Check evidence exists

What's expected based on test_approach:
- Unit tests for X → check test file exists, runs
- Integration test for flow → check exists, runs
- Property-based tests → check Hypothesis/fast-check tests exist

#### 2. Run verification

If tests can be run:
```bash
# Run only relevant tests for this task
pytest tests/ -k "test_user_registration"
# or
vitest run --grep "user registration"
```

Check exit code и output.

#### 3. Verify assertions match AC

Read test files. For each test asserting AC:
- Test name describes AC?
- Assertion checks the right thing?
- Pass condition matches AC pass condition?

This is heuristic check (LLM-based) - flag potential mismatches.

#### 4. Output

```markdown
## AC Fulfillment for T-2

AC 1: "User can register with email"
  Expected verification: test_user_registration_email
  Status: ✓ PASS
  Evidence: tests/test_auth.py::test_user_registration_email - PASS

AC 2: "Email format validated"
  Expected verification: test_email_format_validation
  Status: ✓ PASS
  Evidence: tests/test_auth.py::test_email_format_validation - PASS

AC 3: "Password hashed with bcrypt"
  Expected verification: test_password_hashing
  Status: ✗ FAIL
  Issue: Test exists but mocks the hash function - doesn't verify actual bcrypt usage
  Suggestion: Test should call real password.set_password() and check 
              the resulting hash starts with $2b$ (bcrypt prefix)
```

If any FAIL - task NOT done, executor must address.

## Special cases

### Audit/research tasks

AC might be:
- "All checklist items addressed"
- "Findings.json valid against schema"
- "Hot files identified"

Verification:
- Schema validation
- File presence
- Content sanity check (not empty, structured)

### Documentation tasks

AC might be:
- "All linked examples runnable"
- "All references resolve"

Verification:
- Run example code blocks
- Validate links
- Check claimed code references exist

### Refactoring tasks

AC like "no behavior change":
- Verification: full test suite passes (before и after diff is bit harder)
- Mutation score не degrades (if mutation testing enabled)

## Integration

Used by:
- **dor-validator** для quality check before task starts
- **sprint-executor** для fulfillment verification before task closes
- **dod-validator** для increment verification (cross-check AC vs increment artifacts)

## Output files

Per task, when AC validated:
`.sprints/active/ac-validation-T-{N}.md` with detailed results.
