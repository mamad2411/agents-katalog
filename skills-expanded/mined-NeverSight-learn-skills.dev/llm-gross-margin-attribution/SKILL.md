---
name: llm-gross-margin-attribution
description: Attribute why LLM gross margin got worse using live DCE and Crane data. Use when the user asks whether today's/this week's LLM gross margin decline is caused by model cost, tenant/customer mix, cache hit-rate changes, token usage, billing, or asks for ranked impact attribution such as "今天毛利变差是模型成本、租户结构还是缓存命中率变化导致的？按影响大小排序". Requires real DCE queries; do not answer with a generic framework.
---

# LLM Gross Margin Attribution

Diagnose an LLM gross-margin decline by querying DCE/Crane, comparing a current
period against a baseline period, and ranking the margin impact of:

1. Model cost / unit-cost change.
2. Tenant or workspace mix change.
3. Cache hit-rate change.

Do not fabricate numbers. Every metric must come from a live DCE/Crane command,
a user-provided real model-cost file, or an explicitly reported missing-data
gap.

Runtime dependency rule: use only POSIX `sh` plus the `dce` CLI. Cost inputs and
evidence artifacts are JSON. Do not add extra interpreters, JSON parsers,
package installs, or third-party libraries for this skill.

## Required Stance

- Query real data first. Do not answer with only a decomposition framework.
- Use read-only commands only.
- Keep command traces and raw JSON as internal evidence. Do not expose a
  tool-call or retry log in the final answer unless the user explicitly asks.
- Rank by margin-point impact on gross margin deterioration, not by narrative
  plausibility.
- If Billing Center revenue or LLM Studio token/cache data is missing, stop or
  mark the attribution incomplete. Do not infer them from deployment inventory.
- If Crane/DCE cost config or MaaS model-cost data is unavailable, report the
  cost attribution as incomplete. Do not estimate cost from unrelated runtime or
  inventory data.
- Use a real user-provided model-cost file only as a final fallback and only
  when the user explicitly provides it.

## Quick Start

Run the bundled evidence collector from this skill directory:

```bash
sh scripts/collect_margin_attribution.sh \
  --hostname https://<dce-host> \
  --current-start 2026-06-29T00:00:00+08:00 \
  --current-end 2026-06-29T23:59:59+08:00 \
  --baseline-start 2026-06-28T00:00:00+08:00 \
  --baseline-end 2026-06-28T23:59:59+08:00
```

The shell collector runs live `dce` queries and writes raw JSON evidence plus an
internal trace file. It intentionally does not parse JSON; after it writes the
evidence directory, read those JSON files and compute the ranked attribution
from real results.

## Data Sources

Use the `dce` skill rules for command discovery, auth checks, and module
availability.

Minimum live query set:

```bash
dce auth status --hostname <host>
dce global-management workspace list-workspaces --page 1 --page-size 200 -o json
dce llm-studio apikeymanagement get-api-key-usage-statistics2 --start-time <start> --end-time <end> --period TIME_PERIOD_DAY -o json
dce llm-studio modelservingmanagement list-model-serving --page.page-size -1 -o json
dce llm-studio maasservice list-maas-models -o json
dce billing-center bill list-bills --billing-time-start <date> --billing-time-end <date> --page 1 --page-size 200 -o json
```

Cost config discovery:

1. Search the generated CLI catalog first:

   ```bash
   dce search "analysis-center cost mock config" --json
   dce commands --include-hidden --json
   ```

2. If the catalog exposes the Hydra analysis-center cost mock config endpoint
   (`/apis/hydra.io/v1alpha1/analysis-center/cost-mock-config`), inspect it
   with `dce commands show <path...> --json`, run it read-only with `-o json`,
   and use the returned GPU prices and model costs.
3. If the endpoint is not exposed or the target host cannot serve it, mark
   model-cost attribution incomplete. In user-facing output, say only that
   "成本配置数据不可获取"; do not expose the concrete API path/name.

If tenant/workspace-level attribution cannot be joined from API-key usage,
discover the available LLM Studio workspace dashboard commands with `dce` and
run the matching workspace token-usage endpoint for each relevant workspace as
an optional follow-up. Treat those workspace dashboard rows as enrichment, not
as a dependency that blocks the base collector.

For cache metrics, prefer LLM Studio cached-token fields from API-key usage
statistics. If the deployment also exposes lower-level Prometheus counters
through Insight, use them only as a cross-check unless the LLM Studio field is
missing.

## Cost Rules

- Self-hosted DCE model cost: use Crane cost config GPU unit price and compute
  cost as `gpu_unit_price * gpu_count_or_replicas * runtime`. Treat GPU unit
  price as fixed within the analysis window unless the config returns effective
  periods; if it does, split the calculation by period.
- Upstream/proxy MaaS model cost: use the model-cost fields returned by the MaaS
  model APIs. Do not replace MaaS cost with local GPU cost.
- User-provided cost file: use only when the user explicitly provides a real
  finance/provider source. Cite it as a fallback data source and lower
  confidence if it cannot be reconciled with Crane/DCE metadata.

## Attribution Method

Compare current period against baseline:

```text
gross_margin = (revenue - model_cost) / revenue
margin_delta = current_gross_margin - baseline_gross_margin
```

Compute three ranked impacts:

- `model_cost`: change in model cost per billable token, holding current
  traffic/revenue mix fixed.
- `tenant_mix`: shift of revenue/token share across workspaces or tenants with
  different baseline margins.
- `cache_hit_rate`: change in cached-token share, converted to saved or added
  model cost using the real model cost basis.

Use Shapley-like averaging when all fields are present; otherwise use a
conservative stepwise estimate and label confidence `medium` or `low`. Any
unallocated difference is reported as residual, not hidden.

## Output Requirements

Answer in Chinese when the user asks in Chinese. Use structured Markdown, keep
the conclusion first, and do not show internal tool-call process, retries, or
JSON handling details unless explicitly requested. If data is incomplete, say
"基于当前可获取数据".

Do not expose internal API paths or generated command names for cost config in
the final answer. Refer to them generically as "成本配置数据" or "成本配置接口".

Every final answer must use exactly these sections:

```markdown
# 结论

<1-2 句话直接说明当前判断、风险等级和最重要的问题。>

## 关键指标

|指标|当前值|状态|
|---|---|---|
|收入|...|正常/关注/风险/异常|
|模型成本|...|正常/关注/风险/异常|
|毛利率|...|正常/关注/风险/异常|

## 主要发现

1. **<发现>**
<说明影响。>

2. **<发现>**
<说明影响。>

## 原因分析

### 原因 1：<原因>

证据：<数据证据。>  
影响：<毛利影响。>

## 建议动作

### 立即处理

1. <动作>

### 持续观察

1. <动作>

### 后续优化

1. <动作>

## 后续可以继续追问

- 帮我查看 <对象> 的详细原因
- 帮我生成 <对象> 的处理方案
- 帮我导出一份给交付 / 老板看的报告
```

`## 关键指标` must contain 3-6 metrics. Prefer tables for metrics. Put the
ranked attribution inside `## 主要发现` or `## 原因分析`, for example:

```text
按毛利恶化影响排序：
1. 模型成本上升：-x.x pct point
2. 租户结构变化：-y.y pct point
3. 缓存命中率下降：-z.z pct point
```

Never write "根因一定是 X" unless only one factor has data and the others are
proven flat. Prefer "证据指向 / 主要拖累 / 次要拖累".
