---
name: run-test-plan
description: Interactive test session guided by a test plan. Use when user says "run test plan", "start testing", "let's test", "test this branch", "run tests", or wants to walk through test scenarios on their local machine.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Run Test Plan

Interactive testing co-pilot that walks through test scenarios with the user. The agent sets up state, triggers actions, verifies outcomes, and tracks results — the user handles UI interactions and observes behavior.

This skill runs on the **local machine** where the application is running.

## Instructions

### Step 1: Find and Load Test Plan

1. Get the current branch: `git branch --show-current`
2. Read the test plan at `plans/{branch-name}/test-plan.md`
3. If no test plan exists:
   - Tell the user: "No test plan found for branch `{branch-name}`. Run `/create-test-plan` on the server agent first, then pull the branch."
   - Stop here.
4. Read the implementation plan too (if it exists) for additional context on decisions and edge cases.

### Step 2: Check Prerequisites

Go through the Prerequisites section of the test plan:

1. **Verify MCP connectivity** — attempt a simple query on each required MCP tool listed in the test plan (database ping, cache `DBSIZE`, cloud `get-caller-identity`, observability `list_resources`, etc.).
2. **Report status** to the user:
   ```
   Test plan loaded for branch `{branch-name}`: {N} scenarios

   Prerequisites:
   - [x] db: connected
   - [x] cache: connected
   - [ ] observability: not connected — start with the project's local-run command
   - [ ] public tunnel: needed for scenarios 5-7

   Ready to start with scenario 1? (or pick a specific scenario number)
   ```
3. If critical MCP tools are unavailable, note which scenarios will be skipped.

### Step 3: Run Scenarios Interactively

For each scenario the user wants to run:

#### 3a. Present the Scenario

Tell the user:
- What we're testing and why (from the test plan)
- What the agent will set up
- What the user needs to do (if anything)

#### 3b. Execute Setup

Run the setup steps from the test plan using MCP tools:
- Execute SQL via the database MCP (or staging equivalent)
- Set cache keys via the cache MCP
- Send queue messages via the messaging MCP
- Configure secrets/parameters if needed

**Adapt as needed** — the test plan has template SQL with placeholders. Fill in actual IDs, generate UUIDs, use current timestamps. Report what was created:
```
Setup complete:
- Created entity ID: {id}
- Created dependent row with expected defaults
- Session token: {token}
```

#### 3c. Guide the Action

If the action is user-driven (UI):
- Tell the user exactly where to go and what to do
- Wait for them to confirm they've done it

If the action is agent-driven (API call, queue message):
- Execute it and show the result

#### 3d. Run Verification

After the action completes, run all verification steps:
- Execute verification SQL queries and compare against expected results
- Check cache state
- Query event stores (via the project's event-store MCP)
- Search observability logs and traces for expected entries
- Search observability logs for unexpected errors or warnings

Present results clearly:
```
Verification for Scenario 1: {scenario title from the test plan}

  [PASS] Database: target record created with correct fields
  [PASS] Database: dependent row created with expected defaults
  [PASS] Events: {EventName} found in stream {Aggregate}:{id}
  [PASS] Logs: no errors in structured logs for this trace
  [FAIL] Cache: expected key not found
         Actual: key does not exist
         Expected: key present

Scenario 1: FAIL (1 issue)
```

#### 3e. Handle Failures

When a verification fails:
- Show the expected vs actual values
- Check observability logs for related errors or warnings
- Check traces to see where the flow diverged
- Suggest what might be wrong based on the evidence
- Ask the user how to proceed: investigate further, skip, or re-run after a fix

#### 3f. Record Result

Track pass/fail for each scenario. Move to the next scenario when the user is ready.

### Step 4: Session Summary

After all scenarios (or when the user stops):

```
Test Session Summary for `{branch-name}`

  Scenario 1: {happy-path title}             PASS
  Scenario 2: {edge-case title}              PASS
  Scenario 3: {idempotency replay}           PASS (idempotency)
  Scenario 4: {downstream-dependent title}   FAIL — expected state missing
  Scenario 5: {tunnel-dependent title}       SKIP — tunnel not running
  Scenario 6: {follow-up title}              SKIP — depends on scenario 5

Result: 3 passed, 1 failed, 2 skipped

Failed scenarios need investigation:
- Scenario 4: expected cache key not created during the action under test.
  Observability trace shows the upstream call completed but the cache
  write did not run. Check the relevant cache-writer component.
```

### Step 5: Write Test Results

After the session (all scenarios run, or user stops), write `plans/{branch-name}/test-results.md`:

```markdown
# Test Results: {Feature Title}

Branch: `{branch-name}`
Tested: {date and time}
Test Plan: `plans/{branch-name}/test-plan.md`

## Summary

| # | Scenario | Category | Result |
|---|----------|----------|--------|
| 1 | {title} | {category} | PASS |
| 2 | {title} | {category} | FAIL |
| 3 | {title} | {category} | SKIP — {reason} |

**Result: {N} passed, {N} failed, {N} skipped**

## Failures

### Scenario {N}: {Title}

**Expected:** {what should have happened}
**Actual:** {what actually happened}

**Evidence:**
- Database: {SQL query and actual result}
- Logs: {relevant observability log entries — level, message, exception if any}
- Traces: {trace spans showing where the flow diverged}

**Diagnosis:** {agent's assessment of what's likely wrong and where to look in the code}

---
```

Do NOT commit or push automatically. Leave the test results file in the working tree so review skills can inspect the session's output. The user will commit when ready using `/commit`.

This file is picked up by the server agent to fix failures — it has all the diagnostic evidence needed without re-explanation.

### Step 5b: Knowledge Capture — Rule Check

After writing test results, review whether test failures revealed undocumented constraints worth capturing:

1. **Check for recurring patterns** — did test failures reveal undocumented constraints, edge cases, or behavioral requirements not covered by existing `.agents/rules/` files?
2. **Search existing rules** — grep `.agents/rules/` and `AGENTS.md` by keywords to confirm the pattern is not already documented.
3. **If a new rule is warranted**, suggest `/create-rule` with:
   - The pattern (rule text)
   - The anti-pattern (the code or assumption that caused the test failure, with example)
   - The evidence (source: test failure in this session, scenario number, what was expected vs. actual)
   - Suggested context tags (what kind of work this applies to)

**Do NOT write rule files directly** — `/create-rule` handles dedup, ID assignment, index update, and source tracking.

Skip this step if all scenarios passed or failures were purely environmental (e.g., MCP connectivity, missing test data).

## Critical Rules

- **One scenario at a time** — present, set up, act, verify, then ask before moving to the next. Never rush ahead.
- **The user decides the pace** — they might want to investigate a failure for 20 minutes, skip scenarios, or run them out of order. Follow their lead.
- **Adapt the test plan** — the plan has template SQL. Generate real IDs, use current timestamps, adjust for actual database state. If a prerequisite entity doesn't exist, create it.
- **Verify with evidence, not assumptions** — always run the verification queries. Never say "that should work" without checking.
- **Use observability for debugging** — when something fails, check structured logs and traces immediately. This is the fastest way to understand what happened.
- **Clean up between scenarios if needed** — if scenario state would interfere with the next scenario, clean it up. Mention what you're cleaning.
- **Don't modify application code** — this skill is for testing only. If a bug is found, report it clearly so it can be fixed in a separate session.
- **Always write test results** — at the end of every session, write `test-results.md`. The server agent needs this to fix failures. Never skip this step, even if all scenarios passed (it confirms the feature works). Do NOT commit or push — the user will commit when ready.
- **Be a good co-pilot** — explain what you're seeing in the data. Help the user build intuition for how the feature works by narrating what each verification reveals about the system behavior.

## Reference

- `.agents/skills/create-test-plan/SKILL.md` — companion skill that generates the test plan
- `AGENTS.md` — project constraints and conventions
