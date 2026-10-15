---
name: seo-keyword-metrics
description: "Fetch keyword metrics (volume, KD, intent) in bulk using DataForSEO API"
version: 1.0.0
metadata:
  openclaw:
    emoji: "📊"
    homepage: https://github.com/AipengHuang/seo-keyword-intelligence
    primaryEnv: DATAFORSEO_LOGIN
    envVars:
      - name: DATAFORSEO_LOGIN
        required: true
        description: "DataForSEO account email. See seo-seed-discovery for setup instructions."
      - name: DATAFORSEO_PASSWORD
        required: true
        description: "DataForSEO account password."
    install:
      - kind: node
        package: seo-skill-core
---

# SEO Keyword Metrics

Enrich the keyword candidate pool with quantitative metrics: search volume, keyword difficulty, and search intent.

## Credentials Check

If `DATAFORSEO_LOGIN` or `DATAFORSEO_PASSWORD` are missing, tell the user:
> "DataForSEO credentials are not configured. Please run `seo-seed-discovery` first — it will guide you through the setup."

## When to Use

After `seo-keyword-expansion` has completed and `candidate-pool.json` exists in the workspace.

## Prerequisites

- Workspace with `candidate-pool.json` (merged from expansion results)

## Procedure

### Step 1: Bulk Search Volume

```bash
node {baseDir}/scripts/bulk-volume.ts --workspace <workspace_path>
```

Fetches monthly search volume + CPC + competition for all candidate keywords. Writes `volume.json`.

### Step 2: Bulk Keyword Difficulty

```bash
node {baseDir}/scripts/bulk-kd.ts --workspace <workspace_path>
```

Calculates keyword difficulty scores. Writes `kd.json`.

### Step 3: Search Intent Classification

```bash
node {baseDir}/scripts/search-intent.ts --workspace <workspace_path>
```

Classifies search intent (informational / navigational / commercial / transactional). Writes `intent.json`.

After all three steps, a merged `metrics.json` is produced.

## Expert Analysis Framework

Analyze the metrics data as an SEO strategist:

1. **Volume Distribution**: What's the volume range? Are there hidden gems in the 100-1000 range?
2. **KD vs Volume Efficiency**: Plot keywords on a KD/Volume matrix. Find the "sweet spot" — reasonable volume with manageable difficulty
3. **Intent Distribution**: What percentage is informational vs commercial? Does this match the user's content strategy?
4. **CPC as Signal**: High CPC keywords often indicate commercial value even if volume is low
5. **Quick Win Candidates**: Low KD + decent volume keywords the domain could rank for quickly

## Output Format

- **Metrics Summary** (total keywords, average volume, average KD)
- **Distribution Analysis** (volume tiers, KD tiers, intent breakdown)
- **Top 15 Sweet Spot Keywords** (high value / achievable difficulty)
- **Quick Win List** (KD < 30, Volume > 100)
