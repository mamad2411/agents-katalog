---
name: knowledge-lookup
description: 搜索和查询知识库，从 wiki 索引中快速找到相关信息
---

# Knowledge Lookup

## Usage

```
/knowledge-lookup {query}        # 搜索 wiki
/knowledge-lookup tasks {query}  # 搜索任务
/knowledge-lookup schedule       # 查看当前排班
```

## Workflow

1. **导航协议**:
   - 从 `知识库/_总索引.md` 开始
   - 根据查询关键词定位相关分类
   - 进入分类的 `_索引.md` 查找匹配文章
   - 阅读匹配文章的内容

2. **返回结果**:
   - 匹配的文章列表（含标题和一句话摘要）
   - 关键要点提取
   - 相关链接
   - confidence 级别
   - 如有矛盾，标注出来

3. **任务查询** (`tasks`):
   - 扫描 `任务/` 下所有 TASK-*.md
   - 按 frontmatter 匹配（assignee, status, project, priority）
   - 返回匹配的任务列表

4. **排班查询** (`schedule`):
   - 读取最新的 `排班/weeks/` 文件
   - 展示当前周排班和人员可用度

## Rules

- 始终从 _总索引.md 开始导航，不要凭记忆猜测
- 如果找不到匹配文章，建议用 `/knowledge-compile` 创建
- 返回结果要附带 confidence 级别
- 搜索范围: 知识库/ > 任务/ > 排班/ > 原始资料/
