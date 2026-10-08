---
description: プロジェクト共通の技術スタック、ディレクトリ構造、開発プロセス、ワークフロー連携
alwaysApply: true
---

# プロジェクト共通指示書

## 技術スタック (想定)
- 言語: Go
- アーキテクチャ: Modular/Layered Architecture

## ディレクトリ構造と情報源
- **仕様・設計**: `prompts/phases/` 配下が「正」の情報源です。
    - `000-xxx`: フェーズ名称
        - `branches/`: ブランチ別のアイデアと計画
            - `main/`: `main`ブランチ (現在の作業ブランチ名を入れること)
                - `ideas/`: 主要なアイデアメモと仕様書
                    - `000-yyy.md`: アイディアと要件を記したマークダウンファイル
                    - `001-zzz.md`: 同上
                - `plans/`: 実装計画書

## 開発プロセス

- **仕様ファースト**
    - 実装の前に `prompts/phases/...` 以下の `branches/` > 作業ブランチ名 > `ideas/` フォルダに仕様を作成・更新してください。仕様書のファイル名は、`000-` から始まる3桁の連番の数字で管理してください。

## ワークフロー間の流れ

`.cursor/skills/` 配下のスキルは、以下の順序で連携して動作します:

### 1. 仕様書作成フェーズ
**スキル**: `create-specification` (`.cursor/skills/create-specification/`)

1. **人間**: 実装のアイディアを考える
2. **AI**: `create-specification` スキルに従い仕様のマークダウンファイルを生成
   - 出力先: `prompts/phases/000-xxx/branches/[ブランチ名]/ideas/XXX-Name.md`
   - 内容: 背景、要件、実装計画の概要
3. **人間**: 仕様書をレビュー
   - 修正が必要な場合は、AIに指示して修正させる
   - 問題なければ、**明示的に次のフェーズへ進むよう指示する**（勝手に進まないこと）

### 2. 実装計画作成フェーズ
**スキル**: `create-implementation-plan` (`.cursor/skills/create-implementation-plan/`)

1. **人間**: 仕様マークダウンファイルを指定
2. **AI**: `create-implementation-plan` スキルに従い詳細な実装計画を作成
   - 入力: `prompts/phases/000-xxx/branches/[ブランチ名]/ideas/XXX-Name.md`
   - 出力: `prompts/phases/000-xxx/branches/[ブランチ名]/plans/YYY-Name.md`
   - 内容: 統合テスト計画、単体テスト計画、実装手順、検証計画
   - 大きな仕様の場合: 複数の実装計画ファイルに分割（Part1, Part2, ...）
3. **人間**: 実装計画をレビュー
   - 修正が必要な場合は、AIに指示して修正させる
   - 問題なければ、**明示的に次のフェーズへ進むよう指示する**（勝手に進まないこと）

### 3. 実装実行フェーズ
**スキル**: `execute-implementation-plan` (`.cursor/skills/execute-implementation-plan/`)

1. **人間**: 実装計画ファイルを指定
2. **AI**: `execute-implementation-plan` スキルに従って実装を実行
   - 入力: `prompts/phases/000-xxx/branches/[ブランチ名]/plans/YYY-Name.md`
   - プロセス:
     - コーディングルール (`prompts/rules/coding-rules.md`) を遵守してコード実装
     - テストルール (`prompts/rules/testing-rules.md`) を遵守してテスト作成
     - 実装計画のチェックボックス `[ ]` → `[x]` で進捗管理
     - 進行中項目は `[/]` でマーク

### 4. ビルド・検証フェーズ
**スキル**: `build-pipeline` (`.cursor/skills/build-pipeline/`)

実装実行フェーズ内で自動的に使用されます:

1. **AI**: `scripts/process/build.sh` を実行
   - 全体ビルドと単体テストを実行
   - **Linux**（ワークスペースの OS が Linux）および **Cursor / VS Code の Remote-SSH で接続先が Linux** の場合は、**必ず `--skip-etc` を付けて** `./scripts/process/build.sh --skip-etc` とすること（`etc` 配下の `mcp-command-runner` / `image-inspector` 等が当該環境で失敗しやすいため）
   - 失敗時は即座に修正して再実行
2. **AI**: `scripts/process/integration_test.sh` を実行
   - 統合テストを実行
   - **Linux** および **Remote-SSH の接続先が Linux** のときは **headless 前提**とする: **`--headed` と `--ui` を付けない**（Playwright の headless 既定のまま）。`integration_test.sh` は **`xvfb-run -a` で必ずラップ**して実行する（`./scripts/process/integration_test.sh` を直接叩かない。`--resume` や `--specify` を付けるときも同様）。根拠は `features/frontend/scripts/integration_test.sh` 冒頭コメント。**`xvfb-run` が無いホストでは先に Xvfb 系パッケージを入れてから実行**する。
   - 失敗時は修正して該当テストのみ再実行 (`--specify` オプション使用)
3. **AI**: 必要に応じて全テストを再実行してリグレッション確認

レビュー待ちでフェーズを止める場合は **スキル** `review-point` (`.cursor/skills/review-point/`) を参照してください。

### 調査スキル（開発フローとは独立）
**スキル**: `investigate` (`.cursor/skills/investigate/`)

開発フロー（仕様 → 計画 → 実装）とは独立した、**読み取り専用**の調査スキルです。

1. **人間**: 調査内容を依頼（バグ調査、設計理解、依存関係の把握など）
2. **AI**: `investigate` スキルに従って調査を実施
   - コードの閲覧・検索、ログ分析、Gitの履歴追跡など
   - 必要に応じて既存コマンドの実行による現状把握
   - **コードの変更は一切行わない**
3. **AI**: 調査結果をレポートとしてまとめて報告
4. **人間**: レポートを確認し、必要に応じて追加調査を依頼
   - 修正が必要な場合は、別途 `create-specification` から開発フローを開始

### ワークフロー図

```
=== 開発フロー ===

[人間: アイディア]
       ↓
[AI: create-specification] → 仕様書生成
       ↓
[人間: レビュー・修正・進行指示]
       ↓
[AI: create-implementation-plan] → 実装計画生成
       ↓
[人間: レビュー・修正・進行指示]
       ↓
[AI: execute-implementation-plan]
       ├→ コーディング
       ├→ テスト作成
       └→ [AI: build-pipeline]
              ├→ scripts/process/build.sh (全体ビルド・単体テスト)
              └→ scripts/process/integration_test.sh (統合テスト)

=== 調査フロー（独立・読み取り専用）===

[人間: 調査依頼]
       ↓
[AI: investigate] → コード解析・ログ分析・コマンド実行
       ↓
[AI: レポート作成] → ユーザーへ報告
       ↓
[人間: レポート確認・追加調査依頼]
       └→ 修正が必要な場合は開発フローへ
```

### 重要なポイント

- **人間のレビューポイント**: 仕様書と実装計画の2箇所
- **自動実行部分**: 実装実行とビルド・検証パイプライン
- **進捗管理**: 実装計画のチェックボックスで進捗を可視化
- **テスト順序**: 統合テスト → 単体テスト → その他のテスト
- **スクリプト配置**: `scripts/` ディレクトリに各種ビルド・テストスクリプトを配置
- **フェーズ移行の禁止事項**: 現在のワークフローが完了しても、人間からの明示的な指示があるまでは、勝手に次のフェーズ（仕様 → 実装計画 → 実装実行）を開始してはいけません。

## シェル環境の指定

コマンドラインでスクリプトやコマンドを実行する際は、**bash** の使用を推奨します。

### Windows環境での注意事項

> [!IMPORTANT]
> Windows環境では、PowerShellではなく必ず **Git Bash** などのbash互換環境を使用してください。

- **推奨環境**: Git Bash, WSL (Windows Subsystem for Linux), Cygwin など
- **理由**: プロジェクトのスクリプト (`scripts/` 配下) はbashスクリプトとして記述されているため、PowerShellでは正しく動作しない可能性があります
- **確認方法**: ターミナルで `bash --version` を実行して、bashが利用可能か確認してください

### Mac / Linux環境

- 標準のbashシェルを使用してください
- **Linux**（ローカル Linux および **Remote-SSH のリモートが Linux**）: `scripts/process/build.sh` を叩くときは **`--skip-etc`** を付与すること（例: `./scripts/process/build.sh --skip-etc`）
- **Linux / Remote-SSH（Linux）**: `scripts/process/integration_test.sh` は **`--headed` / `--ui` を付けず**、かつ **`xvfb-run -a` で必ずラップ**して実行する（スクリプトを直接実行しない）
- **macOS**: 上記 `--skip-etc` は Linux / Remote-SSH（Linux）専用の補足であり、macOS では従来どおりプロジェクトの期待に合わせて実行すればよい

## Git 操作ルール

実装フェーズ（`execute-implementation-plan` や `build-pipeline`、`run-all-tests`）では、以下のルールに従って Git 操作を行ってください。

### コミットの方針

- **こまめにコミット**: コードの変更は、目的や意味のある単位で `git add` → `git commit` を実施してください。大きな変更を一度にまとめてコミットすることは避けてください。
- **コミット単位の目安**:
    - 1つの関数/メソッドの実装完了
    - 1つのテストファイルの作成・修正完了
    - 1つのバグ修正完了
    - リファクタリングの1ステップ完了
    - 設定ファイルの変更
- **コミットメッセージ**: 変更内容が分かる簡潔なメッセージを英語で記述してください。
    - 例: `feat: add bearer auth middleware`, `test: add unit tests for token validation`, `fix: handle nil pointer in auth handler`
- **コミットのタイミング**: 実装計画の各ステップを完了するごとに、対応する変更をコミットしてください。

### プッシュの方針

- **ビルド・テスト完了後にプッシュ**: `build.sh` および必要な統合テストが全て成功した時点で `git push` を実施してください。
- テストが失敗している状態ではプッシュしないでください。
- 修正ループ（Fix Loop）中のコミットは、テストが全て通過してからまとめてプッシュします。

### 実行例

```bash
# 実装の各ステップ完了時
git add <変更ファイル>
git commit -m "feat: implement rate limiter struct"

# ビルド・テスト全成功後
git push
```

## ファイル管理規則
- **中間生成ファイル**: タスク進行中に生成される中間ファイル（ビルドエラーログ、デバッグ出力、一時的なドキュメントなど）は、必ず `tmp/` ディレクトリ以下に作成してください。
    - 例: `build_error.txt`, `doc_delta.txt`, `doc_resp.txt` などは `tmp/build_error.txt`, `tmp/doc_delta.txt`, `tmp/doc_resp.txt` として作成
    - ログファイル、PIDファイルなども同様に `tmp/` 以下に配置すること（例: `tmp/vscode_launch.log`, `tmp/.vscode_cdp.pid`）。
    - これらのファイルはプロセスでは必要ですが、タスク完了後はゴミとなり、誤ってコミットされるリスクがあります。
    - `tmp/` ディレクトリは `.gitignore` で除外されているため、コミットされません。
- **ファイルパスの表示**: できるだけ「file://プロジェクトルートからの相対パス」を表示するようにしてください。
