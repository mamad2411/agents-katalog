---
name: executing-ai-development-workflow
description: Execute a structured AI-driven development workflow with research, planning, implementation, optional multi-layer review (4 Sub-agents + /review + CodeRabbit CLI), priority-based fixes, and PR creation. Supports Light mode (fast, default) and Full mode (quality-focused with reviews). Use when implementing new features, performing large refactorings, starting feature development, or when the user mentions "AI development workflow", "AI開発ワークフロー", "feature workflow", "機能開発ワークフロー", "計画的に実装", "開発プロセス実行", "品質重視で実装", or "多層レビューで開発".
---

# Executing AI Development Workflow

## Contents

- 概要
- ワークフロー概要
- モード選択
- Step 1: Research
- Step 2: Planning
- Step 3: Issue & Branch
- Step 4: Implementation
- Step 5: Review (Full mode)
- Step 6: Fix (Full mode)
- Step 7: PR Creation
- Step 8: PR Response & Merge (Full mode)
- 優先度判定
- 人間確認ポイント
- 進捗チェックリスト
- 前提条件
- 関連ファイル

## 概要

調査から実装、レビュー、PR作成まで一貫したAI開発ワークフローを実行する。
2つのモード（Light/Full）で、軽量な機能追加から品質重視の大規模開発まで対応する。

## ワークフロー概要

```
1. Research (調査・探索)
   ↓
2. Planning (計画 + ドキュメント化)
   [人間確認: プラン承認]
   ↓
3. Issue & Branch (Issue作成 + ブランチ作成)
   ↓
4. Implementation (実装)
   ↓                          ┌─ Full mode only ─────────────┐
5. Review (多層レビュー)      │ 4 Sub-agents (並列)          │
   ↓                          │ /review コマンド              │
6. Fix (優先度ベース修正)     │ CodeRabbit CLI               │
   [人間確認: Medium修正判断] │                               │
   ↓                          └───────────────────────────────┘
7. PR Creation
   [人間確認: PR前最終確認 (Full mode)]
   ↓
8. PR Response & Merge (Full mode only)
```

**Light mode**: Step 1 → 2 → 3 → 4 → 7（高速・軽量）
**Full mode**: Step 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8（品質重視）

## モード選択

### デフォルト: Light mode

以下の**いずれか**に該当する場合は **Full mode** に切り替える:

| Full mode 条件 | 例 |
|---|---|
| セキュリティに関わる機能 | 認証、決済、権限管理、暗号化 |
| 10ファイル以上の変更が見込まれる | 大規模リファクタリング |
| ユーザーが明示的に品質重視を指定 | 「品質重視で」「多層レビューで」「Full modeで」 |
| 外部に公開されるAPI変更 | 破壊的変更を含むAPI |
| データベーススキーマの変更 | マイグレーション |

### Full mode トリガーワード

以下のキーワードがリクエストに含まれる場合、Full modeで実行:
- 「品質重視」「多層レビュー」「Full mode」「フルモード」
- 「セキュリティ」「認証」「決済」「payment」
- 「大規模」「リファクタリング」

## Step 1: Research（調査・探索）

**目的**: 実装に必要な情報を収集し、既存パターンを把握する

**実行内容**:
1. `Task(subagent_type=Explore)` でコードベースを調査
2. 既存の類似機能やパターンを特定
3. 依存関係と影響範囲を把握
4. 技術的な制約を整理

**調査すべきポイント**:
- 同様の機能がすでに存在しないか
- 使われている設計パターンとコーディング規約
- テスト戦略（既存テストのパターン）
- 変更が影響するファイルの範囲

**出力**: 調査結果サマリー（ユーザーに提示）

## Step 2: Planning（計画 + ドキュメント化）

**目的**: 実装計画を策定し、ユーザーの承認を得る

**実行内容**:
1. 調査結果を基に実装アプローチを設計
2. 変更対象ファイルをリストアップ
3. 実装ステップを順序立てて分解
4. 潜在的なリスクと代替案を検討
5. モード判定: Light / Full を決定して提示

**方法**:
- `EnterPlanMode` でプランモードに入る
- 計画をユーザーに提示

**ドキュメント化**:
- `assets/templates/plan.md` をベースに使用
- `_docs/plans/YYYY-MM-DD-[feature-name].md` として保存

**人間確認ポイント**: プラン内容と実行モードの承認を得る

## Step 3: Issue & Branch（Issue作成 + ブランチ作成）

**目的**: 作業を記録し、隔離された環境で開発する

### Issue作成

```bash
gh issue create --title "feat: [機能名]" --body "## 概要\n\n[計画のサマリー]\n\n## 実装内容\n\n[チェックリスト]"
```

- プロジェクトの方針によってはIssue作成をスキップしてよい
- ユーザーに確認の上、判断する

### ブランチ作成

**命名規則**: `feature/[issue番号]-[機能名]`

```bash
git checkout main && git pull origin main
git checkout -b feature/[issue番号]-[機能名]
```

例: `feature/123-user-authentication`

Issue番号がない場合: `feature/[機能名]`（例: `feature/user-authentication`）

## Step 4: Implementation（実装）

**目的**: 計画に従って機能を実装する

**実行内容**:
1. `TaskCreate` で実装タスクを分解・管理
2. 適切なSub-agentに委任（必要に応じて）
3. テストを作成
4. 適宜コミットを作成

**Sub-agent委任の例**:
- `frontend-developer`: フロントエンド機能
- `backend-architect`: バックエンドAPI設計
- `test-automator`: テスト追加
- `database-architect`: データベース設計

**コミットメッセージ規則**: プロジェクトの規約に従う。未定義なら Conventional Commits を使用。

## Step 5: Review（多層レビュー）- Full mode only

**目的**: 複数の視点からコード品質を検証する

詳細は [references/review-workflow.md](references/review-workflow.md) を参照。

**概要**:

### 5a. Sub-agent Reviews（並列実行）

以下の4つを `Task` ツールで並列実行:

| Sub-agent | 役割 |
|---|---|
| `code-reviewer` | コード品質全般 |
| `security-auditor` | セキュリティ脆弱性 |
| `architect-review` | アーキテクチャ設計 |
| `test-ai-tdd-expert` | テストカバレッジ |

### 5b. Claude Code /review

```
/review
```

### 5c. CodeRabbit CLI

```bash
coderabbit --prompt-only --type uncommitted
```

**結果の統合**:
- 全レビュー結果を収集
- `assets/config.json` の優先度ルールで分類（Critical/High/Medium/Low）
- `assets/templates/review.md` を使用してレポート作成
- `_docs/reviews/YYYY-MM-DD-[feature-name]-review.md` として保存

## Step 6: Fix（優先度ベース修正）- Full mode only

**目的**: レビュー指摘を優先度に基づいて対応する

### 自動修正（Critical / High）

**妥当な**指摘のみ自動修正する。以下は修正しない:
- 誤検知（false positive）
- プロジェクトの文脈で不適切な提案
- 過剰な抽象化の提案

修正方法:
- 単純な修正: `Edit` ツールで直接修正
- 複雑な修正: 適切なSub-agentに委任

### 人間確認（Medium）

Medium優先度の問題をリストアップし、各項目について確認:
- **修正する**: 妥当な指摘
- **保留**: 後で検討
- **却下**: 誤検知または不要

**人間確認ポイント**: Medium優先度問題の対応方針

### 記録のみ（Low）

ドキュメントに記録するが、修正は行わない。

## Step 7: PR Creation

**目的**: Pull Requestを作成する

**実行内容**:
1. 全ての変更をコミット
2. リモートにプッシュ
3. PRタイトルと本文を作成
4. 関連Issueをリンク

```bash
git push -u origin [ブランチ名]
gh pr create --title "[type]: [機能名]" --body "[PR本文]"
```

**PR本文に含める内容**:
- 変更の概要
- Full modeの場合: レビューサマリー（Critical/High修正済み、Medium対応状況）
- 関連Issue（`Closes #[番号]`）

**人間確認ポイント（Full mode）**: PR作成前の最終確認

## Step 8: PR Response & Merge - Full mode only

**目的**: PR上のレビューコメントに対応し、マージする

**実行内容**:
1. CodeRabbitとClaude Codeの自動レビューコメントを確認
2. **妥当な指摘のみ**修正を実装
3. 誤検知や不要な提案は丁寧に却下

**妥当性判断のポイント**:
- セキュリティ関連 → 基本的に妥当
- パフォーマンス → 実測データがあれば重視
- スタイル・命名 → プロジェクト規約と照合
- 複数ツールで同じ指摘 → 特に注目

最終的に人力レビューを適宜挟みながらマージを実行する。

## 優先度判定

`assets/config.json` で定義。レビュー指摘を以下の基準で分類する:

| 優先度 | 内容 | 対応 |
|---|---|---|
| Critical | セキュリティ脆弱性、重大バグ（SQLi, XSS, CSRF, データ漏洩） | 妥当なものを即時自動修正 |
| High | パフォーマンス問題、設計問題（メモリリーク, N+1, 競合状態） | 妥当なものを即時自動修正 |
| Medium | コード品質、ベストプラクティス（重複, 複雑度, エラー処理） | 人間が妥当性判断 |
| Low | スタイル、命名、ドキュメント（フォーマット, タイポ） | 記録のみ |

**重要**: AIレビューの指摘がすべて正しいとは限らない。Critical/Highでも誤検知はある。プロジェクトの文脈を理解した上で適切に取捨選択すること。

## 人間確認ポイント

### Light mode（1箇所）

1. **プラン承認** (Step 2後) - 実装計画とモード選択の確認

### Full mode（3箇所）

1. **プラン承認** (Step 2後) - 実装計画とモード選択の確認
2. **Medium修正判断** (Step 6) - Medium優先度問題の修正/保留/却下
3. **PR前最終確認** (Step 7前) - PR作成前の最終確認

## 進捗チェックリスト

### Light mode

```
Task Progress:
- [ ] Step 1: Research - コードベース調査完了
- [ ] Step 2: Planning - 計画策定・承認取得
- [ ] Step 3: Issue & Branch - Issue作成・ブランチ作成
- [ ] Step 4: Implementation - 実装完了
- [ ] Step 7: PR Creation - PR作成完了
```

### Full mode

```
Task Progress:
- [ ] Step 1: Research - コードベース調査完了
- [ ] Step 2: Planning - 計画策定・承認取得
- [ ] Step 3: Issue & Branch - Issue作成・ブランチ作成
- [ ] Step 4: Implementation - 実装完了
- [ ] Step 5: Review - 多層レビュー実施・結果統合
- [ ] Step 6: Fix - 優先度ベース修正完了・Medium確認済み
- [ ] Step 7: PR Creation - PR作成完了
- [ ] Step 8: PR Response & Merge - レビュー対応・マージ完了
```

## 前提条件

### 必要なツール

- **Git**: バージョン管理
- **GitHub CLI (`gh`)**: Issue/PR作成（`gh auth status` で認証確認）

### Full mode 追加要件

- **CodeRabbit CLI**: インストール済み & 認証済み

### プロジェクト準備

```bash
mkdir -p _docs/plans _docs/reviews
```

## 関連ファイル

- [references/review-workflow.md](references/review-workflow.md): Full mode多層レビュー詳細
- [references/examples.md](references/examples.md): 使用例
- [assets/config.json](assets/config.json): 優先度判定ルール・モード設定
- [assets/templates/plan.md](assets/templates/plan.md): 計画テンプレート
- [assets/templates/review.md](assets/templates/review.md): レビュー結果テンプレート
