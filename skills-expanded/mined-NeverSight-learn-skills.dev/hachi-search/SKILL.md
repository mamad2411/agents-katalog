---
name: hachi-search
description: Local-LLM-oriented federated search across specified local folders, optional hachiware-labs/wiki-garden knowledge, web search providers, and URL enrichment. Use when a local LLM or local agent needs source-attributed evidence from project files, local documents, wiki-garden notes, or the web with configurable source selection, URL content fetching, search order, and result merging.
---

# Hachi Search

Use this skill to gather evidence for local LLM and local-agent workflows, then merge it into a concise, source-attributed result set.

## Inputs

Collect or infer:

- `query`: The search query or topic.
- `roots`: Local folders to search. Default to the current workspace when the user does not specify roots.
- `tools`: Search sources to use. Supported values: `local`, `wiki-garden`, `tavily`, `exa`, `firecrawl`.
- `order`: Provider execution order. Default: `local,wiki-garden,tavily,exa,firecrawl`.
- `enrich`: URL enrichment providers to run after search. Supported values: `firecrawl`.
- `enrichLimit`: Maximum URL results to enrich. Default: `5`.
- `merge`: Merge strategy. Supported values: `ranked`, `provider-order`, `dedupe-only`, `agent-sort`. Default: `ranked`.
- `agent-sort`: Preferred LLM-based merge strategy for skill use. The helper dedupes results, then the calling local LLM/agent sorts by usefulness in its response.
- `limit`: Maximum results per provider. Default: `8`.

## Procedure

1. Prefer user-specified `tools`, `order`, `merge`, and `roots`. If unspecified, search local context first, then wiki-garden if available, then web providers with configured API keys.
2. Search local folders with `scripts/hachi-search.mjs` or `rg` directly when a custom file inspection is needed.
3. If `hachiware-labs/wiki-garden` is installed or a `wiki-garden` skill/CLI is available, query it after local search and before web search unless the user requests a different order.
4. Use Tavily or Exa to discover candidate URLs. Use Firecrawl enrichment to fetch clean markdown from those URLs when page content is important for the local LLM.
5. Firecrawl can also be used as a search provider, but the default role is URL enrichment after Tavily/Exa search.
6. Merge results by canonical URL or file path. Prefer exact local or wiki-garden evidence over web snippets when answering repo-specific questions.
7. Report the search providers used, enrichment providers used, skipped sources, and any missing API keys or unavailable tools.

## Search Modes

Use one of these modes unless the user gives a more specific plan:

- Local search: run only `local` against the selected `roots`.
- Full search settings: define `roots`, `tools`, `order`, `merge`, and `limit` in JSON.
- Full search from config: run `scripts/hachi-search.mjs` with `--config` and the user query.

Bundled configs:

- `configs/default.json`: default search settings used when no `--config` is passed.
- `configs/local.json`: local-only search.
- `configs/full.json`: local, wiki-garden, Tavily, Exa, Firecrawl search, and Firecrawl enrichment.

## Search vs Enrichment

Search providers find candidate sources:

- `local`: local file matches.
- `wiki-garden`: wiki-garden knowledge.
- `tavily`: general web search that returns URLs and snippets.
- `exa`: semantic/research web search that returns URLs and snippets/content.
- `firecrawl`: Firecrawl web search, available when Firecrawl should also be a search source.

Enrichment providers fetch content from URL results:

- `firecrawl`: scrape URL results into clean markdown so the calling agent can read and sort richer evidence.

The default config uses Tavily for URL discovery, Firecrawl for URL enrichment, and `agent-sort` for final usefulness ordering in the calling local LLM/agent.

Merge strategies:

- `ranked`: Dedupe results, then sort by provider score.
- `provider-order`: Dedupe results and keep the configured provider order.
- `dedupe-only`: Dedupe results without score sorting.
- `agent-sort`: Dedupe results, then sort by usefulness in the calling local LLM/skill response. This does not require a separate LLM API key.

## Shorthands

Treat these shorthand phrases as search mode selectors:

- `local`: local-only search.
- `full`: full search across all configured providers.
- `調べて`: search with the default configured providers.

When the user says `調べて <query>`, search with the default configured providers unless they explicitly specify different sources, order, merge strategy, or roots.
When the user says `$hachi-search <query> を調べて`, treat `<query>` as the search query and use the default configured providers.
When the user says `$hachi-searchの使用する検索をtavily,firecrawlに設定して`, update `configs/default.json` so default searches use `tavily` and `firecrawl`.
When the user says `$hachi-searchのマージ方法をprovider-orderに設定して` or `$hachi-searchのマージ方法をagent-sortに設定して`, update `configs/default.json` so default searches use that merge strategy.

## Helper Script

Run the bundled helper from the skill directory:

```bash
node scripts/hachi-search.mjs --query "search terms" --roots . --tools local,tavily,exa,firecrawl --limit 8
```

Useful options:

- `--config path/to/config.json`: Load defaults from JSON.
- `--preset local|full|調べて`: Load a bundled search mode.
- `--set-tools local|wiki-garden|tavily|exa|firecrawl`: Save default search providers to `configs/default.json`.
- `--enrich firecrawl`: Enrich URL results with Firecrawl after search.
- `--enrich-limit 5`: Limit how many URL results are enriched.
- `--set-merge ranked|provider-order|dedupe-only|agent-sort`: Save the default merge strategy to `configs/default.json`.
- `--order local,wiki-garden,tavily,exa,firecrawl`: Override execution order.
- `--merge ranked|provider-order|dedupe-only|agent-sort`: Override merge behavior.
- `--json`: Print JSON instead of readable text.

The helper reads these environment variables when web providers are enabled:

- `TAVILY_API_KEY`
- `EXA_API_KEY`
- `FIRECRAWL_API_KEY`

## Config Example

```json
{
  "roots": ["."],
  "tools": ["local", "wiki-garden", "tavily", "exa", "firecrawl"],
  "order": ["local", "wiki-garden", "tavily", "exa", "firecrawl"],
  "merge": "ranked",
  "limit": 8
}
```

## Output Standard

Return answers with:

- A short conclusion.
- The merged evidence, each item labeled with provider and source path or URL.
- Provider notes: which providers ran, which were skipped, and why.

For high-stakes or time-sensitive questions, explicitly state that web providers were used and cite current web results.
