---
name: investment-research
description: 特定の日本株1銘柄について、企業概要・セグメント経済性・財務トレンド・株主構成・ガバナンス・リスク要因・競争優位の仮説・バリュエーション素材までを網羅した総合リサーチレポートを作る時に使う。「トヨタを分析して」「〇〇の株を調べて」のように1社を深掘りする指示で発火する。
---

# 総合企業リサーチ

日本株1銘柄について、EDINET DB MCPを一次データ源とした総合リサーチレポートを作る。全体の規律は `../../docs/research-discipline.md` を参照（identifier解決・出典明示・取得不可の扱い・既知の落とし穴は共通ルールとして必ず守る）。

## 手順

### 1. Identifier解決
`search_companies(query="対象企業名")` で検索し、`edinetCode` を確定する。複数候補が出た場合は法人格・事業内容で本人を特定する。以降の全ツール呼び出しはこの `edinetCode` を使う。

### 2. 企業概要
`get_company(edinet_code=...)` で商号・証券コード（5桁生値→4桁表記に変換）・業種・会計基準・上場区分・従業員数を取得。`get_subsidiaries(edinet_code=..., min_match_score=2)` で国内子会社・持分法適用会社を確認する。**海外子会社は法人番号を持たず `matchScore=-1` になるため、`min_match_score` 指定だけでは丸ごと除外される**。海外売上比率が高い企業や海外生産拠点がある企業では、`get_subsidiaries(edinet_code=..., country="foreign")` を別途呼び出して主要海外子会社（連結売上高10%超の特定子会社等）を見落とさないようにする（規律6参照）。

### 3. セグメント経済性
`get_segments(edinet_code=...)` でセグメント別の売上・利益・利益率・YoYを取得。「No segment data」が返る場合は単一セグメント会社であり、これは異常ではない。セグメント構成比の合計が100%に届かない場合は、調整額・消去が個別開示されていない旨を注記する（規律6参照）。

### 4. 財務5年トレンド
`get_financials(edinet_code=..., years=5)` で売上・営業利益・純利益・ROE・自己資本比率・EPS・BPS・営業CF・配当・配当性向の時系列を取得。トレンドの方向（改善/悪化）に着目し、断定できない因果は「取得不可」と書く。

### 5. 直近決算
`get_earnings(edinet_code=..., limit=8)` で直近の決算短信を取得。進捗率と予想比較の扱いは規律6の「決算短信の期間スコープ」を厳守する。

### 6. 株主・ガバナンス
- `get_major_shareholders(edinet_code=...)` — 有報ベースの大株主上位10
- `get_shareholder_categories(edinet_code=...)` — 株主区分別構成
- `get_shareholders(edinet_code=...)` — 大量保有報告書（規律6の別物注意を厳守）
- `get_directors(edinet_code=...)` — 役員一覧
- `get_director_compensation(edinet_code=...)` — 役員報酬内訳（総額は`get_financials`を正とする、規律6参照）
- `get_cross_shareholdings(edinet_code=..., fiscal_year=...)` — 政策保有株式（開示なしの会社も多い）
- `get_related_party_transactions(edinet_code=...)` — 関連当事者取引
- `get_text_blocks_structured(edinet_code=..., element_type="governance_board")` — ガバナンス構造（regex抽出のため`get_directors`の実数と食い違えば後者を優先）

### 7. リスク要因
`get_text_blocks_structured(edinet_code=..., element_type="risk_items")` で有報「事業等のリスク」を取得。項目を列挙し、対応策の記載があれば併記する。

### 8. 業界内ポジション
`get_industry_benchmark` またはget_analysisのbenchmarkセクションで同業種中央値と比較し、ROE・利益率・自己資本比率の相対位置を確認する。

### 9. 直近イベント
`get_events(edinet_code=..., ...)` で直近のコーポレートイベント（M&A・自己株式・大量保有変更・役員人事等）を確認する。日付範囲指定でサイズ超過エラーが出たら範囲を絞る。

### 10. 競争優位の仮説
取得済みデータから論理的に導けるものだけを書く。一般知識・推測での補完は禁止（規律4）。仮説は「〜の可能性がある」「〜と符合する」のように、データから導ける範囲でトーンを抑える。

### 11. バリュエーション素材
`get_financials` のEPS・BPS・PER・PBR相当・配当利回りの時系列を表にする。有報提出時点の株価ベースでありリアルタイムではない旨を注記する。目標株価・売買推奨は書かない。

## レポート構成

1. 免責（`docs/research-discipline.md` 規律5）
2. Identifier（検証済み）
3. 企業概要
4. セグメント経済性
5. 財務5年トレンド
6. 直近決算
7. 株主・ガバナンス
8. リスク要因
9. 競争優位の仮説
10. バリュエーション素材
11. データ品質メモ（取得できたもの／できなかったもの）
12. 使用ツールと呼び出し回数
13. データの鮮度

各セクションの数値には出典（ツール名+パラメータ、可能ならdocID）を付ける。
