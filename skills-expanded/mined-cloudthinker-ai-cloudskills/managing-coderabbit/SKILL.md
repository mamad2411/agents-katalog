---
name: managing-coderabbit
description: |
  Use when working with Coderabbit — codeRabbit AI code review management
  including automated review comments, auto-suggestions, review customization,
  and learning from feedback. Use when configuring CodeRabbit for AI-assisted
  code review, custom review rules, and automated suggestion workflows.
connection_type: coderabbit
preload: false
---

# Managing CodeRabbit

## Overview

Manage CodeRabbit AI-powered code review, including automated review comments, contextual suggestions, review customization, and feedback learning to improve review quality over time.

## Key Capabilities

- Automatically review PRs with AI-generated comments and suggestions
- Configure review focus areas (security, performance, style, bugs)
- Customize review rules and coding standards
- Learn from reviewer feedback to reduce false positives
- Generate PR summaries and walkthrough comments
- Integrate with GitHub, GitLab, and Azure DevOps

## Workflow

### 1 — Review Configuration

```
REVIEW SETTINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Review scope:
    [ ] All PRs automatically
    [ ] PRs with @coderabbitai mention
    [ ] PRs targeting specific branches: ___
[ ] Review focus areas:
    [ ] Bug detection
    [ ] Security vulnerabilities
    [ ] Performance issues
    [ ] Code style and best practices
    [ ] Error handling
    [ ] Documentation completeness
[ ] Review depth: superficial / standard / thorough
```

### 2 — Custom Instructions

```
CUSTOM REVIEW RULES (.coderabbit.yaml)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
reviews:
  profile: assertive / chill
  path_instructions:
    - path: "src/api/**"
      instructions: |
        Review for REST API best practices.
        Check error handling and status codes.
        Verify input validation.
    - path: "src/db/**"
      instructions: |
        Check for SQL injection risks.
        Verify index usage for queries.
        Review transaction handling.
  auto_review:
    enabled: true
    ignore_title_keywords:
      - "WIP"
      - "DO NOT MERGE"
    drafts: false
```

### 3 — Feedback Learning

```
FEEDBACK CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Learn from resolved/dismissed comments: YES / NO
[ ] Thumbs up/down feedback tracking: YES / NO
[ ] Suppress repeated false positives: YES / NO
[ ] Custom knowledge base: YES / NO
[ ] Team-specific review patterns: YES / NO
```

## Common Operations

### Review Analytics
Track AI review accuracy, accepted suggestions, and false positive rates.

### Rule Tuning
Adjust custom instructions based on feedback patterns to improve review quality.

### Incremental Reviews
Trigger re-review on updated PRs analyzing only the new changes.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Too many comments | Review profile too assertive | Switch to "chill" profile or add path exclusions |
| Irrelevant suggestions | Missing context | Add path-specific instructions in .coderabbit.yaml |
| Review not triggered | Draft PR or WIP title | Remove WIP keyword or enable draft review |
| Slow review response | Large diff | Exclude generated files and vendor directories |

## Output Format

Present results as a structured report:
```
Managing Coderabbit Report
══════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

