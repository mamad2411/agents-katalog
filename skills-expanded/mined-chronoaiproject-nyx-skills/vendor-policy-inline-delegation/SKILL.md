---
name: vendor-policy-inline-delegation
description: 验证 workflow_call 的 inline 子定义绑定、子运行与结果回传。用户提到“供应商政策 inline 委派审查”、对应英文名称或要求运行该验收 workflow 时使用。
version: "1.0"
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

# 供应商政策 inline 委派审查

使用随 skill 提供的 `vendor_policy_inline_delegation` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的完整定义集；只有挂载不可用时，才把父定义和 `vendor_policy_inline_evaluator` 子定义两个 YAML 同时作为 `workflow_yamls` inline fallback。禁止只传父定义。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `vendor_policy_inline_delegation`，`inputs.prompt` 设为 `运行合成供应商政策 inline 委派审查，不执行任何外部写入。`。
3. 此案例不需要附件。
4. 不得根据模型文案推断额外授权。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `success=true、inline_definition_bound=true、child_definition_resolved=true、child_workflow_completed=true、side_effects=false`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
