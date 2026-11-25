---
name: deterministic-parallel-evidence-review
description: 验证 deterministic parallel 三路 worker、receipt 与 dispatch index 合并。用户提到“确定性并行证据审查”、对应英文名称或要求运行该验收 workflow 时使用。
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

# 确定性并行证据审查

使用随 skill 提供的 `deterministic_parallel_evidence_review` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的 workflow；只有挂载不可用时，才把随 skill 返回的 YAML 作为 inline fallback。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `deterministic_parallel_evidence_review`，`inputs.prompt` 设为 `并行核对三份合成供应商证据，不执行任何外部写入。`。
3. 此案例不需要附件。
4. 不得根据模型文案推断额外授权。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `success=true、worker_count=3、all_worker_receipts_observed=true、merged_output_order_verified=true、side_effects=false`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
