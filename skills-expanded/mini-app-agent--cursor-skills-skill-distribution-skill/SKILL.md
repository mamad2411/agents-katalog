---
name: skill-distribution
description: "Skillを複数のエージェントリポジトリに一括配布（上書き/新規）する。デスクトップ配下の.cursor/skills/に同名フォルダがあれば上書き、なければ新規作成。「スキル配布」「skill配布」「一括配布」「skills同期」「上書き配布」を依頼されたときに使用する。"
---

# Skill Distribution Workflow

## Overview
browser-controller-agentが持つSkillを、デスクトップ配下の他エージェントリポジトリに一括配布する。
- 上書き配布: 配布先に同名フォルダが存在する場合、完全上書き
- 新規配布: 配布先に同名フォルダが存在しない場合、新規作成
- 選択配布: 単一Skill/複数Skill/全Skillを選択可能

## Instructions

1. Preflight（必須）:
   - ドキュメント精査原則：生成前に必ず以下を実施すること。
     - 配布元のSkillフォルダ構成を確認する。
     - 配布先リポジトリの一覧を取得する。
   - `./questions/skill_distribution_questions.md` を使って配布パラメータを確定する。
   - 配布モードを確定する:
     - `overwrite`: 既存フォルダを上書き（デフォルト）
     - `new_only`: 既存フォルダがない場合のみ配布
     - `all`: 上書き＋新規の両方

2. 配布実行:
   - スクリプトパス: `./scripts/distribute_skill.py`
   - 実行方法:
     ```bash
     # 単一Skill配布（上書き）
     python .cursor/skills/skill-distribution/scripts/distribute_skill.py chatgpt-parallel-research

     # 複数Skill配布
     python .cursor/skills/skill-distribution/scripts/distribute_skill.py chatgpt-parallel-research x-automation note-automation

     # 全Skill配布
     python .cursor/skills/skill-distribution/scripts/distribute_skill.py --all

     # 新規のみ配布（既存は上書きしない）
     python .cursor/skills/skill-distribution/scripts/distribute_skill.py chatgpt-parallel-research --mode new_only

     # ドライラン（実行せず確認のみ）
     python .cursor/skills/skill-distribution/scripts/distribute_skill.py chatgpt-parallel-research --dry-run

     # 特定のリポジトリのみに配布
     python .cursor/skills/skill-distribution/scripts/distribute_skill.py chatgpt-parallel-research --repos fiction_craft_agent o2p-agent
     ```

3. 配布対象:
   - 配布元: `/Users/matuni__/Desktop/browser-controller-agent/.cursor/skills/`
   - 配布先: `/Users/matuni__/Desktop/*/.cursor/skills/`（同名フォルダ）
   - 除外: 配布元自身（browser-controller-agent）

4. 配布可能なSkill一覧:
   | Skill名 | 説明 |
   |---------|------|
   | chatgpt-parallel-research | ChatGPT並列検索・ブレスト |
   | x-automation | X(x.com)自動操作 |
   | kindle-automation | Kindle Cloud Reader操作 |
   | note-automation | note.com自動操作 |
   | teams-automation | Microsoft Teams操作 |
   | notebooklm-workflow | NotebookLM MD→IV変換 |
   | browser-controller | ブラウザ共通操作基盤 |
   | browser-controller-extension-enhancement | 拡張機能開発 |
   | skill-maintenance | Skill保守 |
   | subagent-maintenance | Subagent保守 |
   | core-rule-maintenance | コアルール保守 |
   | skill-distribution | スキル配布（本Skill） |

5. QC（必須）:
   - `recommended_subagents` のQC Subagentに評価を委譲する。
   - Subagentは `./evaluation/evaluation_criteria.md` に基づきQCを実施する。
   - 配布結果を確認し、エラーがあれば修正する。
   - 指摘に対し「修正した/しない」と理由を残す。

6. バックログ反映:
   - 配布に失敗したリポジトリ、追加配布が必要なSkillをバックログへ反映する。

---

## 出力形式

配布完了後、以下の形式で結果を報告する:

```
## 配布結果

### 配布Skill: {skill-name}

| 配布先 | 結果 |
|--------|------|
| fiction_craft_agent | Updated |
| o2p-agent | Updated |
| lifelog_agent | Created (new) |

### サマリー
- 配布先: XX リポジトリ
- 更新: XX
- 新規: XX
- スキップ: XX
- エラー: XX
```

---

## subagent_policy
- 品質ループ（QC/チェック/フィードバック）は必ずサブエージェントへ委譲する
- 指摘の反映は最小差分で行う
- 指摘に対し「修正した/しない」と理由を最終成果物に残す

## recommended_subagents
- qa-skill-qc: 配布完了確認、ファイル整合性、エラー有無を検査

## Resources
- questions: ./questions/skill_distribution_questions.md
- assets: ./assets/skill_distribution_template.md
- evaluation: ./evaluation/evaluation_criteria.md
- scripts: ./scripts/distribute_skill.py

## Next Action
- 配布完了後、各リポジトリでSkillが正常に動作することを確認する。
- 新規配布したリポジトリでは、CLAUDE.mdのワークフロー索引への追記が必要な場合がある。
