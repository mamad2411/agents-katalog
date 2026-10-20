---
name: codex-scan
description: Read-only code review via Codex. Reports issues without fixing. Independent model perspective.
---

# /codex-scan

**Read-only** independent code review using OpenAI Codex CLI. Reports issues without making any changes.
Provides multi-model triangulation — a different model's perspective on your code.

> **No arguments?** Describe this skill and stop. Do not execute.

## Target

If a path argument is provided, review that file/directory.
If no argument, review recently modified files (git diff/log).
Multiple paths can be provided to scan a set of components.

## Process

### Step 0: Load Rubric

Read `.claude/rubric/AUTO-DETECT.md` for the detection table. Then:

1. **Always load:** `.claude/rubric/base.md` and `.claude/rubric/product-quality.md`
2. **Auto-detect domains:** Check target files against the detection table. Load matching domain rubrics (`.claude/rubric/web-api.md`, `.claude/rubric/data-persistence.md`, `.claude/rubric/cli.md`, `.claude/rubric/microservice.md`).
3. **Extract Review Criteria:** From each loaded rubric, collect the numbered items under `## Review Criteria`. Combine into a single criteria list for the Codex prompt.

If a rubric file doesn't exist, skip it and continue.

### Step 1: Find Code to Review

Find target files:
- If path provided, use that
- Otherwise, find recently modified files using git diff or git log
- Look in: src/, lib/, app/, and project root

If NO code exists, output "no code to review" and stop.

### Step 2: Read All Target Code

Read ALL files in scope completely. Do not skim.

### Step 3: Call Codex (MANDATORY)

Invoke Codex CLI non-interactively against the target:

```bash
cd {TARGET} && codex exec -s read-only -o /tmp/lens-codex-scan.md "PRODUCTION READINESS GATE REVIEW. Score like a senior engineer deciding whether to deploy this to production TODAY. If you wouldn't deploy it, score below 8. Review ALL source code. Score each category 1-10 and cite file:line for every finding.

{RUBRIC_CRITERIA}

SCORING ANCHOR: 8+ = deploy today. 5-6 = needs work. 3-4 = major gaps. CRITICAL = blocks production. HIGH = would cause incidents. Rate overall as min of all category scores." 2>&1
```

Replace `{RUBRIC_CRITERIA}` with the combined Review Criteria from all loaded rubric files, numbered sequentially. Example: if base.md has 12 criteria and cli.md has 5, number them (1)-(17).

**Note:** Test Coverage is handled by the testing phase — do not include it in the rubric criteria.

If `codex` is not installed, fall back to Step 3b. If it fails for any other reason, log the error and fall back to Step 3b.

### Step 3b: Fallback — Pattern Scanner

Run the review-bot.sh script bundled with the codex-review skill:

```bash
SKILL_DIR="$(dirname "$(readlink -f workflow-skills/workflow/codex-review/SKILL.md)" 2>/dev/null || echo workflow-skills/workflow/codex-review)"
bash "$SKILL_DIR/review-bot.sh" {TARGET} --run --out /tmp/lens-codex-scan.json
```

### Step 4: Compile Report (DO NOT FIX)

Read `/tmp/lens-codex-scan.md` (or `/tmp/lens-codex-scan.json` if fallback was used).

Parse all findings with file:line references. Categorize by:
- **Security** — vulnerabilities, secret leakage, crypto issues
- **Reliability** — cross-filesystem, atomicity, error handling
- **Operational** — UX gaps, CI/CD support, unclear semantics
- **Architecture** — structural issues, coupling, missing abstractions

**DO NOT edit any files. Report only.**

### Step 5: Clean Up

```bash
rm -f /tmp/lens-codex-scan.md /tmp/lens-codex-scan.json
```

## Output Format

```markdown
## Codex Scan: [target]

### Summary

| Metric | Value |
|--------|-------|
| Files scanned | N |
| Total lines | N |
| Overall rating | production-ready / production-leaning / not-production-ready |
| Security issues | N |
| Reliability issues | N |
| Operational issues | N |
| Architecture issues | N |

### Security Issues

1. **[file:line]** — [description]
   - Problem: [what Codex found]
   - Impact: [why it matters]
   - Suggested fix: [how to address]

### Reliability Issues

1. **[file:line]** — [description]
   - Problem: [what Codex found]
   - Suggested fix: [how to address]

### Operational Issues

1. **[file:line]** — [description]
   - Concern: [what Codex found]

### Architecture Issues

1. **[file:line]** — [description]
   - Concern: [what Codex found]

### AI-Generated Antipatterns Detected

- [ ] Over-abstraction (factories/wrappers used once)
- [ ] Defensive checks for impossible cases
- [ ] Reimplementing stdlib
- [ ] Over-commenting obvious code
- [ ] Unnecessary config options
- [ ] Single-use wrapper functions

### Files Reviewed

| File | Lines | Issues |
|------|-------|--------|
| path/to/file.ts | 245 | 2 security, 1 reliability |
| ... | ... | ... |

---
CODEX_RESULT: called - [N] total issues
SCAN_ONLY: no fixes applied
```

## Rules

- **READ ONLY** - Do not edit any files
- **MUST CALL CODEX** - This skill requires the Codex CLI (or falls back to pattern scanner)
- **COMPLETE** - Review all files in scope
- **ORGANIZE** - Group issues by category
- **ACTIONABLE** - Include suggested fixes (but don't apply them)

## When to Use

- Pre-commit quality check (different perspective from Gemini)
- Multi-model triangulation on code quality
- Assessing AI-generated code smells
- Getting an independent review before PR

## Anti-Patterns (Don't Do)

- Making any edits to files
- Skipping the Codex call
- Summarizing without specific line numbers
- Hiding or downplaying issues
- Applying fixes (use /codex-review for that)
