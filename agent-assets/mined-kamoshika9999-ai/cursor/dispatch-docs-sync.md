---
description: 配台ロジック変更時は 配台ルール.md / 配台ルール.html を必ず同期更新する。
alwaysApply: true
---

# 配台ロジック変更とドキュメント同期

## 必須（エージェントが守ること）

**`planning_core.py` をはじめ、配台・割付・need／skills／チーム選定・段階2に効くロジックを変更したターンでは、同じ依頼の一環として次を実施する。**

1. **`細川/GoogleAIStudio/テストコード/配台ルール.md`** を、変更後の挙動・環境変数・優先順位と矛盾しないよう更新する。
2. **`細川/GoogleAIStudio/テストコード/配台ルール.html`** を、上記と同趣旨で要約・目次・表を更新する（HTML は業務向け要約、詳細は md を正とする想定でよい）。

## 対象の目安（例）

- `python/planning_core.py` の `generate_plan`、日次割付、チーム割当、need／surplus、納期リトライ、§A／§B 関連
- 段階2エントリやマスタ読込が配台に直結する変更（`plan_simulation_stage2.py`、need シート解釈の変更など）

## 正本

- **実装の正** … ソースコード
- **業務・仕様の文章の正（リポジトリ内）** … `配台ルール.md`（HTML は併せて更新）

※ ローカルコミット手順・メッセージは `.cursor/rules/pre-edit-git-commit-push.mdc` に従う。
