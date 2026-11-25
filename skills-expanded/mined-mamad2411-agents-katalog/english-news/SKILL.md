---
name: english-news-skill
description: "English news aggregator fetching from 40+ major sources across Tech, Finance, AI Research, Geopolitics & Policy. Covers FT, Bloomberg, WSJ, Economist, MIT Tech Review, Stratechery, Arxiv, think tanks (CFR, Brookings, RAND), and more. Best for 'morning briefings', 'market updates', 'AI news', 'geopolitics', and 'policy analysis'."
---

# English News Skill

Fetch real-time news from 40+ major English-language sources worldwide.

## Sources

| Category | Sources |
|----------|---------|
| **Tech** | Hacker News, GitHub Trending, Product Hunt, Reddit (r/technology, r/programming), TechCrunch, Ars Technica, The Verge |
| **Global** | BBC News, Reuters, AP News |
| **Finance (Core)** | Financial Times, Wall Street Journal, Bloomberg, Reuters Breakingviews, The Economist |
| **Markets/Trading** | MarketWatch, Barron's, Semafor Business, Axios Markets, FT Alphaville, Yahoo Finance, CNBC, Reddit Stocks |
| **AI/Tech (Serious)** | MIT Technology Review, The Information, Platformer, Stratechery, SemiAnalysis, The Decoder, State of AI |
| **AI Labs & Research** | HuggingFace Blog, OpenAI Blog, Anthropic Blog, DeepMind Blog, Arxiv AI (cs.AI + cs.LG) |
| **Geopolitics & Policy** | Politico, Foreign Affairs, War on the Rocks, CSIS, CFR, Brookings, RAND |
| **Social Media** | Truth Social (Trump) |

## Tools

### fetch_news.py

**Location:** `scripts/fetch_news.py`

**Usage:**

```bash
# Single source
python3 scripts/fetch_news.py --source hackernews --limit 10 --deep

# Source groups
python3 scripts/fetch_news.py --source tech --limit 10 --deep
python3 scripts/fetch_news.py --source global --limit 10 --deep
python3 scripts/fetch_news.py --source finance --limit 10 --deep

# Full scan (all sources)
python3 scripts/fetch_news.py --source all --limit 15 --deep

# Keyword filtering with smart expansion
python3 scripts/fetch_news.py --source tech --keyword "AI,LLM,GPT,Claude,Agent" --deep
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `--source` | Source name, group name, or comma-separated list. Groups: `tech`, `global`, `finance`, `finance_core`, `markets`, `ai_research`, `ai_labs`, `geopolitics`, `policy`, `trump`, `all_finance`, `all_ai`, `all_politics`, `all` |
| `--limit` | Max items per source (default: 10) |
| `--keyword` | Comma-separated keyword filter (case-insensitive) |
| `--deep` | Fetch full article content for deeper analysis |
| `--no-dedup` | Disable deduplication (raw output, backward compatible) |
| `--diff` | Show changes since last run (new/dropped/rank changes) |
| `--format` | Output format: `json` (default), `md`/`markdown`, `slack` |
| `--rank-by` | Ranking strategy: `trending` (social heat), `signals` (credibility), `combined` (default) |

**Individual Sources:**

| Category | Sources |
|----------|---------|
| **Tech** | `hackernews`, `github`, `producthunt`, `reddit_tech`, `reddit_programming`, `techcrunch`, `arstechnica`, `theverge` |
| **Global** | `bbc`, `reuters`, `apnews` |
| **Finance Core** | `ft`, `wsj`, `bloomberg`, `reuters_breakingviews`, `economist` |
| **Markets** | `marketwatch`, `barrons`, `semafor`, `axios_markets`, `ft_alphaville`, `yahoo_finance`, `cnbc`, `reddit_stocks` |
| **AI Research** | `mit_tech_review`, `theinformation`, `platformer`, `stratechery`, `semianalysis`, `thedecoder`, `stateofai` |
| **AI Labs** | `openai_blog`, `anthropic_blog`, `deepmind_blog`, `huggingface`, `arxiv_ai` |
| **Geopolitics** | `politico`, `foreign_affairs`, `warontherocks`, `csis`, `cfr`, `brookings`, `rand` |
| **Social Media** | `truthsocial` |

### Reddit Stocks Tracker (NEW)

Scans r/wallstreetbets, r/stocks, r/investing for the **top 10 most discussed stock tickers**.

```bash
# Get top discussed stocks
python3 scripts/fetch_news.py --source reddit_stocks --limit 10

# Include in finance scan
python3 scripts/fetch_news.py --source finance --limit 10
```

**Output example:**
```json
{
  "title": "$META - Mentioned 15x across r/wallstreetbets, r/stocks",
  "url": "https://finance.yahoo.com/quote/META",
  "heat": "15 mentions",
  "description": "META $90K YOLO + DD",
  "top_post_url": "https://reddit.com/r/wallstreetbets/..."
}
```

## Smart Deduplication (NEW)

Stories are **automatically deduplicated** across sources using:
- URL matching (after stripping tracking params)
- Title fuzzy matching (70% similarity threshold)
- Content hash matching (for `--deep` mode)

**Benefits:**
- Same story from HN + Reddit + BBC = 1 entry with source attribution
- Multi-source coverage = credibility signal (bigger story)
- Ranked by: `(source_count × 100) + normalized_heat + recency_bonus`

**Output format:**
```json
{
  "meta": {
    "fetched_at": "2026-01-25T10:30:00Z",
    "sources_scanned": 40,
    "raw_items": 320,
    "after_dedup": 180,
    "duplicates_merged": 140
  },
  "stories": [
    {
      "title": "DOOM Ported to an Earbud",
      "url": "https://doombuds.com",
      "sources": ["Hacker News", "Reddit r/technology", "The Verge"],
      "source_count": 3,
      "heat": {"hackernews": "227 points", "reddit_tech": "5.2K upvotes"},
      "time": "7 hours ago"
    }
  ]
}
```

## Interactive Menu

When the user invokes this skill without specific instructions, **READ** `templates.md` and **DISPLAY** the menu.

## Smart Keyword Expansion (CRITICAL)

**ALWAYS** expand simple keywords to cover the domain:
- User: "AI" → Agent uses: `--keyword "AI,LLM,GPT,Claude,Gemini,OpenAI,Anthropic,Machine Learning,Neural,Agent"`
- User: "crypto" → Agent uses: `--keyword "crypto,Bitcoin,Ethereum,blockchain,DeFi,Web3"`
- User: "Apple" → Agent uses: `--keyword "Apple,iPhone,Mac,iOS,macOS,iPad,Vision Pro"`

## Response Guidelines (CRITICAL)

### Format & Style
- **Headlines**: English (preserve original)
- **Analysis/Summary**: Simplified Chinese (简体中文)
- **Style**: Magazine/Newsletter style (Morning Brew / The Economist vibe)

### Report Structure
1. **🔥 Top Stories** - Multi-source coverage (3+ sources) - most important
2. **🌍 Global Headlines** - News from BBC, Reuters, AP
3. **🤖 Tech & AI** - Technology, software, AI developments
4. **📈 Markets & Finance** - FT, WSJ, Bloomberg, MarketWatch, Barron's
5. **🧠 AI Research & Labs** - OpenAI, Anthropic, DeepMind, Arxiv papers
6. **🌐 Geopolitics & Policy** - Think tanks (CFR, Brookings, RAND), Foreign Affairs
7. **💡 Developer Insights** - Single-source but high-value items

### Report Header
Always include scan summary at the top:
```markdown
---
📊 **Scan Summary**: 40+ sources • 300+ items fetched • 150 unique stories (duplicates merged)
🔝 **Top Signal**: "Story Title" covered by 4 sources
---
```

### Item Format

**For multi-source stories (3+ sources):**
```markdown
### 1. [Headline Title](https://url.com)
**🔥 Covered by 4 sources**: Hacker News (529 pts) • Reddit (11K) • BBC • The Verge

One-line punchy summary.

- **Why it matters**: Technical details, context
- **Industry impact**: Market or industry implications
- **Keywords**: `#AI #Tech #Finance`
```

**For single-source stories:**
```markdown
### 5. [Headline Title](https://url.com)
**Source**: BBC News | **Time**: 2 hours ago | **Heat**: 500 upvotes

One-line punchy summary.

- **Why it matters**: Technical details, context
- **Keywords**: `#AI #Tech #Finance`
```

### Output Requirements
- **Title MUST be a Markdown link** to the original URL
- **Metadata line** must include Source, Time, and Heat/Score
- **Save report** to `reports/` with timestamped filename (e.g., `reports/tech_news_20260124_0800.md`)

## Time-Based Filtering

If user requests a specific time window (e.g., "past 6 hours"):
1. Prioritize items within the window
2. If sparse (<5 items), include high-value items from wider range
3. Mark supplementary items with ⚠️ or 🔥 annotations

## Example Prompts

| User Says | Action |
|-----------|--------|
| "Morning tech briefing" | Fetch `--source tech --limit 15 --deep`, generate newsletter-style report |
| "What's happening in AI?" | Fetch `--source all_ai --limit 15 --deep` with expanded AI keywords |
| "Global news scan" | Fetch `--source all --limit 10 --deep`, comprehensive report |
| "Market news" | Fetch `--source all_finance --limit 15 --deep` |
| "Premium finance briefing" | Fetch `--source finance_core --limit 15 --deep` (FT, WSJ, Bloomberg, Economist) |
| "AI research updates" | Fetch `--source ai_labs --limit 10 --deep` (OpenAI, Anthropic, DeepMind, Arxiv) |
| "Geopolitics briefing" | Fetch `--source geopolitics --limit 15 --deep` (think tanks + policy) |
| "Trading desk news" | Fetch `--source markets --limit 20 --deep` (MarketWatch, Barron's, etc.) |
| "HN top stories" | Fetch `--source hackernews --limit 20 --deep` |
| "Trump's latest posts" | Fetch `--source truthsocial --limit 10` |
| "Politics + Trump" | Fetch `--source all_politics --limit 15 --deep` (think tanks + Truth Social) |

---

## Headline Generation Guidelines (CRITICAL)

### Chain-of-Thought Process

When rewriting or improving a headline, follow this structured reasoning:

**Step 1: Extract the 5 Ws**
- **Who**: Primary actors/companies/people
- **What**: Core action or event
- **When**: Time relevance (breaking, ongoing, announced)
- **Where**: Geographic or platform context
- **Why**: Significance or motivation

**Step 2: Determine the Angle**
| Angle | When to Use | Example Signal |
|-------|-------------|----------------|
| **Breaking** | Time-sensitive, just happened | "announces", "launches", "just" |
| **Impact** | Major consequences | Market moves, policy changes |
| **Conflict** | Competing interests | Lawsuits, rivalries, debates |
| **Trend** | Pattern or movement | "rise of", "growing", statistics |
| **Surprise** | Unexpected development | Contradicts expectations |

**Step 3: Generate 3 Variations**
1. **Viral/Clicky**: Optimized for shares, curiosity gap
2. **SEO/Searchable**: Keyword-optimized, clear value proposition
3. **AP Style/Factual**: Neutral, objective, traditional journalism

**Step 4: Select Based on Style Setting**

### Headline Style Selector

Use `{{HEADLINE_STYLE}}` variable (defaults to `ap_style`):

| Style | Description | Use When |
|-------|-------------|----------|
| `clicky` | Curiosity gap, emotional hooks | Social media, viral content |
| `ap_style` | Factual, neutral, objective | **Default**, professional reports |
| `seo` | Keyword-optimized, clear value | Blog posts, search-focused |
| `economist` | Witty, sophisticated wordplay | Premium newsletters |

**Examples by Style:**

Original: "Apple announces new MacBook with M4 chip"

| Style | Rewritten Headline |
|-------|-------------------|
| `clicky` | Apple Just Changed Everything About Laptops |
| `ap_style` | Apple Unveils M4-Powered MacBook Lineup |
| `seo` | Apple M4 MacBook 2026: Price, Specs, Release Date |
| `economist` | Chip Off the Old Block: Apple's Silicon Saga Continues |

---

## Banned Words & Phrases (NEGATIVE CONSTRAINTS)

**NEVER use these in headlines or summaries:**

### Hype Words
❌ delve, game-changer, revolutionary, unprecedented, groundbreaking, disruptive, paradigm shift

### Vague Intensifiers
❌ very, really, incredibly, literally, absolutely, extremely, totally

### Clickbait Triggers
❌ you won't believe, shocking, mind-blowing, insane, wild, jaw-dropping, unbelievable

### AI Writing Tells
❌ "in the realm of", "it's worth noting", "it's important to note", "in today's world", "in this day and age", "at the end of the day", "needless to say"

### Filler Phrases
❌ "as we all know", "of course", "obviously", "clearly", "certainly", "undoubtedly"

**Prefer instead:**
- Specific numbers and facts
- Active voice verbs
- Concrete nouns
- Direct statements

---

## A/B Testing Mode

When user requests headline comparison, output in table format:

```markdown
| Version | Headline | Strengths | Weaknesses |
|---------|----------|-----------|------------|
| **Viral** | Apple Just Made Every Other Laptop Look Ancient | High curiosity, emotional | Vague, no specifics |
| **SEO** | Apple M4 MacBook Pro: 18-Hour Battery, 2x Faster | Keywords, scannable | Less engaging |
| **Formal** | Apple Launches MacBook Pro with M4 Processor | Accurate, neutral | Lower click appeal |

**Recommendation**: [SEO] for search visibility while maintaining accuracy.
```

---

## Few-Shot Examples

### Tech Headlines

| Original | Improved (AP Style) |
|----------|---------------------|
| "New AI model is really good at coding" | "Anthropic's Claude Opus 4.5 Matches Human Programmers on SWE-Bench" |
| "Company raises money" | "Stripe Raises $1.2B at $95B Valuation, Largest Fintech Round of 2026" |
| "Big tech layoffs happening" | "Google Cuts 1,200 Jobs in Cloud Division Amid Restructuring" |
| "Cool new open source project" | "Rust-Based Database 'TurboSQL' Hits 10K GitHub Stars in 48 Hours" |
| "Cryptocurrency going up" | "Bitcoin Surges Past $100K as Institutional Inflows Hit Record $2.3B" |

### Global Headlines

| Original | Improved (AP Style) |
|----------|---------------------|
| "Big election news" | "UK Labour Wins 200-Seat Majority in Historic Parliamentary Shift" |
| "Climate change update" | "Antarctic Ice Sheet Loses 2 Trillion Tons in 2025, Fastest Rate on Record" |
| "International conflict" | "EU Imposes Sanctions on 12 Russian Oligarchs Over Ukraine War" |

### Finance Headlines

| Original | Improved (AP Style) |
|----------|---------------------|
| "Fed does something with rates" | "Federal Reserve Holds Rates at 5.25%, Signals Two Cuts by Year-End" |
| "Market is volatile today" | "S&P 500 Swings 3% as Earnings Season Delivers Mixed Results" |
| "Big company earnings" | "NVIDIA Q4 Revenue Beats Estimates by 40%, Data Center Sales Double" |

---

## Bias & Sensationalism Self-Check

Before finalizing any report, verify:

### Balance Checklist
- [ ] Are multiple perspectives represented when applicable?
- [ ] Is the source type disclosed (wire, original reporting, aggregator)?
- [ ] Are claims attributed to specific sources?

### Emotional Language Score (Rate 1-5)
| Score | Description | Action |
|-------|-------------|--------|
| 1-2 | Neutral, factual | ✅ Acceptable |
| 3 | Some emotional words | ⚠️ Review for necessity |
| 4-5 | Heavily emotional | ❌ Rewrite with facts |

**Red Flags to Avoid:**
- Superlatives without evidence ("biggest", "worst", "best ever")
- Loaded adjectives ("controversial", "divisive", "troubled")
- Speculation presented as fact
- Missing context or counterpoints

### Evidence Check
- [ ] Numbers are sourced or verifiable
- [ ] "According to" attributions are specific (not "experts say")
- [ ] Breaking news is marked as developing if unconfirmed

---

## Configuration

User configuration in `config.yaml`:

```yaml
sources:
  enabled: [hackernews, github, bbc, reuters]
  per_source_limits: {hackernews: 15, default: 10}

dedup:
  title_threshold: 0.70
  preserve_alternates: true

output:
  language_mode: "bilingual"  # bilingual | english | chinese
  default_format: "json"      # json | markdown | slack

keyword_presets:
  ai: [AI, LLM, GPT, Claude, Gemini, OpenAI, Anthropic]
  crypto: [crypto, Bitcoin, Ethereum, blockchain, DeFi]
```
