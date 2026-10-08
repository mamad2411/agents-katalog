# project-guidelines-example

## 概要
実際のプロダクション環境に基づいたプロジェクト固有スキルのテンプレートを提供する。自プロジェクトのスキルを作成する際の参考例として使用する。

## 機能要件
- アーキテクチャ概要（フロントエンド・バックエンド・データベース・AIサービスの構成図）
- ファイル構造定義（Next.js app router / FastAPI routers / テストディレクトリ）
- FastAPI向けAPIレスポンス形式（`ApiResponse[T]`ジェネリック型、`ok/fail` クラスメソッド）
- TypeScript向けフェッチラッパー（型付きレスポンス、エラーハンドリング統一）
- Claude APIツール呼び出しと構造化出力を使ったAI統合パターン（Pydantic + `tool_choice`）
- Reactカスタムフック `useApi<T>` による非同期状態管理
- バックエンド（pytest + httpx）とフロントエンド（React Testing Library + Playwright）のテスト手順
- デプロイ前チェックリスト（ビルド成功・テスト通過・シークレット確認・マイグレーション）
- Google Cloud Runデプロイコマンド
- 環境変数一覧テンプレート（フロントエンド / バックエンド）

## 対象技術
- Next.js 15 (App Router), TypeScript, React
- FastAPI, Python, Pydantic
- Supabase (PostgreSQL)
- Claude API, Anthropic SDK
- Google Cloud Run, Vercel
- pytest, Playwright, React Testing Library

## 使用例
- 新規プロジェクト開始時にプロジェクト固有スキルを作成するためのテンプレートとして参照する。
- フルスタックWebアプリとAI統合のアーキテクチャパターンを確認する際に使用する。
