---
name: actrun
description: actrun (ローカル GitHub Actions ランナー) の使い方リファレンスとワークフロー実行支援。actrun コマンドの提案、ワークフロー解析、実行プラン確認を行う。
---

# actrun Skill

actrun は MoonBit で構築されたローカル GitHub Actions ランナー。GitHub Actions ワークフローをローカルで実行・デバッグする。

## このスキルの使い方

ユーザーが以下のいずれかを求めた場合にこのスキルを適用する:
- GitHub Actions ワークフローをローカルで実行したい
- actrun のコマンドや使い方を知りたい
- ワークフローファイルを解析して実行プランを確認したい

## 行動指針

1. まず `.github/workflows/` 内のワークフローファイルを確認する
2. `actrun.toml` が存在するか確認し、設定を把握する
3. ユーザーの目的に合った actrun コマンドを提案する
4. 実行前に `--dry-run` で確認を促す

## CLI リファレンス

### ワークフロー実行

```bash
# 基本実行（以下は同等）
actrun .github/workflows/ci.yml
actrun workflow run .github/workflows/ci.yml

# 実行プラン確認（実行しない）
actrun .github/workflows/ci.yml --dry-run

# ローカルで不要なアクションをスキップ
actrun ci.yml --skip-action actions/checkout --skip-action actions/setup-node

# ジョブ/ステップ指定
actrun ci.yml --job build
actrun ci.yml --job build --step test
actrun ci.yml --job build --step "Run tests"

# トリガー指定
actrun ci.yml --trigger schedule
actrun ci.yml --trigger workflow_dispatch --input env=staging

# 差分実行（変更ファイルがパターンに一致する場合のみ）
actrun ci.yml --affected

# 失敗ジョブのみリトライ
actrun ci.yml --retry
```

### ワークスペースモード

```bash
actrun ci.yml --local      # カレントディレクトリで実行（デフォルト）
actrun ci.yml --worktree   # git worktree で隔離実行
actrun ci.yml --tmp        # 一時ディレクトリにクローン
actrun ci.yml --workspace-mode docker  # Docker コンテナ内
```

### 実行結果の確認

```bash
actrun run list                      # 過去の実行一覧
actrun run view run-1                # 実行サマリ
actrun run view run-1 --json         # JSON 出力
actrun run logs run-1                # 全ログ
actrun run logs run-1 --task build/step_1  # 特定タスク
actrun run download run-1            # アーティファクトDL
```

### 一覧・ユーティリティ

```bash
actrun list                          # ワークフロー一覧 + コマンド例
actrun workflow list                 # ワークフロー一覧（簡易）
actrun doctor                        # 依存ツールチェック
actrun init                          # actrun.toml 生成
actrun cron show                     # schedule トリガーの cron 表示
actrun cron install                  # crontab へ登録
```

### Secrets & Variables

```bash
ACTRUN_SECRET_MY_TOKEN=xxx actrun ci.yml    # シークレット
ACTRUN_VAR_MY_VAR=value actrun ci.yml       # 変数
actrun ci.yml --env .env.local              # .env ファイル読み込み
```

### Nix 連携

```bash
actrun ci.yml                        # flake.nix/shell.nix 自動検出
actrun ci.yml --no-nix               # Nix 無効化
actrun ci.yml --nix-packages "python312 jq"  # アドホックパッケージ
```

### コンテナランタイム

```bash
actrun ci.yml --container-runtime podman     # Podman
actrun ci.yml --container-runtime container  # Apple container
actrun ci.yml --container-runtime lima       # Lima VM
```

## actrun.toml 設定

```toml
workspace_mode = "local"
local_skip_actions = ["actions/checkout", "actions/setup-node"]
trust_actions = true
# nix_mode = ""
# nix_packages = ["python312"]
# container_runtime = "docker"
includes = [".github/workflows/*.yml"]

[affected."ci.yml"]
patterns = ["src/**", "package.json"]
```

## ビルトインアクション対応

| アクション | 主要入力 |
|-----------|---------|
| `actions/checkout@*` | `path`, `ref`, `fetch-depth`, `clean`, `sparse-checkout`, `submodules` |
| `actions/upload-artifact@*` | `name`, `path`, `if-no-files-found`, `overwrite` |
| `actions/download-artifact@*` | `name`, `path`, `pattern`, `merge-multiple` |
| `actions/cache@*` | `key`, `path`, `restore-keys`, `lookup-only` |
| `actions/setup-node@*` | `node-version`, `node-version-file`, `cache`, `registry-url` |

リモートアクション（composite, node, docker）、`docker://image`、`wasm://` も対応。

## ローカルスキップパターン

`ACTRUN_LOCAL=true` が実行環境に自動設定される。ワークフロー内で条件分岐に使える:

```yaml
- uses: actions/checkout@v5
  if: ${{ !env.ACTRUN_LOCAL }}    # ローカルではスキップ

- run: echo "debug"
  if: ${{ env.ACTRUN_LOCAL }}     # ローカルのみ実行
```

## 環境変数

| 変数 | 説明 |
|-----|------|
| `ACTRUN_SECRET_<NAME>` | `${{ secrets.<name> }}` |
| `ACTRUN_VAR_<NAME>` | `${{ vars.<name> }}` |
| `ACTRUN_NODE_BIN` | Node.js バイナリパス |
| `ACTRUN_DOCKER_BIN` | Docker バイナリパス |
| `ACTRUN_NIX` | `false` で Nix 無効化 |

## 参考

- https://github.com/mizchi/actrun
