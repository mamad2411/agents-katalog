---
name: feature-workflow
description: Execute a complete feature development workflow from research to PR creation. Use when starting new feature development, implementing tasks, or when the user mentions "機能開発ワークフロー", "feature workflow", or "開発プロセス実行".
allowed-tools: Task, Bash, Read, Write, Edit, Glob, Grep, TodoWrite, AskUserQuestion
---

# Feature Development Workflow

## 概要

機能開発の完全なワークフローを実行します。
調査から計画、Issue作成、ブランチ作成、実装、PR作成まで一貫して管理します。

### 主な特徴

- **徹底的な調査**: Exploreエージェントによるコードベース探索
- **計画立案**: プランモードで実装計画を策定
- **GitHub連携**: Issue作成とPR作成を自動化
- **進捗管理**: TodoWriteで各ステップを追跡

## 使い方

以下のようなリクエストでこのSkillが発動します：

```
「機能開発ワークフローで〜を実装して」
「feature workflowで認証機能を追加して」
「開発プロセスを実行して〜」
"/feature-workflow ユーザープロフィール機能"
```

## ワークフロー

```
1. Research (徹底的な調査・探索)
   ↓
2. Planning (実装計画の策定)
   ↓
3. Issue Creation (GitHub Issueの作成)
   ↓
4. Branch Creation (作業ブランチの作成)
   ↓
5. Implementation (機能の実装)
   ↓
6. PR Creation (Pull Requestの作成)
```

## 各ステップの詳細

### Step 1: Research（調査・探索）

**目的**: 実装に必要な情報を徹底的に収集する

**実行内容**:
1. Exploreエージェントを使用してコードベースを調査
2. 既存の類似機能やパターンを特定
3. 依存関係と影響範囲を把握
4. 技術的な制約や考慮事項を整理

**使用するツール**:
- `Task(subagent_type=Explore)`: コードベース探索
- `Grep`, `Glob`: パターン検索
- `Read`: 重要ファイルの確認

**出力**: 調査結果のサマリー

---

### Step 2: Planning（計画立案）

**目的**: 実装計画を策定し、ユーザーの承認を得る

**実行内容**:
1. 調査結果を基に実装アプローチを設計
2. 変更が必要なファイルをリストアップ
3. 実装ステップを順序立てて整理
4. 潜在的なリスクや代替案を検討

**方法**:
- プランモード（EnterPlanMode）を使用
- または直接実装計画を提示

**確認ポイント**: ユーザーにプランの承認を求める

---

### Step 3: Issue Creation（Issue作成）

**目的**: GitHub Issueを作成して作業を記録する

**実行内容**:
1. 機能の概要をタイトルにまとめる
2. 実装内容と目的をbodyに記載
3. 適切なラベルを付与

**コマンド例**:
```bash
gh issue create --title "feat: [機能名]" --body "## 概要\n\n## 実装内容\n\n## 関連ファイル"
```

**出力**: Issue番号とURL

---

### Step 4: Branch Creation（ブランチ作成）

**目的**: 作業用のfeatureブランチを作成する

**実行内容**:
1. 最新のmainブランチから分岐
2. 命名規則に従ったブランチ名を使用

**命名規則**:
- `feature/[issue番号]-[機能名]`
- 例: `feature/123-user-profile`

**コマンド例**:
```bash
git checkout main && git pull origin main
git checkout -b feature/123-user-profile
```

---

### Step 5: Implementation（実装）

**目的**: 計画に従って機能を実装する

**実行内容**:
1. TodoWriteで実装タスクを管理
2. 各タスクを順番に実装
3. テストを作成（必要に応じて）
4. 適宜コミットを作成

**コミットメッセージ規則**:
```
<type>(<scope>): <subject>
```
- feat: 新機能
- fix: バグ修正
- refactor: リファクタリング
- docs: ドキュメント
- chore: メンテナンス

---

### Step 6: PR Creation（PR作成）

**目的**: Pull Requestを作成してレビューを依頼する

**実行内容**:
1. 変更をリモートにプッシュ
2. PRタイトルと本文を作成
3. 関連Issueをリンク

**コマンド例**:
```bash
git push -u origin feature/123-user-profile
gh pr create --title "feat: [機能名]" --body "## Summary\n\nCloses #123"
```

**出力**: PR番号とURL

---

## 人間確認ポイント

以下のタイミングで必ずユーザーの確認を得ます：

1. **プラン承認時** (Step 2後)
2. **Issue作成前** (Step 3前) - 必要に応じて
3. **実装完了後** (Step 5後) - コミット前の確認

## 前提条件

### 必要なツール

- **Git**: バージョン管理
- **GitHub CLI (`gh`)**: Issue/PR作成

### 認証

```bash
# GitHub CLIの認証確認
gh auth status
```

## 注意事項

- 調査フェーズを省略しない - 既存パターンを理解することが重要
- 計画なしに実装を始めない - 手戻りを防ぐ
- 小さなコミットを心がける - レビューしやすさのため
- Issueは必須ではない - プロジェクトの方針に従う
