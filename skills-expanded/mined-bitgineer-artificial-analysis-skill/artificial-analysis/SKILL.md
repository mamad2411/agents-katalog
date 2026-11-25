---
name: artificial-analysis
description: Compare LLM models with a fixed scale built from ArtificialAnalysis.ai data, using no API key. Use when the user wants to compare AI models, their benchmarks, prices or speed, asks which model fits a job, or names artificial_analysis_tool.
---

The skill is self-contained: its own scripts, its own scale, no API key, and no dependency on any repository. It works in any agent that can run Node 18 or newer.

The scripts collect and rank the data. The agent running this skill writes the report from that data.

## 1. Find models (optional)

```
node "<skill-dir>/scripts/collect.mjs" --list --query deepseek
```

`<skill-dir>` is this skill's folder. Ids are the slugs shown in the first column. Dots become dashes in URLs.

## 2. Collect the data

```
node "<skill-dir>/scripts/collect.mjs" --models claude-opus-5-5,gpt-6-astra --out aa-comparison.json
```

- Two or more ids. The first two form the comparison slug; the ids must be real slugs or the fetch returns 404.
- The page carries a catalog of several hundred models; only a few dozen have benchmark data (`modelsWithData`). `--models` chooses and validates the pair. The script prints `⚠ not in the page data` for any requested id outside the catalog.
- `--url <comparison url>` reads an existing ArtificialAnalysis comparison instead.
- The script writes JSON and prints a summary. It never calls an AI provider and needs no key. The write is atomic; give each parallel run its own `--out`.

## 3. Read the JSON

| Part | Use |
|---|---|
| `models[]` | One record per model: the fields in `references/scale.md`. |
| `metrics[]` | `label`, `unit`, `direction`, `best.value`, `best.names`, `best.slugs`. These are the leaders. Do not recompute them. |
| `useCases[]` | `label`, `metrics`, `ranking` sorted best first. Row fields: `name`, `slug`, `averageRank` (lower is better), `metricsWithData`, `metricsTotal`. |
| `sourceUrl`, `collectedAt`, `extractionSource` | Cite the first two. |

## 4. Write the report in English

1. Executive summary: two or three paragraphs, the quality leaders and the value leaders.
2. Intelligence: the Intelligence Index ranking, the benchmark leaders, one table of the models with data (top 10 if there are more).
3. Pricing: input and output price, cache price, one table, and the best value points.
4. Performance: speed, time to first token, end-to-end time, context, size, reasoning, images.
5. Recommended use cases: one short block per `useCases` entry, top three, with coverage.
6. Final table: Model | Best for | Price (in/out per 1M) | Verdict.

## Rules

- Use only numbers from the JSON. A null is "not published", never 0.
- Use the rankings and leaders as given. Do not re-rank.
- Name each metric once whose `best.value` is null.
- When a use-case row has `metricsWithData` below `metricsTotal`, say the ranking rests on fewer metrics.
- Mark values far outside the rest as "verify" instead of stating them as fact.
- If the user named specific models, lead with that pair and say the rankings cover every model on the page.
- No invented facts, no filler. English only.
- Write the report in the reply. Save it to a file only if the user asks.
