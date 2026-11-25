---
name: saas-research-to-prototype
description: 競合リサーチ、類似SaaS比較、既存プロダクトの現在地整理をもとに、B2B SaaSの機能ギャップをUI/UX、画面一覧、データ構造、最小MVPへ落とし込むときに使う。ユーザーが「このリサーチからプロトタイプを作りたい」「競合比較をUI要件に変換したい」「SaaSの画面設計に落として」「research-to-prototype」「saas-research-to-prototype」と依頼したときに使用する。
---

# saas-research-to-prototype

リサーチ結果を、そのまま実装可能な SaaS UI プロトタイプ計画へ変換する skill。

この skill の役割は、調査メモを増やすことではなく、以下の順に圧縮することにある。

1. 競合・類似サービスの事実整理
2. 対象プロダクトの現在地整理
3. ギャップ抽出
4. ギャップを機能へ変換
5. 機能を UI / UX とデータ構造へ変換
6. 最小 MVP と実装順へ分解

## 使う前提

- まず `memory/` にドラフトを置く
- 内容が固まったら `docs/` に昇格する
- 最初からフルプロダクトを設計しない
- 競合の機能名を真似るのではなく、ユーザー行動に翻訳する

## 入力として確認するもの

最低限、次のどれかがあること。

- 競合リサーチメモ
- 類似SaaSの比較資料
- 対象プロダクトの現在地メモ
- 改善したい画面やUXの要望

なければ、次を簡潔に確認する。

- プロダクト種別
- ターゲットユーザー
- 主要課題
- 参考にしたいUX

## 出力

この skill では、通常は以下の 2 本を出力する。

1. `memory/research-report-*.md` または `.html`
   - 競合比較、現在地、ギャップ、優先順位
2. `memory/ui-prototype-plan-*.md`
   - 画面一覧、主要コンポーネント、モックデータ、最小実装範囲

必要なら、同じ内容の `feature-system-brief` を追加で作ってよい。

## 標準ワークフロー

### STEP 1: 一次情報と推論を分ける

リサーチを読んだら、まず以下に分離する。

- 事実: 競合が実際に提供しているもの
- 解釈: その意味
- 仮説: 対象プロダクトに必要そうなもの

混ぜたまま先に進まない。

### STEP 2: 現在地を 3 行で定義する

対象プロダクトについて、次を短く確定する。

- 今の主価値は何か
- 今はどの仕事まで支援しているか
- 競合に対して、どの仕事が未対応か

### STEP 3: ギャップを機能名ではなく行動で定義する

悪い例:

- scorecard がない
- dashboard がない

良い例:

- manager が誰に介入すべきか分からない
- sales が会議後に次アクションを確定できない
- CRM に戻すため二重入力が発生する

### STEP 4: 各ギャップを 1 機能システムに変換する

各ギャップについて、最低限これを定義する。

- 誰が使うか
- 何を判断 / 実行するための機能か
- どの画面に置くか
- 必要な最小データは何か
- 最小UIは何か

必要なら [references/feature-system-brief.md](references/feature-system-brief.md) を読む。

### STEP 5: 画面一覧に落とす

次の単位まで落とす。

- Dashboard
- List
- Detail
- Drawer / Modal
- Settings
- Billing
- Analytics
- Calendar

SaaS らしい画面を並べるのではなく、行動に必要な画面だけ残す。

### STEP 6: 最小MVPを切る

最初の実装範囲は次の観点で絞る。

- 既存構造の延長で作れるか
- 価値が伝わるか
- 後から API 接続しやすいか
- モックデータで体験検証できるか

### STEP 7: UI プロトタイプ計画を書く

最終的に、以下を含む計画にする。

- 現在の構成理解
- 追加 / 編集ファイル
- コンポーネント設計
- データ構造案
- 実装ステップ
- リスク
- 最小実装範囲

必要なら [references/ui-prototype-plan.md](references/ui-prototype-plan.md) を読む。

## デフォルトの判断基準

- 競合のフル機能を再現しない
- まずは「読み返す」から「次に動く」への橋を作る
- まずは 3 画面で成立させる
- モックデータ実装しやすい粒度で切る
- 画面を増やすより、既存画面に 1 パネル足す方が速いならそちらを優先する

## 成果物の配置

- 作業中ドラフト: `memory/`
- 承認後の確定版: `docs/`
- 元資料やスクショ: `assets/research/`

## 参考ファイル

- レポート構成: [references/research-report.md](references/research-report.md)
- 機能システム定義: [references/feature-system-brief.md](references/feature-system-brief.md)
- UI 計画: [references/ui-prototype-plan.md](references/ui-prototype-plan.md)
- 叩き台テンプレ: `assets/templates/`
