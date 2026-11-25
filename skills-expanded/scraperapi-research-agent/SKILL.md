---
name: scraperapi-research-agent
description: >
  Autonomous web research agent — takes a research question, uses ScraperAPI to discover and
  scrape relevant sources, uploads content as file artifacts to the Anthropic Files API, then
  feeds everything to Claude for synthesis into a cited research report. All in one flow.
  Use when user asks: "research X for me and give me a cited report",
  "investigate Y online and summarize what you find", "do a deep dive on Z using real web sources",
  "find information about X across multiple websites and cite your sources",
  "run the scraperapi research agent on this topic". Produces a structured markdown report with
  inline citations and a numbered source list. Invoke whenever the user wants multi-source web
  research that requires scraping real pages, not just answering from memory.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI; uploads scraped content to the Anthropic Files API.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
        - ANTHROPIC_API_KEY
    emoji: "🔬"
    homepage: https://docs.scraperapi.com/
---

# ScraperAPI Research Agent

End-to-end autonomous research: ScraperAPI finds and fetches sources → Anthropic Files API
ingests them as cited documents → Claude synthesizes a report.

**Run it:**

```bash
# Install dependencies
pip install requests anthropic

# Set env vars
export SCRAPERAPI_API_KEY=your-key
export ANTHROPIC_API_KEY=your-key

# Run
python skills/scraperapi-research-agent/scripts/research_agent.py \
  --question "What are the best practices for rate limiting in web APIs?" \
  --max-sources 5 \
  --output report.md
```

See [scripts/research_agent.py](scripts/research_agent.py) for the full implementation.

---

## Planning Checklist

Before starting a research run, establish:

- [ ] **Question clarity** — Is the question specific enough to produce useful search queries? Vague questions like "tell me about AI" produce noise. Better: "What are the tradeoffs between RAG and fine-tuning for domain-specific LLMs?"
- [ ] **Source count** — How many sources are needed? 3–5 is usually sufficient for a factual summary; 8–10 for a comparative analysis. More sources = more ScraperAPI credits.
- [ ] **Recency** — Does the answer depend on recent events? Search queries will use recent date filters.
- [ ] **Credit budget** — Each source costs ~1 credit to scrape (more with JS rendering). 5 sources = ~5–10 credits total.
- [ ] **Stop condition** — Define when to stop. The default stop is `--max-sources` (5). Do not loop indefinitely.

---

## Research Loop

```
1. PLAN
   ↓ Claude decomposes the question into 2–3 targeted search queries

2. DISCOVER
   ↓ ScraperAPI google/search structured endpoint → list of (url, title, snippet)

3. DEDUPLICATE
   ↓ Filter to top N unique URLs (default: 5), skipping PDFs and low-quality domains

4. FETCH
   ↓ ScraperAPI scrape each URL as markdown (output_format=markdown)
   ↓ Skip pages returning < 200 characters (blocked, error pages)

5. UPLOAD
   ↓ Upload each scraped page to Anthropic Files API as a text/plain artifact
   ↓ Store file_id for each source

6. SYNTHESIZE
   ↓ Claude (claude-opus-4-8, adaptive thinking) reads all document artifacts
   ↓ Returns structured report with inline citations [1], [2]...

7. CLEAN UP
   ↓ Delete uploaded file artifacts from Anthropic
   ↓ Write or print the final report

STOP when: max_sources reached, or all queries exhausted (whichever comes first).
```

---

## Stop Conditions

The agent stops when any of the following is true:

1. **`--max-sources` reached** (default: 5) — limits credit spend
2. **All search queries exhausted** — no more URLs to explore
3. **`--max-credits` exceeded** — hard cap on ScraperAPI credit use (optional)

Without stop conditions, a research loop will keep fetching until credits are gone.

---

## Key Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--question` | (required) | Research question |
| `--max-sources` | 5 | Max pages to scrape (credit budget) |
| `--output` | stdout | Write report to file |
| `--country` | `us` | ScraperAPI country code for geo-targeted results |
| `--model` | `claude-opus-4-8` | Anthropic model for synthesis |

---

## Output Format

See [assets/report_template.md](assets/report_template.md) for the report structure.

The report is a markdown document with:
- **Title** derived from the research question
- **Summary** — 2–3 sentence executive summary
- **Findings** — structured sections with inline `[N]` citations
- **Sources** — numbered bibliography with URLs and titles

---

## Credit Cost Estimate

| Sources | Scraping credits | Anthropic tokens | Total estimate |
|---------|-----------------|-----------------|----------------|
| 3 | ~3 | ~15K in / ~2K out | Low |
| 5 | ~5 | ~25K in / ~3K out | Medium |
| 10 | ~10 | ~50K in / ~5K out | Higher |

Prompt caching applies to the scraped content on repeated runs for the same question.

---

## ScraperAPI Endpoints Used

- **Google Search** — `GET https://api.scraperapi.com/structured/google/search` — finds source URLs
- **Scrape** — `GET https://api.scraperapi.com/?output_format=markdown` — fetches page content

See [ScraperAPI docs](https://docs.scraperapi.com/) for rate limits and credit costs.

## Anthropic APIs Used

- **Files API** (beta) — uploads scraped pages as document artifacts
- **Messages API** — Claude synthesizes the report with citations

Requires `ANTHROPIC_API_KEY` with access to `claude-opus-4-8` and the Files API beta.
