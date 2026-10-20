---
description: "CB - Execute an approved plan from .claude/memories/ phase by phase"
---

You are tasked with implementing an approved technical plan stored as a markdown file in `.claude/memories/`. Plans contain phases with specific changes and success criteria.

## Getting Started

When given a plan file path:
- Read the plan file completely with the Read tool. **Read it fully — never use limit/offset parameters, you need complete context.**
- Check the frontmatter `status` field. Only build plans with `status: approved` (or `draft` if the user explicitly says so).
- Check for any existing checkmarks (- [x]) — these indicate already-completed work.
- Read all files mentioned in the plan, in full.
- Use the context7 MCP server (`resolve-library-id` then `query-docs`) to look up documentation for any third-party libraries or frameworks you need to work with — don't guess at API signatures or configuration options.
- Use the code-index MCP tools (`find_symbol`, `find_usage`, `get_file_outline`, `get_call_graph`) to understand how the touched code fits into the wider codebase before editing.
- Think deeply about how the pieces fit together.
- Start implementing once you understand what needs to be done.

**Important**: After implementation, you will automatically run the `plan-validator` agent to verify correctness, then address any findings before completion.

If no plan path was provided, list candidate plans:
```bash
ls -1t .claude/memories/*.md
```
Show the user the recent plans and ask which one to implement.

## Implementation Philosophy

Plans are carefully designed, but reality can be messy. Your job is to:
- Follow the plan's intent while adapting to what you find.
- Implement each phase fully before moving to the next.
- Verify your work makes sense in the broader codebase context.
- Update checkboxes in the plan as you complete sections by editing the plan file directly with the Edit tool.

When things don't match the plan exactly, think about why and communicate clearly. The plan is your guide, but your judgment matters too.

If you encounter a mismatch:
- STOP and think deeply about why the plan can't be followed.
- Present the issue clearly:
  ```
  Issue in Phase [N]:
  Expected: [what the plan says]
  Found: [actual situation]
  Why this matters: [explanation]

  How should I proceed?
  ```

## Branch Check

Before making any changes, verify you are not on `main`. If you are, create a feature branch from the plan topic (e.g. `feat/<topic>` or `fix/<topic>`). Use kebab-case. Never commit directly to main.

## Verification Approach

After implementing a phase:
- Run the success criteria checks (Automated Verification commands from the plan).
- Fix any issues before proceeding.
- Update progress — check off completed items in the plan by editing the plan file directly.

Don't let verification interrupt your flow — batch it at natural stopping points.

## Final Validation & Completion

Once you believe the implementation is complete:

### Step 1: Run Plan Validator

Use the Task tool to launch the `plan-validator` agent:

```
Task tool with:
- subagent_type: plan-validator
- prompt: "Validate the implementation of `.claude/memories/<plan-file>.md`. Verify all phases are complete, run automated checks, and identify any deviations or issues. Return a comprehensive validation report with specific findings."
```

### Step 2: Analyze Validation Results

Review the validation report carefully:

1. **Automated Verification Issues**:
   - If tests fail: Fix them immediately.
   - If linting fails: Address critical issues.
   - If build fails: Must be fixed before proceeding.

2. **Missing Implementation**:
   - If phases are incomplete: Implement them now.
   - If features are missing: Add them.
   - Update plan checkboxes as you complete items.

3. **Deviations from Plan**:
   - If deviation is an improvement: Document why in the plan.
   - If deviation is a problem: Fix it or justify why not.
   - If approach changed: Note the reason in the plan.

4. **Identified Issues**:
   - Security concerns: Address immediately.
   - Performance issues: Fix or document trade-off.
   - Missing error handling: Add it.
   - Edge cases: Implement handling or document why they're not relevant.

### Step 3: Address Findings or Document Exceptions

For each issue identified:

**If you implement it**:
- Make the changes.
- Update the plan to reflect completion.
- Mark the item as resolved.

**If you don't implement it**:
- Add a note to the plan explaining why:
  ```markdown
  ## Validation Notes

  ### Items Not Implemented
  - **[Issue]**: [Reason not implemented]
  ```

### Step 4: Append Validation Report to Plan

Edit the plan file and append the validation report at the end:

```markdown
---

## Validation Report

[Date]: [YYYY-MM-DD]

[Insert the validation report from the plan-validator agent]

### Resolution Notes
- [List what was fixed]
- [List what was documented as exception with reasoning]
```

### Step 5: Final Verification

After addressing all issues:
- Re-run automated checks to confirm everything passes.
- Update the plan frontmatter `status` to `built` (or `done` if the user prefers).

**Only after validation passes should you consider the implementation complete.**

### Step 6: Commit, Push, and Open PR

Once validation passes:

1. Stage and commit by file name (never `git add -A`). Use a Conventional Commit subject (e.g. `feat: <topic>`). No AI attribution lines.
2. Push the feature branch to `origin` (never to `upstream`).
3. Open a PR with `gh pr create --base <default-branch>`. Use a short title and a body that links to the plan path.
4. Capture the resulting PR number. If a `{{ output }}` path is provided to this step, write **only** the integer PR number (no `#`, no newlines beyond a trailing one) to that path. The next pipeline step uses this file to find the PR.

If the user has not authorised pushing in this session, stop and ask before pushing.

## If You Get Stuck

When something isn't working as expected:
- First, make sure you've read and understood all the relevant code.
- Consider if the codebase has evolved since the plan was written.
- Present the mismatch clearly and ask for guidance.

## Resuming Work

If the plan has existing checkmarks:
- Trust that completed work is done.
- Pick up from the first unchecked item.
- Verify previous work only if something seems off.

Remember: You're implementing a solution, not just checking boxes. Keep the end goal in mind and maintain forward momentum.
