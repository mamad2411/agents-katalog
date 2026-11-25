---
name: question-authoring-gh200
description: GH-200 (GitHub Actions 認定) の問題集に問題・解説を追加/修正するときの試験固有ルール（slug、カテゴリ名、gh200-q<N> 形式、YAML を code 列に置く流儀）。「GitHub Actionsの問題を追加して」「GH-200の解説を直して」で使う。共通ルールは question-authoring スキルにある。
---

# GH-200 (GitHub Actions 認定)

**先に `question-authoring` スキル（共通ルール・適用手順）を読むこと。** ここは試験固有の情報だけ。

## 科目

| slug | 名前 | 問題数 |
|---|---|---|
| `gh-200` | GH-200 GitHub Actions 認定 | 85 |

## source_ref

`gh200-q<N>` — **slug のハイフンが入らない**（`gh-200` ではなく `gh200`）。ゼロ埋めしない（`gh200-q1`, `gh200-q85`）。次は `gh200-q86` から。

## カテゴリ名（完全一致で JOIN。英語のまま）

```
Author and Manage Workflows
Consume and Troubleshoot Workflows
Author and Maintain Actions
Manage GitHub Actions for the Enterprise
Secure and Optimize Automation
```

## 解説の流儀

`asked` / `terms` / `think` / `vs` / `opt` の 5 キー。`kid` / `why_asked` は未使用。

`snippet` は未使用だが相性は良い（`on:` / `jobs:` の正しい書き方を示せる）。描画は実装済み。

## 内容の注意

- **85 問中 30 問が `code` 列を使っている**（ワークフロー YAML を読ませて解く形式）。このファミリーの中心的な出題形。YAML のインデントは `code` にそのまま入れれば `<pre>` で保たれる
- `multi` は 2 問だけ
- `needs` / `if` / `strategy.matrix` / `permissions` / `secrets` の挙動、再利用可能ワークフローと composite action の違いが作りやすい
