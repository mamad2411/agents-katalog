---
name: wild-scan
description: >
  Pain-quote harvester for the "From the Wild" content series. Searches Reddit,
  HN, Stack Overflow, dev.to, and other communities for SPECIFIC QUOTES of real
  people struggling with a topic (e.g., learning DevOps). Indexes quotes by theme,
  scores them for content potential, and generates "From the Wild" content briefs
  with instructional repo specs. Run weekly to fuel the content loop.
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F3AF"
---

# Wild Scan

Harvest real pain quotes from the internet, index them, and turn the best ones into "From the Wild" content briefs — each backed by a GitHub instructional repo that demolishes the pain point with working code.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## When to Use

- Sourcing real quotes for the weekly "From the Wild" content series
- Finding specific pain points to target with instructional repos
- Building a quote index before writing content
- Validating whether a topic has real, quotable pain (not just assumed pain)
- Refilling the content pipeline with fresh pain signals

## Trigger Phrases

- "Scan the wild for [topic] pain points"
- "Find me quotes about [topic] struggles"
- "Run a wild scan on [topic]"
- "What are people complaining about re: [topic]?"
- "/wild-scan [topic]"
- "From the wild: [topic]"

---

## Prerequisites

Before starting, establish three things with the user:

1. **Topic focus** — What specific area to harvest (e.g., "learning Kubernetes from scratch", "CI/CD pipeline debugging", "Terraform state management"). The more specific, the better the quotes.
2. **Learning stage** — Who is struggling? Beginners? Mid-level engineers transitioning to DevOps? Senior devs dealing with tool complexity?
3. **Repo angle** — What kind of instructional repo would solve these? (e.g., "step-by-step deploy pipeline", "real-world K8s manifests with commentary", "production-grade Terraform modules with explanation")

If the user provides only a topic, ask about stage and repo angle before proceeding. If they say "just go" or provide all three, proceed directly.

---

## Workflow

```
Topic + Stage + Repo Angle (from user)
    |
Phase 1: Search Planning (define queries, platforms, subreddits)
    |
Phase 2: Quote Harvesting (web search — real quotes required)
    |
Phase 3: Quote Scoring (specificity, intensity, solvability, engagement)
    |
Phase 4: Theme Clustering (group by pain theme)
    |
Phase 5: Content Brief Generation ("From the Wild" post outlines)
    |
Phase 6: Repo Spec (instructional repo that demolishes the pain point)
    |
Output: JSON index + Markdown quote collection + Content briefs → vault
```

---

## Phase 1: Search Planning

Define the search strategy before harvesting anything.

**Produce a search plan:**
- Topic boundaries (what's in scope, what's adjacent but excluded)
- Target platforms and specific communities (subreddits, HN, SO tags, etc.)
- Search queries (see [references/search-playbook.md](references/search-playbook.md) for templates)
- Pain language to target (frustration indicators, help-seeking patterns)
- Learning stage filter (what level of quote are we looking for?)

Present this to the user for a quick confirmation. Scope adjustments here prevent harvesting irrelevant quotes.

### Platform Priorities

| Platform | Why | Best For |
|----------|-----|----------|
| Reddit | Unfiltered, emotional, high engagement signals via upvotes | Raw pain, frustration, "I wish..." |
| Hacker News | Technical depth, experienced engineers | Structural critiques, "the real problem is..." |
| Stack Overflow | Behavioral signals (workarounds, repeated questions) | "How do I actually..." pain |
| Dev.to / Hashnode | Learning-focused, personal stories | "What I wish I knew...", tutorial critique |
| Twitter/X | Hot takes, viral frustration threads | Punchy quotes, zeitgeist pain |
| Discord / Slack (public) | Direct community chatter | Unguarded pain, real-time frustration |

---

## Phase 2: Quote Harvesting

**This phase requires extensive web search. Use real quotes. Do NOT fabricate or paraphrase.**

For each platform in the search plan, run targeted searches using the queries from Phase 1. See [references/search-playbook.md](references/search-playbook.md) for search query templates.

### Harvesting Rules

1. **Exact quotes only.** Copy the actual text. Do not paraphrase, summarize, or "clean up" quotes. Typos and all. The rawness is the point.
2. **Attribution required.** Every quote needs: username (or anonymized handle), platform, community/subreddit, date (if available), and engagement metrics (upvotes, likes, comments).
3. **Engagement threshold.** Prioritize quotes with social proof — upvotes, replies, "same here" responses. A 200-upvote Reddit comment is more valuable than a 2-upvote one because the pain is validated.
4. **Minimum harvest: 15 quotes per run.** Aim for 20-30. Cast a wide net; scoring will filter.
5. **No corporate blogs, no marketing content, no course landing pages.** We want real humans, not content marketers performing empathy.
6. **Recency matters.** Prefer quotes from the last 12 months. Older quotes are acceptable if the pain is clearly still active (check for recent duplicates).
7. **Capture context.** Don't just grab the quote — note what thread/question it was responding to. The context shapes how we use it.

### What Makes a Quote Worth Harvesting

**Harvest these:**
- "I've been doing tutorials for 6 months and I still can't deploy to production"
- "Every Terraform tutorial assumes you already know networking. WHERE DO I LEARN NETWORKING?"
- "I spent 3 days debugging a YAML indentation error in my K8s manifest. I am losing my mind."
- "Serious question: how did any of you actually learn CI/CD? Every resource I find is either 'hello world' or 'here's our enterprise pipeline with 47 stages'"

**Skip these:**
- "DevOps is hard" (too vague)
- "I don't like Kubernetes" (no specific pain)
- "Check out my new course!" (marketing, not pain)
- "The industry needs better tools" (editorializing, not suffering)

### Per-Quote Capture Format

For each harvested quote, record:

| Field | Required | Description |
|-------|----------|-------------|
| `quote` | Yes | Exact text of the quote |
| `author` | Yes | Username or handle (e.g., "u/devops_mike") |
| `platform` | Yes | Reddit, HN, SO, dev.to, Twitter, Discord, other |
| `community` | Yes | Specific subreddit, HN thread, SO tag, etc. |
| `url` | Yes | Direct link to the quote (or thread if quote is a comment) |
| `date` | Best effort | When the quote was posted |
| `engagement` | Yes | Upvotes, likes, replies, "same" responses |
| `context` | Yes | What thread/question the quote was responding to |
| `pain_category` | Yes | One of: tutorial-gap, tool-complexity, real-world-gap, career-transition, information-overload, environment-setup, debugging-hell, missing-fundamentals |

---

## Phase 3: Quote Scoring

Score every harvested quote on four dimensions. See [references/scoring-rubric.md](references/scoring-rubric.md) for detailed calibration.

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| specificity | 2x | How specific is the pain? "K8s is hard" = 2. "I can't figure out how to pass secrets from GitHub Actions to my EKS cluster without hardcoding them" = 9. |
| intensity | 2x | How much does this person hurt? Measured by emotional language, effort described, desperation level. |
| solvability | 2x | Can we actually demolish this with a repo? "My company won't adopt DevOps" = 1. "I need a working CI/CD pipeline template" = 10. |
| engagement | 1x | Social proof. Upvotes, replies, "same here" responses. Validates the pain is shared. |

**Overall score** = weighted average: `(specificity*2 + intensity*2 + solvability*2 + engagement) / 7`

### Scoring Discipline

Each score MUST be justified with one sentence. Example:

> specificity: 8 — "Calls out the exact gap: passing secrets from GitHub Actions to EKS. Not a vague complaint."
> intensity: 7 — "Used 'losing my mind', described 3 days of debugging. Real suffering, not casual grumbling."
> solvability: 9 — "A secrets-management tutorial with working GitHub Actions + EKS config would directly solve this."
> engagement: 6 — "47 upvotes, 12 replies including 3 'same here' responses. Validated pain."

---

## Phase 4: Theme Clustering

Group scored quotes into pain themes. A theme is a recurring structural problem that multiple quotes point to.

### Theme Format

| Field | Description |
|-------|-------------|
| `theme` | Name of the pain theme (e.g., "The Tutorial-to-Production Gap") |
| `thesis` | One sentence: what structural failure creates this pain? |
| `quote_count` | How many quotes cluster here |
| `avg_score` | Average score of quotes in this cluster |
| `top_quotes` | The 2-3 highest-scoring quotes in this theme |
| `repo_angle` | What kind of instructional repo would demolish this entire theme? |

### Clustering Rules

- Every quote must belong to exactly one theme
- A theme needs at least 2 quotes to be valid (1 quote = anecdote, 2+ = pattern)
- Themes should be structural, not surface-level. "YAML is annoying" is surface. "Configuration-as-code tools have a documentation gap between 'getting started' and 'production-ready'" is structural.
- If a theme has 5+ quotes and an average score above 7, it's a **gold theme** — flag it for priority content

---

## Phase 5: Content Brief Generation

For each theme with avg_score >= 6 (and especially gold themes), generate a "From the Wild" content brief.

### "From the Wild" Post Format

The content series follows a consistent structure:

```
1. THE QUOTE (screenshot-worthy, raw, real)
   "I've been doing tutorials for 6 months and I still can't deploy
    a real app to production..." — u/frustrated_junior, r/devops, 234 upvotes

2. THE DIAGNOSIS (what's actually going wrong — the structural problem)
   Every tutorial teaches tools in isolation. Nobody shows the full path
   from code → CI → deploy → observe → iterate. The gap isn't knowledge,
   it's integration.

3. THE HACK (the repo that demolishes it)
   "So we built this." → link to repo
   3-5 key decisions highlighted with code snippets

4. THE WALKTHROUGH (enough to prove it works)
   Step-by-step of the critical path, with git tags for each stage

5. THE CTA
   "Found another one? Drop it in the comments."
   (This is how you crowdsource future quotes)
```

### Brief Fields

For each content brief, produce:

| Field | Description |
|-------|-------------|
| `title` | Post title. Punchy, specific. NOT "DevOps is Hard." YES: "Found Another One: 'Every Tutorial Stops at Hello World'" |
| `featured_quote` | The lead quote for the post (highest-scoring in the theme) |
| `supporting_quotes` | 1-2 additional quotes that reinforce the same pain |
| `diagnosis` | 2-3 sentences: what structural failure creates this pain? |
| `repo_name` | Proposed GitHub repo name (kebab-case, descriptive) |
| `repo_description` | One-line repo description |
| `channel` | Where to post: LinkedIn, blog, Substack, Reddit |
| `estimated_words` | Target length by channel |
| `series` | "From the Wild" |
| `difficulty` | easy, medium, hard — how hard is the repo to build? |

---

## Phase 6: Repo Spec

For each content brief, spec the instructional repo that demolishes the pain point.

### What Makes a Repo "Battle Axe" Level

This is NOT a tutorial repo. This is a working, production-grade reference that happens to be teachable. The difference:

| Tutorial Repo | Battle Axe Repo |
|---------------|-----------------|
| `console.log("Hello World")` | Structured logging with correlation IDs |
| "Deploy to Heroku" | Multi-environment deploy with rollback |
| Single `main.tf` | Modular Terraform with state management |
| No tests | CI pipeline with test, lint, security scan |
| README says "getting started" | README says "here's what production looks like" |
| Stops at "it works locally" | Includes monitoring, alerting, runbook |

### Repo Spec Format

| Field | Description |
|-------|-------------|
| `name` | Repo name (kebab-case) |
| `tagline` | One-line description for GitHub |
| `pain_addressed` | Which quote(s) this repo directly answers |
| `structure` | Key directories and files with purpose |
| `progressive_steps` | Git tags or branches for step-by-step learning (e.g., `step-01-basic` through `step-08-production`) |
| `key_decisions` | 3-5 architectural decisions with "why X not Y" explanations |
| `battle_axe_features` | What makes this production-grade, not tutorial-grade |
| `prerequisites` | What the user needs to know before using this repo |
| `estimated_build_time` | How long to build this repo |

### Progressive Step Design

Every repo MUST have progressive steps via git tags:

```
step-01-scaffold     — Basic project structure, nothing works yet
step-02-local        — Works locally, manual everything
step-03-containerize — Dockerized, but still manual deploy
step-04-ci           — Automated tests on push
step-05-cd           — Automated deploy on merge to main
step-06-secrets      — Secrets management (not hardcoded)
step-07-monitor      — Logging, metrics, health checks
step-08-production   — The full thing: rollback, alerting, runbook
```

Each step has its own README section explaining not just WHAT changed but WHY. The "why" is what separates this from every other tutorial.

---

## Output

The scan produces files saved to the Obsidian vault:

**Vault path:** `${VAULT}/`

### 1. Quote Index: `{vault}/Writing/From-The-Wild/{topic-slug}-{YYYY-MM-DD}.md`

The indexed collection of all harvested quotes, scored and themed.

```markdown
---
type: wild-index
date: YYYY-MM-DD
status: active
topic: "[topic focus]"
stage: "[learning stage]"
quote_count: N
theme_count: N
gold_themes: N
tags:
  - content/from-the-wild
  - hunter/domain/{domain-slug}
---

# Wild Scan: [Topic]

**Date**: [date]
**Topic**: [topic focus]
**Stage**: [learning stage]
**Quotes harvested**: N
**Themes identified**: N
**Gold themes**: N (avg score >= 7 with 5+ quotes)

## Gold Themes

### 1. [Theme Name] (Avg Score: X/10, N quotes)
**Thesis**: [structural failure]
**Repo angle**: [what would demolish this]

> "[Top quote text]"
> — [author], [community], [engagement]

> "[Second quote]"
> — [author], [community], [engagement]

### 2. [Next gold theme...]

## All Themes (Ranked)

| Rank | Theme | Quotes | Avg Score | Top Pain Category | Repo Angle |
|------|-------|--------|-----------|-------------------|------------|
| 1 | [name] | N | X.X | [category] | [angle] |
| ... | ... | ... | ... | ... | ... |

## Quote Log (All Quotes, Scored)

### Theme: [Theme Name]

| Score | Quote (truncated) | Author | Platform | Engagement | Category |
|-------|-------------------|--------|----------|------------|----------|
| 8.4 | "I spent 3 days..." | u/name | r/devops | 127 upvotes | debugging-hell |
| ... | ... | ... | ... | ... | ... |

## Full Quotes

### Quote 1 (Score: X.X)
> "[Full quote text]"

- **Author**: [username]
- **Platform**: [platform]
- **Community**: [subreddit/thread]
- **URL**: [link]
- **Date**: [date]
- **Engagement**: [upvotes, replies]
- **Context**: [what thread this was in]
- **Pain category**: [category]
- **Scoring**: specificity X, intensity X, solvability X, engagement X

### Quote 2...
[repeat for all quotes]
```

### 2. JSON Index: `{vault}/Writing/From-The-Wild/wild-scan-{topic-slug}-{YYYY-MM-DD}.json`

Structured data following the schema in [references/output-schema.json](references/output-schema.json).

### 3. Content Briefs: `{vault}/Writing/Content-Briefs/ftw-{topic-slug}-{theme-slug}-{YYYY-MM-DD}.md`

One brief per gold theme (or per theme with avg_score >= 6).

```markdown
---
type: content-brief
status: backlog
series: "From the Wild"
channel: linkedin, blog
estimated_words: 1500
created: YYYY-MM-DD
ready: true
wild_scan_ref: "{topic-slug}-{YYYY-MM-DD}"
theme: "[theme name]"
tags:
  - content/from-the-wild
  - content/brief
  - content/series/from-the-wild
  - hunter/domain/{domain-slug}
---

# Found Another One: "[Featured Quote Snippet]"

## The Quote
> "[Full featured quote]"
> — [author], [community], [engagement]

### Supporting Quotes
> "[Supporting quote 1]"
> — [author], [community]

> "[Supporting quote 2]"
> — [author], [community]

## The Diagnosis
[2-3 sentences: what structural failure creates this pain? Not a restatement of the quote — the WHY behind it.]

## The Hack (Repo Spec)
**Repo**: `[repo-name]`
**Tagline**: [one-line description]

### Structure
[Key directories and files]

### Progressive Steps
[Git tag progression from basic → production]

### Key Decisions
1. [Decision]: [Why X not Y]
2. [Decision]: [Why X not Y]
3. [Decision]: [Why X not Y]

### Battle Axe Features
- [Feature that makes this production-grade]
- [Feature that makes this production-grade]
- [Feature that makes this production-grade]

## Post Outline
1. **Hook**: The quote itself (screenshot-formatted)
2. **Diagnosis**: [2-3 sentences]
3. **Solution**: "So we built this" → repo link
4. **Walkthrough**: [3-5 key steps highlighted]
5. **CTA**: "Found another one? Drop it in the comments."

## Channel Adaptations
- **LinkedIn** (400 words): Lead with quote, tight diagnosis, link to repo, CTA
- **Blog** (1500 words): Full walkthrough with code snippets from repo
- **Reddit** (self-post): Post directly in the subreddit where the quote came from. Value-first, no self-promotion smell.

## Build Estimate
- **Repo difficulty**: [easy/medium/hard]
- **Estimated build time**: [time]
- **Prerequisites for builder**: [what you need to know to build this repo]
```

---

## Cumulative Index

Each wild-scan run produces a new date-stamped file. Over time, the `Writing/From-The-Wild/` folder becomes a searchable quote database.

To find previously harvested quotes on a topic:
```
Glob: Writing/From-The-Wild/*kubernetes*.md
Grep: "tutorial-gap" in Writing/From-The-Wild/
```

To avoid re-harvesting the same quotes, check existing indices before running a new scan:
```
Read {vault}/Writing/From-The-Wild/ → scan for duplicate quotes
```

---

## Integration with Content Planner

Content briefs generated by wild-scan are compatible with content-planner's brief format. After a wild-scan run:

1. Content briefs land in `Writing/Content-Briefs/` with `series: "From the Wild"`
2. Content-planner picks them up on its next scan
3. They appear on `Content-Plan.kanban.md` in the Backlog column
4. The weekly "From the Wild" post gets scheduled like any other content piece

This means: **run wild-scan weekly → content-planner schedules the best brief → you build the repo → you write the post → publish.**

---

## Quality Checklist

Run this before delivering results:

- [ ] Minimum 15 real quotes harvested (not paraphrased, not fabricated)
- [ ] Every quote has: exact text, author, platform, community, URL, engagement, context
- [ ] No corporate blog quotes, no marketing content, no course landing pages — real humans only
- [ ] Every quote scored with per-dimension justification (not just a number)
- [ ] Quotes clustered into themes with structural theses (not surface-level groupings)
- [ ] Gold themes (5+ quotes, avg score >= 7) flagged and prioritized
- [ ] Content briefs generated for all themes scoring >= 6
- [ ] Each brief has a repo spec with progressive steps and battle-axe features
- [ ] Repo specs include "why X not Y" decisions (not just "what to build")
- [ ] Brief titles are punchy and specific (not generic)
- [ ] Channel adaptations included for each brief (LinkedIn, blog, Reddit)
- [ ] JSON output validates against `references/output-schema.json`
- [ ] All files saved to correct vault paths
- [ ] No duplicate quotes from previous wild-scan runs (check existing indices)

---

## Resources

### references/

- `output-schema.json` — JSON Schema for the structured wild-scan output
- `scoring-rubric.md` — Detailed calibration guide for the 4 scoring dimensions
- `search-playbook.md` — Search query templates by platform, topic patterns, and pain-language indicators
