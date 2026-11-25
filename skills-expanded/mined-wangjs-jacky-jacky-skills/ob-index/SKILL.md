---
name: ob-index
description: "Obsidian 知识库索引构建与维护。编译环节委托给 ob-compile 执行。当用户想要更新索引、整理知识库、发现笔记关联时触发此 skill。"
---

<role>Obsidian 知识库索引引擎，负责构建/更新索引、发现知识关联、生成综合文章。编译环节委托给 ob-compile。</role>
<purpose>维护 wiki/index.md 作为知识库的导航核心，确保所有内容可被发现和关联。运行反思引擎发现二阶知识。编译未处理内容时调用 ob-compile。</purpose>
<trigger>

```text
触发词：
- 编译知识库
- 更新索引
- ob-index
- 处理未编译内容
- 发现关联
- 反思引擎

示例：
- "ob-index"
- "编译知识库"
- "更新知识库索引"
- "有哪些内容还没处理"
```

</trigger>
<gsd:workflow xmlns:gsd="urn:gsd:workflow">
  <gsd:meta>requires=OBSIDIAN_REPO; focus=index,reflect</gsd:meta>
  <gsd:goal>维护索引完整性，发现知识间关联并生成综合文章。编译环节委托给 ob-compile。</gsd:goal>
  <gsd:phase>**委托 ob-router skill** 解析当前激活仓库路径，扫描 raw/ 下 status: uncompiled 的文件。</gsd:phase>
  <gsd:phase>调用 ob-compile --mode incremental 编译未处理内容。</gsd:phase>
  <gsd:phase>编译完成后运行反思引擎：从索引摘要中发现跨领域主题、隐含关系、矛盾和空白。</gsd:phase>
  <gsd:phase>对证据充分的关联生成综合文章，写入对应主题目录，更新索引。</gsd:phase>
</gsd:workflow>

# Obsidian 知识库索引 (ob-index)

编译未处理内容，构建/更新知识库索引，发现关联并生成综合文章。

## 配置检查

**【硬约束】仓库路径一律委托 ob-router skill 解析，本 skill 不自行读取路径文件。**

调用 ob-router skill 获取 `$OBSIDIAN_REPO`：
- ob-router 内部处理优先级（ob-router.json → CLAUDE.md → 询问）
- 若 ob-router.json 不存在，ob-router 会**主动提示** `ob-router init` 持久化
- 若存在多个仓库，ob-router 会**主动询问**切换目标，不静默使用默认值

将 ob-router 返回的路径保存为 `$OBSIDIAN_REPO`，后续全程使用此变量。

## 执行流程

### 第一步：检查未编译内容

扫描 `$OBSIDIAN_REPO/raw/` 下所有 `.md` 文件，筛选 frontmatter 中 `status: uncompiled` 的文件。

```bash
grep -rl "status: uncompiled" "$OBSIDIAN_REPO/raw/" --include="*.md"
```

如果没有未编译内容：

```
所有资料已编译。是否需要：
1. 重建完整索引
2. 运行反思引擎
3. 退出
```

使用 AskUserQuestion 让用户选择。

### 第二步：调用 ob-compile 编译未处理资料

将扫描到的未编译文件列表交给 ob-compile 处理：

1. 调用 `ob-compile --mode incremental` 编译所有未编译内容
2. ob-compile 负责完整的编译流程（主题匹配、生成 wiki、分配 article_id、更新索引、标记 raw status → compiled）
3. ob-compile 完成后，继续执行后续步骤（反思引擎等）

> **编译逻辑全部在 ob-compile 中实现**，ob-index 不重复实现编译步骤。

### 第三步：重建索引（可选）

如果用户选择重建完整索引：

1. **扫描 article_id 状态**：检查所有 wiki 文章是否都有 article_id
   ```bash
   # 列出缺少 article_id 的文章
   find "$OBSIDIAN_REPO/wiki/" -name "*.md" ! -name "index.md" ! -name "log.md" -exec sh -c 'grep -L "article_id:" "$1" && echo "  缺少 article_id"' _ {} \;
   ```
   - 如果发现缺少 article_id 的文章，为每篇随机生成唯一 ID（使用上方生成命令 + 唯一性验证）
   - 报告补分配结果

2. 扫描 `$OBSIDIAN_REPO/wiki/` 下所有 `.md` 文件（排除 index.md、log.md）
3. 读取每个文件的 frontmatter 和第一段
4. 重新生成 `$OBSIDIAN_REPO/wiki/index.md`：

```markdown
---
tags: [知识库, index]
type: index
article_id: OBA-{随机8位}
updated_at: {日期}
---

# 知识库索引

> 最后更新：{日期}
> 文章总数：{数量}

## 概念
{按字母排序的概念条目，每行一个}

## 实体
{按字母排序的实体条目}

## 提炼知识
{按日期倒序排列的 distill 条目}
```

**索引条目格式**（每行一个）：
```
- [[{相对路径}]] `OBA-{随机ID}` — {一句话描述，≤ 80 字}
```

**渐进式索引**：

当文章总数超过 200 篇时，拆分为子索引：
- 每个主题目录的 `wiki/{theme}/index.md` 管理自己的条目
- 主 `wiki/index.md` 只保留主题标题和子索引链接

### 第三步半：刷新项目 CLAUDE.md 索引段

索引重建后，扫描所有有项目索引的目录，刷新对应项目 CLAUDE.md 中的 Obsidian 索引段。

**流程**：

1. **扫描项目索引目录**：
   ```bash
   find "$OBSIDIAN_REPO/wiki/projects/" -name "index.md" -type f
   ```
2. **对每个索引**：
   - 读取 index.md 的 frontmatter，提取 `project` 字段
   - 尝试在 `$HOME/jacky-github/` 下找到对应的 git 项目
   - 如果找到：读取项目 CLAUDE.md，更新 `<!-- ob-index -->` 标记区域
   - 如果未找到：跳过（项目可能不在本地）
3. **更新逻辑**（同 ob-project-log 步骤 3.5）：
   - 读取 Obsidian 索引表格
   - 生成紧凑的 CLAUDE.md 索引段
   - 替换或追加标记区域
4. **报告**：
   ```
   CLAUDE.md 索引段已刷新：
     - {project1}：{N} 篇文章
     - {project2}：{N} 篇文章
     - 跳过：{M} 个项目（未找到本地 git 仓库）
   ```

### 第四步：运行反思引擎

编译完成后自动运行两阶段反思：

**阶段 1 — 发现（仅读索引）**

读取 `$OBSIDIAN_REPO/wiki/index.md`，从单行摘要中识别：

| 发现类型 | 检测方法 |
|----------|----------|
| 跨领域主题 | 一个概念出现在多个不相关来源中 |
| 隐含关系 | 两个概念看似相关但无 wikilink |
| 矛盾 | 不同来源对同一概念持对立立场 |
| 空白 | 多来源暗示但无专门文章的主题 |

输出 3-5 个候选关联，展示给用户：

```
发现以下潜在关联：
1. [[ai/attention]] 和 [[ai/rlhf]] — 都涉及"为相关性分配标量分数"
2. [[ai/transformer]] 和 [[ai/rlhf]] — transformer 是 RLHF 的基础架构
3. 空白：缺少 "scaling laws" 概念文章（3 个来源引用但无独立文章）

是否生成综合文章？（可选择感兴趣的关联）
```

**阶段 2 — 综合（定向深度阅读）**

对用户确认的候选：
1. 读取相关文章全文
2. 如果证据充分，根据内容匹配主题目录，生成 `$OBSIDIAN_REPO/wiki/{theme}/{slug}.md`

```markdown
---
tags: [{相关标签}]
type: topic
created_by: ob-index-reflect
updated_at: {日期}
---

# {综合标题}

> 这是一篇综合文章，从已有知识中发现的新关联。

## 关联发现

{描述发现的关联或模式}

## 分析

{综合分析，建议 ≤ 500 字，超出部分通过 [[reference]] 链接补充}

## 证据
- [[{来源 1}]] — {贡献}
- [[{来源 2}]] — {贡献}

## 相关文章
- [[{文章 1}]]
- [[{文章 2}]]
```

3. 更新 index.md 在对应主题分类下追加条目
4. 追加 log.md

### 第五步：首次初始化

如果检测到 `$OBSIDIAN_REPO/raw/` 和 `$OBSIDIAN_REPO/wiki/` 不存在，执行首次初始化：

1. 创建完整目录结构（raw/、wiki/ 及子目录、outputs/）
2. 扫描 `$OBSIDIAN_REPO/` 中所有 `.md` 文件（排除 `.obsidian/`、`raw/`、`wiki/`、`outputs/`）
3. 分类现有笔记：
   - **结构化笔记**（有标题、有内容、> 100 字）→ 根据关键词匹配主题目录，复制到对应 `wiki/{theme}/`，并分配 article_id
   - **碎片笔记**（短文本、速记、< 100 字）→ 复制到 `raw/notes/`
4. 为 raw 中的文件标记 frontmatter `status: uncompiled`
5. 生成初始 `wiki/index.md`
6. 生成初始 `wiki/log.md`

**注意**：不删除或移动原始文件，只读取和复制到新目录。

### 输出

执行完成后展示：

```
处理完成：
- 新编译（由 ob-compile 处理）：{数量} 篇
- 新文章：{数量} 篇（写入对应主题目录）
- 索引更新：{数量} 条
- article_id 缺失：{数量} 篇（已自动补分配）
- CLAUDE.md 索引段刷新：{数量} 个项目

索引总计：{总文章数} 篇文章
所有 article_id 均为随机唯一 ID
```
