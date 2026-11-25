<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: knowledge-refiner
description: >
  Memory refinement with OMC team pipeline. Triggers on "메모리 정리", "지식 정리",
  "중복 제거", "refine", "메모리 최적화", "memory cleanup", "deduplicate",
  "optimize memories", "consolidate" and similar. v3: Uses OMC analyst agent for
  detection, executor for merge execution, verifier for confirmation. Reports
  via messenger. Runs as nightly cron task automatically.
---

# Knowledge Refiner — Memory Optimization & Refinement Skill

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

Analyze, optimize, and maintain the memory store health. Detect duplicates,
merge similar memories, promote important ones, archive stale content, and
apply importance decay. Produces a clear report of all changes made.

## Workflow

### Step 1 — Status Assessment

```
memory_stats → Get current memory store overview
```

Report: total count, category breakdown, average importance, recent activity.

### Step 2 — Duplicate Detection

```
memory_similar(threshold: 0.5, limit: 10) → Find similar memory clusters
```

For each cluster found:
- Show the memories and their similarity scores
- Ask user: "These N memories overlap. Merge into the primary?"

### Step 3 — Merge Execution (on approval)

```
memory_refine(id: primary_id, mode: "consolidate") → Get merge candidates
memory_update(id: primary_id, mode: "append", content: merged_content)
memory_link(source_id: primary_id, target_id: secondary_id, relation: "supersedes")
memory_delete(id: secondary_id) → Remove merged duplicates
```

### Step 4 — Archive Preview

```
memory_archive(older_than: 30, dry_run: true) → Preview stale candidates
```

Show: list of candidates with age, importance, category.
Ask user: "Archive these M stale memories?"

### Step 5 — Archive Execution (on approval)

```
memory_archive(older_than: 30) → Execute archival
```

### Step 6 — Layer Upgrades

```
memory_refine(id: X, mode: "upgrade") → Promote eligible memories
```

Criteria:
- episodic → working: access_count > 5 AND age > 7 days
- working → longterm: importance >= 7 OR access_count > 10

### Step 7 — Trigram Reindex

```
memory_reindex_trigrams → Rebuild similarity index after changes
```

### Step 8 — Final Report

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

```markdown
## Memory Refinement Report

**Before**: X total memories
**After**: Y total memories

### Actions Taken
- Merged: N clusters (M memories consolidated)
- Archived: K memories (older than 30 days, importance < 7)
- Upgraded: J memories (layer promotions)
- Reindexed: trigram index rebuilt

### Memory Health
- Duplicate ratio: X% → Y%
- Average importance: A → B
- Layer distribution: episodic/working/longterm
```

## Safety Rules

1. **Never auto-delete** — Always show candidates and get user approval
2. **Preserve versions** — All mutations save previous version to memory_versions
3. **Link before delete** — Create `supersedes` links before removing merged content
4. **Dry run first** — Archive always previews before executing
5. **Reindex after bulk changes** — Always rebuild trigram index after merges

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
