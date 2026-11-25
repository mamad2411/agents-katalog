---
name: runtime-tool-approval-write-probe
description: 验证未声明风险 POST 的运行时 tool approval 挂起、恢复与真实写入回执。用户提到“运行时工具审批写入探针”、对应英文名称或要求运行该验收 workflow 时使用。
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

# 运行时工具审批写入探针

使用随 skill 提供的 `runtime_tool_approval_write_probe` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的 workflow；只有挂载不可用时，才把随 skill 返回的 YAML 作为 inline fallback。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `runtime_tool_approval_write_probe`，`inputs.prompt` 设为 `{"probe_note":"<当前 UTC 时间戳，8-14 位纯数字，例如 20260806>"}`。
3. 此案例不需要附件。
4. 本 workflow 没有预览分支：每次启动都会真实写入 Base 验收表（分别 1 条、2 条带探针前缀的可清理记录），并在每次写入前挂起等待 typed tool approval。必须由用户明确要求运行写入探针才可启动，并逐次等待用户批准；未获批准时保持 pending，不得代为批准或改走其他分支。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `mutation_executed=true、record_created=true；这是有副作用操作`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
