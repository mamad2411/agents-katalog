---
name: "regmonkey-slide-skill"
description: "Author Quarto Reveal.js slide decks for the regmonkey-presentation site (style/revealjs.css). Use whenever the user wants to create, edit, or extend a slide in this repo — especially when they say 'スライド', 'qmd', 'deck', 'プレゼン', 'セクションを足して', '対比で見せて', 'AS-IS / TO-BE', or reference any house pattern (pentagon-box, square-box, hop-step-jump, info-box, summary, Index, Abstract)."
---


# regmonkey-slide-skill

このリポジトリのスライドは Quarto `.qmd` を Reveal.js にコンパイルする．デザイン本体は `style/revealjs.css`（名前付きコンポーネントが3000行以上）と `_extensions/`（カスタムショートコード）に存在する．生 HTML や独自クラスを発明すると壊れる．この Skill は規約を体系化し，新しいスライドが既存 24本以上の deck と同じ見た目になるよう保証する．

Skill の役割：

1. 既知のコンポーネントから始める（即興マークアップ禁止）
2. Quarto フェンス div 構文を厳密に守る（壊しやすい）
3. ハウスライティングルールに従う（1スライド1メッセージ，MMUF，`/` 区切り禁止）

## どのファイルをいつ読むか

- **`references/components.md`** — 名前付きコンポーネントの完全カタログ（pentagon/square ボックスの全サイズ，def-block，info/success/warning/caution/danger ボックス，hop-step-jump，horizontal-keypoints，summary ブロック，component-cards，tools-grid，mini-section，h2-submessage，border-bottom-headers）．インラインに無いコンポーネントを使うとき，または正確なサイズバリアントが必要なときに開く．
- **`references/utilities.md`** — `.font-07`〜`.font-20`，`.lh-07`〜`.lh-20`，`.padding-L-05`〜`.padding-L-20`，`.width-90`〜`.width-110`，`.position-left-XX`，`.checkmark`，`.squaredmark` のユーティリティとショートコード（`reveal_vspace`, `reveal_hspace`, `fas`, `bi`）．スペーシング・フォントサイズ調整やアイコン追加で開く．
- **`references/patterns.md`** — スライド種別単位のパターン（Index slide，Abstract slide，Summary slide，AS-IS/TO-BE のゴール設定，Research-proposal，書籍紹介，meta-data セクション扉）．コンポーネント単位ではなく*スライド種別*での要望が来たときに開く．
- **`references/wording.md`** — 推奨用語変換（`定石` → `一般的`，誇張語の事実ベース化，口語 → 書き言葉，等）．本文執筆中の語感チェックや推敲フェーズに開く．SKILL.md「ライティングルール」を補完する語彙レベルのチートシート．
- **`references/authoring-checks.md`** — 脚注の書き方，height overflow の検出と対処，render & 目視確認チェックリスト．**完了宣言の前に必ず開く**．
- **`subagents/slide-svg-generator.md`** — フローチャート・関係図・概念図など SVG を新規/リスタイルするとき．ハウススタイル（枠 `#0E3666` / 透明背景 / 黒文字 / viewBox 1920基準）の完全仕様・テンプレート・チェックリスト・アンチパターンを保持．SKILL.md には最小ルールのみ（`## SVG / フローチャート / 図` 参照）．
- **テンプレート群** — 即コピペ可能．**`templates/`（skill 配下）と repo 直下の `template/` はミラーではなく相補的**．下の表で場所を確認．書き直さずコピーして編集する．

迷ったらまず `references/components.md`．間違ったクラス名を選ぶのが最頻の失敗モード．

## 執筆ワークフロー

1. **そのスライドの役割を特定する．** ワンメッセージのテイクアウェイか，比較か，プロセスか，定義か，章扉か，サマリーか？役割がパターンを決める．
2. **パターンを選ぶ．発明しない．** 下のインラインチートシートと照合し，該当無しなら `references/patterns.md` と `references/components.md` をスキャン．
3. **テンプレートが当てはまるならそこから始める．** 下の表からコピーして中身を上書きする — 構造をゼロから書き直さない．
4. **MMUF（Main Message Up Front）で埋める．** H2 タイトルは結論を1文で言い切り，箇条書きはそれを支える．1スライド1メッセージ．2つ言いたいなら分割．
5. **完了宣言前に `references/authoring-checks.md` を開いて render → 目視 → PDF 確認を実施．**

## ライティングルール

順序が優先度．1〜6 は絶対遵守，7〜10 は better practice．

1. **1スライド1メッセージ．** H2（`##`）はそのスライドのテイクアウェイ文であって，トピックラベルではない．「モデル管理の自動化を MLflow 導入により実現」 — yes．「MLflow について」 — no．
2. **MMUF．** 結論先出し，根拠は後．箇条書きは「なぜ H2 が真なのか」を説明するもの．
3. **`/` をリスト区切りに使わない**（日本語散文の中で）．インラインで並列項目には `・` を，文として読ませるときは `、` に置き換える．`Python・SQL・R` または `Python、SQL、R` — yes．`Python / SQL / R` — no．（例外：コード・パス・URL の中はそのまま `/` でよい）
4. **`—`（em dash）より `：` を優先．** 日本語スライド本文で説明・補足・列挙を導く区切り記号は `：` の方が自然．`—` は英文リズムで和文では浮く．`評価の3観点：速度・精度・コスト` — yes．`評価の3観点 — 速度・精度・コスト` — no．（例外：英文 prose や見出しの subtitle，このルール文書のように `yes — no` の対比を示す場面はそのまま `—`）
5. **誇張・煽り表現を使わない．**「驚くほど」「劇的に」「圧倒的に」「魔法のように」「革命的」「完璧」「究極」「秒で」「あっという間に」「楽々」のような不自然な日本語は技術スライドの信頼性を下げる．代わりに具体的な数字・事実・構造で語る．`驚くほど単純` → `3ステップで済む`．`劇的に高速化` → `処理時間が80%減`．「シンプル」「明快」「自動」のような中立語は OK．迷ったら抜いて意味が変わるか確認．
6. **Quarto フェンス div はリテラルに書く．** リポジトリ CSS は特定クラス名をターゲットにしている．`:::{.pentagon-box-500}` は機能する；`<div class="pentagon-box-500">` は Quarto の処理を無効化．
7. **コードに `font-family` を設定しない．** `_quarto.yml` で `monofont: monospace` 指定済み．上書きするとサイト全体の見た目の一貫性が崩れる．
8. **H2 タイトルは32文字以内が望ましい．** 超えるとスライド最上部で折り返し視認性が落ちる．本体を短くまとめ，補足は直下の `[...]{.h2-submessage}` に逃がす．例：「MLflow を導入してモデル管理・実験ログ・成果物アーカイブを統合的に自動化する」（39字）→ H2「MLflow でモデル管理を自動化」（13字）+ h2-submessage「実験ログ・成果物アーカイブも統合的に取り込む」．
9. **対比は pentagon（左）× square（右）でペアにする．** Pentagon の右向き矢印が問題/AS-IS を square 側の解決/TO-BE へ視覚的に運ぶ．左右逆や Square 2つで対比しない．
10. **既出スライドのレイアウトを再利用する．** 同じ deck 内で「N項目を並列で見せる」シーンが複数回出るとき，**最初に確定したレイアウト（columns 比率・カラム数・ブロック種類・font-size）を踏襲**する．ユーザーが「○○スライドと同じレイアウトで」と言ったら，**新しく組み直さずに当該スライドを Read して構造をコピーし中身だけ差し替える**．似て非なる構成（3列のものを2列に変える，`horizontal-keypoints-block` を `info-box` に変える等）は redo を要求される原因の最頻出パターン．用語例：「4つのルールと同じレイアウト」「パターン1と同じレイアウト」が来たら **既存スライドの構造を保存** が第一義．


## Quarto フェンス div 構文

colon の数が重要．**外側ラッパーは内側より多くの colon を必要とする．** 2カラムレイアウトの中に2つのボックス，さらにその中にヘッダー div を入れた場合：

```
:::::: {.columns}                  <- 6 colons, outermost
::::: {.column width="50%"}        <- 5 colons
::::{.pentagon-box-500}            <- 4 colons
:::{.border-bottom-header-left}    <- 3 colons (innermost)
左カラムのヘッダー
:::
:::{.squaredmark}
- 箇条書き本体
:::
::::
:::::
::::: {.column width="50%"}
::::{.square-box-500}
... right column ...
::::
:::::
::::::
```

よくあるミス：閉じフェンス忘れ／同階層で同じ colon 数（Pandoc が混乱）／属性を間違った colon の後．**ネストが壊れたらパッチせず，テンプレートをコピー**．

## YAML frontmatter

すべての post はこのブロックで始まる．`filters` は必須．省略するとショートコード（`reveal_vspace`，`fas`，`bi`）が生テキストとして表示される．

```yaml
---
title: "<スライドの結論を1文で>"
subtitle: "<シリーズ名・サブタイトル>"
author: "Ryo Nakagami"
date: "YYYY-MM-DD"
categories: [<tag1>, <tag2>]
slide-number: true
filters:
  - reveal-auto-agenda
  - inject_anychart_js     # AnyChartを使わないなら省略可
  - regmonkey_slide_editing
auto-agenda:
  bullets: bullets
---
```

post ディレクトリは `posts/YYYY-MM-DD-<slug>/index.qmd`．`posts/_metadata.yml` と `_slide.yml` が format 設定の残り（revealjs，1600×900，Meiryo，MathJax 3 等）を供給するので post 内で重複指定しない．

## インラインパターンチートシート

大半のスライドはこの4パターンでカバーできる．記憶から使い，どれにも当てはまらない時のみ `references/components.md` に手を伸ばす．

**N項目をどの形で見せるか — 早見表：**

| 項目数 | 関係 | 推奨パターン | テンプレート |
|---|---|---|---|
| 2 | 対比（AS-IS / TO-BE，課題 / 対応） | Pentagon × Square | `pentagon-squared-box.qmd` |
| 2 | 並列（情報密度高め） | info-box 並列 | `info-box-with-two-cols.qmd` |
| 3 | 昇順成長（Jr→Mid→Sr 等） | hop-step-jump | `hop-step-jump.qmd` |
| 3 | 並列観点 | horizontal-keypoints（3列） | `three-horizontal-points.qmd` |
| 4-5 | 並列観点 | horizontal-keypoints（N列） | `horizontal-n-keypoints.qmd` |
| 3-6 | 連続プロセス（日次サイクル等） | step-arrow（active-phase-sm） | `step-arrow-process.qmd` |
| 5+ | 並列分類（カテゴリ整理） | yaml2table 3-4 列 | `summary-yaml2table.qmd` / `anti-pattern-table.qmd` |

**「Xスライドと同じレイアウトで」と言われたら**：新規に組み直さず，当該スライドを Read して構造をコピーして中身だけ差し替える（ライティングルール 10）．

### パターン1 — Pentagon × Square（対比）

**問題と応答，AS-IS / TO-BE，現状/目標，gap/bridge** のような関係．左に pentagon（矢印が右に向き答えを指す），右に square（答えがそこに置かれる）．

```
:::::: {.columns}
::::: {.column width="50%"}
::::{.pentagon-box-500}
:::{.border-bottom-header-left}
データ分析プロジェクトにおける課題
:::
:::{.squaredmark style="font-size: 0.9em"}
- 方針・手法・解釈が分析担当者個人に依存
  - 再現性・継続性が低下
- 分析プロセスが終わった段階で共有されがち
  - チーム全体の知見を方針策定に結び付けられない
:::
::::
:::::
::::: {.column width="50%"}
::::{.square-box-500}
:::{.border-bottom-header-left}
会話型データ分析の実現ステップ
:::
:::{.squaredmark style="font-size: 0.9em"}
- Step 1: RAP の観点で現状の知見を整理
- Step 2: 現状課題の洗い出し・言語化
- Step 3: 仮説や分析アプローチをワークショップで議論
:::
::::
:::::
::::::
```

サイズバリアント：`pentagon-box-{400,500,550,600,700}` を，同番号の `square-box-` とペアで使う．数字はボックス高さ（px）．`-500` がデフォルト．

### パターン2 — Hop-Step-Jump（3段階の進展）

**3つの段階・レベル・フェーズが昇順に左から右へ読める**ときに使う．Junior → Mid → Senior．Phase 1 → 2 → 3．順序のない比較には使わない．

```
:::::{.hop-step-jump-container}
::::{.step .step-1}
:::{.step-number}
ジュニアDS
:::
:::{.step-title}
分析ができる
:::
:::{.info-content}
- 実装スキル（Python・SQL・R など）
- 可視化・要約・特徴量エンジニアリングの基本技術
:::
::::
::::{.step .step-2}
:::{.step-number}
ミドルDS
:::
:::{.step-title}
分析を構想できる
:::
:::{.info-content}
- 問いの構造化・仮説立案・手法選定
- 分析計画とタスクの分解・優先順位づけ
:::
::::
::::{.step .step-3}
:::{.step-number}
シニアDS
:::
:::{.step-title}
プロジェクトを組織で推進できる
:::
:::{.info-content}
- PJマネジメント
- 顧客・社内ステークホルダーとの合意形成
:::
::::
:::::
```

### パターン3 — Info-box + 箇条書き（最頻出）

スライドが**フレームに囲まれた概念と支持箇条書きだけ**で済むとき．左の青いバーが「定義/テイクアウェイ」を意味する．

```
{{< reveal_vspace 0.5em >}}

:::{.info-box}

:::{.info-contents .font-10 .padding-L-05 .lh-12}

{{< reveal_vspace 0.25em >}}

- コーディングエージェントとは [LLMが自律的にコードを書き・実行・検証するAIエージェント]{.regmonkey-bold} のこと
- 「[計画 → 実行 → 検証 → 修正]{.regmonkey-bold}」のループを自走しタスク完了まで反復する
:::

:::

{{< reveal_vspace 0.3em >}}

[補足セクション見出し]{.mini-section}
```

ステータスバリアント：`.success-box`（緑），`.warning-box`（黄），`.caution-box`（オレンジ），`.danger-box`（赤）．内部構造は同じ．

**ルール**：`:::{.info-contents ...}` の直後が箇条書き（`-` 始まり）になるときは，最初のリスト項目の上に `{{< reveal_vspace 0.25em >}}` を 1 行入れて上端余白を確保する．`info-box` 系すべて共通．

### パターン4 — 複数ブロックの要約スライド

**Summary — yaml2table 3 列：** 各セクションが「**原則 + 具体アクション**」のセットで束ねられるとき，`.block-azureblue` の代わりに `templates/summary-yaml2table.qmd` を使う．category（短いラベル）/ rule（1 文の主原則）/ actions（プロセスとして読める動詞句リスト）の 3 列構造．推奨ルールと完全な解説は `references/patterns.md` §3．

## regmonkey_index（章立て・目次スライド）の主要オプション

`.regmonkey_index` の YAML は `js/regmonkey_index_summary.js` が render 時に処理する．以下のキーは知らないと毎回ユーザーに教えてもらう羽目になるので最低限覚える．

- `numbering: true` で `1.` `2.` … を自動付与．**`title:` 側で番号は書かない**（二重採番になる）．折返しは番号分の hanging-indent で左揃え．
- `bullet_position: 0.5em` で title 列と bullet 列の間隔を詰める（既定 `1em`）．「title と文字の間が空きすぎる」と言われたらこれを下げる．
- `bullet_fontsize: 0.85em` が 5-7 項目時の標準（既定 `1.5em` は密度が高い deck では大きすぎる）．
- `width: [48, 52]` のように title 列と bullet 列の比率を指定．`numbering: true` でも 48〜52% から始めて調整．

完全な仕様（`title_fontsize` / `title_position` / `children[].description` の型など）は `references/components.md` の Index slide セクション．

## スペーシング・サイズ・アイコン — クイックリファレンス

- ブロック間の縦余白：`{{< reveal_vspace 0.5em >}}`（`1em`，`2em`，`15%` 等）
- フォントサイズ：`.font-09`（= 0.9em）〜 `.font-20`．行送りは `.lh-12`（= 1.2em）等
- 左パディング：`.padding-L-05` 〜 `.padding-L-20`
- 幅・位置：`.width-110` でブロック幅 110%．`.position-left-20` と組み合わせて中央揃えを保つ
- FontAwesome：`{{< fas check-circle mr-2 text-blue-500 >}}`．Bootstrap：`{{< bi signpost-fill size=1.7em color=#428CE6 >}}`
- インライン強調：`[強調語]{.regmonkey-bold}`（#206f83 太字）．小見出し：`[見出し]{.mini-section}`（▶ 付き）

全リストは `references/utilities.md`．

## テンプレートリスト

| ユーザーの依頼 | テンプレート | 場所 |
|---|---|---|
| 対比 / 課題と対応 | `pentagon-squared-box.qmd` | `templates/` |
| 三段階の成長 / フェーズ展開（昇順） | `hop-step-jump.qmd` | `templates/` |
| N ステップの連続プロセス（日次サイクル等．矢印つなぎ） | `step-arrow-process.qmd` | `templates/` |
| 三つの観点を横並び | `three-horizontal-points.qmd` | `templates/` |
| 四つ以上の観点を横並び（4-5 列対応） | `horizontal-n-keypoints.qmd` | `templates/` |
| 概念の定義スライド | `concept-explanation.qmd` | `templates/` |
| 分析サマリースライド (4要素) | `analysis-summary.qmd` | `templates/` |
| Azure blue サマリー | `azureblue-summary.qmd` | `templates/` |
| 章扉・セクション開始 | `meta-data-slide.qmd` | `templates/` |
| 補遺セクション開始（`# Appendix` 扉） | `appendix-divider.qmd` | `templates/` |
| 書籍紹介 | `book-template.qmd` | `templates/` |
| 同じ枠の左右対比（情報密度高め） | `info-box-with-two-cols.qmd` | `templates/` |
| Lecture系トップページ（対象レベル・前提知識・必要環境＋目次） | `lecture-index-slide.qmd` | `templates/`|
| Summary（category × rule × actions の 3 列：ポジティブ向け） | `summary-yaml2table.qmd` | `templates/` |
| アンチパターン一覧（category × 観点 × ペイン の 3 列：ネガティブ向け） | `anti-pattern-table.qmd` | `templates/` |
| 番号付きタイトル付き info-box（2 列 × 3 行のグリッド） | `info-box-titled.qmd` | `templates/` |
| info-box + 箇条書き（パターン3 の起点） | `info-box-bullets.qmd` | `templates/` |
| ステータスボックス4種（success/warning/caution/danger） | `status-boxes.qmd` | `templates/` |
| YAML frontmatter のひな型 | `yaml-frontmatter.txt` | `templates/` |

**`lecture-index-slide.qmd` のサイドバー：** 3 枚の `.component-card-index` のタイトル（テンプレートでは `対象レベル` / `前提知識` / `必要環境`）は固定ではない．deck の趣旨に合わせて差し替えてよい．`{{< bi ... >}}` のアイコン（`bullseye` / `person` / `book` / `terminal` / `chat-square-text` 等）も内容に合わせて選び直す．カード数（2〜3 枚）も deck に合わせて調整可．

**deck の性質ごとの推奨カード構成：**
- **Lecture 系**（チュートリアル・ハンズオン）：`対象レベル` / `前提知識` / `必要環境`
- **ガイドライン系**（開発フロー・運用規約・ルール策定）：`モチベーション` / `Goal` / `前提条件`
- **分析・リサーチ系**（調査報告・実験まとめ）：`背景・課題` / `目的` / `前提・制約`

ガイドライン系のカード例（`posts/2026-05-25-git-development-flow/index.qmd` 参照）：
```qmd
::::{.component-card-index .pl-4 .pr-4 .pt-1 .pb-6 .border-blue-500}
:::{.flex .items-center .mb-2}
{{< bi chat-square-text size=1.7em color=#428CE6 >}}
### モチベーション
:::
- ブランチ運用が属人化し，チームで方針が揃わない
- コミット粒度・マージ戦略に共通認識がない
::::
```

## SVG / フローチャート / 図

スライドにフローチャート・関係図・概念図・タイムライン等を入れるときは **SVG で書く**．ラスター画像（PNG/JPG）と違ってテキスト検索でき，拡大しても粗くならず，本文と同じトーンで揃う．**詳細仕様・テンプレート・チェックリストは `subagents/slide-svg-generator.md` が保持．** 本セクションは最小ルールのみ：

- 枠線：`stroke="#0E3666"`
- 背景：`fill="none"`（透明）
- 全テキスト：`fill="#1A1A1A"`（黒）．`<style>` で一括指定し，個々の `<text>` に色 fill を書かない
- フォント：`Meiryo` を含む font-family を `<style>` で明示
- viewBox 幅は **1920 を基準**．`viewBox="0 0 1920 H"` と書き，embed `width="100%"` でスライド全幅 1600px に充てる
- 矢印・軸・点などの構造線も `#0E3666`（黒一色だと方向性がぼやけるため例外）

**埋め込み構文（.qmd 側）：**

```markdown
:::{style="text-align:center;"}
![](./<filename>.svg){fig-alt="<図の意味（1文）>" width="100%"}
:::
```

新規 SVG をゼロから起こす／既存 SVG をリスタイルする／矢印 marker やフォント指定の完全雛形が必要／完了前チェックリストが必要 — いずれかなら `subagents/slide-svg-generator.md` を開く．

## 完了宣言の前に — `references/authoring-checks.md` を開く

執筆ワークフロー step 5 の本体は別ファイルにある．以下を扱う：

- 脚注の書き方（`<!-- footer -->` 区切り，スライド末尾集約）
- 1600×900 のキャンバスで本文作業領域は約 650px しかない．overflow を起こしやすい5パターンと，対処の優先順位（削る → 分割 → 密度を下げる → サイズ変更 → font-size 直書き）
- render → 全スライド目視 → PDF 確認のチェックリスト

## よくある失敗モード（避けるべき）

- **対比に square を2つ使う．** Pentagon × square の視覚的な非対称性*そのものが*意味．Square 2つだと並列に読めて問題→答えに見えない．
- **YAML の filter を忘れる．** `regmonkey_slide_editing` と `inject_anychart_js` がないと `{{< fas >}}` のショートコードや AnyChart の可視化がリテラルテキストのまま表示される．
- **コードに `font-family` を設定する．** プロジェクトは敢えて汎用 `monospace` を使う．カスタム CSS やインラインスタイルで上書きしない．
- **散文の中で `/` を区切りに使う．** `Python / SQL / R` は誤．`Python・SQL・R` と書く．コード/パス/URL 内はそのまま OK．
- **フェンス colon 数の不整合．** ネストが壊れたらパッチではなくテンプレートをコピー．
- **`.yaml2table .yaml2table-custom-top` の第1列に `regmonkey-bold` を付ける．** 第1列は CSS 側で行ラベル用のスタイルが既に当たっており，`<span class="regmonkey-bold">…</span>` を重ねるとスタイル衝突・全行均一強調・意味の希釈が起きる．第1列は素のテキスト．`regmonkey-bold` は 2 列目以降の本文セル中で特定の語句を目立たせたいときだけ使う．詳細は `references/components.md` の Tables セクション．
- **yaml2table の YAML 値を `` ` `` で始める．** YAML 1.2 で `` ` `` は予約 indicator なので，配列要素の冒頭が `` `foo` `` だと js-yaml が `bad indentation of a sequence entry` で落ちる．`quarto render` は通るがブラウザコンソールに `pageerror` が出る．yaml2table の YAML 内では `` `foo` `` を **`<code>foo</code>` に置き換える**．詳細は `references/components.md` の Tables セクション．

## 新規パターンが必要なとき

`references/components.md`/`patterns.md` のどれにも当てはまらない場合：

1. それを明示的に伝える．既存コンポーネントで偽装しない．
2. 一番近い既存パターンを提案し，変形するか CSS を拡張するか確認．
3. CSS 拡張は `style/revealjs.css` を直接編集．関連クラス近く（`/* keypoints-block */` 等のセクションコメントを検索）に新クラスを追加し，既存命名規則（`-400`/`-500` のサイズサフィックス，`-left` の位置サフィックス）に従い，対応するフェンス div を `template/` 配下の新ファイルに定義して再利用可能にする．
