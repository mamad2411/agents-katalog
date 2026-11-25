---
name: email-access-approval-audit
description: 只读检查邮箱访问审批列表和实例详情。用户提到“邮箱访问审批审计”、对应英文名称或要求运行该验收 workflow 时使用。
version: "2.1"
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

# 邮箱访问审批审计

使用随 skill 提供的 `email_access_approval_audit` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的 workflow；只有挂载不可用时，才把随 skill 返回的 YAML 作为 inline fallback。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `email_access_approval_audit`，`inputs.prompt` 设为 `审计一条邮箱访问审批。`。
3. 此案例不需要附件。
4. 不得根据模型文案推断额外授权。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `instance_reachable=true、side_effects=false`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
