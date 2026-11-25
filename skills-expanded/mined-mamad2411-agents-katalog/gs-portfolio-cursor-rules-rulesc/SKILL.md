---
description: 
globs: 
alwaysApply: true
---
# Gaussian Splattingポートフォリオサイト - Cursor Rules

## 開発手法
- **必須**: TDD（テスト駆動開発）で開発すること
- コーディングタスクでは必ず以下の順序で実行：
  1. 予想される入出力からテストコードを生成
  2. テストが失敗することを確認
  3. 実装コードを作成してテストを通す
  4. リファクタリング
- テストコードのロジックは変更禁止（モック修正以外）

## 技術スタック
- **Frontend**: React 19, TypeScript, Vite 6, React Router v7
- **UI**: shadcn/ui, Tailwind CSS
- **3D**: @playcanvas/react
- **Testing**: Vitest, @testing-library/react
- **Backend**: Cloudflare Workers, Hono
- **Database**: Cloudflare D1
- **Storage**: Cloudflare R2

## コード品質規則

### TypeScript
- 厳密な型定義を使用
- `any`型の使用禁止
- すべてのプロパティに型注釈
- インターフェースは詳細に定義

### React コンポーネント
- 関数コンポーネントのみ使用
- React 19の新機能（use() Hook、Suspense）を積極活用
- Props は interface で型定義
- コンポーネントは単一責任原則に従う
- エラーバウンダリを適切に配置

### ファイル命名規則
- コンポーネント: PascalCase（例: `GSFileCard.tsx`）
- ユーティリティ: camelCase（例: `fileValidator.ts`）
- hooks: `use` prefix（例: `useGSFiles.ts`）
- API関数: camelCase（例: `uploadGSFile.ts`）

### フォルダ構造
```
gs-portfolio-v2/
   ├── docs/                     # プロジェクトドキュメント
   ├── tasks/                    # タスク管理
   └── gs-portfolio-frontend/    # フロントエンドアプリケーション
       ├── src/
       │   ├── assets/           # react.svg
       │   ├── components/       # ui/, layout/
       │   ├── pages/            # HomePage.tsx, HomePage.test.tsx
       │   ├── lib/              # utils.ts
       │   ├── types/            # index.ts
       │   └── test/             # setup.ts
       └── 設定ファイル群
```

## セキュリティ規則
- 入力値は必ずバリデーション・サニタイズ
- ファイルアップロードは型・サイズチェック必須
- 認証トークンはHttpOnly Cookieで管理
- CSRFトークンを実装
- XSS対策を必ず実装

## パフォーマンス規則
- コンポーネントのLazy Loading実装
- 画像はサイズ最適化
- バンドルサイズを意識した実装
- 3Dモデルは適切なLOD設定

## Gaussian Splatting 固有ルール
- 対応ファイル形式: `.splat`, `.ply` のみ
- ファイルサイズ上限: 100MB（設定可能）
- サムネイルは任意アップロード
- サムネイルなしの場合はBoxアイコン表示
- 詳細ページでは1つのモデルのみ表示

## API設計ルール
- RESTful APIを遵守
- エラーレスポンスは統一形式
- 認証が必要なエンドポイントは`/admin/`prefix
- ファイルアクセスは署名付きURL使用

## テスト規則
- 各コンポーネントにUnit Test
- API層にIntegration Test
- 認証フローにE2E Test
- テストカバレッジ80%以上維持
- モックは最小限に抑制

## エラーハンドリング規則
- すべての非同期処理にエラーハンドリング
- ユーザーフレンドリーなエラーメッセージ
- エラーログは適切に分類
- 自動リトライ機能を適所に実装

## アクセシビリティ規則
- WCAG 2.1 AA準拠
- キーボードナビゲーション対応
- セマンティックHTMLの使用
- 適切なARIAラベル設定

## 実装優先順位
1. **フェーズ1**: プロジェクトセットアップ
2. **フェーズ2**: データベース・バックエンド
3. **フェーズ3**: フロントエンド基盤
4. **フェーズ4**: ユーザー向け機能
5. **フェーズ5**: 管理機能

## コミット規則

### 基本形式
- Conventional Commits形式を遵守
- 形式: `<type>(<scope>): <description>`

### コミット粒度ルール
- **1つの論理的変更 = 1コミット**
- 複数の機能や修正を1つのコミットにまとめない
- 関連性のない変更は別々のコミットに分割
- テストコードと実装コードは同一コミットでOK（TDD実践時）

### 適切なコミット例
- `feat(auth): ログイン機能の実装`
- `test(auth): ログインコンポーネントのテスト追加`
- `fix(upload): ファイルサイズバリデーションの修正`
- `refactor(components): GSFileCard コンポーネントの構造改善`
- `style(ui): ボタンコンポーネントのスタイル調整`
- `docs(readme): セットアップ手順の更新`

### 避けるべきコミット例
- `feat: 複数機能追加とバグ修正` ❌（複数の変更を含む）
- `fix: いろいろ修正` ❌（説明が曖昧）
- `update: ファイル更新` ❌（何を更新したか不明）

### コミットタイプ
- `feat`: 新機能追加
- `fix`: バグ修正
- `refactor`: リファクタリング
- `test`: テスト追加・修正
- `style`: コードスタイル修正（機能に影響なし）
- `docs`: ドキュメント更新
- `chore`: ビルド・設定ファイル更新
- `perf`: パフォーマンス改善

### スコープ例
- `auth`: 認証関連
- `upload`: ファイルアップロード
- `ui`: UIコンポーネント
- `api`: API関連
- `db`: データベース関連
- `config`: 設定関連

## 追加ガイドライン
- 日本語コメントOK（重要な部分のみ）
- 設定は環境変数で管理
- デプロイ前に必ずセキュリティチェック実行
- パフォーマンステストを定期実行 