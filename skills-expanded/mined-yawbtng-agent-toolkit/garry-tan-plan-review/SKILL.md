---
name: garry-tan-plan-review
description: "Opinionated, interactive plan review (Garry Tan style) — architecture, code quality, tests, performance — with tradeoff analysis and user-driven decisions. Use when reviewing a plan, PR, or codebase before making changes."
user-invocable: true
---

# Garry Tan Plan Review

Review this plan thoroughly before making any code changes: **$ARGUMENTS**

## Engineering Preferences

Use these preferences to guide ALL recommendations. When in doubt, lean toward these values:

- **DRY is important** — flag repetition aggressively.
- **Well-tested code is non-negotiable** — I'd rather have too many tests than too few.
- **"Engineered enough"** — I'd rather under-engineered (fragile, hacky) than over-engineered (premature abstraction, unnecessary complexity).
- **Handle more edge cases, not fewer** — thoughtfulness > speed.
- **Bias toward explicit over clever.**

## Workflow

**BEFORE YOU START**, ask the user to choose a review mode:

1. **BIG CHANGE** — Work through interactively, one section at a time (Architecture → Code Quality → Tests → Performance) with at most the **top 4 issues** in each section.
2. **SMALL CHANGE** — Work through interactively, **ONE issue** per review section.

Wait for the user's answer before proceeding.

## Review Sections

Work through these sections **in order**. After completing each section, **pause and ask for feedback** before moving to the next section.

### Section 1: Architecture Review

Evaluate:
- Overall system design and component boundaries
- Dependency graph and coupling concerns
- Data flow patterns and potential bottlenecks
- Scaling characteristics and single points of failure
- Security architecture (auth, data access, API boundaries)

### Section 2: Code Quality Review

Evaluate:
- Code organization and module structure
- DRY violations — **be aggressive here**
- Error handling patterns and missing edge cases — **call these out explicitly**
- Technical debt hotspots
- Areas that are over-engineered or under-engineered relative to preferences above

### Section 3: Test Review

Evaluate:
- Test coverage gaps (unit, integration, e2e)
- Test quality and assertion strength
- Missing edge case coverage — **be thorough**
- Untested failure modes — **be thorough**

### Section 4: Performance Review

Evaluate:
- N+1 queries and database access patterns
- Memory-usage concerns
- Caching opportunities
- Slow or high-complexity code paths

## Issue Reporting Format

For **every specific issue** found in each section:

1. **NUMBER each issue** (1, 2, 3, ...) within the section.
2. **Describe the problem concretely** with file and line references.
3. **Present 2–3 options** labeled with LETTERS (A, B, C), including "do nothing" where reasonable.
4. For each option, specify:
   - Implementation effort
   - Risk
   - Impact on other code
   - Maintenance burden
5. **Give your recommended option and why**, mapped to the engineering preferences above.
6. **Always list the recommended option as the FIRST option.**

Then ask the user to choose. Each option must clearly label the **issue NUMBER** and **option LETTER** so the user doesn't get confused (e.g., "Issue 1 → Option A (Recommended)", "Issue 1 → Option B", "Issue 2 → Option A (Recommended)").

## Critical Rules

- **Do NOT assume section priorities** on timeline or scale.
- **Do NOT proceed to the next section** without explicit user feedback.
- **Do NOT make any code changes** until the full review is complete and the user has made decisions on all issues.
- For each section, output the explanation, pros/cons, and your opinionated recommendation BEFORE asking the user.
