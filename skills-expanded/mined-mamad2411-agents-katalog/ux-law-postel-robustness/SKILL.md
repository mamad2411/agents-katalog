---
name: ux-law-postel-robustness
description: Use when designing form input handling, file uploads, or any user-supplied data path — Postel's Law / Robustness Principle applied to UX (be liberal in what you accept from the user, strict/clear in what you produce/require back). Triggers on "input validation UX", "flexible input formats", "accept messy input", "form error messages".
allowed-tools: Read, Edit, Grep, Glob
---

# Postel's Law (Robustness Principle) applied to UX

Be liberal in what you accept from the user, precise and clear in what you show or require of them.

## Rules of thumb
- Accept multiple reasonable input formats and normalize server-side (phone numbers with/without dashes, dates in common formats, whitespace-padded input, case-insensitive emails) instead of forcing the user to match one exact format.
- Never make the user reformat data you can parse yourself.
- When you can't accept the input, be strict and specific in the error: state exactly what's expected and why, not a generic "invalid input."
- The leniency is one-directional: what the system displays or outputs (confirmations, receipts, exported data) should be exact and unambiguous, not loosely formatted.

## Review checklist
1. Does the form reject input a reasonable user would consider valid, that the system could normalize instead?
2. Are error messages specific enough to self-correct without guessing?
