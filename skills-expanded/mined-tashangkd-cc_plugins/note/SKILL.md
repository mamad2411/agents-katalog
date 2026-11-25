---
name: note
description: 个人笔记记录助手。自动以 JSON 格式记录想法、学习笔记、会议纪要到 ~/.note，支持标签分类和全文搜索。
user-invocable: true
---

# /note - 笔记记录助手

## 存储位置

`~/.note/notes/YYYY-MM/YYYY-MM-DD_NNN.json`

## 笔记 JSON 格式

```json
{
  "id": "2026-01-14_001",
  "timestamp": "2026-01-14T10:30:00+08:00",
  "created_at": "2026-01-14",
  "tags": ["git", "workflow"],
  "category": "learning",
  "title": "Git rebase 学习笔记",
  "content": "具体内容..."
}
```

## 自动分类规则

| 分类 | 触发关键词 |
|------|-----------|
| development | 实现、开发、重构、优化 |
| idea | 想法、建议、可以考虑、或许 |
| meeting | 会议、讨论、决定、周会 |
| bugfix | bug、问题、错误、修复 |
| learning | 学习、笔记、了解、研究 |
| other | 默认 |

## 自动标签关键词

| 标签 | 关键词 |
|------|--------|
| git | git, commit, push, pull, merge, rebase, branch |
| python | python, pip, uv, pytest |
| docker | docker, container, image, compose |
| auth | auth, login, token, jwt, oauth |
| api | api, rest, endpoint, http |
| refactor | refactor, 重构 |
| debug | debug, bug, fix, 修复 |

## 执行流程

1. 初始化检查：若 `~/.note` 不存在，创建目录和 `config.json`、`index.json`
2. 解析输入：提取内容、手动标签（`tags:xxx,yyy` 格式）
3. 自动分类：根据关键词匹配 category
4. 自动打标签：根据内容关键词匹配标签
5. 生成时间戳：使用**本地时间**（非 UTC），格式 `YYYY-MM-DDTHH:mm:ss+08:00`
6. 生成 ID：读取本月目录，取最大序号+1，格式 `YYYY-MM-DD_XXX`
7. 保存文件：写入 `~/.note/notes/YYYY-MM/YYYY-MM-DD_XXX.json`
8. 更新索引：追加到 `index.json` 的 `notes` 数组，更新 `total_notes` 和 `last_updated`

## 时间格式

```bash
# 使用 date 命令获取正确的本地时间戳
date "+%Y-%m-%dT%H:%M:%S%z"
# 输出示例：2026-01-14T18:44:24+0800
```

**重要**：必须使用本地时间，而非 UTC 时间。

## 使用方式

| 用户输入 | 操作 |
|----------|------|
| `/note 今天学习了 Git rebase` | 快速记录笔记 |
| `/note tags:git,workflow 学习 rebase` | 记录并指定标签 |
| `/note 初始化` | 创建 ~/.note 目录 |
| `/note 列出最近10条` | 显示最近笔记 |
| `/note 搜索 git` | 全文搜索笔记 |
| `/note 查看 learning 分类` | 按分类查看 |
| `/note` | 交互式记录（引导输入） |
