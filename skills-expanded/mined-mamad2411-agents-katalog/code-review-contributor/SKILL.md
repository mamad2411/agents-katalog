---
name: code-review-contributor
description: |
  Use this skill whenever the user gives you a GitHub repository URL and asks you to review it,
  find bugs and optimization opportunities, and submit a PR as a contributor. Also trigger it
  when the user says things like "帮我混个 contributor", "对这个仓库来一遍", "review this repo",
  "find bugs and fix them", or any request involving auditing a codebase to find and fix issues
  with a pull request. The user may not always explicitly say "review and PR" — they might just
  paste a GitHub URL and expect the full workflow.
---

# Code Review & PR Contributor Workflow

When a user gives you a GitHub repository URL, follow this workflow from start to finish.

## Phase 1: Setup

1. **Determine the clone location.** Default: `~/Documents/<repo-name>/`. If they already said where, use that.
2. **Clone the repo**: `git clone <url> <path>`
3. **cd into the project** and note the primary programming language(s) from the file structure.
4. **Read key config files first**: `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `CMakeLists.txt`, etc. — whatever the language uses. This gives you the project's dependencies, version, and build system context.

## Phase 2: Comprehensive Code Review

Systematically read through the codebase. Do NOT skim — read every significant source file.

**What to look for:**
- Bugs: logic errors, race conditions, missing null checks, broken error handling, incorrect API usage
- Performance issues: unnecessary allocations, blocking I/O in async contexts, missing caches, N+1 queries
- Security issues: injection vectors, token leaks, missing input validation, unsafe defaults
- Code quality: dead code, duplicated logic, misleading comments, deprecated API usage

**How to organize:**
- Use parallel exploration agents for large codebases (split by directory or concern)
- For each finding, record the exact file path and line numbers
- Focus on concrete, actionable issues — not stylistic nitpicks

## Phase 3: Present Findings

Present a ranked list to the user, organized by severity:

- **Critical**: Crashes, data loss, security breaches, silent corruption
- **High**: Significant bugs, major performance issues, important security concerns  
- **Medium**: Clear bugs but limited blast radius, moderate optimizations
- **Low**: Cosmetic issues, minor inefficiencies

For each finding include: file path with line number, what's wrong, and why it matters.

## Phase 4: Recommend and Confirm

Based on your analysis, recommend which fixes to apply. Criteria for selection:

- **Impact**: How much does this affect users or correctness?
- **Fixability**: Can it be fixed cleanly with a small, reviewable change?
- **Reviewer appeal**: Would a maintainer look at this fix and think "yes, this is clearly correct"?

Default to 3 fixes — it's a good PR size that's easy to review. But if there's one overwhelmingly important fix, one is fine. If the user has asked for more, suggest 4-5.

Present your recommendation and ask the user to confirm.

## Phase 5: Fix and PR

Once the user confirms which issues to fix:

1. **Fork the repo** (if not already forked):
   ```bash
   gh repo fork --remote
   ```
   This updates `origin` to the fork and adds `upstream` to the original.

2. **Create a branch** with a descriptive name:
   ```bash
   git checkout -b fix/<brief-description-of-all-fixes>
   ```
   Use kebab-case. Examples: `fix/race-condition-and-memory-leak`, `fix/import-crash-and-cache-miss`

3. **Apply the fixes.** Each fix should be minimal and focused — no unrelated refactoring.

4. **Verify the diff** looks correct:
   ```bash
   git diff
   ```

5. **Commit** with a descriptive message. **Use the primary language of the repository** for the commit message and PR description. If the repo is Chinese, write in Chinese. If English, write in English. Default to English if mixed.

   Message format:
   ```
   fix: <summary of what was fixed>
   
   - <file/area>: <specific change>
   - <file/area>: <specific change>
   ```

6. **Push** to the fork:
   ```bash
   git push origin <branch-name>
   ```

7. **Create the PR** against the upstream main branch:
   ```bash
   gh pr create \
     --base main \
     --head <your-fork>:<branch-name> \
     --title "<descriptive title>" \
     --body "<structured description with Summary and Test plan sections>"
   ```

   The PR body should include:
   - **Summary**: Bullet points of what each fix does
   - **Test plan**: Checklist of manual verification steps (checked boxes for what you verified, unchecked for what needs CI/runtime)

8. **Report the PR URL** to the user.

## Language Matching

The commit message and PR title/body should match the repository's primary language:

- English repo → English PR
- Chinese repo → Chinese PR
- Japanese repo → Japanese PR
- Mixed/international → default to English

This shows respect for the project's community and makes the PR easier for maintainers to review.

## Branch Naming

Use descriptive kebab-case names prefixed with `fix/`:
- Good: `fix/lazy-ffmpeg-check-and-workflow-cache`
- Good: `fix/race-condition-in-session-tracking`
- Avoid: `fix-bugs`, `patch-1`, generic names

## Things NOT to Do

- Don't introduce new features or refactoring beyond the scope of the fix
- Don't add comments unless the why is truly non-obvious
- Don't skip the fork step — pushing directly to the upstream repo will fail
- Don't create the PR until all fixes are committed and pushed
- Don't over-engineer: three similar lines is better than a premature abstraction
