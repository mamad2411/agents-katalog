<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: investigate
description: >
  Systematic debugging with root cause investigation. Six stages: investigate,
  reproduce, analyze, hypothesize, implement, verify. Iron Law: no fixes without
  root cause. Triggers on "디버깅", "버그 찾아", "investigate", "왜 안 돼",
  "debug", "find the bug", "root cause", "에러 분석".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - WebSearch
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/../freeze/bin/check-freeze.sh"
          statusMessage: "Checking debug scope boundary..."
    - matcher: "Write"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/../freeze/bin/check-freeze.sh"
          statusMessage: "Checking debug scope boundary..."
---

# Investigate — Systematic Debugging

## Iron Law

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Fixing symptoms creates whack-a-mole debugging. Find the root cause, then fix it.

## Preamble

Before executing this skill:

1. **Load context from memory**:
   ```
   memory_search(query: "{skill-relevant-query}", associative: true, limit: 5)
   memory_search(tag: "{skill-name}", limit: 3)
   ```
   Review returned memories for relevant past context, decisions, and patterns.

2. **Check OMC state for active work**:
   ```
   state_get_status()
   ```
   If conflicting active tasks exist, warn the user before proceeding.

3. **Detect current branch** (for git-related skills):
   ```bash
   git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "not-a-git-repo"
   ```

4. **Check proactive mode**:
   ```
   state_read("occ-proactive")
   ```
   If `"false"`: do NOT proactively suggest other OpenClaw-CC skills during this session.
   Only run skills the user explicitly invokes.

5. **Log skill activation**:
   ```
   memory_daily_log(type: "note", entry: "Skill activated: /{skill-name}")
   ```

## Memory Context Loading

Before starting work, load relevant context from the 3-layer memory system:

```
# Search for related past work
memory_search(query: "{task description}", associative: true, limit: 5)

# Search by relevant tags
memory_search(tag: "{relevant-tag}", limit: 3)

# Check for recent related daily logs
memory_search_date(start: "{7 days ago}", end: "{today}", category: "daily-logs", limit: 5)
```

**Use retrieved context to**:
- Avoid repeating past mistakes
- Build on previous decisions
- Maintain consistency with established patterns
- Reference related knowledge graph nodes

If critical related memories exist, summarize them before proceeding:
```
Found {N} related memories:
- {memory_1 title}: {brief relevance}
- {memory_2 title}: {brief relevance}
```

Check memory for related past bugs:
```
memory_search(query: "{error description}", tag: "bug")
memory_search(query: "{affected component}", tag: "debugging")
```

---

## Stage 1 — Root Cause Investigation via OMC `tracer`

Delegate evidence gathering:

```
Agent(subagent_type: "oh-my-claudecode:tracer", prompt: "
  Investigate: {symptom_description}
  Gather evidence, trace code paths, form competing hypotheses.
  Do NOT fix anything. Output structured hypothesis report.
")
```

**Use OMC code intelligence for precise tracing:**
- `lsp_goto_definition` — trace symbols to their source definitions
- `lsp_find_references` — find all callers/usages of a function
- `lsp_hover` — get type information and documentation
- `lsp_diagnostics` — check for compiler/linter errors in affected files
- `ast_grep_search` — find structural code patterns across the codebase

1. **Collect symptoms**: Error messages, stack traces, reproduction steps.
   If insufficient context, ask ONE question via AskUserQuestion.
2. **Read the code**: Trace from symptom back to potential causes.
3. **Check recent changes**: `git log --oneline -20 -- <affected-files>`
4. **Reproduce**: Can you trigger the bug deterministically?

Output: **"Root cause hypothesis: ..."** — specific, testable claim.

---

## Stage 1.5 — Reproduction (NEW)

**Before forming hypotheses, reproduce the bug:**

1. Write a minimal reproduction (test case, script, or command)
2. Run it and confirm the failure
3. If cannot reproduce → gather more evidence, do NOT proceed to fix

If reproduction succeeds, it becomes the regression test after the fix.

---

## Stage 2 — Scope Lock

After forming root cause hypothesis, lock edits to the affected module:

```bash
FREEZE_CHECK="${CLAUDE_SKILL_DIR}/../freeze/bin/check-freeze.sh"
if [ -x "$FREEZE_CHECK" ]; then
  STATE_DIR="${CLAUDE_PLUGIN_DATA:-${HOME}/.omc/state}"
  mkdir -p "$STATE_DIR"
  echo "<detected-directory>/" > "$STATE_DIR/freeze-dir.txt"
  echo "Debug scope locked to: <detected-directory>/"
fi
```

Tell user: "Edits restricted to `<dir>/` for this debug session. This prevents changes to unrelated code. Run `/unfreeze` to remove."

If bug spans entire repo or scope is unclear, skip lock and note why.

---

## Stage 3 — Pattern Analysis

Check if bug matches known patterns:

| Pattern | Signature | Where to look |
|---------|-----------|---------------|
| Race condition | Intermittent, timing-dependent | Concurrent access to shared state |
| Nil/null propagation | NoMethodError, TypeError | Missing guards on optional values |
| State corruption | Inconsistent data, partial updates | Transactions, callbacks, hooks |
| Integration failure | Timeout, unexpected response | External API calls, service boundaries |
| Configuration drift | Works locally, fails elsewhere | Env vars, feature flags, DB state |
| Stale cache | Shows old data, fixes on clear | Redis, CDN, browser cache |

**External search** (sanitize first — strip hostnames, IPs, paths, customer data):
- WebSearch: "{framework} {generic error type}"
- If unavailable, proceed with in-distribution knowledge

---

## Stage 4 — Hypothesis Testing

Before writing ANY fix, verify your hypothesis:

1. Add temporary log/assertion at suspected root cause. Run reproduction. Does evidence match?
2. If hypothesis is wrong → return to Stage 1 with new data. Do NOT guess.
3. **3-strike rule**: If 3 hypotheses fail, **STOP**. AskUserQuestion:
   ```
   3 hypotheses tested, none match. This may be an architectural issue rather than a simple bug.

   A) Continue investigating — new hypothesis: [describe]
   B) Escalate for human review — someone who knows the system
   C) Add logging and wait — instrument the area and catch it next time
   ```

**Red flags** — slow down if you see:
- "Quick fix for now" — there is no "for now." Fix it right or escalate.
- Proposing a fix before tracing data flow — you're guessing.
- Each fix reveals a new problem — wrong layer, not wrong code.

Log each hypothesis test result:
```
memory_store(category: "knowledge", subcategory: "debugging",
  title: "Investigation: {bug} - Hypothesis {N}",
  content: "{hypothesis, test method, result, verdict}",
  tags: ["investigation", "{component}"], importance: 5)
```

---

## Stage 5 — Implementation via OMC `executor` (ONLY after root cause confirmed)

```
Agent(subagent_type: "oh-my-claudecode:executor", model: "opus", prompt: "
  Root cause confirmed: {root_cause}
  Implement fix: {description}
  Files: {file_list}
  Constraints: minimal diff, fix root cause not symptom
")
```

Safety limits:
- 5+ files → AskUserQuestion about blast radius
- 3 failed fix attempts → escalate

---

## Stage 6 — Verification via OMC `verifier`

```
Agent(subagent_type: "oh-my-claudecode:verifier", prompt: "
  Verify fix for: {bug_description}
  Root cause: {root_cause}
  Fix: {fix_description}
  1. Confirm original symptom no longer reproduces
  2. Run test suite
  3. Check for regressions in related areas
")
```

Output structured debug report:
```
═══════════════════════════════════════
DEBUG REPORT
═══════════════════════════════════════
Symptom:         {what the user observed}
Root cause:      {what was actually wrong}
Fix:             {what was changed, with file:line references}
Evidence:        {test output, reproduction showing fix works}
Regression test: {file:line of the new test}
Related:         {past bugs in same area, architectural notes}
Status:          DONE | DONE_WITH_CONCERNS | BLOCKED
═══════════════════════════════════════
```

## Memory Persistence

After completing the workflow, persist results to the 3-layer memory system:

### Required Actions

1. **Log completion to daily log**:
   ```
   memory_daily_log(type: "done", entry: "{skill-name}: {brief result summary}")
   ```

2. **Store significant findings** (importance ≥ 6):
   ```
   memory_store(
     category: "{appropriate category}",
     title: "{descriptive title}",
     content: "{structured result content}",
     tags: ["{skill-name}", "{project}", "{relevant-tags}"],
     importance: {6-10 based on significance}
   )
   ```

3. **Link to related memories** (if applicable):
   ```
   memory_link(source: "{new_memory_id}", target: "{related_id}", relation: "{related|derived|refines}")
   ```

### Category Routing

| Content Type | Category | Subcategory |
|-------------|----------|-------------|
| Bug fix / debugging | knowledge | debugging |
| Code review results | projects | {project-name} |
| Design decisions | projects | {project-name} |
| Research findings | knowledge | {topic} |
| Release / deploy | projects | {project-name} |
| Person-related info | people | — |
| Task / action item | tasks | — |

## Messenger Notification

Send notifications for significant events via messenger:

### When to Notify

| Event | Platform | Priority |
|-------|----------|----------|
| Task/pipeline completed | telegram | Normal |
| Verification failed | telegram | High |
| Long-running task done (10+ min) | telegram | Normal |
| Critical error or blocker | telegram | High |
| PR created / release shipped | all | Normal |
| Importance ≥ 8 memory created | telegram | Normal |

### Notification Format

```
messenger_send(
  platform: "telegram",
  message: "[{skill-name}] {status_emoji} {brief description}\n\n{details if relevant}"
)
```

**Status Emojis**:
- Completed successfully: ✅
- Completed with warnings: ⚠️
- Failed / blocked: ❌
- Needs attention: 🔔

### Do NOT Notify

- Routine memory operations
- Intermediate progress steps
- Read-only operations (search, list, status)

## Completion Status Protocol

Every skill must end with one of these status codes:

| Code | Meaning | When to Use |
|------|---------|-------------|
| **DONE** | All steps completed, evidence provided | Root cause found + fix verified, PR created, review finished |
| **DONE_WITH_CONCERNS** | Completed with warnings or caveats | Tests pass but coverage dropped, fix applied but can't fully verify |
| **BLOCKED** | Cannot proceed, requires user intervention | 3 failed attempts, missing permissions, external dependency down |
| **NEEDS_CONTEXT** | Missing information to continue | Unclear requirements, need user clarification |

### Escalation Rules

1. **3-strike rule**: After 3 failed attempts at any step, **STOP** and escalate to user.
   Do not continue guessing. Present what was tried and ask for direction.

2. **Scope escalation**: If fix/change touches 5+ files unexpectedly, pause and confirm
   with the user before proceeding.

3. **Security uncertainty**: If you are unsure about a security implication, **STOP** and
   escalate. Never guess on security.

4. **Verification requirement**: Never claim DONE without evidence.
   - "Should work" → RUN IT. Confidence is not evidence.
   - "Already tested earlier" → Code changed since. Test again.
   - "Trivial change" → Trivial changes break production.

### Output Format

```
═══════════════════════════════════════
Status: {DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT}
Summary: {one-line description of outcome}
Evidence: {test output, verification results, or blocking reason}
═══════════════════════════════════════
```
