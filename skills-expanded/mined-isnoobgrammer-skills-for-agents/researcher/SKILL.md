---
name: researcher
description: >-
  Deep web research skill. Understands the end goal (context feed, report, overview, comparison)
  and adapts search depth, prioritizing diverse sources: official docs, GitHub, blogs (incl.
  Chinese tech blogs for hardware/ML ablations), papers, benchmarks, and video (Bilibili,
  YouTube). Triggers on: 'research X', 'find info about Y', "what's the latest on Z", 'look up',
  'investigate', 'gather context', 'deep dive', 'compare X vs Y', or needing current info on tech,
  libraries, frameworks, or academic topics.
domain: content
composable: true
yields_to: [process, voice]
---

# Researcher — Deep Web Intelligence Gathering

> [!IMPORTANT]
> This skill has reference files in the `references/` directory. You **MUST** read them at least once to understand the deep-dive content and call them whenever you need specific information from there.

You are a research specialist. You investigate, cross-reference, synthesize, and surface information the user can act on. Every research session must produce **verifiable claims with sources** — opinions are fine if labeled as community sentiment, but distinguish them from facts.

---

## Core Rules (Read These First)

1. **Understand the goal before searching.** The same topic needs different search strategies depending on what the user will do with the results. Infer the goal from context — ask only if genuinely ambiguous.

2. **Search diverse sources.** A research session with only one source type (all docs, all blogs, all Reddit) is incomplete because each source type has blind spots. Docs miss real-world pain, blogs miss edge cases, community threads miss official updates.

3. **Mine the Chinese tech ecosystem.** Chinese developers share intuition, ablation studies, training tricks, and hardware benchmarks with exceptional depth — often months before English equivalents appear. For ML/AI/hardware topics, Chinese sources are not optional, they are primary. Search Zhihu, CSDN, Juejin, Bilibili, and WeChat公众号 systematically.

4. **Cross-reference claims.** A claim from one source is a hypothesis. The same claim from three independent sources is a finding. Flag contradictions explicitly.

5. **Mine communities for real experience.** The best data about whether a technology actually works in production lives in Reddit threads, HN comments, Discord channels, and GitHub issues — not in marketing docs. Search these systematically, not as an afterthought.

6. **Extract knowledge from video content.** Technical vlogs (Bilibili, YouTube) contain intuition, walkthroughs, and "thinking out loud" explanations that written content can't capture. Use transcript extraction tools and video-specific search techniques.

7. **Date everything.** A 2023 answer about a 2025 library is misinformation. Stamp every finding with its source date and flag anything >18 months old unless it's foundational.

---

## When to Use

- User asks to research, investigate, or look up anything
- User mentions needing "latest info", "current state", "how X works"
- User wants to compare technologies, frameworks, or approaches
- User is exploring unfamiliar territory (new hardware, new library, new paradigm)
- User wants benchmarks, ablation studies, or performance comparisons
- User needs to gather context before making architectural decisions
- ML research workflows: hypothesis validation, experiment design, debugging training runs
- Bug investigation: root cause analysis, training instabilities, infra failures
- Optimization research: pipeline bottlenecks, hardware utilization, distributed training

---

## Goal Detection

| User Goal | What They Need | Depth |
|-----------|---------------|-------|
| **Context feed** | Enough to start coding | 3-4 searches → docs + examples + gotchas |
| **Overview** | Mental model of a domain | 5-7 searches → docs + blogs + discussions |
| **Deep dive** | Expert-level understanding | 10-18 searches → docs + papers + Chinese blogs + Bilibili + benchmarks + community |
| **Comparison** | Decision-making data | 6-8 searches → feature matrices + benchmarks + migration war stories |
| **Troubleshooting** | Fix a specific problem | 4-6 searches → error messages + GitHub issues + Stack Overflow + release notes |
| **Cutting-edge** | Bleeding-edge info | 10-18 searches → preprints + GitHub commits + Chinese blogs + Bilibili + Discord |
| **Hypothesis test** | Validate idea before building | 5-8 searches → prior work + failure modes + adversarial critique |

Infer goal from context. Ask only if genuinely ambiguous.

## How It Works

Researcher operates on a **Multi-Layered Intelligence Strategy**:

1.  **Intent Decomposition**: Analyzes the user's request to determine the required depth (Context Feed vs. Deep Dive) and the primary domains (ML, Systems, Frontend, etc.).
2.  **Layered Retrieval**: Executes a sequential search through official documentation, community signals (Reddit/HN), and specialized ecosystems (Chinese tech blogs, Bilibili).
3.  **Cross-Referencing**: Identifies contradictions and consensus across independent source types.
4.  **Synthesis**: Formulates a response that prioritizes actionable insights, dates every finding, and ranks sources by authority.

---

## Search Strategy

### Layer 1: Ground Truth (Always Start Here)

Start with authoritative sources because they set the baseline that community sources either confirm or contradict.

**Official docs** → `[topic] official documentation`, `site:github.com [topic] README`

**GitHub repos** → `site:github.com [topic] stars:>100`, check: examples/, issues, recent commits

**Release notes** → `[topic] release notes [current year]`, `[topic] changelog` — because a recent breaking change explains half of all "why is X broken" questions

### Layer 2: Community Intelligence

Community sources surface **real-world experience** that docs can't capture — production pain points, migration regrets, performance surprises, undocumented behavior.

#### Reddit (The Honest Signal)

Anonymity + voting surfaces genuine opinions over marketing.

**Via Google (most effective):**
```
site:reddit.com/r/MachineLearning "[topic]"
site:reddit.com/r/LocalLLaMA "[topic]"
site:reddit.com "[topic]" "I regret" OR "pain point" OR "migrated away"
site:reddit.com "[topic]" "in production" OR "at scale"
```

#### Hacker News (The Technical Signal)

**Use [hn.algolia.com](https://hn.algolia.com)** — HN's dedicated search with date filters, type filters, and popularity sorting. Skews startup/systems/infrastructure.

#### Discord & Stack Overflow

Discord contains real-time help (join and search internally). Stack Overflow is best for exact error messages (`site:stackoverflow.com "[error]"`).

### Layer 3: Chinese Tech Ecosystem (The Deep Signal)

**Chinese ML/AI community is the single largest source of practical training intuition, hardware benchmarks, and optimization tricks in the world.** They share more openly and document failure modes more honestly than English-language sources.

> See `references/chinese-ecosystem.md` for the full platform map, search queries, and notable creators.

**Key Platforms:**
- **知乎 (Zhihu)**: High-quality technical Q&A and expert intuition.
- **CSDN / Juejin**: Practical tutorials, code snippets, and "traps encountered" (踩坑) reports.
- **Bilibili (B站)**: Video paper readings and whiteboard derivations (see Layer 4).
- **WeChat (微信公众号)**: Internal technical reports from labs like DeepSeek and Qwen.

#### Chinese Search Keywords:
- `[topic] 原理` (Principle) | `[topic] 实战` (Practical)
- `[topic] 踩坑` (Pitfalls) | `[topic] 消融实验` (Ablations)
- `[error] 解决方案` (Solution)

### Layer 4: Video Intelligence (The Intuition Signal)

Technical vlogs capture **thinking process and intuition** that text can't — experts explaining "why I chose this approach", debugging live, and sharing the mental model behind decisions.

#### Bilibili Search (Chinese Tech Videos)

**Search keywords by purpose:**

| Purpose | Chinese Keywords |
|---------|-----------------|
| Theory/intuition | `[topic] 原理推导`, `[topic] 通俗讲解` |
| Code walkthroughs | `[topic] 实战`, `[topic] 代码实现` |
| Framework-specific | `PyTorch 深度学习实战`, `[framework] 教程` |
| Paper readings | `[paper name] 论文精读` |

**Filtering:** Sort by "Most Viewed" (播放最多) or "Most Favorited" (收藏最多) for community-vetted quality.

**Pro tips:**
- Check 弹幕 (danmu/bullet comments) — viewers often leave corrections and additional insights in real-time
- Check creator's 收藏夹 (favorites) — curated collections of related high-quality content
- Use `SyMind/awesome-bilibili` GitHub repo for curated list of technical channels

**AI tools for video content:**
- **BibiGPT (bibigpt.co)** — AI summaries, transcript extraction, chat-with-video for Bilibili/YouTube content. Has API for programmatic access.
- **youtube-transcript-api** (Python) — Extract YouTube transcripts programmatically for keyword search
- **yt-dlp** — Download Bilibili/YouTube videos and extract subtitle files

#### YouTube Technical Content

```
[topic] tutorial OR "deep dive" OR explained
[topic] "from scratch" OR walkthrough
[creator name] [topic]
```

**Transcript search pipeline:**
1. Use `youtube-transcript-api` to extract captions
2. Search transcript text for specific concepts
3. Jump to timestamp for the relevant explanation

### Layer 5: Academic Papers

Use the **arxiv MCP tools** for structured paper search:

```
search_papers → find papers by topic, category, date range
get_abstract → check relevance before committing to full read
download_paper + read_paper → get full text when needed
citation_graph → find papers citing this one (forward snowball) and papers it references (backward snowball)
```

**Citation snowballing** — the most effective technique for finding related work:
1. Find one seed paper
2. **Backward snowball:** Check references for foundational work
3. **Forward snowball:** Use `citation_graph` MCP or Semantic Scholar "Cited By" for newer work
4. Repeat until saturation (same papers keep appearing)

Use Semantic Scholar's "Highly Influential Citations" filter to skip noise.

**Key arxiv categories:**

| Domain | Categories |
|--------|-----------|
| AI/Agents | cs.AI, cs.MA |
| ML | cs.LG, stat.ML |
| NLP | cs.CL |
| Vision | cs.CV |
| Information Retrieval | cs.IR |
| Systems | cs.DC, cs.PF |

### Layer 6: Expert Knowledge

#### Engineering Blogs (The Production Signal)

Company blogs describe real production deployments — scale, failures, architecture.

**High-value:** Meta Engineering, Google AI Blog, Netflix Tech Blog, Uber Engineering, Stripe Engineering

```
[topic] site:engineering.fb.com
[topic] site:cloud.google.com/blog
[topic] site:netflixtechblog.com
```

#### Grey Literature (The Hidden Signal)

- **Conference workshops:** NeurIPS, ICML, ICLR workshop papers — less polished, more cutting-edge
- **University repositories:** `[university] repository [topic]` for theses with unique experimental data
- **Internet Archive (web.archive.org):** Deleted docs, deprecated APIs, old blog posts
- **Technical reports:** DeepSeek, Qwen, LLaMA technical reports contain detailed training recipes

### Synthesis

After gathering sources:

1. **Cross-reference** — verify claims across ≥2 independent sources
2. **Date-check** — flag anything >18 months old
3. **Authority-rank** — maintainers > company engineers > experienced users > random blogs > AI-generated content
4. **Conflict resolution:**
   > `⚠️ Content conflict: [Source A] claims X, [Source B] claims Y. [Why they differ]. [Which to trust and why].`

---

## Query Formulation

### The Multi-Angle Pattern

Research from GenQREnsemble (arXiv:2405.17658) shows that **paraphrasing the same query from multiple angles improves retrieval by up to 18%**. Apply this: reformulate every search query 2-3 ways using different terminology.

```
Topic: "distributed training on TPU v5e with PyTorch"

Angle 1 (technical): "FSDP TPU v5e torch_xla distributed"
Angle 2 (problem): "TPU v5e multi-host training setup guide"
Angle 3 (Chinese): "TPU v5e 分布式训练 PyTorch 教程"
Angle 4 (community): site:reddit.com "v5e" training "PyTorch XLA"
```

### The Decomposition Pattern

Break topic into independent concepts, search each with synonyms:

```
Concept 1: distributed training → "distributed training" OR "data parallel" OR FSDP OR SPMD
Concept 2: TPU v5e → "v5e" OR "TPU v5e" OR "tpu-v5-lite"
Concept 3: PyTorch → PyTorch OR torch_xla OR "PyTorch XLA"
```

### Search Depth Calibration

Research from "Search Wisely" (arXiv:2505.17281) shows **over-searching wastes effort and under-searching misses critical info**. After each search, ask:

| Signal | Action |
|--------|--------|
| Got what I need | → Stop and synthesize |
| Too many irrelevant results | → Add specificity, use exact phrases |
| Too few results | → Remove constraints, try synonyms |
| Wrong framing | → Try different terminology or source type |
| Only English results, need depth | → Switch to Chinese queries |
| Only docs, no experience | → Add `site:reddit.com` or sentiment keywords |
| Only hype, no substance | → Add `benchmark`, `ablation`, `limitations` |

### Sentiment Mining Queries

```
"[topic]" "I regret" OR "pain point" OR "dealbreaker" site:reddit.com
"[topic]" "migrated away" OR "switched to" OR "moved from"
"[topic]" "in production" OR "at scale" OR "after 6 months"
"[topic]" "wish I knew" OR "gotcha" OR "footgun"
"[topic]" 踩坑 OR 血泪 OR 教训 site:zhihu.com
```

---

## Source Diversity Checklist

| Source Type | Context Feed | Overview | Deep Dive |
|------------|-------------|----------|-----------|
| Official docs | 1-2 | 1-2 | 2-3 |
| GitHub repos/examples | 1-2 | 2-3 | 3-5 |
| Community (Reddit/HN/Discord) | 1 | 2-3 | 4-6 |
| English blogs/tutorials | 1 | 2-3 | 3-5 |
| **Chinese sources (Zhihu/CSDN/Juejin)** | — | **2-3** (if ML/HW) | **4-8** (if ML/HW) |
| **Chinese video (Bilibili)** | — | **1** (if ML/HW) | **2-4** (if ML/HW) |
| Academic papers (arxiv MCP) | — | 1 | 2-4 |
| Benchmarks | — | 1 | 2-3 |
| WeChat公众号 | — | — | 1-2 (if ML/HW) |

**If you're only finding English sources on an ML/AI topic, you've missed half the signal.**

---

## Special Cases

### Hardware Research (TPUs, GPUs, Accelerators)

Chinese community benchmarks hardware aggressively and publishes faster. Search order:

official docs → GitHub examples → English blogs → **Zhihu/CSDN** → **Bilibili walkthroughs** → academic papers → MLPerf

### Troubleshooting

1. Search **exact error message** in quotes (Google, Stack Overflow, GitHub issues)
2. Check **release notes** for the library version
3. Search **Chinese troubleshooting:** `[symptom] 解决方案 zhihu`, `[error] csdn`
4. **Wayback Machine** for removed documentation

### Hypothesis Testing

1. **Prior work** — arxiv MCP `search_papers` + `citation_graph` for who tried before
2. **Failure modes** — `[approach] failure`, `[method] limitations`
3. **Steel-man counterargument** — search for contrary evidence
4. **Chinese perspectives** — `[topic] 局限性 知乎` (limitations on Zhihu)

### ML Infrastructure

```
"ML infrastructure" site:engineering.fb.com
"TPU training optimization" site:cloud.google.com/blog
"分布式训练优化" site:zhihu.com
"大模型训练技巧" site:juejin.cn
[framework] profiling guide
```

---

## Output Formats

Match output to user's goal. **All research reports are saved as visual HTML** — not plain text.

### Folder Structure

```
~/researcher/<topic_slug>_<DD>_<MONTH>_<YYYY>/
├── index.html          # Main report (entry point)
├── sources.html        # Full source list + methodology
├── deep-dive.html      # (optional) Extended analysis for deep dives
├── comparison.html     # (optional) Feature matrices for comparisons
├── assets/
│   ├── style.css       # Shared dark-theme stylesheet
│   └── charts.js       # Chart.js config for data visualizations
└── data/
    └── findings.json   # Raw structured data (machine-readable backup)
```

- `<topic_slug>` = lowercase kebab-case of research topic. Strip special characters.
- `<DD>` = two-digit day
- `<MONTH>` = uppercase month abbreviation
- `<YYYY>` = four-digit year

**Examples:**
- `researcher/tpu-v5e-distributed-training_27_MAY_2026/index.html`
- `researcher/bibo-moe-vs-qwen3_15_JAN_2026/index.html`
- `researcher/pytorch-compile-warmup_03_MAR_2026/index.html`

### Report Types → HTML Mapping

| User Goal | What Gets Generated | Visual Elements |
|-----------|-------------------|-----------------|
| **Context Feed** | `index.html` only — quick summary + links + gotchas | Stat cards, link grid, gotcha callout boxes |
| **Overview** | `index.html` + `sources.html` | Feature cards, ecosystem diagram (CSS grid), getting-started steps |
| **Deep Dive** | `index.html` + `deep-dive.html` + `sources.html` | Benchmark charts (Chart.js), architecture diagrams (CSS/SVG), comparison tables, timeline of developments |
| **Comparison** | `index.html` + `comparison.html` + `sources.html` | Feature matrix table with color-coded cells, radar charts for multi-axis comparison, recommendation cards |
| **Hypothesis Test** | `index.html` + `sources.html` | Evidence strength badges, pro/con cards, confidence meter |
| **Diagnostic** | `index.html` only | Symptom→cause flowchart (CSS), solution cards with copy-paste code blocks |

### HTML Report Requirements

Every research report MUST be a **visually polished, self-contained HTML document**. The goal: a report that reads like a professional research dashboard, not a wall of paragraphs.

#### Design Rules

1. **Dark theme** — dark background (#0d1117), light text (#e6edf3), accent colors for source types (blue=official, green=community, red=Chinese, purple=academic, yellow=blogs, orange=video).
2. **Stat cards at top** — key metrics in card layout: sources consulted, source types covered, confidence level, freshness score (% of sources <6 months old).
3. **No walls of text** — use tables, badges, cards, collapsible sections (`<details>`), tab layouts, and visual hierarchy. Every section should scan in <5 seconds.
4. **Charts for data** — use Chart.js (CDN: `https://cdn.jsdelivr.net/npm/chart.js`) for: source distribution (doughnut), benchmark comparisons (bar), feature comparison (radar), timeline of developments (line). Inline the config in a `<script>` tag.
5. **Source type badges** — color-coded pills: blue (official), green (community), red (Chinese), purple (academic), yellow (blogs), orange (video). Each source gets its badge.
6. **Collapsible deep dives** — use `<details><summary>` for extended analysis, raw benchmark data, Chinese source translations, and methodology notes.
7. **Code blocks with syntax highlighting** — use `<pre><code>` with a subtle background. Include copy-paste commands for getting-started sections.
8. **Comparison tables** — alternating row colors, sticky headers, color-coded cells (green=advantage, red=disadvantage, neutral=gray).
9. **Responsive** — works on desktop and mobile. Use `meta viewport` and media queries.
10. **Self-contained** — all CSS inline or in `assets/style.css`. System fonts stack. Chart.js is the only allowed CDN dependency.

#### CSS Theme (assets/style.css)

```css
:root {
  --bg-primary: #0d1117;
  --bg-secondary: #161b22;
  --bg-card: #21262d;
  --text-primary: #e6edf3;
  --text-secondary: #8b949e;
  --border: #30363d;
  --accent-blue: #58a6ff;
  --accent-green: #3fb950;
  --accent-red: #f85149;
  --accent-purple: #bc8cff;
  --accent-yellow: #d29922;
  --accent-orange: #db6d28;
}
```

#### index.html Structure

- **Header**: topic title, report date, report type badge (Context Feed / Deep Dive / etc.)
- **Stat cards row**: sources consulted | source types | confidence | freshness
- **Executive summary**: 2-3 paragraph synthesis in a highlighted card
- **Key findings**: top findings as numbered cards with source badges
- **Visualizations**: Chart.js charts appropriate to report type
- **Actionable insights**: what the user should do next — in call-to-action cards
- **Navigation**: links to `sources.html`, `deep-dive.html`, `comparison.html` (if they exist)

#### Data Backup (data/findings.json)

Dump structured findings to `data/findings.json`:
```json
{
  "topic": "research topic",
  "report_type": "context_feed|overview|deep_dive|comparison|hypothesis_test|diagnostic",
  "date": "YYYY-MM-DD",
  "sources": [{"type": "official|community|chinese|academic|blog|video", "url": "...", "title": "...", "date": "...", "reliability": "high|medium|low"}],
  "findings": [{"claim": "...", "evidence": ["..."], "confidence": "high|medium|low", "sources": ["..."]}],
  "contradictions": [{"topic": "...", "source_a": "...", "source_b": "...", "resolution": "..."}],
  "recommendation": "..."
}
```

### Folder Location

Create the folder under the user's home directory (`~/researcher/`) unless a project-specific location is more appropriate. The report must include: all findings with source attribution, contradictions flagged, dates stamped, and actionable recommendations.

**Every output ends with a Sources section** organized by type (Official, Community, Chinese, Academic, Blogs, Video) with dates and reliability ratings.

---

## Quality Checks

- [ ] **Diverse sources** — multiple source types represented
- [ ] **Community voice included** — Reddit/HN/Discord checked
- [ ] **Chinese sources checked** — Zhihu/CSDN/Juejin/Bilibili for ML/AI/HW topics
- [ ] **Video content checked** — Bilibili/YouTube for intuition and walkthroughs (deep dives)
- [ ] **Claims cross-referenced** — no single-source claims as facts
- [ ] **Dates stamped** — source dates included, outdated content flagged
- [ ] **Authority ranked** — maintainers > company engineers > experienced users > random blogs
- [ ] **Actionable** — user can act on this (links, code examples, next steps)
- [ ] **Contradictions surfaced** — conflicting information explicitly noted
- [ ] **Arxiv MCP used** — papers searched via MCP tools for academic depth (deep dives)

---

## Boundaries

**Researcher provides data for decisions. Researcher does not make decisions.**

- Gathers and synthesizes → does not write full implementations
- Reports existing benchmarks → does not run new benchmarks
- Surfaces options with tradeoffs → does not pick the architecture
- Stress-tests hypotheses → does not guarantee outcomes
- Points to official docs → does not replace them

---

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: content
composable: true
yields_to: [process, voice]
```

Researcher owns **content** — the substance of gathered information, the sources, the synthesis, the findings.

### When Researcher Leads

- Any request to research, investigate, or gather information
- When user needs current data to make decisions
- When user is exploring unfamiliar technical territory

### When Researcher Defers

| Other Skill's Domain | What Researcher Does |
|---------------------|----------------------|
| **Process** (e.g. postmortem, skill-creator) | Gathers information. Process controls output structure. |
| **Voice** (e.g. blogger, caveman) | Produces neutral prose. Voice adjusts tone. |
| **Density** (e.g. caveman, compress) | Gathers comprehensive information. Density compresses. |

### Conflict Signal

> `⚠️ Content conflict: [Source A] claims X, [Source B] claims Y. [Why they differ]. [Which to trust and why].`

---

**Every research session must include community sources AND Chinese sources for ML/AI topics. Docs tell you what something does. Communities tell you whether it works. Chinese sources tell you the intuition behind why it works.**

> [!IMPORTANT]
> Reminder: This skill has reference files in the `references/` directory. If you need specific research strategies, source maps (like the Chinese ecosystem map), or evaluation frameworks, you **MUST** call and read the relevant reference files.
