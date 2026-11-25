---
name: monthly-access-certification
description: 执行月末访问认证、提醒预览或明确发送提醒。用户提到“月度访问认证”、对应英文名称或要求运行该验收 workflow 时使用。
version: "3.1"
metadata:
  category: mixed
  output-type: text
  runtime:
    - aevatar-workflow
  tool-list:
    - aevatar_start_workflow
    - aevatar_read_workflow_run_artifact
  tag:
    - workflow
    - acceptance
    - aevatar
---

# 月度访问认证

使用随 skill 提供的 `monthly_access_certification` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的 workflow；只有挂载不可用时，才把随 skill 返回的 YAML 作为 inline fallback。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `monthly_access_certification`，`inputs.prompt` 设为 `{"mode":"preview","run_date":"2026-08-31","period":"2026-08"}`。
3. 此案例不需要附件。
4. 写入、审批或发消息分支必须由用户明确提出，并等待 typed tool approval；一般的检查请求只能走预览。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `预览只读；提交和消息分支需要明确授权`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
