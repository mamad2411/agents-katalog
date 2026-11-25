---
name: lark-contact-batch-resolution
description: 通过 contact batch_get_id 解析入职邮箱身份。用户提到“Lark 联系人批量解析”、对应英文名称或要求运行该验收 workflow 时使用。
version: "1.1"
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

# Lark 联系人批量解析

使用随 skill 提供的 `lark_contact_batch_resolution` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的 workflow；只有挂载不可用时，才把随 skill 返回的 YAML 作为 inline fallback。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `lark_contact_batch_resolution`，`inputs.prompt` 设为 `解析验收入职邮箱，只返回结果数量。`。
3. 此案例不需要附件。
4. 平台可能要求 typed tool approval，但业务契约无副作用；未得到明确批准时保持 pending。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `success=true、resolved_count=1、标识不回显`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
