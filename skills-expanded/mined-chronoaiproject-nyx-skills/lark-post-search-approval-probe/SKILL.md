---
name: lark-post-search-approval-probe
description: 验证 POST 搜索的 typed tool approval pending、resume 或 issue 3184 回归。用户提到“Lark POST 搜索批准恢复探针”、对应英文名称或要求运行该验收 workflow 时使用。
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

# Lark POST 搜索批准恢复探针

使用随 skill 提供的 `lark_post_search_approval_probe` workflow。

## 执行

1. 优先使用 `use_skill` 已挂载的 workflow；只有挂载不可用时，才把随 skill 返回的 YAML 作为 inline fallback。
2. 调用 `aevatar_start_workflow`，`workflow_id` 设为 `lark_post_search_approval_probe`，`inputs.prompt` 设为 `运行语义只读的 Base POST 搜索批准恢复探针，不修改任何记录。`。
3. 此案例不需要附件。
4. 必须从 typed pending event 或 read model 取得完整 approval identity；用户明确批准后只能发送 nested toolApproval resume，未批准或拒绝时不得执行 POST。
5. 使用返回的 `run_id` 调用 `aevatar_read_workflow_run_artifact`。只有 typed artifact 为 completed 且满足 `preview 为 effectiveRisk=write 且 approvalRequired=true；终态 success=true、approval_resumed=true、side_effects=false`，才能报告通过。

如果短 `run_id` 的 artifact 仍为 pending，必须如实报告 pending；不得把 accepted receipt、工具批准等待态或模型总结改写成成功。
