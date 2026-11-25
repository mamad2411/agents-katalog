---
name: improver
description: Self-Improvement の Improver skill。実行観測 (reasoning-bank / audit-log / routing_log / KPI / 失敗パターン) と人間フィードバックを集約し、Skill・Agent instruction・Workflow・Routing policy・Test strategy・Prompt・Docs の改善提案を、golden eval と回帰確認付きの PR として作る。main へ直接反映しない。
when_to_use: 同種の失敗や手戻りが 2 回以上観測された時、定期 (週次) の改善レビュー時、ユーザーが改善提案を求めた時。
allowed-tools: Read, Grep, Bash(node --test*), Bash(npm test*), Bash(git *), Bash(gh pr create *)
---

# Improver (ClaudeOS v10 Self-Improvement)

## Purpose
Base Skill → Execution → Observation → Feedback → Evaluation → Improver → Proposal → Regression Eval → PR → Quality Gate → Merge の後半を担う。

## Trigger
- `state.json.learning.failure_patterns` / `.claude/claudeos/data/reasoning-bank.json` に同一パターンが 2 回以上
- `execution.routing_log` で同じ task_type が繰り返し想定外の実行形態になっている
- 人間のレビューコメント (PR / Issue) に具体的な改善指示がある

## Inputs
観測データ (上記)、対象アーティファクト (skill / agent / workflow / router / test / prompt / doc)、現行 eval 結果 (`node --test scripts/agent-router.test.js` 等)。

## Procedure
1. 証拠を集め、「1 回の失敗」を永久ルールにしない (Repeated Evidence ≥ 2 を要求)。
2. 改善対象を 1 つに絞り、変更前の eval / テスト結果 (pass 率、失敗率、修復回数、トークン・時間) を記録する。
3. 変更を作業 branch で実装し、golden eval (`tests/evals/*.json`) とテストを再実行する。悪化する変更は採用しない (Regression Safety)。
4. 提案 PR を作成する: 証拠 / 変更 / eval 前後比較 / 想定リスク / rollback。`self-improvement` ラベルを付ける。
5. 自己改善結果は Approval PR 相当として扱い、人間のレビューなしに main へ反映しない。

## Validation
eval pass 率が変更前以上。既存テスト全 PASS。lint PASS。

## Failure Handling
証拠が 1 回分しかない、または eval が悪化する場合は提案を Issue 化するに留める。

## Output
改善提案 PR (または Issue)、eval 前後の比較表。
