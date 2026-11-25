---
name: refactor-monitor
description: refactor-instructions.md の Monitoring Protocol を実行する監視スキル。実装担当モデル(Codex/Opus)の作業をフェーズゲートで独立検証し、Red Flag 検査・受け入れ判定・フィードバック記録まで行う。Use when an implementer has completed a phase or the whole refactor and the work needs verification against the instruction doc, or the user says 「実装を監視して」「フェーズ確認して」「受け入れチェックして」. refactor-instructions スキルが生成した指示書を入力とする。
metadata:
  origin: dual-review of refactor-instructions (2026-06)
---

# Refactor Monitor — 指示書ベースの実装監視

[[refactor-instructions]] が生成した指示書の Monitoring Protocol を**実行する側**のスキル。
監視者(あなた)は実装担当の自己申告を鵜呑みにせず、自分でコマンドを実行して検証する。

## 役割の定義

- あなたは**監視者・受け入れ判定者**。実装の続きを自分で書かない
  (発見した問題は差し戻すのが原則。自分で直すのは 1 行未満の typo 級のみ)
- 判定はすべて**自分で実行したコマンドの結果**に基づく

## Phase 1: 前提の検証

1. `refactor-instructions.md` を Read し、メタデータ(version / commit SHA)を確認
2. `git rev-parse HEAD` と指示書記載の SHA を比較。実装開始時点が不一致なら
   file:line 参照がずれている可能性を報告
3. `STATUS: DRAFT` のままなら、`[BLOCKED ON Q-N]` のフェーズに着手していないか
   を最優先で確認する(着手していたら即 Red Flag)

## Phase 2: フェーズ完了ゲートの独立検証

対象フェーズについて:

1. 指示書の exit criteria のコマンドを**自分で実行**し、期待結果と照合する
2. baseline 実測値と比較する(テスト数・pass 数・lint エラー数が劣化していないか)。
   失敗が出た場合は指示書の Baseline Commands の **known failures(failure signature)と
   proceed condition を必ず照合**する: 既知の失敗は劣化に数えない /
   未知の失敗・proceed condition が `stop` のコマンドの失敗は即 STOP
3. `git diff --stat`(またはフェーズ単位の diff)を取り、指示書の
   allowed files / 想定 diff 規模と突き合わせる
4. **Dependency Policy の監査**: package 定義・lockfile・toolchain 設定・env 設定の
   変更有無を diff で確認し、変更がある場合は承認記録(報告+承認)の存在を確認する。
   未承認の依存変更は Red Flag として扱う

## Phase 3: 証拠の監査

実装担当の報告を Reporting Format と照合する:

- 各コマンドに cwd / command / exit code / 所要時間 / 要約(機密はマスク)が揃っているか
  (指示書の Reporting Format と同一の項目)
- 「テストが通った」報告に実行記録が添付されているか
- 触ったファイル → DEBT-NN の対応が記載されているか
- 報告と自分の検証結果が食い違う場合は、**自分の実測を優先**して報告する

## Phase 4: Red Flag 検査

指示書の停止トリガーを 1 つずつ確認する。発火したら介入手順に従う:

1. 実装を停止させる
2. 最後に green だったフェーズの状態まで rollback plan で戻す(または戻すよう指示)。
   **rollback の安全策**: 戻す前に `git status --short` を取り、差分を
   「フェーズの touched files / allowed files / それ以外(ユーザー変更等)」に分類する。
   実装担当由来と確認できる差分だけを reverse patch 等で個別に戻す。
   `git reset --hard` や `git checkout -- .` のような**一括破壊は禁止**。
   差分の所有者が判別できない場合は戻さず STOP してユーザーに報告する
3. 原因を分類: 指示書の曖昧さ → 指示書改訂(version 繰り上げ)を
   [[refactor-instructions]] に依頼 / 仕様不明 → 「実装前に確認すべき質問」に差し戻し /
   実装担当の逸脱 → 該当フェーズをやり直し

## Phase 5: 受け入れ判定(最終フェーズ完了後)

- [ ] Baseline Commands を全件再実行し、結果が baseline 実測以上。失敗は known failures と
      照合し、未知の失敗・proceed condition `stop` 該当があれば REJECT
- [ ] Behaviors To Preserve の該当テストがすべて green
- [ ] 全体 diff をレビューし、Out-of-scope・「提案のみ」項目に踏み込んだ変更が無い
- [ ] Reporting Format どおりの最終報告がある
- [ ] 未承認の allowed files 外変更が無い
- [ ] 未承認の依存変更(package / lockfile / toolchain / env 設定)が無い。あれば REJECT

判定は **ACCEPT / ACCEPT WITH NOTES / REJECT(差し戻し理由付き)** の 3 値で出す。

## Phase 6: フィードバック記録

`refactor-instructions-log.md` に記録する(無ければ作成):

- 各 DEBT-NN の結果: resolved / partially / deferred / rejected(+理由)
- プロダクト判断待ちの「提案のみ」項目
- 実装中に発見された新規負債
- 発火した Red Flag と原因(指示書の不備なら refactor-instructions スキルの改善点)

## 報告形式

[templates/monitor-report.template.md](templates/monitor-report.template.md) を
コピーして全項目を埋める(Gate / Baseline 比較 / Diff 監査 / 依存変更 / 証拠監査 /
Red Flags / 判定。REJECT・STOP には再現可能な証拠を必ず付ける)。

## アンチパターン

- 実装担当の「テスト通りました」を検証せずに信じる
- ゲート検証を省略して diff の見た目だけで判定する
- REJECT 理由を曖昧にする(差し戻しには必ず再現可能な証拠を付ける)
- 監視者が自分で実装を直してしまい、責任分界が崩れる
