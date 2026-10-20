---
name: gemini-scan
description: Read-only code review via Gemini. Reports issues without fixing. Senior engineer style - no false praise.
---

# /gemini-scan

**Read-only** independent code review using Gemini. Reports issues without making any changes.
Senior Google engineer style - no handholding, no false praise.

> **No arguments?** Describe this skill and stop. Do not execute.

## Craft Standards: What We're Looking For

**Code that a master craftsperson would be proud of.**

This scan specifically looks for code that appears AI-generated rather than crafted by a skilled human engineer.

### AI Antipatterns Gemini Will Flag

| Antipattern | Example | Why It's Wrong |
|-------------|---------|----------------|
| Over-abstraction | Factory used once | Abstraction without justification |
| Defensive paranoia | `if (x !== null)` when x can't be null | Doesn't understand the code |
| Reimplementing stdlib | Custom `deepClone` when `structuredClone` exists | Ignorance or arrogance |
| Comment spam | `// loop through users` above `for (user of users)` | Insulting the reader |
| Speculative features | Config options with one possible value | Solving imaginary problems |
| Enterprise patterns | `AbstractUserFactoryBean` | Cargo-culting |

**Goal:** Report code that wouldn't survive a senior engineer's review.

---

## Target

If a path argument is provided, review that file/directory.
If no argument, review recently modified files (git diff/log).
Multiple paths can be provided to scan a set of components.

## Process

### Step 0: Load Rubric

Read `.claude/rubric/AUTO-DETECT.md` for the detection table. Then:

1. **Always load:** `.claude/rubric/base.md` and `.claude/rubric/product-quality.md`
2. **Auto-detect domains:** Check target files against the detection table. Load matching domain rubrics (`.claude/rubric/web-api.md`, `.claude/rubric/data-persistence.md`, `.claude/rubric/cli.md`, `.claude/rubric/microservice.md`).
3. **Extract Review Criteria:** From each loaded rubric, collect the numbered items under `## Review Criteria`. Combine into a single criteria list for the Gemini context.

If a rubric file doesn't exist, skip it and continue.

### Step 1: Find Code to Review

Find target files:
- If path provided, use that
- Otherwise, find recently modified files using git diff or git log
- Look in: src/, lib/, app/, and project root

If NO code exists, output "no code to review" and stop.

### Step 2: Read All Target Code

Read ALL files in scope completely. Do not skim.

### Step 3: Call Gemini (MANDATORY)

For each file or logical group:

```
mcp__gemini-reviewer__gemini_review
  code: <paste the source code>
  focus: "general"
  context: "PRODUCTION READINESS review. If you wouldn't deploy this to production today, flag it. Review against: {RUBRIC_CRITERIA}. For each finding cite file:line and severity (CRITICAL/HIGH/MEDIUM/LOW). CRITICAL = blocks production. HIGH = would cause incidents."
```

Replace `{RUBRIC_CRITERIA}` with the combined Review Criteria from all loaded rubric files, numbered sequentially.

**Note:** Test Coverage is handled by the testing phase — do not include it in the rubric criteria.

If tool unavailable, output: `GEMINI_ERROR: tool not available`

### Step 4: Compile Report (DO NOT FIX)

Collect all issues from Gemini and organize by severity.

**DO NOT edit any files. Report only.**

## Output Format

```markdown
## Gemini Scan: [target]

### Summary

| Metric | Value |
|--------|-------|
| Files scanned | N |
| Total lines | N |
| Critical issues | N |
| High issues | N |
| Medium issues | N |
| Low issues | N |

### Critical Issues 🔴

Must fix before shipping:

1. **[file:line]** — [description]
   - Problem: [what Gemini found]
   - Impact: [why it matters]
   - Suggested fix: [how to address]

### High Issues 🟠

Should fix:

1. **[file:line]** — [description]
   - Problem: [what Gemini found]
   - Suggested fix: [how to address]

### Medium Issues 🟡

Consider fixing:

1. **[file:line]** — [description]
   - Concern: [what Gemini found]

### Low Issues 💭

Minor improvements:

1. **[file:line]** — [description]

### AI-Generated Antipatterns Detected

Patterns typical of AI-generated code that should be simplified:

- [ ] Over-abstraction (factories/wrappers used once)
- [ ] Features not requested
- [ ] Defensive checks for impossible cases
- [ ] Reimplementing stdlib
- [ ] Copy-paste that should be extracted
- [ ] Over-commenting obvious code
- [ ] Unnecessary config options
- [ ] Over-engineered types

### Files Reviewed

| File | Lines | Issues |
|------|-------|--------|
| path/to/file.ts | 245 | 2 🔴, 1 🟠 |
| ... | ... | ... |

---
GEMINI_RESULT: called - [N] total issues
SCAN_ONLY: no fixes applied
```

## Rules

- **READ ONLY** - Do not edit any files
- **MUST CALL GEMINI** - This skill requires the Gemini MCP tool
- **COMPLETE** - Review all files in scope
- **ORGANIZE** - Group issues by severity
- **ACTIONABLE** - Include suggested fixes (but don't apply them)

## When to Use

- Pre-commit quality check
- Code review before PR
- Assessing unfamiliar code
- Finding issues without auto-fix
- Getting external perspective on your code

## Anti-Patterns (Don't Do)

- Making any edits to files
- Skipping the Gemini call
- Summarizing without specific line numbers
- Hiding or downplaying issues
- Applying fixes (use /gemini-review for that)
