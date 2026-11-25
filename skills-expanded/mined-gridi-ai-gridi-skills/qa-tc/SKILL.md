---
name: qa-tc
description: >
  A skill that writes test cases (TCs) based on tech specs and user scenarios.
  It generates systematic test cases including functional tests, boundary value tests, and exception handling tests.
  Use this skill when test case writing, TC documentation, or QA preparation is requested.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

# QA Test Case Generator

Analyzes tech specs and user scenarios to generate test cases.

## Workflow

### 1. Verify Input Documents

Receive the following documents as input:
- Tech spec document
- User story document

```
Example input:
- "Write test cases based on docs/tech-specs/account-tech-spec.md"
```

### 2. Requirements Analysis

1. Extract user scenarios
2. Extract acceptance criteria (AC)
3. Extract API endpoint list
4. Identify business rules

### 3. Generate Test Cases

#### Test Case Format (Given-When-Then)

Test cases are written in **Given-When-Then (GWT)** format. This BDD (Behavior-Driven Development) style clearly communicates the intent of each test.

| Component | Description | Example |
|-----------|-------------|---------|
| **Given** | Preconditions, initial state | "The user is on the login page" |
| **When** | Action/event under test | "The user clicks the login button with valid credentials" |
| **Then** | Expected result, verification items | "The user is redirected to the dashboard page" |

```markdown
# [Feature Name] Test Cases

## Test Overview

| Item | Details |
|------|---------|
| Feature Name | Sign Up |
| Related Document | account-tech-spec.md |
| Created Date | 2024-01-15 |
| Version | 1.0 |

## Test Scope

### Included
- Email sign-up
- Social sign-up (Google, Kakao)
- Input validation

### Excluded
- Email verification flow (separate TC)
- Performance testing

---

## TC-001: Normal Email Sign-up

**Priority**: High
**Test Type**: Positive
**Related Story**: US-001

### Test Data
| Field | Value |
|-------|-------|
| Email | test@example.com |
| Password | Test1234! |
| Confirm Password | Test1234! |

### Given (Preconditions)
- The sign-up page is accessible
- An unused test email (test@example.com) is prepared
- No user is registered with this email in the database

### When (Execution)
- The user enters "test@example.com" in the email field
- The user enters "Test1234!" in the password field
- The user enters "Test1234!" in the confirm password field
- The user clicks the sign-up button

### Then (Expected Result)
- HTTP 201 response is returned
- The user is redirected to the email verification guide page
- A user record is created in the database
- Account status is set to "Email Unverified"
- A verification email is sent

---

## TC-002: Duplicate Email Sign-up Failure

**Priority**: High
**Test Type**: Negative
**Related Story**: US-001

### Test Data
| Field | Value |
|-------|-------|
| Email | test@example.com (duplicate) |
| Password | Test1234! |

### Given (Preconditions)
- A user is already registered with the email test@example.com
- The sign-up page is accessible

### When (Execution)
- The user fills out the sign-up form with the duplicate email (test@example.com)
- The user clicks the sign-up button

### Then (Expected Result)
- HTTP 409 response is returned
- Error message "This email is already registered" is displayed
- Error styling is applied to the email field
- No new user record is created

---
```

### 4. Generate Test Cases by Type

#### Positive Test (Normal Cases)
- Happy Path for all user scenarios

#### Negative Test (Failure Cases)
- Validation failure
- No permission
- Resource not found

#### Boundary Test
- Minimum/maximum input values
- Empty values
- Values just before/after boundaries

#### Security Test
- Access without authentication
- SQL Injection
- XSS

### 5. File Output

```
{project-root}/docs/{backlog-keyword}/test-cases.md
```

> **Directory Rule**: All artifacts are stored under the backlog-keyword directory.

## Test Case ID Rules

```
TC-{feature-code}-{type}-{sequence}

Examples:
TC-AUTH-P-001  : Authentication Positive test 001
TC-AUTH-N-001  : Authentication Negative test 001
TC-AUTH-B-001  : Authentication Boundary test 001
TC-AUTH-S-001  : Authentication Security test 001
```

## Priority Criteria

| Priority | Criteria | Example |
|----------|----------|---------|
| Critical | Core feature unavailable | Cannot log in |
| High | Major feature affected | Sign-up failure |
| Medium | Partial feature limitation | Password recovery failure |
| Low | Usability issue | UI alignment error |

## Test Data Guide

Detailed guide: [references/test-data-guide.md](references/test-data-guide.md)

## References

- Test Data Guide: [references/test-data-guide.md](references/test-data-guide.md)
- Test Case Template: [references/tc-template.md](references/tc-template.md)
