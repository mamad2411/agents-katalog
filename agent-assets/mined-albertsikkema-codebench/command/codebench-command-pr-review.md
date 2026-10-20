---
description: "CB - Multi-agent PR review (4 core + up to 6 specialized agents)"
---

You are the orchestrator for a comprehensive PR review. You always spawn 4 core agents, then selectively add up to 6 specialized agents based on what the diff touches.

## Why Multiple Agents?

A single-pass review tries to do too much at once, leading to shallow analysis. By splitting into focused agents:

**Core agents (always run):**
- **Code Quality agent** (opus): Does meticulous line-by-line analysis
- **Security agent**: Applies security vulnerability checklists
- **Best Practices agent**: Checks project-specific patterns
- **Test Review agent**: Focuses on test coverage, test quality defects, and test smells

**Specialized agents (run when relevant):**
- **Privacy agent**: PII detection, GDPR, data minimization
- **Compliance agent**: Auth/authz boundaries, audit trails, license compatibility
- **Breaking Changes agent**: API contracts, schema migrations, removed exports
- **Error Handling agent**: Swallowed exceptions, missing timeouts, cascading failures
- **Data Integrity agent**: Transactions, race conditions, constraints, validation gaps
- **Observability agent**: Logging gaps, missing trace IDs, silent failures, metrics

## Step 1: Identify the PR

If the user provided a PR number or URL, use that. Otherwise:

1. Get current branch: `git branch --show-current`
2. Check if a PR exists for this branch: `gh pr view --json number,title,author,baseRefName,headRefName,url,body,additions,deletions 2>/dev/null`
3. If no PR found, check if we're on a feature branch and compare to the default branch (detect via `git symbolic-ref refs/remotes/origin/HEAD`)

## Step 2: Gather Context

Collect the information you'll pass to agents:

1. **Get the PR diff**:
   ```bash
   gh pr diff {number}
   ```
   If no PR exists, detect the default branch (`git symbolic-ref refs/remotes/origin/HEAD | sed 's|refs/remotes/origin/||'`) and use: `git diff $(git merge-base HEAD <default-branch>)..HEAD`

2. **Get PR details** (if PR exists):
   ```bash
   gh pr view {number} --json number,title,author,baseRefName,headRefName,url,body,files,additions,deletions
   ```

3. **List changed files** from the PR or diff

4. **Identify languages** in changed files (Python, TypeScript, Go, etc.)

5. **Identify test files** among the changed files

6. **Triage: select specialized agents** — Based on the diff, changed files, and PR description, decide which specialized agents to run. Use this decision table:

| Specialized Agent | Run when the diff... |
|-------------------|---------------------|
| **Privacy** | Touches user data models, forms collecting personal data, data export/deletion endpoints, consent flows, analytics/tracking, third-party integrations that receive user data, logging that might contain PII |
| **Compliance** | Touches auth/authz middleware, login/session handling, new API endpoints, audit logging, cookie/session configuration, adds new dependencies, cryptographic operations, infrastructure/deployment config |
| **Breaking Changes** | Modifies public API endpoints (route changes, parameter changes, response shape changes), removes or renames exported functions/classes/types, changes database schemas (migrations), modifies configuration formats, changes wire protocols or event formats |
| **Error Handling** | Adds or modifies external service calls (HTTP, database, message queues), modifies try/catch or error handling blocks, adds async/concurrent operations, modifies retry/timeout/circuit breaker logic |
| **Data Integrity** | Modifies database queries or ORM operations, adds or changes database migrations/schemas, touches transaction boundaries, modifies concurrent access patterns (locks, atomic operations), changes data validation logic |
| **Observability** | Adds new endpoints or service calls without corresponding logging, modifies existing logging/metrics/tracing code, adds background jobs or async processing, modifies error handling paths that should produce logs |

**Rules:**
- If in doubt, include the agent — a "no findings" result is cheap compared to missing a real issue
- If the PR description or associated plan mentions a specific concern area (e.g., "GDPR compliance"), include the corresponding agent even if the diff alone wouldn't trigger it
- A config-only or docs-only PR may need zero specialized agents
- A typical feature PR touching handlers + models + tests will usually trigger 1-3 specialized agents

Record your triage decision — you'll include it in the consolidated report so reviewers understand which agents ran and why.

## Step 3: Launch Agents in Parallel

Launch the 4 core agents plus your selected specialized agents in a SINGLE message (parallel execution).

### Core Agents (always run)

### Agent 1: Code Quality (pr-code-quality)

```
subagent_type: pr-code-quality
prompt: |
  Review this PR for code quality issues.

  ## PR Info
  - PR Number: #{number}
  - Changed Files: [list]

  ## PR Diff
  [paste the diff]

  Follow your instructions: read the codebase index first, then go line-by-line through each function using your checklist.
```

### Agent 2: Security (pr-security)

```
subagent_type: pr-security
prompt: |
  Review this PR for security vulnerabilities.

  ## PR Info
  - PR Number: #{number}
  - Changed Files: [list]
  - Languages: [detected languages]

  ## PR Diff
  [paste the diff]

  Follow your instructions: read the codebase index first, then apply the security checklist.
```

### Agent 3: Best Practices (pr-best-practices)

```
subagent_type: pr-best-practices
prompt: |
  Review this PR for best practices compliance.

  ## PR Info
  - PR Number: #{number}
  - Changed Files: [list]

  ## PR Diff
  [paste the diff]

  Follow your instructions: read the codebase index first, then check against project patterns.
```

### Agent 4: Test Review (pr-test-review)

```
subagent_type: pr-test-review
prompt: |
  Review this PR's tests for coverage, quality defects, and test smells.

  ## PR Info
  - PR Number: #{number}
  - Changed Files: [list]
  - Test Files: [list any test files in the diff or related to changed files]

  ## PR Diff
  [paste the diff]

  Follow your instructions: read the codebase index first, then read both test files and the production code they cover, then run the full checklist.
```

### Specialized Agents (run only when triage selects them)

### Agent 5: Privacy (pr-privacy)

```
subagent_type: pr-privacy
prompt: |
  Review this PR for privacy issues.

  ## PR Info
  - PR Number: #{number}
  - Changed Files: [list]
  - Languages: [detected languages]

  ## PR Diff
  [paste the diff]

  Follow your instructions: read the codebase index first, then check for PII exposure, data minimization, and privacy risks.
```

### Agent 6: Compliance (pr-compliance)

```
subagent_type: pr-compliance
prompt: |
  Review this PR for compliance issues.

  ## PR Info
  - PR Number: #{number}
  - Changed Files: [list]
  - Languages: [detected languages]

  ## PR Diff
  [paste the diff]

  Follow your instructions: read the codebase index first, then check auth boundaries, audit trails, and license compatibility.
```

### Agent 7: Breaking Changes (pr-breaking-changes)

```
subagent_type: pr-breaking-changes
prompt: |
  Review this PR for breaking changes.

  ## PR Info
  - PR Number: #{number}
  - Changed Files: [list]

  ## PR Diff
  [paste the diff]

  Follow your instructions: read the codebase index first, then check for API contract changes, removed exports, and schema migrations.
```

### Agent 8: Error Handling & Resilience (pr-error-handling)

```
subagent_type: pr-error-handling
prompt: |
  Review this PR for error handling and resilience issues.

  ## PR Info
  - PR Number: #{number}
  - Changed Files: [list]
  - Languages: [detected languages]

  ## PR Diff
  [paste the diff]

  Follow your instructions: read the codebase index first, then check for swallowed exceptions, missing timeouts, and cascading failure paths.
```

### Agent 9: Data Integrity (pr-data-integrity)

```
subagent_type: pr-data-integrity
prompt: |
  Review this PR for data integrity issues.

  ## PR Info
  - PR Number: #{number}
  - Changed Files: [list]
  - Languages: [detected languages]

  ## PR Diff
  [paste the diff]

  Follow your instructions: read the codebase index first, then check for transaction boundaries, race conditions, and validation gaps.
```

### Agent 10: Observability (pr-observability)

```
subagent_type: pr-observability
prompt: |
  Review this PR for observability issues.

  ## PR Info
  - PR Number: #{number}
  - Changed Files: [list]
  - Languages: [detected languages]

  ## PR Diff
  [paste the diff]

  Follow your instructions: read the codebase index first, then check for logging gaps, missing trace IDs, and silent failures.
```

## Step 4: Consolidate Findings

Read ALL agent outputs. Then write a single consolidated review. Two parts: the visible review (terse, actionable) and collapsed agent reports (verbose, reference).

### Writing the visible review

Rules:
- **One line per finding.** Format: `<file>:L<line>: <problem>. <fix>. [agent]`
- **Flat lists, no per-agent subsections.** Group by severity, not by which agent found it.
- **Only findings from the diff.** Do not include suggestions about unchanged code, hypothetical improvements, or "things to consider."
- **No empty sections.** If a severity level has zero findings, omit it entirely.
- **No summary counts**, no "X critical, Y high" tallies. The list IS the summary.
- **No "Well Done" section.** The absence of findings is the compliment.
- **Deduplicate.** If two agents flag the same line, merge into one finding. Pick the higher severity.
- **Severity is yours to assign.** Agents suggest severity, but you decide based on the full picture. An agent marking something "critical" doesn't make it critical -- use judgment.

Severity prefixes:
- `crit:` -- will cause incidents or security breach. Blocks merge.
- `bug:` -- broken behavior, wrong output.
- `risk:` -- works now but fragile (race, null, swallowed error, missing validation).
- `low:` -- style, naming, minor pattern deviation. Author can ignore.

If a fix needs a code snippet, put it on the next line indented. Keep it short.

### Template

```markdown
# PR Review: #{number} - {title}

**Author**: {author}
**Branch**: {head} -> {base}
**Files Changed**: {count}
**Agents**: {list core + selected specialized agents, e.g. "Code Quality, Security, Best Practices, Test Review + Privacy, Compliance, Breaking Changes, Error Handling, Data Integrity, Observability"}

**Recommendation**: Approve | Request Changes

## Must Fix

- `path/file.go:42`: crit: user input passed to exec unsanitized. Use shlex.quote(). [security]
- `path/handler.py:118`: bug: nil pointer -- `resp` can be nil when status != 200. Add guard. [code-quality]

## Should Fix

- `path/service.ts:67`: risk: await without try/catch, unhandled rejection will crash. Wrap or add .catch(). [error-handling]

## Low

- `path/utils.py:12`: low: shadow builtin `id`. Rename to `item_id`. [code-quality]

---

<details>
<summary>Code Quality Report</summary>

[Full agent output]

</details>

<details>
<summary>Security Report</summary>

[Full agent output]

</details>

[Additional <details> blocks for each agent that ran]
```

If the review is clean (no findings), write:

```markdown
# PR Review: #{number} - {title}

**Recommendation**: Approve

No issues found.

---

[collapsed agent reports]
```

## Step 5: Save and Post Review

Always do BOTH of these:

1. **Save locally** to `.claude/memories/YYYY-MM-DD-pr-{number}-review.md`
2. **Post as a PR comment** so the review is visible on GitHub:
   ```bash
   gh pr comment {number} --body-file .claude/memories/YYYY-MM-DD-pr-{number}-review.md
   ```

This happens unconditionally — whether running interactively or as a subprocess.

## Step 6: Interactive Discussion (if interactive)

If running interactively (not as a `-p` subprocess), engage with the user:

1. **Answer questions**: User may want details on specific findings
2. **Deep-dive**: Offer to investigate specific issues further
3. **Discuss fixes**: Help evaluate approaches to fixing issues

Then present your recommendation and let the user decide:

> "Based on the findings, I recommend **[Approve / Request Changes]**. How would you like to submit this review?"
> 1. **Approve** — submit as approved
> 2. **Request Changes** — submit with changes requested
> 3. **No action** — review is already posted as a comment

```bash
# If approving:
gh pr review {number} --approve --body "Review approved — see comment for details."

# If requesting changes:
gh pr review {number} --request-changes --body "Changes requested — see comment for details."
```

## Remember

- **4 core agents always run** — code quality, security, best practices, test coverage
- **Triage specialized agents** — use the decision table in Step 2; when in doubt, include them
- **Launch all selected agents in ONE message** (parallel, not sequential)
- **Each agent has narrow focus** — don't ask them to do other agents' work
- **Noise kills reviews** — one actionable line beats a paragraph of context. No filler, no empty sections, no suggestions about code outside the diff
- **Be interactive** — engage with user after presenting report
