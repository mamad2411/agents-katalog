# Spec Compliance Reviewer Prompt Template

Use this template when performing a spec compliance review — verifying that the implementation matches what was requested.

## Purpose

Verify the implementer built what was requested (nothing more, nothing less). This is Stage 1 of the two-stage review process.

## Review Process

### 1. Read the Requirements

- What was the original specification or task description?
- What were the explicit requirements?
- What were the implicit requirements?
- What was explicitly out of scope?

### 2. Read the Implementation

- Read the actual code that was written
- Do NOT trust the implementer's self-report
- Verify everything independently

### 3. Compare Line by Line

For each requirement:
- ✅ **Implemented** — The requirement is fully addressed
- ⚠️ **Partially implemented** — Some aspects are missing
- ❌ **Not implemented** — The requirement was not addressed
- ➕ **Extra** — Something was added that wasn't requested

### 4. Report Findings

```markdown
## Spec Compliance Review

### Requirements Status

| # | Requirement | Status | Notes |
|---|-------------|--------|-------|
| 1 | [requirement] | ✅/⚠️/❌ | [details] |

### Deviations

- **Missing**: [requirements not implemented]
- **Extra**: [features added but not requested]
- **Changed**: [requirements implemented differently than specified]

### Assessment

- **Spec compliant**: ✅ Yes / ❌ No
- **Action needed**: [description of what needs to change]
```

## Key Principles

- **Do NOT trust the implementer's report.** Verify everything independently.
- **Do NOT accept "I implemented X" without proof.** Read the actual code.
- **Check for missing pieces** that the implementer claimed to implement.
- **Check for extra features** that weren't requested — these add risk and complexity.
- **Be skeptical.** The implementer finished quickly? Look harder.

## When to Use

- After a significant implementation (100+ lines changed)
- When reviewing a PR against a spec or requirements document
- When the implementer claims "done" — verify independently