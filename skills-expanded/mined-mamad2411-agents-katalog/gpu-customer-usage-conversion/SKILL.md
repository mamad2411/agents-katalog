---
name: gpu-customer-usage-conversion
description: >
  Analyze whether GPU resources in a DCE environment have converted into real
  customer usage and billable consumption. Use when a user asks "当前环境的 GPU
  资源有没有真正转化成客户用量", "哪些 GPU 只是有资源没客户用", "GPU 算力有没有变现/产生账单",
  "GPU 资源利用和客户 Token 用量能不能闭合", "GPU customer usage conversion",
  "GPU monetization", or similar questions about connecting GPU supply to
  workspaces/customers, LLM/API usage, runtime activity, and Billing Center
  revenue evidence.
---

# GPU Customer Usage Conversion

Judge whether deployed GPU capacity has become real customer usage by joining
DCE evidence across GPU supply, workspace/customer carrier, LLM/API activity,
runtime workload activity, and Billing Center billing.

**REQUIRED SUB-SKILL:** Use `dce` for command discovery, auth checks, module
availability checks, and read-only command execution.

**SCOPE:** Read-only analysis and recommendations. Do not create, update,
delete, scale, reprice, recalculate bills, change quota, or change routing.

## Core Rule

Do not treat "GPU exists" as customer usage. A conversion conclusion requires
evidence that connects:

```text
GPU resource -> workspace/customer carrier -> actual usage -> fee/revenue/chargeback
```

If a link is missing, say "基于当前可获取数据" and classify the result as partial
conversion or insufficient evidence. Treat voucher/credit consumption separately
from cash revenue.

## Quick Start

Run the bundled collector from this skill directory:

```bash
sh scripts/collect_gpu_customer_usage.sh \
  --hostname https://<dce-host> \
  --start 2026-06-01 \
  --end 2026-06-30 \
  --cluster <gpu-cluster> \
  --workspace <workspace-id>
```

If no cluster or workspace is supplied, run the collector anyway, inspect the
generated `clusters.json` and `workspaces.json`, then rerun with the GPU
clusters and relevant workspace ids. The collector writes raw JSON evidence and
`trace.tsv`; after collection, read the JSON files and calculate the final
tables from real data.

## Workflow

1. Establish scope.
   - Default window: last 30 days.
   - Use `YYYY-MM-DD` for report and billing commands.
   - Use RFC3339 timestamps for LLM Studio usage commands when needed.
   - Use Unix seconds only for Billing Center commands that require Unix time.
2. Check access and module availability.
   - Run `dce auth status --hostname <host>` when a host is provided or needed.
   - Use `dce global-management about list-g-product-versions -o json` if a
     module route returns 404.
3. Inspect unfamiliar commands before execution.
   - Use `dce commands show <path...> --json`.
   - Prefer `-o json`.
   - Use only read-only commands.
4. Collect GPU supply evidence.
   - Clusters, GPU devices, GPU modes, node/device inventory, utilization,
     allocated/requested GPU, memory total/used/allocated when available.
5. Collect carrier evidence.
   - Workspaces, namespaces, shared resources, quotas, queues, model services,
     API keys, and owner/customer mapping when present.
   - Do not call a workspace a customer unless DCE data or the user confirms
     the mapping.
6. Collect usage evidence.
   - Token counts, request counts, active users, active API keys, model instance
     usage, pod/runtime activity, queue activity, and last-used time.
   - Do not treat model deployment or API key existence as usage.
7. Collect billing evidence.
   - Billing Center `amountDue`, `productName`, `voucherPayment`, chargeback,
     and workspace/account aggregation.
   - Report voucher/credit consumption separately from cash revenue.
8. Classify conversion and report in the required output format.

## Conversion Levels

- `已转化`: GPU supply can be connected to workspace/customer, sustained usage,
  and billing/revenue or chargeback evidence in the analysis window.
- `部分转化`: GPU has a carrier and usage, but billing is missing/low, usage is
  unstable, utilization is weak, or evidence is concentrated in one
  workspace/customer.
- `未转化`: GPU exists but no proven customer/workspace usage or billable
  consumption is visible.
- `证据不足`: DCE data cannot connect GPU, carrier, usage, and money strongly
  enough to classify.

Map conversion levels to risk labels:

| Conversion level | Risk label |
|---|---|
| 已转化 | 正常 |
| 部分转化 | 关注 |
| 未转化 | 风险 |
| 证据不足 | 异常 |

## Data Sources

Use catalog discovery over hardcoded assumptions. Useful searches:

```bash
dce search "gpu devices" --json
dce search "workspace resources" --json
dce search "model serving" --json
dce search "llm studio token usage" --json
dce search "api key usage statistics" --json
dce search "billing aggregation" --json
dce search "workspace report" --json
```

Common read-only commands may include:

```bash
dce global-management workspace list-workspaces --page 1 --page-size 200 -o json
dce global-management workspace list-shared-resources-by-workspace --workspace-id <id> -o json
dce container-management cluster list-clusters --page 1 --page-size 200 -o json
dce container-management devices list-gpu-devices --cluster <cluster> -o json
dce llm-studio modelservingmanagement list-model-serving --page.page-size -1 -o json
dce llm-studio apikeymanagement get-api-key-usage-statistics2 --start-time <rfc3339> --end-time <rfc3339> --period TIME_PERIOD_DAY -o json
dce llm-studio wsdashboardmanagement get-ws-dashboard-summary --workspace <id> --start-time <rfc3339> --end-time <rfc3339> -o json
dce llm-studio wsdashboardmanagement list-ws-user-token-usage --workspace <id> --start-time <rfc3339> --end-time <rfc3339> --page.page-size -1 -o json
dce llm-studio wsdashboardmanagement list-ws-instance-token-usage --workspace <id> --start-time <rfc3339> --end-time <rfc3339> --page.page-size -1 -o json
dce billing-center bill get-account-bill-aggregation --workspace-id <id> --start-time <unix-seconds> --end-time <unix-seconds> -o json
```

If a command is absent or fails, inspect the command catalog and module
availability before concluding the data does not exist.

## Output Format

Answer in Chinese when the user asks in Chinese. Follow this Markdown structure
exactly unless the user asks for another format. Do not output a tool-call
waterfall, skill-loading details, retry chatter, or JSON processing internals.

```markdown
# 结论

基于当前可获取数据，<GPU 是否已转化为客户用量的判断>。当前风险等级为：<正常/关注/风险/异常>。

## 关键指标

| 指标 | 当前值 | 状态 |
|---|---:|---|
| GPU 总量/可用量 | ... | 正常/关注/异常 |
| GPU 平均利用率/分配率 | ... | 正常/关注/异常 |
| 活跃 workspace/customer | ... | 正常/关注/异常 |
| Token/request 用量 | ... | 正常/关注/异常 |
| 账单金额/抵扣金额 | ... | 正常/关注/异常 |
| 证据闭合度 | ... | 正常/关注/异常 |

## 主要发现

1. **<发现 1>**

<说明影响。>

2. **<发现 2>**

<说明影响。>

3. **<发现 3，可选>**

<说明影响。>

## 原因分析

### 原因 1：<原因>

证据：<真实数据证据。>  
影响：<对转化判断的影响。>

### 原因 2：<原因>

证据：<真实数据证据。>  
影响：<对转化判断的影响。>

## 建议动作

### 立即处理

1. <具体动作>
2. <具体动作>

### 持续观察

1. <具体动作>
2. <具体动作>

### 后续优化

1. <具体动作>
2. <具体动作>

## 后续可以继续追问

- 帮我查看未转化 GPU 的详细原因
- 帮我生成 GPU 客户用量转化提升方案
- 帮我导出一份给交付 / 老板看的报告
```

Keep `关键指标` to 3-6 rows. Include at least GPU capacity/utilization, active
workspace/customer, token/request usage, billing amount, or an evidence gap. Put
data gaps in the metric table or reason analysis; do not bury them in a command
trace.

## Evidence Rules

- Every number must come from pulled DCE output, a user-provided file, or an
  explicitly labeled assumption.
- Use `基于当前可获取数据` when Billing Center, LLM Studio, GPU metrics, or
  workspace/customer joins are incomplete.
- Do not infer revenue from GPU utilization or deployment inventory.
- Do not infer usage from API key existence, model service existence, or quota.
- Do not merge voucher/credit consumption with cash revenue.
- Do not report precise revenue, utilization, or conversion rate when only
  directional evidence exists.
- Show concise data-source coverage when useful, but avoid operational
  walkthroughs unless the user explicitly asks.
