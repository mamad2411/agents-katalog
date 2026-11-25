# /project:test-design

**Interactive QA Test Design & Matrix Creation**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:test-design AB#123
/project:test-design AB#123 --scope=unit+integration
/project:test-design AB#123 --create-automation
```

## What This Does

1. **Loads story AC** and system design
2. **Creates test matrix** (happy path, edge cases, errors)
3. **Designs test cases** (Gherkin format)
4. **Generates automation scripts** (if applicable)
5. **Documents manual testing** approach
6. **Creates QA tasks** in ADO

## Interactive Flow

```
User: /project:test-design AB#123

Claude: 🧪 Test Design & Matrix

✅ STORY LOADED:
  Story: Phone verification & OTP (AB#123)
  AC: 6 items (phone entry, OTP, validation, errors, edge cases)

📊 TEST MATRIX:

Test Scope:
  [1] Unit tests only (backend business logic)
  [2] Integration tests (API endpoints + DB)
  [3] End-to-end tests (UI flow)
  [4] All of above (complete coverage)

User: [4]

Generating test matrix for complete coverage...

UNIT TESTS (Backend):
  UT-01: ValidatePhone with valid US number → PASS
  UT-02: ValidatePhone with invalid format → throw ValidationException
  UT-03: GenerateOTP creates 6-digit code → PASS
  UT-04: VerifyOTP with correct code → return session
  UT-05: VerifyOTP with expired OTP → throw ExpiredException
  UT-06: VerifyOTP with max attempts exceeded → throw LockedException
  (6 total, ~2 hours)

INTEGRATION TESTS (API):
  IT-01: POST /signup/initiate with valid phone → 200 + session_id
  IT-02: POST /signup/initiate with existing user → 400 conflict
  IT-03: POST /signup/verify-otp with valid code → 200 + token
  IT-04: POST /signup/verify-otp with expired OTP → 400 expired
  IT-05: POST /signup/verify-otp rate limiting → 429 too many requests
  IT-06: Concurrent requests don't cause race conditions → PASS
  (6 total, ~3 hours)

END-TO-END TESTS (UI):
  E2E-01: Happy path flow (phone → OTP → success) → PASS
  E2E-02: Phone validation error → user corrects & retries → PASS
  E2E-03: OTP expiration → resend code flow → PASS
  E2E-04: Network failure → retry logic → PASS
  (4 total, ~4 hours via Selenium/Cypress)

PERFORMANCE TESTS:
  PERF-01: Load test signup API (100 concurrent users) → P95 <200ms
  PERF-02: Database query time with 100k users → <50ms
  (2 total, ~3 hours)

TOTAL: 18 test cases, ~12 hours QA effort

CREATE TEST CASES (GHERKIN FORMAT)?
  [1] Yes, generate all test cases
  [2] Generate selected scope
  [3] Preview first
  [4] Skip, create manually

User: [1]

Generating test cases...

**UT-01: ValidatePhone - Valid US Number**
```gherkin
Feature: Phone Validation
  Scenario: Validate US phone number
    Given phone validator is initialized
    When I validate phone "+1-555-1234567"
    Then validation should PASS
    And phone should be normalized to "+15551234567"
```

**IT-02: API - Existing User Conflict**
```gherkin
Feature: Signup Initiation
  Scenario: User already exists with phone
    Given user with phone "+15551234567" exists
    When I POST to /api/v1/signup/initiate
      With body: { "phone": "+1-555-1234567" }
    Then response status is 400
    And error message contains "PHONE_ALREADY_REGISTERED"
```

**E2E-01: Happy Path Flow**
```gherkin
Feature: Signup Flow
  Scenario: Complete signup from phone to success
    Given signup page is loaded
    When I enter phone "+15551234567"
    And I click "Send OTP"
    Then I see "OTP sent" confirmation
    And I wait for SMS message
    And I enter received OTP code
    And I click "Verify"
    Then I see "Profile Setup" page
```

[Generate all test cases...]

✓ Generated 18 test cases in Gherkin format
✓ Saved test matrix to .sdlc/memory/test-design-AB#123.md

CREATE QA TASKS IN ADO?
  [1] Yes, create all test tasks
  [2] Just save test matrix
  [3] Preview first

User: [1]

✓ Created QA-01, QA-02, QA-03 tasks in ADO
✓ Linked to story AB#123
✓ Assigned to QA team
✓ Test design complete
```

## CLI Mode

```bash
$ sdlc skill test-design AB#123 --scope=unit+integration
$ sdlc skill test-design AB#123 --create-automation
$ sdlc skill test-design AB#123 --post-comments
```

## Outputs

- **Test Matrix**: Coverage map (unit, integration, E2E, performance)
- **Gherkin Test Cases**: All scenarios in BDD format
- **Test Scripts**: Automation code (if applicable)
- **QA Tasks**: Created in ADO with estimates

## G7 Gate Clear Conditions

Gate G7 is CLEAR when:
- Test matrix designed (all states covered)
- Gherkin test cases written (or recorded)
- Automation scripts passing (if applicable)
- Manual test execution plan documented
- No test blockers identified

## Next Commands

- `/project:performance-testing AB#123` - Performance validation
- `/project:staging-validation AB#123` - SIT/UAT validation
- `/project:deployment AB#123` - Deployment prep

---

## Model & Token Budget
- **Model Tier:** Sonnet (test generation)
- Input: ~1.5K tokens (story + AC)
- Output: ~2.5K tokens (test matrix + cases)

