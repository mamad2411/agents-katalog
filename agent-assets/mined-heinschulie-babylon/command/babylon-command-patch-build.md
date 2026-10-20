---
allowed-tools: Bash(gh *), Bash(bun *), Read, Grep, Glob, Write
description: Create fix sub-issues from a build review's gaps, ready for the next ralph loop
argument-hint: [path to build review file]
model: opus
---

# Purpose

Read a build review (output of `/review-build`) and turn its **Gaps** checklist into actionable GitHub sub-issues on the original parent issue. Each gap becomes either a reopened existing sub-issue or a new sub-issue — ready for the next ralph loop run.

## Variables

REVIEW_PATH: $ARGUMENTS

## Instructions

- Read the review file FULLY before doing anything else.
- Extract the parent issue number from the review's build metadata (build directory name contains it, e.g. `83_ralph_*`).
- Extract every gap item from the `### Gaps` section — each `- [ ]` line is a gap.
- For each gap, determine whether it maps to an existing closed sub-issue or needs a new one:
  - **Reopen**: if the gap clearly corresponds to an existing closed sub-issue (same feature scope), reopen it with `gh issue reopen` and add a comment explaining what's still missing.
  - **Create new**: if the gap is a new concern not covered by any existing sub-issue, create a new sub-issue linked to the parent.
- Group related gaps into a single issue when they belong to the same feature slice (e.g. "clickable tag filtering", "clear filter button", and "tag cloud section" all belong to the same poll tag filtering slice).
- New sub-issues MUST follow the issue template from the Workflow section.
- Use `createSubIssue()` from `adws/src/github.ts` for new issues — it handles creation + GraphQL sub-issue linking.
- Label new issues with `auto-fix`, `sub-issue`, and the appropriate `complexity:<level>`.
- After all issues are created/reopened, list them as a summary.

## Workflow

1. **Read the review** — read `REVIEW_PATH` fully. Parse the Gaps section and the build metadata.
2. **Fetch parent context** — use `gh issue view <parent>` to get the parent issue body (the PRD). Use the GraphQL sub-issues query to find existing closed sub-issues under the parent:
   ```bash
   gh api graphql -f query='
     query($owner:String!,$name:String!,$num:Int!){
       repository(owner:$owner,name:$name){
         issue(number:$num){
           subIssues(first:50,includeClosedItems:true){
             nodes{number,title,state}
           }
         }
       }
     }' -F owner='{owner}' -F name='{repo}' -F num=PARENT_NUMBER
   ```
3. **Map gaps to issues** — for each gap (or group of related gaps):
   a. Check if an existing closed sub-issue covers this scope
   b. If yes: reopen it (`gh issue reopen <number>`) and comment with the specific unmet requirements from the review
   c. If no: create a new sub-issue using the template below
4. **Create new sub-issues** — use `createSubIssue()` from `adws/src/github.ts`:
   ```bash
   bun -e "
   import { createSubIssue } from './adws/src/github.ts';
   const result = await createSubIssue(PARENT_NUMBER, 'Fix: <title>', \`FULL_BODY\`, ['auto-fix', 'sub-issue', 'complexity:standard']);
   console.log(JSON.stringify(result));
   "
   ```
5. **Report** — output the summary per the Report section.

### Issue Template (for new sub-issues)

```
## Review Defect

**Source review**: <path to review file>
**Original issue**: #<number of the closed sub-issue this relates to, or "new">

## Interface Specification

<What needs to be built or fixed — specific enough for a TDD agent to write tests from this section alone. Include function signatures, component specs, props, i18n keys.>

## Behaviors to Test (prioritized)

1. <Most critical behavior>
2. <Next most critical>
3. ...

## Mocking Boundaries

- **Real**: <what's real in tests>
- **Stubbed**: <what's stubbed>

## Acceptance Criteria

- [ ] <Criterion 1>
- [ ] <Criterion 2>
- [ ] ...

## Dependencies

- **Blocked by**: None — can start immediately
- **Blocks**: None
```

## Report

Present the patch summary in this format:

```
## Patch Summary

**Parent issue**: #<number>
**Review**: <REVIEW_PATH>

### Reopened Issues
| # | Title | Gaps addressed |
|---|-------|---------------|
| <number> | <title> | <which gaps> |

### New Issues Created
| # | Title | Gaps addressed |
|---|-------|---------------|
| <number> | <title> | <which gaps> |

### Remaining (not actionable)
- <any gaps that couldn't be mapped to issues, with explanation>
```
