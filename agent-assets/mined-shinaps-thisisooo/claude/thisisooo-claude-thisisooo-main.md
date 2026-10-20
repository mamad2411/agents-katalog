# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 開発言語
自然言語での出力に関しては日本語を使用してください。

## プロジェクト概要
AIがあらゆるテーマでインタビュー記事を自動生成するサービス。Next.js 15 + Cloudflare Workers で構築。

## 技術スタック
- **フレームワーク**: Next.js 15 (App Router, Typed Routes有効)
- **ランタイム**: Cloudflare Workers (@opennextjs/cloudflare)
- **認証**: better-auth (Google OAuth + Email/Password)
- **ORM**: Drizzle ORM
- **データベース**:
  - Turso (LibSQL) - 認証データ用
  - Cloudflare D1 (SQLite) - アプリケーションデータ用 (articles, interviews, user profiles)
- **AI**: Vercel AI SDK + OpenAI
- **スタイリング**: Tailwind CSS 4 + shadcn/ui
- **Linter/Formatter**: Biome
- **パッケージマネージャー**: pnpm

## 主要コマンド

### 開発・ビルド
```bash
pnpm dev           # ローカル開発サーバー起動
pnpm build         # プロダクションビルド
pnpm start         # プロダクションサーバー起動
pnpm lint          # Linter実行
pnpm fix           # Biomeでコード自動修正 (src配下)
pnpm preview       # Cloudflareプレビュー環境でビルド確認
```

### デプロイ
```bash
pnpm deploy:stg    # ステージング環境へデプロイ (stg.thisis.ooo)
pnpm deploy:prod   # 本番環境へデプロイ (thisis.ooo)
```

### データベース操作

#### Turso (認証データ)
```bash
pnpm better-auth:generate      # better-authスキーマ生成
pnpm generate:turso            # Tursoマイグレーションファイル生成
pnpm migrate:turso:stg         # ステージング環境へマイグレーション
pnpm migrate:turso:prod        # 本番環境へマイグレーション
```

#### D1 (アプリケーションデータ)
```bash
pnpm generate:d1               # D1マイグレーションファイル生成
pnpm migrate:d1:dev            # ローカル開発環境へマイグレーション
pnpm migrate:d1:preview        # プレビュー環境へマイグレーション
pnpm migrate:d1:stg            # ステージング環境へマイグレーション (リモート)
pnpm migrate:d1:prod           # 本番環境へマイグレーション (リモート)
```

#### Cloudflare型定義
```bash
pnpm cf-typegen                # wranglerからCloudflare環境変数の型定義生成
```

## アーキテクチャ

### データベース構造
プロジェクトは**2つの独立したデータベース**を使用:

1. **Turso (LibSQL)** - `src/drizzle/schema/turso/`
   - better-authの認証データ (users, sessions, accounts等)
   - Turso固有の接続クライアント (`@libsql/client`) を使用

2. **Cloudflare D1 (SQLite)** - `src/drizzle/schema/d1/`
   - `articles` - 記事データ
   - `interviews` - インタビューデータ
   - `userProfile` - ユーザープロフィール
   - Cloudflare Workers環境で利用

### データベース接続パターン
- **Turso**: `src/lib/auth.ts` で `@libsql/client/web` + `drizzle-orm/libsql` を使用
- **D1**: `src/drizzle/client.ts` で `getCloudflareContext()` 経由で取得し `drizzle-orm/d1` を使用
  - `getDb()` - 同期版 (Server Components用)
  - `getDbAsync()` - 非同期版 (必要に応じて)

### ルーティング構造
Next.js App Routerの**Parallel Routes**を活用:

- `src/app/layout.tsx` - ルートレイアウト (header slotとchildren slotを持つ)
- `src/app/@header/` - ヘッダー用Parallel Route
- `src/app/(index)/` - トップページ (Route Group)
- `src/app/interviews/` - インタビュー機能
- `src/app/articles/` - 記事表示機能
- `src/app/profile/` - プロフィール機能
- `src/app/sign-in/` - サインイン

### 認証フロー
- `src/lib/auth.ts` でbetter-authインスタンスを設定
- Turso + Drizzle Adapterを使用
- Google OAuth + Email/Password認証対応
- `src/middleware.ts` でセッションクッキーを確認し未認証時は `/sign-in` へリダイレクト
  - パブリックルート: `/`, `/sign-in`, `/articles/*`
- **after hook**: OAuth認証後、D1のuserProfileテーブルに自動でプロフィール作成

### インタビュー機能
- `src/app/interviews/_prompts/` - 各インタビューテーマ別のプロンプト定義
  - career, hobby, favoriteArtist, favoriteBook, favoriteMovie, favoriteGame, recentRestaurant, selfIntroduction, product, thoughtReason
  - `index.ts` でプロンプトマッピングと日本語タイトル定義
- `src/app/interviews/_actions/` - Server Actions
- `src/app/interviews/[interviewId]/` - 動的ルート (インタビュー実行画面)
- Vercel AI SDK (AI RSC) でストリーミング対応のインタビュー生成

### Cloudflare環境設定
- `wrangler.jsonc` で3環境を定義:
  - **development** (local/preview)
  - **staging** (`stg.thisis.ooo`)
  - **production** (`thisis.ooo`)
- 各環境ごとにKV, D1, R2 bindingを設定
- D1マイグレーションディレクトリ: `drizzle/d1`
- R2バケット: Next.jsのインクリメンタルキャッシュ用

### 環境変数管理
- `src/lib/env.ts` で `@t3-oss/env-nextjs` + Zod を使用し型安全に管理
- 必要な環境変数:
  - `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`
  - `TURSO_DATABASE_URL`, `TURSO_AUTH_TOKEN`
  - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
  - `OPENAI_API_KEY`, `OPENAI_ADMIN_API_KEY`, `OPENAI_PROJECT_ID`
  - `NEXT_PUBLIC_APP_URL`
- 環境別のファイル: `.env`, `.env.development`, `.env.production`

### コンポーネント構成
- `src/components/ui/` - shadcn/uiコンポーネント
- `src/components/` - アプリケーション共通コンポーネント (confirm-dialog, providers等)
- 各ページディレクトリ内に `_components/`, `_actions/` を配置 (Private Folders)

### shadcn/ui MCPツールの使用
UIコンポーネントが必要な場合、以下のMCPツールを**優先的に**使用すること:

1. **コンポーネント検索**
   - `mcp__shadcn__search_items_in_registries` - コンポーネントを検索
   - `mcp__shadcn__list_items_in_registries` - 利用可能なコンポーネント一覧を取得

2. **コンポーネント詳細確認**
   - `mcp__shadcn__view_items_in_registries` - コンポーネントの詳細情報とファイル内容を確認
   - `mcp__shadcn__get_item_examples_from_registries` - 使用例とデモコードを確認

3. **コンポーネント追加**
   - `mcp__shadcn__get_add_command_for_items` - インストールコマンドを取得
   - 取得したコマンドを実行してプロジェクトに追加

**ワークフロー例:**
```
1. 必要なUIを実装する前に、shadcn MCPで既存コンポーネントを検索
2. 適切なコンポーネントが見つかったら、view_itemsで実装内容を確認
3. get_item_examplesで使用例を確認
4. get_add_commandでインストールコマンドを取得し実行
5. プロジェクトに統合
```

**重要:** 新規UIコンポーネントを自作する前に、必ずshadcn MCPで既存のコンポーネントやブロックが利用できないか確認すること。

## 開発ルール

### 実装の基本フロー
**すべてのコード変更後は必ず以下のフローを実行すること:**

1. **既存コードの参照**
   - 新しいコードを書く前に、必ず既存の類似実装を確認する
   - データベースクエリは既存のクエリパターンに従う（`db.query`は使用しない）
   - 既存のコーディングスタイルとパターンを踏襲する

2. **ビルドチェック**
   - 実装が完了したら必ず `pnpm build` を実行する
   - TypeScriptの型エラーがないことを確認する
   - ビルドエラーが出た場合は修正してから次のタスクに進む

3. **データベースクエリのパターン**
   - ❌ 使用禁止: `db.query.article.findFirst()` などの`query` API
   - ✅ 使用推奨: `db.select().from(table).where()` パターン
   - 既存コード（例: `src/app/articles/[articleId]/page.tsx`）を参考にする

### ページ実装の原則
**各ページは完全に独立した実装を行う**こと。以下のルールを厳守してください:

1. **ヘッダーの実装**
   - 各ページごとに必ず `src/app/@header/[対応するパス]/page.tsx` を作成する
   - デフォルトのヘッダー (`src/app/@header/page.tsx`) に依存しない
   - デフォルトだと反映されないことがあるため、明示的にページごとに実装する

2. **コンポーネントとアクションの分離**
   - 各ページディレクトリに `_components/` と `_actions/` を独立して作成する
   - 他のページとコンポーネントやアクションを共通化しない
   - 共通化が必要な場合は人間が判断して実施する

3. **独立したレイアウト設計**
   - 各ページは全く違うレイアウトで実装できるようにする
   - ページ間の依存関係を最小限にする
   - 将来的な変更や拡張に柔軟に対応できる構造を維持する

## 重要な設定

### Next.js設定 (`next.config.ts`)
- `serverExternalPackages`: `@libsql/client`, `@libsql/isomorphic-ws` を外部化
- `experimental.serverActions.bodySizeLimit`: 5MB
- `typedRoutes: true` - 型安全なルーティング
- `@opennextjs/cloudflare` の開発モード初期化

### OpenNext設定 (`open-next.config.ts`)
- R2インクリメンタルキャッシュ + Regional Cache使用
- `mode: 'long-lived'`, `shouldLazilyUpdateOnCacheHit: true`

### Drizzle設定
- `drizzle.turso.config.ts` - Turso用 (dialect: turso)
- `drizzle.d1.config.ts` - D1用 (dialect: sqlite)
- 各設定で `out`, `schema` ディレクトリを分離
