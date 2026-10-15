---
name: eng-bugfix-rca
description: Investigate software bugs or GitHub issues and produce a structured Root Cause Analysis (RCA) document. Use when diagnosing defects, analyzing bug reports, and designing targeted bug fixes.
---

# Bugfix: Root Cause Analysis (RCA)

Investigate reported bugs, identify the root mechanism of failure, and formulate an evidence-backed remediation strategy.

## Process

### 1. Issue Triage & Reproduction
1. Ingest the issue description, error logs, and stack traces (from issue trackers or direct user input).
2. Trace the execution path that leads to the failure.
3. Establish a deterministic reproduction case (minimal test case or reproduction script).
4. **Test-First Evidence Chain**: Convert the repro into an executable failing test BEFORE any fix exists. Capture the red run output as evidence; the fix phase is only legitimate when it turns this exact test green without weakening assertions.

### 2. Codebase Investigation
1. Search for affected functions, components, or API boundaries using code search tools.
2. Review recent git commit history on affected paths (`git log -n 10 -- <path>`) to see if recent changes introduced regressions.
3. Formulate and test hypotheses regarding the bug's root mechanism.

### 3. Formulate Remediation Plan
1. Detail the precise technical root cause (why it failed).
2. Design a minimal, clean fix with zero unintended side effects.
3. Plan regression tests to permanently prevent recurrence.

---

## Output RCA Template

Save to `docs/rca/issue-<issue-id>.md` (or `.agents/rca/...`):

```markdown
# Root Cause Analysis: <Bug Title / Issue #ID>

## 1. Problem Description
- **Symptoms**: <What failed, error messages, broken behavior>
- **Reproduction**: <Exact steps or test case to reproduce>

## 2. Root Cause Analysis
- **Failing Component**: `path/to/file.ext:line`
- **Mechanism**: <Detailed explanation of the logical or environmental failure>
- **Contributing Factors**: <Concurrency, unhandled nulls, type mismatches, etc.>

## 3. Proposed Fix Strategy
- **Target Files**:
  - `path/to/file.ext`: <Specific modification needed>
- **Regression Test Plan**:
  - `tests/path/to/test_issue.ext`: <New test to verify the fix>

## 4. Verification Command
- `<executable test command>`
```
---

## Checkable Completion Criteria

- [ ] A deterministic reproduction case exists and was captured failing BEFORE any fix.
- [ ] Root cause identified with exact `file:line` location and failure mechanism explanation.
- [ ] RCA document saved with fix strategy, target files, and regression test plan.
- [ ] Verification command is executable and currently red on the unfixed code.
