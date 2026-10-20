# プロンプトインジェクション検査サイト

任意のテキストにプロンプトインジェクションが含まれていないかを、ブラウザ内のルールベース検知で検査する静的サイト。**GitHub Pages** 上で動作し、サーバー・DB・API キーを持たない。入力は外部に送信されない（URL取得を除く）。

## 使い方（利用者向け）

- `pnpm dev` で開発サーバーを起動
- `pnpm verify` で品質チェック（変更後に実行）
- 「〇〇な検知ルールを追加して」「〇〇な画面を作って」など、やりたいことを Claude Code に指示するだけでOK
- エラーが出たらエラーメッセージを貼り付けて「直して」と指示

### コマンド一覧

```sh
pnpm dev        # 開発サーバー起動
pnpm verify     # lint → typecheck → unit test → depcruise
pnpm test:unit  # Unit テスト（検知ロジック中心）
pnpm test:e2e   # E2E テスト（任意・クリティカルパスのみ）
pnpm lint:fix   # 自動フォーマット
pnpm build      # 静的エクスポート（out/ を生成）
```

> DB を持たないため、`prisma generate` / `db:migrate` / Integration（DB 接続）テストは**使用しない**。

---

## Claude Code への指示（利用者は読まなくてOK）

### プロダクトの性質（最重要）

- **静的サイト**: Next.js 15 App Router を**静的エクスポート**（`output: 'export'`）で GitHub Pages に配信する
- **サーバー機能は使用不可**: Server Actions・API Routes・動的 `next/image`・SSR/ISR・DB は使わない
- **検知はブラウザ内で完結**: 検知ロジックは外部依存を持たない純粋な TypeScript として実装し、入力を外部送信しない
- **シークレットを持たない**: 静的バンドルに埋め込む値はすべて公開される前提。秘密情報を埋め込まない

### アーキテクチャ

pnpm workspace monorepo。`apps/webapp/` に Next.js 15 App Router アプリ。

バックエンド (`apps/webapp/src/backend/`) は DDD 4層構造:

```text
依存方向: presentation → application → domain ← infrastructure
```

- **domain** — 検知エンジン・検知ルール（データ）・モデル。外部依存なし。最内層
- **application** — UseCase（検査オーケストレーション）。domain のみ依存（infrastructure 直接参照禁止、Gateway interface 経由）
- **infrastructure** — Gateway 実装（ファイル読込・URL取得）。domain の interface を implements。**DB/Repository は不使用**
- **presentation** — composition（唯一の DI ポイント、全層参照可）。**loaders/actions はサーバーが無いため不使用**

### ファイル配置ルール

```text
apps/webapp/src/backend/
├── domain/
│   ├── models/          # ドメインモデル (.model.ts) — 検出結果・リスクスコア
│   ├── services/        # 検知エンジン (.service.ts)
│   ├── rules/           # 検知ルール定義（データ）— ja / en / 言語非依存
│   └── gateways/        # Gateway interface (.gateway.ts) — ファイル読込・URL取得
├── application/
│   └── usecases/        # UseCase (.usecase.ts) — 検査オーケストレーション
├── infrastructure/
│   └── adapters/        # Gateway 実装 (.adapter.ts) — 本番 + Stub
└── presentation/
    └── composition/     # DI組み立て (.composition.ts)

apps/webapp/src/frontend/
├── components/          # UI（'use client'）。ui/ + inspection/
├── hooks/               # use-inspection.ts 等
└── lib/                 # クライアント側 util
```

> `infrastructure/repositories`・`infrastructure/db`・`presentation/loaders`・`presentation/actions` は本プロダクトでは作らない（DB・サーバーが無いため）。

### Key Rules

- ファイル命名: kebab-case + レイヤーサフィックス
- 検知ルールは `domain/rules/` に**データ（配列・定数）として定義**し、検知エンジン（コード）から分離する
- 検知エンジンは入力とルールを受け取り検出結果を返す**純粋関数/クラス**（副作用・DOM・ブラウザ API 依存なし）
- Rich Domain Model 必須。バリデーション・生成はモデル自身のメソッドで行う
- サービス（UseCase, Domain Service）はクラスベース + コンストラクタ DI。関数エクスポート禁止（型・ルール定義データ・ユーティリティ型は例外）
- Domain 層のエラーは `Result<T, E>` 型で返す。Application/Infrastructure（ファイル読込・URL取得失敗等）は throw
- 外部 I/O（`fetch`・`FileReader`）は Gateway 実装に閉じ込め、必ず Stub 実装を用意。Composition で本番/Stub を切り替え
- `index.ts` バレルエクスポート禁止
- frontend は `backend/presentation/composition` 経由でのみ検知機能を利用（domain・infrastructure を直接 import 禁止）
- Server Component デフォルト。検査 UI（入力・検知実行）は `'use client'`

### テスト

- Unit（中心）: domain（検知エンジン・ルール・モデル）+ application（UseCase、Gateway は Stub）。カテゴリごとに陽性・陰性ケースを用意
- E2E（任意）: 「貼り付け → 検査 → 結果表示」のクリティカルパス（Playwright）
- Integration（DB 接続）は**不使用**
- テストパス: `test/unit/`, `test/e2e/`（ソース構造を mirror）

### 品質チェック

`pnpm verify` は lint → typecheck → unit test → depcruise を順に実行する（`prisma generate` は不使用のため含めない）。
コード変更後は必ず `pnpm verify` を実行して全パスすることを確認する。

### 詳細ルール

詳細な設計ルールは必要に応じて `docs/` を読むこと:

- `docs/要件定義.md` — 機能要件・検知カテゴリ・制約・受け入れ条件
- `docs/アーキテクチャ.md` — DDD 4層（静的サイト向け適用範囲）・依存ルール・命名規約
- `docs/フロントエンドアーキテクチャ.md` / `docs/フロントエンド規約.md` — UI スタック・データフロー・Server/Client 使い分け
- `docs/インフラストラクチャ規約.md` — 静的エクスポート・GitHub Pages デプロイ
- `docs/リポジトリ層設計規約.md` — Gateway（ファイル読込・URL取得）設計
- `docs/テストガイドライン.md` / `docs/品質チェック・テスト規約.md` — テスト方針・verify コマンド
- `docs/スタイルガイド.md` — Tailwind スタイルルール・アクセシビリティ
- `docs/実装計画.md` — 実装フェーズ・ディレクトリ構成・実装例コード
