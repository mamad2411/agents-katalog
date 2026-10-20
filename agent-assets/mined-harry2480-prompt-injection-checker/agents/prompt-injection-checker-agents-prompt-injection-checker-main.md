# プロンプトインジェクション検査サイト AIエージェントへの指針 (AGENTS.md)

このファイルは、このリポジトリでコードを操作する際のAIエージェントへのルールおよび指針を提供します。
プロダクトの詳細な設計ルールは `CLAUDE.md` および `docs/` を参照すること。

## プロダクトの前提（最重要）

- **GitHub Pages 上の静的サイト**。Next.js 15 を静的エクスポート（`output: 'export'`）で配信する
- **サーバー・DB・API キーを持たない**。Server Actions・API Routes・SSR/ISR・DB・Repository は使用しない
- **検知はブラウザ内で完結**。検知ロジックは外部依存を持たない純粋な TypeScript として実装し、入力を外部送信しない（URL取得を除く）
- **シークレットを持たない**。静的バンドルに秘密情報を埋め込まない

## 必須ルール

### Worktree 必須
コード変更を伴う作業は、**必ず git worktree を作成してから開始すること**。メインのリポジトリディレクトリでは直接コード変更を行わない。

```bash
# 1. worktree を作成
git worktree add ../pic-<branch-name> -b <branch-name>

# 2. 依存をインストール
cd ../pic-<branch-name> && pnpm install
```

- **目的**: `develop` ブランチを常にクリーンに保ち、作業の分離と並列作業を容易にする
- **例外なし**: ドキュメントのみの変更も含め、すべてのコミットで worktree を使用すること

### 検知ロジックの配置
**UIコンポーネント（`.tsx` ファイル）に検知ロジック（正規表現・辞書・Unicode 解析）を直接書いてはいけない。** 検知は `backend/domain` に置き、frontend は `backend/presentation/composition` 経由で UseCase を呼び出すこと。
コード例・配置場所の詳細は `docs/アーキテクチャ.md` / `docs/実装計画.md` を参照。

### 検知ルールの宣言的管理
検知ルール（各インジェクション手口のパターン）は **`backend/domain/rules/` にデータ（配列・定数）として宣言的に管理** されている。検知エンジン（コード）に直接ハードコードしないこと。

- `domain/rules/ja-rules.ts` — 日本語の検知ルール
- `domain/rules/en-rules.ts` — 英語の検知ルール
- `domain/rules/structural-rules.ts` — Unicode・エンコード等の言語非依存ルール

ルールを追加・変更したら、対応する陽性（検知すべき）・陰性（誤検知してはならない）の Unit テストを必ず追加する。

### 外部 I/O（ファイル読込・URL取得）
- **`fetch` / `FileReader` を UI や UseCase から直接呼ばない**。`domain/gateways/` の interface を介し、`infrastructure/adapters/` の実装（本番 + Stub）を Composition で注入する
- **URL取得は CORS 制約に注意**（`docs/要件定義.md` §10）。取得先の扱い（プロキシ経由等）は未確定事項として扱う
- **入力内容を外部に送信しない**。アクセス解析等を入れる場合も入力テキストは送信対象に含めない

## 作業ルール

### 要件定義・実装計画
依頼された場合は、最初に論点を洗い出してユーザーに質問しながらクリアにし、マークダウンでドキュメントを作成すること。

### 自己学習
セッション中の発見やPRレビューのフィードバックを、プロジェクト設定に反映する。

- **学びの分類先**:
  - 普遍ルール → `CLAUDE.md` / `AGENTS.md`
  - 設計・仕様の詳細 → `docs/`
  - ワークフロー改善 → `.claude/skills`, `.claude/commands`

### ドキュメント管理
設計ドキュメントの作成を依頼された場合は、`docs/` 配下に Markdown で作成すること。既存の設計ドキュメント群と用語・方針を整合させる。

### GitHub Issue作成
- プラン内容を簡略化せず、そのまま issue に記載する
- コード例、型定義、検知ルールの仕様などの詳細な実装内容を含める
- 検証方法（テストケース・確認手順）を具体的に記載する

### Push前の必須チェック
`git push` する前に、以下を必ず実行し、全てパスすることを確認する：

1. `pnpm lint` — フォーマット + リント
2. `pnpm typecheck` — 型チェック
3. `pnpm test:unit` — ユニットテスト
4. `pnpm depcruise` — 依存方向チェック

（`pnpm verify` で 1〜4 をまとめて実行できる）いずれかが失敗した場合は修正してから push すること。

## 開発コマンド

よく使うコマンド:
- `pnpm dev` — 開発サーバー起動
- `pnpm test:unit` — ユニットテスト実行
- `pnpm verify` — lint → typecheck → unit test → depcruise
- `pnpm build` — 静的エクスポート（`out/` を生成）

## アーキテクチャ

**設計思想**: DDD 4層（静的サイト向けに domain / application を中核に据え、DB・Repository・loaders/actions は不使用）

**主要技術スタック**: Next.js 15（静的エクスポート）/ TypeScript / Tailwind CSS / shadcn/ui / Vitest / dependency-cruiser / Biome。検知エンジンは外部ライブラリに依存しない純粋 TypeScript。

## ディレクトリ構造

```text
apps/webapp/src/
├── app/                 # Next.js App Router（静的生成のエントリ）
├── frontend/            # UI レイヤー（components / hooks / lib）
└── backend/             # 検知ロジック
    ├── domain/          # 検知エンジン・ルール定義・モデル（純粋ロジック）
    ├── application/     # 検査 UseCase
    ├── infrastructure/  # Gateway 実装（ファイル読込・URL取得 + Stub）
    └── presentation/    # composition（DI 組み立て）
```
