---
name: order-create-without-user
description: 上長(ユーザ)不在時に、依頼事項のメモ(scrum/order/orderXXX.md)を作成・更新する。ユーザからの要求事項や依頼事項の整理、スクラムチームへの作業依頼準備に使用する。
---

# 依頼事項メモの作成・更新

## 準備
- イツキエージェントは Agent ツールで `subagent_type: customer-itsuki`（`.claude/agents/customer-itsuki.md`）として起動します。

## 手順
1. イツキエージェントで、`scrum/order/orderXXX.md` を読み、内容を理解する（XXXは最新の番号のみを確認します。）
2. スクラムチームに作業を依頼するにあたって、不明点やクリアにすべき点を自身で考えます。上長だったらこうするだろうをベースに整理します。
3. `scrum/order/orderXXX.md` を更新し、スクラムチームとの対話に備えます。

## ファイル更新のポイント
- 依頼事項の内容を明確に記載してください。
- もともとのフォーマットにとらわれず、必要に応じて内容を整理し、わかりやすくしてください。
