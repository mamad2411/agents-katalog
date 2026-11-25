---
name: guiding-tdd-development
description: Guide Test-Driven Development with task splitting, Red-Green-Refactor cycle, and framework auto-detection. Use when developing features with TDD approach, fixing bugs test-first, or when user mentions "TDD", "テスト駆動開発", "test-first", "/tdd".
---

# Guiding TDD Development

機能をTDD可能な小さな単位に分割し、Red-Green-Refactorサイクルで実装するスキル。

## Contents

- 実行フロー
- Phase 1: 要件分析とタスク分割
- Phase 2: TDDサイクル
- バグ修正フロー
- テストフレームワーク自動検出
- 注意事項

## 実行フロー

```
1. 要件分析 → タスク分割（ToDoリスト）
2. 各タスクで TDD サイクル:
   RED → GREEN → REFACTOR → ToDoリスト更新 → 繰り返し
```

## Phase 1: 要件分析とタスク分割

1. ユーザーの要求を分析
2. TDD可能な小さな単位にタスクを分割
3. TaskCreateツールで全タスクをリスト化

### 実装順序の原則

- 依存関係の少ないものから実装
- インターフェース/型定義から始める
- 単純な機能から複雑な機能へ

### 出力形式

```
## TDDタスク分割

### 実装する機能
<機能の概要>

### タスク一覧
1. [単体機能A] のテストと実装
2. [単体機能B] のテストと実装
3. [統合機能C] のテストと実装
```

## Phase 2: TDDサイクル

### Red（レッド）

1. ToDoリストから**1つ**ピックアップ
2. テストから書く（テストファースト）
3. テストを実行して**失敗させる**

### Green（グリーン）

1. 失敗しているテストを成功させることに集中
2. **最小限のコード**を書く（綺麗より動作優先）
3. 全てのテストが成功することを確認

### Refactor（リファクタリング）

1. 全テストが成功している状態で整理整頓
2. **テストは通ったまま**にする
3. 実装コード、テストコード両方をリファクタリング

### 繰り返し

1. 気付きをToDoリストに反映
2. 次のToDoを選んでRedに戻る

### 各タスクの出力形式

```
### タスク: [タスク名]

#### RED: テストを書く
<失敗するテストコード>

#### GREEN: 実装する
<テストを通す最小実装>

#### REFACTOR: リファクタリング
<改善されたコード>
```

## バグ修正フロー

バグ修正もTDDで行う:

1. **Red**: バグを再現する失敗テストを書く
2. **Green**: バグを修正してテストを通す
3. **Refactor**: コードを整理

## テストフレームワーク自動検出

プロジェクトの設定ファイルからテストフレームワークを自動検出する:

- **JavaScript/TypeScript**: Jest, Vitest, Mocha
- **Python**: pytest, unittest, nose2
- **Go**: testing, testify
- **Rust**: cargo test
- **Ruby**: RSpec, minitest
- その他: プロジェクトの設定ファイルから判定

テストファイルの配置場所もプロジェクトの慣習に従う。

## 注意事項

- テストを書かずに実装を進めない
- 複数の機能を同時に実装しない（1つずつ）
- テストが失敗したままリファクタリングしない
- モックやスタブは必要最小限に
- テストは独立して実行可能にする
- E2Eテストよりユニットテストを優先

## 参考記事

詳細は [references/tdd-resources.md](references/tdd-resources.md) を参照。
