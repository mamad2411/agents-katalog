<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: autonomous-ops
description: >
  24/7 autonomous operation loop combining OMC multi-agent orchestration with
  OpenClaw-CC's messenger and scheduler. Triggers on "자율 모드", "autonomous",
  "24/7 모드", "자동 운영", "autonomous mode", "self-driving", "unattended"
  and similar requests. Polls messenger for user requests, analyzes tasks,
  dispatches OMC teams for execution, persists results to memory, and reports
  back via messenger. The crown jewel of OMC × OpenClaw-CC integration.
---

# Autonomous Operations — 24/7 Self-Driving AI Agent Loop

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

## Role

Operate autonomously as a 24/7 AI agent. Poll for user requests via
Discord/Telegram, analyze and execute them using OMC multi-agent teams,
persist all results to permanent memory, and report back. Schedule recurring
polls to maintain continuous operation.

## Prerequisites

- messenger-bot MCP connected (Discord or Telegram tokens configured)
- task-scheduler MCP available
- daemon.sh or systemd service running for cron execution

## Autonomous Loop

### Step 1 — Poll for Requests

```
messenger_poll(platform: "all") → Check for new user messages
messenger_read(platform: "all", limit: 5) → Read recent if poll empty
```

Parse user messages for actionable requests:
- Commands: "해줘", "만들어", "찾아", "분석해", "리뷰해" (do it, create, find, analyze, review)
- Questions: "뭐야?", "어떻게?", "왜?" (what is it, how, why)
- Ignore: greetings, acknowledgments, emoji-only

### Step 2 — Context Loading

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

```
memory_search(associative: true, context: {
  tags: ["{extracted_topic}"],
  date: "{today}"
}) → Load relevant past context
```

### Step 3 — Task Analysis & Decomposition

Invoke `/task-analyzer` internally:
1. Classify request type (code, research, memory, scheduling, general)
2. Estimate complexity (simple: 1 agent, complex: team pipeline)
3. Select execution strategy

### Step 4 — OMC Team Dispatch

**Simple tasks (1-2 subtasks):**
```
Agent(subagent_type: "oh-my-claudecode:executor", prompt: "{task}")
```

**Complex tasks (3+ subtasks):**
```
TeamCreate(name: "auto-{timestamp}", members: ["executor", "verifier"])
SendMessage(to: "executor", prompt: "{decomposed_subtasks}")
SendMessage(to: "verifier", prompt: "verify results of {task}")
```

**Research tasks:**
```
Agent(subagent_type: "research-agent", prompt: "{research_query}")
```

### Step 5 — Result Collection & Persistence

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

```
memory_store(
  category: "{appropriate}",
  title: "Auto: {task_summary}",
  tags: ["autonomous", "{topic}"],
  importance: 5,
  content: "{results}"
)
memory_daily_log(type: "done", entry: "Autonomous: {one-line}")
```

### Step 6 — Report Back

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

```
messenger_send(platform: "{original_platform}", message: "
  ✅ **Task Complete**: {task_summary}
  📋 Results: {brief_results}
  💾 Memory: #{memory_id}
  ⏱ Duration: {duration}

  Full details: memory_get(id: {memory_id})
")
```

### Step 7 — Schedule Next Poll

```
task_create(
  name: "auto-poll-{timestamp}",
  prompt: "Run autonomous-ops: poll messenger and execute pending requests",
  cron: "*/15 * * * *",
  allowedTools: ["messenger_poll", "messenger_read", "messenger_send",
    "memory_search", "memory_store", "memory_daily_log", "task_list"],
  tags: ["autonomous", "polling"],
  enabled: true
)
```

## Error Handling

| Situation | Action |
|-----------|--------|
| No new messages | Log idle, skip execution, wait for next poll |
| Task fails | Retry once with different strategy; report failure to user |
| Messenger offline | Log to memory, retry notification on next poll |
| Ambiguous request | Send clarification question via messenger |
| Rate limit | Back off 5 minutes, log warning |

## Safety Rules

1. **Never execute destructive operations** (delete, force-push, drop) without explicit user confirmation via messenger
2. **Bound execution time** — single task max 10 minutes; total loop max 30 minutes
3. **Cost guard** — max 5 team creations per poll cycle
4. **Audit trail** — every action logged to `memory_daily_log`
5. **Kill switch** — user sends "중지" (stop), "stop", "cancel" → disable auto-poll cron task

## Completion Codes

| Code | Meaning |
|------|---------|
| DONE | All pending requests processed and reported |
| IDLE | No pending requests found |
| BLOCKED | Request requires user confirmation |
| ERROR | Execution failed after retry |

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
