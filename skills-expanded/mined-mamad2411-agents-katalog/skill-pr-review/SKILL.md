---
name: skill-pr-review
description: Comprehensive code review for pull requests using parallel multi-agent analysis. Audits CLAUDE.md compliance, checks for bugs, analyzes git history, reviews comments, and filters by confidence score. Use when reviewing a GitHub PR, mentions "code review", "review this PR", or "/code-review".
version: 1.0.0
allowed-tools: 
  - Bash(gh issue view:*)
  - Bash(gh search:*)
  - Bash(gh issue list:*)
  - Bash(gh pr comment:*)
  - Bash(gh pr diff:*)
  - Bash(gh pr view:*)
  - Bash(gh pr list:*)
---

# Skill: Pull Request Code Review

Multi-angle code review using 5 parallel agents + confidence scoring. Audits CLAUDE.md compliance, detects bugs, checks git history, reviews prior feedback, validates comment guidance. Filters issues by confidence (≥80) to reduce false positives.

## Process Overview

```
1. Eligibility check (Haiku)
   ├─ Skip if: closed, draft, automated, trivial, already reviewed
   │
2. Collect CLAUDE.md files (Haiku)
   ├─ Root CLAUDE.md + phase-specific CLAUDE.md files
   │
3. Get PR summary (Haiku)
   ├─ Understand the change at high level
   │
4. Parallel 5-agent review (5x Sonnet)
   ├─ Agent #1: CLAUDE.md compliance audit
   ├─ Agent #2: Shallow bug scan (large bugs only)
   ├─ Agent #3: Git blame & history context
   ├─ Agent #4: Prior PR comments (similar files)
   └─ Agent #5: Code comments in modified files
   │
5. Confidence scoring (Parallel Haiku agents)
   ├─ Score each issue 0-100
   ├─ Filter: keep only score ≥ 80
   │
6. Final eligibility check (Haiku)
   ├─ Verify PR still eligible (not closed/merged while reviewing)
   │
7. Post comment via gh (Bash)
   └─ Format: brief description, file link with full SHA, line range
```

## Step 1: Eligibility Check

Skip review if:
- **Closed**: PR is already closed
- **Draft**: PR marked as draft
- **Automated**: Author is bot/automation (e.g., dependabot)
- **Trivial**: Obvious fix (typo, docs, one-liner) with no risk
- **Pre-reviewed**: You already reviewed this PR earlier

Use:
```bash
gh pr view <number> --json state,isDraft,author,commits
```

## Step 2: Collect CLAUDE.md Files

Gather all relevant CLAUDE.md files:
- Root `./CLAUDE.md` (if exists)
- Any `./some-phase/CLAUDE.md` (if modified files are in that phase)
- Any `./services/*/CLAUDE.md` (if monorepo, for modified service)

Use:
```bash
gh pr diff <number> --name-only | xargs -I {} dirname {} | sort -u | xargs -I {} find {} -name CLAUDE.md
```

## Step 3: Get PR Summary

Fetch PR metadata and commit summary:

```bash
gh pr view <number> --json title,body,commits
```

Ask agent: "Summarize this PR in 2-3 sentences. What changed and why?"

## Step 4: Parallel 5-Agent Review

Launch 5 agents in parallel (one per strategy). Each agent returns a list of issues found.

### Agent #1: CLAUDE.md Compliance

- Read CLAUDE.md file(s) from step 2
- Check if changes violate explicit rules in CLAUDE.md
- Flag only issues **explicitly mentioned** in CLAUDE.md (not general best practices)
- Ignore issues if code has lint-ignore comments

Example issues:
- CLAUDE.md says "always use pnpm", but PR introduces npm
- CLAUDE.md forbids modifying .env, but PR modifies .env
- CLAUDE.md says "do not access DB outside src/db/", but PR queries DB in src/api/

### Agent #2: Shallow Bug Scan

- Read PR diff (`gh pr diff`)
- Scan for **large, obvious bugs** only
- Ignore: nitpicks, style, lint issues, type errors, missing tests
- Focus on logic errors, bounds checks, null pointer risks, hardcoded values

Example issues:
- Off-by-one loop error
- Missing null check before .length access
- Hardcoded password or API key
- SQL injection due to string concatenation

### Agent #3: Git History & Blame

- Use `git log` on modified files to understand context
- Look for: related commits, previous bug fixes in same code, warnings in commit messages
- Flag if new code conflicts with historical patterns

Example issues:
- Previous commit explicitly fixed this pattern, but PR reintroduces it
- Code was refactored 3 months ago to avoid this approach, PR undoes it

### Agent #4: Prior PR Comments

- Search prior PRs that touched modified files (`gh search prs --repo=... --involved=<author>`)
- Look for: reviewer comments, feedback on similar code, known issues
- Flag if same issue is being re-introduced

Example issues:
- PR #42 had same change, reviewer flagged issue X, now issue X reappears here

### Agent #5: Code Comments

- Read code comments in modified files
- Flag if changes violate guidance in comments (e.g., "DO NOT modify this", "precondition: X must be true")

Example issues:
- Comment says "This value must be immutable", but PR mutates it
- Comment says "DO NOT call this without Y", but PR calls without Y

## Step 5: Confidence Scoring

For each issue found, launch a Haiku agent to score 0-100:

**Rubric** (give to agent verbatim):

- **0**: Not confident. False positive, doesn't stand up to scrutiny, or pre-existing issue.
- **25**: Somewhat confident. Might be real, but unverified. If stylistic, not in CLAUDE.md.
- **50**: Moderately confident. Real issue, but nitpick or rare. Not very important.
- **75**: Highly confident. Verified real issue, will happen in practice. Important, directly impacts functionality or in CLAUDE.md.
- **100**: Absolutely certain. Double-checked, confirmed real. Happens frequently, direct evidence.

**Filter**: Keep only issues with score ≥ 80.

## Step 6: Final Eligibility Re-check

Before posting, verify PR still eligible:
```bash
gh pr view <number> --json state,isDraft
```

If closed/merged/draft, abort.

## Step 7: Post Comment

Use `gh pr comment`:

```bash
gh pr comment <number> --body "
### Code review

Found X issues:

1. <brief description> (CLAUDE.md says \"<...>\")

https://github.com/owner/repo/blob/<full-sha>/path/to/file.md#L10-L15

2. <brief description> (bug in <file>)

https://github.com/owner/repo/blob/<full-sha>/path/to/file.md#L20-L25

🤖 Generated with [Claude Code](https://claude.ai/code)

<sub>- If this code review was useful, please react with 👍. Otherwise, react with 👎.</sub>
"
```

**Or, if no issues**:

```bash
gh pr comment <number> --body "
### Code review

No issues found. Checked for bugs and CLAUDE.md compliance.

🤖 Generated with [Claude Code](https://claude.ai/code)
"
```

## Requirements for Links

When linking to code:
- Use **full git SHA** (40 chars), not branch name
- Format: `https://github.com/owner/repo/blob/<sha>/file/path#L<start>-L<end>`
- Include at least 1 line context before and after the issue
- Line format: `L4-L7` (not `L4..7` or other variants)

Example:
```
https://github.com/anthropics/claude-code/blob/1d54823877c4de72b2316a64032a54afc404e619/README.md#L13-L17
```

## False Positives to Avoid

- Pre-existing issues (not introduced by this PR)
- Things that look like bugs but aren't
- Pedantic nitpicks (senior engineer wouldn't call out)
- Issues linter/typechecker catch (don't run CI yourself)
- General code quality (unless required by CLAUDE.md)
- Lint-ignored issues in code
- Intentional functionality changes
- Issues on lines the user didn't modify

## False Positive Examples

❌ "Missing test coverage" (unless CLAUDE.md requires it)  
❌ "Function name is unclear" (style, not bug)  
❌ "import statement on wrong line" (linter will fix)  
❌ "Off-by-one in code from 2 years ago" (pre-existing)  
❌ "This function doesn't handle null" (handled 2 lines later)  
✅ "PR reintroduces bug fixed in commit abc123"  
✅ "CLAUDE.md forbids this approach, PR violates it"  
✅ "Off-by-one in code just added by this PR"  

## Integration with SDLC

**Phase 4 (Testing & Security)**: Code review as part of quality gates  
**Phase 5 (Deploy)**: Pre-merge validation before CI/CD  
**Utilities**: Anytime parallel review needed

---

**Status**: Ready for production PR reviews  
**Best for**: High-confidence, multi-angle code review; parallel agent coordination
