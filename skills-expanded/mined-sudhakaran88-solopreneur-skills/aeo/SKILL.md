---
name: aeo
description: When the user wants to win featured snippets, position-zero results, People Also Ask boxes, or optimize for voice search on Google. Also trigger on "AEO", "answer engine optimization", "featured snippet", "position zero", "People Also Ask", "PAA optimization", "voice search SEO", "snippet optimization". For AI search engines (ChatGPT/Perplexity/GEO), see ai-seo. For broader SEO, see seo-audit.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

# AEO — Answer Engine Optimization

You are an answer engine optimization expert helping solopreneurs claim featured snippets and position-zero results — the prime real estate that appears before all organic results.

---

## When to Use This Skill

Trigger this skill when the user wants to:

- Win a featured snippet (paragraph, list, table, or video) on Google
- Appear in People Also Ask (PAA) boxes
- Optimize existing content for position zero
- Improve voice search visibility
- Audit why a competitor holds a snippet they want
- Understand whether chasing a snippet is worth it (CTR trade-off)
- Build a snippet-capture workflow for their blog or content calendar

**Not this skill:** If the goal is to appear in ChatGPT, Perplexity, or Google AI Overviews as a cited source, use `ai-seo`. Featured snippets and AI citations overlap but require distinct strategies.

---

## Context Check

Before advising, confirm:

1. **Do they already rank on page 1?** — Snippets pull from the top 10. If they don't rank yet, snippet optimization is premature; fix ranking first via `seo-audit`.
2. **What query type are they targeting?** — Paragraph/definition, list/steps, table/comparison, or video/how-to.
3. **Do they have an existing page to optimize, or are they creating new content?**
4. **What's their goal?** — Brand visibility, voice search traffic, lead capture, or pure traffic? (This affects whether the CTR trade-off matters.)
5. **Do they have Schema markup in place?** — If not, flag `schema-markup` as a quick parallel win.

---

## Featured Snippet Types and How Google Selects Them

Google serves five primary snippet formats. Each requires a different content structure.

### 1. Paragraph Snippet
- **Triggered by:** "What is," "Who is," "Why does," "How does," definition and explanation queries
- **Format:** 40–60 words of plain prose directly below a question-style H2/H3
- **Selection signal:** Google extracts the clearest, most direct answer from a top-10 page
- **Example query:** "What is content marketing?"

### 2. List Snippet (Ordered & Unordered)
- **Triggered by:** "Steps to," "How to," "Types of," "Best ways to," sequential or categorical queries
- **Format:** `<ol>` or `<ul>` lists with concise, parallel items (aim for 6–8 items; Google truncates at ~8)
- **Selection signal:** Items must be clearly delimited — avoid comma-separated prose lists
- **Example query:** "How to write a cold email"

### 3. Table Snippet
- **Triggered by:** Comparison queries, pricing queries, "X vs Y," data-heavy lookups
- **Format:** Actual HTML `<table>` with clear headers — Google does not convert prose into tables
- **Selection signal:** Tabular data with labeled rows and columns that directly answer a comparison intent
- **Example query:** "Email marketing platform pricing comparison"

### 4. Video Snippet
- **Triggered by:** "How to," tutorial, and demonstration queries — especially procedural tasks
- **Format:** YouTube video with a matching title and chapter timestamps
- **Selection signal:** Video title closely matches the query; timestamps let Google start at the relevant moment
- **Example query:** "How to record a podcast on your phone"

### 5. Accordion / PAA Snippet
- **Triggered by:** Multi-part questions and follow-up questions
- **Format:** FAQ-style content with collapsible Q&A sections; FAQPage schema amplifies eligibility
- **Selection signal:** Short, scannable answers under each question heading

**How Google selects:** Google picks from pages already in the top 10. It favors pages where the answer is easy to extract — meaning the answer is isolated under a matching question heading, written in plain language, not buried in a long paragraph, and from a domain Google has established as authoritative on the topic. Freshness matters: Google re-evaluates snippet holders roughly every 2–4 weeks.

---

## The 4 Tactics to Win Featured Snippets

### Tactic 1: Use Question H2s That Match the Query
Write H2 or H3 headings as exact or near-exact versions of target queries. If someone searches "what is topical authority," your heading should read "What Is Topical Authority?" — not "Understanding Topical Authority in SEO."

**Why it works:** Google maps the heading to the query, then extracts the content immediately beneath it.

### Tactic 2: Give a Direct Answer in the First 2 Sentences
Immediately after the question heading, deliver the answer in 1–2 sentences before expanding. Don't build up to the answer — state it first.

**Template for paragraph snippets:**
```
[Term] is [concise definition in one sentence]. [One sentence of context or importance].
```
Keep the direct answer to 40–60 words. Everything beyond that is supporting content Google won't pull into the snippet box.

### Tactic 3: Format for the Snippet Type the Query Demands
Match your content structure to the query's implicit format expectation:

| Query Type | Structure to Use |
|---|---|
| "What is / Why does" | Short paragraph, 40–60 words |
| "How to / Steps to" | Numbered list with action verbs |
| "Types of / Best X" | Bulleted list, 6–8 items |
| "X vs Y / Pricing" | HTML table with headers |
| "How to [physical task]" | YouTube video + timestamps |

### Tactic 4: Build Supporting Content Around the Answer
Google rewards pages where the snippet answer is part of a comprehensive resource — not a thin page. The 40–60 word answer earns the snippet; the 1,000–2,000 words around it earns the trust to hold it.

Structure: question heading → direct answer → deeper explanation → examples → related questions.

---

## People Also Ask (PAA) Optimization

PAA boxes now appear in over 50% of all Google searches. They expand dynamically — each click surfaces new related questions, creating a fractal keyword opportunity.

### How PAA Works
Google groups semantically related questions around a query and pulls answers from pages it trusts. PAA and featured snippets often share the same source pages — optimize for one and you often win both.

### PAA Strategy for Solopreneurs

**Step 1: Mine PAA questions as a content brief.**
Use AlsoAsked.com or the free PAA results directly in Google to find every question cluster around your topic. These questions are your H2/H3 heading list.

**Step 2: Answer each PAA question in 2–4 sentences.**
Each answer should stand alone — Google extracts it independently. Avoid answers that require reading the previous section to make sense.

**Step 3: Cluster PAA questions onto a single pillar page.**
One page answering 8–12 related questions performs better than 8–12 thin individual pages. This builds topical authority and gives Google more extractable answers per URL.

**Step 4: Use FAQPage schema.**
Wrap PAA-targeted Q&A sections with FAQPage schema. This doesn't guarantee inclusion but signals structure to Google's parser.

**Step 5: Update quarterly.**
PAA refreshes based on real-time query patterns. An answer that wins a PAA box today may be replaced in 60 days. Monitor and refresh.

### What Triggers PAA
- Informational queries (not transactional)
- Questions beginning with: who, what, when, where, why, how, is, can, does, should
- Topics with natural follow-up questions (almost every niche has them)

---

## Table Snippet Strategy

Table snippets are underutilized because most content creators write in paragraphs. This creates an opening for solopreneurs willing to structure data properly.

**When to build a table snippet target:**
- Comparison pages (tool A vs tool B)
- Pricing pages (show competitor pricing ranges)
- "Best X for Y" content (feature matrix)
- Historical or statistical data (growth rates, benchmarks)

**Technical requirements:**
- Use actual HTML `<table>` tags — Markdown tables may not render correctly in all CMS outputs
- Include `<th>` header cells with descriptive labels
- Keep tables scannable: 3–5 columns, labeled rows, no merged cells
- Add a brief paragraph above the table summarizing what it shows (helps Google understand context)

**Pro tip:** Steal table snippet opportunities from competitors who present comparison data as prose. Convert their lists into a table and Google often reassigns the snippet within weeks.

---

## List Snippet Strategy

List snippets are the easiest to win for solopreneurs because how-to and steps content is natural to write.

**Rules for list snippets:**
- Use `<ol>` for sequential steps; `<ul>` for unordered lists
- Start each list item with an action verb ("Choose," "Install," "Configure")
- Keep items to 1–2 lines each — Google truncates long list items
- Aim for 6–8 items; fewer than 4 rarely earns a snippet; more than 10 gets cut off
- Each item should be self-explanatory without requiring the surrounding paragraph

**Common list snippet opportunities:**
- "How to [do X]" — numbered steps
- "Best [tools/practices] for [audience]" — bulleted list
- "Types of [topic]" — category list
- "[Topic] checklist" — checklist format

---

## Voice Search Optimization

Voice search pulls from featured snippets over 80% of the time. Winning a featured snippet is effectively winning voice search. But voice queries have distinct characteristics that require an additional layer of optimization.

### Voice Query Characteristics
- Conversational and longer than typed queries ("What's the best free email marketing tool for beginners?" vs "email marketing tool free")
- Often local intent ("near me," "in [city]")
- Often action-oriented ("How do I...," "Where can I...")
- Read aloud — answers must sound natural when spoken, not stiff or keyword-stuffed

### Voice Optimization Tactics

**Use natural language in answers.** Write answers in second person ("You can do this by...") and avoid jargon. Voice assistants read the snippet aloud — if it sounds robotic, test it by reading it out loud yourself.

**Avoid first-person in snippet-targeted paragraphs.** "I recommend" or "Our tool" in the snippet text makes it sound odd when read by a voice assistant with no context. Stick to objective, third-person or second-person framing.

**Target question-based long-tail keywords.** Voice queries average 7–10 words. Pages optimized for "what is the best free scheduling tool for solopreneurs" will capture voice results that a page targeting "free scheduling tool" cannot.

**Optimize for local voice intent if relevant.** Ensure Google Business Profile is complete and consistent with on-site NAP (name, address, phone). 75% of local searches are predicted to be voice-driven.

**Page speed is non-negotiable.** Voice search results load in an average of 4.6 seconds — 52% faster than regular results. Use Core Web Vitals as your technical floor.

---

## Monitoring and Tracking

### Which Queries Trigger Snippets

Use these methods to find your snippet opportunities:

1. **Google Search Console** — Filter "Search type: Web," sort by impressions, look for queries with question words where your average position is 3–15. These are prime targets.
2. **SEMrush Position Tracking** — Add your domain, then view the "Featured Snippets" tab to see which queries trigger snippets and whether you or a competitor currently holds them.
3. **Ahrefs Organic Keywords** — Filter by "SERP Features: Featured Snippet" to see all queries in your ranking profile where snippets appear.
4. **AlsoAsked.com** — Free tool for mapping PAA question trees around any seed topic.
5. **Google SERP manual checks** — Still the fastest way to confirm whether a snippet exists for a specific query.

### Snippet Monitoring Workflow (Weekly, 15 min)

1. Pull GSC data: queries with impressions drop + keywords containing "what, how, why, best, vs"
2. Check SEMrush Position Tracking → Featured Snippets tab for losses (you held, competitor took)
3. Spot-check top 3 target queries manually in an incognito browser
4. Flag any snippet you lost to a competitor for a content refresh within 2 weeks

### KPIs to Track

| Metric | What It Tells You |
|---|---|
| Snippet ownership count | How many position-zero results you hold |
| CTR for snippet queries | Whether winning the snippet is sending clicks |
| Impressions on snippet queries | Visibility breadth |
| PAA appearances | Topical authority signal |
| Clicks pre/post snippet win | Measures the CTR trade-off |

---

## The Position-Zero Trade-Off

This is the most misunderstood aspect of AEO. Winning a featured snippet does not always mean more traffic.

### The Problem
When your snippet fully answers the query, users get what they need without clicking. Studies show:
- Position 1 CTR without a snippet: ~26%
- Position 1 CTR when a snippet exists: ~20%
- The snippet itself: ~8–9% CTR
- Net result: a snippet can reduce total clicks to your domain if the snippet steals traffic from your own position 1

One analysis documented a 60% traffic drop after winning a snippet for a query where the answer was fully self-contained.

### When Snippets Help
- Query intent is **research/exploratory** — the snippet previews value but doesn't resolve the need
- The answer requires action on your site (e.g., "How do I log in to [your tool]?")
- The snippet increases **brand visibility** — you want recognition, not necessarily the click
- You are **not currently ranking #1** — a snippet win jumps you above position 1 competitors
- Voice search is a priority — snippets are the answer for voice, regardless of click behavior

### When Snippets Hurt
- Query intent is **fully resolved** by a short answer (e.g., "What year was X founded?")
- You already rank #1 and the snippet cannibalizes your existing CTR
- The topic is transactional and you need the click to convert

### The Solopreneur Decision Framework

Before optimizing for a snippet, ask: "If someone reads only this 50-word answer, will they still want to visit my site?" If yes — optimize for it. If no — consider withholding the full answer in the snippet by structuring content so it previews the answer but requires a click to get the full picture.

You can also opt out per page using `<meta name="robots" content="nosnippet">` though this removes you from the running entirely.

---

## Common Mistakes

1. **Targeting snippets before ranking on page 1.** Snippets only pull from top-10 results. If you're on page 2, fix your ranking first.

2. **Writing answers that are too long.** Google extracts 40–60 words for paragraph snippets. A 200-word answer paragraph won't be pulled cleanly. Front-load your answer.

3. **Using first-person language in snippet paragraphs.** "I recommend" and "We believe" are extracted awkwardly for voice search and look unprofessional as standalone snippets.

4. **Using prose where a list or table is expected.** A comma-separated list of steps will not win a list snippet. Use actual HTML list tags.

5. **Neglecting freshness.** Google re-evaluates snippets every 2–4 weeks. Stale data (old stats, outdated pricing) gets replaced by fresher competitors. Refresh your top snippet pages quarterly.

6. **Adding nosnippet tags accidentally.** Some SEO plugins or CMS themes add `max-snippet:0` or `nosnippet` directives. Check your meta tags if snippets aren't appearing despite good optimization.

7. **Optimizing for quantity over quality.** Chasing every potential snippet dilutes focus. Prioritize 10–20 high-value queries where the snippet appears, you rank in the top 10, and a click has business value.

8. **Ignoring the CTR trade-off.** Winning a snippet on a high-traffic, transactional query can hurt conversions. Measure before declaring victory.

---

## Contrarian Takes

**"Featured snippets are dying."** Not accurate, but nuanced. AI Overviews are absorbing some query types that once showed snippets. However, featured snippets still appear for hundreds of millions of queries and are now a direct feed into AI citation engines. Winning a snippet makes you more likely to appear in AI Overviews — they are complementary, not competing.

**"Chasing snippets is a waste for small sites."** Wrong for solopreneurs specifically. Snippets are a rare SEO channel where a 50-page site can outrank a 10,000-page authority domain, because snippet selection is based on answer quality and structure, not domain authority alone.

**"Schema markup guarantees snippets."** Schema helps, but Google pulls snippets from visible content — not schema alone. A page with perfect FAQPage schema but a poorly written answer will lose to a page with no schema and a direct, clean answer.

**"More content is better for snippets."** The opposite is true for the snippet paragraph itself. Brevity and directness win. More supporting content helps you rank and hold the snippet, but the snippet extract itself should be ruthlessly concise.

---

## Quick Wins (Do These First)

For solopreneurs who want results in 30 days:

- [ ] **Identify your top 10 ranking pages** in GSC where you rank positions 3–15 for question queries
- [ ] **Rewrite the opening paragraph** of each page to answer the target query directly in 40–60 words, placed immediately under a question H2
- [ ] **Audit list content** — anywhere you have steps or types written as prose, convert to `<ol>` or `<ul>` HTML lists
- [ ] **Add one comparison table** to your highest-traffic "vs" or "best" page
- [ ] **Check AlsoAsked** for your top 3 topics and add 3–5 PAA-targeted Q&A sections to each pillar page
- [ ] **Set up Position Tracking in SEMrush** (or Ahrefs) with "Featured Snippet" filter on — takes 10 minutes, gives you a live dashboard
- [ ] **Read your snippet answers aloud** — if it sounds odd spoken, rewrite it for voice compatibility
- [ ] **Add FAQPage schema** to any page with explicit Q&A sections

---

## Related Skills

| Skill | When to Use It |
|---|---|
| `seo-audit` | Fix ranking issues before targeting snippets; technical SEO foundation |
| `ai-seo` | Optimize for ChatGPT, Perplexity, and Google AI Overviews citations |
| `schema-markup` | Implement FAQPage, HowTo, and other structured data to amplify AEO |
| `content-strategy` | Plan a content calendar built around PAA clusters and snippet opportunities |
| `site-architecture` | Structure pillar pages and topic clusters that maximize snippet eligibility |

---

*Generated using the aeo skill from Solopreneur Skills*
