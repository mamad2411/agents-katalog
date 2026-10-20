# Laravel ブログプロジェクト設定

## プロジェクト概要

Laravel を使用したモダンなブログサイトの構築。認証、投稿管理、コメント機能を含む完全な CMS を目指す。

## 技術スタック

-   **フレームワーク**: Laravel 12.x with Sail
-   **データベース**: MySQL 8.0 (Docker)
-   **フロントエンド**: Livewire 3.x + Alpine.js + Tailwind CSS
-   **テスト**: Pest（並列実行対応）
-   **キャッシュ/キュー/セッション**: Redis
-   **認証**: Laravel Breeze + 2FA
-   **ファイルストレージ**: S3 互換（MinIO for local）

## アーキテクチャパターン

-   **ドメイン駆動設計**: `app/Domain/Blog/` 以下にドメイン層を配置
-   **サービス層パターン**: 複雑なビジネスロジックはサービスクラスに分離
-   **リポジトリパターン**: データアクセス層の抽象化（複雑なクエリのみ）
-   **イベント駆動**: ユーザーアクション時のイベント発行

## プロジェクト構造

```
app/
├── Domain/Blog/
│   ├── Models/           # Eloquentモデル
│   ├── Services/         # ビジネスロジック
│   ├── Events/           # ドメインイベント
│   └── Enums/           # 列挙型
├── Http/
│   ├── Controllers/Blog/ # コントローラー
│   ├── Requests/Blog/    # フォームリクエスト
│   └── Resources/Blog/   # APIリソース
├── Livewire/Blog/        # Livewireコンポーネント
└── Jobs/Blog/            # 非同期ジョブ

resources/
├── views/blog/           # Bladeテンプレート
└── js/                   # Alpine.jsコンポーネント

tests/
├── Feature/Blog/         # フィーチャーテスト
├── Unit/Blog/           # ユニットテスト
└── Datasets/            # Pestデータセット
```

## 開発標準とベストプラクティス

### コーディング規約

-   Laravel Pint（PSR-12 準拠）を使用
-   厳密型宣言: `declare(strict_types=1);`
-   型ヒントと DocBlock を必須とする
-   変数・メソッド名は意図を明確に表現

### データベース設計

-   Eloquent リレーションを優先（生クエリは最小限）
-   マイグレーションファイルは可逆性を保つ
-   外部キー制約とインデックスを適切に設定
-   ソフトデリートを活用

### セキュリティ

-   Form Request でバリデーション必須
-   CSRF トークンの適切な使用
-   SQL インジェクション対策（パラメータバインディング）
-   XSS 対策（適切なエスケープ）

### テスト戦略

-   フィーチャーテスト: エンドユーザー視点のテスト
-   ユニットテスト: 個別クラス・メソッドのテスト
-   テスト DB は`:memory:`を使用して高速化
-   ファクトリーとシーダーでテストデータを管理

## 必須機能要件

1. **認証システム**

    - ユーザー登録・ログイン
    - 二要素認証（2FA）
    - パスワードリセット

2. **ブログ管理**

    - 記事の作成・編集・削除
    - カテゴリ・タグ管理
    - 下書き・公開状態管理
    - 画像アップロード

3. **コメントシステム**

    - 記事へのコメント投稿
    - コメント承認制
    - スパム対策

4. **管理機能**
    - 管理者ダッシュボード
    - ユーザー管理
    - 記事統計表示

## 必須コマンドセット

```bash
# 開発環境
./vendor/bin/sail up -d              # 開発環境開始
./vendor/bin/sail down               # 開発環境停止

# データベース
./vendor/bin/sail artisan migrate:fresh --seed    # DB初期化
./vendor/bin/sail artisan migrate:status          # マイグレーション状況確認

# テスト
./vendor/bin/sail artisan test --parallel         # 並列テスト実行
./vendor/bin/sail artisan test --coverage         # カバレッジ付きテスト

# コード品質
./vendor/bin/pint                    # コード整形
./vendor/bin/sail artisan insights   # コード品質チェック

# キャッシュ管理
./vendor/bin/sail artisan optimize   # 本番環境用最適化
./vendor/bin/sail artisan config:clear && ./vendor/bin/sail artisan cache:clear  # キャッシュクリア
```

## 環境設定ガイドライン

-   `.env.example`を適切に更新・維持
-   本番環境とステージング環境で異なる設定を明記
-   API キーやシークレットは環境変数で管理
-   デバッグモードは開発環境でのみ有効化

## 禁止事項と注意点

❌ **絶対にやってはいけないこと:**

-   適切なエスケープなしでユーザー入力を使用
-   `.env`ファイルやシークレットをバージョン管理に含める
-   本番環境でデバッグモードを有効化
-   vendor ディレクトリの直接編集

❌ **避けるべきパターン:**

-   コントローラーでの複雑なビジネスロジック
-   生 SQL の乱用（Eloquent で表現困難な場合のみ使用）
-   バリデーション処理の省略
-   テストのないコード

## パフォーマンス考慮事項

-   Eloquent のイーガーローディング（N+1 問題対策）
-   Redis キャッシュの活用
-   画像最適化と CDN 使用
-   データベースインデックスの適切な設定

## 外部依存関係

主要パッケージと用途を明記：

-   `laravel/breeze`: 認証システム
-   `livewire/livewire`: リアクティブ UI
-   `spatie/laravel-permission`: 権限管理
-   `intervention/image`: 画像処理
-   `league/commonmark`: Markdown 処理

## 開発フロー

1. 機能設計とユーザーストーリー作成
2. テスト駆動開発（TDD）でテストケース先行実装
3. 最小限の実装でテストを通す
4. リファクタリングで品質向上
5. コードレビューと品質チェック
