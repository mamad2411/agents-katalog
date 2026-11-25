---
name: question-authoring-gcp-pca
description: GCP Professional Cloud Architect (PCA) の問題集に問題・解説を追加/修正するときの試験固有ルール（slug、セット構成、カテゴリ名）。「PCAの問題を追加して」「アーキテクトの問題集を作って」で使う。共通ルールは question-authoring スキルにある。
---

# GCP Professional Cloud Architect

**先に `question-authoring` スキル（共通ルール・適用手順）を読むこと。** ここは試験固有の情報だけ。

## 科目（6 セット・計 300 問）

| slug | 名前 | 問題数 |
|---|---|---|
| `gcp-pca` | GCP Professional Cloud Architect | 50 |
| `gcp-pca-b` | 第2弾 | 50 |
| `gcp-pca-c` | 問題集C | 50 |
| `gcp-pca-d` | 問題集D | 50 |
| `gcp-pca-e` | 問題集E | 50 |
| `gcp-pca-f` | 問題集F | 50 |

新しいセットは `gcp-pca-g` から。1 セット 50 問が定型。

## source_ref

`<slug>-q<N>` — **ゼロ埋めしない**（`gcp-pca-c-q1`, `gcp-pca-c-q50`）。無印セットは `gcp-pca-q1`。

## カテゴリ名（全セット共通・完全一致で JOIN）

```
設計・計画
インフラのプロビジョニングと管理
セキュリティとコンプライアンス
プロセスの分析と最適化
実装の管理
信頼性の確保
```

## 解説の流儀

300 問すべてに `asked` / `kid` / `terms` / `think` / `vs` / `opt` が入っている。新規問題も揃える。`why_asked` と `snippet` はこのファミリーでは使っていない（PCDE とは流儀が違う）。

## 内容の注意

- 9 問が `question_type='multi'`。`correct_indices` を忘れない
- `code` 列は未使用。PCA は設計判断を問う試験なので、コードではなく要件文で状況を作る
- 誤答は「技術的には動くが、要件（コスト・可用性・コンプライアンス）のどれかを壊す案」にすると試験の型に合う
