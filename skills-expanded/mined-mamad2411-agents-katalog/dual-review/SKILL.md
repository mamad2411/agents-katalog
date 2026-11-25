---
name: dual-review
description: 成果物(スキル定義・指示書・設計文書・プロンプト・コード)を Codex と Fable の 2 つの独立した視点でクロスレビューし、指摘をマージして修正適用・確認ラウンドまで行う改善ループ。Use when the user asks for a two-sided / cross-model review(「両面レビュー」「codexとfableでレビュー」), or after authoring skills, agent definitions, instruction documents, or prompts that another model will consume. 片方のモデルだけのレビューでは視点の盲点が残るときに使う。
metadata:
  origin: user-proven (refactor-instructions dual review, 2026-06)
---

# Dual Review — Codex × Fable クロスレビュー改善ループ

同じ成果物を **2 つの独立した視点**でレビューし、指摘をマージして改善まで完了させる。
単一モデルのレビューは「作った本人と同じ盲点」を持つ。視点を分離することで、
生成側が気づけない欠落(消費者側の困りごと)を拾う。

- レビュープロンプト雛形: [templates/review-prompt.template.md](templates/review-prompt.template.md)
- Codex 呼び出しの実証済みパターン: [references/codex-invocation.md](references/codex-invocation.md)

## Step 0: モードの確認

依頼が **review-only**(指摘の提示まで)か **review-and-fix**(修正適用まで)かを判定する。
明示がなければ: 自分が作った成果物の出荷前チェックなら review-and-fix、
他人の成果物への評価依頼なら review-only を既定とする。
review-only の場合は Step 3 のマージ済み指摘を提示して終了する。

## Step 1: レンズ(視点)の設計

レビュー前に、成果物に応じた**相補的な 2 視点**を決める。同じ観点を 2 回やらない。

| 成果物 | Fable レンズ(例) | Codex レンズ(例) |
|---|---|---|
| 指示書・ハンドオフ文書 | 設計者: 矛盾・証拠規律・監視の実効性 | 実装者: 受け取って困る曖昧さ・欠落情報 |
| スキル/エージェント定義 | 実行モデル: 迷わず実行できるか | 別系統モデル: 暗黙前提・環境依存の検出 |
| コード | アーキテクチャ・保守性 | 正当性・エッジケース・回帰 |
| プロンプト | 意図の伝達・構造 | 誤読可能性・敵対的解釈 |

各レンズには「あなたは◯◯の立場である」というロール定義を必ず入れる。

## Step 2: 並行レビューの実行

**2 つのレビューは独立に・並行に走らせる**(互いの結果を見せない)。
プロンプトは [templates/review-prompt.template.md](templates/review-prompt.template.md)
をレンズごとに埋めて使う。

- **Fable 側**: Agent ツールでサブエージェントを起動
- **Codex 側**: [references/codex-invocation.md](references/codex-invocation.md) の
  基本形で `codex exec` を実行。**exit code 非 0 はそちら側のレビュー失敗**として
  原因を直して再実行する(片側だけで完了としない)

出力形式は雛形で統一されている(`[SEVERITY] file:line — 指摘 + 修正案必須`)。

## Step 3: 指摘のマージ

1. 重複する指摘を統合する(両者が同じ箇所を指摘 = 確度が高い。優先対応)
2. 矛盾する指摘は**証拠で裁定**する(どちらのモデルが言ったかではなく、
   対象ファイルの実態と成果物の目的に照らして判断)
3. 採用判定: CRITICAL / HIGH は必須対応。MEDIUM は成果物の目的に照らして判断。
   LOW は任意。**不採用にした指摘は理由を 1 行残す**

## Step 4: 修正の適用

- 修正は自分(メインセッション)で適用する。レビュアーには適用させない
- 採用した修正案をそのまま貼らず、成果物全体との整合(用語・構造・トーン)を取る

## Step 5: 確認ラウンド

- 修正した箇所に限定した再レビューを行う(全文再レビューは不要)。
  軽量に済ませるなら Codex 1 回 + 自分での通読で可
- CRITICAL / HIGH が 0 になるまで繰り返す。**最大 3 ラウンドで打ち切り**
  (収束しない場合は残指摘をユーザーに提示して判断を仰ぐ)

## Step 6: 機械的検証(レビューと別軸で必ず実施)

成果物の種類に応じた検証を最後に走らせる:

- スキル/エージェント定義: frontmatter 検証(name / description の存在、YAML 構文)。
  references/ templates/ への**相対リンクが実在するか**も確認する
- JSON / 設定ファイル: `jq -e` で構文 + 主要キーの存在確認
- コード: プロジェクトの build / lint / test(実在するコマンドのみ)
- 文書: 参照しているファイルパス・コマンドの実在確認(Glob / which)

## 報告形式

```markdown
## Dual Review 結果 — <成果物>
- Fable 側: N 件(C/H/M/L 内訳) / Codex 側: N 件(内訳) / 重複: N 件
- 適用: N 件 / 不採用: N 件(理由付き)
- 確認ラウンド: N 回で CRITICAL/HIGH ゼロ
- 機械的検証: <結果>
```

## アンチパターン

- 2 つのレビューに同じ観点を与える(視点が分離されず、二度手間になるだけ)
- 片方の結果をもう片方に見せてからレビューさせる(独立性が壊れ、追認になる)
- 指摘の列挙だけで終わり、修正を適用しない(review-and-fix モード時)
- 確認ラウンドを省略する(修正が新たな矛盾を生むことは普通にある)
- レビュアーの指摘を無検証で全採用する(裁定者はあくまで自分)
