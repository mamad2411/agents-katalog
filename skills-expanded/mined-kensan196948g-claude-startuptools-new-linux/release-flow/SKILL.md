---
name: release-flow
description: PR 作成から品質ゲート判定、自動マージ、Phase 2 (本番リリース)・Phase 3 (安定化) までの標準手順。PR を作る時、マージ可否を判定する時、リリース後確認をする時に使う。
when_to_use: 実装と検証が終わり PR を作成・更新する時。CI が通った後にマージ判定する時。マージ後の本番反映と安定化確認。
allowed-tools: Bash(git *), Bash(gh pr *), Bash(gh run *), Bash(npm test*), Bash(npm run *), Bash(bash bin/release-check.sh*), Read
---

# Release Flow (ClaudeOS v10)

## Purpose
品質ゲート付き自動マージ (組織方針 §5 / policy/github-release.md §16) を、手順を省略せず再現可能に実行する。

## Trigger
Phase 1 完了 (必須機能・lint/test/build・secret 露出なし・docs 整合・CI 成功) の後。

## Inputs
作業 branch、head SHA、テスト/CI 結果、migration の有無、影響範囲、rollback 手段。

## Procedure
1. `bash bin/release-check.sh` (または `--allow-dirty`) で git / README / .gitignore / test / lint を統合確認する。
2. PR 本文 12 項目を書く: 目的・背景 / 変更 / 対象外 / 影響 / テスト・CI / セキュリティ / migration・データ影響 / deployment / rollback / preview 確認 / 残課題・リスク / production-safe 判定。
3. `gh pr create` (Draft 可) → CI を確認 (`gh pr checks`)。失敗は原因分析→最小修正→再 push。head SHA が変わったら影響検証を再実行。
4. 高リスク変更 (policy/github-release.md §17、DB 破壊操作、security policy 緩和、自己改善結果) が含まれていれば Approval PR へ分離し `/approval-pr` へ。
5. 品質ゲート (CI 全成功 / lint・test・build / Critical・High 0 / secret なし / additive migration / PR 本文完備 / production-safe / head SHA 一致 / conflict なし) を全て確認したら `gh pr merge --auto --squash <PR>`。
6. マージ後 Phase 2: PR 番号・head SHA・対象資源を再確認 → tag / Release (規則がある場合) → 検証済み migration (直前に `bin/pg-ops.sh backup`) → ホスト側 systemd deploy → deployment ID・commit・時刻を記録。
7. Phase 3: health check、主要画面・API・業務フロー smoke、認証認可・DB 接続・整合性、logs・error rate、必要なら事前検証済み rollback、Issue / Project / release note 更新、最終報告 (`/final-report`)。

## Validation
`gh pr view --json mergeStateStatus,statusCheckRollup` が CLEAN / SUCCESS。Ruleset の必須チェック名が CI job 名と一致していること。

## Failure Handling
品質ゲート未達は自動マージせず修正・再検証を反復。自律解消できない場合のみ未達項目・原因・影響・修正計画を提示して「マージ判定：Y / N」で停止。rollback 後の自動再デプロイは繰り返さない。

## Output
PR URL、merge commit、deployment 記録、Phase 3 の確認結果 (PASS / FAIL / BLOCKED / NOT RUN)。
