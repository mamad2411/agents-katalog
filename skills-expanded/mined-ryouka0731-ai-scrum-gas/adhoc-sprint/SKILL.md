---
name: adhoc-sprint
description: ユーザからの突発的な要望に対応するスクラムチーム作業
---

## 準備
- シュリエージェントは Agent ツールで `subagent_type: product-owner-shuri`（`.claude/agents/product-owner-shuri.md`）として起動します。
- マヤエージェントは Agent ツールで `subagent_type: developer-maya`（`.claude/agents/developer-maya.md`）として起動します。
- ダイチエージェントは Agent ツールで `subagent_type: developer-daichi`（`.claude/agents/developer-daichi.md`）として起動します。
- ヨミエージェントは Agent ツールで `subagent_type: contractor-yomi`（`.claude/agents/contractor-yomi.md`）として起動します。
- サキトエージェントは Agent ツールで `subagent_type: contractor-sakito`（`.claude/agents/contractor-sakito.md`）として起動します。
- ケンジエージェントは Agent ツールで `subagent_type: scrum-master-kenji`（`.claude/agents/scrum-master-kenji.md`）として起動します。
- ヒツギエージェントは Agent ツールで `subagent_type: reviewer-hitsugi`（`.claude/agents/reviewer-hitsugi.md`）として起動します。

## セッション実施

- ユーザからのリクエストをシュリエージェントが受け取ります。
- シュリエージェントは内容を確認し、適切なサブエージェント（マヤ、ダイチ、ケンジ、ヨミ、サキト、ヒツギ）にタスクを割り振ります。
 - サブエージェントは作業に対して、最新の情報・公式情報の裏どりを取りながら作業を行います。
 - 並列でのタスク処理を行うことができます
 - シュリエージェントで回答できる内容は、直接ユーザに回答します。
- シュリエージェントが、タスクの結果をもとにユーザのリクエストに回答できるか確認します。
  - 回答できる場合は、ユーザに回答します。
  - 回答できない場合は、タスクの結果をもとに追加のタスクを割り振ります。
  - このプロセスを繰り返します。もし3回繰り返しても回答できない場合は、ユーザにその旨を伝えます。
- ヒツギエージェントが、タスクの結果やユーザへの回答内容をレビューします。指摘がある場合は、シュリエージェントに修正リクエストを送ります。シュリエージェントは、必要に応じてサブエージェントに修正タスクを割り振ります。
 - ヒツギエージェントのレビューで指摘がなくなるまでこのプロセスを繰り返します。

**タスクの割り振りや回答の際には、必要に応じてサブエージェント同士で情報共有や協力を行ってください。**
