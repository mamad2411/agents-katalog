---
name: question-authoring-terraform
description: HashiCorp Terraform Associate (004) の問題集に問題・解説を追加/修正するときの試験固有ルール（slug、カテゴリ名、source_ref、snippet の付け方）。「Terraformの問題を追加して」「テラフォームの解説を直して」で使う。共通ルールは question-authoring スキルにある。
---

# Terraform Associate (004)

**先に `question-authoring` スキル（共通ルール・適用手順）を読むこと。** ここは試験固有の情報だけ。

## 科目

| slug | 名前 | 問題数 |
|---|---|---|
| `terraform-associate` | HashiCorp Terraform Associate (004) — Set A | 50 |

新しいセットを足すなら `terraform-associate-b` のように続ける。

## source_ref

`terraform-associate-q<N>` — **ゼロ埋めしない**（`q1`, `q50`）。

## カテゴリ名（完全一致で JOIN。番号込みで書く）

```
1. IaC概念
2. Terraform基礎
3. コアワークフロー
4. 構成(HCL)
5. モジュール
6. State管理
7. インフラ保守
8. HCP Terraform
```

## 解説の流儀

全 50 問に `asked` / `why_asked` / `kid` / `terms` / `think` / `vs` / `opt` が入っている。新しい問題も揃える。

### 因果の背骨（`think` に「なぜその挙動になるか」を通す）
`explanation-clarity` の⑥。この試験の仕組み系＝**なぜ Terraform がそう振る舞うのか**。例: `count` は番号（index）でリソースを管理するから、途中の要素を消すと後続の番号がずれて再作成される（`for_each` はキー管理なのでずれない）／`plan` と `apply` を分けるのは適用前に差分を人が確認できるようにするため／依存グラフを自分で作るから明示的な `depends_on` が要らない／state があるから「あるべき姿」と現状の差分を出せる。`think` を挙動の羅列で止めず、「**内部の仕組み（state・依存グラフ・キー/番号管理）から、なぜその結果になるか**」を鎖でつなぐ。`snippet` の○×対比と噛み合わせると効く。**IaC の概念定義や用語の弁別など事実系には通さない。**

`snippet`（正しい書き方）は **50 問中 31 問**にだけ付いている。

- 付ける : HCL の書き方、コマンド、ブロック構文など**コードで示すのが最短**の問題
- 付けない : IaC の概念、HCP Terraform の役割など概念問題（19 問）。無理に付けるとノイズになる

`snippet` は解説側のコード。問題文と一緒に見せるコード（読ませて解かせる題材）は questions の `code` 列で、別物。

`snippet` の書き方は既存に合わせる。○×を対比させると効く。

```hcl
# ○ キーで管理されるので、途中を消しても他がずれない
resource "aws_instance" "web" {
  for_each = toset(var.names)
}

# ✗ count は番号管理。途中を消すと後続の index がずれて再作成される
# resource "aws_instance" "web" {
#   count = length(var.names)
# }
```

## 内容の注意

- **004 は現行版**。非推奨の書き方を正解にしない（`terraform taint` ではなく `terraform apply -replace=`、`moved` / `removed` / `import` ブロックは現行構文）
- 出典を確認するなら developer.hashicorp.com を引く（このリポジトリでは許可済みドメイン）
- 選択肢はコマンド名が似たものを並べると弁別力が上がる（`state list` / `state show` / `output` / `show -json`）
