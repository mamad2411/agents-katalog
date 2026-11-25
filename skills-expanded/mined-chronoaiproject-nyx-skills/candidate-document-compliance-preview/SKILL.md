---
name: candidate-document-compliance-preview
description: 检查候选人附件、材料完整性或隐私约束。用户提到“候选人材料完整性预览”、对应英文名称或要求运行该验收 workflow 时使用。
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

# 候选人材料完整性预览

使用随 skill 提供的 `candidate_document_compliance_preview` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的 workflow；只有挂载不可用时，才把随 skill 返回的 YAML 作为 inline fallback。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `candidate_document_compliance_preview`，`inputs.prompt` 设为 `检查当前消息中的合成候选人附件。`。
3. 当前请求必须带合成文本附件；让 aevatar_start_workflow 使用会话已登记的 input file refs。
4. 不得根据模型文案推断额外授权。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `五项材料布尔值全部为 true`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
