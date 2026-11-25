---
name: scraperapi-research-agent
description: >
  Runs the bundled Python research script: it plans Google searches, scrapes the top sources
  through ScraperAPI, uploads them to the Anthropic Files API, and has Claude write a cited
  markdown report with a numbered source list. Use only when the user wants this script run, or
  wants a standalone, repeatable research pipeline outside the chat. Trigger on: "run the
  scraperapi research agent on X", "use the research agent script to investigate Y", "give me a
  script that researches a question and writes a cited report". Requires Python 3.9+, `pip install
  requests anthropic`, SCRAPERAPI_API_KEY and ANTHROPIC_API_KEY. For research done directly in the
  conversation, use the ScraperAPI MCP tools (scraperapi-mcp); for a whole market or category, use
  scraperapi-market-research; for one person or company, use scraperapi-lead-enrichment.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI; uploads scraped content
  to the Anthropic Files API.
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
- [ ] **Credit budget** — Each Google search costs 25 credits and the script runs up to 3. Each source then costs ~1 credit to scrape on a normal site (more on protected sites). 5 sources ≈ 55–80 credits total.
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
| 3 | ~28–78 | ~15K in / ~2K out | Low |
| 5 | ~30–80 | ~25K in / ~3K out | Medium |
| 10 | ~35–85 | ~50K in / ~5K out | Higher |

Search dominates: 1–3 Google searches at 25 credits each, then ~1 credit per source on a normal site.

Prompt caching applies to the scraped content on repeated runs for the same question.

---

## ScraperAPI Endpoints Used

- **Google Search** — `GET https://api.scraperapi.com/structured/google/search` — finds source URLs
- **Scrape** — `GET https://api.scraperapi.com/?output_format=markdown` — fetches page content

See [ScraperAPI docs](https://docs.scraperapi.com/) for rate limits and credit costs.

## Anthropic APIs Used

- **Files API** — uploads scraped pages as document artifacts
- **Messages API** — Claude synthesizes the report with citations

Requires `ANTHROPIC_API_KEY` with access to `claude-opus-4-8` and the Files API.
