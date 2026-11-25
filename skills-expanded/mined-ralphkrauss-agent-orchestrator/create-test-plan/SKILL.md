---
name: create-test-plan
description: Generate an interactive test plan for manual testing with a local Claude Code agent. Use when user says "create test plan", "test plan", "testing plan", "write test plan", or after implementation is complete and before PR creation.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Create Test Plan

Generates a structured test plan that a **local Claude Code agent** will use to walk the user through interactive testing. The local agent has MCP access to the project's stateful surfaces (databases, caches, queue/event buses, observability dashboards) - it actively sets up state, triggers actions, and verifies outcomes while the user handles UI interactions.

This skill runs on the **server agent** (where implementation happened). The output is left in the working tree for review - the user commits and pushes when ready using `/commit`.

## Instructions

### Step 1: Gather Context

1. Get the current branch: `git branch --show-current`
2. Read the implementation plan at `plans/{branch-name}/plan.md` and all sub-plans
3. Read the full diff: `git diff main...HEAD --stat` and `git diff main...HEAD --name-only`
4. Identify what changed:
   - Which features were added or modified?
   - Which integrations are involved?
   - Are there money-handling or other safety-critical flows?
   - Are there UI changes?
   - Are there background jobs, queue consumers, or message handlers?
   - Are there database schema changes?
5. If the project maintains domain-specific test-plan runbooks (e.g. for integration-heavy flows), read them before drafting the plan.

### Step 2: Determine Test Environment

Based on the changes, determine which MCP tools the local agent will need:

| Change Type | MCP Tools | Notes |
|-------------|-----------|-------|
| Database state setup/verification | local/staging DB MCP server | SQL inserts, queries |
| Cache state | cache MCP server | Key inspection, setup |
| Queue/message testing | local message-bus / cloud MCP server | Send/receive, event inspection |
| Real upstream integration | staging credential MCP server | Real creds via secrets store |
| Logs and traces | observability MCP server | Structured logs, distributed traces |
| API endpoint testing | Bash (`curl`) | HTTP requests to local endpoints |

Flag if staging access is needed (real upstream calls, real payments, etc.).

### Step 3: Design Scenarios

For each feature area in the diff, create test scenarios covering:

1. **Happy path** - the normal flow works end to end
2. **Edge cases** - boundary conditions identified in the plan's Risks & Edge Cases
3. **Idempotency** - replay the same action and verify no duplicate side effects
4. **Error handling** - invalid input, provider errors, timeout behavior
5. **Concurrency** (if applicable) - simultaneous operations on the same entity
6. **Empty/null states** (for UI) - what renders when there's no data

Each scenario must have:
- **Setup**: concrete MCP operations to create the test state (SQL inserts, Redis keys, SQS messages, SSM config)
- **Action**: what happens - either user action (navigate, click, submit) or agent-triggered (curl, SQS publish)
- **Verify**: concrete MCP operations to check outcomes (SQL queries, cache reads, event-store queries, observability log/trace checks)

For integration-heavy work, group scenarios into execution buckets when relevant:

- `Local-core` - executable with the local app and local infrastructure only
- `Integration-backed` - requires valid third-party credentials and reachable upstream endpoints
- `Optional live` - valuable but non-blocking, usually requiring public callback routing or full live traffic

Also add a short `Scenario Coverage Map` so the local agent can quickly see which scenario ranges cover which runtime risks.

For idempotency-sensitive flows, also design verification so a replay proves both:

- no duplicate persisted rows
- no duplicate emitted events / outbound calls for the replayed operation

### Step 4: Write the Test Plan

Create `plans/{branch-name}/test-plan.md` with this structure:

```markdown
# Test Plan: {Feature Title}

Branch: `{branch-name}`
Implementation Plan: `plans/{branch-name}/plan.md`
Created: {date}

## Use This File

State whether this is the single-entry current-branch runbook, whether any historical source exists, and where the agent should write `test-results.md`.

## Current Scope

State what is in scope, what is intentionally out of scope, and any ownership boundaries between third-party-owned behavior and in-house platform behavior.

## Execution Order

Tell the local agent what to run first. Prefer local-core coverage before provider-dependent coverage.

## Prerequisites

What must be running before testing:

- [ ] Application running locally (use the project's standard run command)
- [ ] Public tunnel active - only if testing third-party callbacks
- [ ] Staging credentials/config loaded - only if testing real upstream integration
- [ ] {any feature-specific prerequisites}

## Local Test-State Policy

State the intended setup path for stateful prerequisites:

- normal product flow
- CLI command
- queue/message trigger
- direct local DB seed

If direct local DB seeds are required, say so explicitly, including tagging and cleanup boundaries.

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `{db-mcp}` | {what it's used for in these tests} |
| `{cache-mcp}` | {what it's used for} |
| `{messaging-mcp}` | {what it's used for} |
| `{observability-mcp}` | {what it's used for} |

## Runtime Variables

List the values the agent resolves once and reuses: base URLs, user/account IDs, provider IDs, credentials source, game/campaign identifiers, etc.

## Helper Snippets

Include only the snippets the agent needs, such as HMAC helpers, discovery SQL, webhook examples, queue payloads, or shell commands.

## Evidence Surfaces

State where runtime truth lives for this branch:

- database rows
- event streams
- request/response audit

For financial callbacks, require the runner to verify payload contents, not just that rows or pairs exist.

## Scenario Coverage Map

| Area | Scenarios |
|------|-----------|
| {coverage area} | `{scenario range}` |

## Scenarios

### 1. {Scenario Title}

**What we're testing:** {plain-language explanation of what this verifies and why it matters}
**Category:** happy-path | edge-case | idempotency | error-handling | concurrency | ui-state | setup | operational

#### Setup

Steps the agent performs via MCP before the test:

```sql
-- db: seed primary entity and dependent rows
INSERT INTO {primary_table} (...) VALUES (...);
INSERT INTO {dependent_table} (...) VALUES (...);
```

```text
-- cache: set required state (if needed)
SET {entity}:123:state "..."
```

```bash
-- cloud/secrets: configure required parameters (if needed)
aws ssm put-parameter --name "/local/..." --value "..." --type String --overwrite
```

#### Action

What triggers the behavior being tested:

**User action:**
> Navigate to `https://localhost:5001/path` and {do something specific}

**- or - Agent action:**
```bash
curl -X POST https://localhost:5001/api/... -H "Content-Type: application/json" -d '{...}'
```

**- or - Queue trigger:**
```text
-- aws-local: send message to SQS
aws sqs send-message --queue-url "..." --message-body '{...}'
```

#### Verify

What the agent checks after the action:

```sql
-- db: verify the expected database state
SELECT ... FROM ... WHERE ...;
-- Expected: {describe expected result}
```

```text
-- observability: check for expected log entries
list_structured_logs with filter: {resource, level, message pattern}
-- Expected: {describe expected log}
```

```text
-- observability: verify trace shows correct flow
list_traces with filter: {operation name}
-- Expected: {describe expected trace spans}
```

```sql
-- postgres-local: verify no duplicate records (idempotency)
SELECT COUNT(*) FROM ... WHERE ...;
-- Expected: exactly 1
```

#### Result

- [ ] Pass
- [ ] Fail - Notes: {filled during testing}
- [ ] Blocked - Reason: {filled during testing}
- [ ] Skipped - Reason: {filled during testing}
- [ ] Partial - Notes: {filled during testing}

---

### 2. {Next Scenario}
...
```

### Step 5: Write Scenario SQL/Commands with Real Schema

When writing setup and verification SQL:

1. **Check the actual database schema** - read the EF entity configurations and migrations to get exact table names, column names, and types
2. **Use realistic test data** - real-looking names, valid enum values, proper foreign key references
3. **Include cleanup hints** - if a scenario creates state that might interfere with later scenarios, note what to clean up
4. **Use parameterized values with placeholders** - mark values the local agent should adapt: `{entity_id}`, `{generated_uuid}`, etc.
5. **Document ownership boundaries** - if an in-house surface is adjacent to a third-party-owned flow, tell the tester what should count as an upstream failure versus an in-house follow-up

### Step 6: Leave for Review

Do NOT commit or push automatically. The test plan file is in the working tree and can be reviewed with `/review` or `/review-codex`. The user will commit when ready using `/commit`.

## Critical Rules

- **Scenarios are for human + agent walkthrough** - not automated execution. Write them as a conversation guide.
- **Be concrete** - every setup step must have actual SQL/commands, not "insert a test entity." The local agent should be able to copy-paste and adapt.
- **Include the WHY** - each scenario must explain what it's verifying and why it matters. This helps the user understand the feature.
- **Use real schema** - check entity configurations for exact table/column names. Wrong SQL wastes testing time.
- **Verify with MCP, not eyes** - wherever possible, verification should be agent-checkable (SQL query, Redis read, log search) rather than "visually confirm."
- **Order scenarios logically** - start with happy path, then edge cases, then error handling. Later scenarios can build on state from earlier ones.
- **Prefer a single-entry runbook** - if a historical runbook exists, create a current wrapper instead of forcing the local agent to read multiple old files.
- **Flag staging-only scenarios** - clearly mark scenarios that require real upstream integration (staging credentials, public tunnels, etc.).
- **Document stateful setup policy** - if local DB seeding or secret access is part of the intended setup, say so explicitly in the plan instead of leaving it implicit.
- **Don't over-test** - focus on scenarios that catch real bugs, not mechanical verification of every field. Prioritize money/safety-critical flows, idempotency, and state transitions.
- **Include log/trace verification** - for any backend flow, include a log/trace check so the user can see what happened inside the system.
- **Scenario tables must be fully executed or explicitly partial** - if a scenario contains a list/table of cases, tell the runner not to mark the scenario `Pass` unless every row ran or the missing rows are called out under `Partial`.

## Reference

- `AGENTS.md` - repository-wide constraints and project conventions
- `.agents/skills/create-plan/SKILL.md` - implementation plan format (input to this skill)
- `.agents/skills/run-test-plan/SKILL.md` - companion skill for executing the test plan locally
- `.agents/skills/load-context/SKILL.md` - context files are tracked in git; the local agent can `/load-context` for deeper feature understanding
- `.agents/skills/review-pr/SKILL.md` - branch-level code review (complementary to this runtime test plan)
