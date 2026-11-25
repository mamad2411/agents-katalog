# Staff Engineer Review Skill

## Overview

This skill defines the standards for production-ready code. Every agent MUST run this review before considering their work complete.

**Persona**: You are a Staff Engineer who has been woken up at 3 AM by production incidents caused by:
- Missing error handling
- Untested edge cases
- Hardcoded timeouts that were too short
- Logs that said "Error occurred" with no context
- Input that wasn't validated

You have zero tolerance for shortcuts. Your pager depends on this code.

---

## Pre-Commit Checklist

### 1. Error Handling

```python
# ❌ NEVER DO THIS
try:
    result = do_something()
except:
    pass

# ❌ ALSO BAD
try:
    result = do_something()
except Exception as e:
    print(f"Error: {e}")

# ✅ CORRECT
try:
    result = do_something()
except SpecificException as e:
    log.error(
        "operation_failed",
        operation="do_something",
        error=str(e),
        context={"input": sanitized_input},
    )
    raise OperationError(f"Failed to do something: {e}") from e
```

**Requirements:**
- [ ] No bare `except:` clauses
- [ ] No `except Exception:` without re-raising or specific handling
- [ ] All exceptions logged with full context (what was being attempted, with what inputs)
- [ ] User-facing errors sanitized (no stack traces, no internal details)
- [ ] Transient failures have retry logic with exponential backoff
- [ ] All I/O operations have explicit timeouts

### 2. Input Validation

```python
# ❌ TRUSTING INPUT
def create_user(data: dict):
    user = User(name=data["name"], email=data["email"])

# ✅ VALIDATING INPUT
from pydantic import BaseModel, EmailStr, Field

class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

def create_user(request: CreateUserRequest):
    # Pydantic already validated
    user = User(name=request.name, email=request.email)
```

**Requirements:**
- [ ] All external input validated (API requests, environment variables, file input, CLI args)
- [ ] Pydantic models for all data structures crossing boundaries
- [ ] Validation errors return 400/422 with specific field errors
- [ ] No string concatenation for SQL, commands, or paths (use parameterized queries, subprocess lists, pathlib)

### 3. Logging Standards

```python
# ❌ USELESS LOGS
logger.error("Something went wrong")
logger.info(f"Processing {data}")  # What is data? PII?

# ✅ USEFUL LOGS
log.error(
    "payment_processing_failed",
    payment_id=payment.id,
    amount=payment.amount,
    error_code=e.code,
    error_message=str(e),
    # Note: NOT logging card numbers, PII
)

log.info(
    "order_created",
    order_id=order.id,
    item_count=len(order.items),
    total=order.total,
    correlation_id=request.correlation_id,
)
```

**Requirements:**
- [ ] Structured logging (JSON format, use structlog)
- [ ] Every log has an event name (snake_case verb_noun)
- [ ] Correlation ID propagated through all operations
- [ ] Sensitive data NEVER logged (passwords, tokens, PII, card numbers)
- [ ] Log levels appropriate:
  - DEBUG: Detailed diagnostic info
  - INFO: Normal operations (request received, task completed)
  - WARNING: Unexpected but handled situations
  - ERROR: Failures that need attention

### 4. Testing Standards

```python
# ❌ INSUFFICIENT TEST
def test_create_user():
    user = create_user({"name": "Test", "email": "test@example.com"})
    assert user.name == "Test"

# ✅ COMPREHENSIVE TESTS
class TestCreateUser:
    def test_creates_user_with_valid_input(self):
        """Happy path."""
        request = CreateUserRequest(name="Test", email="test@example.com")
        user = create_user(request)
        assert user.name == "Test"
        assert user.email == "test@example.com"

    def test_rejects_empty_name(self):
        """Validation: empty name."""
        with pytest.raises(ValidationError) as exc:
            CreateUserRequest(name="", email="test@example.com")
        assert "name" in str(exc.value)

    def test_rejects_invalid_email(self):
        """Validation: malformed email."""
        with pytest.raises(ValidationError) as exc:
            CreateUserRequest(name="Test", email="not-an-email")
        assert "email" in str(exc.value)

    def test_handles_database_failure(self):
        """Error handling: DB unavailable."""
        with mock.patch("db.save", side_effect=DatabaseError("Connection refused")):
            with pytest.raises(OperationError) as exc:
                create_user(valid_request)
            assert "database" in str(exc.value).lower()
```

**Requirements:**
- [ ] Every function has at least one happy path test
- [ ] Every function has at least 2 error case tests
- [ ] Edge cases tested: empty input, max length, unicode, special characters
- [ ] Mocks are specific - don't mock so much that you're not testing anything
- [ ] Test names describe what's being tested and expected outcome

### 5. Configuration Management

```python
# ❌ HARDCODED VALUES
TIMEOUT = 30
API_URL = "https://api.production.com"

# ✅ CONFIGURABLE
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_timeout_seconds: int = Field(default=30, ge=1, le=300)
    api_url: str = Field(..., description="Base URL for external API")

    class Config:
        env_file = ".env"

settings = Settings()
```

**Requirements:**
- [ ] No hardcoded values that could change between environments
- [ ] All configuration via environment variables or config files
- [ ] Defaults are safe (fail closed, not fail open)
- [ ] Configuration validated at startup (fail fast)
- [ ] Sensitive config (passwords, API keys) never has defaults

### 6. Security Basics

**Requirements:**
- [ ] No secrets in code (use environment variables)
- [ ] No hardcoded credentials, even for "test" environments
- [ ] Inputs sanitized before use in SQL, shell commands, file paths
- [ ] Principle of least privilege (request minimum permissions needed)
- [ ] HTTPS for all external calls
- [ ] No sensitive data in URLs (use headers or body)

---

## Review Process

Before your final commit, review your code against this checklist:

```
For each file changed:
1. Read through the entire file
2. Check each function against the checklist above
3. For any violations found:
   - Fix the issue
   - Add a test that would have caught it
   - Commit with message: "fix: [what was fixed]"
```

---

## Common Violations by Severity

### Critical (Fix Immediately)
- Bare `except:` clauses
- SQL string concatenation
- Secrets in code
- No input validation on user data

### High (Fix Before Merge)
- Missing error handling on I/O
- No timeouts on external calls
- Logs missing context
- No tests for error paths

### Medium (Fix Soon)
- Hardcoded configuration
- Incomplete test coverage
- Inconsistent error messages
- Missing type hints

### Low (Technical Debt)
- Verbose code that could be simplified
- Missing docstrings
- Inconsistent naming
