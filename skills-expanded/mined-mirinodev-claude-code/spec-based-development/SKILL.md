---
name: spec-based-development
description: Generate detailed, agent-executable feature specifications by interviewing the user with AskUserQuestionTool. Transforms rough ideas into comprehensive SPEC.md files through phased deep interviews (5 phases) covering technical architecture, data design, API design, UI/UX, edge cases, security, performance, and tradeoffs. Produces hybrid specs with Acceptance Criteria and phased implementation tasks with dependencies. Use when user mentions "spec", "仕様書作成", "仕様駆動", "インタビューして", "SPEC.md", "feature spec", "仕様を書いて", "大きな機能を計画", or wants to plan a feature before implementation.
---

# Spec-Based Development

AskUserQuestionToolでフェーズ制インタビューを実施し、Agentが自律実装可能な精度のSPEC.mdを生成する。

## Workflow

Task Progress:

- [ ] Step 1: アイデア把握
- [ ] Step 2: 既存SPEC.md確認
- [ ] Step 3: フェーズ制インタビュー実施
- [ ] Step 4: SPEC.md書き出し
- [ ] Step 5: 次ステップ案内

### Step 1: アイデア把握

ユーザーの入力から対象機能・プロジェクトの概要を把握する。情報が不足していても問題ない（Step 3で掘り下げる）。

### Step 2: 既存SPEC.md確認

プロジェクトルートに `SPEC.md` が存在するか確認する。

- **存在する場合**: 内容を読み込み、既存の仕様を踏まえてインタビューする
- **存在しない場合**: 新規作成前提で進む

### Step 3: フェーズ制インタビュー実施

5フェーズで段階的に深堀りする。各フェーズの開始時に現在のフェーズ名をユーザーに伝えること。

**フェーズ概要:**

1. **概要・ゴール**（3-5問）: 目的、ターゲットユーザー、成功指標、スコープ境界
2. **技術的実装**（10-15問）: アーキテクチャ、データ設計、API設計、状態管理、外部依存
3. **UI/UX**（5-10問）: 操作フロー、状態遷移、レスポンシブ、アクセシビリティ ※該当時のみ
4. **エッジケース・非機能要件**（5-10問）: 異常系、セキュリティ、パフォーマンス、運用
5. **トレードオフ・未決定事項**（3-5問）: 技術選定理由、MVP境界、既知のリスク

各フェーズの詳細な質問パターンは [references/interview-phases.md](references/interview-phases.md) を参照。

**CRITICAL: インタビュールール:**

- 明らかな質問はしない。ユーザーが考慮していなかった深い部分を掘り下げる
- 1回のAskUserQuestionToolで1-4問ずつ質問する
- 大きな機能では最低40問以上質問すること
- ユーザーが「完了」「十分」「もういい」と言うまで継続する
- 技術フェーズでは特に深く掘り下げる（DB選定で終わらず、インデックス戦略・キャッシュ無効化・トランザクション境界まで）

### Step 4: SPEC.md書き出し

インタビュー結果をプロジェクトルートの `SPEC.md` に書き出す。

フォーマットは [references/spec-template.md](references/spec-template.md) を参照。ハイブリッド型テンプレートを使用し、以下を必ず含める:

- **機能要件**: 各要件にAcceptance Criteria（チェックボックス形式）
- **実装タスク**: フェーズ分割・依存関係・完了条件付き

セクションは機能の性質に応じて調整する。不要なセクションは省略してよい。

### Step 5: 次ステップ案内

SPEC.md作成後、以下を案内する:

```
SPEC.mdを作成しました！

次のステップ:
1. SPEC.mdの内容を確認・修正してください
2. 実装は新しいセッションで行うのがおすすめです:
   - /clear でコンテキストをリセット
   - 「@SPEC.md に基づいて実装して」と指示

インタビューのやりとりでコンテキストが消費されているため、
クリーンな新セッションの方が実装品質が高くなります。
```

## References

- Original concept: https://x.com/trq212/status/2005315275026260309
- Interview depth: https://x.com/trq212/status/2005315277828096030
