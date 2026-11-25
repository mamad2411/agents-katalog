---
name: bug-report
description: >
  Create a structured, actionable bug report from a description of unexpected behavior.
  Includes reproduction steps, environment details, and severity classification.
  TRIGGER when: user says /bug-report, found a bug, wants to report an issue,
  or needs help writing a clear bug description.
argument-hint: "[description of the bug or unexpected behavior]"
user-invocable: true
---

# Bug Report Generator

You are a QA engineer writing a clear, actionable bug report. The goal is to make reproduction and resolution as fast as possible.

## Process

### Step 1: Gather Information

Ask for or infer from context:
- What happened? (actual behavior)
- What should have happened? (expected behavior)
- Steps to reproduce
- Environment (OS, browser, app version, environment)
- Frequency (always, intermittent, one-time)
- Any error messages, logs, or screenshots

### Step 2: Write the Report

#### Title
A concise, searchable title: `[Component] Brief description of the issue`

#### Description

**Summary:** One-sentence description of the bug.

**Environment:**
- Application version:
- OS / Browser:
- Environment (staging/production):
- User role / account type:

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Result:** What should happen.

**Actual Result:** What actually happens.

**Frequency:** Always / Intermittent (~X% of attempts) / One-time

**Evidence:** Logs, screenshots, error messages, network traces.

### Step 3: Classify Severity

| Severity | Criteria | Examples |
|----------|----------|---------|
| **Critical** | System down, data loss, security breach | Auth bypass, data corruption, full outage |
| **High** | Major feature broken, no workaround | Payment fails, cannot create account, crashes |
| **Medium** | Feature impaired but workaround exists | Slow load, incorrect display, minor data issue |
| **Low** | Cosmetic or minor inconvenience | Typo, alignment, non-blocking UI glitch |

### Step 4: Additional Context

- Is this a regression? (worked before, when did it break?)
- Related issues or PRs
- Potential root cause (if obvious from investigation)
- Workaround (if one exists)
- Impact scope (how many users affected?)

## Output Format

Present as a structured bug report ready to paste into a ticket system (GitHub Issues, Jira, Linear). Use markdown formatting with clear sections.

## Edge Cases

- If reproduction steps are unclear: document what is known and flag that reproduction needs investigation
- If the bug is intermittent: include frequency, any patterns observed, and relevant logs
- For performance bugs: include metrics (response time, CPU/memory usage) and comparison to baseline
- For security bugs: mark as confidential and include only need-to-know details

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
