---
name: question-authoring-ccao-f
description: Anthropic Claude Certified Associate – Foundations（CCAO-F）の問題集（slug ccao-f）に問題・解説を追加/修正するときの試験固有ルール（公式7ドメインに配点比例したカテゴリ構成、問題文は英語、解説は日本語で小学生にもわかるレベル、全問viz図解）。「CCAO-Fの問題を追加して」「Claude認定の問題集を作って」で使う。共通ルールは question-authoring スキルにある。
---

# Claude Certified Associate – Foundations (CCAO-F)

**先に `question-authoring`（共通ルール・適用手順）と `explanation-clarity`（わかりやすさの方法論）を読むこと。ドリルの型は `question-authoring-kcna`（資格ドメイン準拠＋小学生レベルの噛み砕きのハイブリッド）を踏襲する。** ここは本問題集固有の情報だけ。

## この問題集の性格

**Anthropic公式のパートナー認定試験（Claude Certified Associate: Foundations Exam Guide, Version 1.0, 2026年7月発効, 試験コード CCAO-F）のドメインに準拠しつつ、解説は教養ドリル並みに小学生でも分かるレベルに振り切る。** 対象は「コンサルタント・セールス・デリバリーリード」＝開発者ではなく、業務でClaudeを使う人向けの基礎資格。KCNAと同じ「資格的な範囲設定」＋「stats-basics/linux-basicsと同じ噛み砕き」のハイブリッド。

- **問題文は英語。** 実際の試験が英語のため、問題文（`question_text`）・選択肢（`options`）は英語で書く。`code` 列を使う場合も英語
- **解説（`explanation_data` の全キー）は日本語で、小学生でも分かるレベルに振り切る。** ただし読者は大人の社会人なので漢字は普通に使う（stats-basics/kcnaと同じトーン）
- **全問に `viz`（1枚の図解SVG）を付ける。** これがこの問題集の看板。図なしの問題を足さない
- 読者はQAエンジニアだが、この試験は非エンジニア（コンサル・セールス）向けの内容なので、コード的な例え・専門用語の接地よりも「業務での使い方」の比喩を優先する（会議・提案書・メール下書きのような場面）
- 出典はAnthropic公式ヘルプセンター（support.anthropic.com）やAnthropic公式ブログの内容に沿わせる。API仕様の細部（開発者向け）ではなく、Claude.ai / Claude for Work の**業務ユーザー向け機能**が主戦場（Projects、Artifacts、モデル選択、システムプロンプト的な「カスタム指示」、知識ソースなど）

## 出題範囲（公式7ドメイン。配点比率に問題数を比例させる）

Anthropicの公式試験ガイドが公開する配点比率。第一弾（Set A）はこの比率に合わせて60問を配分する。

| # | ドメイン（公式名） | 配点 | 日本語の芯 | Set A 問数 |
|---|---|---|---|---|
| 1 | Prompting and Task Execution | 14% | 効果的なプロンプトの作り方、タスクの分解、反復改善、タスク類型（分析・調査・作成・ブレインストーミング）への適応 | 8 |
| 2 | Output Evaluation and Validation | 21% | 出力の正確性検証、ハルシネーション・バイアスの見抜き方、事実確認、出力形式の選択、人間レビューの要否判断 | 13 |
| 3 | Product and Model Selection | 12% | Claudeの機能選定（Projects/Artifacts等）、モデル階層（Haiku/Sonnet/Opus）の使い分け、コスト・速度・品質のバランス | 7 |
| 4 | Workflow Integration and Solution Design | 16% | 要件分析、既存ワークフローへの組み込み・再設計、ソリューション設計、ステークホルダーへの説明 | 10 |
| 5 | Configuration and Knowledge Management | 12% | Projectsの設定、知識ソース（ナレッジベース）の管理、カスタム指示（システム指示）の作成・保守 | 7 |
| 6 | Governance, Risk, and Responsible Use | 15% | 適切な利用場面の判断、データの機密性・プライバシー、AI利用方針の遵守、責任あるAI利用 | 9 |
| 7 | Troubleshooting and Optimization | 10% | 弱い出力の原因診断、フィードバックへの対応、効率の最適化 | 6 |

合計60問＝実際の試験の出題数と一致させる。増産するときも、この配点比率を維持したまま各カテゴリに追加する（特定ドメインだけ厚くしない）。

## 科目とセット構成

| slug | 名前 | 状態 |
|---|---|---|
| `ccao-f` | Claude Certified Associate – Foundations (CCAO-F) | Set A 60問 投入 |

1 subject に7カテゴリで持つ（kcna/stats-basicsと同じ方式）。カテゴリ名は完全一致でJOINするため、下記をそのまま使う（英語ドメイン名＋日本語の言い換えを併記）。

```
1. Prompting and Task Execution（プロンプト設計とタスク実行）
2. Output Evaluation and Validation（出力の評価と検証）
3. Product and Model Selection（製品・モデル選定）
4. Workflow Integration and Solution Design（ワークフロー統合と解決策設計）
5. Configuration and Knowledge Management（設定と知識管理）
6. Governance, Risk, and Responsible Use（ガバナンス・リスクと責任ある利用）
7. Troubleshooting and Optimization（トラブルシューティングと最適化）
```

sort_order は上記の番号-1（0始まり）。

## source_ref

`ccao-f-q<N>`（ゼロ埋めしない）。Set A は q1〜q60。次のセットを足すなら `ccao-f-b` のように subject を分ける（terraform-associate-b と同じ方式）。

## 問題の形

- 4択 single が基本。実際の試験は multiple-response（複数選択・設問文に選ぶ数が明示される）も含むため、**multiple-response 相当の問題は `question_type='multi'` で数問混ぜてよい**。選択肢文の冒頭や末尾に「(Select two.)」のように選ぶ数を明示する（本試験の作法に合わせる）
- 問題文（英語）は1〜3文。**業務シナリオから入る**（コンサルが提案書を作る、セールスが顧客向けメールを書く、デリバリーリードが導入を計画する、など）。無理にシナリオ化せず、素直な "Which of the following..." でもよい
- 誤答は「隣の概念」を置く（Projectsの知識ソースとチャット単発の添付ファイルの混同、Sonnet/Opus/Haikuの取り違え、ハルシネーションと単なる不正確さの混同、システム指示とユーザープロンプトの混同など）。共通ルールの長さ縛り（正解を単独最長にしない）を厳守
- `code` 列は基本使わない。プロンプト例を見せたいときは `snippet`（解説側）で短く示す

## 解説の流儀

kcna/stats-basicsと同じキー構成：

| 要望 | キー |
|---|---|
| 何がどういう意味か | `asked` + `kid`（ざっくり言うと） |
| たとえで直感 | `eg`（一番力を入れる。業務・日常の場面で） |
| なんのためにあるか | `why_asked`（「この考え方が無いと業務で何に困るか」） |
| どういうことに役立つか | `usecase`（実務のどの場面で効くか） |

加えて `point`（決め手1文）・`terms`（2〜4個）・`think`（因果の背骨。「なぜこの判断が正しいか」を鎖でつなぐ。プロンプト設計・モデル選定・ガバナンス判断のような"仕組み系"の問いに通す）・`vs`（隣接概念との違い。「ハルシネーション vs 単純な誤字」「Projects vs 単発チャット」「Sonnet vs Opus」など）・`opt`（選択肢と同数）・**`viz`（全問必須）**。

`snippet`（プロンプトの模範例）は、プロンプトの書き方そのものを問う問題（ドメイン1・一部ドメイン7）にだけ付ける。ガバナンスや概念問題には無理に付けない。

## viz（図解SVG）の書き方

`question-authoring-stats` の「viz（図解SVG）の書き方」節に完全準拠（viewBox・配色・PNG目視検証手順すべて同じ）。CCAO-F固有の定番の型:

- **モデル比較（横棒3本）**: Haiku/Sonnet/Opusを「速さ」「コスト」「対応できる複雑さ」の軸で比較する棒グラフ
- **箱と矢印（ワークフロー）**: 入力 → Claude（プロンプト/Project）→ 出力 → 人間レビュー、のようなパイプライン図
- **循環矢印（反復改善）**: 下書き → 評価 → 指示を直す → 下書き、のループ
- **2列比較（良い例 vs 惜しい例）**: 曖昧なプロンプト vs 具体的なプロンプト、生の出力 vs 人間が検証した出力
- **信号（ガバナンスの可否判断）**: 緑（そのまま使ってよい）・黄（要確認・要匿名化）・赤（使ってはいけない）の3段階
- **入れ子の箱（Projectsの構造）**: Project の中に「カスタム指示」「知識ソース（複数ファイル）」「会話（複数）」が入っている構造図
- **虫眼鏡/チェックリスト（出力評価）**: 出力を検証する着眼点（事実確認・引用元・数値の再計算）を並べる

## 内容の注意

- **API/開発者向けの細部（コード、SDK、レート制限の数値等）は問わない。** この試験は非エンジニアの業務ユーザー向け。問うのは「Claude.ai / Claude for Work をどう業務に使うか」の判断力
- モデル名・機能名は2026年時点のAnthropic公式情報に沿わせる（Haiku/Sonnet/Opusという3階層、Projects、Artifacts）。特定のバージョン番号を正解の決め手にしない（試験のように長寿命な範囲設定を優先し、バージョンが古くなって陳腐化する問い方を避ける）
- ハルシネーション・バイアスの見抜き方（ドメイン2）は出題比重が一番高い（21%）。**「もっともらしく書かれているが事実と違う」ことに気づく着眼点**（数値の再計算、引用元の実在確認、知っている事実との突き合わせ）を厚めに扱う
- ガバナンス（ドメイン6）では「機密情報・個人情報を外部ツールに貼ってよいか」の判断が中心。**具体的な業種の実データを想起させない**（一般化した業務シナリオに留める）
- 「決め手」が実際の試験と矛盾しないよう、断定的すぎる細部（正確な合格点720点など）を問題文・解説の主張には使わない（試験のバージョンアップで変わりうる運用値のため）。試験の全体像（60問・120分・7ドメイン）はこの問題集の設計根拠として使ってよいが、個々の問題の正解根拠には使わない
