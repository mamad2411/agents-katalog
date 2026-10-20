---
name: refactor-instructions
description: コードベースを深く分析し、実装担当モデル(Codex/Opus等)へ渡す refactor-instructions.md(リファクタリング指示書)を生成する。分析モデル自身は実装しない。負債マップ・実装前質問・検証要件・監視プロトコルまで含めたハンドオフ文書を作る。Use when the user asks to analyze a codebase and produce a refactor handoff/instruction document for another implementation model, says 「リファクタ指示書を作って」「実装担当に渡す指示書」, or invokes /refactor-instructions. 監視の実行は refactor-monitor、文書の品質レビューは dual-review スキルと連携する。
metadata:
  origin: user-proven (Fable 5 refactor handoff workflow, 2026-06)
---

# Refactor Instructions — 分析 → 指示書 → 監視ハンドオフ

コードベースを分析し、実装担当モデルが安全にリファクタリングを完遂するための
**refactor-instructions.md** を作成するワークフロー。

- 指示書の雛形: [templates/refactor-instructions.template.md](templates/refactor-instructions.template.md)
- 分析チェックリスト詳細: [references/analysis-checklist.md](references/analysis-checklist.md)
- フィードバックログ雛形: [templates/refactor-instructions-log.template.md](templates/refactor-instructions-log.template.md)
- 関連スキル: 監視の実行は [[refactor-monitor]]、出荷前レビューは [[dual-review]]

## 役割の定義(最重要)

あなたは**分析者・指示書作成者**であり、実装者ではない。

- このスキル実行中は **コードを 1 行も変更しない**(読み取り系コマンドの実行は可)
- 成果物は Markdown 指示書のみ。人間がそれを実装担当モデル(Codex / Opus 等)に
  「refactor-instructions.md に書かれたことを完遂しろ」という形で渡す
  (呼び出し方法は実装担当の環境に従う。例: `codex <<EOF ... EOF`)
- 推測で判断しない。**証拠(file:line)にもとづいてのみ**記述する

## Phase 0: スコープと前提の固定

1. **スコープ確認**: リファクタ対象(全体 / 特定モジュール / 特定の負債種別)を特定。
   曖昧なら最初に確認する。大規模リポジトリではスコープ外は浅い把握に留め、
   Read の深掘りはスコープ内に集中する
2. **分析時点の固定**: `git rev-parse HEAD` で commit SHA を記録。非 git なら
   その旨を記録し、バックアップ手段の確保を質問に回す
3. **既存指示書の確認**: 既存の `refactor-instructions.md` があれば上書きせず
   version を繰り上げ、changelog を書く

## Phase 1: 証拠ベースのプロジェクト理解

確認するファイル・整理する項目・baseline 実測の規律は
[references/analysis-checklist.md](references/analysis-checklist.md) に従う。

### 証拠規律(常時適用)

- ファイルは **Read してから** 記述する。ファイル名からの推測で内容を語らない
- すべての主張に `file:line` の根拠を付ける。**根拠は記述した時点で Read 済みであること**
  (セルフチェックの「再検証」は出力直前の 2 回目の確認であり、初回の確認を免除しない)
- 推論には文末に `(inferred)` タグを付ける(Debt レコード内でも同様)
- 検証コマンドは設定ファイルから実在するものを引き、**分析時に実測**する。発明しない

## Phase 2: 技術的負債マップ

[references/analysis-checklist.md](references/analysis-checklist.md) の 14 観点で
負債を洗い出し、テンプレートの DEBT レコード形式(根拠 + anchor / 理由 / 影響範囲 /
リスク / 改善案 / 検証方法 / 実装可・提案のみ判定)で記録する。
「提案のみ」基準も同ファイル参照。

## Phase 3: 実装前に確認すべき質問

機能的に何が正しいか分からない場合は**勝手に決めない**。
必ず質問にする条件は [references/analysis-checklist.md](references/analysis-checklist.md) 参照。
**コードから判断できるものは質問しない。**

未解決質問が残る場合: 指示書冒頭に `STATUS: DRAFT` を明記し、回答に依存するフェーズに
`[BLOCKED ON Q-N]` を付けて着手不可と明示する。回答を受けたら改訂版
(version 繰り上げ)を発行し、DRAFT / BLOCKED を解除する。

## Phase 4: refactor-instructions.md の生成

[templates/refactor-instructions.template.md](templates/refactor-instructions.template.md)
を**コピーして全セクションを埋める**。セクションの削除・省略はしない:

メタデータ(version / 分析日 / commit SHA)→ 1 Objective → 2 Project Understanding →
3 Behaviors To Preserve → 4 Non-Negotiables(必須制約 + Dependency Policy)→
5 Stop And Ask Conditions → 6 Execution Environment & Setup →
7 Baseline Commands(verified / known failures / proceed condition)→ 8 Debt Map →
9 Implementation Phases(各フェーズに DEBT 対応 / depends_on / allowed files /
想定 diff 規模 / exit criteria / rollback plan)→ 10 Verification Requirements →
11 Reporting Format → 12 Out-of-scope → Monitoring Protocol

### Implementation Phases の推奨順序

1. 現在状態と検証コマンドの確認(baseline 記録)
2. 重要挙動にテストや再現手順がなければ**先に安全網を作る**
3. 明らかに安全な整理 → 4. 小さな責務分離 → 5. 境界・インターフェースの明確化
6. テストしやすい構造にする
7. 大きな設計変更は、承認なしに実装せず**提案に留める**

## Phase 5: 監視プロトコル

テンプレートの Monitoring Protocol セクション(完了ゲート / 提出証拠 / Red Flags /
介入手順 / 受け入れ判定)をプロジェクトの実態に合わせて具体化する。
**監視の実行は [[refactor-monitor]] スキルが担う**(指示書はその入力になる)。

## Phase 6: 実装結果のフィードバック

受け入れ判定後、[templates/refactor-instructions-log.template.md](templates/refactor-instructions-log.template.md)
の形式で `refactor-instructions-log.md` に記録する(DEBT 結果 / 判断待ち項目 /
新規負債 / Red Flag 原因)。次イテレーションの Debt Map・質問の種になる。

## 最終出力

1. **実装前に確認すべき質問**(必要な場合のみ)
2. **refactor-instructions.md 本文**(ファイルとして書き出す。保存場所未指定なら
   プロジェクトルート)

時間が許すなら、出荷前に [[dual-review]] で
「Fable=分析者視点 × Codex=実装者視点」のクロスレビューを通すと事故が減る。

## 出力前セルフチェック

- [ ] 自分はコードを変更していない
- [ ] 参照ファイルの存在は全件 Glob で確認。行番号の Read 再検証(2 回目)は
      「実装可」判定の DEBT と Behaviors To Preserve の根拠のみ必須
- [ ] Baseline Commands は実在し、verified ステータスが付いている
- [ ] テンプレートの全セクション + Monitoring Protocol が埋まっている
- [ ] 全 DEBT に「提案のみ / 実装可」判定と anchor 併記がある
- [ ] 冒頭メタデータ(version / 分析日 / commit SHA)がある
- [ ] 未解決質問がある場合、STATUS: DRAFT と [BLOCKED ON Q-N] が正しく付いている
- [ ] 質問リストに「コードから判断できる質問」が混ざっていない

## アンチパターン(絶対にやらない)

- 曖昧な「全部リファクタして」という計画にする
- 見た目の綺麗さを目的にする / 古いコードをすべて悪と決めつける
- 実装担当モデルが証拠なく大きな削除や全面書き換えをできる余地を残す
- 存在しない検証コマンドやファイルパスを書く(指示書のハルシネーションは実装事故に直結)
- テンプレートのセクションを「該当なし」の根拠なしに削る
