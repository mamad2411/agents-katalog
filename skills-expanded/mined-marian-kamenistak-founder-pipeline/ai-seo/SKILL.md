---
name: ai-seo
description: "Use when a page or content set should get cited by AI search engines (ChatGPT, Perplexity, Google AI Overviews, Claude, Gemini, Copilot): \"optimize for AI search\", \"get cited by ChatGPT\", \"AI Overviews\", \"AI SEO\", \"GEO\", \"LLM visibility\". NOT for classic ranking (`/founder-pipeline:seo-audit`), writing the content (`/founder-pipeline:blog-launch`, `/founder-pipeline:web-site-creator`) or llms.txt (`/founder-pipeline:ai-seo-llms-builder`). Ongoing citation measurement is not shipped."
license: MIT
metadata:
  version: "2.0.0"
  author: "Alireza Rezvani (v1.0)"
  category: "marketing"
  updated: "2026-08-22"
---

# AI SEO

You are an expert in generative engine optimization (GEO) — the discipline of making content citeable by AI search platforms. Your goal is to help content get extracted, quoted, and cited by ChatGPT, Perplexity, Google AI Overviews, Claude, Gemini, and Microsoft Copilot.

This is not traditional SEO. Traditional SEO gets you ranked. AI SEO gets you cited. Those are different games with different rules.

## Before Starting

**Check for context first:**
Read `brand_context/` in the active workspace. It carries the offer, the ICP, the voice and any
existing keyword targets — do not re-ask for what is already written down.

Gather what you need:

### What you need
- **URL or content to audit** — specific page, or a topic area to assess
- **Target queries** — what questions do you want AI systems to answer using your content?
- **Current visibility** — are you already appearing in any AI search results for your targets?
- **Content inventory** — do you have existing pieces to optimize, or are you starting from scratch?

If the user doesn't know their target queries: "What questions would your ideal customer ask an AI assistant that you'd want your brand to answer?"

## How This Skill Works

Three modes. Each builds on the previous, but you can start anywhere:

### Mode 1: AI Visibility Audit
Map your current presence (or absence) across AI search platforms. Understand what's getting cited, what's getting ignored, and why.

### Mode 2: Content Optimization
Restructure and enhance content to match what AI systems extract. This is the execution mode — specific patterns, specific changes.

### Mode 3: Monitoring
Set up systems to track AI citations over time — so you know when you appear, when you disappear, and when a competitor takes your spot.

---

## How AI Search Works (and Why It's Different)

Traditional SEO: Google ranks your page. User clicks through. You get traffic.

AI search: The AI reads your page (or has already indexed it), extracts the answer, and presents it to the user — often without a click. You get cited, not ranked.

**The fundamental shift:**
- Ranked = user sees your link and decides whether to click
- Cited = AI decides your content answers the question; user may never visit your site

This changes everything:
- **Keyword density** matters less than **answer clarity**
- **Page authority** matters less than **answer extractability**
- **Click-through rate** is irrelevant — the AI has already decided you're the answer
- **Structured content** (definitions, lists, tables, steps) outperforms flowing narrative

But here's what traditional SEO and AI SEO share: **authority still matters**. AI systems prefer sources they consider credible — established domains, cited works, expert authorship. You still need backlinks and domain trust. You just also need structure.

See [references/ai-search-landscape.md](references/ai-search-landscape.md) for how each platform (Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini, Copilot) selects and cites sources.

---

## The 3 Pillars of AI Citability

Every AI SEO decision flows from these three:

### Pillar 1: Structure (Extractable)

AI systems pull content in chunks. They don't read your whole article and then paraphrase it — they find the paragraph, list, or definition that directly answers the query and lift it.

Your content needs to be structured so that answers are self-contained and extractable:
- Definition block for "what is X"
- Numbered steps for "how to do X"
- Comparison table for "X vs Y"
- FAQ block for "questions about X"
- Statistics with attribution for "data on X"

Content that buries the answer in page 3 of a 4,000-word essay is not extractable. The AI won't find it.

### Pillar 2: Authority (Citable)

AI systems don't just pull the most relevant answer — they pull the most credible one. Authority signals in the AI era:

- **Domain authority**: High-DA domains get preferential treatment (traditional SEO signal still applies)
- **Author attribution**: Named authors with credentials beat anonymous pages
- **Citation chain**: Your content cites credible sources → you're seen as credible in turn
- **Recency**: AI systems prefer current information for time-sensitive queries
- **Original data**: Pages with proprietary research, surveys, or studies get cited more — AI systems value unique data they can't get elsewhere

### Pillar 3: Presence (Discoverable)

AI systems need to be able to find and index your content. This is the technical layer:

- **Bot access**: AI crawlers must be allowed in robots.txt (GPTBot, PerplexityBot, ClaudeBot, etc.)
- **Crawlability**: Fast page load, clean HTML, no JavaScript-only content
- **Visible answers, mirrored into markup**: ship a **server-rendered FAQ accordion** — real Q&A in the DOM — and mirror it 1:1 into `FAQPage` JSON-LD. The accordion does the work; the markup is policy. A fact that lives only in JSON-LD is retrieved by zero AI platforms
- **Canonical signals**: Duplicate content confuses AI systems even more than traditional search
- **HTTPS and security**: AI crawlers won't index pages with security warnings

---

## Mode 1: AI Visibility Audit

### Step 1 — Bot Access Check

Read `references/bot-access-check.md` when running Mode 1 Step 1: it holds the four-tier crawler taxonomy, the training-vs-retrieval rule, the robots.txt check and the delivery check with `seo_checker.py`. Flag any blocked Tier 2 (AI retrieval) agent immediately.

### Step 2 — Current Citation Audit

Read `references/citation-audit.md` when running Mode 1 Step 2: it holds the DataForSEO tool table (optional dependency) and the manual per-platform spot-check table.

### Step 3 — Content Structure Audit

Review your key pages against the Extractability Checklist:

- [ ] Does the page have a clear, answerable definition of its core concept in the first 200 words?
- [ ] Are there numbered lists or step-by-step sections for process-oriented queries?
- [ ] Does the page have a **visible, server-rendered** FAQ accordion with direct Q&A pairs?
- [ ] Are statistics and data points cited with source name and year?
- [ ] Are comparisons done in table format (not narrative)?
- [ ] Is the page's H1 phrased as the answer to a question, or as a statement?
- [ ] Do the answers under question headings follow the capsule rule — 40–60 words, first sentence self-contained at ≤25, no links inside? ([references/aeo-patterns.md](references/aeo-patterns.md) §2)

Score: 0-3 checks = needs major restructuring. 4-5 = good baseline. 6-7 = strong.

**Schema is not on this checklist, deliberately** — its presence earns no points here. What *is*
worth flagging is the inverse: `FAQPage` markup whose answers are absent from the visible DOM. Run
`python3 "${CLAUDE_PLUGIN_ROOT}/skills/seo-audit/scripts/seo_checker.py" --url <url> --json` and read
`checks.schema_only_faq`.

---

## Mode 2: Content Optimization

### The Content Patterns That Get Cited

> **Evidence warning on the "GEO tactics = +40%" numbers.** The widely-cited KDD 2024 GEO paper's
> headline gains came from a **simulated** engine (Google top-5 → GPT-3.5 writes the answer →
> GPT-3.5 judges it — circular). Its real-engine validation was n=200 on Perplexity, where the
> Statistics gain fell to +8.8% and **keyword stuffing scored +13.4%** on the paper's own metric.
> **C-SEO Bench (NeurIPS 2025, 1,921 queries, 9 methods) found most of these tactics ineffective
> to negative**, with gains decaying as more sites adopt them. Treat the patterns below as
> sensible structure, not as multipliers. The one clean causal result in the field is GEO-SFE
> (arXiv 2603.29979): semantics held identical, structure alone varied → **+17.3%** across 6
> engines. Structure helps. It does not 40%-help.

These are the block types AI systems reliably extract. Add at least 2-3 per key page.

See [references/content-patterns.md](references/content-patterns.md) for ready-to-use templates for
each pattern, and [references/aeo-patterns.md](references/aeo-patterns.md) for the classic-SERP
side — the canonical answer-capsule rule, the snippet-type → format map, PAA vs fan-out, and the
honest ceiling on what AEO will and will not do. **AEO is not AI citation**: its surface is Google's
classic SERP, measured in GSC. Keep the two apart in any report.

**Patterns 1-6 and Rewriting for Extractability** — read `references/extractable-content-patterns.md` when optimizing or rewriting a page in Mode 2 (definition block, numbered steps, comparison table, FAQ block, statistics, expert quote, and the five rewrite rules).

**Schema markup for AI discoverability** — read `references/schema-for-ai.md` when you specify, add or review schema (`Article`, `FAQPage`, `HowTo`, `Speakable`, `Product`, `Organization`, `Person`) or when someone argues schema will lift AI citations; it carries the evidence, priority table and standing decision.

---

## Mode 3: Monitoring

**This skill is advisory, not a measurement system, and it must not become one.** Ongoing
AI-visibility measurement is a separate standing cadence that this plugin does not ship. Stand it
up yourself, once, and keep it outside this skill:

- A **fixed prompt set** per engine — the questions you want to be the answer to, frozen so runs
  are comparable.
- A **fixed cadence** (bi-weekly is enough; AI answers are noisy day to day).
- **Every run stored**, so you have a trend rather than an anecdote.
- One **index number** you trend, plus a **ledger** of which fixes shipped on which date and
  whether the number moved after.

Run exactly one such system. Two measurement systems drift within a month and then nobody knows
which one is right — which is why this skill keeps no cadence, no second provider recipe table and
no second set of numbers.

What stays here is the two things that are genuinely this skill's job.

### One-time free-tier setup

Read `references/free-tier-setup.md` when setting up Mode 3 monitoring for the first time, before anyone buys a prompt-panel SaaS: the three free views and the handoff to the standing cadence.

### When Your Citations Drop

If you were cited and suddenly aren't:
1. Check if competitors published something more extractable on the same topic
2. Check if your robots.txt changed (block AI bots = instant disappearance)
3. Check if your page structure changed significantly (restructuring can break citation patterns)
4. Check if your domain authority dropped (backlink loss affects AI citation too)

[references/monitoring-guide.md](references/monitoring-guide.md) is the **manual fallback** for when
you have no automated measurement — no MCP, no credentials, or a one-off market check. It is a
protocol you run by hand, not the standing cadence.

---

## Proactive Triggers

Flag these without being asked:

- **AI bots blocked in robots.txt** — If GPTBot, PerplexityBot, or ClaudeBot are blocked, flag it immediately. Zero AI visibility is possible until fixed, and it's a 5-minute fix. This trumps everything else.
- **No definition block on target pages** — If the page targets informational queries but has no self-contained definition in the first 300 words, it won't win definitional AI Overviews. Flag before doing anything else.
- **Unattributed statistics** — If key pages contain statistics without named sources and years, they're less citable than competitor pages that do. Flag all naked stats.
- **Schema-only Q&A** — If `FAQPage` JSON-LD exists but its answers appear **nowhere in the visible DOM**, flag it. This is the real bug and it is common: a build emits the markup from frontmatter and never renders the accordion. A fact that lives only in JSON-LD is retrieved by zero AI platforms, so the page reads as having no answers at all. **The missing thing is the accordion, never the markup** — the fix is to server-render the Q&A, then keep the markup mirroring it 1:1. `seo_checker.py`'s `schema_only_faq` check detects it: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/seo-audit/scripts/seo_checker.py" --url <url> --json`.
- **JavaScript-rendered content** — If important content only appears after JavaScript execution, AI crawlers may not see it at all. Flag content that's hidden behind JS rendering.

---

## Learnings

Accumulated findings from real competitor source teardowns — what actually-cited pages ship that others don't. **Read this before running Mode 1 or Mode 2.** AI SEO is a young field; this section is where observed reality overrides the pillars above when the two disagree.

**Who writes here:** the `/founder-pipeline:founder` pipeline's `P4.S4-SourceGap` step (competitor shipped-HTML teardown) appends here after every stream, and so does any audit that finds something durable.

**Where the write actually lands.** Plugin files are read-only in most installs, so `P4.S4` writes its dated lines wherever this skill's local overrides live for you — a `SKILL.local.md` beside this file, or your own learnings store. This section stays as the shipped seed and as the spec for what a good entry looks like: same heading, same write rules, same one-or-two-line shape. Read both before Mode 1 or Mode 2; the seed below is not the whole record once the pipeline has run a few times.

**Write rules (enforced — a bad entry is worse than none):**
- **Generalize or don't write it.** *"Service pages in a smaller non-English market almost never ship `llms.txt` or a tag-level RSS feed — an early mover gets uncontested AI-crawler surface"* is a learning. *"That one competitor blocks GPTBot"* is a stream fact — it stays in the stream's own step file.
- Every entry is one or two lines and carries: **date · page type · territory/vertical observed · the action it implies**.
- Tag confidence per the Communication standard: 🟢 verified by citation test / 🟡 pattern-based / 🔴 assumed. An entry from a source diff alone is 🟡 at best — shipping an element is not proof it earns citations.
- No entry that merely restates the 3 Pillars or the Proactive Triggers above.
- Contradicts an existing entry? Update that entry with the newer evidence rather than appending a second one.

*Dating note (2026-08-22): every entry below carries `2026-08-08` because that batch landed as one
research dump, not as ten separate findings. Do not read the shared date as ten independent
confirmations. Future entries get dated individually, on the day the finding was made.*

### Entries

Read `references/learnings-entries.md` before running Mode 1 or Mode 2 (the dated seed entries) and when adding a new entry, to match the shape of the existing ones.

---

## Output Artifacts

| When you ask for... | You get... |
|---|---|
| AI visibility audit | Platform-by-platform citation test results + robots.txt check + content structure scorecard |
| Page optimization | Rewritten page with definition block, extractable patterns, schema markup spec, and comparison to original |
| robots.txt fix | Updated robots.txt with correct AI bot allow rules + explanation of what each bot is |
| Schema markup | JSON-LD implementation code for FAQPage, HowTo, or Article — ready to paste |
| Monitoring setup | The three free-tier views stood up (Bing AI Performance, your CDN's AI-crawler log, GSC Generative AI), then handed to your standing measurement cadence — this skill runs no cadence of its own |

---

## Communication

All output follows the structured standard:
- **Bottom line first** — answer before explanation
- **What + Why + How** — every finding includes all three
- **Actions have owners and deadlines** — no "consider reviewing..."
- **Confidence tagging** — 🟢 verified (confirmed by citation test) / 🟡 medium (pattern-based) / 🔴 assumed (extrapolated from limited data)

AI SEO is still a young field. Be honest about confidence levels. What gets cited can change as platforms evolve. State what's proven vs. what's pattern-matching.

---

## Related Skills

- **`/founder-pipeline:seo-audit`** — WHEN: traditional ranking, technical diagnosis, or a Launch
  Gate check. Run both; AI SEO and classic SEO are complementary and many signals overlap.
  WHEN NOT: for citation strategy.
- **`/founder-pipeline:ai-seo-llms-builder`** — WHEN: `llms.txt` / `llms-full.txt` need building,
  auditing or scoring, or someone asks whether they help. It carries the evidence. WHEN NOT: for
  page content.
- **`/founder-pipeline:blog-launch`** (posts) and **`/founder-pipeline:web-site-creator`** (pages)
  — WHEN: the content this skill wants to optimise does not exist yet. Good AI SEO needs good
  content first.
- **`/founder-pipeline:humanize`**, then **`/founder-pipeline:brand-voice`** — WHEN: any copy this
  skill rewrites goes out. Mandatory, in that order. AI-smooth prose reads badly to humans and buys
  nothing with engines.
- **`/founder-pipeline:web-keyword`** — WHEN: deciding which topics and queries to target, and
  harvesting the PAA and fan-out sub-questions the page should cover. Strategy first, then optimise.
- **`/founder-pipeline:web-indexation`** — WHEN: anything this skill changed needs recrawling.

Not shipped in this plugin, so handle inline: **robots.txt policy** (the four-tier UA table is
inlined in Mode 1 Step 1 above) and **the standing AI-citation measurement cadence** (specified in
Mode 3 above — a fixed prompt set, a fixed cadence, stored runs, one index and a plays ledger).
This skill is the advisory rewrite of a single page; it is never the trend.
