# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
本ファイルがプロジェクトの唯一のルートレベル開発ガイドです（旧DEVELOPMENT.md・INSTRUCT.mdの内容を統合済み）。

## プロジェクト概要

.nksf (Massive Xのプリセットファイル)のパーサーライブラリおよびCLIツール

### 実装状況

- ✅ パーサーライブラリ完成（全4チャンク対応）
- ✅ CLIツール完成（JSON/JSONL出力、複数ファイル処理対応）
- ✅ 全720個のMassive X Libraryプリセット対応確認済み
- ✅ セキュリティ対策実装済み（DoS攻撃防御）
- ✅ テストライブラリ導入完了（rstest, cargo-nextest, insta, pretty_assertions, proptest, criterion）
- ✅ 全テスト成功（ユニット32個、統合テスト（エラーケース・プロパティベース）、fixtureテスト720個）

### アーキテクチャ

本プロジェクトはRustワークスペース構成で、2つの主要コンポーネントから成る:

- **lib** (`nksf-parser`): .nksfファイルを解析するパーサーライブラリ
  - 責任分離の観点から、JSON形式の出力は行わない
  - JSON最適化も行わない（純粋なパーサー機能のみ）
  - 全4チャンク対応: NISI（メタデータ）、NICA（パラメータ）、PLID（プラグインID）、PCHK（プラグインデータ）
- **cli** (`nksf-parser-cli`): コマンドラインインターフェース
  - libを使用して.nksfファイルを解析
  - 解析結果をJSON/JSONL形式で出力
  - 複数ファイルの一括処理対応
  - 出力先の柔軟な指定（`-o`, `-d`オプション）
  - JSONL形式での結合出力対応（`--jsonl`フラグ）
  - ユーザーフレンドリーなエラーメッセージ

## 開発環境のセットアップ

- 必要なツール: edition 2024 に対応するRust（1.85以上。推奨: 最新のstable版）、Cargo（同梱）
- セットアップ後の動作確認:

```bash
cargo check   # 依存関係の確認
cargo build   # ビルドの確認
```

## 開発コマンド

### ビルド
```bash
# ワークスペース全体のビルド
cargo build

# リリースビルド
cargo build --release

# 特定のクレートのビルド
cargo build -p nksf-parser       # ライブラリのみ
cargo build -p nksf-parser-cli   # CLIのみ
```

### テスト
```bash
# 全テスト実行（cargo-nextest使用、推奨）
cargo nextest run

# 従来のテストランナー使用
cargo test

# ライブラリのテストのみ
cargo nextest run -p nksf-parser

# 特定のテストファイル実行
cargo nextest run --test integration
cargo nextest run --test fixture_test  # 720プリセット

# プロパティベーステスト実行
cargo test --test integration test_parser_never_panics

# スナップショットテスト（更新モード）
INSTA_UPDATE=always cargo test --test fixture_test

# ベンチマーク実行
cargo bench
```

### フォーマット・Lint
```bash
# コードフォーマット
cargo fmt

# フォーマットチェック（CI用）
cargo fmt --check

# Clippy（リンター）
cargo clippy

# Clippy（警告をエラーとして扱う）
cargo clippy -- -D warnings
```

### 依存関係の管理
```bash
# 依存関係の追加（Cargo.tomlを直接編集してはいけない）
cd lib && cargo add <package-name>
cd cli && cargo add <package-name>

# 開発依存関係の追加
cargo add --dev <package-name>

# 現在の開発依存関係
# - rstest: パラメータ化テスト・フィクスチャ
# - cargo-nextest: 高速テストランナー
# - insta: スナップショットテスト
# - pretty_assertions: アサーション強化
# - proptest: プロパティベーステスト
# - criterion: ベンチマーク
```

## テスト構造

### テストの種類と配置

1. **ユニットテスト**: `lib/src` 以下の各 `.rs` ファイル内に記述
   - 各モジュールの関数・構造体の単体テスト
   - `#[cfg(test)]` モジュール内に配置
   - 実装ファイルと同じファイル内に記述

2. **統合テスト**: `lib/tests` 以下に配置
   - **integration.rs**: エラーケーステスト、性能テスト（`#[ignore]`付き）、プロパティベーステスト
   - **fixture_test.rs**: 720プリセットの統合テスト（rstest + insta）
     - 720個の`#[case]`を1つの関数で実行
   - **snapshots/**: instaスナップショットファイル（約380MB、Gitコミット済み）
     - `fixture_test__<Preset Name>.snap` × 720個: 各プリセットの期待値（YAML形式）
   - **massive_x_factory_library_tests/fixture/**: テストフィクスチャ
     - `*.nksf` × 720個: 全Massive X Libraryプリセット

3. **ベンチマーク**: `lib/benches` に配置
   - **parser_bench.rs**: パース処理のベンチマーク（criterion）

### テスト技術スタック

- **rstest**: パラメータ化テスト（`#[case]`で720プリセットを1関数で実行）
- **insta**: スナップショットテスト（YAMLで期待値を自動管理）
- **proptest**: プロパティベーステスト（任意入力でパニックしないことを検証）
- **criterion**: 統計的に正確なベンチマーク
- **pretty_assertions**: テスト失敗時のdiff表示
- **cargo-nextest**: 高速並列テスト実行

### スナップショットテストの管理

新しいプリセットファイルを追加した場合:

1. fixtureディレクトリに`.nksf`ファイルを配置
2. `lib/tests/fixture_test.rs`に`#[case("New Preset")]`を追加
3. スナップショットを生成・承認:
   ```bash
   INSTA_UPDATE=always cargo test --test fixture_test
   ```

**注意**: スナップショットファイルは全てGitにコミットされます（約380MB）。

## コーディング規約

### 基本原則

- **YAGNI**: 将来使うかもしれない機能は実装しない
- **DRY**: 重複コードは必ず関数化・モジュール化する
- **KISS**: 複雑な解決策より単純な解決策を優先

### Rustスタイル

- **フォーマット**: rustfmt に従う
- **命名規則**: Rustの標準命名規則に準拠（スネークケース: 関数・変数・モジュール、キャメルケース: 型・トレイト、スクリーミングスネークケース: 定数）
- **関数・構造体・ファイルの適切な分割**: 責任を明確に分離
- **ドキュメントコメント**: パブリックAPIには `///` で必ず記述（例を含めることを推奨）

### ファイル構成

- **末尾改行**: すべてのファイルの末尾に改行を入れる（trailing newline）
- **コメント**: コード内コメントは日本語で記述
- **インポート順序**: std → 外部クレート → 内部モジュール

## ワークフロー

### 作業開始時

1. 作業前に必ず公式ドキュメントを調査し、ライブラリの型定義を確認する
2. `pwd` でカレントディレクトリを確認する

### 作業終了時

1. テスト・フォーマット・Lintを実行して検証する:
   ```bash
   cargo nextest run && cargo fmt && cargo clippy -- -D warnings
   ```
2. 修正の根拠を明確にする（エビデンスを残す）
3. プロジェクトの状況に変化があった場合、本ファイル（CLAUDE.md）を更新する

### プルリクエスト

- 明確なタイトルと説明を記述する
- 変更内容の概要を説明する
- テスト結果を含める
- 関連するIssueがあれば参照する

## 重要な制約

### 責任分離

- ライブラリ (`lib`) では JSON 出力を実装しない
- CLI (`cli`) でのみ JSON 形式での出力を実装

### パース要件

- **完全なバイト解析**: .nksfファイルの全てのバイトを解析する
- **データの欠損禁止**: 1バイトも見逃さず、「不明なデータ」として捨てることを許可しない
- すべてのチャンクとフィールドを構造化して保持する
- 解析できないデータがある場合はエラーを返す（無視しない）

### テスト要件

- すべてのプリセットに対してテストを記述し、必ずパスさせる
- `lib/src` 以下の各 `.rs` ファイルにユニットテストを記述する
- `lib/tests` 以下に統合テストを記述する

### セキュリティ要件

- チャンクサイズ上限: 100MB
- zlib展開サイズ上限: 50MB
- MessagePack値数上限: 100,000個
- DoS攻撃・Zip Bomb攻撃への防御を実装

## 技術仕様（概要）

- **ベースフォーマット**: RIFF / フォーマット識別子 "NIKS"
- **エンコーディング**: MessagePack（PCHKチャンクのみzlib圧縮）
- **チャンク構造**: `[4 bytes] チャンクID` + `[4 bytes] チャンクサイズ（リトルエンディアン）` + `[n bytes] チャンクデータ`
- 詳細は [docs/specs/](./docs/specs/) を参照

## ドキュメント

- [docs/specs/](./docs/specs/): .nksf形式の仕様書
- [docs/adr/](./docs/adr/): アーキテクチャ決定記録（ADR）

## 参考資料

- [NKSF File Format (Community)](https://community.native-instruments.com/discussion/13469/)
- [Native Instruments Massive X](https://www.native-instruments.com/en/products/komplete/synths/massive-x/)
- [RIFF Format Specification](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format)
- [MessagePack Specification](https://msgpack.org/)
