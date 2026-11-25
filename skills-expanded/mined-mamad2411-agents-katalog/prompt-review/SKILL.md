---
name: prompt-review
description: Audit the assistant's previous reply for unnecessary verbosity and, when the latest reply is verbose, rewrite it once in a concise form. Use after turning on pi-prompt review mode or whenever the user asks to trim a reply.
---

# prompt-review

审计上一条回复：找出明显冗余，并在必要时用精炼版重写一次。

## 判定标准（符合任一再重写）

- 头/尾有与问题无关的寒暄、铺垫或"下面我将…"式预告
- 复述了用户已经给出的事实或上下文
- 有重复的结论、冗余的过渡词、客套句（如"随时问我 / 希望对你有帮助"）
- 散文解释长度超过代码本身（代码场景）

## 重写规则

- 只输出被审回复的核心结论：结论先行、列表优先、每句删到不可再删
- 保留用户明确要求的信息、错误处理细节、路径/报错原文
- 不新增信息、不改变建议、不改结论
- 重写后追加一行审计结果：`[prompt-review] 原 N 行/约 M 词 → 新 N 行/约 M 词`（粗略估算即可）
- 原回复已足够精炼时，只输出一行结果，不再重写

## 边界

- 永远不删除：错误处理、安全提示、用户点名要求的信息
- 审计对象是"怎么说"，不是"写什么"——不要建议删功能/删代码