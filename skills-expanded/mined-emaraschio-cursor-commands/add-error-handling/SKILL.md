---
name: add-error-handling
description: Add consistent error handling to the targeted code
user-invocable: false
---
## Overview

Implement comprehensive error handling for the current code to make it robust and resilient to failures while maintaining good user experience.

## Steps

1. **Error Detection**
    - Identify potential failure points and edge cases
    - Find unhandled exceptions and error conditions
    - Detect missing validation and boundary checks
    - Analyze async operations and network calls
2. **Error Handling Strategy**
    - Implement try-catch blocks where appropriate
    - Add input validation and sanitization
    - Create meaningful error messages and logging
    - Design graceful degradation for non-critical failures
3. **Recovery Mechanisms**
    - Implement retry logic for transient failures
    - Add fallback options for service unavailability
    - Create circuit breakers for external dependencies
    - Design proper error propagation and handling
4. **User Experience**
    - Provide clear error messages to users
    - Implement proper error status codes for APIs
    - Add loading states and error boundaries for UI
    - Include helpful suggestions for error resolution

## Add Error Handling Checklist

- [ ] Identified all potential failure points and edge cases
- [ ] Implemented try-catch blocks where appropriate
- [ ] Added input validation and sanitization
- [ ] Created meaningful error messages and logging
- [ ] Implemented retry logic for transient failures
- [ ] Added fallback options and circuit breakers
- [ ] Provided clear error messages to users
- [ ] Implemented proper error status codes for APIs
- [ ] Added loading states and error boundaries for UI

## Guardrails

- Never swallow errors silently; handle them meaningfully, or log and rethrow.
- Handle errors at meaningful boundaries instead of wrapping every call in try/catch.
- Do not commit, push, merge, or run destructive commands without explicit user consent.
- Never include secrets or credentials in error messages or logs; flag any exposure instead of printing or committing it.