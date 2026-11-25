# 10X Research — Real-Time Platform Research Skill

The research orchestration engine for 10X Vibe Marketer. Powers multi-platform, real-time research across 13 platforms using Claude in Chrome and WebSearch/WebFetch. Spawns platform-specific research agents in parallel, consolidates findings through the research lead, and delivers actionable marketing intelligence.

*Developed by 10x.in*

---

## When This Skill Activates

This skill activates when the CMO orchestrator detects research intent:

**Trigger keywords:** "research", "trending", "what's happening on", "deep research", "platform trends", "analyze {platform}", "what's working on", "competitive intelligence", any platform name (LinkedIn, Twitter, Reddit, Instagram, Facebook, Google Ads, Google Keywords, YouTube, Pinterest, TikTok, Quora, Medium, Product Hunt)

**Trigger commands:** `/deep-research`, `/research` (with platform option), `/analyze`

---

## No-Setup-Required Architecture

This skill works at 3 tiers — NO setup needed for basic research:

| Tier | Setup Required | Capabilities | Data Persistence |
|------|---------------|--------------|-----------------|
| **Tier 1: Instant** | Nothing | WebSearch + WebFetch research, output to files | Files only (`output/research/`) |
| **Tier 2: Browser** | Chrome extension installed | Real-time platform browsing via `/chrome` | Files + JSONL knowledge base |
| **Tier 3: Full** | `/setup` completed + DB | All of above + database tracking | Files + JSONL + DoltgreSQL DB |

### Setup Warning (One-Time Per Session)

Before starting any research, check `user-preferences.json` (project root) → `wizard_completed`. If `false`, show this warning ONCE:

```
AskUserQuestion({
  question: "You haven't run /setup yet. You can use all research features right now, but your data won't be saved to the database for maximum reusability. How would you like to proceed?",
  header: "Setup",
  options: [
    { label: "Continue without setup (Recommended)", description: "Research works fully. Results saved to files and knowledge base. Run /setup later to enable database persistence." },
    { label: "Run /setup first", description: "Configure your database, preferences, and tools before researching. Takes 2-3 minutes." },
    { label: "Don't ask again this session", description: "Proceed without setup and suppress this warning for the rest of this session." }
  ],
  multiSelect: false
})
```

After this warning, set an internal flag and NEVER show it again in the same session.

---

## References

| Reference | File |
|-----------|------|
| Browser tools | [references/browser-tools.md](references/browser-tools.md) |
| Platform registry | [references/platform-registry.md](references/platform-registry.md) |
| Research patterns | [references/research-patterns.md](references/research-patterns.md) |
| Scoring rubric | [references/scoring-rubric.md](references/scoring-rubric.md) |
| Platform research domain guide | The orchestrator's `references/domains/platform-research.md` |

---

## Research Orchestration Flow

### Step 1: Detect Research Intent

Parse the user's request for:
- **Topic:** What they want to research (e.g., "SaaS marketing trends")
- **Platforms:** Which platforms they mention (or "all" for broad research)
- **Depth:** Quick scan vs deep dive
- **Purpose:** Content creation, competitor analysis, trend tracking, audience research

### Step 2: Check Setup Status

Read `user-preferences.json` (project root). Determine persistence mode:
- `wizard_completed: true` + `database.provider` != "file_only" → `PERSISTENCE MODE: full`
- Otherwise → `PERSISTENCE MODE: file-only`

Show one-time warning if not setup (see above).

### Step 3: Present Platform Selection

Use AskUserQuestion with multiSelect to let user choose platforms:

```
AskUserQuestion({
  question: "Which platforms should I research for '{topic}'? I'll deploy specialist agents for each approved platform.",
  header: "Platforms",
  options: [
    { label: "LinkedIn", description: "Professional trends, industry discussions, B2B insights" },
    { label: "Twitter/X", description: "Real-time trends, hashtags, public sentiment" },
    { label: "Reddit", description: "Community discussions, pain points, authentic feedback" },
    { label: "Instagram", description: "Visual trends, hashtag engagement, Reel formats" },
    { label: "Facebook", description: "Group discussions, Ad Library intelligence, community insights" },
    { label: "Google Ads", description: "Competitor ads, ad copy patterns, bid landscape" },
    { label: "Google Keywords", description: "Search trends, SERP features, keyword opportunities" },
    { label: "YouTube", description: "Video trends, channel analysis, content gaps" },
    { label: "Pinterest", description: "Visual trends, seasonal content, pin engagement" },
    { label: "TikTok", description: "Trending content, sounds, hashtag challenges" },
    { label: "Quora", description: "Audience questions, pain points, expert insights" },
    { label: "Medium", description: "Thought leadership, article trends, publication analysis" },
    { label: "Product Hunt", description: "Product launches, tech trends, maker insights" }
  ],
  multiSelect: true
})
```

### Step 4: Load Knowledge Base Context

Before spawning agents, load relevant context:
```bash
python scripts/research/knowledge_base.py context research --tags {topic_tags}
```

Inject relevant strategies, learnings, and past errors into agent prompts.

### Step 5: Spawn Platform Agents in Parallel

For each approved platform, spawn the corresponding platform agent as a background task:

```python
Task(
    subagent_type="platform-{platform}",
    description="{emoji} {Platform} Research -- {topic}",
    prompt="""CONTEXT: You are a WORKER agent for the 10X Vibe Marketer agency (Developed by 10x.in).
You are the {Platform} Research Specialist.
PLATFORM: win32
PROJECT_ROOT: C:\\Users\\Anit\\Downloads\\Swarms of Agent

PERSISTENCE MODE: {full|file-only}

RULES:
- Complete ONLY the research task described below
- Start with WebSearch + WebFetch (fastest). Use /chrome only if needed
- Do NOT spawn sub-agents or call TaskCreate/TaskUpdate
- Extract structured data: trending topics, engagement metrics, key content
- Save findings to: output/research/{platform}/YYYY-MM-DD-{platform}-{description}.md
- Save learnings: python scripts/research/knowledge_base.py add learnings --title "..." --description "..." --tags {platform}
- Include source URLs for all data points
- Report results with absolute file paths

KNOWLEDGE BASE CONTEXT:
{injected context from Step 4}

RESEARCH QUERY: {user's original query}
FOCUS AREA: {specific topics/keywords}

OUTPUT LOCATION: C:\\Users\\Anit\\Downloads\\Swarms of Agent\\output\\research\\{platform}\\

TASK:
Research '{topic}' on {Platform}. Extract trending topics, engagement data, relevant content, and audience insights. Structure findings in the standard platform research report format.""",
    model="{sonnet|haiku per registry}",
    run_in_background=True
)
```

### Step 6: Consolidate Findings (Research Lead)

After all platform agents complete, spawn the research-analyst as Research Lead:

```python
Task(
    subagent_type="research-analyst",
    description="📊 Research Dept -- consolidate platform findings",
    prompt="""CONTEXT: You are the Research Lead consolidating multi-platform findings.

PLATFORM RESEARCH FILES:
{list of output file paths from each platform agent}

ORIGINAL QUERY: {what the user asked for}
BUSINESS CONTEXT: {from user preferences}

TASK:
1. Read ALL platform research files
2. Synthesize into a unified cross-platform research report
3. Identify cross-platform patterns and themes
4. Rank findings by strategic importance
5. Save consolidated report to: output/research/consolidated/YYYY-MM-DD-research-{topic}.md
6. Save key learnings to knowledge base
7. Produce an executive summary with top 5 insights""",
    model="opus",
    run_in_background=True
)
```

### Step 7: Quality Gate

Spawn quality-judge to evaluate the consolidated report:

```python
Task(
    subagent_type="quality-judge",
    description="⚖️ Quality Review -- platform research evaluation",
    prompt="""DELIVERABLE TO EVALUATE: {consolidated_report_path}
ORIGINAL TASK: Multi-platform research on '{topic}' across {platforms}
EVALUATION TYPE: research""",
    model="sonnet",
    run_in_background=True
)
```

Score >= 75: Deliver to user
Score < 75: Send back to research-analyst for revision (max 2 rounds)

### Step 8: Deliver Results

Present to user:
- Executive summary (top 5 insights)
- File paths to all outputs (per-platform + consolidated)
- Key recommendations
- Suggested next actions (e.g., "/content to create content from these findings", "/strategy to build a strategy")

---

## Platform Agent Registry

| Agent | Emoji | Model | Primary Tool | Best For |
|-------|-------|-------|-------------|----------|
| platform-linkedin | 🔗 | sonnet | /chrome | B2B, professional trends |
| platform-twitter | 🐦 | sonnet | WebSearch | Real-time trends, hashtags |
| platform-reddit | 🟠 | sonnet | WebSearch | Pain points, community feedback |
| platform-instagram | 📸 | sonnet | /chrome | Visual trends, Reels |
| platform-facebook | 👤 | sonnet | /chrome | Groups, Ad Library |
| platform-google-ads | 💲 | sonnet | /chrome | Competitor ads, PPC |
| platform-google-keywords | 🔎 | sonnet | WebSearch | SERP, keyword trends |
| platform-youtube | ▶️ | sonnet | WebSearch | Video trends, channels |
| platform-pinterest | 📌 | sonnet | WebSearch | Visual trends, seasonal |
| platform-tiktok | 🎵 | sonnet | /chrome | Short-form, sounds |
| platform-quora | ❓ | haiku | WebSearch | Questions, pain points |
| platform-medium | 📝 | haiku | WebSearch | Thought leadership |
| platform-producthunt | 🚀 | haiku | WebSearch | Product launches, tech |

---

## Integration with Existing Agents

When platform research is completed, the CMO can inject research file paths into subsequent department agent prompts:

```
RESEARCH CONTEXT AVAILABLE:
Recent platform research has been completed for '{topic}':
- LinkedIn: output/research/linkedin/2026-02-06-linkedin-{topic}.md
- Reddit: output/research/reddit/2026-02-06-reddit-{topic}.md
- Consolidated: output/research/consolidated/2026-02-06-research-{topic}.md
Use these findings to inform your work. Do NOT re-research what's already gathered.
```

### Department → Platform Research Triggers

| Department Agent | When They Need Research | Relevant Platforms |
|-----------------|----------------------|-------------------|
| seo-specialist | Keyword trends, SERP data | google-keywords, youtube |
| social-media-manager | Platform-specific trends | linkedin, twitter, instagram, tiktok, facebook, pinterest |
| paid-ads-specialist | Competitor ad intelligence | google-ads, facebook |
| content-strategist | Content trend data | medium, reddit, quora, youtube |
| outreach-pr-specialist | Influencer data | linkedin, twitter, medium, producthunt |
| community-manager | Community discussion data | reddit, quora, facebook |
| brand-creative-director | Visual trend data | instagram, pinterest, tiktok |
| copywriter | Messaging trends | twitter, linkedin, reddit |

---

## Knowledge Base Integration

### Before Every Research Task
```bash
python scripts/research/knowledge_base.py context {task_type} --tags {platform} {topic_tags}
```

### After Every Research Task
```bash
python scripts/research/knowledge_base.py add learnings \
  --title "{key finding title}" \
  --description "{description of what was learned}" \
  --tags {platform} {topic} research {date}
```

### Knowledge Base Location
- `knowledge/strategies.jsonl` — Research strategies that work
- `knowledge/plans.jsonl` — Research workflow plans
- `knowledge/learnings.jsonl` — Platform-specific learnings (grows with use)
- `knowledge/prompts.jsonl` — Effective research prompts
- `knowledge/errors.jsonl` — Error patterns and solutions
- `knowledge/templates.jsonl` — Research output templates

---

## Output Structure

```
output/research/
├── linkedin/           # LinkedIn agent outputs
├── twitter/            # Twitter/X agent outputs
├── reddit/             # Reddit agent outputs
├── instagram/          # Instagram agent outputs
├── facebook/           # Facebook agent outputs
├── google-ads/         # Google Ads agent outputs
├── google-keywords/    # Google Keywords agent outputs
├── youtube/            # YouTube agent outputs
├── pinterest/          # Pinterest agent outputs
├── tiktok/             # TikTok agent outputs
├── quora/              # Quora agent outputs
├── medium/             # Medium agent outputs
├── producthunt/        # Product Hunt agent outputs
├── scraped/            # Web scraper outputs
└── consolidated/       # Cross-platform consolidated reports
```

---

*Developed by 10x.in*
