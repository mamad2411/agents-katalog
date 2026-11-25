---
name: issue-triage-bot
description: "Issue classification, prioritization, duplicate detection, reproducibility checks, automated fix recommendations. Use when triaging or prioritizing bug reports."
---

# Issue Triage Bot

## Overview

Automatically classifies, prioritizes, detects duplicate reports, and, where possible, recommends code fixes for incoming issue reports. By automating issue management, it alleviates maintainer burden and ensures users receive rapid feedback.

**Core principle:** EVERY ISSUE IS A SIGNAL. Rather than getting buried in the backlog, each issue must be categorized, prioritized, and linked to a concrete action.

## The Iron Law

```
NO ISSUE SHALL BE LEFT UNANSWERED. Every issue must be classified, marked as duplicate, given a fix recommendation, or closed with a clear explanation of why it cannot be addressed.
```

## When to Use

**Use this when:**
- The repository receives 10+ issues daily, making manual tracking unsustainable.
- The duplicate rate is high (users report the same issues repeatedly).
- Issues accumulate in the backlog without any clear priority metadata.
- Users experience weeks of delay before receiving an initial response.

**Use this ESPECIALLY when:**
- Managing community issues in an open-source project.
- Scanning all outstanding bugs prior to a major release.
- A new maintainer team is onboarding and the triage workflow is undefined.

**Don't skip when:**
- "There are only a few issues" — every issue deserves a systematic triage.
- "Everything is urgent" — when everything is urgent, nothing is. Prioritization is mandatory.

## Phase 1: Issue Classification

**BEFORE proceeding:**

1. **Determine the issue type:**
   - **Bug:** Unexpected behavior, errors, crashes, incorrect outputs.
   - **Feature Request:** Proposals for new features or enhancements.
   - **Question:** How-to queries, installation support, or documentation questions.
   - **Documentation:** Reports of missing, incomplete, or incorrect documentation.
   - **Discussion:** Ideas, design proposals, or Requests for Comments (RFCs).
2. **Assign labels:**
   - `type/bug`, `type/feature`, `type/question`, `type/docs`
   - Subcategories: `component/api`, `component/ui`, `component/cli`, etc.
3. **Template audit:** Was the issue submitted using the correct template? Are there missing fields?

```bash
# Tag issues using the GitHub CLI
gh issue edit <ISSUE_NUMBER> --add-label "type/bug,component/api"

# Read the issue body to verify template compliance
gh issue view <ISSUE_NUMBER> --json body,title,labels
```

## Phase 2: Priority Assignment

**BEFORE proceeding:**

1. **Assess Severity:**
   - **Critical:** Data loss, security vulnerability, constant crash, production down.
   - **Major:** A core feature is non-functional with no straightforward workaround.
   - **Minor:** A small bug with an easy workaround, or cosmetic issues.
   - **Trivial:** Typo fixes or very minor UI alignment issues.
2. **Assess Impact:**
   - **High:** Affects the vast majority of users or a core user flow.
   - **Medium:** Affects a subset of users or common scenarios.
   - **Low:** Affects very few users or is limited to extreme edge cases.
3. **Priority Matrix (Severity × Impact):**

   | Severity \ Impact | High | Medium | Low |
   |-------------------|------|--------|-----|
   | Critical | P0 (immediate) | P0 | P1 |
   | Major | P1 (today) | P1 | P2 |
   | Minor | P2 (this week) | P3 | P3 |
   | Trivial | P3 (when possible) | P4 | P4 |

4. **Assign maintainers and priority labels:**

```bash
# Assign priority labels
gh issue edit <ISSUE_NUMBER> --add-label "priority/critical,priority/p0"
gh issue edit <ISSUE_NUMBER> --add-assignee <MAINTAINER>
```

## Phase 3: Duplicate Detection

**BEFORE proceeding:**

1. **Scan open issues** — Search for identical or highly similar issue titles or body text.
2. **Apply similarity thresholds:**
   - **Title similarity:** Matching error messages, identical components, or similar scenarios.
   - **Body similarity:** Identical stack traces, error codes, or reproduction steps.
   - **Label similarity:** Matches across component labels.
3. **Check closed issues** — Check if the issue was already resolved in a previous tag or release.
4. **When a duplicate is found:**
   - Add a comment to the new issue: "This issue appears to be a duplicate of #DUPLICATE_ISSUE"
   - Add the `duplicate` label.
   - Cross-reference the original issue number.

```bash
# Search for similar open issues via GitHub Search API
gh search issues --repo <OWNER/REPO> "<similar title>" --state open --json number,title

# Search closed issues as well
gh search issues --repo <OWNER/REPO> "<similar title>" --state closed --json number,title

# Mark as duplicate and cross-reference
gh issue edit <ISSUE_NUMBER> --add-label "duplicate"
gh issue comment <ISSUE_NUMBER> --body "Duplicate of #ORIGINAL_ISSUE"
```

## Phase 4: Reproducibility Check

**BEFORE proceeding:**

1. **Verify reproduction steps:**
   - Are the steps clear and actionable (step 1, step 2, step 3)?
   - Is the expected behavior specified?
   - Is the actual behavior/error output included?
   - Is the environment metadata present (OS, version, browser, dependencies)?
2. **Tag issues with missing details:**
   - `needs-reproduction-steps` — missing actionable steps.
   - `needs-environment-info` — missing environment metadata.
   - `needs-logs` — missing error output or stack traces.
3. **Send an automated response:**
   - Request the missing information.
   - Provide a template to guide their input.
4. **Mark fully detailed issues as `reproducible`.**

```bash
# Inspect the issue body for reproducibility indicators
gh issue view <ISSUE_NUMBER> --json body,labels,comments

# Add request labels
gh issue edit <ISSUE_NUMBER> --add-label "needs-reproduction-steps"

# Send automated comment requesting data
gh issue comment <ISSUE_NUMBER> --body "Thank you for the report! To help us investigate, please provide:\n\n1. Step-by-step reproduction steps\n2. Expected behavior\n3. Actual behavior\n4. Environment details (OS, version, runtime)"
```

## Phase 5: Automated Fix Recommendation

**BEFORE proceeding:**

1. **Recognize common error patterns:**
   - **Null Pointer / NoneType errors:** Missing null checks, incorrect optional unwrapping.
   - **ImportError / ModuleNotFoundError:** Missing dependencies, incorrect import paths.
   - **TypeError:** Incompatible type operations, incorrect type conversions.
   - **Timeout / ConnectionError:** Network timeouts, API rate limits.
   - **PermissionError:** Incorrect file or system permissions.
2. **Pinpoint the error source from the stack trace:**
   - Extract the target file and line number.
   - Search the codebase to analyze the surrounding lines.
   - Formulate a clean code fix.
3. **Post the fix recommendation as an issue comment:**
   - Explain the root cause of the error.
   - Provide a clear, copy-pasteable code block showing the proposed fix.
   - Recommend opening a Pull Request (or initiate it automatically if configured).

```bash
# Search for the source of the stack trace
# Example: NoneType error in api/service.py at line 42
# View the surrounding source code
read_file("api/service.py", offset=40, limit=5)

# Post the analysis and fix suggestion
gh issue comment <ISSUE_NUMBER> --body "**Analysis:** ...\n**Error:** ...\n**Fix Proposal:** ...\n**PR:** #..."
```

## Phase 6: Final Verification

Before marking complete:

- [ ] All new issues have been successfully categorized and labeled.
- [ ] Priorities (P0-P4) have been calculated and assigned to every issue.
- [ ] Duplicates have been identified, cross-referenced, and marked.
- [ ] Reproducibility checks are complete, and requests for missing information have been sent.
- [ ] Fix recommendations are provided for known error patterns and stack traces.
- [ ] P0/P1 issues are assigned to their respective maintainers.
- [ ] Triage stats are reported (bug/feature distribution, count of active P0s, duplicate rates).

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "This issue is probably a duplicate, but I don't feel like searching" — Skipping duplicate checking clutters the database and fractures effort.
- "Let's make all bugs P2 and we'll deal with them later" — Unprioritized issues get lost in the backlog.
- "Repro steps are missing, but I can guess what they mean" — Never operate on assumptions. Always request missing reproduction details.
- "This issue is too old, let's just close it" — Always triage the issue first before making closure decisions.
- "Providing a fix recommendation will take too long" — A 5-minute fix suggestion now can save days of investigation later.

**ALL of these mean: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "This is a bug, why did you label it as a feature?" — Incorrect classification. Return to Phase 1.
- "This cannot be a P3; it is bringing down production" — Incorrect priority calculation. Return to Phase 2.
- "This is an exact duplicate of #42, why wasn't it marked?" — Missed duplicate checking. Return to Phase 3.
- "Repro steps are completely missing, why didn't you ask for them?" — Skipped reproducibility audit. Return to Phase 4.
- "The fix for this is trivial, why did you not recommend it?" — Passive behavior instead of suggesting a fix. Return to Phase 5.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Checking duplicates takes too much time." | A 30-second search saves hours of redundant discussions and management downstream. |
| "We don't need to assign priority metadata to everything." | Without prioritization, teams try to fix everything at once, resulting in nothing getting finished. |
| "The user should have provided reproduction steps in the first place." | Users frequently submit incomplete issues; guiding them to provide proper details is our responsibility. |
| "Suggesting code fixes is the developer's job, not the triage bot's." | Suggesting even simple fixes from stack traces saves immense developer time. |
| "It's not worth triaging stale issues." | Every issue represents a user's time and effort; they are always valuable to evaluate. |

## Related Skills

- **code-reviewer** — Integrates fix recommendations into PR review flows.
- **pr-babysitter** — Automatically manages and merges PRs opened for issue fixes.
- **auto-changelog** — Appends resolved issues to changelogs upon closure.
- **edge-case-hunter** — Helps identify subtle edge cases flagged within issues.

## Self-Review

After completing this skill's process:

1. **Coverage check:** Did you scan all incoming issues? Is each one labeled and classified?
2. **Edge case check:** How do you handle multiple duplicate candidates? How do you classify issues that don't fit default categories?
3. **Quality check:** Are priority levels consistent? Are fix recommendations valid and actionable? Are responses polite and professional?
