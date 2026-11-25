---
name: my-lookup
description: 搜索个人知识库 My vault 的 wiki
---

# My Lookup — 个人知识查询

> 搜索 `~/Desktop/My vault/My vault/知识库/`。

## 知识库路径

```
~/Desktop/My vault/My vault
```

## Usage

```
/my-lookup {query}       # 搜索个人 wiki
```

## Workflow

1. 从 `~/Desktop/My vault/My vault/知识库/_总索引.md` 开始
2. 根据关键词定位相关分类
3. 进入 `_索引.md` 查找匹配文章
4. 阅读文章并返回关键要点

## Rules

- 从 _总索引.md 开始，不凭记忆猜
- 找不到就建议用 `/my-compile` 创建
