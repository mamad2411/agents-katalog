<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: knowledge-sync
description: >
  Bidirectional synchronization between OMC's project-memory and OpenClaw-CC's
  persistent memory store. Triggers on "지식 동기화", "sync memory", "knowledge sync",
  "메모리 동기화", "OMC 동기화", "synchronize", "sync state" and similar requests.
  Ensures knowledge is shared across both systems — OMC's ephemeral state becomes
  persistent, and OpenClaw-CC's long-term knowledge becomes available to OMC agents.
---

# Knowledge Sync — OMC ↔ OpenClaw-CC Memory Synchronization

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

Synchronize knowledge between oh-my-claudecode's project-memory (ephemeral, `.omc/`)
and OpenClaw-CC's persistent memory store (SQLite + Markdown files). This ensures
that insights captured by OMC agents survive sessions, and long-term knowledge from
OpenClaw-CC is available to OMC's planning and execution.

## Sync Directions

```
OMC project-memory  ──→  OpenClaw-CC memory_store    (Persist)
OpenClaw-CC memory  ──→  OMC notepad_write_priority  (Inject)
```

## Workflow

### Step 1 — Read OMC State

```
project_memory_read → Full OMC project memory
notepad_read → Current OMC notepad (priority + working)
state_list_active → Active OMC states
```

### Step 2 — Read OpenClaw-CC State

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
memory_search(limit: 20) → Recent memories
memory_stats → Overall health
memory_search(category: "projects") → Project-specific knowledge
```

### Step 3 — Diff Analysis

Compare both datasets to find:

| Gap Type | Detection | Action |
|----------|-----------|--------|
| OMC-only entries | In project-memory but not in memory_search | Persist to OpenClaw-CC |
| CC-only entries | In memory_search but not in project-memory | Inject to OMC notepad |
| Stale OMC state | OMC state older than CC memory | Update OMC from CC |
| Conflicts | Same topic, different content | Flag for manual review |

### Step 4 — OMC → OpenClaw-CC (Persist)

For each OMC-only entry:
```
memory_similar(text: "{omc_entry}") → Check for near-duplicates
If no duplicate (similarity < 0.5):
  memory_store(
    category: "projects",
    title: "{omc_entry_title}",
    content: "{omc_entry_content}",
    tags: ["synced-from-omc", "{project}"],
    importance: 5,
    source: "system"
  )
If duplicate found:
  memory_update(id: existing_id, mode: "append",
    content: "\n\n---\n**OMC Sync**: {new_info}")
```

### Step 5 — OpenClaw-CC → OMC (Inject)

For critical CC knowledge not in OMC:
```
notepad_write_priority(content: "
  ## Synced from Memory Store
  {key_findings_summary}
  Memory IDs: {id_list}
  Use memory_get(id) for full details.
")

project_memory_add_note(note: "{critical_knowledge_summary}")
```

### Step 6 — Report

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

```markdown
## Knowledge Sync Report

**Direction**: Bidirectional
**Timestamp**: {datetime}

### OMC → OpenClaw-CC (Persisted)
- {N} new entries stored
- {M} existing entries updated
- Categories: {list}

### OpenClaw-CC → OMC (Injected)
- {K} entries injected to notepad
- {J} entries added to project-memory

### Conflicts (Manual Review)
- {conflict_list or "None"}

### Memory Health
- Total memories: {count}
- Sync coverage: {percentage}%
```

## Automation

Register as periodic task:
```
task_create(
  name: "knowledge-sync",
  cron: "0 */6 * * *",
  prompt: "Run knowledge-sync: synchronize OMC and OpenClaw-CC memory",
  tags: ["sync", "maintenance"]
)
```

## Principles

1. **Dedup before store** — Always check `memory_similar` before creating
2. **Tag synced entries** — Use `synced-from-omc` tag for traceability
3. **Don't overwrite** — Append, don't replace, when updating existing entries
4. **Lightweight injection** — Only inject summaries to OMC (use memory IDs for details)
5. **Conflict resolution** — Flag conflicts, don't auto-resolve

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
