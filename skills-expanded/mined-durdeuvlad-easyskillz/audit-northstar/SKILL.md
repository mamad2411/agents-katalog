---
name: audit-northstar
description: Audits easyskillz code changes against North Star principles for design integrity and correctness.
---
# audit-northstar

Audits easyskillz code changes — diffs, new files, staged changes, or PRs — against the five North Star principles defined in CONTRIBUTING.md.

Use this skill whenever someone asks to review, check, QA, or audit easyskillz changes for correctness, design integrity, or principle compliance. Also trigger when a PR or branch is being prepared and the user wants a second opinion on whether the implementation respects the project's design values.

Returns a per-principle PASS/FAIL verdict with specific file+line violations and actionable fixes.

## North Star Principles

1. **Centralise** — one source of truth. Skills live in `.easyskillz/skills/`. Tool-specific dirs are outputs, never inputs.
2. **Never force the user** — no operation is mandatory. Every write is opt-in or idempotent. Never overwrite user-owned content.
3. **Sync is the entry point** — `easyskillz sync` is the one command users remember. It handles everything on first run and is safe to re-run at any time.
4. **Respect user decisions** — if the user edited something outside a managed block, preserve it. Only delete/overwrite files easyskillz created.
5. **Automation** — agents run easyskillz on behalf of users. Users should be able to forget easyskillz exists.

## Audit Workflow

### 1. Identify Scope Automatically

**Never ask the user what to audit.** Detect scope intelligently:

1. Check if there are staged changes: `git diff --cached --name-only`
   - If yes: audit staged changes
2. If no staged changes, check unstaged: `git diff --name-only`
   - If yes: audit unstaged changes
3. If no uncommitted changes, check recent commits: `git log -1 --name-only`
   - Audit the most recent commit

**Use piping** to check all scenarios in one command:
```bash
git diff --cached || git diff || git diff HEAD~1..HEAD
```

The first non-empty result is what you audit. No user input required.

### 2. Extract Changes

Run the detected `git diff` command to get actual code changes. Parse the diff to identify:
- Modified files and line ranges
- Added files (entire content is new)
- Deleted files (usually safe, but check if they were user-owned)

### 3. Per-Principle Analysis

For each principle, scan the changes for violations:

#### P1: Centralise
**PASS if:**
- New features read from `.easyskillz/skills/` as source of truth
- Tool-specific directories (`.claude/skills/`, `.cursor/skills/`) are only written to, never read from
- No logic treats tool dirs as input

**FAIL if:**
- Code reads skill content from tool-specific directories
- Logic merges or reconciles tool dirs back into `.easyskillz/skills/`
- Any "sync from tool to central" pattern exists

**Common violations:**
- `fs.readFileSync(path.join(toolDir, 'skill', 'SKILL.md'))` — should read from `.easyskillz/skills/` instead
- Loops that scan tool directories to discover skills

#### P2: Never Force the User
**PASS if:**
- All filesystem writes check for existence first
- Managed blocks are used for files that may contain user content
- Operations are idempotent (safe to re-run)
- User is asked before destructive actions

**FAIL if:**
- `fs.writeFileSync` without checking if file exists
- Overwrites files without checking if they're managed
- Deletes files without verifying easyskillz created them
- No confirmation prompt for destructive operations

**Common violations:**
- `fs.writeFileSync(instructionFile, content)` — should check `fs.existsSync` first or use managed blocks
- `fs.unlinkSync` without checking if file is user-owned
- Missing `isManaged()` checks before overwriting instruction files

#### P3: Sync is the Entry Point
**PASS if:**
- New features are integrated into `easyskillz sync` workflow
- `sync` remains the one-command setup
- Documentation mentions `sync` as the primary command

**FAIL if:**
- New commands are required for initial setup
- `sync` no longer handles a critical setup step
- User must run multiple commands in sequence for first-time setup

**Common violations:**
- Adding a new `easyskillz init` command that's required before `sync`
- Splitting setup into multiple mandatory steps

#### P4: Respect User Decisions
**PASS if:**
- Managed blocks preserve user content outside markers
- Only easyskillz-created files are deleted
- User edits outside managed blocks are never touched

**FAIL if:**
- Deletes entire instruction files without checking for user content
- Overwrites user content outside managed blocks
- Removes user-added sections from instruction files

**Common violations:**
- `fs.unlinkSync(instructionFile)` without checking if file has content outside managed blocks
- Replacing entire file content instead of updating only managed sections
- No distinction between easyskillz-created and user-created files

#### P5: Automation
**PASS if:**
- Commands support `--json` flag for machine-readable output
- No interactive prompts when stdin is not a TTY
- Exit codes are correct (0 = success, non-zero = failure)
- Errors go to stderr, output to stdout

**FAIL if:**
- Missing `--json` support on new commands
- Interactive prompts in non-TTY environments
- Inconsistent exit codes
- Errors printed to stdout instead of stderr

**Common violations:**
- New command without `--json` flag
- `readline` prompts without TTY check
- `console.log` for errors instead of `console.error`

### 4. Generate Report

Output format:

```
# North Star Audit Report

## P1: Centralise — [PASS/FAIL]
[If FAIL: list violations with file:line and explanation]

## P2: Never Force the User — [PASS/FAIL]
[If FAIL: list violations with file:line and explanation]

## P3: Sync is the Entry Point — [PASS/FAIL]
[If FAIL: list violations with file:line and explanation]

## P4: Respect User Decisions — [PASS/FAIL]
[If FAIL: list violations with file:line and explanation]

## P5: Automation — [PASS/FAIL]
[If FAIL: list violations with file:line and explanation]

---

## Summary
- Principles passed: X/5
- Violations found: N
- Recommended actions: [list of fixes]
```

### 5. Actionable Fixes

For each violation, provide:
- Exact file and line number
- What the code currently does wrong
- How to fix it (code snippet if possible)
- Why it violates the principle

## Edge Cases

- **No changes found**: Report "No changes to audit" and exit gracefully
- **Non-easyskillz files**: If diff includes files outside `src/`, `bin/`, `tests/`, note that they're out of scope but still audit them if they interact with easyskillz logic
- **Test files**: Apply same principles — tests should also respect the design philosophy
- **Documentation changes**: P3 and P5 are most relevant — ensure `sync` is still documented as primary command and `--json` examples are present

## Example Invocations

**User**: "Audit my changes"
→ Auto-detect: `git diff --cached || git diff || git diff HEAD~1..HEAD`, analyze all 5 principles, report

**User**: "Review this PR before I merge"
→ Auto-detect scope, run appropriate diff, audit and report (no questions asked)

**User**: "Check if this new feature respects our design principles"
→ Auto-detect changes, analyze, report violations with file:line citations

**User**: "Is this code change safe to merge?"
→ Auto-detect scope, audit all 5 principles (focus on P2 and P4), report

**All invocations are autonomous** — the skill detects what to audit and runs the analysis without asking for confirmation or additional input.

## Supporting Files

- `CONTRIBUTING.md` — canonical source of North Star principles
- `src/` — all implementation code
- `tests/` — test files (should also follow principles)
- `bin/easyskillz.js` — CLI entry point

## Automation Strategy

This skill follows P5 (Automation) strictly:

- **Zero user prompts**: Never ask what to audit, which files, or which principles to check
- **Pipe all commands**: Use `||` to chain fallback detection (`git diff --cached || git diff || git diff HEAD~1..HEAD`)
- **Always check all 5 principles**: Never ask which principles to audit — check all of them every time
- **Exit codes matter**: Return 0 if all principles pass, non-zero if violations found
- **Machine-readable output**: Support `--json` flag for structured violation reports

The AI agent running this skill should execute it seamlessly without any back-and-forth with the user. The skill is self-contained and autonomous.

## Notes

- This skill is meta — it audits easyskillz itself, not user projects
- Focus on design integrity, not syntax or style
- A PASS means the change aligns with easyskillz philosophy
- A FAIL means the change introduces technical debt or violates core values
- Always provide specific file:line citations, never vague claims
- **Never interrupt the user** — detect, analyze, report, done
