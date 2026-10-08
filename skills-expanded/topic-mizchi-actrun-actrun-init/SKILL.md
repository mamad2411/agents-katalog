---
name: actrun-init
description: プロジェクトに actrun を導入する。インストール、actrun.toml 設定、ワークフロー調整をガイドする。
---

# actrun-init Skill

プロジェクトに actrun を導入し、GitHub Actions ワークフローをローカルで実行できるようにする。

## このスキルの使い方

ユーザーが以下のいずれかを求めた場合にこのスキルを適用する:
- actrun をプロジェクトに導入したい
- actrun.toml を設定したい
- 既存のワークフローを actrun 対応にしたい

## 導入手順

### Step 1: インストール

```bash
# curl (Linux / macOS)
curl -fsSL https://raw.githubusercontent.com/mizchi/actrun/main/install.sh | sh

# Docker（インストール不要）
docker run --rm -v "$PWD":/workspace -w /workspace ghcr.io/mizchi/actrun workflow run .github/workflows/ci.yml

# moon install
moon install mizchi/actrun/cmd/actrun

# ソースからビルド
git clone https://github.com/mizchi/actrun.git && cd actrun
moon build src/cmd/actrun --target native
```

### Step 2: 環境チェック

```bash
actrun doctor
```

以下を確認:
- `git`: 必須
- `bash`: 必須
- `node`: Node.js アクション実行に必要
- `docker`: Docker アクション/コンテナジョブに必要
- `nix`: Nix 連携を使う場合

### Step 3: 設定ファイル生成

```bash
actrun init
```

`actrun.toml` が生成される。ローカルにインストール済みのツールを自動検出し、対応する setup アクションのスキップ設定を提案する。

### Step 4: ワークフローの動作確認

```bash
# まず dry-run で実行プランを確認
actrun .github/workflows/ci.yml --dry-run

# 問題なければ実行
actrun .github/workflows/ci.yml
```

## actrun.toml 設定ガイド

### 基本設定

```toml
# ワークスペースモード
workspace_mode = "local"         # local, worktree, tmp, docker

# ローカルで不要なアクションをスキップ
local_skip_actions = [
  "actions/checkout",            # ローカルではチェックアウト不要
  "actions/setup-node",          # ローカルの node を使う
]

# サードパーティアクションを自動信頼
trust_actions = true
```

### プロジェクトタイプ別の推奨設定

#### Node.js プロジェクト

```toml
local_skip_actions = [
  "actions/checkout",
  "actions/setup-node",
]
```

#### Python プロジェクト

```toml
local_skip_actions = [
  "actions/checkout",
  "actions/setup-python",
]
```

#### Go プロジェクト

```toml
local_skip_actions = [
  "actions/checkout",
  "actions/setup-go",
]
```

#### Rust プロジェクト

```toml
local_skip_actions = [
  "actions/checkout",
  "actions-rust-lang/setup-rust-toolchain",
]
```

#### 複数言語 / Nix 環境

```toml
local_skip_actions = [
  "actions/checkout",
  "actions/setup-node",
  "actions/setup-python",
]
# Nix で全ツールチェーンを提供
# nix_mode = ""  # 自動検出（flake.nix / shell.nix）
# nix_packages = ["python312", "nodejs"]
```

### 差分実行設定

モノレポや大規模プロジェクトで有用:

```toml
[affected."ci.yml"]
patterns = ["src/**", "package.json", "pnpm-lock.yaml"]

[affected."lint.yml"]
patterns = ["src/**", "*.config.*"]

[affected."docs.yml"]
patterns = ["docs/**", "*.md"]
```

```bash
actrun ci.yml --affected    # 変更があるときだけ実行
```

### ワークフローパターン設定

```toml
# actrun list で表示するワークフローの glob
includes = [".github/workflows/*.yml", "ci/**/*.yaml"]
```

## ワークフローの actrun 対応

### ACTRUN_LOCAL 条件分岐

ローカルとGitHub Actions で挙動を分けたい場合:

```yaml
steps:
  # GitHub Actions でのみ実行（ローカルではスキップ）
  - uses: actions/checkout@v5
    if: ${{ !env.ACTRUN_LOCAL }}

  # ローカルでのみ実行
  - run: echo "local debug"
    if: ${{ env.ACTRUN_LOCAL }}
```

### シークレットの扱い

```bash
# 環境変数で渡す
ACTRUN_SECRET_GITHUB_TOKEN=$(gh auth token) actrun ci.yml

# .env ファイルを使う
echo "ACTRUN_SECRET_NPM_TOKEN=xxx" >> .env.local
actrun ci.yml --env .env.local
```

`.env.local` は `.gitignore` に追加すること。

### cron スケジュールの設定

ワークフローに `schedule` トリガーがある場合:

```bash
actrun cron show       # スケジュール確認
actrun cron install    # crontab に登録
actrun cron uninstall  # crontab から削除
```

## 典型的な導入フロー

```bash
# 1. インストール
curl -fsSL https://raw.githubusercontent.com/mizchi/actrun/main/install.sh | sh

# 2. 環境チェック
actrun doctor

# 3. 設定生成
actrun init

# 4. dry-run で確認
actrun .github/workflows/ci.yml --dry-run

# 5. 実行
actrun .github/workflows/ci.yml

# 6. 結果確認
actrun run view run-1
actrun run logs run-1

# 7. (オプション) cron 登録
actrun cron install
```

## .gitignore への追加

```gitignore
# actrun
actrun.toml        # プロジェクトに合わせて共有するか個人用か選択
.env.local         # シークレット
_build/actrun/     # run store（デフォルトパス）
```

## 参考

- https://github.com/mizchi/actrun
