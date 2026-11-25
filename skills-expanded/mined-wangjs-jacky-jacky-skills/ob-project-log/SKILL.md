---
name: ob-project-log
description: "项目知识沉淀到 Obsidian。四种模式：自动沉淀（Hook）、手动沉淀、浏览追问、架构回顾（生成档案+批注+resolve 改代码）。触发词：ob-project-log、项目沉淀、追问文章、架构回顾、review init/resolve。"
---

<role>Obsidian 项目知识沉淀助手。从 AI 对话或代码库提取项目知识，支持自动沉淀、手动沉淀、浏览追问、架构回顾四种模式。</role>
<purpose>将项目知识写入 Obsidian wiki，按主题组织为活文档。支持从对话提取、从代码扫描提取、就地批注后 resolve 改代码的闭环工作流。</purpose>
<trigger>

```text
触发词：
模式一（自动沉淀）：由 Stop Hook 自动触发，无需手动调用
模式二（手动沉淀）：ob-project-log / 项目沉淀 / 记录到项目 / 沉淀对话
模式三（浏览追问）：追问文章 / 继续讨论 / 优化笔记 / 项目追问 / 追问
模式四（架构回顾）：架构回顾 / 项目回顾 / review init / review resolve / 生成架构档案

示例：
- "ob-project-log"
- "把这次对话沉淀到项目"
- "追问文章" → 列出文章 → 选择 → 追问优化
- "架构回顾" / "review init" → 扫描代码 → 生成 architecture-flow.md + decisions.md
- "review resolve" → 扫描批注 → 列出 → 确认 → 批量改代码 + 更新档案
```

</trigger>
<gsd:workflow xmlns:gsd="urn:gsd:workflow">
  <gsd:meta>requires=OBSIDIAN_REPO</gsd:meta>
  <gsd:goal>四种模式：自动沉淀、手动沉淀、浏览追问、架构回顾，将项目知识写入 Obsidian 并支持就地批注后 resolve 闭环。写入后自动更新项目 CLAUDE.md 索引段。</gsd:goal>
  <gsd:phase>模式判断：Hook → 自动沉淀；"追问/继续讨论" → 浏览追问；"架构回顾/review init/resolve" → 架构回顾；其他 → 手动沉淀。</gsd:phase>
  <gsd:phase>自动/手动沉淀：识别项目 → 分析对话 → 提取知识 → 匹配/创建文件 → 写入更新 → 更新 CLAUDE.md 索引段。</gsd:phase>
  <gsd:phase>浏览追问：列出文章 → 用户选择 → 读取全文 → 追问循环 → 更新文章 → 更新 CLAUDE.md 索引段。</gsd:phase>
  <gsd:phase>架构回顾：init 派 Explore 扫码生成档案+建软链；用户在 Obsidian 用 [!review] 批注；resolve 列出批注+确认+派 sub-agent 批量处理（改文档/改代码/给推理）。</gsd:phase>
</gsd:workflow>

# Obsidian 项目知识沉淀 (ob-project-log / 项目沉淀)

## 做什么

把项目知识写入 Obsidian wiki，按主题组织为活文档。支持四种模式：

| 模式 | 知识来源 | 主要动作 |
|------|---------|----------|
| 一·自动沉淀 | 对话 | Hook 触发，静默写入 |
| 二·手动沉淀 | 对话 | 用户触发，输出摘要 |
| 三·浏览追问 | 对话 + 已有文章 | 选文章 → 追问 → 更新 |
| 四·架构回顾 | **代码库** | 扫码生成档案 → 用户批注 → resolve 改代码 |

模式四是闭环工作流（详见 [references/architecture-review-guide.md](references/architecture-review-guide.md)），其他三种是单向沉淀。

## 配置检查

**【硬约束】仓库路径一律委托 ob-router skill 解析，本 skill 不自行读取路径文件。**

调用 ob-router skill 获取 `$OBSIDIAN_REPO`：
- ob-router 内部处理优先级（ob-router.json → CLAUDE.md → 询问）
- 若 ob-router.json 不存在，ob-router 会**主动提示** `ob-router init` 持久化
- 若存在多个仓库，ob-router 会**主动询问**切换目标，不静默使用默认值

将 ob-router 返回的路径保存为 `$OBSIDIAN_REPO`，后续全程使用此变量。

## 项目路径解析

**核心问题**：不同类型的项目，Obsidian wiki 目录不同。必须先检测项目类型，再确定写入路径。

### 检测流程（按优先级）

1. **检查 CLAUDE.md 已有索引路径**：如果 `<!-- ob-index:start -->` 区域内已有 `> 索引路径：` 行，直接使用该路径
2. **检查 `.study-meta.json`**：如果项目根目录存在此文件且包含 `"managedBy": "repo-study"`，判定为 repo-study 项目
3. **检查目录名后缀**：如果项目目录名以 `-study` 结尾，且 `$OBSIDIAN_REPO/wiki/open-source/{project-name}/` 存在，判定为 repo-study 项目
4. **模糊搜索已有目录**：在 `$OBSIDIAN_REPO/wiki/` 下搜索与项目名匹配的目录
5. **以上都不匹配**：默认为开发项目

### 路径规则

| 项目类型 | 检测条件 | Wiki 路径 | 示例 |
|----------|---------|-----------|------|
| **repo-study 项目** | `.study-meta.json` 存在，或目录名以 `-study` 结尾且在 `open-source/` 下有对应目录 | `$OBSIDIAN_REPO/wiki/open-source/{project-name}/` | `wiki/open-source/codex-plugin-cc-study/` |
| **开发项目** | 其他 | `$OBSIDIAN_REPO/wiki/projects/{project-name}/` | `wiki/projects/CodeIsland/` |

### 使用约定

文档中所有 `$WIKI_PATH` 指代根据上述规则解析后的项目 wiki 目录路径。路径末尾无 `/`。

```
$WIKI_PATH = $OBSIDIAN_REPO/wiki/open-source/{project}    # repo-study
$WIKI_PATH = $OBSIDIAN_REPO/wiki/projects/{project}        # 开发项目
```

## 模式判断

根据触发方式自动判断模式：

| 触发方式 | 模式 | 行为 |
|----------|------|------|
| Stop Hook 自动触发 | **自动沉淀** | 分析对话，提取知识，静默写入 |
| "项目沉淀" / "记录到项目" / "ob-project-log" | **手动沉淀** | 同上，但输出详细摘要 |
| "追问文章" / "继续讨论" / "优化笔记" / "项目追问" | **浏览追问** | 列出文章，选择后进入追问循环 |
| "架构回顾" / "项目回顾" / "review init" / "生成架构档案" | **架构回顾·init** | 派 Explore sub-agent 扫码 → 生成 architecture-flow.md + decisions.md → 建项目软链 |
| "review resolve" / "处理批注" / "resolve 架构回顾" | **架构回顾·resolve** | 扫描 `> [!review]` 批注 → 列出确认 → TeamCreate 批量派单 → 改文档/改代码 |

---

## 模式一：自动沉淀（Hook 触发）

Stop Hook 在每次对话结束时自动触发，Claude 执行以下流程：

### 1. 检测环境

- 当前目录是否在 git 项目中
- `$OBSIDIAN_REPO` 是否已配置
- 两者都满足才继续

### 2. 分析对话

判断本次对话是否包含值得沉淀的项目知识：

**值得沉淀的信号**：
- 讨论了项目架构、模块划分、数据流
- 做了技术选型或方案决策
- 踩了坑并找到了解决方案
- 发现了设计规范或最佳实践
- 提出了改进计划或未来展望

**不需要沉淀的信号**：
- 纯闲聊或无结论讨论
- 临时调试命令（无长期价值）
- 已经沉淀过的重复内容
- 仅涉及文件编辑/创建（无知识增量）

### 2.5 读取质量偏好

如果 `$OBSIDIAN_REPO/wiki/.rating-preferences.md` 存在：
1. 读取偏好文件，提取核心偏好规则
2. 在后续提取和写入时参考这些规则：
   - 内容需要有深度和干货（非表面介绍）
   - 标题需准确反映内容
   - 文章间应互相串联（使用 [[wikilinks]]）
   - 包含 reference/相关链接
   - 其他偏好规则作为写作质量指引
3. 不存在则跳过，使用默认标准

### 3. 提取与写入

- 按维度提取内容（参考 [references/study-dimensions.md](references/study-dimensions.md)）
- **涉及具体代码时**：生成 code-ref callout 引用，不嵌入代码片段（参考 [references/code-ref-format.md](references/code-ref-format.md)）
- **质量规范**：判断文章类型，按 [references/writing-quality.md](references/writing-quality.md) 对应类型标准写入
- 提取 git remote URL 生成 GitHub 链接（`git remote get-url origin` → 提取 `owner/repo`）

**索引加速匹配**：在匹配已有文件前，先检查 `index.md`：
1. 读取 `$WIKI_PATH/index.md`
2. 如果存在：从索引表格中查找主题匹配的文件，无需全量读取所有文件
3. 如果不存在：fallback 到原有逻辑（ls 目录 + 逐个读取文件），并在写入完成后创建索引

- 匹配已有文件或新建文件
- 追加/合并内容，不覆盖

**新建文件的 frontmatter 模板**（必填）：
```yaml
---
article_id: OBA-{随机8位}
tags: [{项目名}, {主题标签}]
type: {预定义类型}    # concept/tutorial/troubleshooting/reference/note
updated_at: {YYYY-MM-DD}
created_at: {YYYY-MM-DD}
source: conversation
---
```

**article_id 分配规则**（随机生成，无状态）：
1. 生成方式：`OBA-` + 8位随机小写字母数字
2. 生成命令：`python3 -c "import random,string; print(''.join(random.choices(string.ascii_lowercase+string.digits,k=8)))"`
3. 生成后验证唯一性：`grep -rh "OBA-{生成的ID}" "$OBSIDIAN_REPO/wiki/" --include="*.md"`，如果已存在则重新生成
4. 已有文章更新时**不修改** article_id
5. ID 一旦分配即永久绑定，即使文章被删除，该 ID 也不会被复用

**写入后验证**（遵循 [frontmatter-schema](references/frontmatter-schema.md)）：
1. **Frontmatter**：确认 article_id、tags（非空）、type（预定义值）、updated_at 存在
2. **Wikilink**：扫描 `[[xxx]]` 引用，确认目标文件存在
3. **索引一致性**：确认新文件已出现在 `index.md` 表格中
4. **交叉引用**：在同目录已有文章中查找相关主题，添加 `[[新文章名]]` 反向链接

**更新索引**：写入完成后，同步更新 `index.md`（格式见下方"索引机制"章节）

### 3.5 更新项目 CLAUDE.md 索引段

写入文章后，自动更新项目 CLAUDE.md 中的 Obsidian 索引段（格式参考 [references/claude-index-format.md](references/claude-index-format.md)）。

**流程**：

1. **获取项目 git 根目录**：`git rev-parse --show-toplevel`
2. **查找 CLAUDE.md**：`{git_root}/CLAUDE.md`
3. **发现 Obsidian 索引路径**（按优先级）：
   - 读取 CLAUDE.md 中已有的 `<!-- ob-index:start -->` 标记内的路径
   - 精确匹配：`$WIKI_PATH/index.md`
   - 模糊搜索：在 `$OBSIDIAN_REPO/wiki/` 下搜索 frontmatter 含 `project: {project_name}` 的 index.md
   - 目录名匹配：`find "$OBSIDIAN_REPO/wiki/" -type d -name "*{project}*"`
4. **读取 Obsidian 索引**：解析 index.md 表格中的文件名和主题
5. **生成 CLAUDE.md 索引段**：
   - 表格列：文件 | 主题 | 何时读取
   - "何时读取" 基于主题和涵盖维度自动推导
6. **写入 CLAUDE.md**：
   - 已有 `<!-- ob-index:start -->` 标记 → 替换标记区域内容
   - 已有旧的手动 "Obsidian 知识库" 部分（无标记）→ 替换为标记区域
   - 都没有 → 在 CLAUDE.md 末尾追加标记区域

**跳过条件**：
- 项目不在 git 仓库中
- CLAUDE.md 不可写
- 未找到对应的 Obsidian 索引文件

### 4. 创建标记文件

无论是否有内容沉淀，都创建标记文件防止 Hook 死循环：

```bash
echo $(date +%s) > /tmp/ob-project-log-synced-$PPID
```

### 5. 简短告知

```
📝 已自动沉淀到 {wiki_relative_path}（{N} 条更新）
```

**无有价值内容时**：
```
本次对话无需沉淀（未发现项目知识增量）
```

### 6. 偏好自学习

沉淀完成后（无论是否有内容写入），分析本次对话中的偏好信号并更新 `$OBSIDIAN_REPO/wiki/.rating-preferences.md`：

1. 扫描对话，识别以下偏好信号：
   - 用户对文章内容做了修改/调整（说明偏好某种写法）
   - 用户要求补充或删除某些内容（反映质量偏好）
   - 用户对结构、格式、深度表达了满意或不满
   - 用户主动提到"我喜欢/不喜欢"某种风格
2. 如果发现新的偏好信号，追加到 `.rating-preferences.md` 的**偏好规则**部分：
   - 新增规则用 `###` 标题 + 规则内容
   - 标注 `(auto-learned {date})` 标记来源
3. 如果已有规则在本次对话中被验证或强化，更新其 `支撑` 描述
4. 无新偏好信号时跳过，不修改文件

---

## 模式二：手动沉淀

与自动沉淀逻辑相同，但由用户主动触发，增加以下交互：

### 1. 识别项目

```
CLAUDE.md 已有索引路径 → .study-meta.json → 目录名 -study 后缀 → 模糊搜索 → 询问用户
```

按"项目路径解析"章节确定 `$WIKI_PATH`。

### 2. 提取内容

如果 `$OBSIDIAN_REPO/wiki/.rating-preferences.md` 存在，先读取偏好规则作为内容质量指引。

分析当前对话，按 [references/study-dimensions.md](references/study-dimensions.md) 中的维度提取有价值内容。

每个内容块包含：
- **维度**：属于哪个知识维度（架构设计、核心机制、设计规范等）
- **主题**：具体讲什么（如"插件架构"、"错误处理规范"）
- **内容**：核心知识，简洁精准
- **代码引用**（如适用）：当对话涉及具体代码文件时，生成 code-ref callout

**提取标准**：只取有长期参考价值的内容。闲聊、临时调试、重复内容不取。

**代码处理规则**（详见 [references/code-ref-format.md](references/code-ref-format.md)）：
- 对话中讨论了具体代码文件/函数/类 → 生成 `> [!code-ref]` callout
- code-ref 包含：简要描述、仓库路径 + 行号、GitHub 链接、设计意图
- **不嵌入代码片段**，只保留文字描述 + code-ref 引用
- 短配置片段（JSON/YAML，< 5 行且不太变化）可内联，不需要 code-ref

### 3. 匹配或创建文件

**索引加速匹配**：先读取 `$WIKI_PATH/index.md`：
1. 如果索引存在：从索引表格中查找主题匹配的文件，无需全量读取
2. 如果索引不存在：fallback 到原有逻辑（ls 目录 + 逐个读取文件内容），并在写入完成后创建索引

对每个内容块：

- 已有文件主题匹配 → 追加到该文件对应位置
- 无匹配文件 → 新建 `{slug}.md`，slug 从主题生成（短英文+连字符）

**不预设固定文件名**，完全根据对话内容动态决定。

**更新索引**：写入完成后，同步更新 `index.md`（格式见下方"索引机制"章节）

**更新项目 CLAUDE.md 索引段**：与自动沉淀模式 3.5 相同，写入后自动更新项目 CLAUDE.md 中的 Obsidian 索引段（参考 [references/claude-index-format.md](references/claude-index-format.md)）。

### 4. 写入规则

#### 基本规则

- **不覆盖**：已有内容保留，新内容追加或合并
- **去重**：相同主题合并，不重复
- **敏感信息**：API key、密码、token → `{REDACTED}`
- **简洁**：每条点到为止

#### 代码引用

涉及具体代码时使用 code-ref callout，格式见 [references/code-ref-format.md](references/code-ref-format.md)：
```
> [!code-ref] {描述}
> **仓库**: {repo} | **路径**: `{path}:{line_start}-{line_end}`
> 🔗 [GitHub]({github_url}#L{start}-L{end})
>
> {设计意图}
```

#### 质量规范（必须遵循）

写入前判断文章类型，按 [references/writing-quality.md](references/writing-quality.md) 中对应类型的标准执行：

| 类型 | 触发信号 | 必填要素 |
|------|----------|----------|
| **概念/分析** | 架构、原理、对比 | 独到视角 + 关键论点有 code-ref 支撑 + 底部参考 |
| **操作指南** | 安装、配置、教程 | 前置条件 + 编号步骤 + 代码示例 + 常见问题 |
| **踩坑记录** | Bug、兼容性、意外行为 | 症状 + 根因 + 方案 + 预防 |
| **决策记录** | 选型、方案取舍 | 背景 + 备选方案 + 对比 + 选择理由 |

**质量底线**：文章必须通过 [质量自检清单](references/writing-quality.md)，不达标的先补充再写入。

### 5. 输出摘要

```
📝 已沉淀到 {wiki_relative_path}

更新：
  - {filename}.md  → {做了什么}
  - {filename}.md  → {做了什么}（新建）
```

### 6. 偏好自学习

与自动沉淀模式 6 相同：分析本次对话中的偏好信号，更新 `.rating-preferences.md`。

---

## 浏览追问与索引联动

执行以下任务前，必须读取 [references/browse-and-index.md](references/browse-and-index.md)：

- 浏览项目文章并进入追问循环
- 将追问结论回写原文章
- 创建或更新 `index.md`、`article_id`
- 维护项目 `CLAUDE.md` 的 Obsidian 知识索引段

## 模式四：架构回顾（review init / resolve）

**完整流程详见 [references/architecture-review-guide.md](references/architecture-review-guide.md)**，本章只列入口和核心约束。

### 子命令

| 子命令 | 触发词 | 作用 |
|--------|--------|------|
| `init` | "架构回顾"、"项目回顾"、"review init"、"生成架构档案" | 派 Explore sub-agent 扫描代码 → 生成两份档案 → 项目根建软链 |
| `resolve` | "review resolve"、"处理批注"、"resolve 架构回顾" | 扫描批注 → **列出让用户勾选** → TeamCreate 批量派单 → 改文档/改代码 |
| `status` | "review status"、"查看批注" | 列出当前所有未处理的 `[!review]` 批注，不执行 |

### 产出文件（真文件在 Obsidian，项目根软链）

| 文件 | 真文件路径 | 项目根软链 |
|------|-----------|-----------|
| 架构流水线 | `$WIKI_PATH/architecture-flow.md` | `{project-root}/ARCHITECTURE.md` |
| 决策清单 | `$WIKI_PATH/decisions.md` | `{project-root}/DECISIONS.md` |

源文件锚点 ID 规则：流水线步骤 `F-001/F-002/...`，决策点 `D-001/D-002/...`，永久绑定不复用。

### 批注语法（Obsidian Callout）

用户在档案中任意位置写：

```markdown
> [!review] 可选标题
> 我想把豆包换成 macOS say 当 fallback
> 不要为了便宜牺牲稳定性
```

支持的批注类型（用 `[!review:类型]` 显式标注，未标注由 resolve 阶段自动判定）：

| 类型 | 含义 | resolve 行为 |
|------|------|-------------|
| `[!review:clarify]` | 看不懂，要补充说明 | 改文档（追加补充内容） |
| `[!review:modify]` | 要改代码 | 产出 diff 让用户确认后 apply |
| `[!review:challenge]` | 质疑决策，想要论证 | 给推理回应，写入档案，不改代码 |
| `[!review]`（无类型） | 由 resolve 阶段根据内容自动分类 | 同上对应类型 |

### 核心约束

1. **resolve 必须先列后改**：扫描出所有批注后，先用编号列表展示，让用户勾选要处理的项再派单
2. **代码改动必须二次确认**：teammate 产出 diff，主会话展示给用户确认后才 apply
3. **resolve 完成后清理批注**：成功处理的 `[!review]` 块从档案中删除，未处理的保留
4. **软链幂等**：init 重复执行时，已存在的软链跳过；档案存在时增量更新（保留 `[!review]` 块）

---

## 异常处理

| 场景 | 处理 |
|------|------|
| OBSIDIAN_REPO 未配置 | 询问用户 |
| 项目识别失败 | 询问用户 |
| 目录不存在 | 自动创建 |
| 对话无有价值内容 | 自动沉淀模式不操作；手动模式告知用户 |
| 追问模式无匹配文章 | 提示用户先沉淀，或创建新文章 |
| 追问模式目录为空 | 提示先使用手动沉淀创建内容 |
| Hook 触发但非 git 项目 | 跳过，不执行任何操作 |
| `index.md` 不存在 | fallback 到原有逻辑（ls + 逐个读取），完成后自动创建索引 |
| `index.md` 损坏或格式异常 | 忽略索引，fallback 到原有逻辑，下次写入时重建索引 |
| 索引与实际文件不一致 | 以实际文件为准，更新索引 |
| review init 时档案已存在 | 增量更新：保留所有 `[!review]` 批注块，仅刷新自动生成内容 |
| review resolve 时无批注 | 提示"无待处理批注"并退出 |
| review resolve 时项目根软链丢失 | 重建软链后继续 |
| review init 时项目根已有同名实体文件（非软链） | 报警提示并跳过软链创建，避免覆盖 |
