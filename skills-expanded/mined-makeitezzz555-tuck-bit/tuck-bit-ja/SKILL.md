---
name: tuck-bit-ja
description: "TuckBit はコーディングエージェント向けのポータブルなスキルです。正確性を損なわず、適切な情報・ツール・検証手順を選びます。"
license: MIT
compatibility: Portable Agent Skills; project-scoped install only.
metadata:
  author: TuckBit contributors
  version: "0.4.0"
  locale: ja
---

# TuckBit — 日本語

> スキルの主要部分は翻訳済みです。技術リファレンスは現時点で英語のままで、コミュニティによる確認が必要です。

単にトークン数を減らすのではなく、使用資源あたりの正しく検証された成果を最適化してください。

基本機能はレジストリ、コンテキスト、検証、予算の4つ。オーケストレーションと計測は任意です。

## 標準的な作業手順

ユーザーの正確な依頼、実際に利用できる指示、許可されたツールから始めます。制約、承認、必須検証を維持してください。

1. 目的、制約、リスク、停止条件を定義します。簡単な作業を過度に計画しません。
2. 関連するコード・文書・ツールを必要最小限で探し、必要なときだけ範囲を広げます。
3. ホストの標準ツール検索を優先します。メタデータは手がかりであり実行許可ではありません。
4. 小規模な作業には1エージェントを使い、独立した作業だけ責任範囲と成果条件を決めて分担します。
5. 対象テストを実行し、最終リビジョンですべての必須統合・安全性チェックを行います。
6. 変更、テスト、リスク、障害を検証可能な形で報告します。無限のポーリングではなくチェックポイントを使います。

## 必要なリファレンスだけを読み込む

- `references/task-contract.md` — task contracts / host instructions.
- `references/workflows.md` — Fast / Standard / Deep workflows.
- `references/registry.md` — discovery and permission limits.
- `references/context.md` — source-linked evidence and checkpoints.
- `references/verification.md` — tests and integration checks.
- `references/budget.md` — bounded iterations.
- `references/orchestration.md` — optional independent agents.
- `references/metrics.md` — optional evaluation.

## 必須の制約

安全確認を省略せず、正確性を下げず、測定値を捏造せず、認証情報を読まず、承認を迂回しません。権限はホスト側で管理します。

**開発者プレビューです。インストールだけではスキルの起動やトークン削減は証明できません。**
