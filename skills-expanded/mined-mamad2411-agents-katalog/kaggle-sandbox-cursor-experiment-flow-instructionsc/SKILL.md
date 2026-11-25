---
description: "Kaggle Experiment Flow Instructions for AI Agents"
globs: ["**/*.py", "**/*.ipynb", "**/*.md", "**/*.csv", "**/*.json"]
alwaysApply: true
priority: high
team: "kaggle"
version: "1.0"
project: "house_prices"
type: "experiment_flow"
---

# 🤖 Experiment Flow Instructions for AI Agents

## 基本原則

### 役割の明確な分離
- 各エージェントは自分の専門領域に集中
- 他のエージェントの領域に侵入しない
- 役割に関する疑問が生じた場合、`kaggle_team.mdc`を参照

### 品質保証
- 各ステップで品質チェックポイントを必ず実行
- エラー発生時は適切なエスカレーション手順に従う
- 次のエージェントが受け取りやすい形式で出力する

### 情報の流れ
```
User → Document Manager → Planner → User → Developer → Validator → User → Validator → Document Manager → Version Controller
```

**注意**: Validatorは、Developerから引き継ぎを受けた後、ユーザーに結果（Public LBスコア等）の入力を依頼し、受け取ってからレポート作成を開始する。

---

## 🔄 Experiment実行フロー

### Step 1: アイディア受領・情報収集
**担当**: Document Manager

**入力**:
- ユーザーのアイディア・フィードバック
- 関連ドキュメント・リソース

**処理**:
1. アイディアの整理・要約
2. 関連情報の収集・整理
3. 前回のexperiment結果の確認（該当する場合）

**出力**:
- 整理されたアイディア
- 関連情報の要約
- コンテキスト情報

**品質チェック**:
- [ ] アイディアの意図が明確
- [ ] 関連情報が適切に収集されている
- [ ] 前回の結果との関連性が明確

### Step 2: 計画立案
**担当**: Planner

**入力**:
- Document Managerからの整理されたアイディア
- 関連情報の要約
- **タスク情報**: `tasks/current_sprint.json` から読み込んだタスク情報

**タスク読み取り手順**:
1. `scripts/workflow/task_loader.py` を使用してタスクを読み込む
   - **推奨**: `load_active_tasks()` を使用して進行中のタスク（`status: "in_progress"`）を読み込む
   - 注意: `load_pending_tasks()` は `status: "pending"` のタスクを読み込むが、実際のシステムでは通常存在しない
2. タスクの優先順位、依存関係、期待される成果を確認
3. タスクを具体的な実装ステップに分解
4. 各ステップを適切なエージェントに割り当て

**処理**:
1. 実装の目的と仮説を明確化
2. 具体的な実装手順を立案
3. 期待される成果を定量化
4. リスク要因と対策を特定

**出力**:
```
[Plan:]
- 実装の目的と仮説
- 具体的な実装手順
- 期待される成果
- リスク要因と対策

[Action:]
- 次のエージェントへの指示
- 必要なリソースの要求
```

**品質チェック**:
- [ ] 実装可能性の確認
- [ ] リソース要件の明確化
- [ ] 期待成果の定量化
- [ ] リスク要因の特定

### Step 3: 計画承認
**担当**: ユーザー

**処理**:
- Plannerの計画をレビュー
- 承認または差し戻しの判断

**承認条件**:
- 実装可能性が確認できる
- 期待成果が明確
- リスクが適切に評価されている

### Step 4: 実装・実行
**担当**: Developer

**入力**:
- 承認された計画

**処理**:
1. `experiments/exp[timestamp]_[description]/`ディレクトリの作成
2. コードの実装・実行（train.py, predict.py）
3. 結果ファイルの生成
4. **提出ファイル（submission.csv）の作成まで完了**

**実験IDの命名規則**:
- 形式: `exp[YYYYMMDDHHMMSS]_[description]`（タイムスタンプ形式）
- 例: `exp20260106030720_baseline_tfidf_lr`
- 例: `exp20260112174906_keyword_tfidf_lr`
- **重要**: 実験IDは実験開始時の現在時刻を使用して生成します。全ファイルに同じ実験IDを付与します。

**ディレクトリ構造**:
```
experiments/exp[YYYYMMDDHHMMSS]_[description]/
├── exp[timestamp]_config.yaml  # 設定ファイル（SSOT）
├── exp[timestamp]_train.py     # 訓練スクリプト
└── exp[timestamp]_predict.py   # 推論スクリプト

results/exp[YYYYMMDDHHMMSS]_[description]/
├── exp[timestamp]_metrics.json      # 評価指標（CV Mean, CV Std, Train, Public LB）
├── exp[timestamp]_cv_results.json   # CV結果（各フォールドの詳細）
├── exp[timestamp]_model.pkl         # モデルファイル（Git管理対象外）
├── exp[timestamp]_submission.csv    # 提出ファイル
└── exp[timestamp]_report.md         # 実験レポート（Validatorが作成）
```

**重要**: コードと結果は分離されています。実験コードは `experiments/` に、実験結果（レポート含む）は `results/` に保存されます。

**出力**:
- Pythonコードブロック
- `[Result:]` 実行結果要約（提出ファイル作成完了まで）

**品質チェック**:
- [ ] コードが正常に実行される
- [ ] 結果ファイルが適切に生成される
- [ ] 提出ファイル（submission.csv）が生成される
- [ ] エラーが発生していない

**引き継ぎ**:
- Developer → Validator: 提出ファイル作成完了後、Validatorに引き継ぎ、実験結果の入力を依頼する

### Step 5: 結果入力依頼・レポート作成
**担当**: Validator

**入力**:
- Developerが作成した実験コードと結果ファイル
- **ユーザーから提供される提出後の結果**（Public LBスコア等）

**処理**:
1. Developerからの引き継ぎを受ける
2. **ユーザーに結果入力を依頼する**: Kaggle提出後の結果（Public LBスコア等）をユーザーに入力依頼する
   - 例: "Kaggleに提出された結果（Public LBスコア等）を教えてください"
3. **ユーザーから結果を受け取る**
4. **関連タスク・プロジェクトの検索と提案**:
   - `experiments/exp[YYYYMMDDHHMMSS]_[description]/exp[timestamp]_config.yaml` からプロジェクト名を取得
   - `knowledge/tasks/projects/project_[project_name].md` を検索して関連プロジェクトを特定
   - `knowledge/tasks/active/`, `knowledge/tasks/completed/` から関連タスクを検索
     - 検索条件: タスクの `project` フィールドが実験のプロジェクト名と一致
     - 検索条件: タスクの `id` に実験IDやタイムスタンプが含まれる場合
     - 検索条件: タスクの `tags` に実験に関連するタグが含まれる場合
   - `knowledge/zettelkasten/` から関連知識ノートを検索
   - 見つかった関連タスク・プロジェクト・ノートがあれば、ユーザーに提案して確認する
     - 例: "以下の関連タスク・プロジェクトが見つかりました：task-20260105120020, project_kaggle_disaster_tweets。これらをレポートに記載しますか？"
5. モデル性能の客観的評価（CV結果、Public LBスコア等を含む）
6. 結果の解釈と分析
7. 実験レポートの作成（関連タスク・プロジェクト・ノートを含む）

**評価項目**:
- CV結果（各フォールドのスコア、平均、標準偏差）
- Public LBスコア（ユーザー入力）
- 特徴量情報
- モデルの特徴

**出力**:
- 実験レポート（`results/exp[YYYYMMDDHHMMSS]_[description]/exp[timestamp]_report.md`）
  - **保存場所**: `results/` ディレクトリに保存されます
  - YAMLフロントマター（metricsにPublic LBスコアを含む）
  - 実験概要、実装内容、結果、学んだこと、次のステップ
  - 関連タスク・プロジェクト・ノートへのリンク

**品質チェック**:
- [ ] ユーザーから結果（Public LBスコア等）を受け取った
- [ ] 関連タスク・プロジェクト・ノートを検索し、提案した
- [ ] ユーザーに確認を取り、関連情報をレポートに記載した
- [ ] YAMLフロントマターの`related_task`と`links`に適切な情報を記載した
- [ ] 評価指標が適切に記載されている
- [ ] 結果の解釈が客観的
- [ ] 改善点が明確に示されている
- [ ] YAMLフロントマターがknowledgeフォルダの様式に合っている

**引き継ぎ**:
- Validator → Docs Manager: 実験レポート作成完了後、Docs Managerに引き継ぎ、知識化を依頼する

### Step 6: ドキュメント化
**担当**: Document Manager

**入力**:
- 実験結果
- 評価結果

**処理**:
1. 実験概要の文書化
2. 結果の要約
3. 学んだことの記録

**出力**:
- Markdownレポート
- 実験概要
- 結果サマリー

**品質チェック**:
- [ ] 実験の目的が明確に記録されている
- [ ] 結果が適切に要約されている
- [ ] 学んだことが記録されている

### Step 7: バージョン管理
**担当**: Version Controller

**入力**:
- 全ファイル（コード、結果、ドキュメント）

**処理**:
1. 変更の記録
2. 適切なコミットメッセージの生成
3. Gitコミットの実行

**コミットメッセージ規約** (Conventional Commits準拠):

詳細な規約は `.cursor/version_controller_rules.mdc`（運用規約 / SSOT）を参照してください。

**基本形式**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**実験の場合**:
```
exp(feature): keyword特徴量追加 exp20260112174906

- keywordカラムをターゲットエンコーディングで特徴量化
- CV F1 Score: 0.7501 ± 0.0123
- Public LB: 0.80123
- ベースラインから0.00044改善

Closes: task-20260112170000
```

**実験スコープの例**:
- `exp(baseline): ...`: ベースライン実験
- `exp(feature): ...`: 特徴量エンジニアリング（keyword追加、特徴量追加など）
- `exp(hyperparameter): ...`: ハイパーパラメータチューニング（C値、max_depthなど）
- `exp(data): ...`: データ変更（データソース変更、データ分割方法変更など）
- `exp(model): ...`: モデル変更（LR → XGBoostなど）
- `exp(preprocessing): ...`: 前処理変更（テキストクリーニング、欠損値処理など）
- `exp(ensemble): ...`: アンサンブル

**インフラ整備の場合**:
```
infra(workflow): 監視スクリプトの追加

- task_watcher.pyを実装
- 自動タスク変換機能を追加
```

**インフラスコープの例**:
- `infra(mlops): ...`: MLOpsパイプライン
- `infra(workflow): ...`: ワークフロー
- `infra(script): ...`: スクリプト
- `infra(template): ...`: テンプレート

**注意**: スコープは英語、説明（subject）は日本語で記述します。

**出力**:
- Gitコマンド
- コミットメッセージ

**品質チェック**:
- [ ] コミットメッセージが適切
- [ ] 必要なファイルがすべて含まれている
- [ ] 実験の内容が明確に記録されている

---

## 🚨 エラーハンドリング

### 各ステップでの失敗時の対応

#### Document Manager
- 情報収集に失敗した場合
  - ユーザーに追加情報を要求
  - 利用可能な情報で可能な限り進める

#### Planner
- 計画立案に失敗した場合
  - より詳細な情報をDocument Managerに要求
  - 段階的な計画に分割

#### Developer
- コード実行に失敗した場合
  - エラーメッセージを詳細に記録
  - 代替手法をPlannerに提案

#### Validator
- 評価に失敗した場合
  - 基本的な評価指標から開始
  - 段階的に詳細な評価を追加

#### Document Manager
- 文書化に失敗した場合
  - 最低限の情報から開始
  - 段階的に詳細を追加

#### Version Controller
- コミットに失敗した場合
  - エラーの原因を特定
  - 適切な修正を実行

### エスカレーション手順

1. **レベル1**: 同じエージェント内で再試行
2. **レベル2**: 前のステップのエージェントに相談
3. **レベル3**: ユーザーに報告・相談

---

## 📊 品質チェックポイント

### 各ステップ完了時の確認事項

#### 全エージェント共通
- [ ] 入力が適切に処理されている
- [ ] 出力が次のエージェントに適している
- [ ] エラーが発生していない
- [ ] ログが適切に記録されている

#### ステップ別確認事項

**Step 1 (Document Manager)**
- [ ] アイディアの意図が明確
- [ ] 関連情報が適切に収集されている
- [ ] 前回の結果との関連性が明確

**Step 2 (Planner)**
- [ ] 実装可能性が確認できる
- [ ] 期待成果が定量化されている
- [ ] リスクが適切に評価されている

**Step 4 (Developer)**
- [ ] コードが正常に実行される
- [ ] 結果ファイルが適切に生成される
- [ ] エラーが発生していない

**Step 5 (Validator)**
- [ ] 評価指標が適切に計算されている
- [ ] 結果の解釈が客観的
- [ ] 改善点が明確に示されている

**Step 6 (Document Manager)**
- [ ] 実験の目的が明確に記録されている
- [ ] 結果が適切に要約されている
- [ ] 学んだことが記録されている

**Step 7 (Version Controller)**
- [ ] コミットメッセージが適切
- [ ] 必要なファイルがすべて含まれている
- [ ] 実験の内容が明確に記録されている

---

## 🔄 次のステップへの引き継ぎ

### 各エージェントから次のエージェントへの引き継ぎ方法

#### Document Manager → Planner
- 整理されたアイディア
- 関連情報の要約
- 前回の結果（該当する場合）

#### Planner → Developer
- 承認された計画
- 実装手順の詳細
- 期待される成果

#### Developer → Validator
- 実装されたコード
- 生成された結果ファイル
- 実行ログ

#### Validator → Document Manager
- 評価結果
- 改善点の提案
- 次のexperimentへの示唆

#### Document Manager → Version Controller
- 文書化された結果
- 実験概要
- 関連ファイル

---

## 📚 参考情報

### 関連ドキュメント
- **基本ルール（チーム憲法）**: `.cursor/kaggle_team.mdc`
- **Developer 実験運用ルール（運用規約 / SSOT）**: `.cursor/developer_experiment_rules.mdc`
- **Docs Manager ルール（運用規約 / SSOT）**: `.cursor/docs_manager_rules.mdc`
- **Version Controller ルール（運用規約 / SSOT）**: `.cursor/version_controller_rules.mdc`
- **Docs Manager ルール（人間向け入口）**: `docs/docs_manager_rules.md`

### 実験管理

**実験IDの命名規則**:
- 形式: `exp[YYYYMMDDHHMMSS]_[description]`（タイムスタンプ形式）
- 例: `exp20260106030720_baseline_tfidf_lr`
- 例: `exp20260112174906_keyword_tfidf_lr`
- **重要**: 実験IDは実験開始時の現在時刻を使用して生成します。全ファイルに同じ実験IDを付与します。

**ディレクトリ構造**:
- **実験コード**: `experiments/exp[YYYYMMDDHHMMSS]_[description]/`
  - `exp[timestamp]_config.yaml` - 設定ファイル（SSOT）
  - `exp[timestamp]_train.py` - 訓練スクリプト
  - `exp[timestamp]_predict.py` - 推論スクリプト
- **実験結果**: `results/exp[YYYYMMDDHHMMSS]_[description]/`
  - `exp[timestamp]_metrics.json` - 評価指標（CV Mean, CV Std, Train, Public LB）
  - `exp[timestamp]_cv_results.json` - CV結果（各フォールドの詳細）
  - `exp[timestamp]_model.pkl` - モデルファイル（Git管理対象外）
  - `exp[timestamp]_submission.csv` - 提出ファイル
  - `exp[timestamp]_report.md` - 実験レポート（Validatorが作成）

**結果記録**:
- JSON形式でメトリクスを管理（`exp[timestamp]_metrics.json`）
- CV結果は詳細に記録（`exp[timestamp]_cv_results.json`）
- 実験レポートはMarkdown形式（`exp[timestamp]_report.md`）

### 品質保証
- **チェックリスト**: 各ステップで必ず確認
- **エラーハンドリング**: 段階的な対応
- **エスカレーション**: 適切なレベルでの報告

---

**すべてのエージェントは、experimentを実行する際はこの指示書に従うこと。**