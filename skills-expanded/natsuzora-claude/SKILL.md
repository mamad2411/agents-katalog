# CLAUDE.md
## プロジェクト概要

Natsuzoraは「表示専用」のミニテンプレート言語で、Rust・Rubyの2実装を持つモノレポ。静的HTML生成とRailsプレビュー共有テンプレートに使用される。

## ディレクトリ構成

```
natsuzora/
├── spec/           # 言語仕様（spec.md v4.0, bnf.md）
├── tests/          # 共有テストケース（*.json）
├── rust/           # Rust実装
├── ruby/           # Ruby実装
└── tree-sitter/    # Tree-sitter文法（シンタックスハイライト用）
```

## コマンド

### Rust

```bash
cd rust
cargo build          # ビルド
cargo test           # テスト実行
cargo build --release # リリースビルド
```

### Ruby

```bash
cd ruby
bundle install       # 依存関係インストール
bundle exec rspec    # テスト実行
bundle exec rubocop  # Lint
```

### Tree-sitter

```bash
cd tree-sitter
npm install          # 依存関係インストール
npx tree-sitter generate  # パーサー生成
npx tree-sitter parse <file.tmpl>  # パース確認
```

## アーキテクチャ

全実装が同じパイプライン構造を持つ：

```
render(source, data)
    ↓
Lexer → Token[] → Parser → AST::Template → Renderer → String
                              ↑
                    TemplateLoader (include時)
```

### 主要コンポーネント

| コンポーネント | 責務 |
|---------------|------|
| Lexer | 字句解析（TEXT ↔ タグ切替、コメント、空白制御） |
| Parser | 再帰下降構文解析、予約語検証 |
| AST | ノード定義（Template, Text, Variable, IfBlock, etc.） |
| Context | スコープスタック管理、名前解決、シャドーイング検出 |
| Renderer | AST評価、HTMLエスケープ適用 |
| TemplateLoader | パーシャル読込、循環検出、パストラバーサル防止 |

## 言語仕様の要点

詳細は `spec/spec.md` を参照。

### Truthiness（偽とみなす値）

`false`, `null`, `0`, `""`, `[]`, `{}`

### 文字列化

- 可: String, Integer, null
- エラー: Boolean, Array, Object

### 予約語

`if`, `unless`, `else`, `each`, `as`, `unsecure`, `true`, `false`, `null`, `include`

### 禁止プレフィックス

- `_` で始まる識別子
- `@` を含む識別子

### 制約

- シャドーイング禁止（include引数を除く）
- 未定義変数は即時エラー
- `each` は配列のみ、配列以外はエラー
- include循環検出でエラー
- パストラバーサル禁止

## 共有テストケース

`tests/` ディレクトリに全実装で使用するテストケースがある。新機能追加時は必ずここにテストを追加し、全実装でパスすることを確認する。

## 実装変更時の注意

1. 仕様変更は `spec/spec.md` を先に更新
2. `tests/` に対応するテストケースを追加
3. 全実装（Rust, Ruby）を更新し、テストがパスすることを確認
4. BNF（`spec/bnf.md`）も必要に応じて更新
