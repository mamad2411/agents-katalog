<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: deep-research
description: >
  Multi-agent deep research with parallel execution and knowledge graph
  integration. Triggers on "심층 조사", "deep research", "thorough investigation",
  "comprehensive analysis", "깊이 파봐", "detailed study", "in-depth research"
  and similar requests. Spawns multiple research agents in parallel, synthesizes
  via analyst, deduplicates against existing knowledge, builds graph connections,
  and delivers a comprehensive report.
---

# Deep Research — Multi-Agent Parallel Research with Knowledge Graph

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

Perform comprehensive research using multiple OMC agents in parallel.
Unlike basic web research, deep research cross-references multiple sources,
deduplicates against existing knowledge, builds knowledge graph connections,
and produces analyst-grade reports.

## Workflow

### Phase 1 — Existing Knowledge Assessment

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
  tags: ["{topic}", "research"],
  date: "{today}"
})
memory_graph(id: related_memory_id, depth: 2) → Map existing knowledge
```

Produce a **knowledge gap analysis**: what is known vs what needs research.

### Phase 2 — Parallel Agent Dispatch

Spawn 3 research agents with different angles:

```
Agent(name: "researcher-1", subagent_type: "research-agent",
  prompt: "Research '{topic}': focus on OVERVIEW and landscape.
    Search in both Korean and English.
    Return structured findings with source URLs.",
  run_in_background: true)

Agent(name: "researcher-2", subagent_type: "research-agent",
  prompt: "Research '{topic}': focus on RECENT DEVELOPMENTS (last 6 months).
    Find news, announcements, and technical updates.
    Return structured findings with dates and sources.",
  run_in_background: true)

Agent(name: "researcher-3", subagent_type: "research-agent",
  prompt: "Research '{topic}': focus on TECHNICAL DEPTH and implementation.
    Find documentation, code examples, architecture details.
    Return structured findings with code snippets if available.",
  run_in_background: true)
```

### Phase 3 — Synthesis via OMC Analyst

```
Agent(subagent_type: "oh-my-claudecode:analyst", model: "opus",
  prompt: "
    Synthesize these 3 research reports into a unified analysis:

    Report 1 (Overview): {researcher_1_output}
    Report 2 (Recent): {researcher_2_output}
    Report 3 (Technical): {researcher_3_output}

    Produce:
    1. Key findings (ranked by importance)
    2. Trend analysis
    3. Technical assessment
    4. Gaps and uncertainties
    5. Recommendations
  ")
```

### Phase 4 — Deduplication & Knowledge Graph

```
# Check each finding against existing knowledge
For each key finding:
  memory_similar(text: "{finding}") → Check duplicates

  If similarity > 0.7:
    memory_update(id: existing, mode: "append", content: "Updated: {new_info}")
  Else:
    new_id = memory_store(
      category: "knowledge",
      subcategory: "{domain}",
      title: "Research: {finding_title}",
      tags: ["research", "deep-research", "{topic}"],
      importance: 6
    )

# Build knowledge graph connections
memory_link(source: new_id, target: existing_id, relation: "related")
memory_link(source: new_id, target: overview_id, relation: "derived")
```

### Phase 5 — Quality Review via OMC Critic

```
Agent(subagent_type: "oh-my-claudecode:critic", model: "opus",
  prompt: "
    Review this research report for completeness and accuracy:
    {synthesized_report}

    Check for:
    1. Unsupported claims (no source)
    2. Logical gaps
    3. Missing perspectives
    4. Outdated information
    5. Contradictions between sources

    Provide a quality score (1-10) and specific improvement suggestions.
  ")
```

### Phase 6 — Final Report & Delivery

```markdown
## Deep Research Report: {Topic}

**Quality Score**: {critic_score}/10
**Sources Consulted**: {N} across {M} domains
**Knowledge Graph**: {K} new nodes, {J} new connections

### Executive Summary
{one_paragraph_overview}

### Key Findings
1. {Finding} — Source: {url} — Confidence: High/Medium/Low
2. {Finding} — Source: {url} — Confidence: High/Medium/Low
3. ...

### Trend Analysis
{trends_and_direction}

### Technical Assessment
{technical_details_with_code_examples}

### Data Points
| Metric | Value | Source | Date |
|--------|-------|--------|------|

### Source Credibility Matrix
| Source | Type | Credibility | Recency |
|--------|------|-------------|---------|

### Gaps & Uncertainties
- {unverified_claims}
- {missing_perspectives}

### Recommendations
1. {actionable_recommendation}
2. {actionable_recommendation}

### Knowledge Graph Impact
- New memories created: {list_with_ids}
- Connected to existing: {list_of_links}
- Stored as: memory #{primary_id}
```

### Delivery

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
memory_store(category: "knowledge", title: "Deep Research: {topic}",
  importance: 7, tags: ["deep-research", "{topic}"])
memory_daily_log(type: "done", entry: "Deep research completed: {topic}")
```

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
messenger_send(platform: "telegram",
  message: "📊 Deep research complete: {topic}\nScore: {score}/10\nFindings: {count}\nMemory: #{id}")
```

## Principles

1. **Parallel-first** — Always run 3 researchers in parallel for speed
2. **Multi-angle** — Overview + Recent + Technical = comprehensive coverage
3. **Dedup-before-store** — Every finding checked against existing knowledge
4. **Graph-connected** — All new knowledge linked to existing via `memory_link`
5. **Quality-gated** — Critic review before final delivery
6. **Bilingual** — Korean and English sources for Korean-context topics
7. **Attribution** — Every claim traced to its source URL

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
