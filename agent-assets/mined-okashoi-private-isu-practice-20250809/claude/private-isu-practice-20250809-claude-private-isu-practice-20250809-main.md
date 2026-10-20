# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

Private ISU練習環境 - ISUCONスタイルのパフォーマンスチューニングコンテスト用アプリケーション。Instagram風のソーシャルメディアプラットフォーム（画像アップロード、投稿、コメント、ユーザー管理機能）。

## 競技ルール・制約

### 競技時間・スコアリング
- **スコア計算**: 成功レスポンス数(GET) x 1 + 成功レスポンス数(POST) x 2 + 成功レスポンス数(画像投稿) x 5 - (サーバエラー x 10 + リクエスト失敗 x 20 + 遅延POSTレスポンス x 100)
- **重要制約**: `/initialize` エンドポイントは10秒以内に応答必須

### 許可される変更
- データベーススキーマ変更・インデックス作成削除
- キャッシュ機構追加
- 遅延書き込み用ジョブキュー実装
- 他言語での再実装

### 厳格な保持要件（変更禁止）
- URIアクセスポイント
- HTML DOM構造
- JavaScript/CSSファイル
- メディアファイル内容
- メンテナンスコマンド互換性
- サーバー再起動後の動作
- ベンチマーク中に書き込まれたデータの保持

### 禁止事項
- 他チームへの妨害行為
- 提供EC2インスタンス外のリソース使用
- DOM構造の変更
- 機能的な動作の変更

## アーキテクチャ

### システム構成
- **Webアプリケーション**: Go (Chi router + sqlx) - `golang/app.go`
- **データベース**: MySQL 8.4 - ユーザー、投稿、コメントデータ
- **セッション管理**: Memcached + gorilla-sessions-memcache
- **Webサーバー**: Nginx - リバースプロキシと静的ファイル配信
- **開発環境**: Docker Compose

### データモデル
- `User`: account_name, passhash, authority, del_flg (論理削除)
- `Post`: user_id, imgdata (BLOB), body, mime, created_at
- `Comment`: post_id, user_id, comment, created_at

## 開発・運用コマンド

### 基本開発サイクル
```bash
# ISUCON練習用の完全デプロイサイクル
make gogo                   # 停止 → ビルド → ログクリア → 開始

# 個別操作
make build                  # Go アプリケーションビルド
make stop-services         # 全サービス停止
make start-services        # 全サービス開始
```

### ログ管理・分析
```bash
# アプリケーションログ
make logs                   # 最新ログ表示
make logs/error            # エラーログのみ
make logs limit=1000       # 指定行数表示
make logs/clear            # 全ログクリア

# パフォーマンス分析
make kataribe              # Nginxアクセスログ分析
make pprof                 # CPU プロファイリング (90秒)
make pprof time=30         # カスタム時間指定

# ベンチマーク
make bench                 # ベンチマーク実行
```

### 専用分析ツール (`mybin/`)

#### MySQL スロークエリ分析
```bash
# スロークエリログ設定
./mybin/mysql/mysql_slow_query.sh init  # 初期設定
./mybin/mysql/mysql_slow_query.sh on    # 有効化
./mybin/mysql/mysql_slow_query.sh off   # 無効化
```

#### Nginx ログ管理
```bash
# アクセスログ設定
./mybin/nginx/init_nginx_access_log.sh    # with_time フォーマット設定
./mybin/nginx/enable_nginx_access_log.sh  # ログ有効化
./mybin/nginx/disable_nginx_access_log.sh # ログ無効化
```

## パフォーマンス最適化戦略

### データベース最適化
1. **インデックス設計**: 頻繁なクエリパターンの分析
2. **N+1問題解決**: JOIN やバルクロードの活用
3. **スロークエリ分析**: `mybin/mysql/mysql_slow_query.sh` 活用
4. **不要カラム削除**: SELECT文の最適化

### アプリケーション最適化
1. **画像処理**: BLOBからファイルシステムへの移行検討
2. **キャッシュ戦略**: Memcached活用の拡大
3. **並行処理**: Goroutine の適切な利用
4. **JSON処理**: 不要なマーシャリング削除

### インフラ最適化
1. **静的ファイル配信**: Nginx直接配信
2. **gzip圧縮**: レスポンスサイズ削減
3. **接続プール**: データベース接続の最適化
4. **ログレベル調整**: 本番時のログ出力制御

## 重要な設定

### サービス設定
- **アプリケーション**: ポート8080 (systemd: `isu-go.service`)
- **MySQL**: ポート3306 (root/root)
- **Memcached**: ポート11211
- **Nginx**: ポート80 (アプリケーションへプロキシ)

### 初期化処理
データベース初期化(`golang/app.go:79`)では、パフォーマンステスト用に：
- テストデータ削除 (users>1000, posts>10000, comments>100000)
- ユーザー削除フラグリセット
- 50番目ごとのユーザー削除設定

### プロファイリング
- CPU プロファイリング: `/debug/fgprof` エンドポイント
- アクセス解析: kataribe による統計生成
- エラー監視: journalctl による集約ログ

パフォーマンスチューニング時は `make gogo` による完全サイクル実行を推奨。

## 作業指針

### 原則
- 最小のステップ、最小の差分で指示の完遂を目指す
- 最初に最新のリモートリポジトリのmainブランチを取り込んでから作業用ブランチを切る

### パフォーマンス改善の原則
1. ボトルネックを特定してから最適化を行う
2. 最も効果の高い改善から着手する
3. 変更前後でパフォーマンスを計測し、効果を確認する
4. N+1問題の解消など、ロジック自体を早くすることを優先
5. GitHub issueの最新施策状況を優先度判断に反映

### コード変更管理ルール
1. 変更は小さな単位で行い、それぞれの目的を明確にする
2. 変更後は必ずテストを行い、問題が解決したことを確認する
3. 変更内容は適切にコミットし、日本語でわかりやすいコミットメッセージを記述する
4. コードは`go build`が通ったことを確認してから提示する
5. 提示する前に`go fmt`をかけて整形する

### ISUCON固有Tips

- シャーディング対応しやすいN+1問題解消時はJOINよりもWHERE INを使うこと

### Go言語 sqlx バルク処理パターン

#### NamedExecを使ったバルクINSERT
```go
// 構造体のスライスを用意
items := []*UserItem{
    {ID: 1, UserID: 100, ItemID: 1, Amount: 10, CreatedAt: now, UpdatedAt: now},
    {ID: 2, UserID: 100, ItemID: 2, Amount: 20, CreatedAt: now, UpdatedAt: now},
    // ...
}

// NamedExecにスライスを渡すことで自動的にバルクINSERTが実行される
query := `INSERT INTO user_items(id, user_id, item_id, amount, created_at, updated_at)
          VALUES (:id, :user_id, :item_id, :amount, :created_at, :updated_at)`

if _, err := tx.NamedExec(query, items); err != nil {
    return err
}
```

#### sqlx.Inを使った安全なWHERE IN句の構築
```go
// IDのスライス
ids := []int64{1, 2, 3, 4, 5}

// sqlx.Inを使って安全にIN句を構築
query := "SELECT * FROM user_items WHERE id IN (?)"
query, params, err := sqlx.In(query, ids)
if err != nil {
    return err
}

// 実行
items := []*UserItem{}
if err := tx.Select(&items, query, params...); err != nil {
    return err
}
```
