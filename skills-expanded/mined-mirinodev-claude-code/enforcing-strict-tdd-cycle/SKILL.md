---
name: enforcing-strict-tdd-cycle
description: Orchestrate a comprehensive TDD workflow with multi-agent Red-Green-Refactor discipline, phase gates, and coverage validation. Use when user mentions "tdd-cycle", "TDDサイクル", "厳密なTDD", "TDDオーケストレーション", or needs strict test-first development with automated quality checks.
---

# Enforcing Strict TDD Cycle

マルチエージェントによる厳密なRed-Green-Refactorサイクルを実行するスキル。
各フェーズにゲートを設け、規律あるテスト駆動開発を保証する。

## Contents

- いつ使うか / guiding-tdd-development との違い
- ワークフロー概要
- Phase 1: テスト仕様設計
- Phase 2: RED - 失敗テスト作成
- Phase 3: GREEN - 最小実装
- Phase 4: REFACTOR - 品質改善
- Phase 5: 統合テスト
- Phase 6: 最終レビュー
- 開発モード
- 規律違反時のリカバリ

## いつ使うか

- 新機能の厳密なTDD開発
- カバレッジ閾値を担保した開発
- マルチエージェントによる品質チェックが必要な時

**guiding-tdd-development との違い**: `guiding-tdd-development` は手動で回すシンプルなTDDガイド。このスキルは各フェーズをサブエージェントで自動化し、ゲートチェックで規律を強制する包括版。

## ワークフロー概要

```
Phase 1: テスト仕様設計 (architect-review + test-automator)
    ↓ [仕様レビュー完了]
Phase 2: RED (test-automator → 失敗確認ゲート)
    ↓ [全テスト失敗を確認]
Phase 3: GREEN (実装 → 成功確認ゲート)
    ↓ [全テスト成功を確認]
Phase 4: REFACTOR (code-reviewer → テスト維持確認)
    ↓ [テスト緑のまま]
Phase 5: 統合テスト (RED→GREEN for integration)
    ↓ [統合テスト成功]
Phase 6: 最終レビュー (architect-review)
```

## Phase 1: テスト仕様設計

### 1-1. 要件分析

- Use Task tool with subagent_type="architect-review"
- Prompt: "Analyze requirements for: [対象機能]. Define acceptance criteria, identify edge cases, and create test scenarios. Output a comprehensive test specification."
- **Output**: テスト仕様、受入基準、エッジケースマトリクス

### 1-2. テストアーキテクチャ設計

- Use Task tool with subagent_type="test-automator"
- Prompt: "Design test architecture for: [対象機能] based on test specification. Define test structure, fixtures, mocks, and test data strategy."
- **Output**: テスト構造、フィクスチャ設計、モック戦略

## Phase 2: RED - 失敗テスト作成

### 2-1. ユニットテスト作成

- Use Task tool with subagent_type="test-automator"
- Prompt: "Write FAILING unit tests for: [対象機能]. Tests must fail initially. Include edge cases, error scenarios, and happy paths. DO NOT implement production code."

### 2-2. 失敗検証ゲート

- Use Task tool with subagent_type="code-reviewer"
- Prompt: "Verify that all tests for: [対象機能] are failing correctly. Ensure failures are for the right reasons (missing implementation, not test errors)."

**GATE**: 全テストが適切に失敗するまで次フェーズに進まない。

ゲートの検証チェックリストは [references/validation-checkpoints.md](references/validation-checkpoints.md) を参照。

## Phase 3: GREEN - 最小実装

### 3-1. 最小限の実装

- Use Task tool with subagent_type="backend-architect"
- Prompt: "Implement MINIMAL code to make tests pass for: [対象機能]. Focus only on making tests green. Do not add extra features or optimizations."

### 3-2. 成功検証ゲート

- Use Task tool with subagent_type="test-automator"
- Prompt: "Run all tests for: [対象機能] and verify they pass. Check test coverage metrics."

**GATE**: 全テスト成功 + カバレッジ閾値達成まで次フェーズに進まない。

閾値とトリガー設定は [references/thresholds.md](references/thresholds.md) を参照。

## Phase 4: REFACTOR - 品質改善

### 4-1. 実装コードのリファクタリング

- Use Task tool with subagent_type="code-reviewer"
- Prompt: "Refactor implementation for: [対象機能] while keeping tests green. Apply SOLID principles, remove duplication, improve naming. Run tests after each change."

### 4-2. テストコードのリファクタリング

- Use Task tool with subagent_type="test-automator"
- Prompt: "Refactor tests for: [対象機能]. Remove duplication, improve names, extract common fixtures. Ensure coverage unchanged."

## Phase 5: 統合テスト

Phase 2-4 と同じ RED→GREEN サイクルを統合テストに適用する。

### 5-1. 統合テスト作成（RED）

- Use Task tool with subagent_type="test-automator"
- Prompt: "Write FAILING integration tests for: [対象機能]. Test component interactions, API contracts, and data flow."

### 5-2. 統合実装（GREEN）

- Use Task tool with subagent_type="backend-architect"
- Prompt: "Implement integration code for: [対象機能] to make integration tests pass."

## Phase 6: 最終レビュー

- Use Task tool with subagent_type="architect-review"
- Prompt: "Perform comprehensive review of: [対象機能]. Verify TDD process was followed, check code quality, test quality, and coverage. Suggest improvements."
- **Action**: 重要な指摘はテスト緑を維持しつつ修正

## 開発モード

### Incremental モード（デフォルト）

1テストずつ RED→GREEN→REFACTOR を回す。小さな単位で確実に進める。

### Suite モード

機能/モジュール単位で全テストを一括作成してから実装。大きな機能に向く。

## 規律違反時のリカバリ

TDD規律が破られた場合:
1. 即座に停止
2. 違反フェーズを特定
3. 最後の正常状態にロールバック
4. 正しいフェーズから再開

## アンチパターン

- テストより先に実装を書く
- 最初から成功するテストを書く
- Refactorフェーズをスキップする
- テストを修正して通す
- 失敗テストを無視する

## 注意事項

- `guiding-tdd-development` スキルとの併用は不要（このスキルが上位互換）
- コンテキスト消費が大きいため、小規模な修正には `guiding-tdd-development` か `/tdd` を推奨
- テストフレームワークはプロジェクトの既存設定に従う
