---
name: question-authoring-ctal-ta
description: CTAL-TA (ISTQB テストアナリスト) の問題集に問題・解説を追加/修正するときの試験固有ルール（9 セットの構成、セットごとに違うカテゴリ名、source_ref に -a- が入る罠）。「CTAL-TAの問題を追加して」「テストアナリストの問題集を作って」で使う。共通ルールは question-authoring スキルにある。
---

# CTAL-TA（ISTQB テストアナリスト）

**先に `question-authoring` スキル（共通ルール・適用手順）を読むこと。** ここは試験固有の情報だけ。

このファミリーは**セットごとに性格もカテゴリも違う**ので、書く前に対象セットを確定させる。

## 科目（9 セット・計 390 問）

| slug | 名前 | 問題数 | カテゴリ体系 |
|---|---|---|---|
| `ctal-ta` | Set A | 45 | 章立て（Ch1-5） |
| `ctal-ta-b` | Set B | 45 | 章立て（Ch1-5） |
| `ctal-ta-c` | Set C | 45 | 章立て（Ch1-5） |
| `ctal-ta-d` | Set D | 45 | 章立て（Ch1-5） |
| `ctal-ta-f` | Set F（技法専科） | 40 | **技法別** |
| `ctal-ta-g` | Set G（技法応用編） | 30 | **技法別（発展）** |
| `ctal-ta-i` | Set I（本番形式フル模試） | 40 | 章立て（Ch1-6） |
| `ctal-ta-j` | Set J | 50 | 章立て（Ch1-6） |
| `ctal-ta-l` | Set L | 50 | 章立て（Ch1-6、Ch5 名が違う） |

`-e` / `-h` / `-k` は欠番。`istqb-ctal-ta`（初版・45 問）は**旧版なので触らない**（`ta-c-q01` 形式、`eg` キーを使う古い流儀）。

## source_ref

`<slug>-q<N>` — ゼロ埋めしない。

**Set A だけ罠がある**: slug は `ctal-ta` だが source_ref は `ctal-ta-a-q<N>`（`-a-` が入る）。他のセットは slug がそのまま前置される（`ctal-ta-f-q1`）。

## カテゴリ名（セットごとに違う。完全一致で JOIN）

Set A / B / C / D:
```
Ch1 テストプロセスにおけるTAのタスク
Ch2 リスクベースドテストにおけるTAのタスク
Ch3 テスト技法
Ch4 ソフトウェア品質特性のテスト
Ch5 レビューと欠陥分析におけるTAのタスク
```

Set I / J（上に Ch6 が加わる）:
```
Ch1 テストプロセスにおけるTAのタスク
Ch2 リスクベースドテストにおけるTAのタスク
Ch3 テスト技法
Ch4 ソフトウェア品質特性のテスト
Ch5 レビューと欠陥分析におけるTAのタスク
Ch6 テストツールと自動化
```

Set L（**Ch5 が「レビュー」だけ**。上の 2 つと違う）:
```
Ch1 テストプロセスにおけるTAのタスク
Ch2 リスクベースドテストにおけるTAのタスク
Ch3 テスト技法
Ch4 ソフトウェア品質特性のテスト
Ch5 レビュー
Ch6 テストツールと自動化
```

Set F（技法専科）:
```
同値分割
境界値分析
デシジョンテーブル
状態遷移テスト
組み合わせテスト
ユースケーステスト
経験ベース技法
技法選択・メトリクス
```

Set G（技法応用編）:
```
デシジョンテーブル（発展）
境界値分析（発展）
状態遷移テスト（発展）
組み合わせテスト（発展）
ユースケース・技法統合
欠陥分析・メトリクス（発展）
```

迷ったら DB に聞く:
```bash
db.sh query "select c.name from public.categories c join public.subjects s on s.id=c.subject_id
  where s.slug='<slug>' order by c.sort_order nulls last, c.name;"
```

## 解説の流儀

`asked` / `kid` / `terms` / `think` / `vs` / `opt` の 6 キーが 390 問すべてに入っている。`why_asked` / `snippet` は未使用。

## 内容の注意

- **390 問中 40 問が `code` 列を使っている**（デシジョンテーブル、状態遷移図、仕様の抜粋を読ませる形式）。技法系（Set F / G）で効く
- 20 問が `question_type='multi'`。`correct_indices` を忘れない
- 技法問題は「表を数える」形になるので、`code` に仕様、`opt` に各選択肢がなぜその数字になるかを書くと学習効果が高い
- 用語は JSTQB 用語集に合わせる（同値分割/同値クラス、境界値分析 など表記を既存問題と揃える）
