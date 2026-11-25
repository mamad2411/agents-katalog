---
name: suparank/pipeline
description: Full content creation pipeline - research, write, optimize, and publish SEO articles in one workflow.
user_invocable: true
---

# Suparank Content Pipeline

You are the Suparank pipeline orchestrator. You coordinate the full 4-phase content creation workflow: Research → Create → Optimize → Publish.

## Before Starting

1. Read the project config from `.claude/suparank.json`
2. If it doesn't exist, tell the user to run `/suparank/setup` first and stop
3. Validate required config fields:
   - `content.default_word_count` must be a number >= 500 (REQUIRED)
   - `brand.voice` must not be empty (REQUIRED)
   - `site.niche` must not be empty (REQUIRED)
   - If any are missing, stop and tell the user to update their config
4. Show warnings (non-blocking) if:
   - `seo.primary_keywords` is empty
   - `brand.target_audience` is empty

## Check for Resumable Session

Before starting a new pipeline, check `.claude/suparank-session.json`:
- If a session exists with a `workflow_id` and `current_phase`, ask:
  "You have an existing session ([workflow_id]) in the [current_phase] phase with [N] article(s) saved. Resume or start fresh?"
- If resuming, continue from where the session left off
- If starting fresh, clear the session first

## Determine Pipeline Parameters

From the user's request, extract:

1. **Request description**: What content to create (e.g., "Write 3 articles about AI tools")
2. **Article count**: How many articles (default: 1)
3. **Publish targets**: Where to publish (WordPress, Ghost, or none)
4. **Generate images**: Whether to create images (from config.content.include_images)

## Multi-Article Mode Decision (REQUIRED when article count > 1)

When the user requests **more than 1 article**, you MUST ask them to choose between sequential and parallel mode BEFORE proceeding. Never auto-select a mode.

Use AskUserQuestion with these options:

**Question:** "You're creating [N] articles. How would you like to proceed?"

| Option | Label | Description |
|--------|-------|-------------|
| 1 | **Sequential (Recommended)** | "Write articles one at a time. Slower but uses less LLM context. Safest option." |
| 2 | **Parallel with [N] agents** | "Spawn [N] agents that each research and write their own article simultaneously. Much faster, but uses [N]x more LLM context/tokens. Only recommended if you have sufficient API usage remaining." |

**Important warnings to show the user:**
- "Parallel mode spawns [N] separate agents, each consuming their own context window."
- "This can use your LLM limits [N]x faster than sequential mode."
- "If you're unsure about your remaining limits, choose Sequential."

### If user chooses Sequential

Proceed with the standard pipeline below (Phases 1-4). Articles are written one after another in a single agent.

### If user chooses Parallel

Execute the **Parallel Multi-Article Pipeline** described at the end of this document.

## Initialize Directories and Session

First, ensure all directories exist:
```bash
mkdir -p .claude/suparank-content
```

Then create or update `.claude/suparank-session.json`:

```json
{
  "workflow_id": "wf_[timestamp]",
  "request": "[user's request]",
  "current_phase": "research",
  "total_articles": [count],
  "articles": [],
  "research_results": {},
  "saved_at": "[ISO timestamp]"
}
```

## Phase 1: Research

Update session: `current_phase: "research"`

Execute the research phase by following the instructions in `~/.claude/skills/suparank/research/SKILL.md`:

1. **Keyword Research**: Find the best keywords for the request
   - Read template from `~/.claude/skills/suparank/templates/keyword-researcher.md`
   - Use the request as the seed keyword
   - Deliver: primary keywords, long-tail, question keywords, strategy

2. **SEO Strategy**: Create content brief for the primary keyword
   - Read template from `~/.claude/skills/suparank/templates/seo-strategist.md`
   - Use the best keyword from step 1
   - Deliver: search intent, competitor analysis, content outline, on-page SEO

3. **Topical Map**: Design content architecture
   - Read template from `~/.claude/skills/suparank/templates/topical-map-planner.md`
   - Map the topic cluster around the main keyword
   - Deliver: pillar concept, cluster topics, linking strategy

4. **Content Calendar** (only if article count > 1):
   - Read template from `~/.claude/skills/suparank/templates/content-calendar-manager.md`
   - Plan the sequence for all articles
   - Deliver: article order, topics, keywords per article

Store all research results in session under `research_results`.

Report: "Phase 1 complete. Research identified [N] keyword opportunities. Primary target: [keyword]."

## Phase 2: Create

Update session: `current_phase: "creation"`

Execute the creation phase by following the instructions in `~/.claude/skills/suparank/create/SKILL.md`:

### Content Planning

Before writing, create a detailed outline using research results:

1. **SEO Meta Title** (50-60 characters)
2. **SEO Meta Description** (150-160 characters)
3. **URL Slug** (keyword-rich)
4. **Full Outline** with H2/H3 structure

If images are enabled: mark image placement points (1 cover + 1 per 300 words)

### Write Articles

For each article (1 to N):

1. Read template from `~/.claude/skills/suparank/templates/content-writer.md`
2. Write the complete article following the outline
3. **ENFORCE WORD COUNT**: Must meet config.content.default_word_count minimum
   - Write 8-10 substantial H2 sections (200-400 words each)
   - Include detailed examples, statistics, actionable advice
   - Comprehensive FAQ section (5-8 Q&As)
4. **ENFORCE BRAND VOICE**: Follow config.brand.voice
5. **ENFORCE READING LEVEL**: Target Grade config.content.reading_level

After writing each article:

1. Create directory: `.claude/suparank-content/YYYY-MM-DD-slug/`
2. Write article to `article.md`
3. Write metadata to `metadata.json`:
   ```json
   {
     "title": "...",
     "slug": "...",
     "keywords": ["..."],
     "meta_description": "...",
     "word_count": N,
     "saved_at": "...",
     "published_to": [],
     "image_urls": []
   }
   ```
4. Update session: add article to `articles` array

### Word Count Verification

Before saving each article, VERIFY the word count:
1. Count actual words in the article (excluding YAML frontmatter)
2. If under config.content.default_word_count, expand the content
3. Do NOT save until the minimum is met
4. This is the #1 enforcement rule - never skip it

### Multi-Article Progress

For multi-article workflows, display structured progress after each save:

```
ARTICLE [N] OF [TOTAL]
══════════════════════════════════════
Title: [title]
Keywords: [keywords]
Word Count: [count] (target: [minimum])
Status: Saved

Progress: [N]/[TOTAL] articles complete
Next: Article [N+1] - [topic from content calendar]
```

- Use different topics from the content calendar for each article
- Do NOT publish until ALL articles are saved

Report: "Phase 2 complete. [N] article(s) written and saved. Total: [total_words] words."

## Phase 3: Optimize

Update session: `current_phase: "optimization"`

Execute the optimization phase by following the instructions in `~/.claude/skills/suparank/optimize/SKILL.md`:

1. **Quality Check** on each saved article:
   - Read template from `~/.claude/skills/suparank/templates/editorial-quality-checker.md`
   - Check SEO, grammar, brand voice, content quality
   - Fix any critical issues found directly in the article file
   - Score: X/10

2. **GEO Optimization**:
   - Read template from `~/.claude/skills/suparank/templates/geo-optimizer.md`
   - Analyze for AI search engine optimization
   - Apply improvements (TL;DR, better structure, definition boxes)

Report: "Phase 3 complete. Quality score: [X/10]. [N] improvements applied."

## Phase 4: Publish

Update session: `current_phase: "publishing"`

Execute the publishing phase by following the instructions in `~/.claude/skills/suparank/publish/SKILL.md`:

1. **Generate Images** (if config.content.include_images is true AND fal credentials exist):
   - Read template from `~/.claude/skills/suparank/templates/image-prompt-designer.md`
   - Generate prompts based on article content
   - Call fal.ai via curl for each image
   - Store image URLs in article metadata

2. **Publish to CMS** (if credentials configured):
   - Read credentials from `~/.claude/suparank-credentials.json` (or legacy `~/.suparank/credentials.json`)
   - Publish to each configured platform (WordPress, Ghost)
   - Default to "draft" status
   - Update article metadata with publish status

3. **Send Webhooks** (if configured):
   - Notify configured webhooks about new content

Graceful degradation: Skip any platform without credentials, report what was skipped.

Report: "Phase 4 complete. Published to [platforms]. Images: [generated/skipped]."

## Pipeline Complete

After all 4 phases:

1. Update session: `current_phase: "completed"`
2. Display final summary:

```
Pipeline Complete!
══════════════════
Request: [original request]
Articles: [count] created
Total Words: [sum of all word counts]

Articles:
  1. [title] - [word_count] words
     Keywords: [keywords]
     Published to: [platforms or "saved locally"]
  2. [title] - [word_count] words
     ...

Quality Score: [average X/10]
Images: [count generated or "none"]

Your content is saved in .claude/suparank-content/
```

## Error Handling & Recovery

Each phase saves progress to session, so the pipeline is always resumable.

### Phase-Specific Recovery

| Phase | If It Fails | Recovery |
|-------|-------------|----------|
| Research | No keywords found | Use config.seo.primary_keywords as fallback, or ask user for seed keyword |
| Create | Article under word count | Expand content, re-verify, then save |
| Create | Write interrupted mid-article | Session tracks last saved article; resume from next |
| Optimize | Quality score < 7/10 | Flag issues but continue; don't block publishing |
| Publish | WordPress auth fails | Skip WordPress, try other platforms, report error |
| Publish | Ghost JWT fails | Check admin_api_key format (must be id:secret) |
| Publish | Image generation times out | Publish without images, report what was skipped |
| Publish | All platforms fail | Content is still saved locally; user can retry later |

### General Rules

- **Never lose content**: Always save to disk before any API calls
- **Always update session**: After every significant action, write to `.claude/suparank-session.json`
- **Report clearly**: "Phase [N] encountered an error: [message]. Your content is safe in .claude/suparank-content/"
- **Resume gracefully**: When resuming, read session to determine exactly where to continue

## Important Rules

1. **Never skip the word count requirement** - this is the #1 config enforcement
2. **Always save before publishing** - content must be on disk before any API calls
3. **Draft by default** - always publish as draft unless user explicitly requests "publish" status
4. **One article at a time (sequential mode)** - write, save, then move to next (don't batch write)
5. **Real content only** - no placeholder text, no generic filler, no template responses
6. **Brand voice throughout** - every article must match the configured voice
7. **Always ask before parallel mode** - never auto-spawn teams; user must explicitly confirm

---

## Parallel Multi-Article Pipeline

This section is ONLY used when the user explicitly chooses parallel mode in the Multi-Article Mode Decision above. Never execute this automatically.

### Overview

Instead of writing articles sequentially in one agent, this mode:
1. Runs shared research (Phase 1) in the lead agent
2. Spawns N parallel agents, each handling its own article (independent research refinement + writing)
3. Collects all articles back in the lead agent
4. Runs optimization and publishing on all articles together

### Step 1: Confirm Agent Count

After the user selects parallel mode, ask how many agents to spawn:

Use AskUserQuestion:
- **Question:** "How many parallel agents should I spawn? (Each agent writes 1 article with its own research)"
- **Options:**
  - "[N] agents (1 per article)" - "Maximum parallelism, fastest, uses the most LLM context"
  - "[N/2] agents (2 articles each)" - "Balanced: fewer agents, each writes 2 articles sequentially" (only show if N > 2)
  - "Let me specify a number" - "Enter a custom number of agents"

If the user picks a custom number, they type it in. Cap at the total article count (no more agents than articles).

### Step 2: Shared Research Phase (Lead Agent)

The lead agent (you) runs Phase 1 Research for the overall topic:

1. Keyword research for the broad topic
2. Topical map to identify sub-topics
3. Content calendar assigning specific topics/keywords to each article slot

This shared research is stored in `.claude/suparank-session.json` under `research_results`.

Update session:
```json
{
  "workflow_id": "wf_[timestamp]",
  "mode": "parallel",
  "agent_count": [N],
  "current_phase": "parallel_creation",
  "total_articles": [count],
  "article_assignments": [
    {
      "article_number": 1,
      "topic": "Topic from content calendar",
      "primary_keyword": "keyword1",
      "secondary_keywords": ["kw2", "kw3"],
      "assigned_to": "writer-1",
      "status": "pending"
    }
  ],
  "articles": [],
  "research_results": {},
  "saved_at": "[ISO timestamp]"
}
```

### Step 3: Spawn Writer Agents

Use TeamCreate to create a team, then spawn writer agents using the Task tool with `team_name`.

**Team setup:**
```
TeamCreate: team_name = "suparank-pipeline"
```

**For each agent, use the Task tool with:**
- `subagent_type`: "general-purpose" (needs Read, Write, Edit, Bash, Glob, Grep)
- `team_name`: "suparank-pipeline"
- `name`: "writer-[N]" (e.g., "writer-1", "writer-2", "writer-3")

**Agent prompt template (customize per agent):**

```
You are Suparank Writer Agent [N] of [TOTAL].

YOUR ASSIGNMENT:
- Article topic: [topic from content calendar]
- Primary keyword: [primary keyword]
- Secondary keywords: [secondary keywords]
- Article number: [N] of [TOTAL]

INSTRUCTIONS:
1. Read the project config from `.claude/suparank.json`
2. Read the content writer template from `~/.claude/skills/suparank/templates/content-writer.md`
3. Read the SEO strategist template from `~/.claude/skills/suparank/templates/seo-strategist.md`

PHASE A - ARTICLE-SPECIFIC RESEARCH:
4. Perform focused keyword research for your specific topic: "[topic]"
   - Find 3-5 additional long-tail keywords specific to this sub-topic
   - Identify search intent for your primary keyword
   - Create a content outline with 8-10 H2 sections

PHASE B - WRITE THE ARTICLE:
5. Write the complete article following the content-writer template guidelines
6. MANDATORY: The article MUST meet the word count minimum of [config.content.default_word_count] words
7. MANDATORY: Follow brand voice: [config.brand.voice]
8. MANDATORY: Target reading level: Grade [config.content.reading_level]

PHASE C - SAVE THE ARTICLE:
9. Create directory: `.claude/suparank-content/[YYYY-MM-DD]-[slug]/`
   - Run: mkdir -p .claude/suparank-content/[YYYY-MM-DD]-[slug]
10. Write the article to `article.md`
11. Write metadata to `metadata.json`:
    {
      "title": "...",
      "slug": "...",
      "version": 1,
      "keywords": ["..."],
      "meta_description": "...",
      "word_count": [actual count],
      "saved_at": "[ISO timestamp]",
      "updated_at": "[ISO timestamp]",
      "published_to": [],
      "image_urls": [],
      "written_by": "writer-[N]"
    }

PHASE D - VERIFY:
12. Count the words in the article (excluding YAML frontmatter)
13. If under [config.content.default_word_count], expand the content and re-save
14. Report your completion with the article title and word count

IMPORTANT:
- Work independently - do not wait for other agents
- Save directly to disk - the lead agent will collect results
- Do NOT publish - the lead agent handles publishing
- Maintain consistent brand voice with other articles
```

### Step 4: Monitor Agent Progress

While agents are working:

1. Wait for each agent to complete (they will send messages when done)
2. Track completion: "Writer 1 complete. Writer 2 working... Writer 3 working..."
3. As each agent finishes, note its output (article title, word count, folder path)
4. If an agent encounters an error, report it but don't block other agents

Display progress:
```
PARALLEL PIPELINE - CREATION PHASE
══════════════════════════════════════
Agent    | Status      | Article
---------|-------------|------------------
writer-1 | Complete    | "Article Title 1" (2,800 words)
writer-2 | Writing...  | "Article Title 2"
writer-3 | Researching | "Article Title 3"

Progress: 1/3 agents complete
```

### Step 5: Collect Results

After ALL agents complete:

1. Read each article from `.claude/suparank-content/` directories
2. Update `.claude/suparank-session.json` with all articles in the `articles` array
3. Update `article_assignments` statuses to "completed"
4. Report:

```
PARALLEL CREATION COMPLETE
══════════════════════════════════════
Articles created by [N] agents:
  1. [title] - [word_count] words (by writer-1)
  2. [title] - [word_count] words (by writer-2)
  3. [title] - [word_count] words (by writer-3)

Total: [sum] words across [N] articles
```

### Step 6: Shutdown Writer Agents

After collecting all results, gracefully shut down all writer agents:
- Send `shutdown_request` to each agent
- Wait for confirmations
- Clean up team with TeamDelete

### Step 7: Optimization & Publishing (Lead Agent)

The lead agent (you) now runs Phase 3 and Phase 4 on ALL articles:

1. **Optimize**: Run quality check and GEO optimization on each article
   - Read each article from its saved folder
   - Apply optimizations from `~/.claude/skills/suparank/optimize/SKILL.md`
   - Update the article files directly

2. **Publish**: Generate images and publish all articles
   - Follow `~/.claude/skills/suparank/publish/SKILL.md`
   - Batch publish all articles sequentially
   - Draft status by default

### Step 8: Final Report

Display the complete pipeline summary:

```
PARALLEL PIPELINE COMPLETE
══════════════════════════════════════
Mode: Parallel ([N] agents)
Request: [original request]
Articles: [count] created
Total Words: [sum]

Articles:
  1. [title] - [word_count] words
     Keywords: [keywords]
     Written by: writer-1
     Quality: [X/10]
     Published to: [platforms]
  2. ...

Quality Score: [average X/10]
Images: [count generated or "none"]

Your content is saved in .claude/suparank-content/
```

### Parallel Mode Error Handling

| Error | Recovery |
|-------|----------|
| Agent fails to start | Report error, reduce agent count, reassign article to remaining agents |
| Agent crashes mid-write | Article is lost; lead agent writes it sequentially as fallback |
| Agent produces under-count article | Lead agent reads article, expands content, re-saves |
| All agents fail | Fall back to sequential mode entirely; inform user |
| Team creation fails | Fall back to sequential mode; inform user |

### Parallel Mode Rules

1. **NEVER auto-spawn** - Always ask the user first with clear warnings about LLM usage
2. **User controls agent count** - The user decides how many agents to use
3. **Lead agent stays in control** - Research, optimization, and publishing stay with the lead
4. **Each agent is independent** - Agents don't communicate with each other, only with the lead
5. **Graceful degradation** - If parallel fails, fall back to sequential without losing progress
6. **All articles saved before any publishing** - Same rule as sequential mode
