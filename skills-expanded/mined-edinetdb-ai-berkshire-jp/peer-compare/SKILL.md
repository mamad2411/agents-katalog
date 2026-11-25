---
name: peer-compare
description: 同業種の複数企業（3〜5社程度）を横並びで比較し、業界内のポジショニングを整理する時に使う。「〇〇と△△を比較して」「この業界の主要企業を並べて」のような、複数社の比較指示で発火する。
---

# 同業比較

同一業種の複数企業を横並びで比較し、各社のポジションと差別化要因を整理する。全体の規律は `../../docs/research-discipline.md` を参照。

## 手順

### 1. 対象企業の確定
`search_companies_batch(queries=[...])` で比較対象企業をまとめて検索し、全社の `edinetCode` を1回の呼び出しで確定する。個別に1社ずつ検索すると取り違えに気付きにくいため、まとめて解決してから表にする（`docs/research-discipline.md` 規律1）。

業種で括る比較なら `search_companies(industry="対象業種")` で業種内の企業リストを取得してから対象を選定してもよい。

### 2. 業界の全体像
`get_ranking(metric="revenue")` で売上規模の分布、`get_ranking(metric="operating-margin")` や `get_ranking(metric="roe")` で収益性の分布を確認し、対象企業が業界の中でどのレンジにいるかを把握する。

### 3. 各社の財務データ取得
`get_financials(edinet_code=..., years=3)` を対象企業ごとに実行する（3年程度が比較には扱いやすい）。取得したら必ず全社を1つの表にまとめ、identifier・数値・出典を並べて目視確認する（規律のStep 2/3に相当）。

### 4. 各社の健全性・業界比較
`get_analysis(edinet_code=...)` で各社の健全性スコアと業界ベンチマークとの乖離を取得する。

### 5. 比較すべき指標
- 規模: `revenue`
- 収益力: `operatingMargin`, `roe`
- 成長性: `revenueGrowth`, CAGR系（`get_ranking(metric="revenue-cagr-3y")` 等）
- 安定性: `equityRatio`, `healthScore`
- 株主還元: `dividendYield`, `payoutRatio`

## 注意点

- IFRS総合商社・銀行・US GAAP企業は`operatingIncome`が構造的にNULL。比較表では空欄にせず「N/A（制度的非開示）」と明記する
- 自己資本比率の業種特性に注意する（金融業・不動産業は構造的に低くなる。同一業種内比較なら問題にならないが、業種横断比較では要注意）
- 会計基準（JP GAAP / IFRS / US GAAP）が異なる企業を比較する場合、指標の算出方法が完全に同一でない可能性があるため、比較表に会計基準列を必ず入れる

## レポート構成

1. 免責
2. 対象企業一覧（Identifier検証済み、会計基準付き）
3. 業界の概観（企業数、売上規模のレンジ、get_rankingでの主要プレイヤー）
4. 主要KPI比較表（N社×指標のマトリクス）
5. 業界内順位
6. 差別化要因の示唆（データから導ける範囲のみ）
7. データ品質メモ（N/A項目とその理由）
8. 使用ツールと呼び出し回数
9. データの鮮度
