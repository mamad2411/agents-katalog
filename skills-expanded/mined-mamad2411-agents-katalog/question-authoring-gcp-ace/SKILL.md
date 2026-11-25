---
name: question-authoring-gcp-ace
description: GCP Associate Cloud Engineer (ACE) 弱点問題集に問題・解説を追加/修正するときの試験固有ルール（slug、カテゴリ名、m<M>q<NN> 形式の source_ref、解説未整備の 57 問）。「ACEの問題を追加して」で使う。共通ルールは question-authoring スキルにある。
---

# GCP Associate Cloud Engineer（弱点問題集）

**先に `question-authoring` スキル（共通ルール・適用手順）を読むこと。** ここは試験固有の情報だけ。

## 科目

| slug | 名前 | 問題数 |
|---|---|---|
| `gcp-ace` | GCP ACE 弱点問題集 | 168 |

セット分割していない唯一のファミリー。バッチ（`m<M>`）を足していく形で育っている。

## source_ref

**このファミリーだけ形式が違う。** `m<M>q<NN>` — `<M>` はバッチ番号、`<NN>` は問題番号。

現在 m2〜m7 まで使用済み。**次に足すなら `m8q01` から**（ゼロ埋め 2 桁）。

ゼロ埋めは**バッチによって違う**ので、既存に合わせるのではなく上記に従う。

| バッチ | ゼロ埋め | 例 |
|---|---|---|
| m2, m3 | していない | `m2q2`, `m3q1` |
| m4〜m7 | **している** | `m4q01`, `m6q01`, `m7q50` |

例外が 1 件ある: `m2q32b`（`m2q32` の派生問題として後から追加されたもの）。形式を踏襲する必要はない。

## カテゴリ名（完全一致で JOIN）

```
IAM・組織ポリシー
コンピュート・VM
GKE
ストレージ
ネットワーク
サーバーレス
監視・ログ
データ分析
運用・CLI
```

`docs/question-authoring.md` には「データベース・データ分析」「App Engine・Cloud Run」「ネットワーキング」も載っているが、**`00014_organize_subjects_and_categories.sql` で統合されて今は存在しない**。上の 9 個が正。

## 解説の流儀

`asked` / `terms` / `think` / `vs` / `opt` の 5 キー。`kid` / `why_asked` / `snippet` は未使用。

**168 問中 57 問は `explanation_data` が NULL**（初期の m2/m3 由来）。解説を厚くする作業をするなら、まずここが候補。

```bash
db.sh query "select source_ref, left(question_text,50) from public.questions q
  join public.subjects s on s.id=q.subject_id
  where s.slug='gcp-ace' and q.explanation_data is null order by source_ref;"
```

NULL 行に後付けする場合、`||` マージは NULL を吸収してしまうので `jsonb_build_object(...)` を直接代入する（共通スキルのマージ用 SQL は `explanation_data IS NOT NULL` が条件なので当たらない）。

## 内容の注意

- 「弱点問題集」なので、間違えた分野を潰す目的。汎用の網羅より、混同しやすい所を狙う
- `code` 列は未使用
- ロードマップ上、この試験が現在の主戦場（Phase C）
