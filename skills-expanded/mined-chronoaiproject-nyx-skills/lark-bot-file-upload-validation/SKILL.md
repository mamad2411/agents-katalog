---
name: lark-bot-file-upload-validation
description: 验证通过 Lark Bot 上传的文件、附件引用或 document_extract 主链。用户提到“Lark Bot 文件上传验证”、对应英文名称或要求运行该验收 workflow 时使用。
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

# Lark Bot 文件上传验证

使用随 skill 提供的 `lark_bot_file_upload_validation` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的 workflow；只有挂载不可用时，才把随 skill 返回的 YAML 作为 inline fallback。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `lark_bot_file_upload_validation`，`inputs.prompt` 设为 `验证当前消息中的合成上传文件，不执行任何外部写入。`。
3. 当前请求必须带 `lark-bot-upload-manifest.json`；直接入口只验证文件主链，只有同一 typed artifact 的 `lark_bot_ingress_validated=true` 才能证明 Lark Bot 入站附件链。
4. 不得根据模型文案推断额外授权。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `success=true；通过 Lark Bot 运行时还必须 lark_bot_ingress_validated=true`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
