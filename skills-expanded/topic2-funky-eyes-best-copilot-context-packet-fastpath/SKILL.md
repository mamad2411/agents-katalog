---
name: context-packet-fastpath
description: "Use to prepare a minimal context packet for a delegated subtask or to consume a frozen packet without re-reading unrelated files."
---

# Context Packet Fastpath

Uses the six-block PM dispatch packet from `core-workflow-contract`. This skill lists all fields grouped by block for quick reference.

## Packet Fields (by block)

### 1. task_intent

`goal`, `user_provided_paths`, `user_intent_summary`, `expected_outcome`, `task_type` (`implementation | design_review | verification | fix | spec`), `work_mode` (`micro | standard | full`)

### 2. frozen_scope

`scope`, `non_goals`, `files_involved`, `changed_files`, `priority_files`, `already_read_files`, `dependencies`, `owner_lane`, `reviewer_lanes`, `write_set`, `parallel_group`, `review_package_ref`, `diff_ref`, `task_brief_ref`, `acceptance_ref`, `context_shards`

### 3. fact_packet

`authoritative_repo_facts`, `source_provenance_refs`, `reference_files`

### 4. execution_contract

`assumptions`, `tradeoffs`, `simpler_option_considered`, `constraints`, `acceptance_checks`, `verification_budget`, `search_hints`, `context_budget` (max files/shards before returning for scope widening), `model_policy`, `model_cost_boundary`, `cost_boundary`, `reviewer_input_boundary`, `reviewer_permission_boundary`, `final_independent_review`, `stop_conditions`, `forbidden_approaches`, `read_before_write_targets`

### 5. review_state

`review_followup_scope`, `previously_verified_items`, `review_lanes`, `ready_artifacts` (files, commands, screenshots, review outputs already produced)

### 6. output_contract

`required_artifacts`, `recommended_next_stage`, `dispatch_reason`, `retrieval_provenance`, `memory_refs`, `spec_refs`

## Artifact Reuse Contract

Use `artifact_refs` when evidence is shared across lanes instead of copying the content into each prompt:

```text
artifact_ref:
  kind: diff | context | verification | review | search_result | state_update | metric | evolution
  path_or_command:
  producer:
  scope:
  freshness_or_base_head:
  summary:
  recovery_note:
  sensitive_data_checked: yes | no | n/a
```

Delegates read artifact refs first and reopen search only when refs are stale, incomplete, contradicted, or outside `context_budget`.

## Token Cost Metrics

Track lightweight metrics when practical: `files_read`, `broad_searches`, `context_budget_used`, `artifact_reuse_count`, and `escalation_reason`. These are optimization signals only; do not hide raw failure evidence, verification output, or residual risk to make numbers look better.

## Rules

- Lean packet: enough for one small task.
- Full packet: needed only for cross-module or high-risk work.
- Prefer `micro` or `standard` packets when the file set and acceptance checks are already clear.
- Prefer file-backed refs (`review_package_ref`, `diff_ref`, `task_brief_ref`, `acceptance_ref`, `context_shards`) over pasting large diffs, logs, specs, screenshots, or repeated context into multiple agents.
- Do not include whole logs, whole specs, or unrelated memory.
- Include recovery pointers for omitted detail so a delegate can fetch only the needed shard.
- Include only the retrieval provenance needed to justify selected files.
- Include material assumptions and tradeoffs only when they affect implementation, routing, or verification; do not pad the packet with obvious facts.
- For code-editing packets, include read-before-write targets: the file public surface/exports, immediate caller/callee, and obvious shared utility/local pattern to inspect.
- For review packets, include allowed evidence and forbidden influence: no controller severity opinion, author merge recommendation, approval framing, or unverifiable status claim.
- If a delegate needs new files, return to PM to widen scope.
- A delegate must consume `task_type`, `user_intent_summary`, `review_followup_scope`, `previously_verified_items`, `ready_artifacts`, file-backed refs, `required_artifacts`, and `recommended_next_stage` before reopening search.
- A delegate should stop at `context_budget` and return `NEEDS_CONTEXT` instead of broad-scanning.
- A delegate should treat `authoritative_repo_facts` and `source_provenance_refs` as fixed context unless the packet says they are provisional.
- Follow the Specialist Ask Boundary from `core-workflow-contract`.
