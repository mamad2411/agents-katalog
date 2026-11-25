---
name: aidlc-init-profile
description: .aidlc-workflow/profile/を自動検出・スキャフォールドし、プロジェクト固有情報を生成する。
---

# プロジェクトプロファイル初期化

## project-profile とは

AI-DLC ワークフローをプロジェクト非依存にするための仕組み。ワークフローの骨格（Intent→Unit→Bolt、DDD概念、TDDサイクル）は共通だが、技術スタック・テストコマンド・lint設定はプロジェクトごとに異なる。`.aidlc-workflow/profile/` にプロジェクト固有情報を markdown で記述し、ワークフローがそれを読んで適応する。

### 設計原則

- **ワークフロー側はプロジェクト固有情報をハードコードしない** — コマンド名、ディレクトリパス、ツール名は全て profile から読み取る
- **ユーザーは markdown 自然言語で書く** — YAML スキーマではなく、人間が読み書きしやすい形式
- **DDD 概念定義はワークフロー側に残す** — 「Entity とは何か」等は `rules/aidlc-ddd.md` に残し、「どのディレクトリに配置するか」は profile に置く
- **git 管理対象** — チームで共有する

### 5ロール

| ロール | ファイル | ワークフローが読み取るもの | 参照元の例 |
|--------|----------|---------------------------|-----------|
| Stack | stack.md | 言語、ランタイム、パッケージマネージャ、主要フレームワーク | aidlc-init-profile、aidlc-plan-task |
| Structure | structure.md | パッケージ一覧、各パッケージのパスと type（BE/FE/shared） | aidlc-scan-codebase、aidlc-dev、aidlc-test |
| Testing | testing.md | テスト実行コマンド、テストフレームワーク、テストファイルの命名・配置パターン | aidlc-implement-task、aidlc-write-test、aidlc-verify |
| Quality | quality.md | lint/format/typecheck の実行コマンド、自動修正コマンド、ビルドコマンド | aidlc-dev、aidlc-deploy、aidlc-verify |
| Conventions | conventions.md | ファイル命名規約、DDD レイヤーのディレクトリマッピング、実装パターン | engineer、aidlc-review、aidlc-plan-task |

### 責務の分離

| 情報の種類 | 置き場所 | 例 |
|-----------|---------|---|
| 概念定義 | `rules/` | 「Entity は一意な識別子を持ち、ビジネスロジックをメソッドで持つ」 |
| 具体的実装パターン | `profile/conventions.md` | 「VO は private constructor + static create/from で実装する」 |
| ディレクトリ構造 | `profile/structure.md` | 「Entity は apps/api/src/domain/models/ に配置する」 |
| テストコマンド | `profile/testing.md` | 「API テスト: cd apps/api && bun test --coverage」 |

### hooks との関係

`settings.json` の hooks はシェルコマンドなので markdown を動的に読めない。`/aidlc-init` 実行時に検出結果に基づいて hooks を更新する。

| Hook | イベント | 内容 |
|------|---------|------|
| WorktreeRemove | worktree マージ後 | テスト + typecheck |
| SubagentStop(engineer) | engineer 完了後 | lint + typecheck |

## 手順

1. プロジェクトルートをスキャンし、技術スタックを検出する
   - パッケージマネージャ: `package.json`（npm/bun/yarn）, `Cargo.toml`（Rust）, `go.mod`（Go）, `pyproject.toml`/`requirements.txt`（Python）
   - フレームワーク: `package.json` の dependencies から検出
   - 言語: tsconfig.json, Cargo.toml, go.mod 等から推定
2. ディレクトリ構造をスキャンし、パッケージ構成を推定する
   - モノレポ: workspaces 設定（package.json, pnpm-workspace.yaml）
   - 各パッケージのパスと type（BE/FE/shared）を推定
3. テスト設定を検出する
   - jest.config, vitest.config, bun test, pytest.ini, cargo test 等
   - テストファイルの命名パターン（*.test.ts, *_test.go, test_*.py 等）
4. lint・品質ツール設定を検出する
   - biome.json, .eslintrc, prettier, ruff.toml, golangci-lint, clippy 等
   - 型チェック: tsc, mypy, pyright 等
   - ビルドコマンド: package.json scripts, Makefile 等
5. 5ファイルのドラフトを生成する
   - `.aidlc-workflow/profile/stack.md` — 言語、ランタイム、フレームワーク
   - `.aidlc-workflow/profile/structure.md` — パッケージ構成、ディレクトリ配置
   - `.aidlc-workflow/profile/testing.md` — テスト実行コマンド、テストパターン
   - `.aidlc-workflow/profile/quality.md` — lint/format/typecheck/build コマンド
   - `.aidlc-workflow/profile/conventions.md` — 命名規約、アーキテクチャパターン
6. ユーザーに生成内容を提示し、確認・修正を促す
7. settings.json の hooks セクションを検出結果に基づき更新する
   - テストコマンド、lint コマンドをプロジェクト固有のものに設定

## 出力形式

```markdown
## project-profile 生成結果

### 検出結果
- 言語: [検出結果]
- ランタイム: [検出結果]
- パッケージマネージャ: [検出結果]
- フレームワーク: [検出結果]
- テストツール: [検出結果]
- lint/format: [検出結果]

### 生成ファイル
1. .aidlc-workflow/profile/stack.md — [概要]
2. .aidlc-workflow/profile/structure.md — [概要]
3. .aidlc-workflow/profile/testing.md — [概要]
4. .aidlc-workflow/profile/quality.md — [概要]
5. .aidlc-workflow/profile/conventions.md — [概要]

確認して修正があればお知らせください。
```

## 注意

- 既存の `.aidlc-workflow/profile/` がある場合は上書き確認を行う
- 検出できなかった項目は `[要記入]` プレースホルダーを置く
- conventions.md は検出した技術スタックに合った実装パターンを提案する
- Brownfield の場合、conventions.md には実際のソースコードから読み取った以下のパターンを必ず記述する:
  - VO: create/from メソッドのバリデーション方針（ID 系 vs enum 系）
  - Entity: reconstruct パターン（VO.from 経由）
  - Route: HTTP ステータスコード規約、toDto パターン、フィルタリング禁止ルール
  - FE: テスト用属性（data-testid）、hooks パターン
