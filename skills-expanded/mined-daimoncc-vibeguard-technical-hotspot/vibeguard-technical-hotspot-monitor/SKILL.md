---
name: VibeGuard-Technical-Hotspot-monitor
description: "Use when the user wants a self-contained AI hotspot monitoring skill that does not depend on a local server, SQLite, or OpenRouter. Triggers: monitor hot topics, add watch keyword, scan AI news, summarize recent hotspots, VibeGuard hotspot monitor."
---

# VibeGuard Technical Hotspot Monitor

## Purpose

Use this Skill when the user wants a self-contained hotspot monitor that:

- directly queries public search and news sources,
- optionally uses TwitterAPI.io when a key exists,
- stores local state in JSON files,
- relies on the chat model itself for relevance, authenticity, urgency, and summary analysis.

This Skill does not require the local web app, server, SQLite, or OpenRouter.

## Core Behavior

1. Bootstrap the local state store if it does not exist.
2. Manage watch targets through local scripts.
3. Fetch candidates directly from external sources.
4. Stage ranked candidates for model-side analysis.
5. Have the agent analyze the staged candidates in chat.
6. Persist the final analysis back into the Skill data files.
7. Summarize recent results for the user.

## State Model

- `data/watches.json`: watch targets and schedule metadata.
- `data/results.json`: analyzed hotspot results.
- `data/runs.json`: scan runs, staged candidates, and run-level summaries.
- `data/cache/`: fetch cache and temporary analysis payloads.

## Execution Workflow

### Initialize

Run once before the first operation or whenever the data folder is missing.

```powershell
node skills/VibeGuard-Technical-Hotspot-monitor/scripts/bootstrap.mjs
```

### Manage watches

Add a watch target:

```powershell
node skills/VibeGuard-Technical-Hotspot-monitor/scripts/watch-manager.mjs add --query "Claude Code" --interval 15
```

List current watches:

```powershell
node skills/VibeGuard-Technical-Hotspot-monitor/scripts/watch-manager.mjs list
```

### Stage a scan

Scan a direct query:

```powershell
node skills/VibeGuard-Technical-Hotspot-monitor/scripts/run-scan.mjs --query "AI coding" --limit 12
```

Scan all due watch targets:

```powershell
node skills/VibeGuard-Technical-Hotspot-monitor/scripts/run-scan.mjs --all-due --limit 12
```

### Analyze in chat

After `run-scan.mjs` returns staged candidates, use the generated analysis prompt file and fill the generated analysis template JSON. The payload must follow the schema described in `references/data-model.md`.

### Persist analysis

Save the analysis payload to a temporary JSON file, then commit it:

```powershell
node skills/VibeGuard-Technical-Hotspot-monitor/scripts/commit-analysis.mjs --run-id RUN_ID --input skills/VibeGuard-Technical-Hotspot-monitor/data/cache/analysis-RUN_ID.json
```

### Summarize recent results

```powershell
node skills/VibeGuard-Technical-Hotspot-monitor/scripts/summarize-results.mjs --limit 5
```

## Source Policy

Default sources require no API key:

- Google News RSS
- Bing News RSS
- DuckDuckGo Instant Answer API
- Hacker News Algolia Search

Optional enhanced source:

- TwitterAPI.io via `TWITTERAPI_IO_API_KEY`

If Twitter is not configured, the Skill still works and should not report that as an error.

## Analysis Policy

- Use the chat model as the only analysis engine.
- Do not call OpenRouter.
- Prioritize recency, source quality, query overlap, and directness of the signal.
- Be explicit when confidence is limited.
- Avoid overstating authenticity when a result is weak or indirect.

## Output Rules

When reporting back to the user:

- surface the strongest results first,
- include source, title, summary, urgency direction, and why it matters,
- mention if Twitter was skipped because no key was configured,
- mention when a run produced only weak or stale candidates.

`run-scan.mjs` automatically creates:

- an analysis template JSON file in `data/cache/analysis-RUN_ID.json`,
- an analysis prompt markdown file in `data/cache/analysis-RUN_ID.md`.

## References

| File | Purpose |
| --- | --- |
| `references/architecture.md` | Runtime architecture and workflow |
| `references/source-strategy.md` | Source coverage, fallback rules, and limits |
| `references/data-model.md` | JSON schemas and analysis payload contract |
| `acceptance-criteria.md` | Minimum acceptance criteria |
