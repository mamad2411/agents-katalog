---
name: rca-postmortem
description: Perform a blameless RCA/postmortem with impact summary, timeline, root causes, defense gaps, and actionable remediation items with owners and validations. Use after incidents/bugs to prevent recurrence and track follow-ups.
---

# RCA / Postmortem

## 1. Impact Summary

- What happened, when, duration
- Who/what was impacted
- Severity (S0–S3) + rationale

**Expected**: Clear statement of user/business impact.

## 2. Timeline

- Detection → triage → mitigation → resolution
- Include decision points and unknowns

**Expected**: Timeline is factual and complete enough to reason about.

## 3. Root Cause Analysis

- Immediate cause (trigger)
- Root causes (systemic contributors)
- “Why chain” (5 whys), focusing on system/process, not blame

**Expected**: Root causes explain why the incident was possible.

## 4. Defense Gaps

- Monitoring/alerts gaps
- Missing/weak tests
- Review gaps
- Rollout/release guardrails gaps

**Expected**: Identified missing guardrails.

## 5. Remediation Plan (Actionable)

Split into:
- Fix now (stop the bleeding)
- Fix right (harden/refactor/redesign)
- Prevent (tests, alerts, docs, runbooks)

Each action item must include:
- Owner
- Priority
- Due date
- Validation method

**Expected**: Follow-ups are owned, prioritized, and verifiable.

## 6. Verification

- Add tests that reproduce the issue and prevent recurrence.
- Validate via canonical commands from `PROJECT.md`.

**Expected**: Regression is prevented by automated checks.

## Output

Save to `docs/rca/RCA-[yyyy-mm-dd]-[short-title].md`.

