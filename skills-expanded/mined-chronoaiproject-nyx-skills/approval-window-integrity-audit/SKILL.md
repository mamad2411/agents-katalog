---
name: approval-window-integrity-audit
description: 审计审批查询时间窗口是否过期、历史窗口陷阱或窗口重基线。用户提到“审批窗口完整性审计”、对应英文名称或要求运行该验收 workflow 时使用。
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

# 审批窗口完整性审计

使用随 skill 提供的 `approval_window_integrity_audit` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的 workflow；只有挂载不可用时，才把随 skill 返回的 YAML 作为 inline fallback。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `approval_window_integrity_audit`，`inputs.prompt` 设为 `{"epoch_now_ms":<当前 UTC 毫秒时间戳，例如 1786000000000>}`。
3. 此案例不需要附件。
4. 不得根据模型文案推断额外授权。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `success=true、reads_ok=true、active_window_covers_now=true；legacy_window_expired 如实上报`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
