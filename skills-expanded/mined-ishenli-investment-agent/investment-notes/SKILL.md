---
name: investment-notes
description: >
  查询用户的投资笔记：公司关键词笔记、行业分析记录、投资重点备忘。
  当用户问"我的笔记里怎么看 XX"、"之前记过什么"、"我的投资备忘"、"把我的观点找出来"，
  或分析某资产前想参考用户自己沉淀过的观点时，**务必使用此技能**。
version: "1.0.0"
category: notes
author: investment-agent
---

# 投资笔记查询

## 优先：语义查询工具

调用 `noteQueryTool`，参数 `query` 传关键词（公司名、代码、主题均可）：

```json
{"query": "NVDA"}
```

工具按关键词匹配标题、内容与标签，返回最相关的笔记。多主题时拆多次查询（公司名、行业、事件关键词各查一次），不要一次塞超长查询串。

## 补充：结构化列表

需要"最近记了什么"这类列表场景时，用 `dbQueryTool` 查表 `notes`（列：title, content, tags, updatedAt）：

```json
{"table": "notes", "orderBy": "updated_at", "limit": 20}
```

按用户过滤会自动落到当前用户，无需手动指定 userId。

## 回答要求

1. 引用笔记时说明"这是你自己之前记录的观点"，与外部资讯（`TravilySearchTool`、`stockSearchNewsTool`）的结论区分开。
2. 用户笔记与当前市场数据冲突时，同时呈现两者并指出差异时间点。

## 限制

- 当前没有创建/修改笔记的工具；用户要求"帮我记一笔"时，告知本次在聊天中即可记录要点，或建议用户把结论保存到应用笔记页。
