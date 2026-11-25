# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

github-notifyは、GitHubのIssue、プルリクエスト、コミットの変更を監視してデスクトップ通知を送信するGoアプリケーションです。クロスプラットフォーム（Linux、macOS、Windows）対応で、単一バイナリとして配布されます。

## 開発コマンド

### ビルドとテスト
```bash
# 依存関係のダウンロード
make deps

# ビルド
make build

# テスト実行
make test

# 開発用ビルド（デバッグ情報付き）
make build-dev

# プログラム実行
make run

# テスト通知送信
make test-notify
```

### インストール
```bash
# ローカルインストール (~/.local/bin)
make install

# システムインストール (sudo required)
make install-system

# リリースビルド (複数プラットフォーム)
make build-release
```

### 設定
```bash
# 設定ファイル情報表示
make config-info

# systemdタイマー設定 (Linux)
make setup-systemd
```

## アーキテクチャ

### ディレクトリ構造
```
cmd/github-notify/main.go     - エントリーポイント、CLI設定
internal/config/config.go     - 設定管理（YAML読み込み、バリデーション）
internal/github/client.go     - GitHub API クライアント
internal/cache/manager.go     - 重複防止キャッシュシステム
internal/notifier/desktop.go  - クロスプラットフォーム通知
```

### 主要コンポーネント

#### 1. 設定管理（config）
- YAMLベースの設定ファイル（`~/.config/github-notify/config.yaml`）
- GitHub Token、監視対象リポジトリ、通知設定を管理
- 初回実行時にデフォルト設定を自動生成

#### 2. GitHub API クライアント（github）
- GitHub API v4を使用した通知・コミット取得
- ページネーション対応で大量データを効率的に処理
- レート制限チェック機能
- 全ブランチ監視（`branches: ["*"]`）対応

#### 3. キャッシュシステム（cache）
- SHAベースのコミット重複チェック
- 通知ID重複チェック
- JSONファイルでの永続化（`~/.cache/github-notify/`）
- thread-safe な実装

#### 4. 通知システム（notifier）
- beeepライブラリによるクロスプラットフォーム通知
- プラットフォーム別アイコン設定
- 通知タイプ：Issue、PR、コミット
- バルク通知とサマリー通知対応

#### 5. メインロジック（main）
- Cobraを使用したCLI実装
- 通知チェックとコミットチェックを並行実行
- エラーハンドリングと詳細ログ出力

### 設定ファイル例

```yaml
# GitHub Token（環境変数GITHUB_TOKENも使用可能）
github_token: "ghp_xxxxxxxxxxxxxxxxxxxx"

# 監視対象リポジトリ
repositories:
  - repo: "microsoft/vscode"
    branches: ["main"]
  - repo: "torvalds/linux" 
    branches: ["master"]
  - repo: "golang/go"
    branches: ["*"]  # 全ブランチ監視

# 通知設定
notifications:
  enable_issues: true
  enable_prs: true  
  enable_commits: true
```

### 使用ライブラリ

- `github.com/spf13/cobra` - CLI フレームワーク
- `github.com/google/go-github/v62` - GitHub API クライアント
- `golang.org/x/oauth2` - OAuth2 認証
- `github.com/gen2brain/beeep` - クロスプラットフォーム通知
- `gopkg.in/yaml.v3` - YAML パーサー

### テストとデバッグ

- `go test -v ./...` でユニットテスト実行
- `--verbose` フラグで詳細ログ出力
- `--test` フラグでテスト通知送信
- キャッシュファイルは `~/.cache/github-notify/` で確認可能

### 定期実行設定

- Linux: systemd timer（`make setup-systemd`）
- macOS: launchd
- Windows: タスクスケジューラ
- cron: 5分間隔での実行推奨