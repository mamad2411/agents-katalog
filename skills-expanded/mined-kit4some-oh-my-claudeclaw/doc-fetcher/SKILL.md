<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: doc-fetcher
description: >
  API/SDK documentation fetcher via Context Hub MCP + web fallback. Triggers on
  "API docs", "SDK docs", "docs for X", "how to use X", "documentation",
  "API reference", "API 문서", "라이브러리 사용법", "패키지 문서" and similar.
  Uses chub MCP tools (chub_search, chub_get) for curated registry access.
  Falls back to web search when unavailable. Progressive Disclosure with
  memory caching, persistent annotations, quality feedback, and knowledge graph linking.
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - WebSearch
---

# Doc Fetcher — API & SDK Documentation Retrieval

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

Fetch, structure, and persist API/SDK documentation. Uses Progressive Disclosure
(summary first, details on request) to minimize context usage. Leverages Context Hub
(chub) MCP for curated, versioned, LLM-optimized documentation with persistent
annotations and quality feedback.

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
memory_search(query: "{library} documentation", tag: "api-docs")
```

If found and recent (< 30 days): return cached version with any chub annotations.
If found but old: fetch fresh and update.

### Step 2 — Fetch from Context Hub (Primary)

Use chub MCP tools directly (not CLI):

**2a. Search for the doc:**
```
chub_search(query: "{library name}", lang: "{language if known}")
```

Pick the best-matching `id` from results (e.g., `openai/chat`, `stripe/api`).
If nothing matches, try a broader term. If still no results, fall through to Step 3.

**2b. Fetch the doc:**
```
chub_get(id: "{matched_id}", lang: "{py|js|ts}", full: false)
```

- Omit `lang` if the doc has only one language variant (auto-selected)
- Use `full: true` for comprehensive reference (all files)
- Use `file: "references/streaming.md"` for specific reference files

**2c. Check for existing annotations:**
Annotations from previous sessions appear automatically in the `chub_get` response.
These contain workarounds, version quirks, and project-specific notes.

### Step 3 — Web Fallback (if chub unavailable or doc not found)

```
WebSearch("{library} official documentation API reference")
```

Fetch the top result and extract structured documentation.
Note: Web fallback lacks versioning, annotations, and feedback — prefer chub when available.

### Step 4 — Structure, Store & Link

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
  category: "knowledge",
  subcategory: "docs",
  title: "{Library} API Reference v{version}",
  content: "{structured documentation}",
  tags: ["api-docs", "{library}", "{language}"],
  importance: 6
)
```

Link to the current project in the knowledge graph:
```
memory_link(source: "{doc_memory_id}", target: "{project_id}", relation: "related")
```

### Step 5 — Annotate Discoveries

After using the docs, if you discovered something not in the documentation — a gotcha,
workaround, version quirk, or project-specific detail — save it for future sessions:

```
chub_annotate(id: "{doc_id}", note: "{concise actionable discovery}")
```

Annotations are local, persist across sessions, and appear automatically on future
`chub_get` calls. Keep notes concise and actionable. Don't repeat what's already in the doc.

Examples:
- "Webhook verification requires raw body — do not parse before verifying"
- "Rate limit is 100/min not 1000/min as stated — confirmed 2026-03"
- "v2 endpoint deprecated, use v3 with compatibility header"

### Step 6 — Quality Feedback

Rate the doc after using it. This helps authors fix outdated or incorrect docs:

```
chub_feedback(id: "{doc_id}", rating: "up", labels: ["accurate", "helpful"])
chub_feedback(id: "{doc_id}", rating: "down", labels: ["outdated"], comment: "Lists gpt-4o as latest but gpt-5 is out")
```

**Available labels:**
- Positive: `accurate`, `well-structured`, `helpful`, `good-examples`
- Negative: `outdated`, `inaccurate`, `incomplete`, `wrong-examples`, `wrong-version`, `poorly-structured`

**When to rate:**
- Always rate after using a doc for the first time
- Rate down with specific details if you find wrong model names, deprecated APIs, or incorrect code patterns

### Step 7 — Progressive Disclosure Response

**Level 1 — Summary** (always shown):
```markdown
## {Library} v{version}

**Key APIs**: function1(), function2(), Class1, Class2
**Install**: `npm install {library}` / `pip install {library}`
**Source**: Context Hub ({doc_id}) | Annotations: {count}
**Stored**: memory ID #{id}

For detailed usage: `memory_get(id: "{id}")`
```

**Level 2 — Details** (on request):
- Full API signatures with parameters
- Code examples from the doc
- Common patterns and best practices
- Gotchas from annotations

## Source Priority

| Priority | Source | When | Capabilities |
|----------|--------|------|-------------|
| 1 | memory_search | Cached docs from previous sessions | Fastest, project-linked |
| 2 | chub MCP (chub_get) | Curated registry (4,400+ libraries) | Versioned, annotatable, feedback |
| 3 | WebSearch + WebFetch | Fallback for unavailable docs | Broad coverage, no versioning |

## Storage Rules

1. Always store fetched docs in `knowledge/docs/` subcategory
2. Tag with `api-docs` + library name + language
3. Include version number in title
4. Set importance 6 (reference material)
5. Update existing entry if version changed
6. Link to project via `memory_link(relation: "related")`

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
