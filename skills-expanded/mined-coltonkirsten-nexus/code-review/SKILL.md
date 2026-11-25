---
name: code-review
description: Code review checklist and best practices. Use when reviewing code or preparing code for review.
---

# Code Review

## What to Check

### Correctness
- Does the code do what it claims to do?
- Are edge cases handled?
- Are there off-by-one errors?
- Is error handling appropriate?

### Clarity
- Are variable and function names descriptive?
- Is the code self-documenting?
- Are complex sections commented?
- Is the code organized logically?

### Performance
- Are there obvious inefficiencies?
- Is there unnecessary work being done?
- Are appropriate data structures used?

### Security
- Is user input validated?
- Are secrets kept out of code?
- Are there injection vulnerabilities?

### Testing
- Are there tests for new functionality?
- Do tests cover edge cases?
- Are tests readable and maintainable?

## Giving Feedback

- Be specific about what and why
- Suggest improvements, don't just criticize
- Distinguish between blocking issues and suggestions
- Acknowledge good work
