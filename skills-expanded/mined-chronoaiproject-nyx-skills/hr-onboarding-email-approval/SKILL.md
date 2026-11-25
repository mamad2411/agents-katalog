---
name: hr-onboarding-email-approval
description: 入职邮箱开通审批。当用户说入职邮箱、新员工邮箱、邮箱申请、开通邮箱、邮箱审批、onboarding email，或 Employee Master 新员工入职状态触发邮箱审批时使用。支持自然语言预览/提交和 Base record 自动化；默认只预览，用户无需知道 workflow、skill、工具或 JSON。
version: "7.0"
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
    - hr
    - lark
    - onboarding
    - email
    - approval
---

# 入职邮箱开通审批

运行 canonical `hr_onboarding_email_approval`。所有技术细节都只在 agent 内部处理，不向业务用户展示。

## 调用契约

每次严格按顺序执行：

1. 判断入口：
   - 普通对话是 inline 入口，从自然语言提取姓名、部门、入职日期和可选邮箱前缀。
   - 上游自动化或明确提供 Employee Master 记录时是 record 入口，使用 `record_id` 读取新人信息；不要再追问记录中已有的姓名、部门和入职日期。
2. 仅用业务中文追问真正缺失的业务事实。绝不向用户提 workflow、skill、工具、参数、JSON、record schema 或内部标识。
3. 在内部构造一个非空序列化 JSON 字符串：
   - inline preview：
     `{"lark_name":"…","department":"…","onboarding_date":"YYYY-MM-DD","email_username":"…","submit":false}`
   - record preview：
     `{"record_id":"rec…","submit":false}`
   - 审批发起人由 workflow 部署配置解析；不得把人员标识写入用户回复或 skill 提示词。
   - 用户明确给出申请日期时可加入 `"run_date":"YYYY-MM-DD"`；未给出时省略，由 workflow 按 sandbox 步骤墙钟固定偏移 UTC+8 生成。
   - 仅当用户在当前对话明确说「正式提交」「确认提交」时把 `submit` 改为 `true`。
   - `email_username` 可省略；仅 ASCII 姓名会自动按小写、空格转点派生，中文名必须先询问邮箱前缀。
4. 用精确 canonical 名查询 workflow，然后只调用一次 `aevatar_start_workflow`：
   - `workflow_id` 使用查询返回的精确 id；
   - `inputs.prompt` 使用第 3 步的非空序列化字符串；
   - `wait` 设为 `complete`。
   不得传空串、对象或用户原句，也不得把内部 JSON 发给用户。
5. 等待 committed 终态并读取 typed artifact。只从 artifact 生成用户回复；工具 receipt、Bot 中间文案或 202 都不算成功。
6. preview 允许只读 Employee Master、联系人和审批历史；不得创建审批。submit 只有在完整查重通过且 `ready_for_submit=true` 后才创建一次审批。
7. preview 后正式提交时，复用 preview artifact 的 `run_date`，避免跨 UTC+8 午夜改变查重窗口或 UUID。submit 请求带确定性 UUID，但审批创建后的网络或回读失败仍可能是 partial failure。任何 submit 失败都不得自动重试；先让人工到 Lark 审批中心核对。

## 业务字段

Inline 入口：

| 用户会说 | 内部字段 | 规则 |
|---|---|---|
| 姓名，如 Lin Xiaoyu / 林晓雨 | `lark_name` | 原样 |
| 部门 | `department` | 原样 |
| 入职日期 | `onboarding_date` | 规范为 `YYYY-MM-DD` |
| 邮箱前缀 | `email_username` | 小写；ASCII 姓名可自动派生 |
| 申请日期 | `run_date` | 可选；未提供不追问 |

Record 入口由自动化提供 `record_id`；审批发起人来自 workflow 部署配置。不要要求业务用户填写这些内部字段。

## 回复格式

Preview 且 `ready_for_submit=true`：

> 📮 **入职邮箱审批预览 — {name}**
> 拟开通邮箱：**{new_email}**
> 申请日期：{run_date}
> 审批文案：{approval_detail_preview 原文}
> ✅ 查重已完成，本次未创建审批。内容无误的话，回复「正式提交」即可发起。

Preview 且 `ready_for_submit=false`：

> ⚠️ **暂不能提交 {name} 的入职邮箱审批**
> 系统发现已有待处理/已批准申请，或查重尚未完整完成。
> 本次没有创建审批，请先让 HR 在 Lark 审批中心核对。

Submit 且 `partial_failure=false`：

> ✅ **{name} 的入职邮箱审批已创建**，当前状态：{approval_status}。
> ⚠️ 已产生真实审批，请勿重复提交。

Submit 且 `partial_failure=true`：

> ⚠️ 审批可能已经创建，但状态回读失败。请先到 Lark 审批中心核对，**不要重试**。

禁止回显 operator、recipient、document URL、Base token、记录 ID、审批实例号，以及 run/actor/service/message/file 等内部标识。

## 失败处理

- Employee Master 读取失败：请用户联系 Base owner，确认 ChronoAI Lark 应用具有文档访问权，且目标表的高级权限角色已对该应用生效；不要建议绕过 ACL。
- 姓名无法安全派生邮箱：只询问邮箱前缀。
- 操作者缺失：报告「审批发起人配置缺失」，不要向业务用户索要内部 ID。
- 查重分页或明细扫描不完整：保持 preview，不允许 submit。
- 审批创建或回读失败：说明审批可能已经建立，要求先人工核对，绝不自动重试。
- 启动输入错误：修正 agent 自己构造的内部输入；仅 preview 可以重试一次，仍不得向用户展示 JSON 或原始引擎错误。
