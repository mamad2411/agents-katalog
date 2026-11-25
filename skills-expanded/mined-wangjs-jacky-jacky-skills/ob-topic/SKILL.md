---
name: ob-topic
description: "对话中快速收藏通用知识点到 Obsidian 知识库。触发词：/save、/collect、收藏、记录一下、ob-topic。"
---

<role>Obsidian 知识点快速收藏助手。从对话上下文中提取知识点，精炼概括后保存到 Obsidian wiki 主题目录。写入后自动更新项目 CLAUDE.md 的 Obsidian 索引段。</role>
<purpose>两种模式：1) 手动触发：用户说触发词 + 知识点描述，立即收藏；2) 自动提醒：对话中识别到通用知识点时主动询问是否收藏。写入后同步更新项目 CLAUDE.md。</purpose>
<trigger>

```text
触发词：
- /save / /collect / 收藏 / 记录一下 / ob-topic
- 把这个收藏 / 保存到知识库 / 记录一下这个知识点
- 新增 topic / 新建 topic / 创建 topic

示例：
- "/save React Server Components 的流式渲染原理"
- "收藏一下：Tauri Sidecar 的启动流程"
- "记录一下：Node.js SEA 编译的局限性"
- "新增一个 topic hermes"
- "新建 topic crypto 关于加密货币"
- "创建 topic rust，收藏 Rust 所有权机制"
```

</trigger>

# Obsidian 知识点收藏 (ob-topic)

## 配置检查

**执行前必读**：本 skill 需要使用 Obsidian 仓库路径。

**【硬约束】仓库路径一律委托 ob-router skill 解析，本 skill 不自行读取路径文件。**

调用 ob-router skill 获取 `$OBSIDIAN_REPO`：
- ob-router 内部处理优先级（ob-router.json → CLAUDE.md → 询问）
- 若 ob-router.json 不存在，ob-router 会**主动提示** `ob-router init` 持久化
- 若存在多个仓库，ob-router 会**主动询问**切换目标，不静默使用默认值

将 ob-router 返回的路径保存为 `$OBSIDIAN_REPO`，后续全程使用此变量。

## 收藏流程

### 1. 提取内容

- 从用户触发词描述中提取知识点
- 检查当前对话上下文是否有相关讨论内容，有则一并提取
- 精炼概括，核心内容 ≤ 500 字

### 2. 主题分类

优先检测用户是否指定了 topic，再走自动匹配逻辑。

#### 2a. 用户指定 topic（优先）

解析用户输入，检测以下意图模式：

- "新增 topic xxx" / "新建 topic xxx" / "创建 topic xxx"
- "新增一个 topic xxx" / "新建一个 topic xxx"
- "topic xxx 关于 yyy"

**处理方式**：
1. 提取 topic 名称（如 `hermes`、`crypto`、`rust`）
2. 转为英文短横线命名作为目录名（如 `wiki/hermes/`、`wiki/crypto/`）
3. 标记为 **新 topic**，后续执行 Step 2.5 创建目录
4. 如果用户同时提供了知识点内容（如"创建 topic rust，收藏 Rust 所有权机制"），继续走 Step 3 写入笔记

**注意**：如果用户指定的 topic 名称与已有分类表中的目录重名（如 `ai`、`claude`），直接使用已有目录，不重复创建。

#### 2b. 自动匹配（无 topic 指定时）

根据知识点关键词自动匹配主题目录：

| 主题 | 目录 | 关键词 |
|------|------|--------|
| AI 技术 | `wiki/ai/` | AI, LLM, GPT, transformer, 机器学习, 深度学习, RAG, agent |
| Claude 生态 | `wiki/claude/` | Claude, Claude Code, Skills, MCP, hooks, Subagents |
| Tauri | `wiki/tauri/` | Tauri, 桌面应用, tauri-app, Sidecar, invoke |
| 开发工具 | `wiki/dev-tools/` | VSCode, IDE, 编辑器, CLI, 终端, Git, Zed |
| 前端开发 | `wiki/front-end/` | React, JavaScript, TypeScript, CSS, 前端, Next.js, Vue |
| 时事分析 | `wiki/current-affairs/` | 经济, 政治, 国际, 金融, 投资, 时事 |
| 职业发展 | `wiki/career/` | 职级, 面试, 求职, 职业规划, 大厂 |
| Obsidian | `wiki/obsidian/` | Obsidian, 知识管理, 笔记, 双链 |
| 最佳实践 | `wiki/best-practice/` | 使用习惯, 效率技巧, 工具推荐, 插件体验, 工作流, 快捷键, 软件配置, 使用心得 |

无匹配时自动创建新主题目录（kebab-case 英文命名）。

匹配后直接使用，不询问用户确认（全自动模式）。

### 2.5 创建新 topic 目录（仅 Step 2a 触发时执行）

当确定为新 topic 时，执行以下步骤：

1. **检查目录是否已存在**：
   ```bash
   ls "$OBSIDIAN_REPO/wiki/{topic-name}/"
   ```
   如果已存在，跳过创建，直接使用。

2. **创建目录**：
   ```bash
   mkdir -p "$OBSIDIAN_REPO/wiki/{topic-name}/"
   ```

3. **创建 index.md**，格式如下：
   ```markdown
   ---
   tags: [{topic-name}, index]
   type: index
   updated_at: {YYYY-MM-DD}
   ---

   # {Topic 显示名}

   > {一句话描述，来自用户输入或从上下文推断}

   ## 文章列表

   <!-- 后续文章会自动追加到这里 -->
   ```

4. **更新 wiki/index.md 全局索引**，在合适位置（按字母顺序或末尾）添加：
   ```markdown
   - [[{topic-name}/index|{Topic 显示名}]] — {一句话描述}
   ```
   如果 `wiki/index.md` 不存在，不创建（由 ob-index skill 统一管理）。

### 3. 写入笔记

文件名：`{slug}.md`，slug 用英文短横线连接。

**分配 article_id**：

在写入前，为新文章分配全局唯一的 article_id（格式 `OBA-{8位随机小写字母数字}`，如 `OBA-k7jm2p9q`）。分配方式：

```bash
# 生成随机 ID（8位小写字母+数字）
python3 -c "import random,string; print(''.join(random.choices(string.ascii_lowercase+string.digits,k=8)))"
```

- 生成后验证唯一性：
  ```bash
  grep -rh "OBA-{生成的ID}" "$OBSIDIAN_REPO/wiki/" --include="*.md"
  ```
  无结果则 ID 唯一，可使用；否则重新生成

```markdown
---
tags: [{主题标签}, {关键词}]
type: {预定义类型}
article_id: OBA-{随机8位}
created_at: {YYYY-MM-DD}
source: conversation
---

# {知识点标题}

> 从对话中整理 · {主题分类}

## 核心内容

{精炼概括，≤ 500 字}

## 关键要点

1. {要点一}
2. {要点二}
3. {要点三}
```

**type 选择规则**（必须遵循 [frontmatter-schema](references/frontmatter-schema.md)）：

| 内容性质 | type |
|---------|------|
| 解释技术概念/术语 | `concept` |
| 教程/操作步骤 | `tutorial` |
| 问题排查/踩坑 | `troubleshooting` |
| 学习记录 | `learning` |
| 参考/对比/速查 | `reference` |
| 其他 | `note` |

### 4. 写入后验证

遵循 [frontmatter-schema](references/frontmatter-schema.md) 中的验证清单：
1. **Frontmatter**：确认 tags（非空）、type（预定义值）、updated_at 存在
2. **Wikilink**：扫描 `[[xxx]]` 引用，确认目标文件存在
3. **索引**：确认文章已出现在对应 index.md
4. **交叉引用**：在同目录已有文章中查找 tags 重叠的文章，添加 `[[新文章名]]` 反向链接

### 5. 更新索引

- 更新 `wiki/{theme}/index.md`：追加新条目到对应分类下
- 新主题目录时创建 `wiki/{theme}/index.md`（Step 2.5 已处理，此处验证即可）
- 新主题分类时更新 `wiki/index.md` 全局索引（Step 2.5 已处理，此处验证即可）
- **对新 topic**：确认 `wiki/{topic-name}/index.md` 存在且包含新文章条目；确认 `wiki/index.md` 已包含该 topic 的链接

### 5.5 更新项目 CLAUDE.md 索引段

写入完成后，如果当前在 git 项目中，自动更新项目 CLAUDE.md 中的 Obsidian 索引段。流程参考 [ob-project-log/references/claude-index-format.md](../ob-project-log/references/claude-index-format.md) 中的"共享更新流程"。

**注意**：ob-topic 写入的内容在主题目录（wiki/{theme}/），不一定有项目级索引。更新会静默跳过，不影响主流程。如果用户已为当前项目建立了 Obsidian 项目索引，则同步更新 CLAUDE.md。

### 6. 返回结果

简短返回：文件路径、主题分类、标题。

## 与其他 skill 的区别

| 维度 | ob-topic | ob-collect | ob-project-log |
|------|----------|------------|----------------|
| 来源 | 对话上下文 | 外部 URL/视频/PDF | 对话上下文（项目相关） |
| 绑定 | 不绑定项目 | 不绑定项目 | 绑定 git 项目 |
| 触发 | 手动 + 自动提醒 | 手动 | Stop hook 自动 |
| 目标 | wiki/{theme}/ | raw/ → wiki/{theme}/ | wiki/projects/{project}/ |
