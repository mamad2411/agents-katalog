---
name: review-leancode-arch
description: Review Flutter code against LeanCode architecture standards. Use when auditing a feature or folder for project structure, error handling, or logging.
argument-hint: "<feature-directory-or-file-path>"
---
# Review LeanCode Architecture

Review the specified feature or file against the architecture rules covered by this plugin.

## Checklist

### 1. Project Structure

- [ ] Feature has its own dedicated directory
- [ ] Feature follows the `features/<feature_name>` pattern
- [ ] Feature parts stay together; multi-page features use subdirectories
- [ ] No unnecessary cross-feature references
- [ ] Common code stays infrastructural and does not depend on features

### 2. Error Handling

- [ ] Failures are returned rather than thrown as exceptions
- [ ] Failure objects are defined as dedicated classes
- [ ] Error messages are precise and helpful
- [ ] Failing operations expose a retry path
- [ ] Network errors are handled separately
- [ ] Error UI uses reusable patterns rather than one-off implementations

### 3. Logging

- [ ] `logging/logging.dart` is used for logging
- [ ] Expected exceptions are caught and logged
- [ ] Important user and business-process traces are logged
- [ ] Sensitive data is not logged
- [ ] Frequent automatic actions are not logged

## Output Format

Group findings by domain. For each finding, include:

```
Location: <path>
Violation: <what is wrong>
Fix: <concrete suggestion>
```

If a finding really belongs to DI, navigation, analytics, localization, or state management, point to the matching dedicated plugin instead of forcing it into this review.
