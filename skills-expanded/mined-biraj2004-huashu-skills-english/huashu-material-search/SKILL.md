---
name: huashu-material-search
description: Search a personal material library of 1,800+ real experiences and opinions to add a human touch to content. Use when the user mentions "personal experiences", "real examples", "material bank", or "human feel".
---

# Personal Material Library Search

Quickly search Huashu's real experiences, opinions, and case studies to add authenticity and credibility to content creation.

## When to Use This Skill

This skill is automatically loaded when:

- The user says "find my past experiences" or "do I have a related example?"
- An article or script needs real case studies for support
- Content feels too AI-like and needs more human character
- Need genuine reviews of specific tools or products
- Need a personal experience as an opening hook

## Core Features

1. **Fast search**: Search across all Jike posts (1,800+) by keyword
2. **Smart matching**: Automatically match relevant material based on the topic
3. **Rewrite suggestions**: Guidance on how to expand short posts into long-form logic
4. **Authenticity guaranteed**: All material represents Huashu's real expressions

## Material Library Overview

### Data Sources

- **All Jike Posts.csv**: 1,800+ real posts (May–October 2025)
- **My AI Exploration Station Posts.csv**: AI-related posts
- **Curated Thematic Material**: High-quality material organised by theme

### Main Theme Distribution

- **AI coding tools**: 504 entries (Cursor, Claude Code, GitHub Copilot, etc.)
- **Product development**: 200 entries (HarmonyOS development, Kitty Catchlight, automated operations)
- **AI model reviews**: 150 entries (GPT, Claude, DeepSeek, etc.)
- **Social media operations**: 100 entries (growth strategies, content creation)
- **Technical learning**: 80 entries (coding experience, lessons learned)

## Search Methods

### Method A: Search Raw Data Directly (Recommended First) ⭐

**Suitable for**:

- New topics, unorganised themes
- Need the most authentic, unfiltered expressions
- Current affairs commentary, trending topics

**Steps**:

1. **Use Grep tool to search**

```text
pattern: "keyword1|keyword2|keyword3"
path: /Users/alchain/Documents/writing/writing-reference/personal-material-library/all-jike-posts.csv
output_mode: content
-n: true
-i: true  # Case-insensitive
```

1. **Extract core insights**
From the search results, find:

- Huashu's genuine gripes
- Specific observations and attitudes
- Real usage experiences
- Data and results

1. **Rewrite as article material**

- ✅ Expand into long-form logic (short post → complete paragraph)
- ✅ Preserve the authentic tone and candid voice
- ✅ Add background context and detail
- ❌ Do not copy verbatim

**Search examples**:

```text
# Writing about Amap street rankings
pattern: "Amap|street rankings"

# Writing about AI coding tool comparisons
pattern: "Cursor|Claude Code|Copilot|GitHub"

# Writing about product growth strategy
pattern: "growth|conversion|users|retention"

# Writing about technical learning experience
pattern: "learning|mastering|understanding|lessons learned"

# Writing about social media operations
pattern: "WeChat|video|Xiaohongshu|views|readership"
```

**Advantages**:

- Fastest way to find Huashu's real opinions
- Access the most raw, authentic expressions and emotions
- Works for all topics — not limited to curated material
- Can find the most recent posts (latest: October 2025)

---

### Method B: Review Curated Materials

**Suitable for**:

- Common topics (AI coding tools, product development, etc.) that have been systematically organised
- Need complete experience summaries
- Looking for systematic perspectives

**Steps**:

1. **Open the master index**

```text
/writing-reference/personal-material-library/README.md
```

1. **Find the topic**
Open `_jike-topic-index.md` and find the relevant theme:

- AI coding tools? → 504 entries
- Product development? → 200 entries
- AI model reviews? → 150 entries

1. **Select material**
View the extracted file (e.g., `AI-coding-tool-insights.md`)

2. **Rewrite for use**
Follow `_jike-usage-guidelines.md`:

- ✅ Expand into long-form logic
- ✅ Preserve authentic attitude
- ❌ Do not copy verbatim

**Available curated themes**:

- `AI-coding-tool-insights.md`
- `product-development-experience.md`
- `social-media-operations-practice.md`
- `technical-learning-methods.md`

---

## Typical Use Cases

### Scenario 1: Article Opening (Hook with Real Experience)

**Requirement**: Writing "Claude Code In-Depth Review" — need an opening

**Search**:

```text
pattern: "Claude Code"
```

**Material found**:
> "Claude Code's biggest advantage is contextual understanding. When modifying a feature, it knows which files need to be changed."

**Rewrite example**:

```text
Two weeks with Claude Code. The most noticeable change: previously, modifying a feature meant manually checking 5–6 files. Now Claude Code finds them all in one go. That ability is critical — especially when inheriting legacy projects.

Today, let's talk about whether Claude Code is worth it.
```

---

### Scenario 2: Supporting a Point (Genuine Review)

**Requirement**: Writing "AI Coding Tool Selection Guide" — need a real comparison

**Search**:

```text
pattern: "Cursor|Claude Code|comparison"
```

**Material found**:
> "Cursor suits small projects; Claude Code suits large projects. Price is the dealbreaker."

**Rewrite example**:

```text
I used Cursor and Claude Code simultaneously for 3 months. My conclusion:

- Cursor: Good for personal projects and small teams. £15/month — good value for money.
- Claude Code: Better for large projects and complex refactors. £75+/month — more suited to companies.

If you're an individual developer, start with Cursor. If your company covers the expense, go for Claude Code.
```

---

### Scenario 3: Case Study (Real Project)

**Requirement**: Writing "Getting Started with HarmonyOS Development" — need a real project case

**Search**:

```text
pattern: "HarmonyOS"
```

**Material found**:
> "HarmonyOS development's biggest pitfall is incomplete documentation. The official examples don't run."

**Rewrite example**:

```text
I previously developed a HarmonyOS app using Cursor and hit quite a few snags. The biggest problem was incomplete documentation — about 30% of the official examples wouldn't run, and the error messages were vague.

Eventually I discovered the fastest approach is to read the source code directly. HarmonyOS component source code is fairly well-written — more reliable than the documentation.
```

---

### Scenario 4: Closing Thought (Personal Insight)

**Requirement**: Writing "The Value of Programmers in the AI Era" — need an elevated closing

**Search**:

```text
pattern: "AI|replacement|programmer|value"
```

**Material found**:
> "AI can write for me, but it can't think for me. Real value lies in judgement."

**Rewrite example**:

```text
AI can write code for me, but it can't think through why I need to write this code.

Technology will keep getting stronger, but judgement will always be human — choosing the tech stack, deciding what product to build, defining who to serve, and figuring out how to grow. That's something AI can't learn.

A programmer's value has never been the speed of typing code. It's the clarity of knowing what code needs to be written.
```

---

## Rewriting Guidelines

### ✅ Correct Rewriting

1. **Expand context**: Short post → complete paragraph; add time, scene, and reasons
2. **Preserve attitude**: Keep the genuine candour and clear opinions — don't "wash" them into corporate speak
3. **Add detail**: Specific numbers, timelines, operational steps
4. **Natural integration**: Let the material flow into the article without feeling forced

### ❌ Incorrect Rewriting

1. **Copy verbatim**: Pasting the short post as-is
2. **Overpolishing**: Turning "a painful lesson" into "a learning opportunity"
3. **Losing personality**: Softening the candid tone into neutral objectivity
4. **Fabricating detail**: Adding data that wasn't in the original material

### Rewriting Comparison Example

**Original material** (Jike post):
> "Amap's forced pop-up for the National Holiday street ranking feature. Absolutely disgusting. Product manager must have lost the plot."

**❌ Incorrect rewriting** (over-polished):
> "Amap Maps still has room for improvement in user experience, particularly in the design of pop-up features, which could be made more user-friendly."

**✅ Correct rewriting** (preserves attitude, expands detail):
> "Open Amap during the National Holiday and a pop-up forces you into the street ranking activity — you can't dismiss it without tapping 'Join'. I just want to navigate. Why am I being forced to join an activity?

> The design logic here baffles me. What is the user's core need when opening a navigation app? To start navigating quickly — not to join a street ranking. A forced pop-up only creates resentment, and it won't help activity participation rates either. Will someone who was forced to tap 'Join' actually go out and walk the streets?

> The core of product design is respecting user intent — not pushing KPIs on them."

---

## Important Notes

### 1. Authenticity Principle

- ✅ All material is genuine — it cannot be fabricated or exaggerated
- ✅ Data, dates, and tool names must be accurate
- ✅ You cannot attribute someone else's experience to Huashu

### 2. Timeliness Principle

- ✅ Be aware of the time range (May–October 2025)
- ✅ Avoid using outdated information (e.g., "GPT-3.5 is the mainstream option")
- ✅ When referencing product features, verify they still apply

### 3. Rewriting Principle

- ✅ Must rewrite into long-form logic — never copy-paste
- ✅ Preserve Huashu's authentic tone and candid voice
- ✅ Add background, detail, and thought process
- ❌ Do not "wash" into corporate speak or neutral objectivity

### 4. Usage Frequency

- ✅ Use at least 1–2 pieces of genuine material in every article
- ✅ The opening, case studies, and closing are the best positions
- ❌ Don't over-rely — maintain originality

---

## Frequently Asked Questions

### Q1: What if I can't find relevant material?

**A**:

1. Try adjusting keywords (synonyms, related concepts)
2. Broaden the search scope (search for a parent concept)
3. Check the topic index to see if there's a related category
4. If genuinely nothing fits, supplement with searches and analysis without material

### Q2: What if the material doesn't perfectly match the article topic?

**A**:

- Extract the core opinion and attitude rather than the specific content
- Introduce it by analogy ("This reminds me of the time when...")
- Use it as a counterexample or point of contrast

### Q3: How do I know if material is outdated?

**A**:

- Check the time stamp (the CSV includes publication dates)
- For product features, search to verify the current status
- If in doubt, note "back then..." or "in [month]..."

### Q4: Does every article need personal material?

**A**:

- Not mandatory, but strongly recommended
- Genuine material is the most effective way to reduce AI-sounding language
- Use at least 1–2 instances in the opening or case sections

---

## Technical Implementation

### Grep Search Examples

```bash
# Search keywords (supports regex)
grep -i "Cursor\|Claude Code" /Users/alchain/Documents/writing/writing-reference/personal-material-library/all-jike-posts.csv

# Search with line numbers
grep -in "growth\|conversion" /Users/alchain/Documents/writing/writing-reference/personal-material-library/all-jike-posts.csv

# Search with context (3 lines before and after)
grep -i -C 3 "HarmonyOS" /Users/alchain/Documents/writing/writing-reference/personal-material-library/all-jike-posts.csv
```

### Using Grep Tool in Claude Code

```text
Grep tool parameters:
pattern: "keyword1|keyword2"
path: /Users/alchain/Documents/writing/writing-reference/personal-material-library/all-jike-posts.csv
output_mode: content
-n: true
-i: true
-C: 2  # Show context lines
```

---

## Reference Resources

- `/writing-reference/personal-material-library/README.md` — Master index (start here)
- `/writing-reference/personal-material-library/all-jike-posts.csv` — Raw data (1,800+ entries)
- `/writing-reference/personal-material-library/_jike-topic-index.md` — Topic categories
- `/writing-reference/personal-material-library/_jike-usage-guidelines.md` — Rewriting guidelines and examples

---

## Success Examples

- **"Why the Best Content Is Useless"**: Used the MrBeast case material — added authenticity
- **"The Team Burning Billions of Tokens a Month: How They Use Claude Code"**: Used multiple real Claude Code usage experiences — high credibility

---

**Last Updated**: 2025-11-07
**Applicable Projects**: WeChat article writing, video scripting
**Maintained by**: Huashu

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
