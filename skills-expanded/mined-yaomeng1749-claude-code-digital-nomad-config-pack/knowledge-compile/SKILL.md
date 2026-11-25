---
name: knowledge-compile
description: 将用户指定知识库中的原始资料编译为结构化 wiki 文章。仅在用户显式要求编译知识库、整理 raw、更新 wiki 或 knowledge compile 时使用。
---

# Knowledge Compile

> 仅在用户显式要求编译知识库时使用。不要自动写入任何默认知识库。

## 目标知识库

优先使用用户在本轮提供的知识库路径。若用户没有提供路径，询问目标位置。

可使用的通用约定：

| 用途 | 示例路径 |
|---|---|
| 团队/项目知识库 | `~/KnowledgeBase/Work` |
| 个人知识库 | `~/KnowledgeBase/Personal` |

## Usage

```
/knowledge-compile drop          # 编译 原始资料/碎片/ 中的新文件
/knowledge-compile convo         # 编译 原始资料/对话记录/ 中未编译的对话
/knowledge-compile worklog       # 编译工作日志
/knowledge-compile TASK-xxx      # 从已完成任务提取经验
```

## Workflow

1. **扫描未编译资料** — 在 `<KNOWLEDGE_BASE>/原始资料/` 中找 `compiled: false` 的文件

1.5 **读取知识库规范**：
   - 若目标知识库存在开发规范、踩坑记录、ADR、模板或索引，先读取这些文件。

2. **质量审核（编译前）**:
   - 列出从源文件中提取的知识点
   - **展示给用户，等用户确认"可以写入"后才继续**（不能跳过！）
   - 垃圾内容（临时调试、无意义记录）标记跳过

3. **识别核心主题** → 匹配 知识库/ 本体论分类:
   - `tech-*` — 技术模式 | `team-*` — 组织知识
   - `project-*` — 项目知识 | `process-*` — 流程规范
   - `synthesis/` — 跨领域洞察

4. **矛盾和重复检测**:
   - 在 `<KNOWLEDGE_BASE>/知识库/` 搜索相关文章
   - **重复**: >80% 重叠 → 合并到已有文章
   - **矛盾**: 新旧冲突 → **不自动裁决，问用户**，在 frontmatter 标记

5. **编译为 wiki 文章**:
   - 若存在 `<KNOWLEDGE_BASE>/模板/知识文章模板.md`，优先参考该模板
   - 保持简洁：要点式 + 表格，有 `## 关键要点`
   - 用 `[[wikilinks]]` 交叉引用

6. **更新索引和日志**:
   - 更新 `知识库/{category}/_索引.md`
   - 更新 `知识库/_总索引.md`
   - 追加 `知识库/活动日志.md`

7. **标记已编译** — 源文件 `compiled: true`

## Rules

- **质量门槛**: 垃圾内容不进 wiki
- **矛盾不自动裁决**: 问用户
- **重复自动合并**: 更新而不创建新文章
- 所有路径使用绝对路径
