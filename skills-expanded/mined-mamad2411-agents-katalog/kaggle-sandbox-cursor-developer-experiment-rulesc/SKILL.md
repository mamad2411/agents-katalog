---
description: "Developer Experiment Rules (Operational Constitution) for Kaggle Multi-Agent System"
globs: ["experiments/**/*.py", "experiments/**/*.yaml", "experiments/**/*.md", "results/**/*"]
alwaysApply: true
priority: highest
team: "kaggle"
version: "1.0"
type: "rules"
---

# 💻 Developer 実験運用ルール（運用規約 / SSOT）

このドキュメントは、本リポジトリにおける **Developer（実験実装エージェント）** の運用ルールを定めます。  
目的は、実験コード・結果・ログを **再現可能・追跡可能・一貫性のある形**で管理することです。

> **位置づけ**: これはマルチエージェントシステム（`.cursor/`）の設定文書の一つです。  
> 人間向けの入口（参照用）: `docs/developer_experiment_rules.md`（将来作成）

---

## 基本原則（最重要）

- **実験IDはタイムスタンプ形式（衝突回避）**
  - 二人で作業するため、番号（exp001）ではなく **タイムスタンプ形式** を使用
  - 形式: `expYYYYMMDDHHMMSS`（例: `exp20260105180000`）
- **全ファイルに実験IDを付与**
  - 実験ディレクトリ内の**全てのファイル**に同じタイムスタンプ（実験ID）を付与
  - ファイル名からどの実験に属するかが分かるようにする
- **コードと結果を分離**
  - `experiments/exp[timestamp]_[description]/` → 実験コード
  - `results/exp[timestamp]_[description]/` → 実験結果
- **config.yamlをSSOTとして使用**
  - 実験設定は `config.yaml` に集約し、コードはこれを読み込んで実行
  - 再現性のため、`config.yaml` は必ずGitにコミットする
- **リポジトリルート基準の相対パス**
  - データパスはリポジトリルート基準の相対パスを使用（ポータビリティのため）

---

## 実験作成時の必須手順

### 1. 実験IDの生成

- **タイムスタンプ形式**: `expYYYYMMDDHHMMSS`（例: `exp20260105180000`）
- **生成方法**: 実験開始時の現在時刻を使用
  ```python
  from datetime import datetime
  exp_id = f"exp{datetime.now().strftime('%Y%m%d%H%M%S')}"
  ```

### 2. ディレクトリ構造の作成

```
experiments/
└── exp20260105180000_baseline_tfidf_lr/
    ├── exp20260105180000_report.md
    ├── exp20260105180000_config.yaml
    ├── exp20260105180000_train.py
    └── exp20260105180000_predict.py

results/
└── exp20260105180000_baseline_tfidf_lr/
    ├── exp20260105180000_metrics.json
    ├── exp20260105180000_cv_results.json
    ├── exp20260105180000_submission.csv
    └── exp20260105180000_model.pkl
```

### 3. テンプレートからのコピー

- `experiments/_template_experiment/config.yaml` をコピー
- `experiments/_template_experiment/README.md` をコピーし、ファイル名を `exp[timestamp]_report.md` に変更
- **重要**: コピー後、**全てのファイル名に実験IDを付与**する

### 4. config.yamlの編集

- `experiment.id`: 実験ID（タイムスタンプ）を設定
- `experiment.name`: 短い説明（例: `baseline_tfidf_lr`）
- `experiment.created_at`: ISO形式の日時
- `data.train_path` / `data.test_path`: リポジトリルート基準の相対パス
- その他の設定（前処理、特徴量、モデル、CV）を編集

---

## コード実装のルール

### 1. config.yamlの読み込み

- **必須**: 実験コードは必ず `config.yaml` を読み込む
- **パス解決**: config.yamlがあるディレクトリを基準に、リポジトリルートを取得
  ```python
  from pathlib import Path
  import yaml

  # config.yamlがあるディレクトリ
  EXP_DIR = Path(__file__).parent
  # リポジトリルート（3階層上）
  REPO_ROOT = EXP_DIR.parent.parent.parent

  # config.yamlを読み込む
  with open(EXP_DIR / f"{exp_id}_config.yaml") as f:
      config = yaml.safe_load(f)

  # データパスを解決（リポジトリルート基準）
  train_path = REPO_ROOT / config["data"]["train_path"]
  ```

### 2. 実験IDの使用

- **ファイル名**: 全てのファイル名に実験IDを含める
  - `exp20260105180000_train.py`
  - `exp20260105180000_config.yaml`
  - `exp20260105180000_README.md`
- **結果ファイル**: resultsディレクトリ内のファイルにも実験IDを付与
  - `exp20260105180000_metrics.json`
  - `exp20260105180000_submission.csv`
  - `exp20260105180000_model.pkl`

### 3. 乱数シードの固定

- **必須**: 全実験で `random_state=42` を統一（再現性のため）
- **適用範囲**:
  - モデルの `random_state`
  - CVの `random_state`
  - データ分割の `random_state`
  - NumPy/Pythonの乱数シード（`np.random.seed(42)`, `random.seed(42)`）

### 4. 結果の保存

- **保存先**: `results/exp[timestamp]_[description]/`
- **保存形式**:
  - `metrics.json`: 評価指標（CV Mean, CV Std, Train, Public LB）
  - `cv_results.json`: 各フォールドの詳細結果
  - `submission.csv`: 提出ファイル
  - `model.pkl`: 学習済みモデル（`save_model: true` の場合）
- **ファイル名**: 全ての結果ファイルに実験IDを付与

---

## 前処理済みデータの扱い

### 1. 保存場所

- **ディレクトリ**: `data/processed/` の下を**前処理パイプラインごと**に整理
- **命名規則**: 前処理内容を反映（例: `text_only_basic/`, `text_only_no_url/`, `text_keyword/`）

### 2. config.yamlでの指定

```yaml
data:
  train_path: "data/processed/text_only_basic/train.csv"
  test_path: "data/processed/text_only_basic/test.csv"
```

### 3. 共有の原則

- 複数の実験で同じ前処理データを使う場合は、同じディレクトリを参照
- 前処理が異なる場合は、新しいディレクトリを作成

---

## 実行ログの保存

### 1. 保存形式

- **metrics.json**: 評価指標を構造化して保存
  ```json
  {
    "experiment_id": "exp20260105180000",
    "train_f1": 0.85,
    "cv_mean": 0.82,
    "cv_std": 0.01,
    "public_lb": null
  }
  ```
- **cv_results.json**: 各フォールドの詳細結果
  ```json
  {
    "fold_0": 0.81,
    "fold_1": 0.83,
    "fold_2": 0.82,
    "fold_3": 0.81,
    "fold_4": 0.83
  }
  ```
- **.logファイル**: 実行ログ（オプション、`.gitignore` で除外）

### 2. 保存先

- `results/exp[timestamp]_[description]/` に保存
- ファイル名に実験IDを付与

---

## Git管理方針

### 1. コミット対象

- ✅ **コミットする**: 実験コード（`.py`）、`config.yaml`、`exp[timestamp]_report.md`
- ✅ **コミットする**: 結果ファイル（`metrics.json`, `submission.csv`）※軽量なもの
- ❌ **コミットしない**: モデルファイル（`.pkl`）※`.gitignore` で除外
- ❌ **コミットしない**: ログファイル（`.log`）※`.gitignore` で除外

### 2. コミットメッセージ (Conventional Commits準拠)

- **実験の場合**: `exp(<scope>): <説明> <実験ID>`
  - スコープは実験の種類や変更内容を表す（例: `baseline`, `feature`, `hyperparameter`, `data`, `model`, `preprocessing`, `ensemble`）
  - 例: `exp(baseline): ベースラインTF-IDF+LRモデル exp20260106030720`
  - 例: `exp(feature): keyword特徴量追加 exp20260112174906`
  - 例: `exp(hyperparameter): C値グリッドサーチ exp20260112201310`
- **インフラ整備の場合**: `infra(<scope>): <説明>`
  - 例: `infra(script): task_converterの改善`
- **注意**: スコープは英語、説明（subject）は日本語で記述します。

---

## 実験レポートの記入

### 1. 必須項目

- 実験ID、実施日、目的
- 仮説、実装内容（前処理/特徴量/モデル/CV）
- ハイパーパラメータ
- 結果（評価指標、特徴量重要度）
- 学んだこと、次のステップ

### 2. テンプレート

- `experiments/_template_experiment/README.md` をテンプレートとして使用
- コピー後、ファイル名を `exp[timestamp]_report.md` に変更
- 実験IDをタイムスタンプ形式に更新

---

## エラーハンドリング

### 1. 実験失敗時

- エラーログを `results/exp[timestamp]_[description]/exp[timestamp]_error.log` に保存
- 実験レポート（`exp[timestamp]_report.md`）に失敗理由を記録

### 2. 再実行時

- 同じ実験IDを使用（上書きではなく、結果を追記）

---

## 関連ドキュメント

- `experiments/_template_experiment/config.yaml`（実験設定テンプレート）
- `experiments/_template_experiment/README.md`（実験レポートテンプレート、コピー後 `exp[timestamp]_report.md` にリネーム）
- `docs/project_architecture.md`（大枠の設計）
- `knowledge/tasks/projects/project_kaggle_disaster_tweets.md`（プロジェクトノート）

---

## チェックリスト（実験作成時）

- [ ] 実験IDをタイムスタンプ形式で生成
- [ ] `experiments/exp[timestamp]_[description]/` ディレクトリを作成
- [ ] `results/exp[timestamp]_[description]/` ディレクトリを作成
- [ ] テンプレートからファイルをコピーし、**全てのファイル名に実験IDを付与**
- [ ] `config.yaml` を編集（実験ID、データパス、設定）
- [ ] `train.py` で `config.yaml` を読み込み、リポジトリルート基準でパス解決
- [ ] 乱数シードを `random_state=42` に統一
- [ ] 結果ファイルに実験IDを付与して保存
- [ ] `exp[timestamp]_report.md` に実験内容を記録
- [ ] Gitにコミット（コード、config.yaml、実験レポート）
