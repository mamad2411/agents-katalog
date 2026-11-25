---
description: nomoca-kagawa プロジェクトの開発ルール
alwaysApply: true
---

# Cursor Project Rules

## 開発ブランチ作成ルール

新しいチャットで指示を受けた際は、必ず以下の手順で作業を実行してください：

### 1. 開発ブランチの作成
- `develop`ブランチから新しい開発ブランチを作成
- 開発ブランチ名は作業内容を表す適切な名前を付ける（例：`feature/otp-button-removal`、`fix/login-validation`など）

### 2. 作業の実行
- 作成した開発ブランチで作業を実行
- コードの変更や新機能の実装を行う

### 3. 作業完了後の処理
- 作業完了後、developブランチにマージ
- 必要に応じてプルリクエストを作成

### 4. ブランチ作成コマンド例
```bash
git checkout develop
git pull origin develop
git checkout -b feature/[作業内容]
```

## フロントエンドアーキテクチャルール

### 1. page.tsx の責務（薄いコンテナパターン）
`app/*/page.tsx` は以下の責務のみを持つ薄いコンテナとして実装する：

#### 許可される処理
- ルーティング処理（`router.push` など）
- UI コンポーネントへの props 受け渡し
- 軽い URL パラメータの読取（`useSearchParams` 推奨）
- `Suspense` によるローディング境界の設定

#### 禁止される処理
- API 呼び出し（fetch など）
- ビジネスロジック
- 状態機械の実装
- モック処理
- 複雑な状態管理

### 2. レイヤー分離

#### services/ - API クライアント層
- **責務**: API 呼び出しの実装、fetch 処理の隔離
- **配置**: `src/services/`

#### hooks/ - ビジネスロジック層
- **責務**: 状態管理、ビジネスロジック、副作用の管理
- **配置**: `src/hooks/`
- **管理する状態**: フォーム状態、ローディング状態、エラー状態、ステップ管理など

#### components/templates/ - プレゼンテーション層
- **責務**: UI の描画のみ
- **禁止事項**: ビジネスロジック、API 呼び出し、状態管理
- **受け取るもの**: props として渡された値とコールバック関数

### 3. データフロー

```
page.tsx (薄いコンテナ)
  ↓ useRouter
  ↓ useCustomHook (hooks/)
    ↓ API クライアント (services/)
      ↓ fetch
  ↓ props
components/templates/ (プレゼンテーション)
```

このルールにより、保守性、テスタビリティ、再利用性の高いコードを実現します。
