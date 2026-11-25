---
name: ai-news-fetcher
description: "Fetches and summarizes the latest AI news from across the internet — including tech blogs, research outlets, newsletters, and news sites — then renders a polished interactive digest as a React artifact in chat. Trigger this skill whenever the user asks about recent or latest AI news, developments, breakthroughs, releases, or anything like \"what's new in AI\", \"AI news this week\", \"catch me up on AI\", \"latest AI updates\", or specifies a time window like \"AI news in the last 3 days / week / month\". Also trigger for queries like \"what happened in AI recently\", \"any new model releases\", \"AI headlines\", \"AI recap\", or \"AI digest\". Always use this skill when the user wants a digest, roundup, or summary of AI happenings over a time period."
---

---
name: ai-news-fetcher
description: "Fetches and summarizes recent AI news from tech outlets, research sources, and newsletters, pulls trending AI GitHub repos, and renders an interactive React artifact in chat. Trigger when the user asks about latest AI news, recent AI developments, model releases, AI digest/recap/roundup, trending AI repos, or specifies a window like 'AI news this week / last 3 days / past month'."
---

# AI News Fetcher

## Purpose
Produce a polished, interactive **React JSX artifact** summarizing recent AI news and trending repos. Always an artifact — never plain markdown.

**Output language:** match the user's language. If unclear, default to English.

**Output file:** `/mnt/user-data/outputs/ai-news-digest.jsx` → present via `present_files` when done.

---

## Workflow

### 1. Parse the time window
Default to **7 days** if unspecified. Build `[DATE_Q]` from the *actual* current date — never use the literal word "today" in a query, since most search backends don't resolve it.

- ≤ 2 days → explicit date (e.g., `April 17 2026`)
- 3–10 days → `this week April 2026`
- 11–30 days → `April 2026`
- > 30 days → `March April 2026`

Compute `[DAYS]` as the numeric window. Story-count target: ~1 story per day of window, capped at 20.

### 2. News research

**Run the first 3–4 broad queries in parallel** (single tool turn, no dependencies between them). Then run 1–3 adaptive follow-ups based on coverage gaps.

Cover these angles across all queries — order and exact phrasing flexible:
- Broad catch-all: `AI news [DATE_Q]`
- Model releases / research: `AI model release [DATE_Q]`, `AI paper breakthrough [DATE_Q]`
- Money: `AI funding OR acquisition [DATE_Q]`
- Policy & safety: `AI regulation OR safety [DATE_Q]`
- Tools & products: `AI product launch [DATE_Q]`

After the parallel batch, scan for gaps (no open-source coverage? no China AI? no chips?) and run targeted follow-ups.

**Snippet mining:**
- Extract from snippets alone: headline, date, entity names, concrete numbers (funding $, benchmarks, params, users), source name, URL.
- Don't fetch if the snippet already has headline + date + 1–2 concrete facts.
- Note overlapping coverage — same story across sources gets merged later.

### 3. Depth fetches — up to 5 articles

Fetch only when payoff is high:
- **Should fetch:** editor-pick caliber story with vague snippet (no numbers, no timeline) — *and* if the snippet references an official announcement (company blog, model card, arXiv), prefer fetching that primary source over secondary coverage.
- **Should fetch:** snippets conflict and need reconciliation.
- **Skip:** snippet already concrete; story is low-impact; you have 3+ details already.

**Source quality (for depth fetches):**
- **Prefer:** Official company blogs, arXiv papers, government sites, and primary sources. Well-established tech and business outlets with strong editorial standards.
- **Snippet only, never fetch:** Personal blogs, forums, social media posts, and unknown outlets.
- **Rule of thumb:** When multiple sources cover the same story, always prefer the primary source (e.g., fetch the company's official blog post rather than a secondary news summary of it).
**Fetch failure handling:** If a fetch returns a paywall stub, login wall, or <300 chars of usable text, fall back to the snippet and do not retry that URL. If the story is critical and another source covers it, fetch that instead (counts toward the 5 budget).

While fetching, also harvest: stat-card-worthy numbers, links to official primary sources, named quotes.

### 4. GitHub trending repos

**4a.** Search: `trending AI GitHub repos [DATE_Q]`. If <3 viable repos, run one fallback: `most starred AI GitHub [DATE_Q]`.

**4b. Fetch strategy:**
- `github.com/trending` (or `/trending/python`, `/trending?since=weekly`) is server-rendered and reliable — fetch it if it appears in results. Note: the actual labels on this page are **"stars today"** and **"stars this month"** (with `?since=` filter), *not* "stars this week" — use whichever label the page shows.
- Curated AI repo roundup articles are also good fetch targets for structured repo data.
- These count toward the 5-fetch budget.

**4c. Include a repo if ≥ 2 of:**
- Appears on a trending page or gained substantial stars in window
- Cited by name in newsletters/articles
- Clear AI/ML relevance (not tangential)
- Practical use (not toy/demo)
- Created or majorly updated in window

**4d. Per repo capture:** `{ name, description, stars, starsGained?, starsGainedLabel?, language, url, whyTrending, category }` where `category ∈ Agent | Model | Tool | Framework | Dataset | Other`. `starsGainedLabel` is the literal label from the source ("today", "this month", etc.) so the UI shows accurate context.

**Aim for 4–8 repos.** Omit the section only if you confirm 0–1.

### 5. Filter, dedupe, cluster

**5a. Date requirement:** every story must have a date resolvable to a specific calendar day (from snippet metadata or fetched article). Relative phrases like "recently" or "this week" without a concrete publish date are **not acceptable** — exclude the story.

At least 50% of final stories must fall inside the user's window. Stories slightly outside (e.g., 8 days old in a 7-day window) are OK only if high-impact with in-window follow-up.

**5b. Deduping (one event = one story):**
Merge when sources cover the same event. Sameness signals: same entity + same event type, same dollar/benchmark figure, same date ±1 day.

When merging: pick the most specific title, combine facts, keep all source URLs (up to 3) in `sources`, use the earliest date.

**5c. Story count targets:**
- 1–3 day window: 5–8 stories
- 4–10 day window: 8–14 stories
- 11–30 day window: 12–20 stories

Don't pad with weak or out-of-window stories to hit the target.

### 6. Categorize & rank

**6a. Exactly one category per story:**
- **Safety** — incidents, alignment, red-team results, bias audits
- **Research & Models** — model releases, benchmarks, architectures, training, papers
- **Industry** — funding, M&A, revenue, hiring, partnerships, chips/hardware
- **Policy** — legislation, regulation, EOs, court rulings, governance
- **Tools & Products** — consumer launches, API updates, IDE plugins, enterprise tools

**6b. Editor picks:** mark 2–4 stories `editorPick: true` if you have ≥4 stories. Criteria: breadth of impact, first-of-kind, multi-source coverage. Never <2, never >4.

**6c. Sort:** stories newest first; repos by `starsGained` desc (fall back to `stars` desc).

### 7. Stat cards — 3–5, real numbers only

Extract concrete metrics from fetched/snippet content. Good candidates: $ amounts, percentages, counts (params, users, stars), performance scores.

Format: `{ label, value, subtitle }` — short noun phrase, number with unit, 3–6 word context.

Rules:
- **Never invent numbers.** Omit cards you can't ground.
- Diversify — don't show 3 funding amounts.
- If you can ground only 0–2 stats, omit the section entirely.

### 8. Week-in-Review

3–5 sentences of editorial synthesis with a thesis — not a summary. Answer: *what's the through-line, where is the field heading, what tension does this period reveal?* Confident plain language, no hedging.

---

## Data schema

Hardcode `DIGEST_DATA` into the artifact. Shape:

```
{
  dateRange: string,
  generatedAt: ISO8601 UTC string,
  stats?: [{ label, value, subtitle }],          // omit if <3 grounded
  stories: [{
    id: string,                                   // hash of title+date, or `${index}-${slug}`
    category: one of the 5 categories,
    title, date, summary,
    editorPick: boolean,
    borderline?: boolean,                         // true if outside window but included
    sources: [{ name, url }]                      // 1–3 entries
  }],
  trendingRepos?: [{
    name, description, language, url, whyTrending,
    stars: number,
    starsGained: number | null,
    starsGainedLabel: string | null,              // "today" | "this month" | "this week" — literal source label
    category: Agent|Model|Tool|Framework|Dataset|Other
  }],                                             // omit if ≤1 confirmed
  weekInReview: string
}
```

Note: the UI derives the category tab list from `stories` — don't hardcode a `categories` field.

---

## Artifact build spec

- **File:** `/mnt/user-data/outputs/ai-news-digest.jsx`
- **Default export, no required props.**
- **Tailwind utility classes only.** Theme-aware (works in light + dark).
- **Icons:** `lucide-react` (`Star, Github, ExternalLink, Calendar, Filter, AlertCircle, ChevronDown` etc.).
- **Hooks:** `useState` from `react`. **No `localStorage`/`sessionStorage`.** No `<form>` tags — use `onClick`.

**Layout, top to bottom:**
1. Header — title, date range, generated-at timestamp.
2. Stat cards — horizontal-scroll row (omit section if no `stats`).
3. Category tabs — `All` + one per category present in `stories`, derived at render time. Pill style, active = solid bg.
4. Story cards — title (click to expand), date + category badge, editor-pick star, source-count badge if >1 source, collapsible summary, source links open in new tab. Show a small "borderline" indicator if `borderline: true`.
5. Trending repos — section with `Github` icon, 1-col mobile / 2-col desktop grid. Each card: repo name (mono), `⭐ {stars}` + `(+{starsGained} {starsGainedLabel})` if available, language pill, description, "why trending" muted italic, category badge, GitHub link.
6. Week-in-Review — distinct background, prose only, no bullets.

**Responsive:** mobile single column with horizontal-scroll stats; desktop wider with 2-col repo grid.

---

## Hard rules

1. Never fetch YouTube, TikTok, Twitter/X, Instagram URLs (JS-rendered, return garbage).
2. Never use `site:youtube.com` / `site:tiktok.com` in queries.
3. Never fabricate URLs, dates, star counts, or any number — use `null` or omit.
4. Never copy source text verbatim. Paraphrase summaries. One quote per source max, under 15 words.
5. Never render an empty section — omit it from data and UI.
6. Budget caps: ≤7 total searches, ≤5 total fetches. If short on data near the cap, stop and build with what you have.
7. Always present the final artifact via `present_files`.
8. Always include 2–4 editor picks if ≥4 stories exist.
9. Never include a story without a concrete calendar date.