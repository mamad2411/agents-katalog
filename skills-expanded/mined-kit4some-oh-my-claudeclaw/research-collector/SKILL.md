<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly. Run: node scripts/gen-skill-docs.mjs -->

---
name: research-collector
description: >
  Automated web research pipeline with OMC integration. Triggers on "조사해",
  "수집해", "리서치", "찾아봐", "동향 파악", "경쟁사 분석", "뉴스 모아", "트렌드 분석",
  "research", "collect", "find out", "trend analysis", "competitor analysis" and
  similar. v3: Delegates to research-agent for parallel collection, uses
  memory_similar for deduplication, builds knowledge graph connections.
  For deeper research use /deep-research instead.
---

# Research Collector — Research & Information Collection Automation Pipeline

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

Analyze the user's research request, collect information through web search and
page fetching, structure it, persist it in memory, and report in a standard
format. Before starting, check existing related knowledge with `memory_search`
and focus collection on the delta from what is already known.

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

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `memory_search` | Retrieve existing relevant memories (required at task start) |
| `memory_store` | Persist collected results |
| `web_search` | Execute multi-angle search queries |
| `web_fetch` | Collect detailed content from promising URLs |

## Research Pipeline — 5 Steps

### Step 1 — Request Analysis

Determine 3 things from the user request:

| Item | Question | Determination Criteria |
|------|----------|------------------------|
| **Topic** | What is the research about? | Extract 1–3 core keywords |
| **Information Type** | What kind of information is needed? | See type classification table below |
| **Depth** | How deeply should we investigate? | quick / standard / deep |

**Information Type Classification**:

| Type | Trigger Expressions | Research Strategy |
|------|--------------------|--------------------|
| Competitor analysis | "경쟁사", "competitor", "비교", "compare" | → Competitor analysis strategy |
| Technology trends | "동향", "trend", "기술 스택", "최신", "latest", "tech stack" | → Technology trends strategy |
| Person research | Name + affiliation, "누구", "프로필", "who is", "profile" | → Person research strategy |
| Market research | "시장", "market", "규모", "성장률", "size", "growth rate" | → Market research strategy |
| General research | None of the above | → Technology trends strategy (adapted) |

**Depth Determination**:

| Depth | Queries | web_fetch calls | Est. Time |
|-------|---------|-----------------|-----------|
| quick | 3 | 1–2 | Under 1 min |
| standard | 5 | 3–5 | 2–3 min |
| deep | 8 | 5–10 | 5+ min |

Default: standard. User says "briefly", "quickly" → quick. "In detail", "in depth", "thoroughly" → deep.

### Step 2 — Search Strategy

Generate 3–8 search queries depending on depth.

**Query Generation Rules**:

1. **Bilingual**: Generate Korean + English query pairs for every topic
2. **Multi-angle**: Search the same topic from different perspectives (news, technical, business, opinion)
3. **Date keywords**: Include "2026", "latest", "recent", "최근" when recency matters
4. **Refinement**: Narrow subsequent queries based on initial search results

**Query Structure Template**:

```
Query 1 (Korean general):   "{topic} {info_type} 최신"
Query 2 (English general):  "{topic} {info_type} 2026 latest"
Query 3 (Korean specific):  "{topic} {detail_keyword} {date_range}"
Query 4 (English specific): "{topic} {specific_keyword} {date_range}"
Query 5+ (expansion):       Follow-up queries based on results (deep mode only)
```

### Step 3 — Information Collection

**Execution Order**:

1. Run each query with `web_search`
2. Select promising URLs from results (based on title and snippet)
3. Fetch detailed content from selected URLs with `web_fetch`
4. Extract key data points from each source

**Source Priority** (highest first):

| Priority | Source Type | Examples |
|----------|------------|---------|
| 1 | Official announcements / press releases | Company blogs, PR Newswire |
| 2 | Major tech media | TechCrunch, The Verge, ZDNet Korea |
| 3 | Professional analysis reports | Gartner, CB Insights, Statista |
| 4 | Communities / forums | Hacker News, Reddit, GeekNews |
| 5 | Personal blogs / social media | Medium, Twitter/X, personal blogs |

**Collection Guidelines**:

- Avoid collecting duplicate information (compare against already-extracted data points)
- Check dates: flag information older than 6 months with "date caution"
- Always record the source URL for numerical data

### Step 4 — Structuring & Memory Storage

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

Persist collected information with `memory_store`.

**memory_store Parameter Mapping by Research Type**:

| Research Type | category | subcategory | Tags Rule | importance |
|---------------|----------|-------------|-----------|------------|
| Competitor analysis | `projects` | Project name (e.g., `sapiens`) | `["competitor", "analysis", competitor_name...]` | 7 |
| Technology trends | `knowledge` | Tech domain (e.g., `ai`, `web3`) | `["trend", "technology", keywords...]` | 6 |
| Person research | `people` | _(none)_ | `["profile", affiliation, role...]` | 6 |
| Market research | `knowledge` | `business` | `["market", "analysis", industry_name...]` | 6 |
| General research | `knowledge` | Topic domain | `["research", keywords...]` | 5 |

**Content Structure for Storage**:

```markdown
## Research Overview
- Topic: {topic}
- Date: {YYYY-MM-DD}
- Queries: {N} | Sources: {M}

## Key Findings
1. {Finding 1} — [Source]({url})
2. {Finding 2} — [Source]({url})

## Detailed Content
{Structured analysis}

## Sources
- [{Title}]({url}) — {date}, {source type}
```

**Storage Rules**:

- Competitor analysis: store each competitor individually + 1 comparison matrix = N+1 total entries
- Technology trends: consolidate into 1 entry per topic
- Person research: 1 entry per person
- Market research: 1 entry per market

### Step 5 — Report Generation

After all collection and storage is complete, report using the standard template below:

```markdown
## Research Report: {Topic}

**Date**: {YYYY-MM-DD HH:MM}
**Research Type**: {Competitor Analysis / Technology Trends / Person Research / Market Research}
**Depth**: {quick / standard / deep}
**Queries**: {N} | **Sources Collected**: {M}

---

### Key Findings

1. **{Finding Title}** — {One-line summary} ([Source]({url}))
2. **{Finding Title}** — {One-line summary} ([Source]({url}))
3. ...

### Detailed Analysis

{Structured analysis by type — comparison table for competitors, change timeline for technology, etc.}

### Source List

| # | Title | URL | Date | Reliability |
|---|-------|-----|------|-------------|
| 1 | {title} | {url} | {date} | {High/Medium/Low} |

### Memory Storage Log

| Item | category | tags | importance |
|------|----------|------|------------|
| {title} | {category} | {tags} | {importance} |

### Items Requiring Further Investigation

- {Unresolved questions or areas needing additional research}
```

## Detailed Strategies by Research Type

### 1. Competitor Analysis

```
Steps:
1. memory_search(query: "competitor", category: "projects") → check existing competitor list
2. If no competitor list → web_search("{project} competitor alternatives") to identify them
3. For each competitor (parallelizable):
   a. web_search("{competitor_name} funding news 2026")
   b. web_search("{competitor_name} product update latest")
   c. web_fetch(official site/blog)
4. Build comparison matrix:
   | Item        | Ours | Competitor A | Competitor B |
   |-------------|------|--------------|--------------|
   | Product     | ...  | ...          | ...          |
   | Funding     | ...  | ...          | ...          |
   | Tech stack  | ...  | ...          | ...          |
   | Strengths   | ...  | ...          | ...          |
   | Weaknesses  | ...  | ...          | ...          |
5. memory_store(category:"projects", subcategory:"{project}", tags:["competitor","analysis"], importance:7)
```

### 2. Technology Trends

```
Steps:
1. memory_search(query: "{tech keyword}", category: "knowledge") → check existing knowledge
2. Search queries (Korean/English pairs):
   a. "{기술} 최신 동향 2026" / "{technology} trend 2026 latest"
   b. "{기술} 신규 릴리즈" / "{technology} new release announcement"
   c. "{기술} 비교 분석" / "{technology} comparison benchmark"
3. Extract key changes (delta vs. existing knowledge):
   - New versions/features
   - Market adoption rate changes
   - Major events (acquisitions, open-sourcing, etc.)
4. memory_store(category:"knowledge", subcategory:"{domain}", tags:["trend","technology",keyword], importance:6)
```

### 3. Person Research

```
Steps:
1. memory_search(query: "{name}", category: "people") → check existing profile
2. Search queries:
   a. "{이름} {소속}" / "{name} {organization}"
   b. "{이름} LinkedIn" / "{name} conference speaker"
   c. "{이름} interview" / "{name} 인터뷰"
3. Collect:
   - Current affiliation and title
   - Career history
   - Areas of expertise and interests
   - Recent talks/activities
   - Social media/contact info (public info only)
4. memory_store(category:"people", title:"{name}", tags:["profile", affiliation, role], importance:6)
5. If related project memory exists, add link via memory_update
```

### 4. Market Research

```
Steps:
1. memory_search(query: "{market}", category: "knowledge") → check existing market data
2. Search queries:
   a. "{시장} 시장 규모 2026" / "{market} market size 2026"
   b. "{시장} 성장률 전망" / "{market} growth forecast CAGR"
   c. "{시장} 주요 기업 점유율" / "{market} key players market share"
   d. "{시장} 규제 동향" / "{market} regulation policy"
3. Collect:
   - TAM/SAM/SOM (where available)
   - CAGR and growth outlook
   - Key players and market share
   - Barriers to entry and regulatory environment
   - Recent M&A/investment activity
4. memory_store(category:"knowledge", subcategory:"business", tags:["market","analysis",industry_name], importance:6)
```

## Execution Principles

1. **Existing knowledge first** — Always run `memory_search` before collecting. Avoid duplicate collection.
2. **Sources required** — Attach a URL source for every figure and fact. Mark unverified information as "unconfirmed".
3. **Bilingual** — Run Korean + English queries in parallel to balance domestic and international coverage.
4. **Recency first** — When multiple items cover the same topic, prioritize the most recent.
5. **Delta-focused** — Focus on new changes rather than information already in existing memories.

## Reference Documents

- Detailed search strategies and query examples by type: `references/research-strategies.md`
- Report formatting script: `scripts/format-report.py`

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
