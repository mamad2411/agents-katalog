---
name: code-review
description: Reviews code for security (OWASP), performance, accessibility, and quality. Outputs findings by severity (Critical, Warning, Suggestion, Good) with a verdict. Use when reviewing code, diffs, or PRs.
user-invokable: true
---

# Code Review

A code review skill that checks for web security vulnerabilities, performance issues, accessibility problems, and code quality — then delivers structured feedback with severity levels.

## Instructions

**STEP 1 — GATHER CHANGES**

Determine what to review:

- If a GitHub PR URL is provided: fetch the PR diff and context
- If a branch name is provided: diff it against the main branch
- If file paths are provided: read those files directly
- If nothing is provided: check for staged changes, then fall back to unstaged changes

**STEP 2 — ANALYZE**

Review the changes across these dimensions:

**Security (OWASP Top 10):**

- Injection flaws (SQL, XSS, command injection)
- Broken authentication / authorization
- Sensitive data exposure (hardcoded secrets, API keys, tokens)
- Insecure dependencies (check for known CVEs if possible)
- CSRF, open redirects (including client-side navigation to unvalidated URLs), unsafe deserialization

**Performance:**

- Unnecessary re-renders (React: missing memo, unstable refs in deps, missing key props in lists)
- Bundle size impact (large imports, tree-shaking issues)
- N+1 queries, unoptimized loops, missing pagination
- Memory leaks (event listeners, subscriptions not cleaned up)
- Lazy loading opportunities

**Accessibility:**

- Missing ARIA attributes, roles, or labels
- Keyboard navigation issues
- Color contrast, focus management
- Semantic HTML usage

**Code Quality:**

- Type safety issues (TypeScript)
- Error handling gaps
- Dead code, unused imports
- Naming clarity, readability
- Test coverage for new logic

**STEP 3 — REPORT**

Output the review in this format:

```
## Code Review

### Summary
[1-2 sentence overview of the changes and overall assessment]

### Findings

#### 🔴 Critical
[Issues that MUST be fixed before merging — security vulnerabilities, data loss risks, breaking bugs]

#### 🟡 Warning
[Issues that SHOULD be fixed — performance problems, accessibility gaps, potential bugs]

#### 🔵 Suggestion
[Nice-to-haves — code style improvements, minor optimizations, better patterns]

#### ✅ Good
[Things done well worth calling out — encouragement for good patterns]

### Verdict: [APPROVE | REQUEST CHANGES | NEEDS DISCUSSION]
```

## Rules

- Every finding must reference the specific file and line number. If code is provided inline (not from a file), reference the relevant line within the snippet
- Include a concrete fix or code suggestion for each Critical and Warning item
- If there are no findings in a severity category, omit that category
- Be direct and specific — no vague feedback like "consider improving this"
- If the diff is clean with no issues, say so and approve
- For security findings, explain the attack vector briefly so the author understands the risk
