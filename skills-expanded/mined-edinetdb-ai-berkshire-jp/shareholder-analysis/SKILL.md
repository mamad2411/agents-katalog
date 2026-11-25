---
name: shareholder-analysis
description: 特定企業の株主構成・大量保有報告書・役員報酬・ガバナンス構造を深掘りする時に使う。「〇〇の株主構成を教えて」「大株主は誰」「アクティビストは入っているか」のような、企業統治・資本政策の観点の指示で発火する。
---

# 株主・ガバナンス深掘り

株主構成と企業統治を、有報の大株主データと大量保有報告書の両面から深掘りする。全体の規律は `../../docs/research-discipline.md` を参照。

## 手順

### 1. Identifier解決
`search_companies(query="対象企業名")` で `edinetCode` を確定する。

### 2. 有報ベースの大株主
`get_major_shareholders(edinet_code=...)` で大株主上位10を取得する。系列企業（取引先・グループ会社）が上位に入っていれば安定株主構成の材料として明記する。

### 3. 大量保有報告書
`get_shareholders(edinet_code=...)` で5%以上保有者の直近の変更報告を取得する。**`get_major_shareholders` とは別のデータソースであり集計方法・タイミングが異なるため、混ぜて1つの「大株主リスト」として扱わない**（`docs/research-discipline.md` 規律6）。保有目的欄（「経営参加を目的とした安定株主」「純投資、状況に応じ重要提案行為等」等）はアクティビスト性の判断材料になるため原文に近い形で引用する。

### 4. 保有目的の時系列変化
`get_shareholder_history(issuer_edinet_code=...)` があれば、同一株主の保有比率の推移を確認し、増加・減少・撤退のトレンドを見る（このツールに `edinet_code` という引数は無い。対象企業を軸に引く場合は `issuer_edinet_code`、特定の株主を軸に引く場合は `filer_edinet_code` を使う。いずれか、または `parent_group_id` の少なくとも1つが必須）。

### 5. アクティビストポジション
`get_activist_positions()` で既知のアクティビスト投資家のポジションと突合する。大量保有報告書の保有目的から「アクティビスト的関与の可能性」を推測した場合でも、本ツールで裏付けを確認していなければ「裏付け未確認」と明記する。

### 6. 株主区分別構成
`get_shareholder_categories(edinet_code=...)` で機関投資家・個人・外国法人等の構成比を取得する。

### 7. 役員一覧・報酬
`get_directors(edinet_code=...)` で役員一覧を取得し、大株主リストに役員本人・創業家が含まれるかを突合する。`get_director_compensation(edinet_code=...)` で区分別内訳を取得するが、**総額は `get_financials` の `directorRemunerationTotal` を正とする**（規律6の二重計上リスク）。ただし `directorRemunerationTotal` と `directorRemunerationHeadcount` の組み合わせ自体が、別々の区分（例: 総額は社内取締役区分、人数は社外役員区分）から取られている場合がある。`get_director_compensation` で全区分を合算した値・人数と突き合わせ、一致しなければその旨を明記する（規律6）。

### 8. ガバナンス構造
`get_text_blocks_structured(edinet_code=..., element_type="governance_board")` で取締役総数・社外比率・委員会設置状況を取得する。regex抽出のため、`get_directors` の実数と大きく食い違う場合は後者を信頼する。

### 9. 政策保有・関連当事者取引
`get_cross_shareholdings(edinet_code=..., fiscal_year=...)` と `get_related_party_transactions(edinet_code=...)` を確認する。開示なしの会社も多く、「開示なし」は取得不可ではなく正常な応答であることが多い。

## レポート構成

1. 免責
2. Identifier
3. 有報ベースの大株主上位10
4. 大量保有報告書（変更履歴・保有目的）
5. 株主区分別構成
6. 役員一覧・役員報酬
7. ガバナンス構造
8. 政策保有・関連当事者取引
9. 観察（創業家支配・安定株主構成・アクティビスト関与可能性等、データから導ける範囲のみ）
10. 使用ツールと呼び出し回数
11. データの鮮度
