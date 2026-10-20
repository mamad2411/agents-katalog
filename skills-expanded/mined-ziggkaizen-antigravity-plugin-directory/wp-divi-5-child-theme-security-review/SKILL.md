---
name: wp-divi-5-child-theme-security-review
description: Reviews Divi 5 child-theme PHP and assets for authorization, input handling, output escaping, database safety, secret exposure, accessibility, performance, and operational failure modes.
---

# Divi 5 Child-Theme Security Review

## Review Model

Review child-theme code as production application code, not as harmless presentation glue.

## Areas

### Authorization and Requests

- Identify every admin action, form handler, Ajax callback, REST route, URL-triggered action, and state change.
- Require capability checks for privileged operations.
- Verify nonces where CSRF protection is relevant, without treating them as authorization.
- Reject ambiguous request shapes and enforce allowlists.

### Data and Output

- Trace request, database, custom-field, remote, and user-generated inputs.
- Validate before sanitizing.
- Escape late for HTML, attributes, URLs, JavaScript, and CSS.
- Use prepared queries or supported APIs.
- Review redirects, file paths, uploads, remote requests, and serialized data.

### Secrets and Privacy

- Search PHP, JS, CSS, JSON, maps, and build output for credentials or private endpoints.
- Keep secrets outside the theme and browser-delivered code.
- Minimize personal-data collection and logging.

### Assets and Frontend

- Check enqueue scope, dependency integrity, cache versions, duplicate libraries, and development artifacts.
- Review Content Security Policy compatibility where applicable.
- Verify semantic markup, keyboard behavior, focus visibility, labels, alternatives, contrast, and reduced-motion behavior.
- Test logged-out frontend and failure states.

## Workflow

Use [review-divi-child-theme-security-workflow.md](workflows/review-divi-child-theme-security-workflow.md) and [child-theme-security-checklist.md](resources/child-theme-security-checklist.md).

## Output

Report findings with severity, path/line, exploit or failure scenario, affected users/data, exact remediation, and validation evidence.
