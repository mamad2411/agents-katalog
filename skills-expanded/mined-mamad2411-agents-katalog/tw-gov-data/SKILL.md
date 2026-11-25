---
name: tw-gov-data
description: Search, inspect, compare, and summarize datasets from data.gov.tw. Use when the user wants Taiwan government open datasets, dataset metadata, resource download links, provider information, update times, formats, recent changes, or bulk dataset inventory from data.gov.tw.
---

# Taiwan Government Open Data

Use this skill when the user wants to discover, inspect, compare, or inventory datasets listed on `data.gov.tw`.

This skill is for dataset discovery and metadata inspection, not schema validation. Do not use `schema.gov.tw` for this skill unless the user explicitly changes scope.

## When To Use This Skill

- The user wants datasets from `data.gov.tw`
- The user wants dataset metadata, update times, formats, or providers
- The user wants resource download links or access URLs
- The user wants to compare candidate datasets
- The user wants a recent-change list or a bulk dataset inventory

## When Not To Use This Skill

- Do not validate field values against government schema rules
- Do not infer or enforce `schema.gov.tw` URIs
- Do not analyze the actual data rows until the correct dataset resource has been identified
- Do not promise that two datasets share the same field standard unless the source explicitly says so
- Do not assume every resource URL is hosted by `data.gov.tw`; many resources point to external agency systems

## Data Sources

Prefer `data.gov.tw` APIs over page scraping.

See [API quick reference](references/API.md) for endpoint selection and common metadata fields.
See [prompt examples](references/EXAMPLES.md) for representative user intents this skill should handle.
See [maintenance guidance](references/MAINTENANCE.md) for when this skill should be reviewed or updated.

- Prefer the live site-facing APIs on `https://data.gov.tw/api/front`
- Use dataset export for bulk inventory tasks
- Treat the published `api/v1/rest` cross-platform spec as documented but not operational until re-verified
- Avoid page scraping unless the APIs do not expose the needed view

## Default Workflow

1. Clarify the user goal from the request.
2. Choose the API path:
   - If the user wants keyword search or candidate discovery, use `api/front/dataset/list`.
   - If the user wants a bulk inventory, use `api/front/dataset/export?format=json`.
   - If the user already has a dataset page id (`nid`), use search results, export data, or a page-backed API only if needed.
3. Retrieve the minimum data needed first.
4. Summarize the results before expanding into more datasets.
5. When listing candidate datasets, include why each one is relevant.
6. When available, surface resource links, file formats, update times, provider, and field descriptions.

## Response Priorities

When presenting a dataset, prioritize:

- title
- provider or agency
- last updated time
- update frequency
- dataset description
- key fields
- available resource formats
- download or access URLs

When comparing datasets, highlight:

- topic overlap
- update freshness
- machine-readable formats
- whether the resource appears to be downloadable files or service endpoints

## Typical User Intents

- "幫我找空氣品質相關的政府資料"
- "列出最近 7 天異動的交通資料集"
- "比較這幾份資料哪份比較適合分析"
- "幫我整理某個資料集有哪些下載格式"
- "找某個機關目前公開了哪些資料集"
- "把某主題的資料集做成盤點清單"

## Output Guidance

For a single dataset, provide a concise summary.

For multiple datasets, prefer a short ranked list. Each item should explain:

- what the dataset is
- why it is relevant
- what formats or resource URLs are available

For bulk inventory tasks, provide:

- the selection rule used
- the total count when available
- a compact list or table-ready summary

## Cautions

- One dataset may contain multiple resources.
- Different resources under the same dataset may have different formats, encodings, and update times.
- Some datasets expose service endpoints, while others expose downloadable files.
- Always identify the correct resource URL before attempting downstream data work.

## Mutating Operations

The formal cross-platform specification includes write operations such as create, update, and delete for metadata.

Do not use mutating endpoints unless the user explicitly asks to publish, edit, or remove dataset metadata and the environment is clearly authorized for that action.
