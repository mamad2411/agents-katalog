---
name: ask-to-po-shuri
description: プロダクトオーナーシュリとの対話型セッション
---

# プロダクトオーナーシュリとの対話型セッション

- **シュリエージェント**は Agent ツールで以下の構成で起動してください。
  - 役割：Product Owner
  - subagent_type：`product-owner-shuri`
  - 定義：`.claude/agents/product-owner-shuri.md`

# セッション実施

- 対話型セッションを通じてユーザとシュリエージェントで会話を行います。
  - ユーザの質問や要望を受けて、ファイルの調査回答やプロダクトバックログのPBIの追加や修正を行います。
