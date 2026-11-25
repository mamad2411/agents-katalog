# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

ハルシネーション・ランチ (hlunch) - LLMを活用したレシピ生成アプリケーション

### 主要機能
- プロンプトの保存・管理
- プロンプトからLLMを使ったレシピ生成
- プロンプトの合成による新規プロンプト生成

### データモデル
- Prompt (title, prompt) - プロンプトを管理
- Recipe (title, ingredients, instructions) - レシピを管理。Promptに1:Nで紐づく

### 使用技術
- Rails 8.0.2
- SQLite3
- Bootstrap (UI)
- Turbo (ページ遷移の高速化のみ使用)

## 開発コマンド

### セットアップ
```bash
bin/setup                 # 初回セットアップ
```

### データベース
```bash
rails db:migrate          # マイグレーション実行
rails db:rollback         # マイグレーションをロールバック
rails db:seed             # シードデータ投入
rails db:reset            # DB削除、再作成、マイグレーション、シード実行
```

### サーバー起動
```bash
bin/dev                   # 開発サーバー起動
rails server              # Railsサーバーのみ起動
```

### テスト
```bash
bundle exec rspec                                    # 全テスト実行
bundle exec rspec spec/models/prompt_spec.rb         # 特定ファイルのテスト実行
bundle exec rspec spec/requests/                     # Request specの実行
```

### コード品質
```bash
bundle exec rubocop                   # Linter実行
bundle exec rubocop -a                # 自動修正可能な問題を修正
bundle exec brakeman --no-pager       # セキュリティスキャン
```

YOU MUST: Rubyファイルを編集したら `bundle exec rubocop <編集したファイル>` を自動実行する
YOU MUST: Gemfile.lockが変更されたら `bundle exec brakeman --no-pager` を自動実行する

### コンソール
```bash
rails console             # Railsコンソール起動
```

## アーキテクチャ

### ディレクトリ構造
- `app/models/` - ActiveRecordモデル
- `app/controllers/` - コントローラー（標準的なRails MVCパターン）
- `app/views/` - ERBビューテンプレート
- `db/migrate/` - データベースマイグレーション
- `spec/models/` - モデルの単体テスト
- `spec/requests/` - Request spec（コントローラーの統合テスト）
- `spec/factories/` - FactoryBotのファクトリー定義
- `doc/` - 実装計画などのドキュメント

### データベース構成
- 開発環境: `storage/development.sqlite3`
- テスト環境: `storage/test.sqlite3`

### フロントエンド
- シンプルなHTMLとERB
- Bootstrapを使用したレスポンシブデザイン
- Turboによるページ遷移の高速化（デフォルト動作のみ）

## Planモードの出力

YOU MUST: Planモードで作成したプランは必ず `doc/` ディレクトリにMarkdownファイルとして書き出す。ファイル名は `doc/` 内の既存ファイルの連番を確認して次の番号を使い、`doc/<NN>_<内容>.md`（例: `doc/06_add_logo.md`）とする。

## 開発ガイドライン

### モデル作成
```bash
rails generate model ModelName field:type
```

### コントローラー作成
```bash
rails generate controller ControllerName action1 action2
```

### テスト方針
- モデルspec (`spec/models/`): バリデーションとアソシエーションをテスト
- Request spec (`spec/requests/`): HTTPリクエスト/レスポンスとリダイレクトをテスト

### 削除リンクの書き方
```erb
<%= button_to "削除", prompt_path(@prompt), method: :delete, data: { turbo_confirm: "本当に削除しますか？" } %>
```
