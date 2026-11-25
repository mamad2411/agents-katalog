---
name: invoice-ocr-policy-review
description: 从发票图片或 PDF 提取字段、归一化并检查历史重复。用户提到“发票 OCR 与策略审查”、对应英文名称或要求运行该验收 workflow 时使用。
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

# 发票 OCR 与策略审查

使用随 skill 提供的 `invoice_ocr_policy_review` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的 workflow；只有挂载不可用时，才把随 skill 返回的 YAML 作为 inline fallback。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `invoice_ocr_policy_review`，`inputs.prompt` 设为 `提取当前消息中的合成发票，归一化并检查重复；不要创建审批。`。
3. 当前请求必须带发票图片或文件；Assistant /api/chat 使用图片，direct workflow 验证可使用 PDF。
4. 不得根据模型文案推断额外授权。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `字段和归一化通过、精确重复 1 条、同供应商 2 条`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
