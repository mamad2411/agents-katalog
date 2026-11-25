---
name: agent-router
description: タスク特性 (種類・複雑さ・リスク・影響ファイル数・所要時間・並列度・security/database/deployment 影響) から Main / Subagent / Background Agent / Agent View / Agent Teams / Dynamic Workflow / Worktree を決定し理由を記録する。CTO が作業を分解・委任する直前に使う。
when_to_use: 新しい作業単位を始める前、複数の独立作業を並列化するか判断する時、Agent Teams や Dynamic Workflow を使うべきか迷った時。
argument-hint: '[task summary]'
allowed-tools: Bash(node scripts/tools/agent-router.js *), Bash(node .claude/claudeos/scripts/tools/agent-router.js *), Read
---

# Agent Router (ClaudeOS v10 Lazy Agent Architecture)

## Purpose

「必要な Agent だけ、必要な時だけ、必要な Context だけ」を守るため、Claude Code Native の実行形態を決定論的に選ぶ。
Agent Teams は「Agent 間の相互通信が本当に必要」な場合に限定し、同一ファイルを複数 Agent へ同時に割り当てない。

## Trigger

- CTO が作業単位を分解した直後 (Plan → Development の境界)
- 並列化・長時間化・大量調査のいずれかが見込まれる時

## Inputs

`task_type`, `complexity` (low|medium|high), `risk`, `files_affected`, `expected_duration_min`, `parallelism`,
`security_impact` / `database_impact` / `deployment_impact` (low|medium|high|critical), `needs_inter_agent_communication`, `shared_files`, `read_only`

## Procedure

1. 作業単位ごとに上記の入力を JSON にまとめる (不明値は保守的に high / true 側へ倒す)。
2. 決定を実行し、state.json の `execution.routing_log` に記録する:

```bash
node scripts/tools/agent-router.js --record --json '{"task_type":"feature","complexity":"medium","files_affected":8,"expected_duration_min":25,"parallelism":1}'
```

（配布先プロジェクトでは `node .claude/claudeos/scripts/tools/agent-router.js`）

3. `execution` に従って起動する:
   - `Main`: このセッションで実施
   - `Subagent`: Agent tool。読み取り専用なら `Explore`、実装なら `general-purpose`。結果だけを受け取る
   - `BackgroundAgent`: `claude --bg --name <task>` またはセッション内 `/background`。`worktree: true` なら `--worktree`
   - `AgentView`: 複数の `claude --bg` を起動し `claude agents` で監視。各作業は別 worktree
   - `AgentTeams`: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` の時のみ。3〜5 teammate、ファイル所有権を分割、先に plan 承認
   - `DynamicWorkflow`: `/workflows` または `ultracode` で fan-out + 相互検証。`workflowSizeGuideline` でコスト制御
4. `guardrails` を作業計画に転記する (Human Approval Gate / migration-risk / security-reviewer / 品質ゲート)。

### Managed Agents を補完先に含める場合 (opt-in)

入力に `managed` ブロックを付けると、低リスク・読取専用タスクに限り `ManagedAgent` が候補になる。ブロックが無ければ判定は従来通り。
Local が稼働中というだけでは選ばれない (`managed.requested=true` の明示要求か `managed.local_available=false` が必要)。
安全条件は fail-closed: `risk: "low"`、`read_only: true` に加え、`managed.data_sensitivity` (public / internal) を指定し、`managed.human_gate` / `requires_secrets` / `requires_external_network` を
明示的に `false` で渡す。省略・不明値は拒否される。
`managed.policy_denied=true` は安全上の拒否であり、別経路で回避しない。可用性・予算・重複の証拠収集と記録は
`scripts/tools/managed-agents.js route --json '<task>'` (ClaudeOS 本体リポジトリ) が行う。

## Validation

- `tests/evals/agent-router.golden.json` の全ケースが PASS (`node --test scripts/agent-router.test.js`)
- 決定理由が `routing_log` に残っている

## Failure Handling

- 入力が不足して判定が Main に倒れた場合は、そのまま Main で実施し、次回のために入力を補う
- Agent Teams が使えない (env 未設定 / 非対話) 場合は AgentView または Subagent へフォールバックし、理由を記録する

## Output

`{ execution, worktree, reasons[], guardrails[] }` と `state.json` の `execution.routing_log`
