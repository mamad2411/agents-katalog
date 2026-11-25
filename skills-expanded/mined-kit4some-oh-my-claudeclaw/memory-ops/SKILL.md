<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: memory-ops
description: >
  Unified memory interface with associative search and OMC integration.
  Triggers on "기억해", "저장해", "메모리", "뭐였지", "지난번에", "기록해", "잊지마",
  "정리해", "요약해줘", "remember", "save", "store", "what was it", "last time",
  "record this", "don't forget", "organize", "summarize" and similar.
  v3: Default to associative search mode (5-signal ranking). Uses memory-specialist
  agent for complex operations. Auto-indexes trigrams via PostToolUse hook.
---

# Memory Operations — Persistent Memory Management Skill

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

## Core Principles

1. **Store all important information**: Decisions, insights, and plans from conversations go into memory
2. **Store with structure**: Assign appropriate category, tags, and importance level
3. **Retrieve when needed**: Run `memory_search` first whenever related context is required
4. **Periodically organize**: Clean up old/duplicate memories and consolidate summaries

## Category Guide

| Category | Purpose | Subcategory Examples |
|----------|---------|----------------------|
| `projects` | Everything project-related | rutile, sapiens, nexus |
| `people` | Person info, relationships, meeting notes | ken-huang, investors |
| `knowledge` | Learned knowledge, technical docs | web3-security, ai-agents |
| `tasks` | To-dos, work in progress | urgent, backlog |
| `daily-logs` | Daily activity logs | (date auto-generated) |
| `inbox` | Unsorted temporary storage | (classify later) |

## Auto-Save Triggers

When the following patterns appear in conversation, **automatically suggest** saving to memory:

- **Decision**: "we decided to ~", "going with ~", "direction is ~"
- **Plan/Strategy**: "planning to ~ going forward", "the plan is ~"
- **Person info**: New name + role/relationship
- **Insight**: "realized that", "the key thing is", "most important is"
- **Data/Metrics**: Revenue, deadlines, prices, or other specific figures
- **Risk/Issue**: Problems, risks, cautions

## Store Workflows

### 1. Quick Store
```
User: "Remember this — Ken Huang is co-chair of CSA and we're meeting in SF on 3/25"

→ memory_store:
  category: "people"
  subcategory: null
  title: "Ken Huang - CSA Co-Chair"
  content: "Ken Huang is co-chair of the Cloud Security Alliance. Meeting in SF on 3/25."
  tags: ["ken-huang", "csa", "sf-trip", "meeting"]
  importance: 7
```

### 2. Project Context Store
```
User: "We decided to migrate Sapiens to PydanticAI"

→ memory_store:
  category: "projects"
  subcategory: "sapiens"
  title: "Framework Migration Decision - PydanticAI"
  content: "Decision to migrate from LangGraph to PydanticAI. Reason: ..."
  tags: ["sapiens", "migration", "pydanticai", "decision"]
  importance: 8
```

### 3. Knowledge Store
```
User: "Save this vulnerability pattern"

→ memory_store:
  category: "knowledge"
  subcategory: "web3-security"
  title: "Reentrancy Attack Pattern - Cross-function"
  content: [detailed content]
  tags: ["vulnerability", "reentrancy", "solidity"]
  importance: 6
```

## Search Workflows

### Proactive Context Search
**Proactively search** relevant memories before starting a task:

```
User: "Tell me the status of RSA Conference prep"

→ 1. memory_search(query: "RSA Conference")
→ 2. memory_search(tag: "rsa")
→ 3. memory_search(category: "projects", query: "rutile conference")
→ 4. Synthesize results and respond
```

### Time-Based Lookup
```
User: "What did I do last week?"

→ memory_search(category: "daily-logs")
→ Summarize logs from the past 7 days
```

## Memory Organization Workflows

### Inbox Classification
```
memory_list(directory: "inbox")
→ Determine appropriate category for each item
→ Move via memory_update (or file move + re-index)
```

### Duplicate Consolidation
```
Discover similar items with memory_search
→ Merge content
→ Delete old entries
```

### Project Summary Refresh
```
memory_search(category: "projects", subcategory: "rutile")
→ Consolidate recent changes
→ Update _meta.md summary file
```

## Daily Log Pattern

Record daily logs automatically or on user request:

```
memory_daily_log:
  entry: "AhnLab PoC meeting completed, received additional feature requests"
  type: "meeting"
```

Entry types: note, decision, todo, done, idea, meeting

## Memory Tree Navigation

When user requests "show me the memory structure":
```
memory_list(directory: "", max_depth: 2)
→ Visualize and display the full tree structure
```

## Importance Guide

| Score | Criteria | Examples |
|-------|----------|---------|
| 9-10 | Business critical, legal obligation | Investment contract terms, incorporation decision |
| 7-8 | Core decisions, key relationships | Technical architecture decision, key partner info |
| 5-6 | Useful reference information | Technical notes, meeting summaries |
| 3-4 | General records | Daily logs, idea memos |
| 1-2 | Temporary/one-off | Quick notes, information that will soon be obsolete |

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
