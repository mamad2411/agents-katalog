---
name: supermap-search
description: 统一搜索 Supermap wiki、Jira 和 YouTrack。同时搜索三个系统并整合结果。使用方法：/supermap-search <搜索词>
disable-model-invocation: false
allowed-tools: Bash
---

# Supermap 统一搜索技能

同时搜索 wiki、jira、youtrack 三个系统，整合展示搜索结果。

## 使用方法

```
/supermap-search <搜索关键词>
```

**示例：**
- `/supermap-search iManager` - 搜索所有系统中与 iManager 相关的内容
- `/supermap-search 部署` - 搜索所有系统中与部署相关的内容

## 执行方式

Claude 应该并行执行以下三个搜索：

1. **Wiki 搜索**
```bash
python3 .claude/skills/supermap-wiki-search/scripts/search_wiki.py "<搜索词>"
```

2. **Jira 搜索**
```bash
python3 .claude/skills/supermap-jira-search/scripts/search_jira.py "<搜索词>"
```

3. **YouTrack 搜索**
```bash
python3 .claude/skills/supermap-youtrack-search/scripts/search_youtrack.py "<搜索词>"
```

## 输出格式

结果按以下格式展示：

```markdown
## Wiki 搜索结果

| Title | Space | Excerpt |
|-------|-------|---------|
| ... | ... | ... |

## Jira 搜索结果

| 标题 | 链接 |
| --- | --- |
| ... | ... |

## YouTrack 搜索结果

| 标题 | 链接 |
| --- | --- |
| ... | ... |
```

## 前置要求

需要设置以下环境变量：
- `SUPERMAP_WIKI_TOKEN` - Wiki 搜索 token
- `SUPERMAP_JIRA_TOKEN` - Jira 搜索 token
- `SUPERMAP_YOUTRACK_TOKEN` - YouTrack 搜索 token

## 错误处理

- 如果某个系统的 token 未设置，跳过该系统的搜索并提示用户
- 如果某个系统搜索失败，继续显示其他系统的结果