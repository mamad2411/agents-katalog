---
name: review-s
description: Review code for quality, bugs, and improvements. Use when user wants to review code with /review-s.
---

# Review Skill (/review-s)

Review code and provide structured feedback on quality, bugs, and improvements.

## Input

- `$ARGUMENTS`: Optional file path to review
- If no path provided, review current git diff

## Review Focus Areas

### 1. Bugs & Errors
- Logic errors and incorrect calculations
- Missing null/None checks
- Unhandled edge cases
- Incorrect exception handling

### 2. Security
- Input validation gaps
- SQL injection risks
- Sensitive data exposure
- Authentication/authorization issues

### 3. Performance
- N+1 query problems
- Missing database indexes
- Inefficient loops or algorithms
- Unnecessary memory allocations

### 4. Readability
- Unclear naming conventions
- Overly complex functions
- Missing or unclear comments
- Inconsistent code style

## Process

### Step 1: Gather Code

If file path provided:
- Read the file directly

If no path:
- Run `git diff` to see unstaged changes
- Run `git diff --staged` to see staged changes

### Step 2: Analyze Code

For each file:
1. Check for bugs and logic errors
2. Look for security vulnerabilities
3. Identify performance issues
4. Assess readability and maintainability

### Step 3: Document Findings

Structure feedback by severity.

## Output Format

```markdown
## Code Review

### Summary
[One sentence overall assessment]

### Issues Found

#### Critical (Must Fix)
- [issue]: [location] - [brief explanation]

#### Warnings (Should Fix)
- [issue]: [location] - [brief explanation]

#### Suggestions (Nice to Have)
- [suggestion]: [location] - [brief explanation]

### What's Good
- [positive observation]
```

## Guidelines

- Be specific about locations (file:line if possible)
- Provide actionable feedback with clear remediation steps
- Don't nitpick style unless it significantly impacts readability
- Acknowledge good patterns and well-written code
- Focus on issues that could cause bugs, security issues, or maintenance problems
