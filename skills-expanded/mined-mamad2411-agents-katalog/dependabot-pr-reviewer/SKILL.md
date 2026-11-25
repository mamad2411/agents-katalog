---
name: dependabot-pr-reviewer
description: dependabot が作成したブランチ/PR のパッケージ更新内容を調査し、changelog・既存実装との差分から懸念点をパッケージ単位の表にまとめ、取り込み時のチェック項目も整理するスキル。Node.js / Ruby / Go / Python / Rust 等エコシステム横断対応で、リポジトリのマニフェストファイルから自動判定する。TRIGGER when ブランチ名が `dependabot/` で始まるブランチ・PR に対して「調査して」「レビューして」「確認して」「取り込んで大丈夫？」等の依頼があった時、または依存関係更新 PR のレビュー依頼時。DO NOT TRIGGER when 依存パッケージとは無関係なコード変更ブランチや、単なるパッケージマネージャの使い方質問。
argument-hint: "[branch_name_or_pr_number] [output_file]"
---

# Dependabot PR Reviewer

## 概要

dependabot が作成したブランチ（または PR）のパッケージ更新差分を調査し、以下を成果物として生成する:

1. **更新パッケージ一覧** — バージョン差分（major / minor / patch）
2. **パッケージ別の懸念点表** — changelog や breaking changes、既存実装との衝突可能性
3. **取り込み時チェックリスト** — lint / type-check / test / 動作確認すべきフロー

懸念点が見つからなかったパッケージについては「特になし」と明記し、無理にリスクを捏造しない。

**エコシステム横断対応**: Node.js / Ruby / Go / Python / Rust など、リポジトリ内のマニフェストファイルを検出して自動判定する。複数エコシステム混在のリポジトリ（例: Rails + フロント）にも対応。

## 使用タイミング

### TRIGGER when（自動発動すべき条件）

以下のいずれかに該当する場合、必ずこのスキルを発動する:

1. **ブランチ名が `dependabot/` で始まる** ブランチ・PR を対象に、ユーザが「調査して」「レビューして」「確認して」「見て」「取り込んで大丈夫？」「マージしていい？」等の依頼をした
2. PR タイトル / author が `dependabot[bot]` で、その PR に対するレビュー依頼があった
3. 「依存関係更新 PR をレビューして」「npm bump の影響を調べて」「gem update の確認」など、依存パッケージ更新レビューを明示的に求められた

判定の優先度: **ブランチ名のプレフィックスが `dependabot/` であることが最も強いシグナル**。このプレフィックスを検出したら、ユーザが「dependabot」という単語を使っていなくてもスキルを起動する。

### DO NOT TRIGGER when（発動すべきでない条件）

- ブランチ名が `dependabot/` で始まらない、かつ依存関係更新の文脈もない通常のコードレビュー依頼
- 単なる `pnpm install` / `bundle install` 等の使い方質問
- パッケージのドキュメント検索のみの依頼

### 具体例

- ✅ 「`dependabot/npm_and_yarn/next-15.0.0` ブランチ調査して」 → 発動
- ✅ 「`dependabot/bundler/rails-7.2.0` 取り込んで大丈夫？」 → 発動
- ✅ 「いま dependabot のブランチに居るからレビューして」 → 発動
- ✅ 「PR #300（dependabot 作成）取り込んで大丈夫？」 → 発動
- ❌ 「`feat/add-login` ブランチをレビューして」 → 発動しない
- ❌ 「next の使い方教えて」 → 発動しない

## 入力パラメータ

| パラメータ | 説明 | デフォルト |
|-----------|------|-----------|
| `$0` | 対象ブランチ名 または PR 番号（`#258` 形式可） | 現在チェックアウト中のブランチ |
| `$1` | 出力ファイルパス（明示指定された場合は懸念有無に関わらずファイル出力） | なし（後述の出力モード判定に従う） |

## 出力モード

懸念の有無で出力先を切り替える:

| 状況 | 出力先 |
|------|-------|
| 🔴 High / 🟡 Medium の懸念が **1 件以上** ある | ファイル出力 (`./tmp/dependabot-review-{branch}.md`) + stdout に要約 |
| 🟢 Low / ⚪ None のみ（懸念なし扱い） | **stdout のみ**。ファイルは作らない |
| `$1` で出力ファイルパスが明示指定された | 懸念有無に関わらずファイル出力 |

理由: 懸念がない時にファイルを作っても tmp が汚れるだけぺこ。レビュー結果がチャット内で完結すれば十分。逆に懸念があるときは後から見返したり関係者に共有したりするからファイルが欲しい。

## エコシステム判定マトリクス

リポジトリ直下（または monorepo の各サブディレクトリ）に存在するファイルから判定する:

| エコシステム | マニフェスト | ロックファイル | パッケージマネージャ | 主なレジストリ |
|-------------|------------|---------------|-------------------|--------------|
| **Node.js** | `package.json` | `pnpm-lock.yaml` / `yarn.lock` / `package-lock.json` | pnpm / yarn / npm | npmjs.com |
| **Ruby** | `Gemfile` / `*.gemspec` | `Gemfile.lock` | bundler | rubygems.org |
| **Go** | `go.mod` | `go.sum` | go modules | pkg.go.dev |
| **Python** | `pyproject.toml` / `requirements*.txt` / `Pipfile` | `poetry.lock` / `uv.lock` / `Pipfile.lock` | poetry / uv / pip / pipenv | pypi.org |
| **Rust** | `Cargo.toml` | `Cargo.lock` | cargo | crates.io |
| **Java/Kotlin** | `pom.xml` / `build.gradle*` | - | maven / gradle | mvnrepository.com |
| **PHP** | `composer.json` | `composer.lock` | composer | packagist.org |
| **GitHub Actions** | `.github/workflows/*.yml` | - | - | github.com/marketplace |

dependabot のブランチ名にもエコシステムのヒントが含まれる:

| ブランチプレフィックス | エコシステム |
|--------------------|------------|
| `dependabot/npm_and_yarn/` | Node.js |
| `dependabot/bundler/` | Ruby |
| `dependabot/go_modules/` | Go |
| `dependabot/pip/` | Python |
| `dependabot/cargo/` | Rust |
| `dependabot/maven/` / `dependabot/gradle/` | Java/Kotlin |
| `dependabot/composer/` | PHP |
| `dependabot/github_actions/` | GitHub Actions |

複数エコシステムが混在する場合は、すべてのマニフェストを並行して扱う。

## 前提条件

- `git` が使えること
- `gh` CLI が認証済みで PR 情報が取れること（PR 番号指定時）
- インターネットアクセス（changelog / release notes を取得するため WebFetch を使う）

## 実行手順

### Step 1: 対象ブランチの特定とチェックアウト状態の確認

```bash
git rev-parse --abbrev-ref HEAD
git status --short
```

PR 番号で指定された場合は `gh pr view <番号> --json headRefName,title,body` でブランチ名を取得し、必要に応じて `gh pr checkout <番号>` を提案する（ユーザに確認してから実行）。

dependabot のブランチかどうかは以下で判定:
- ブランチ名が `dependabot/` で始まる
- 直近コミットの author が `dependabot[bot]`
- PR の author が `dependabot[bot]`

dependabot 以外のブランチだった場合は、ユーザに「dependabot のブランチではないぺこが、このまま依存差分レビューを進めるぺこか？」と確認する。

### Step 2: エコシステムの自動判定

ブランチ名のプレフィックスと、リポジトリ内のマニフェストファイル存在を Glob で確認して、対象エコシステムを決定する:

1. ブランチ名から推定（例: `dependabot/bundler/...` → Ruby）
2. リポジトリ直下と各サブディレクトリで該当マニフェストファイルを検索
3. 複数エコシステム混在ならすべてを対象にする
4. 該当ファイルが見つからなければユーザに「このリポジトリのエコシステムが判定できなかったぺこ。手動で指定するぺこ？」と確認

### Step 3: ベースブランチとの差分取得

```bash
# ベースブランチを推定（develop または main）
git remote show origin | grep "HEAD branch" || echo "develop"
```

判定したエコシステムに応じて、対象ファイルの差分を取得する:

| エコシステム | diff 対象 |
|-------------|----------|
| Node.js | `**/package.json` `**/pnpm-lock.yaml` `**/yarn.lock` `**/package-lock.json` |
| Ruby | `**/Gemfile` `**/Gemfile.lock` `**/*.gemspec` |
| Go | `**/go.mod` `**/go.sum` |
| Python | `**/pyproject.toml` `**/requirements*.txt` `**/Pipfile*` `**/poetry.lock` `**/uv.lock` |
| Rust | `**/Cargo.toml` `**/Cargo.lock` |
| Java/Kotlin | `**/pom.xml` `**/build.gradle*` |
| PHP | `**/composer.json` `**/composer.lock` |
| GitHub Actions | `.github/workflows/*.yml` `.github/workflows/*.yaml` |

monorepo の場合は変更されたマニフェストがどのアプリ/パッケージに属するかも記録する。

### Step 4: 更新パッケージの抽出

エコシステム別のパース戦略:

- **Node.js**: `package.json` の diff から `"name": "old" → "new"` を抽出。`dependencies` / `devDependencies` / `peerDependencies` を区別。lock ファイルから transitive deps も拾う
- **Ruby**: `Gemfile.lock` の `GEM` セクションを diff し、gem 名とバージョンを抽出。`Gemfile` の直接指定との対応関係も取る
- **Go**: `go.mod` の `require` ブロック diff。indirect は transitive 扱い
- **Python**: `pyproject.toml` / `requirements.txt` / lock ファイルから抽出
- **Rust**: `Cargo.toml` の `[dependencies]` と `Cargo.lock` の `[[package]]` から抽出
- **GitHub Actions**: workflow YAML の `uses: owner/action@vX` の diff

各パッケージについて以下を分類:
- **major bump**: 互換性に影響しうる更新
- **minor bump**: 機能追加
- **patch bump**: バグ修正
- **transitive only**: 直接依存ではない更新

セマンティックバージョニング非準拠のエコシステム（Java の date-based バージョン等）は、リリース時期と changelog で判断する。

### Step 5: changelog / release notes の取得

各更新パッケージについて、以下の優先順位で情報を取得:

1. **PR 本文** — dependabot は PR 本文に release notes / commits を貼ってくれる。`gh pr view <番号> --json body` で取得して最優先で参照
2. **GitHub Releases** — `https://github.com/<org>/<repo>/releases` を WebFetch
3. **CHANGELOG.md** — リポジトリ直下の CHANGELOG を WebFetch
4. **エコシステム別レジストリ**:
   - Node.js: `https://www.npmjs.com/package/<name>`
   - Ruby: `https://rubygems.org/gems/<name>` / `https://rubygems.org/api/v1/versions/<name>.json`
   - Go: `https://pkg.go.dev/<module>`
   - Python: `https://pypi.org/project/<name>/`
   - Rust: `https://crates.io/crates/<name>`
   - PHP: `https://packagist.org/packages/<vendor>/<name>`

取得時の注意:
- 旧→新のバージョン範囲に含まれるリリースをすべて拾う（中間バージョンの breaking change を見落とさない）
- "BREAKING CHANGE" / "Breaking Changes" / "Migration" / "Upgrade Guide" セクションは必ず読む
- patch でも security fix の場合があるので "Security" / "CVE" 関連も確認

### Step 6: 既存実装との照合

更新されたパッケージが本リポジトリ内でどう使われているかを Grep で確認:

| エコシステム | 検索パターン例 |
|-------------|--------------|
| Node.js | `from '<pkg>'` / `require\(['"]<pkg>` |
| Ruby | `require ['"]<gem>['"]` / `<ModuleName>` のクラス参照 |
| Go | `"<module>"` の import |
| Python | `import <pkg>` / `from <pkg> import` |
| Rust | `use <crate>::` / `extern crate <crate>` |

確認ポイント（エコシステム共通）:
- **API 変更**: 削除されたメソッド / 変更されたシグネチャを使っていないか
- **設定変更**: 設定ファイルのスキーマ変更に追従が必要か（biome.json / .rubocop.yml / pyproject.toml 等）
- **依存整合性**: 他パッケージ・他 gem との peer 関係
- **副作用**: グローバルな挙動変化（autoload / monkey patch / polyfill 等）

エコシステム特有の確認:
- **Node.js / TypeScript**: 型定義変更で `tsc` が落ちないか
- **Ruby / Rails**: deprecation warning、`ActiveSupport` の互換性、初期化順序、`config.load_defaults` の影響
- **Go**: `go vet` / `go build` / インターフェース実装漏れ
- **Python**: 型ヒント・`typing` モジュール変更、async API 変更
- **Rust**: edition 互換性、`unsafe` 周辺の変化

monorepo では各サブプロジェクトごとに使用箇所を整理する。

### Step 7: 懸念点の整理と取り込みチェック項目の決定

懸念点は以下のレベルで分類:

| レベル | 意味 |
|--------|------|
| 🔴 High | breaking change を含み、既存コードの修正が必要、もしくはランタイムで壊れる可能性が高い |
| 🟡 Medium | breaking はないが、設定変更や挙動変化があり動作確認が必要 |
| 🟢 Low | patch / 内部実装変更のみ。基本テストが通れば OK |
| ⚪ None | 特に懸念なし |

取り込み時チェック項目はエコシステムと更新内容に応じて以下から選定:

#### Node.js
- `pnpm install` (or `npm` / `yarn`) で lock file が破損していないか
- `pnpm lint` / `pnpm fix` / `pnpm type-check` / `pnpm test:run` の通過
- `pnpm build` の成功（ビルド系ツール更新時）
- `pnpm storybook` で UI 表示確認
- `pnpm dev` でローカル起動 → 影響しそうなフローを叩く

#### Ruby / Rails
- `bundle install` で lock 破損なし
- `bundle exec rubocop` / `bundle exec rspec` の通過
- (Rails) `bin/rails db:migrate:status` でマイグレーション影響なし
- (Rails) `bin/rails zeitwerk:check` でオートロード破損なし
- (Rails) `bin/rails server` 起動 → ログイン等の主要フロー確認
- (Sorbet/Steep 利用時) 型チェック実行

#### Go
- `go mod tidy` で差分が出ないか
- `go build ./...` / `go vet ./...` / `go test ./...` の通過
- (該当時) `golangci-lint run`

#### Python
- `pip install -e .` / `poetry install` / `uv sync` で破損なし
- `pytest` / `ruff check` / `mypy` の通過

#### Rust
- `cargo check` / `cargo clippy` / `cargo test` の通過

#### GitHub Actions
- workflow の YAML が valid（`actionlint` 等）
- 該当 workflow を branch で実際に走らせて確認

### Step 8: レポート生成と出力先の決定

「出力モード」セクションに従って出力先を決定する:

1. 全パッケージの懸念レベルを集計
2. 🔴 High または 🟡 Medium が **1 件以上** あれば → ファイル出力（`./tmp/dependabot-review-{branch}.md` または `$1`）+ stdout に要約サマリ表示
3. 🟢 / ⚪ のみなら → **stdout に直接全文出力。ファイルは作らない**
4. `$1` が明示指定されている場合は懸念有無に関わらずファイル出力

ファイル出力時は出力先パスを stdout に必ず明示する（例: `📄 レポートを ./tmp/dependabot-review-xxx.md に出力したぺこ`）。

stdout のみの場合は「⚪ 懸念なし。ファイルは出力しないぺこ」と明記する。

## 出力フォーマット

```markdown
# Dependabot PR レビュー: {ブランチ名 / PR タイトル}

- **PR**: {番号 or N/A} ({URL})
- **ブランチ**: `{branch_name}`
- **ベースブランチ**: `{base}`
- **エコシステム**: {Node.js / Ruby / Go / ...}
- **レビュー日**: {YYYY-MM-DD}

## サマリ

| 項目 | 内容 |
|------|------|
| 直接依存の更新数 | X 件 |
| 推移的依存の更新数 | Y 件 |
| 🔴 High 懸念 | A 件 |
| 🟡 Medium 懸念 | B 件 |
| 🟢 Low 懸念 | C 件 |
| ⚪ 懸念なし | D 件 |
| 総合判定 | ✅ そのままマージ可 / ⚠️ 動作確認後マージ / ❌ 修正必要 |

## 更新パッケージ別 懸念点

| パッケージ | 種別 | 旧 → 新 | bump | 影響範囲 | レベル | 懸念点 / 備考 |
|-----------|------|--------|------|---------|-------|-------------|
| `<pkg-name>` | direct | x.y.z → x.y.z | major/minor/patch | <path> | 🔴/🟡/🟢/⚪ | ... |
| ... | | | | | | |

### 詳細

#### 🔴 `<pkg-name>` x.y.z → x.y.z

- **breaking change**:
  - ...
- **本リポジトリでの使用箇所**:
  - `path/to/file.ext:line`
- **対応方針**: ...
- **参考**: {release notes URL}

(懸念ありのパッケージのみ詳細を書く。⚪ None のパッケージは表で十分)

## 取り込み時チェックリスト

### 必須（自動チェック）

- [ ] 依存インストールが成功し、lock file が破損していない
- [ ] lint パス
- [ ] 型チェックパス（該当時）
- [ ] テストパス
- [ ] CI が green

### 動作確認（手動）

更新内容に応じて選定:

- [ ] {具体的な動作確認シナリオをここに}

### 取り込み後

- [ ] マージ後の preview / staging で smoke test
- [ ] (該当時) 関係者へ周知（major bump や挙動変化があった場合）

## 備考 / 引き継ぎメモ

- {dependabot PR 本文に書かれていた重要情報}
- {次の dependabot PR とのコンフリクトリスク}
- {手動で追加対応が必要な事項}
```

## ガイドライン

### やること / やらないこと

**やる**:
- 旧→新の **すべての中間リリース** の breaking change を確認する
- monorepo / マルチエコシステムの場合、サブプロジェクトごとに影響範囲を切り分ける
- 懸念がないものは正直に「⚪ None」と書く
- パッケージの使用箇所は file_path:line_number 形式で示す

**やらない**:
- 推測で breaking change を捏造しない（必ず changelog / release notes を根拠にする）
- WebFetch が失敗した場合は「changelog 取得失敗」と明記し、代替手段を提案する
- ユーザに無断でブランチをチェックアウトしたり、依存をインストールしたりしない（提案だけする）

### bump レベルの目安

| bump | デフォルト判定 | 例外 |
|------|--------------|------|
| major | 🟡 以上から検討開始 | breaking なし宣言の major（`v1.0.0` 初版等）は 🟢 |
| minor | 🟢 が基本 | 設定スキーマ変更や lint ルール追加で既存コードに影響する場合は 🟡 |
| patch | ⚪ が基本 | security fix の場合は内容を必ず確認 |
| transitive | ⚪ が基本 | lock file のみで直接マニフェストは変わらない |

### lint / formatter / build ツールの特殊扱い

以下のパッケージは patch でも挙動が変わって既存コードがエラー化することがあるため、minor 以上でも一度 lint / 型チェックを必ず流す。

#### Node.js
- `@biomejs/biome`
- `eslint`, `eslint-config-*`, `eslint-plugin-*`
- `stylelint`, `stylelint-config-*`
- `typescript`
- `next`, `vite`, `vitest`
- `storybook`, `@storybook/*`
- `tailwindcss`, `postcss`

#### Ruby
- `rubocop`, `rubocop-*`
- `standard`
- `rails`（特に `config.load_defaults` の対象バージョン）
- `sorbet`, `sorbet-runtime`
- `rspec-rails`

#### Go
- `golangci-lint`（関連 linters 全部）
- `go` 本体（toolchain ディレクティブ）

#### Python
- `ruff`, `black`, `mypy`, `pyright`
- `django`, `fastapi`

#### Rust
- `clippy`
- `rustc`（toolchain）

### メジャーフレームワークの major bump

以下は原則 🔴 High からスタートし、影響範囲を見て下げる:

- **React major**: hooks / concurrent / Strict Mode 差分
- **Next.js major**: app router / proxy(middleware) API、`next.config`、`use client`
- **Next.js minor/patch**: Turbopack の安定性改善が含まれていないか changelog を確認する。取り込み後に `next dev`（Turbopack）で CPU 異常消費が発生した場合は `rm -rf node_modules .next && pnpm install` を試す（node_modules の不整合で暴走する事例あり）
- **TypeScript major**: 型推論厳格化、ライブラリ型定義の更新影響
- **Rails major**: `config.load_defaults`、deprecation 一掃、Zeitwerk、ActiveRecord の挙動変化
- **Django major**: ORM 挙動、async 対応、deprecation
- **Go major (1.x)**: GC / runtime / std lib の変化
- **Python メジャー**: 構文・stdlib 削除

## 使用例

```bash
# 現在チェックアウト中の dependabot ブランチをレビュー
/dependabot-pr-reviewer

# PR 番号を指定してレビュー
/dependabot-pr-reviewer "#258"

# ブランチ名と出力先を指定（Node.js）
/dependabot-pr-reviewer dependabot/npm_and_yarn/next-15.0.0 docs/review/next-15.md

# Ruby gem 更新のレビュー
/dependabot-pr-reviewer dependabot/bundler/rails-7.2.0
```
