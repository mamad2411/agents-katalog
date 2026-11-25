---
name: contractor-access-package-approval
description: 检查外包人员附件、历史去重并预览或创建审批。用户提到“外包人员访问资料审批”、对应英文名称或要求运行该验收 workflow 时使用。
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

# 外包人员访问资料审批

使用随 skill 提供的 `contractor_access_package_approval` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的 workflow；只有挂载不可用时，才把随 skill 返回的 YAML 作为 inline fallback。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `contractor_access_package_approval`，`inputs.prompt` 设为 `{"submit":false}`。
3. 当前请求必须带合成文本附件；让 aevatar_start_workflow 使用会话已登记的 input file refs。
4. 写入、审批或发消息分支必须由用户明确提出，并等待 typed tool approval；一般的检查请求只能走预览。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `资料完整且 preview 无写入；submit 需要明确授权`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
