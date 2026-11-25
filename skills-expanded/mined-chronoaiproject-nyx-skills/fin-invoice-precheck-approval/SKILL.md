---
name: fin-invoice-precheck-approval
description: "Lark FIN-01 发票预检 workflow 路由。用户说‘帮我预检刚上传的发票’、‘发票预检’、‘检查发票’、‘检查刚上传的发票’、‘发票审批’、‘付款审批’、‘发起付款’、‘invoice precheck’或 fin-invoice-precheck-approval 时，优先加载这个精确 skill；附件和申请日期齐备后执行 workflow，缺项时先索取；不要走通用 OCR。"
version: "15.0"
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
    - invoice
    - payment
    - approval
---

# FIN-01 发票预检与付款审批

只运行当前 scope 的 canonical `fin_invoice_precheck_approval`。随 skill 打包的
workflow YAML 是含 `__FINANCE_LARK_USER_SERVICE_ID__` 的可分发审计模板；用当前 scope
的 exact UserService UUID 渲染后才应与该 scope canonical 一致。业务运行时不要
draft-run、重新挂载、发布或编辑定义，也不要绕过 workflow 直接调用 Lark 审批接口。

## Lark 自然语言入口（最高优先级）

把下面这些业务句子视为 FIN-01 业务请求，而不是普通问答。附件和申请日期齐备时
立即执行 workflow；缺少任一必填输入时先索取，不得启动一个必失败的 run：

- 「帮我预检刚上传的发票，申请日期按 2026 年 8 月 14 日，先不要提交审批」
- 「发票预检」「检查这张发票」「发票审批预览」「付款审批预览」

有发票附件时，附件 + 上述意图优先于会话里的预算、报销或 OCR 上下文。先加载本
skill，再核对申请日期并执行精确 lookup；不要先自行 OCR 后拼接结果。没有发票附件
或没有申请日期时只索取缺失项，不启动 workflow。

- 需要搜索 skill 时，只用精确 slug `fin-invoice-precheck-approval`；搜索结果必须是
  这个 slug，不能按相似度接受别的结果。
- 只调用 `scope_workflows_get`，参数必须是精确 workflow 名
  `fin_invoice_precheck_approval`；要求 `available=true`，再把 exact ID 传给
  `aevatar_start_workflow`，且只启动一次。不要调用 `nyxid_proxy` 代替，不要调用
  draft-run，也不要只返回自然语言。
- `inputs.prompt` 必须是非空的序列化 JSON 字符串，例如
  `{"run_date":"2026-08-14","submit":false}`。默认 `submit:false`；只有用户
  在同一对话中明确确认已经看过的成功预览，才允许 `submit:true`。
- 只要用户说“先不要提交/先预览/不要发起审批”，必须把 `submit` 固定为 `false`；
  不得把普通的“帮我看看”解释成提交授权。

## 附件和输入

- 发票附件是必需的。优先使用本回合/本对话最近上传的附件；没有附件时只提示：
  「请先把发票文件发到这个对话里，再让我预检。」不要向用户询问 file ref、JSON
  或工具参数。
- 多个附件视为同一张发票的多页；不同发票必须分开运行。
- `run_date` 必填。把用户给出的申请日期/运行日期规范化为 `YYYY-MM-DD`；通用 workflow
  引擎没有可供本 skill 信任的当前日期。用户未给日期时只询问「申请日期是哪一天？请按
  YYYY-MM-DD 提供。」不得猜测今天、沿用旧日期或调用 `aevatar_start_workflow`。预览输入
  必须为 `{"run_date":"YYYY-MM-DD","submit":false}`。
- 付款表单补充字段放在 `review`。DigitalAsset 示例：

  ```json
  {"run_date":"2026-08-14","submit":false,"review":{"Department":"Finance","Department Open ID":"od-0123456789abcdef","Payment Entity":"DigitalAsset Payment","Payer Information":"Finance","Recipient Address":"TRC-20 T..."}}
  ```

- `Department Open ID` 可省略；提供时必须是 `od-...`。省略后由 applicant profile 的
  `department_ids[0]` 回填。AELF INVEST / DigitalAsset 要求非空
  `Recipient Address`，DigitalAsset 还要求非空 `Payer Information`；法币分支可省略。

## FIN-01 #5/#7 runtime contract

- 图片或文本发票的 `vendor` 必须取开票方/卖方；页眉、logo、法定名称、网站域名和
  支持邮箱是优先证据。不得把买方、收票方或付款方当作 vendor。
- `invoice_date` 必须在确定性校验中归一化为 `YYYY-MM-DD`；无效或有歧义的日期按缺失
  处理并阻止 submit。币种和金额也必须来自 artifact，不能由 agent 自行推断。
- 审批历史必须保持与生产流程一致的 365 天服务端时间窗，按 `page_token` 持续分页直到
  `has_more=false`，再逐条回读做查重。不得缩短时间窗，也不得另加页数、候选条数、迭代
  次数或执行时长上限；第四页及以后必须继续读取，禁止静默截断。预览 artifact 中
  `duplicate_check.history_pagination_complete` 和 `dedup_scan_complete` 都必须为 true；
  不完整时不得称为通过，也不得提交。
- 历史详情读取必须把完整唯一候选列表交给单个 foreach，`min/max_concurrent_workers` 都为
  `10`，不得按页拆成多个 foreach 或用 `n`/`take` 截断。详情调用必须使用 fail-closed
  response projection，只持久化 `code`、`instance_code`、`approval_code`、`status`、
  `serial_number` 和每个 fieldList 行的付款事由；不得把 vendor、金额、银行字段、时间线或
  人员/部门标识写入 workflow state。任一详情读取或投影失败时，run 必须 fail closed；
  若仍能产出 preview artifact，则必须标记查重不完整。submit 必须中止。
- 线上付款 `fieldList` schema 有 26 个 child，其中 22 个 required。默认无关联审批的
  法币分支应构造 18 个唯一明细 child，加 fieldList、remark、attachment 后计划填充
  21 个表单项。合成 canary 必须精确命中 `schema_child_widgets=26`、
  `schema_required_widgets=22`、`populated_row_widgets=18`、
  `populated_widgets_after_attachment=21`；其他条件分支数量可能变化。
- 预览只计划附件上传，不上传附件、不创建审批；`side_effects` 必须为 false。

## 执行和证据

1. 精确 lookup 后以 `wait="stream"` 启动一次。保留同一次调用返回的 run、actor 和
   command identity；收到 accepted/streaming receipt 后不得再次启动。
2. 用 `aevatar_observe_run` 的 `workflow_current_state` target 观察到 committed terminal，
   再调用 `aevatar_read_workflow_run_artifact` 读取 typed artifact。
3. 只依据 committed artifact 回复；文件卡片、Bot 文案、工具 receipt、`202 Accepted`
   或自然语言 JSON 都不是成功证据。
4. 成功预览至少必须同时满足：`mode="preview"`、`side_effects=false`、
   `ready_for_submit=true`、`problems=[]`、附件数量正确、分页与查重完整，并精确检查
   `extracted_invoice`、`currency`、`amount_value` 和 `form_summary`。
5. 提交必须先有成功预览和同一用户的明确确认；只接受 committed artifact 的
   `mode="submit"`、`approval_created=true`、`side_effects=true`。提交失败或回读失败时
   不自动重试，先让人工核对 Lark。

## 回复约束

不展示 workflow/skill/tool 名、run/actor/service/message/file 标识、token、完整文档链接
或银行敏感编号。字段和数字必须原样来自 typed artifact；缺失字段写「未返回」。

预览可用如下格式：

> 🧾 **发票预检结果**
> 供应商：{vendor}
> 发票号：{invoice_number}｜开票日期：{invoice_date}
> 金额：**{currency} {amount_value}**
> 检查结果：{problems 为空则说明通过，否则逐条说明}
> ✅ 本次为预览，未发起任何审批。金额等字段请对照发票原件人工核对。

不要向业务用户展示 widget/schema 计数；这些字段只用于内部验收。遇到
`parse_validate`、`accumulate_history_page`、`dedup_eval` 或 `build_lark_form` 失败时，
只说明提取、日期、分页查重或表单必填项未通过。遇到 `merge_attachment_form`、
`create_approval` 或 `summarize_submit` 失败时，说明审批可能已建立，先到 Lark 核实，
不要重试。
