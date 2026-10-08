---
name: actrun-debug
description: actrun の実行失敗を診断する。ログ解析、エラー原因特定、修正提案を行う。
---

# actrun-debug Skill

actrun のワークフロー実行が失敗した場合に、原因を特定し修正方法を提案する。

## このスキルの使い方

ユーザーが以下のいずれかを求めた場合にこのスキルを適用する:
- actrun の実行が失敗して原因を知りたい
- ワークフローのエラーをデバッグしたい
- actrun の出力を解析してほしい

## 診断手順

### Step 1: 実行結果の取得

```bash
# 最新の実行一覧を確認
actrun run list

# 失敗した run の詳細を取得
actrun run view <run-id>

# JSON で詳細情報を取得（解析しやすい）
actrun run view <run-id> --json
```

### Step 2: ログの確認

```bash
# 全ログを確認
actrun run logs <run-id>

# 失敗したタスクのログを特定して確認
actrun run logs <run-id> --task <job_id>/<step_id>
```

`run view --json` の `steps` 配列から `status: "failed"` のステップを特定し、その `id` を `--task` に渡す。

### Step 3: 原因分類と対処

以下のパターンに分類して対処する:

#### A. ツール未インストール

**症状**: `command not found`, `No such file or directory`

**対処**:
```bash
# 依存ツールチェック
actrun doctor

# ローカルツールがあるならスキップ設定
# actrun.toml:
#   local_skip_actions = ["actions/setup-node"]
```

#### B. アクション互換性問題

**症状**: `unsupported action input`, `action not found`

**対処**:
- ビルトイン対応アクションか確認（checkout, cache, artifact, setup-node）
- 未対応アクションは `--skip-action` でスキップ
- リモートアクションは `--trust` フラグでフェッチ許可

```bash
actrun ci.yml --skip-action unsupported/action --trust
```

#### C. パス/ワークスペース問題

**症状**: ファイルが見つからない、パスが違う

**対処**:
- `--workspace-mode` を変更（`local` → `worktree` or `tmp`）
- `actions/checkout` をスキップしている場合、ファイルがカレントディレクトリにあるか確認

```bash
# worktree で隔離実行
actrun ci.yml --worktree
```

#### D. シークレット/変数の未設定

**症状**: `${{ secrets.XXX }}` が空、認証エラー

**対処**:
```bash
# シークレットを環境変数で渡す
ACTRUN_SECRET_GITHUB_TOKEN=$(gh auth token) actrun ci.yml

# .env ファイルから読み込み
actrun ci.yml --env .env.local
```

#### E. 条件式エラー

**症状**: `if` 条件の評価エラー、予期しないスキップ

**対処**:
- `--dry-run` で実行プランを確認
- `ACTRUN_LOCAL=true` による条件分岐を確認
- `${{ env.ACTRUN_LOCAL }}` が設定されているか確認

#### F. Nix 関連

**症状**: `nix develop` エラー、パッケージが見つからない

**対処**:
```bash
# Nix を無効化して切り分け
actrun ci.yml --no-nix

# アドホックパッケージを指定
actrun ci.yml --nix-packages "nodejs python312"
```

#### G. Docker/コンテナ関連

**症状**: `docker: command not found`, イメージ pull 失敗

**対処**:
```bash
# Docker が動いているか確認
actrun doctor

# ランタイム変更
actrun ci.yml --container-runtime podman
```

### Step 4: リトライ

```bash
# 修正後、失敗ジョブのみリトライ
actrun ci.yml --retry

# 特定ジョブだけ実行
actrun ci.yml --job <failed-job-id>
```

## JSON 出力の解析ポイント

`actrun run view <run-id> --json` の重要フィールド:

| フィールド | 説明 |
|-----------|------|
| `state` | `completed`, `partial_failed`, `failed` |
| `ok` | 全体の成否 (boolean) |
| `exit_code` | 終了コード |
| `steps[].id` | ステップID (`job_id/step_name`) |
| `steps[].status` | `success`, `failed`, `skipped` |
| `steps[].message` | 出力メッセージ |
| `tasks[].stdout_path` | stdout ログファイルパス |
| `tasks[].stderr_path` | stderr ログファイルパス |
| `issues[]` | 実行中の警告・問題 |

## ログファイルの直接読み取り

run store のログファイルを直接読むことも可能:

```bash
# デフォルトの run store パス
_build/actrun/runs/<run-id>/tasks/<task_id>.stdout.log
_build/actrun/runs/<run-id>/tasks/<task_id>.stderr.log
```

## 参考

- https://github.com/mizchi/actrun
