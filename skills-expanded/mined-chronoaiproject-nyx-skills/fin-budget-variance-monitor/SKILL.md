---
name: fin-budget-variance-monitor
description: "Lark FIN-02 预算差异 workflow 路由。用户说‘帮我查看 2026 年第 32 周的预算差异’、‘预算差异’、‘预算对比’、‘预算执行’、‘超支情况’、‘第 N 周预算’、‘budget variance’或 fin-budget-variance-monitor 时，优先加载并执行这个精确 skill/workflow；不要只生成泛化周报或分析发票。"
version: "13.0"
metadata:
  category: mixed
  output-type: text
  runtime:
    - aevatar-workflow
  tool-list:
    - scope_workflows_get
    - aevatar_start_workflow
    - aevatar_observe_run
    - aevatar_read_workflow_run_artifact
  tag:
    - chronoai
    - finance
    - lark
    - budget
    - monitor
---

# FIN-02 预算差异监控

只运行当前 scope 的 canonical `fin_budget_variance_monitor`。随 skill 打包的
workflow YAML 是含 `__FINANCE_LARK_USER_SERVICE_ID__` 的可分发审计模板；用当前 scope
的 exact UserService UUID 渲染后才应与该 scope canonical 一致。业务运行时不要
draft-run、重新挂载、发布或编辑定义，也不要绕过 workflow 直接读取 Lark Base 或发送卡片。

## Lark 自然语言入口（最高优先级）

把下面这些业务句子视为“立即执行 FIN-02 workflow”的请求，而不是普通问答：

- 「帮我查看 2026 年第 32 周的预算差异，先不要发送」
- 「看第 32 周预算」「预算执行对比」「本周超支情况」「预算差异预览」

预算意图优先于会话里残留的发票附件或上一轮发票回复。即使当前对话有发票文件，
也必须运行预算 workflow；不要把发票金额当作预算数据，不要要求用户上传预算表。

- 需要搜索 skill 时，只用精确 slug `fin-budget-variance-monitor`；搜索结果必须是这个
  slug，不能按相似度接受别的结果。
- 只调用 `scope_workflows_get`，参数必须是精确 workflow 名
  `fin_budget_variance_monitor`；要求 `available=true`，再把 exact ID 传给
  `aevatar_start_workflow`，且只启动一次。不要调用 `nyxid_proxy` 代替，不要调用
  draft-run，不要直接访问 Lark Base，也不要只返回自然语言。
- `inputs.prompt` 必须是非空的序列化 JSON 字符串。把「2026年第32周」「第32周」等
  规范化为 `2026-W32`，例如 `{"period_label":"2026-W32","submit":false}`。
- 默认 `submit:false`；只有用户在同一对话中明确确认已经看过的成功预览，才允许
  `submit:true`。只要用户说“先不要发送/先预览/不要发卡片”，必须固定为 false。

## FIN-02 #4/#6/#7 runtime contract

- canonical 配置读取两个看板各自的实际支出表和预算表。Agent 不得直接访问、替换或
  猜测 Base/table identity；所有读取必须由 workflow 的受管 `nyxid_request` 完成。
- 四张表都必须用 `field_names` 只投影日期、一级类目和金额三列，并分别沿
  `page_token` 完整分页。每表最多三页；第三页仍有 `has_more=true`、缺 token、
  `total` 不一致、record ID 重复或零行时硬失败，不得用截断数据生成报告。
- 每表全部原始页只交给对应的 `code_execute` 做 record ID 去重、API `total` 核对、
  文本/epoch-ms 日期归一化和紧凑分类聚合。模板只构造分页请求、路由和展示，禁止
  逐页遍历或累加业务记录行，也不得由 skill 或 agent 自行重算。
- 每个聚合的 `output.stdout` 必须立即经 `json_parse` 变成 typed summary。预算聚合只接收
  对应实际支出的 cutoff 标量，最终 combine 只接收四个 typed summary；任何下游步骤都
  不得嵌套或重传完整 `code_execute` output envelope。
- 每个看板的 cutoff 是该看板实际支出数据中的最新有效日期。预算聚合必须使用同一
  cutoff，并明确统计晚于 cutoff 的预算行；ISO 文本、斜杠日期和 epoch ms 都归一化为
  `YYYY-MM-DD`，无效日期硬失败。
- 成功 artifact 必须包含两个看板，每个看板的 cutoff、总额、分类明细、告警数、
  undated/excluded 行数和 `source_rows`。`source_rows.actual` / `budget` 必须分别等于
  API total；全局必须 `pagination_complete=true`、`truncated=false`、
  `side_effects=false`。

## 执行和证据

1. 精确 lookup 后以 `wait="stream"` 启动一次。保留同一次调用返回的 run、actor 和
   command identity；收到 accepted/streaming receipt 后不得再次启动。
2. 用 `aevatar_observe_run` 的 `workflow_current_state` target 观察到 committed terminal，
   再调用 `aevatar_read_workflow_run_artifact` 读取 typed artifact。
3. 只依据 committed artifact 回复；Base 读取 receipt、Bot 文案、工具 receipt、
   `202 Accepted` 或自然语言 JSON 都不是成功证据。
4. 成功预览至少必须同时满足：`mode="preview"`、请求的 `period_label`、两个 boards、
   每个 board 的 cutoff/source row counts、`pagination_complete=true`、
   `truncated=false` 和 `side_effects=false`。任何一项缺失都不得描述成完整报告。
5. 分类等级为 `over`（超支）、`warning`（达上限）、`watch`（接近上限）、`ok`（正常）；
   无预算由 row 的 `no_budget=true` 单独表示。保留 artifact 原顺序和数值。
6. 提交必须先有成功预览和同一用户的明确确认；只接受 committed artifact 的
   `mode="submit"`、`message_sent=true`、`side_effects=true`。提交失败时不自动重试，
   因为卡片可能已经发送。

## 回复约束

不展示 workflow/skill/tool 名、run/actor/service/message 标识、token、完整文档链接或
接收人编号。字段和数字必须原样来自 typed artifact；缺失字段写「未返回」。

预览可用如下格式：

> 📊 **{period_label} 预算差异**
> 数据截止：{data_cutoff}
> **{看板名}**（截止 {cutoff}，实际 {total_actual} / 预算 {total_budget}）
> {按 artifact 顺序逐类目列出图标、实际/预算、百分比或「无预算」}
> 告警合计：{alerts} 项｜源数据：实际 {source_rows.actual} 行 / 预算 {source_rows.budget} 行
> ✅ 数据分页完整；本次为预览，未发送任何卡片。

遇到 `ca_agg`、`cb_agg`、`aa_agg`、`ab_agg` 或 `combine` 失败时，只说明分页、金额、
日期或源数据核对失败，不展示部分报告。遇到 `send_notify` 或 `summarize_submit` 失败时，
说明卡片可能已发送，先到 Lark 核实，不要自动重试。
