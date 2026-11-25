---
name: hr-monthly-attendance-approval
description: 月度考勤审批。当用户说：月度考勤、考勤审批、考勤汇总、提交考勤、预览某月考勤、monthly attendance 时使用。读取考勤表并汇总人数/应出勤/离职/事假/病假，生成审批预览；确认后可正式创建审批并通知。
version: "6.0"
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
    - attendance
    - approval
---

# HR monthly attendance approval（月度考勤审批）

Runs the canonical `hr_monthly_attendance_approval` workflow.

## Invocation contract (agent-internal — the user never sees any of this)

Follow these steps exactly, in order, for every request this skill handles:

1. **Extract business fields** from the user's Chinese message using the field
   table below. Normalize dates like 「2026年8月17日」 to `2026-08-17` and month
   labels like 「2026年8月」 to the literal string `2026年8月`.
2. **Ask only for missing business facts**, in plain business Chinese
   (e.g. 「请问入职日期是哪天？」). Never mention JSON, input, parameters,
   workflows, skills, or tools in a question to the user.
3. **Build the run input yourself** as a single JSON object per the input
   template below. Then call `scope_workflows_get` with the exact workflow name
   to resolve the workflow, and call `aevatar_start_workflow` ONCE with:
   - `workflow_id`: the exact id returned by the lookup;
   - `inputs.prompt`: the input JSON **serialized to a non-empty string**
     (e.g. "{\"period_label\":\"2026年8月\",\"submit\":false}").
     NEVER pass an empty string, an unserialized object, or the user's
     sentence — the run rejects such input at start;
   - `wait`: "complete" — this suppresses the platform's raw result relay;
     YOU own the user-facing reply.
4. **Observe to terminal**: use `aevatar_observe_run` with the returned run/actor
   id until the run is completed, then `aevatar_read_workflow_run_artifact` to
   fetch the typed artifact. Compose the reply from the artifact only.
5. **Default to preview** (`submit: false`). Set `submit: true` ONLY when the
   user explicitly says 正式提交 / 正式发送 / 确认提交 in this conversation.
   Treat anything ambiguous (「提交吧?」「可以发了吗」) as preview and confirm
   first. The submit path has NO idempotency protection: never retry a failed
   submit — report and let a human check Lark first.
6. **Reply in natural business Chinese** using the reply template below.
   Absolute rules: no JSON, no key=value listings, no skill/workflow/tool
   names, and never echo recipient ids, document links, tokens, or any
   run/actor/service/message/file identifiers. Numbers and quoted texts must
   come verbatim from the artifact; write 「未返回」 for missing fields.
7. **On failure**: never show the engine's raw error. Explain in one Chinese
   sentence using the failure map below and say what the user can do next.

## Field table

| 用户会说 | 字段 | 格式 |
|---|---|---|
| 月份（如 2026年8月） | `period_label` | 字面 `2026年8月`（须与考勤表「月份」列一致） |
| 申请日期/运行日期 | `run_date` | `2026-08-31` |

## Input template

Preview: `{"period_label":"2026年8月","run_date":"YYYY-MM-DD","submit":false}`
Submit (explicit confirmation only): same with `"submit":true`.

## Reply template

Preview（artifact `mode=preview`）：

> 📋 **{period} 考勤审批预览**
> 人数 {stats.headcount} 人 ｜ 应出勤 {stats.workdays} 天
> 离职 {stats.resign_count} 人 ｜ 事假 {stats.leave_count} 人 ｜ 病假 {stats.sick_count} 人
> 数据完整性：{truncated=false → "✅ 完整" / true → "⚠️ 超出单页，正式提交会被拒绝"}
> —— 审批文案 ——
> {approval_description_preview 原文，保留换行}
> ✅ 本次为预览，未创建审批、未发送通知。请核对数字后再决定是否正式提交。

Submit（artifact `mode=submit`）：

> ✅ **{period} 考勤审批已创建**，状态：{approval_status}；
> 通知卡片：{notify_sent=true → "已发送" / false → "发送失败（审批已创建成功，请人工转告，不要重跑）"}。
> ⚠️ 已产生真实审批，请勿重复提交。

（不展示审批单号、接收人等编号类信息。）

## Failure map

- `aggregate`：考勤表读取失败 / 该月份没有匹配行 / 天数字段不是数字；提交时还可能因数据超页或应出勤为 0 被拒——向用户说明该核对考勤表哪里。
- `build_verify_request` / `build_notify_request` / `summarize_submit`：审批创建或回读校验失败——**审批可能已建立，先到 Lark 核实，不要重试**。
- 运行启动即失败且提示输入必须是 JSON：按第 3 步修正你的输入后重来（仅预览路径）。
