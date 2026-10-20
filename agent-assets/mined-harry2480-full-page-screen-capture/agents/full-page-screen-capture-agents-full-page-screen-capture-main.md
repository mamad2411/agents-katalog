<!--
【テンプレート】AIエージェント運用ガイド
リポジトリ内でAIエージェント（Copilot, Claude Code, Cursorなど）が自律的または対話的にコード操作・調査・ドキュメント作成を行う際のルールや指針を定義するテンプレートです。
プレースホルダー（{{ }}）をプロジェクト固有の情報に置き換えて使用してください。
-->

# {{PROJECT_NAME / 例：〇〇プロジェクト}} AIエージェントへの指針 (AGENTS.md)

このファイルは、このリポジトリでコードを操作する際のAIエージェントへのルールおよび指針を提供します。

## 必須ルール

### {{WORKTREE_RULE_TITLE / 例：Worktree必須}}
コード変更を伴う作業は、**必ず {{GIT_WORKFLOW / 例：git worktree}} を作成してから開始すること**。メインのリポジトリディレクトリでは直接コード変更を行わない。

```bash
# 1. {{WORKFLOW_STEP_1 / 例：worktreeを作成}}
{{CMD_WORKTREE_CREATE / 例：git worktree add ../{{PROJECT_PREFIX}}-<branch-name> -b <branch-name>}}

# 2. {{WORKFLOW_STEP_2 / 例：環境や権限定義のコピー}}
{{CMD_ENV_COPY / 例：cp .env ../{{PROJECT_PREFIX}}-<branch-name>/}}
```

- **目的**: {{WORKFLOW_PURPOSE / 例：developブランチを常にクリーンに保ち、作業の分離と並列作業を容易にする}}
- **例外なし**: {{WORKFLOW_EXCEPTION / 例：ドキュメントのみの変更も含め、すべてのコミットでworktreeを使用すること}}

### データアクセス
**UIコンポーネント（{{UI_EXTENSION / 例：`.tsx`}}ファイル）から{{DB_CLIENT / 例：Supabase}}を直接呼び出してはいけない。** {{SERVICE_LAYER / 例：Service層}}経由でアクセスすること。
コード例・配置場所の詳細は設計ガイドラインを参照。

### {{DECLARATIVE_DATA_TITLE / 例：宣言的データ管理}}
{{DATA_DOMAIN / 例：マスターデータや定義データ}}は **{{DATA_FORMAT / 例：YAML}}ファイルで宣言的に管理** されている。SQLマイグレーションで直接変更しないこと。
- `{{DATA_FILE_PATH_1 / 例：data/items.yaml}}` - {{DATA_DESC_1 / 例：アイテム定義}}
- CI/CDデプロイ時に `{{SYNC_CMD / 例：npm run data:sync}}` で自動同期される

### 認可（Authorization）
- **{{USER_ID_VAR / 例：userId}}は必ずサーバーサイドでセッションから取得する**（クライアントから受け取らない）
- **認可チェックは{{ACTION_LAYER / 例：actions層}}で行う**
- **リソースの所有者チェックは専用の認可関数に分離する**

## 作業ルール

### {{PARALLEL_PR_RULE / 例：並列PR作成}}
複数の独立したPRを作成する場合は `{{SKILL_PARALLEL_PR / 例：/parallel-pr}}` スキルを使用すること。

### 要件定義・実装計画
依頼された場合は、最初に論点を洗い出してユーザーに質問しながらクリアにし、マークダウンでドキュメントを作成すること。

### 自己学習
セッション中の発見やPRレビューのフィードバックを、プロジェクト設定に自動反映する仕組み。

- **PRレビュー後**: `{{SKILL_RETRO / 例：/retro}} {PR番号}` でCodeRabbit・レビュアーの指摘を分析し、各種設定ファイルに反映する
- **学びの分類先**:
  - 普遍ルール → `{{GUIDELINE_FILE / 例：CLAUDE.md}}`
  - ワークフロー改善 → `{{SKILLS_DIR / 例：skills/commands}}`
  - 運用知識・ワークアラウンド → `{{MEMORY_FILE / 例：MEMORY.md}}`

### ドキュメント管理
設計作業などのドキュメント作成を依頼された場合は、以下のルールに従ってファイルを作成すること：

- ファイル名: `{{DOC_NAME_FMT / 例：YYYYMMDD_HHMM_{日本語の作業内容}.md}}`
- 保存場所: `{{DOC_DIR / 例：docs/}}` 以下
- フォーマット: Markdown

### GitHub Issue作成
- プラン内容を簡略化せず、そのままissueに記載する
- コード例、SQL、型定義などの詳細な実装内容を含める
- 検証方法を具体的に記載する

### Push前の必須チェック
`git push` する前に、以下のコマンドを必ず実行し、全てパスすることを確認する：

1. `{{CHECK_CMD_1 / 例：pnpm run biome:check:write}}` - フォーマット + リント
2. `{{CHECK_CMD_2 / 例：pnpm run typecheck}}` - 型チェック
3. `{{CHECK_CMD_3 / 例：pnpm run test:unit}}` - ユニットテスト

いずれかが失敗した場合は修正してからpushすること。

## 開発コマンド

よく使うコマンド:
- `{{DEV_CMD / 例：pnpm run dev}}` - 開発サーバー起動
- `{{TEST_CMD / 例：pnpm run test:unit}}` - ユニットテスト実行

## アーキテクチャ

**設計思想**: {{ARCH_CONCEPT / 例：機能単位モジュール分割}}

**主要技術スタック**: {{TECH_STACK / 例：Next.js / Supabase / Tailwind CSS / TypeScript}}

## ディレクトリ構造

```text
{{SRC_DIR / 例：src/}}
├── {{APP_DIR / 例：app/}}              # {{APP_DIR_DESC / 例：ルーティング}}
├── {{COMPONENTS_DIR / 例：components/}}       # {{COMPONENTS_DIR_DESC / 例：共通UIコンポーネント}}
├── {{FEATURES_DIR / 例：features/}}         # {{FEATURES_DIR_DESC / 例：機能ベースモジュール}}
└── {{LIB_DIR / 例：lib/}}              # {{LIB_DIR_DESC / 例：共有ライブラリ}}
```
