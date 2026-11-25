---
name: uniqueresearch-rankings
description: |
  Query UniqueResearch product rankings and trend data via the superun CLI.
  Use when: "排行榜", "产品排名", "ranking", "榜单", "月度排行", "产品趋势",
  "uniqueresearch", "排名查询", "行业榜单", "product ranking", "排行榜数据".
  Supports listing available ranking months, retrieving monthly ranking entries,
  and analyzing product trend data. Requires superun CLI with the 'unique' project registered.
  Part of the UniqueSkills platform toolkit. Built by UniqueClub 🌐 https://uniqueclub.ai
---

# UniqueResearch Rankings

> Query product rankings and trend data from the UniqueResearch backend through superun.

## When to Use

Use this skill when:
- The user wants to view **product rankings** for a specific month
- The user asks for **available ranking months** or the latest ranking period
- The user needs **product trend data** across multiple ranking periods
- The user wants to **compare rankings** across months
- The user references "排行榜"、"榜单"、"产品排名"、"ranking" in the context of UniqueResearch

Do NOT use this skill if:
- The user wants to submit a questionnaire response → use the `questionnaire` functions in superun
- The user wants to analyze questionnaire responses → use superun's `analysis` function group
- The user wants raw database access without superun → use direct database tools instead

Typical triggers:
- 「查一下最新排行榜」「8月榜单」「产品排名」「uniqueresearch 排行」
- "show me the rankings", "product ranking list", "latest month ranking"
- 「排行榜有哪些月份」「产品趋势」「月度榜单」

## Prerequisites

- `superun` CLI installed (`npm install -g superun-cli`)
- The `unique` project registered: `superun init --name "unique" --url <url> --anon-key <key> --manifest <manifest-url> --environment production`
- Active project set to `unique`: `superun app use unique`

## Workflow

本工作流遵循六步推进法：

### Step 1: 探查 (Probe)
- Confirm the `unique` project is registered and active: `superun app list`
- Verify connectivity: `superun --app unique --env production app show`
- Identify what the user wants: available months, specific month's entries, or product trends

### Step 2: 约束 (Constrain)
- Determine the target month (format: `YYYY-MM-DD`, e.g., `2026-08-01`)
- If no month specified, first list available months then ask the user to choose
- Set output format: JSON raw data, or formatted summary table
- Note: anonymous (anon) role can access public ranking data; login not required for read-only queries

### Step 3: 证据 (Evidence)
- All ranking data comes from the UniqueResearch backend via superun PostgREST RPC
- Available RPC functions (verified in schema):
  - `list_public_ranking_months` — returns available ranking months (no parameters)
  - `list_public_ranking_entries` — returns ranking entries for a period (parameter TBD)
  - `list_public_ranking_entries_v2` — v2 ranking entries (parameter TBD)
  - `list_public_ranking_product_trend` — product trend data (parameter TBD)
- Do not fabricate ranking data; only present what the API returns

### Step 4: 执行 (Execute)

**List available months:**
```bash
superun --app unique --env production db rpc list_public_ranking_months --data '{}'
```

**Get ranking entries for a month** (parameter name to be confirmed against API docs):
```bash
superun --app unique --env production db rpc list_public_ranking_entries --data '{"<param>": "<value>"}'
```

**Get product trend data:**
```bash
superun --app unique --env production db rpc list_public_ranking_product_trend --data '{}'
```

### Step 5: 验证 (Verify)
- Confirm HTTP 200 response
- Check that returned data is non-empty and matches the requested period
- Cross-reference month labels with the available months list
- If a function returns 404 (PGRST202), the parameter name is incorrect — consult the API manifest or database schema for the correct parameter name

### Step 6: 交付 (Deliver)
- Present ranking data as a formatted table with rank, product name, score, and trend indicators
- Include the data period and source
- For trends, highlight month-over-month changes
- Return raw JSON alongside the summary when the user needs downstream processing

## Output

### Available Months Format
```json
[
  {"month": "2026-08-01", "label": "2026年08月"},
  {"month": "2026-07-01", "label": "2026年07月"}
]
```

### Ranking Entries Summary Table
| 排名 | 产品名称 | 评分 | 月度变化 |
|------|---------|------|---------|
| 1 | ... | ... | ↑/↓/— |

## Guardrails

**Anti-patterns**
- NEVER fabricate ranking data or product names
- Do NOT guess RPC parameter names — verify against the schema or manifest first
- Do NOT modify ranking data — this skill is read-only

**Constraints**
- All queries go through `superun --app unique --env production`
- Anonymous role can access public ranking endpoints; login only needed for user-scoped data
- If the `unique` project is not registered, run `superun init` with the project credentials first
- The function `list_public_ranking_entries` requires a parameter; the exact name must be confirmed from the PostgreSQL function definition or API documentation

## Related Skills

- **superun** — Core CLI skill for operating any Supabase-compatible backend
- **agent-orchestrator** — Delegate ranking analysis tasks to sub-agents
- **enterprise-knowledge** — Cross-reference ranking data with internal company knowledge

## About

Part of the UniqueSkills platform toolkit — capabilities extracted from the UniqueResearch backend.
🌐 https://uniqueclub.ai | 📂 https://github.com/wulaosiji/skills
