---
name: accessibility-audit
description: Audit UI for WCAG accessibility issues and fixes
user-invocable: false
---
## Overview

Perform comprehensive accessibility (a11y) audit of the current UI code to ensure compliance with WCAG guidelines and provide an inclusive user experience.

## Steps

1. **WCAG Compliance**
    - Check conformance to WCAG 2.1 guidelines (A, AA, AAA levels)
    - Verify proper semantic HTML structure
    - Ensure keyboard navigation support
    - Review color contrast and visual accessibility
2. **Screen Reader Support**
    - Validate ARIA labels and descriptions
    - Check heading hierarchy and structure
    - Ensure form labels and error messages are accessible
    - Review dynamic content announcements
3. **Interactive Elements**
    - Verify focus management and visible focus indicators
    - Check tab order and keyboard shortcuts
    - Ensure interactive elements are properly sized
    - Review modal and dialog accessibility
4. **Testing & Tools**
    - Suggest automated accessibility testing tools
    - Provide manual testing procedures
    - Create accessibility test cases
    - Recommend browser extensions and validators
5. **Remediation**
    - Provide specific code fixes for each issue
    - Include ARIA attributes and semantic improvements
    - Suggest alternative approaches for complex interactions
    - Create accessible component patterns

## Accessibility Audit Checklist

- [ ] WCAG compliance verified
- [ ] Screen reader support validated
- [ ] Interactive elements accessible
- [ ] Testing tools recommended
- [ ] Remediation code provided with examples

## Guardrails

- Change only accessibility issues; do not touch unrelated code.
- Verify keyboard navigation and screen reader behavior, not only automated scans.
- Do not print or commit secrets, tokens, or credentials found while auditing UI code; flag their location instead.
- Do not commit, push, or merge changes without explicit consent.