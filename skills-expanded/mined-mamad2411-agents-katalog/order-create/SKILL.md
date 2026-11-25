---
name: order-create
description: 上長(ユーザ)との対話セッションを通じ、依頼事項のメモ(scrum/order/orderXXX.md)を作成・更新する。ユーザからの要求事項や依頼事項の整理、スクラムチームへの作業依頼準備に使用する。
---

# 依頼事項メモの作成・更新

## 準備
- イツキエージェントは Agent ツールで `subagent_type: customer-itsuki`（`.claude/agents/customer-itsuki.md`）として起動します。

## 手順
1. イツキエージェントで、`scrum/order/orderXXX.md` を読み、内容を理解する（XXXは最新の番号のみを確認します。）
2. スクラムチームに作業を依頼するにあたって、不明点やクリアにすべき点を上長と対話で確認してください。
3. `scrum/order/orderXXX.md` を更新し、スクラムチームとの対話に備えます。
4. 更新した `scrum/order/orderXXX.md` が保存されていることを確認します。Drive 共有フォルダ経由で他のメンバーに行き渡ります。
 - git へのコミットは管理者が行います（`scrum/git-operation-policy.md`）。

## ファイル更新のポイント
- 依頼事項の内容を明確に記載してください。
- もともとのフォーマットにとらわれず、必要に応じて内容を整理し、わかりやすくしてください。
