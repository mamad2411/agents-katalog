---
name: dfs-keyword-research
description: |
  Keyword research, SERP analysis, and competitor intelligence via the dfs CLI (data-4-seo-cli).
  Returns 10-20x smaller responses than raw DataForSEO API, optimized for agent context windows.
  Use when asked about keyword volumes, search difficulty, keyword ideas, SERP features, competitor
  rankings, domain overlap, content analysis, content briefs, or competitor gap analysis.
  Requires: npm install -g data-4-seo-cli
---

# DFS Keyword Research

The `dfs` CLI wraps the DataForSEO API and returns only the fields that matter. Raw API responses are 15-30KB per query; `dfs` compresses them to 1-2KB. This keeps your context window clean when doing multi-step research.

## Prerequisites

The CLI must be installed globally before any commands will work:

```bash
npm install -g data-4-seo-cli
```

## Auth

Check if credentials are already stored:

```bash
dfs whoami
```

If not authenticated, set environment variables or store credentials permanently:

```bash
export DATAFORSEO_LOGIN=your_login
export DATAFORSEO_PASSWORD=your_password
# Or store permanently:
dfs login --login "$DATAFORSEO_LOGIN" --password "$DATAFORSEO_PASSWORD"
```

## Choosing the right command

Pick the command based on what you need:

| Need | Command | When to use |
|------|---------|-------------|
| Check metrics for known keywords | `dfs volume` | You have specific keywords and need volume, CPC, difficulty, competition, intent |
| Expand a seed keyword | `dfs suggestions` | You have one keyword and need more ideas |
| Find semantically related terms | `dfs related` | You want lateral keyword ideas, not just autocomplete |
| Bulk difficulty check | `dfs difficulty` | You only need difficulty scores, nothing else |
| Analyze a SERP | `dfs serp` | You need to see who ranks, what features appear (AI Overview, PAA, etc.) |
| See what a domain ranks for | `dfs ranked` | Competitor research or auditing a domain's keyword portfolio |
| Compare two domains | `dfs overlap` | Find shared keywords and position gaps between two competitors |
| Find SERP competitors | `dfs competitors` | Discover which domains compete for a set of keywords |
| Analyze page content | `dfs content` | Fetch a URL's title, headings, and word count for content gap analysis |

## Commands

### dfs volume

```bash
dfs volume "seo tools" "keyword research" "backlink checker"
```

Returns: `keyword, volume, cpc, difficulty, competition, intent, trend`

Accepts up to 50 keywords in one call. The trend column shows 12 months of search volume.

### dfs suggestions

```bash
dfs suggestions "seo tools" -n 15
```

Returns: `keyword, volume, cpc, difficulty, competition`

Takes one seed keyword. Use `-n` to control how many suggestions.

### dfs related

```bash
dfs related "keyword research" -n 15
```

Returns: `keyword, volume, cpc, difficulty, competition`

Semantically related terms, not just autocomplete matches. Good for finding angles you might miss.

### dfs difficulty

```bash
dfs difficulty "seo tools" "keyword research" "backlink checker"
```

Returns: `keyword, difficulty`

Use this when you only need difficulty scores and want the smallest possible response.

### dfs serp

```bash
dfs serp "best seo tools" --target yourdomain.com
```

Features and PAA questions go to stderr. Organic results go to stdout: `position, domain, title, url`

The `--target` flag highlights where a specific domain ranks. Use `--json` for the full structured result including features, snippets, and PAA questions.

### dfs ranked

```bash
dfs ranked ahrefs.com -n 20
```

Returns: `keyword, position, volume, cpc, url`

Keywords sorted by volume. Use this to understand a competitor's keyword portfolio.

### dfs overlap

```bash
dfs overlap ahrefs.com semrush.com -n 20
```

Returns: `keyword, pos1, pos2, volume, cpc`

Shows keywords both domains rank for with their respective positions. Great for finding where you're losing to a competitor.

### dfs competitors

```bash
dfs competitors "seo tools" "keyword research tool" -n 10
```

Returns: `domain, avg_position, visibility, keywords_count`

Pass one or more keywords to discover which domains compete in those SERPs.

### dfs content

```bash
dfs content "https://example.com/page"
dfs content "https://example.com/page" --full --json
```

TSV returns: `url, title, word_count, headings_count` (headings detail on stderr).
JSON with `--full` returns the complete headings tree and content preview.

## Output formats

Use `--table` when presenting results to the user. Use default TSV when processing data internally. Use `--json` when you need to parse specific fields programmatically.

## Options

```
-l, --location <code>    Location code (default: 2840 = US)
    --language <code>     Language code (default: en)
-n, --limit <n>          Max results (default: 50)
    --no-cache           Force fresh API call
```

Look up location and language codes with `dfs locations <search>` and `dfs languages <search>`.

## Caching

Results are cached automatically to avoid duplicate API costs. Repeated queries within the TTL are free:

| Data Type | Cache TTL |
|-----------|-----------|
| Keyword data | 7 days |
| Competitor data | 3 days |
| SERP results | 1 day |
| Locations/languages | 30 days |

Use `--no-cache` only when you need guaranteed fresh data.

## Workflow references

For detailed workflows, step-by-step guides, and interpretation tips, read the relevant reference file:

| Task | Reference |
|------|-----------|
| Keyword research, content briefs, bulk volume checks, difficulty interpretation | [references/keyword-research.md](references/keyword-research.md) |
| SERP analysis, feature detection, content gap analysis, PAA research | [references/serp-analysis.md](references/serp-analysis.md) |
| Competitor ranked keywords, domain overlap, competitive landscape mapping | [references/competitor-intel.md](references/competitor-intel.md) |

Read only the reference you need for the current task.
