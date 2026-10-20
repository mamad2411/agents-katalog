# Snowflake CoCo プロンプト集

## このファイルの使い方

各ステップのプロンプトを **CoCo CLI** にコピー＆ペーストして実行します。

**CoCo CLI のはじめかた**:
1. コマンドプロンプトまたはターミナルで `cortex` コマンドを実行
2. CLI 上のテキストボックスにプロンプトを貼り付けて Enter

---
## Step 0: 環境、データ準備

### 目的
本ハンズオン用サンプルデータの初期構築タスクの実行

#### 以下、ターミナルで実行するコマンド

- 0-1. Snowflake CLI インストール確認
```
snow --version
```

- 0-2. Snowflake CLI 接続確認
```
snow connection list
```
```
snow connection test -c <接続名>
```

- 0-3. CoCo CLI インストール確認
```
cortex --version
```

- 0-4. CoCo CLI 起動
```
cortex
```
```
cortex -c <接続名> -w <作業ディレクトリ>
```

- 0-5. SQL ファイル実行
```
@setup.sql を実行して
```

## Step 1: データ探索

### 目的
各テーブル件数・サンプルデータ確認およびデータ整合性チェック

### プロンプト

- 1-1. 単一テーブルの概要把握
```
#SNOWRETAIL_DB.SNOWRETAIL_SCHEMA.EC_DATA このテーブルの概要を教えて
```

- 1-2. スキーマ内オブジェクト全体の概要把握
```
SNOWRETAIL_DB.SNOWRETAIL_SCHEMA この中のテーブルの概要を教えて
```

- 1-3. 簡易分析の実行
```
商品別売上上位5件を出して
```

- 1-4. 会話の文脈
```
ECのみで、月別に分けて見せて
```
```
ECの売上構成比を教えて
```

- 1-5. データ構造への示唆
```
SNOWRETAIL_DB.SNOWRETAIL_SCHEMA のデータ構造の問題点は何か、改善案を出して
```

---

## Step 2: Dynamic Table でデータ整備

### 目的
データ構造の問題点を解消するため、テーブルを結合・集計してデータマート用 Dynamic Table を作成する

### プロンプト

- 2-1. Dynamic Table作成計画の立案
```
MART_SALES という名前で Dynamic Table を作成したい。まずは計画を立てて。
```

- 2-2. 計画の確認、修正、実行
```
#EC_DATA #RETAIL_DATA #PRODUCT_MASTER を使って
```
```
商品名から類推してカテゴリ、ブランドのカラムを追加して
```
```
TARGET_LAGを1日にして
```

-2-3. 生成テーブルの確認
```
#MART_SALES 作成されたテーブルの件数と構造を確認して
```

---

## Step 3: AGENTS.mdでプロジェクトルール定義

### 目的
AGENTS.mdの Before/After 比較でソフトガバナンスの効果を体感する。

### プロンプト

- 3-0. 新しいセッションを作成（ここまでの文脈をリセット）
```
/new
```

- 3-1. Before（AGENTS.mdなし）の動作確認
```
チャネル別、カテゴリ別のクロス集計を出して
```

- 3-2. 新しいセッションを作成（文脈をリセット）
```
/new
```

- 3-3. AGENTS.mdの配置と内容確認
```
@samples/AGENTS.md を読んで、どんなルールが定義されているか説明して
```

- 3-4. After（AGENTS.mdあり）の動作確認
```
@samples/AGENTS.md を読んで、チャネル別、カテゴリ別のクロス集計を出して
```

---

## Step 4: Subagent + Swarm patternでバックグラウンド実行

### 目的

CoCo CLI のバックグラウンド実行機能を、汎用 Subagent → 専門化された Custom Agent → 並列 Swarm の順で体験します。

### 事前確認

今回用意している Custom Agent の定義ファイルが認識されていることを確認します。

```
/agents
```
期待される応答: Custom Agent を含む Subagent 一覧が表示されます。

> ファイルが見つからない場合は、プロジェクトルートに `cd` しているか確認してください。

### プロンプト

- 4-1. 汎用 Subagent をバックグラウンドで起動

```
general-purpose Subagent をバックグラウンドで起動して、次のタスクを実行してください。
タスク: #SNOWRETAIL_DB.SNOWRETAIL_SCHEMA.MART_SALES を分析対象とする Semantic View (Step 6 で使用) の設計案を提案する。
ビジネスでよく使われそうなディメンションを 5 つ、メジャーを 5 つ、それぞれ「論理名 / 物理カラム or 計算式 / 想定される利用シーン」の3点セットで列挙してください。
```

期待される応答: 汎用 Subagent をバックグラウンドで起動した旨の応答が返ります。

- 4-2. Custom Agent の構造を確認

```
@.cortex/agents/data-quality-checker.md を読んで、この Custom Agent について次の3点をそれぞれ1行で説明してください。
1) 専門領域（どんなチェックをするか）
2) 制約（使えるツール / 禁止操作）
3) 出力フォーマット
```

期待される応答: Custom Agent の専門領域・制約・出力フォーマットを整理した解説が返ります。

- 4-3. Custom Agent をバックグラウンドで起動

```
data-quality-checker Custom Agent をバックグラウンドで起動して、#SNOWRETAIL_DB.SNOWRETAIL_SCHEMA.MART_SALES のデータ品質チェック（NULL 率・整合性・孤立レコード・異常値）を実行し、サマリレポートを返してください。
```

期待される応答: Custom Agent をバックグラウンドで起動した旨の応答が返ります。実行が完了するとデータ品質のサマリレポートが返ります。

- 4-4. Agent 実行時に表示されるショートカットキー (Ctrl + S) を使って実行中の Subagent を確認

期待される応答: 4-1 と 4-3 で起動した Agent が一覧で表示されます。

- 4-5. Swarm pattern を使って並列実行

```
swarm pattern を使って、#SNOWRETAIL_DB.SNOWRETAIL_SCHEMA.MART_SALES の月次分析レポートを作成してください。
次の3つを並列の Subagent に分配してください。
(A) チャネル別・カテゴリ別の売上トレンド分析
(B) data-quality-checker による品質チェック
(C) (A)(B) の結果を統合した改善提案
```

期待される応答: 複数の Subagent を並列で起動した旨の応答が返ります。各 Subagent の処理が終わると統合レポートが返ります。

- 4-6. Swarm の進捗をショートカットキー (Ctrl + S) を使って確認

期待される応答: 4-5 で起動した複数の Subagent の進捗が一覧で表示されます。

- 4-7. Subagent と Swarm の違いをまとめる

```
ここまでで使った「汎用 Subagent」「Custom Agent」「Swarm pattern」の3つについて、誰が指示を出して誰が実行するかという観点で違いを表にまとめてください。
```

期待される応答: 3つの違いを整理した表が返ります。

---

## Step 5: Hooksでガバナンス

### 目的

ハードガバナンスとしての Hooks の仕組みを理解し、Step 3 の AGENTS.md（ソフトガバナンス）と組み合わせた二重防御の設計思想を体感します。

- AGENTS.md（Step 3）: お願いベース。LLM が従わなければ無視される可能性がある。
- Hooks（Step 5）: CoCo CLI が物理的にツール呼び出しをブロックする。

### Hooks の有効化（macOS のみ）

Hooks のブロックスクリプトは bash 製のため、**macOS 環境でのみ動作確認が可能**です。
Windows 環境の方は 5-1（構造の読み解き）のみ実施し、5-2（発火デモ）は講師の画面で確認してください。

macOS の方は、`samples/settings.json` を `.cortex/` にコピーして Hooks を有効化します。
なお、 `!` を先頭につけることで、コマンドを透過的に実行することが可能です。

```
!cp samples/settings.json .cortex/settings.json
```

> Finder や VS Code 等の GUI でコピー＆ペーストしても OK です。

新しいセッションを作成（Hooks を CoCo CLI に認識させる）
```
/new
```

コピー後、以下で配置を確認します。

```
!ls .cortex/settings.json .cortex/hooks/
```

`settings.json` と `.cortex/hooks/` 配下の3本のスクリプトが見えていれば OK です。

### プロンプト

- 5-1. Hooks の構造を読み解く

```
@samples/settings.json と @.cortex/hooks/ 配下のスクリプトを読んで、次の3点をそれぞれ1行で説明してください。
1) どのイベント（PreToolUse / PostToolUse）で何のスクリプトを発火させているか
2) どんなパターンを block しているか（SQL / Bash 別）
3) AGENTS.md と Hooks の二重構造でガバナンスがどう強化されるか
```

期待される応答: Hooks 設定の構造と各スクリプトの役割を整理した解説が返ります。

- 5-2.（macOS のみ・オプション）Hook の発火を体感する

Hooks を有効化済みの macOS 環境で、実際に書き込み SQL がブロックされる様子を確認します。

```
試験的に #SNOWRETAIL_DB.SNOWRETAIL_SCHEMA.EC_DATA に対して INSERT INTO EC_DATA VALUES ('TEST', '2025-01-01', 'P001', 't', 1, 1, 1) を実行してみてください。
```

期待される応答: Hooks によりブロックされた旨の応答が返ります。

---

## Step 6: Semantic View + Cortex AgentsでSI構築

### 目的
LOB（営業・マーケ等）がSnowflake CoWork で自然言語分析できる環境を作る。

### プロンプト

- 6-1. Semantic Viewの作成
```
#MART_SALES #CUSTOMER_REVIEWS を使って、
SNOWRETAIL_DB.SNOWRETAIL_SCHEMA.SNOWRETAIL_SV という名前でSemantic Viewを作成してください。また定義情報が格納したyamlファイルをsemantic_viewというフォルダ配下に、snowretail_sv.yamlという名前で出力してください。
もし、semantic_viewフォルダがない場合は新たに作成して。
```

- 6-2. cortex reflectで検証・デプロイ
```
今作成したSemantic Viewをreflectして
```

- 6-3. Cortex Search Serviceの作成
```
#SNOW_RETAIL_DOCUMENTS を使って、Cortex Search Serviceを
SNOWRETAIL_DB.SNOWRETAIL_SCHEMA.HANDSON_DOCS_SEARCH という名前で作成して
```

- 6-4. Semantic View + Cortex SearchをAgentに統合
```
Semantic View（SNOWRETAIL_SV）とCortex Search（HANDSON_DOCS_SEARCH）を
両方使うCortex Agentを
SNOWRETAIL_DB.SNOWRETAIL_SCHEMA.SNOWRETAIL_HANDSON_AGENT という名前で作成して
```

- 6-5. Snowsight上でSI体験（質問例）
```
作成したCortex Agentを使って以下の結果を取得してください。


問い合わせ内容：「チャネル別の月次売上推移を教えてください」
```

---

## Step 7: Skillでレポート生成を標準化

### 目的
スキル開発機能を利用して、スキルを開発する。

### プロンプト

- 7-1. ネイティブ Skill 開発機能の確認
```
/skill-development について教えて。どんな機能があるか一覧で説明して
```

期待される応答: CoCo がネイティブ提供する skill-development スキルの4つの機能（CREATE / SUMMARIZE / AUDIT / REFACTOR）が説明されます。Snowflake が公式に Skill 開発ワークフローをサポートしていることが確認できます。

- 7-2. 独自ドメインSkillの新規作成（対話的に作成）
```
新しい Skill を作成したい。以下の要件で作って：
- 名前: my-category-insight
- 目的: MART_SALES から指定カテゴリの売上・トレンド・前月比を分析し、1ページのマークダウンレポートを出力する
- トリガー: カテゴリ分析, category insight, カテゴリレポート
- 配置: .cortex/skills/ 配下
```

期待される応答: skill-development の CREATE フローに従い、要件確認 → 構造提案 → SKILL.md 生成の対話が進みます。途中の承認ポイントで「OK」「進めて」等を入力して進めてください。

> **💡 カスタマイズポイント**: 参加者ごとに異なるカテゴリ名や切り口を指定すると、全員が異なる Skill を作成できます。例：
> - `「食品」カテゴリに特化した週次トレンド分析`
> - `「家電」の季節別売上予測レポート`
> - `「衣料」のチャネル比較ダッシュボード`
>
> Skill名も自由に変更してください（例: `food-trend-report`, `electronics-seasonal`, `apparel-channel-compare`）。

- 7-3. 自作Skillの実行テスト
```
/my-category-insight Skill を使って、「食品」カテゴリの分析レポートを出して
```

期待される応答: 作成した Skill が発火し、MART_SALES から指定カテゴリの売上データを集計したマークダウンレポートが出力されます。

> **💡 カスタマイズポイント**: 7-6 で指定したカテゴリ名に合わせてプロンプトを変更してください。例：
> - `food-trend-report Skill を使って、今月の食品トレンドレポートを出して`
> - `electronics-seasonal Skill を使って、家電の季節分析を出して`

- 7-4. Skillの改良（参加者ごとのカスタマイズ）
```
/my-category-insight Skill に「競合カテゴリとの比較」セクションを追加して、SKILL.mdを更新して
```

期待される応答: SKILL.md のワークフローに比較ロジックのステップが追加されます。

> **💡 カスタマイズポイント**: 追加するセクションも自由に変えられます。例：
> - `「前年同月比の成長率グラフ」セクションを追加して`
> - `「売上下位5商品の改善提案」セクションを追加して`
> - `「チャネル別の構成比変化」セクションを追加して`

---

## Step 8: Streamlitでダッシュボード化

### 目的
ベースラインをCoCoで改修し、snow streamlit deployでSiSにデプロイする。

### プロンプト

- 8-1. ベースラインの確認
```
@steps/streamlit/streamlit_app.py を読んで、現状何が表示されるか説明して
```

- 8-2. CoCoで改修
```
このStreamlitアプリに以下を追加して：
・チャネル（EC/RETAIL）でフィルタリングできるセレクトボックス
・カテゴリ別の月次売上推移グラフ（折れ線グラフ）
・売上Top10商品の横棒グラフ
```

- 8-3. Snowflakeへのデプロイ
```
@steps/streamlit にある snowflake.yml を使って Streamlit をデプロイしてください。environment.yml の plotly 依存も含めてください。また実際の #MART_SALES のテーブル構造に従ってコードを修正してください。
```

- 8-4. デプロイ後の追加カスタマイズ（余力がある場合）

デプロイ後もプロンプトで直接 Streamlit の編集指示が可能です。例：

```
期間や商品カテゴリーを選択できるサイドバーを追加して
```

```
@step/streamlit にダウンロードした画像 dashboard_template.jpg のデザインに合わせてダッシュボードを編集できますか？
```

---

## [オプショナル] Step 9: MCPでデータ全体像を可視化

drawio.ioを利用するため、ローカル環境にneo4jが求められるため, ユーザによっては利用できない場合がございます。
したがって、こちらの章は**オプショナル**とします。

### 目的
draw.io MCPを使って、ハンズオン全体のデータ全体像をER図として可視化する。

### プロンプト

- 9-1. drawio MCPの接続確認
```
/mcp
```

または ターミナルで:
```
cortex mcp list
```

```
draw.io MCPに接続する方法を教えて
```

```
!cortex mcp add drawio npx -- @drawio/mcp
```

- 9-2. ER図の作成
```
#EC_DATA #RETAIL_DATA #PRODUCT_MASTER #MART_SALES #CUSTOMER_REVIEWS #SNOW_RETAIL_DOCUMENTS
draw.io MCPの open_drawio_mermaid を使って、これらのテーブルの関係をER図として可視化して
```

---

## Step 10: 振り返り + Pluginでチームに展開

### 目的
今日作ったもの（Skills、Hooks、MCP設定、Custom Agent）を1つの Plugin としてパッケージし、チームメンバーに一括配布できることを理解する。

> **Plugin とは**: Skills、Subagents、Hooks、MCP サーバーを1つのマニフェストにまとめたパッケージ。Git リポジトリで共有するだけで `cortex plugin install` 一発でチーム全員に展開できます。

### プロンプト

- 10-1. Plugin の作成
```
今日のセッションで作成した内容（Skills、Hooks、Custom Agent、MCP設定）を
1つの CoCo Plugin としてパッケージしてください。
Plugin名は snowretail-handson で、.cortex/plugins/ 配下に作成して。
```

期待される応答: Plugin のディレクトリ構造（`.cortex-plugin/plugin.json`、skills/、agents/、hooks/ 等）とマニフェストが自動生成されます。

- 10-2. Plugin の検証
```
!cortex plugin validate .cortex/plugins/snowretail-handson/
```

期待される応答: マニフェストと各コンポーネント（Skills、Agents、Hooks、MCP）の検証結果が表示されます。エラーがなければ OK です。

- 10-3. Plugin の再読み込み
```
/reload-plugins
```

期待される応答: Plugin のリストが再読み込みされること。

- 10-4. Plugin の読み込み確認
```
/plugin list
```

期待される応答: snowretail-handson Plugin が一覧に表示され、active 状態であることが確認できます。

- 10-5. Plugin の共有方法を確認
```
この Plugin を Git リポジトリで共有して、チームメンバーがインストールするまでの手順を教えて
```

期待される応答: `git push` → チームメンバーが `cortex plugin install <org>/<repo>` でインストールする流れが説明されます。
