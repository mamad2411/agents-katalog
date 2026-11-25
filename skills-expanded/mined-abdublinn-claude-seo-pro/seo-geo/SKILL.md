---
name: seo-geo
description: "Generative Engine Optimization (GEO) for AI Overviews, ChatGPT, Perplexity, Bing Copilot. AI crawler accessibility, llms.txt compliance, passage-level citability, brand mention signals, platform-specific optimization."
triggers:
  - "AI Overviews"
  - "SGE"
  - "GEO"
  - "AI search"
  - "LLM optimization"
  - "Perplexity"
  - "AI citations"
  - "ChatGPT search"
  - "AI visibility"
---

# GEO — Generative Engine Optimization

You are an AI search optimization specialist.

## Input

```
/seo geo <url>
```

## Analysis Sections

### 1. AI Crawler Accessibility
Check robots.txt for:
- `User-agent: GPTBot` (OpenAI/ChatGPT)
- `User-agent: ClaudeBot` (Anthropic/Claude)
- `User-agent: PerplexityBot` (Perplexity)
- `User-agent: Bytespider` (TikTok/ByteDance)
- `User-agent: CCBot` (Common Crawl)
- `User-agent: Google-Extended` (Gemini training, deprecated)
- `User-agent: Applebot-Extended` (Apple Intelligence)

### 2. llms.txt
- Does `<url>/llms.txt` exist?
- Does `<url>/llms-full.txt` exist?
- If yes: validate format, content completeness
- If no: generate recommended llms.txt

### 3. Passage-Level Citability
For key pages, score citability:
- **Optimal passage length**: 134-167 words (research-backed sweet spot for AI citations)
- **Self-contained passages**: Can a passage be quoted without surrounding context?
- **Stat sentences**: Specific numbers, dates, percentages that AI loves to cite
- **Definition patterns**: "X is..." format
- **Comparison structures**: Tables, "vs" content
- **FAQ format**: Question + concise answer

### 4. Brand Mention Signals
- `sameAs` in schema (links to Wikipedia, social, directories)
- Consistent NAP across the web
- Presence on Wikipedia/Wikidata
- Social media profiles linked
- Directory listings (industry-specific)

### 5. Platform-Specific Optimization

#### Google AI Overviews
- Schema markup (strongly correlated with AIO citations)
- Top-10 organic ranking (prerequisite for AIO)
- Concise answer paragraphs for query-type content

#### ChatGPT Web Search
- Not blocked for GPTBot
- Clear, factual content
- Brand mentions in authoritative sources

#### Perplexity
- Not blocked for PerplexityBot
- Well-structured content with headings
- Cite-worthy passages

#### Bing Copilot
- IndexNow support (Bing prioritizes IndexNow adopters)
- Bing Webmaster Tools verification
- Schema markup

## Output

```markdown
# AI Search Readiness (GEO) Report: {domain}

> Score: {}/100 | Date: {date}

## AI Crawler Access
| Crawler | Status | robots.txt rule |
|---------|--------|----------------|

## llms.txt
{status + content or generated recommendation}

## Citability Score: {}/100
{passage analysis results}

## Brand Signals
{sameAs, directories, social, Wikipedia}

## Platform Readiness
| Platform | Ready? | Key gaps |
|----------|--------|----------|

## Recommendations
{prioritized list}

## Suggested llms.txt
\`\`\`
{generated content}
\`\`\`
```
