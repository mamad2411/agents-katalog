# 開発プロセス

本プロジェクトの開発は、以下のスキルを順番に実行して進めます。
各スキルがテンプレート・レビュー基準・手順を内包しており、自己完結しています。

## 初期セットアップ

| コマンド | 工程 | 出力 |
|---------|------|------|
| `/setup` | プロジェクト初期設定・再設定 | profile.yaml, rules/, CLAUDE.md 更新 |

## スキル一覧（実行順）

### ドキュメント工程

| コマンド | 工程 | 出力 |
|---------|------|------|
| `/step01-plan {feature名}` | 計画書作成 | 01-plan.md |
| `/step01-review {feature名}` | 計画レビュー | 01-plan-review.md |
| `/step02-requirements {feature名}` | 要件定義書作成 | 02-requirements.md |
| `/step02-review {feature名}` | 要件レビュー | 02-requirements-review.md |
| `/step03-design {feature名}` | 設計書作成 | 03-design.md |
| `/step03-review {feature名}` | 設計レビュー | 03-design-review.md |
| `/step04-specs {feature名}` | 仕様書作成 | 04-specs-technical.md + 04-specs-business.md |
| `/step04-review {feature名}` | 仕様レビュー | 04-specs-review.md |

### 実装工程

| コマンド | 工程 | 出力 |
|---------|------|------|
| `/step05-tasks {feature名}` | タスク化 + ブランチ作成 | 05-tasks.md |
| `/step05-run {feature名}` | タスク実行 + 完了管理 | 05-tasks.md (ステータス更新) |
| `/step06-report {feature名}` | 実装レポート | 06-report.md |
| `/step07-code-review {feature名}` | PR作成 + コードレビュー | 07-code-review.md |

### 品質保証工程

| コマンド | 工程 | 出力 |
|---------|------|------|
| `/step08-test {feature名}` | テスト設計 + 項目書作成 | 08-test-design.md + 08-test-cases.md |
| `/step08-run {feature名}` | テスト実行 | 08-test-cases.md (結果記入) |
| `/step09-inspection {feature名}` | 検品チェックリスト作成 | 09-inspection-checklist.md |
| `/step09-run {feature名}` | 検品実行 | 09-inspection-checklist.md (結果記入) |
| `/step10-summary {feature名}` | リリースサマリー | 10-release-summary.md |

### 振り返り・自己修復（マージ前に実施）

| コマンド | 工程 | 出力 |
|---------|------|------|
| `/step11-retro {feature名}` | 振り返り (Good/Bad/Try) | retro.md |
| `/step12-evolve {feature名}` | Agent/Skill/Rules 自己修復 | evolve-report.md |

### リリース

| コマンド | 工程 | 出力 |
|---------|------|------|
| `/step13-archive {feature名}` | PRマージ + アーカイブ | docs/03_done/ へ移動 |

## プロセスパス

step01-plan で変更規模を判定し、適切なパスを選択:

| パス | 条件 | スキップされる工程 |
|------|------|-----------------|
| **Full** | 複数ファイル or 50行超 | なし（全工程実行） |
| **Light** | 1ファイル and 50行以下 | step02-requirements, step02-review, step03-design, step03-review |
| **Refactoring** | UI変更なし and DB変更なし and ロジック変更なし（コード移動・分割・リネームのみ） | step02-requirements を簡略版に、step03-design を簡略版に（レビューは各1回に短縮） |

## レビューの判定フロー

各レビュー (step01-review 〜 step04-review, step07-code-review) は以下の判定を返します:

- **承認** → 次の工程へ進む
- **条件付き承認** → 軽微な修正後、再レビュー不要
- **差し戻し** → 修正して同じレビューを再実行

## フィーチャーのライフサイクル

```
docs/01_backlog/{feature名}/  ← 計画書作成時
     ↓ step05-tasks で移動
docs/02_active/{feature名}/   ← 実装〜品質保証
     ↓ step13-archive で移動
docs/03_done/{feature名}/     ← 完了（読み取り専用）
```

## .claude/ 構成

```
.claude/
├── agents/          ← レビュー・テスト・検品・プロセス分析の専門エージェント (10)
├── skills/          ← 開発プロセスのスキル定義 (21: setup + step01-13)
│   └── */assets/    ← テンプレート + レビュー基準
├── rules/           ← コーディング規約（/setup で Tech Stack 別に生成）
└── settings.json    ← 権限・プラグイン設定
```

## ナレッジベース

振り返り (`/step11-retro`) と自己修復 (`/step12-evolve`) で蓄積:

```
docs/knowledge/
├── patterns/         ← 成功パターン
├── anti-patterns/    ← 失敗パターン
├── playbooks/        ← 手順書
└── retros/           ← 振り返り・修復レポート
```
