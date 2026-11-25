---
name: fix
description: 'Fix bugs by reproducing, debugging, fixing, and testing. Supports cross-stack and hotfix workflows. Use: /fix [Notion ticket link or bug description]'
---

# /fix - Bug Fix

Fix bugs by reproducing the issue, finding root cause, implementing fix, and preventing regression.

**Input:** Notion ticket link or bug description via `$ARGUMENTS`

## When to use /fix vs /implement

- **Use /fix**: Bug reports, production issues, error fixes, incorrect behavior, performance issues
- **Use /implement**: New features, enhancements, new endpoints, schema changes (even if they fix a limitation)

## Workflow

### Step 1: Read the bug ticket

If `$ARGUMENTS` contains a Notion link:
- Use Notion MCP to read the ticket properties and description
- **Extract and save the ticket ID** — read `userDefined:ID` property from Notion response (e.g., `CRM-1279`) — you will use this for branch naming in Step 4
- **Read the "Stacks" property** (multi-select: BE, FE, App) to determine scope
- Look for: bug description, steps to reproduce, expected vs actual behavior, error messages
- Read any linked documents or related tickets
- **Images/Screenshots:** Notion MCP may not be able to read images. If the ticket mentions screenshots or you see image references:
  - Ask the user: "I see the ticket has screenshots/images attached. Please share them so I can see the error/bug visually."
  - Wait for user to attach images before proceeding
- If Notion MCP is unavailable, ask the user to paste the ticket content

If `$ARGUMENTS` is just a description:
- Use that as the bug description
- Ask user for reproduction steps if not clear
- If bug is visual (UI issue, wrong display), ask user to attach screenshot

**Critical information needed:**
- What is the expected behavior?
- What is the actual (buggy) behavior?
- How to reproduce it (exact steps)?
- Any error messages or stack traces?
- Screenshots (if the bug is visual or shows an error)

**If any critical information is missing:** Ask user before proceeding.

---

### Step 2: Detect stack and cross-stack scope

**Detect current stack:** Read `package.json` to determine current repo's stack (nestjs/nextjs/react-native).

**Determine scope from ticket status fields:**
- **Cross-stack**: ticket has BOTH `BE Status` AND `FE Status` properties → determine root cause stack first
- **Single-stack BE**: ticket has `BE Status` only (no `FE Status`)
- **Single-stack FE**: ticket has `FE Status` only (no `BE Status`)
- **Neither field**: infer from bug description, or ask user

**For cross-stack bugs, also check Notion comments:**
- If another stack already posted a fix or root cause analysis → reference it
- If root cause is clearly in the other stack → report to user with recommendation

---

### Step 3: Determine root cause stack

**Single-stack bug:** Skip this step, proceed to Step 4.

**Cross-stack bug:** Analyze where the root cause likely is:

| Symptom | Likely root cause |
|---------|-------------------|
| API returns wrong data | BE |
| API returns error 4xx/5xx | BE (unless FE sends wrong request) |
| UI displays wrong data | FE (if API response is correct) |
| UI crashes or errors | FE |
| Data not saving | Check both: FE request payload → BE handler |
| Performance issue | Profile both, fix where bottleneck is |

**If root cause is in CURRENT stack:** Proceed to Step 4.

**If root cause is in OTHER stack:**
1. Comment on Notion ticket with your analysis:
   ```
   🔍 Root cause analysis ({current_stack}):
   Bug appears to originate in {other_stack}.
   Evidence: [specific finding]
   Suggested fix: [what needs to change in other stack]
   ```
2. Report to user:
   ```
   Root cause is in {other_stack}, not {current_stack}.
   I've posted the analysis to the Notion ticket.
   Switch to {other_stack} repo and run: /fix [same ticket URL]
   ```
3. STOP. Do not attempt to fix code in the wrong stack.

**If root cause spans BOTH stacks:**
- Fix the current stack's portion first
- Note remaining work for the other stack in Notion comment

---

### Step 4: Create branch (if needed)

**Check current branch:**
- If already on a fix/hotfix branch for this ticket → skip
- If on `main` or `master` → create branch

**Branch naming:** Use the ticket `ID` extracted in Step 1 (e.g., `RRR-351`):
```bash
# Regular bug fix
git checkout -b fix/{ticket-id}-{short-slug}
# e.g.: git checkout -b fix/RRR-351-point-not-calculated

# Hotfix (production emergency) — branch from master
git checkout master && git pull && git checkout -b hotfix/{ticket-id}-{short-slug}
```

**Determine type:**
- Regular bug → `fix/`
- Production emergency → `hotfix/` (see Hotfix Workflow below)

If no ticket ID available, use descriptive slug: `fix/payment-timeout`

---

### Step 5: Locate the bug using docs

**5a — Read the index first (no scouting):**
- Read `docs/module-index.md` → find which Service/Controller/Entity is relevant to the bug
- Read `docs/code-standards.md` and `.claude/rules/stack-rules.md` for context

**5b — Read targeted files directly:**
- Use file paths from `module-index.md` to open exact files — no broad Grep exploration
- If `module-index.md` doesn't exist or doesn't cover the area: use Grep with specific terms (function name, endpoint, error message) as fallback

**Goal: 2-3 targeted reads, not broad scouting. Run `/docs init` if module-index.md is missing.**

---

### Step 6: Reproduce the bug

**Attempt to reproduce locally:**

**For API bugs:** Use curl or API client to reproduce the request
**For database bugs:** Query the database directly to check state
**For UI bugs:** Reproduce in browser/simulator
**For test failures:** Run the specific failing test

Use commands from `.claude/rules/stack-rules.md` for stack-specific tools.

**Document reproduction:**
- Did you successfully reproduce it? (Yes/No)
- If yes: what were the exact steps and what did you observe?
- If no: what's different from the bug report? (environment, data, timing)

**If you cannot reproduce:** Report to user and ask for clarification before proceeding.

---

### Step 7: Debug and find root cause

**Investigate directly** using Grep and Read — do NOT spawn sub-agents for routine bugs:

1. Search for the relevant function/endpoint from Step 5:
   ```bash
   # Search by function name, endpoint, or error message
   grep -rn "functionName\|/endpoint\|ErrorMessage" src/
   ```
2. Read the affected files (already identified in Step 5)
3. Trace the logic: follow the data flow from input → processing → output
4. Identify root cause: logic error, missing validation, wrong query, race condition, etc.

**Only spawn `debugger` agent if:**
- You've read the relevant files and still cannot identify root cause
- The bug involves complex multi-service interaction
- There are cryptic stack traces requiring deep analysis

**Document root cause:**
- Affected code location (file:line)
- Why the bug occurs

---

### Step 8: Implement the fix

Based on the root cause from Step 7, implement the fix:

**Read the affected file(s) first:**
- Understand the current logic and surrounding code
- Check for similar patterns elsewhere in the codebase

**Implement the fix:**
- Make the minimal change needed to fix the bug (KISS principle)
- Preserve existing behavior for non-buggy cases
- Add input validation if the bug was caused by invalid data
- Add error handling if the bug was an unhandled exception
- Follow project patterns from `.claude/rules/stack-rules.md`

**Common fix patterns:**
- Missing null checks: Add guards for nullable values
- Missing input validation: Add proper validation
- Logic errors: Fix conditionals or calculations
- Missing error handling: Add try-catch blocks
- Stack-specific patterns: See `.claude/rules/stack-rules.md` → "Debug Patterns"

---

### Step 9: Write unit tests

**Critical:** Write tests for ALL changed files, not just a regression test.

**Regression test (every fix):**
- If test file exists: add new test case reproducing the buggy scenario
  - Name: `it('should handle null workspace owner', ...)`
  - Assert expected (correct) behavior
- If no test file: create one following existing patterns in the module

**Unit tests for every changed file:**
- Every file modified in Step 8 → must have a corresponding test file
- Backend: `*.spec.ts` in same directory or `__tests__/` folder
- Frontend React components: `__tests__/[ComponentName].snapshot.test.tsx` minimum + behavior tests for changed logic
- If changing a utility function: update/add unit test covering the function's cases

---

### Step 10: Verify the fix

Run build/lint/test commands from `.claude/rules/stack-rules.md`.

**Verify the specific fix:**
- Re-run the reproduction steps from Step 6
- Confirm the bug no longer occurs
- Confirm expected behavior now happens

**If tests fail:**
- Read the failure message
- Determine if the fix broke something else or if the test needs updating
- Use `debugger` agent if stuck after 2 attempts

Do NOT proceed until all checks pass and the bug is verified fixed.

---

### Step 11: Update Notion ticket

If the ticket is from Notion:
- Add comment with:
  ```
  🐛 Bug fix ({stack}):
  Root cause: [one-line explanation]
  Fix: [what was changed]
  Regression test: [file path]
  Branch: [branch name]
  ```
- If cross-stack and other stacks still need fixes:
  ```
  ⚠️ Cross-stack: {other_stack} portion still needs fixing.
  See root cause analysis above.
  ```
- If status field name or options differ, report to user

If no Notion ticket, skip this step.

---

### Step 12: Handoff

**Single-stack fix:**
```markdown
## Bug Fix Complete

**Bug:** [brief description]
**Root cause:** [one-line explanation]
**Files changed:** [list]
**Regression test:** [file path]
**Verification:** [PASS / FAIL]

Next: /review
```

**Cross-stack fix (current stack done, other stacks remain):**
```markdown
## Bug Fix Complete ({stack})

**Bug:** [brief description]
**Root cause:** [one-line explanation]
**Files changed:** [list]
**Regression test:** [file path]

Cross-stack: {other_stack} portion still needs fixing.
After this stack: /review → /commit
Then switch to {other_stack} repo and run: /fix [same ticket URL]
```

---

## Hotfix Workflow

For production emergencies that need immediate deployment.

### When to use hotfix

- Production is down or critically broken
- Data corruption or security vulnerability
- User explicitly says "hotfix" or "urgent"

### Hotfix differences from regular fix

| Aspect | Regular fix | Hotfix |
|--------|------------|--------|
| Branch from | feature branch or main | Always `main` |
| Branch prefix | `fix/` | `hotfix/` |
| Scope | Full investigation | Minimal fix only |
| Review | Standard (2 approvers) | Expedited (1 approver) |
| Deploy | Next release cycle | Immediate |
| Follow-up | None needed | Post-mortem required |

### Hotfix steps

1. **Branch from master:** `git checkout master && git pull && git checkout -b hotfix/{id}-{slug}`
2. **Minimal fix only:** Fix the immediate issue, nothing else
3. **Regression test:** Still required, but keep it focused
4. **Verify:** Build + test must pass
5. **Handoff:**
   ```
   ## Hotfix Ready

   **Bug:** [description]
   **Root cause:** [brief]
   **Fix:** [what changed]
   **Impact:** [what was affected]

   Next: /review (expedited — 1 approver)
   After merge: deploy immediately
   ```
6. **After merge:** Add post-mortem comment to Notion ticket:
   ```
   📝 Post-mortem:
   - What happened: [description]
   - Root cause: [why it happened]
   - Fix applied: [what was changed]
   - Prevention: [how to prevent recurrence]
   ```

### Cross-stack hotfix

For hotfixes spanning multiple stacks, fix sequentially (not parallel):
1. Fix BE first → /review → /commit → deploy
2. Then fix FE → /review → /commit → deploy
3. Each stack has its own hotfix branch from main

---

## Rules

- **Always reproduce first:** Never fix a bug you can't reproduce (except in rare cases like race conditions)
- **Minimal changes:** Fix only what's broken, don't refactor unrelated code
- **Always add regression test:** Every bug fix MUST include a test that would have caught the bug
- **Root cause, not symptoms:** Fix the underlying cause, not just the visible symptom
- **Verify the fix:** Re-run reproduction steps to confirm bug is gone
- **Document in commit:** Commit message should reference bug ticket and explain what was fixed
- **Cross-stack scope:** Only fix code in current stack. If root cause is in another stack, post analysis to Notion and stop
- **Hotfix = minimal:** For hotfixes, fix only the immediate issue. Broader improvements go in a follow-up ticket
- Use `debugger` agent for complex issues (can't find root cause after 15 minutes of investigation)
- Use `tester` agent if regression test needs more comprehensive coverage analysis
- Follow `.claude/rules/development-rules.md`
- Keep fixes simple and targeted (KISS principle)
