<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: web-researcher
description: >
  Web research with OMC team parallel execution. Triggers on "웹에서 찾아",
  "최신 정보", "리서치해", "동향", "web research", "find online", "latest info",
  "look up", "search the web", "trend analysis" and similar. v3: Spawns
  research-agent in parallel for multi-angle search. Deduplicates via
  memory_similar. Builds knowledge graph connections. For comprehensive
  research use /deep-research instead.
---

# Web Researcher — Automated Web Research & Knowledge Integration

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

Perform systematic web research using multiple queries and angles. Collect,
verify, structure, and persist findings in memory. Link new knowledge to
existing related memories for a connected knowledge graph.

## Workflow

### Step 1 — Check Existing Knowledge

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
memory_search(query: "{research topic}")
memory_search(tag: "{topic tag}")
```

Identify what is already known to avoid redundant research.

### Step 2 — Multi-Query Search Strategy

Generate at least 3 search queries from different angles:

```
web_search("{topic} overview 2026")              → General landscape
web_search("{topic} latest developments")          → Recent news
web_search("{topic} {specific_aspect}")            → Targeted depth
```

For bilingual topics (Korean context):
```
web_search("{Korean query}")                       → Korean sources
web_search("{English query}")                      → English sources
```

### Step 3 — Content Collection

Fetch top 3-5 URLs from search results:

```
web_fetch(url_1) → Extract key information
web_fetch(url_2) → Extract key information
web_fetch(url_3) → Extract key information
```

For each source, extract:
- Key facts and data points
- Dates and recency
- Source credibility assessment
- Relevant quotes or statistics

### Step 4 — Synthesis & Structuring

Organize findings into a structured report:

```markdown
## Research: {Topic}

### Key Findings
1. {Finding with source attribution}
2. {Finding with source attribution}
3. {Finding with source attribution}

### Data Points
| Metric | Value | Source | Date |
|--------|-------|--------|------|
| {metric} | {value} | {source} | {date} |

### Source Assessment
| Source | Credibility | Recency | Notes |
|--------|------------|---------|-------|
| {url} | High/Medium/Low | {date} | {notes} |

### Analysis
{Synthesized analysis combining multiple sources}

### Gaps & Uncertainties
- {What couldn't be confirmed}
- {Conflicting information found}
```

### Step 5 — Memory Persistence

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
memory_store:
  category: "knowledge"
  subcategory: "{topic-area}"
  title: "Research: {Topic} ({date})"
  content: {structured report}
  tags: ["research", "{topic}", "{subtopic}"]
  importance: 6
  summary: "{one-line key finding}"
```

### Step 6 — Knowledge Graph Integration

Link new findings to existing related memories:

```
memory_search(query: "{related topic}") → Find related memories
memory_link(source_id: new_id, target_id: related_id, relation: "related")
```

### Step 7 — Report Delivery

```markdown
## Research Complete: {Topic}

**Sources consulted**: {N} web pages across {M} domains
**Key finding**: {one-line summary}
**Stored as**: memory #{id}
**Linked to**: {N} related existing memories

{Full structured report}
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
  message: "Research complete: {topic}. Key finding: {summary}")
```

## Research Principles

1. **Multiple sources** — Never rely on a single source. Cross-reference
2. **Recency matters** — Prefer sources from the last 6 months
3. **Source attribution** — Always cite where information came from
4. **Acknowledge uncertainty** — Flag conflicting or unverifiable claims
5. **Build on existing** — Check memory first, add incrementally
6. **Bilingual coverage** — For Korean-context topics, search both Korean and English
