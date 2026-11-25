---
name: acceptance-fixture-drift-attestation
description: 只读体检验收 canary 数据是否漂移、fixture 是否完好。用户提到“验收 fixture 漂移体检”、对应英文名称或要求运行该验收 workflow 时使用。
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

# 验收 fixture 漂移体检

使用随 skill 提供的 `acceptance_fixture_drift_attestation` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的 workflow；只有挂载不可用时，才把随 skill 返回的 YAML 作为 inline fallback。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `acceptance_fixture_drift_attestation`，`inputs.prompt` 设为 `运行验收 fixture 漂移体检，不执行任何写入。`。
3. 此案例不需要附件。
4. 不得根据模型文案推断额外授权。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `reads_completed=true、fixtures_intact=true、side_effects=false`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
