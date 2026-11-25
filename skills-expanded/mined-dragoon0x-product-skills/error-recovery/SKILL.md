---
name: error-recovery
description: "When things break, guide people forward instead of leaving them stranded. Error message copy, retry patterns, graceful degradation, and recovery flows. Use when building error handling or failed state UIs."
---

# Error Recovery

When things break, guide people forward instead of leaving them stranded.

## How to use

- `/error-recovery` Apply error recovery constraints to this conversation.

## Constraints

### Error Message Structure
- What happened (in plain language, not error codes)
- Why it might have happened (if knowable)
- What the user can do about it (specific action)
- NEVER show raw error codes, stack traces, or technical jargon to end users
- MUST log the technical details for debugging separately

### Recovery Patterns
- Auto-retry for transient failures (network timeout, rate limit) with backoff
- Save user input before showing errors. NEVER lose their work.
- Offer offline functionality for core features when possible
- MUST provide a manual retry button for any auto-retried action that fails
- SHOULD offer an alternative path ("Can't upload? Try drag and drop instead")

### Graceful Degradation
- If a non-critical feature fails, hide it. Don't break the whole page.
- MUST maintain layout stability when components fail to load
- SHOULD show cached/stale data with a "last updated" notice rather than nothing
- NEVER redirect to a generic error page for recoverable errors

### Copy Rules
- Use "we" language for system errors ("We couldn't save your changes")
- Use "try" language for recovery ("Try refreshing the page")
- NEVER blame the user ("Invalid input" -> "This field needs a valid email")
- Include a support contact for errors that can't be self-resolved
