---
name: CUSIPValidationFormatter
description: Use this skill after CUSIP validation to ensure results are formatted for user readability. Always apply this post-process to validation outcomes.
tools:
  - bash
---

# CUSIP Validation Formatter

## Purpose
Formats the validation result for easy readability and user comprehension.

## Workflow
1. Receive the raw result from `cusip-validator`.
2. Run: `python pipeline/skills/CUSIPValidationFormatter/scripts/postprocess.py "<validation_result>"`
3. Present the formatted output to the user.
