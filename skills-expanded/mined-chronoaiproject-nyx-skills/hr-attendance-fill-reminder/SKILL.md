---
name: hr-attendance-fill-reminder
description: 考勤填写提醒。当用户说：考勤提醒、催填考勤、考勤填写、月底提醒、提醒大家填考勤、attendance reminder 时使用。生成月底考勤核对清单卡片预览；确认后可正式发送提醒。
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
    - reminder
---

# HR attendance fill reminder（考勤填写提醒）

Runs the canonical `hr_attendance_fill_reminder` workflow.

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
| 月份（如 2026年8月） | `period_label` | 字面 `2026年8月` |
| 离月底还有 N 天 / 距月末 N 天 | `days_left` | 字符串数字，如 `"3"` |

## Input template

Preview: `{"period_label":"2026年8月","days_left":"3","submit":false}`
Submit (explicit confirmation only): same with `"submit":true`.

## Reply template

Preview（artifact `mode=preview`）：

> ⏰ **{period} 考勤填写提醒预览**（距月末 {days_left} 天）
> —— 卡片文案 ——
> {card_text_preview 原文，保留换行与勾选框}
> ✅ 本次为预览，没有发送任何消息。文案无误的话，回复「正式发送」即可。

Submit（artifact `mode=submit`）：

> ✅ **{period} 考勤填写提醒已发送**。
> ⚠️ 重复执行会重复发送，请勿重跑。

**绝不回显**：接收人、文档链接、消息编号——这些是内部配置，与用户无关。

## Failure map

- `build_request`：缺少月份或剩余天数——向用户要。
- `summarize_submit`：消息被 Lark 拒绝，未送达——可核对配置后重试一次。
- 运行启动即失败且提示输入必须是 JSON：按第 3 步修正你的输入后重来（仅预览路径）。
