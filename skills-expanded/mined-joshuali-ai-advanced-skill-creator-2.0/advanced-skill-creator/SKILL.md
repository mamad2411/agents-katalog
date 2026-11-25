---
name: advanced-skill-creator
description: "ASC (Advanced Skill Creator) 是一个元技能，用于创建能够持续学习和进化的 AI 技能。当用户需要以下操作时触发：从专业参考文件（模板、playbook、实践指南）中提取结构化知识，从实际工作定稿中逆向提炼经验，构建一个能在日常工作中自主积累经验并越来越好的技能，或者将专业领域的隐性知识转化为可复用的 AI 工作流。触发关键词包括：'创建技能'、'建技能'、'教会AI'、'从我的工作中学习'、'提取知识框架'、'建立经验库'、'让AI学会做XX'。即使用户只是说'帮我做一个能起草合同的AI助手'，也应当触发本技能。"
---

# Advanced Skill Creator (ASC)

## 核心定位

ASC 是一个**元技能（Meta-Skill）**，专门用于帮助用户创建能持续学习和进化的专业 AI 技能。

ASC 的职责边界：
- **ASC 负责：** 设计技能结构、从参考资料中提取知识、从历史项目中提取经验、为技能注入持续学习机制
- **ASC 不负责：** 直接参与终端用户的实际工作流程（这是 ASC 创建的子技能的职责）

ASC 的最终产出物是一套完整的技能文件结构，由用户部署后独立运行。

---

## 阶段模型

ASC 严格按照四个阶段顺序执行。每个阶段完成后，必须输出对应产出物并请求用户确认，确认后方可进入下一阶段。

| 阶段 | 名称 | 目的 | 核心产出物 | 执行时机 |
|---|---|---|---|---|
| Stage 1 | 初创 | 确定技能的名称、目的、功能和适用场景 | `SKILL.md` 主文件 + 完整文件框架 | ASC 运行时 |
| Stage 2 | 初学者 | 从参考模板和 Playbook 中提取知识框架 | `KNOWLEDGEMAP.md` + `Reference/` | ASC 运行时 |
| Stage 3 | 实习 | 从实际工作文件中提取经验并建立链接 | `EXPERIENCELOG.md` + `Archives/` | ASC 运行时 |
| Stage 4 | 实际工作 | 知识/经验调用 + 持续学习闭环 | *注入子技能 SKILL.md 的运行时指令* | 子技能运行时 |

**关于 Stage 4 的特殊说明：** Stage 4 不是 ASC 自身的工作阶段，而是 ASC 在 Stage 1 就写入子技能 `SKILL.md` 中的运行时指令。子技能部署后，这些指令驱动子技能在实际工作中自主积累经验。此处按逻辑顺序排列在第四阶段，但其内容在 Stage 1 就已植入。

---

## Stage 1：初创

### 进入条件
用户要求创建新技能，或 ASC 被触发后尚未完成 Stage 1。

### 执行流程

**Step 1 — 需求访谈**

通过对话逐步明确以下信息（不要一次性询问所有问题，根据用户回答自然推进）：

1. **技能目标：** 这个技能要帮用户做什么？（例如：起草股权转让协议、审阅合规文件、准备尽职调查清单）
2. **适用场景：** 在什么情况下应该触发这个技能？用户通常会说什么来启动它？
3. **输出格式：** 技能的工作成果是什么形式？（.docx 文件、markdown 报告、结构化清单等）
4. **输出路径：** 用户希望子技能安装到哪个位置？（每次询问用户指定）
5. **专业领域：** 这个技能涉及哪个专业领域？这会影响后续 Stage 2/3 的知识和经验提取策略
6. **领域专属变量：** 根据领域特点，预定义该技能需要记录的关键变量（例如 SPA 技能可能需要：谈判地位、法域、行业、交易规模、风险偏好）

**Step 2 — 确认理解**

将访谈结果整理为结构化摘要，请求用户确认：

```
技能名称：[name]
技能目标：[purpose]
触发场景：[triggers]
输出格式：[format]
安装路径：[path]
专业领域：[domain]
领域变量：[variables list]
```

**Step 3 — 生成技能框架**

用户确认后，执行以下操作：

1. 在用户指定的路径下创建完整的子技能文件结构：
   ```
   {skill_name}/
   ├── SKILL.md              # 基于 templates/CHILD_SKILL_TEMPLATE.md 生成
   ├── KNOWLEDGEMAP.md       # 空模板，Stage 2 填充
   ├── EXPERIENCELOG.md      # 空模板，Stage 3 填充
   ├── Reference/            # 空目录，Stage 2 存放参考文件
   └── Archives/             # 空目录，Stage 3 存放工作文件
   ```

2. 子技能的 `SKILL.md` 必须包含：
   - YAML frontmatter（name、description）
   - 技能概述和工作流程
   - **知识与经验调用机制**（Stage 4 的三级检索优先级逻辑——此内容在 Stage 1 就植入）
   - **持续学习机制占位区**（Phase 4 完成后由 ASC 填充完整逻辑）
   - 文件结构说明
   - 行为规则（相对路径强制、双链语法、信息不足时提问）

3. 所有模板文件位于 ASC 自身的 `templates/` 目录下。生成时读取模板并替换占位符。

**Step 4 — 交付确认**

向用户展示已创建的文件结构，并说明：
- 当前 `KNOWLEDGEMAP.md` 和 `EXPERIENCELOG.md` 为空模板，将在 Stage 2 和 Stage 3 填充
- 子技能 `SKILL.md` 中的"持续学习机制"部分为占位区，将在 Phase 4 完善
- 下一步（Stage 2）需要用户提供参考模板和/或 Playbook

获得用户确认后，Stage 1 完成。

---

## Stage 2：初学者

> **深度参考：** `references/stage2_knowledge.md` 包含完整的格式规范、质量检查清单和增量更新机制

### 进入条件
Stage 1 已完成并经用户确认。

### 执行流程

**Step 1 — 接收与存档参考文件**

1. 用户提供参考文件（模板、Playbook、实践指南）。支持格式：.docx、.pdf、.md、.txt
2. 将文件复制至子技能的 `Reference/` 目录，保持原文件名
3. 如果用户分批提供文件，支持增量式知识提取（在已有 KNOWLEDGEMAP.md 基础上追加）

**Step 2 — 解析参考文件**

调用 `scripts/knowledge_extractor.py parse` 将参考文件转换为结构化文本：
```bash
python scripts/knowledge_extractor.py parse \
  --input ./Reference/Template.docx ./Reference/Playbook.pdf \
  --output ./parsed_references.md
```
解析器会保留标题层级结构（Word 的 Heading 样式 → Markdown `#` 层级），这对后续知识节点的层级映射至关重要。

**Step 3 — 结构化知识提取（LLM 执行）**

阅读解析后的文本，按以下策略提取知识框架：

- 按文档章节结构，为每个主要章节创建一个知识节点
- 每个节点包含：`section_id`（KN-XXX）、`section_name`、`core_rule`（≤80字骨架概括）、`keywords`（3-5个）、`rule_type`（mandatory/recommended/conditional）、`source_refs`（`[[Reference/文件名#标题]]` 格式）
- 可嵌套一层子节点（如 KN-002-a）
- 一份 30-50 页文件理想产出 15-25 个顶级节点
- 输出为 JSON 格式，保存至临时文件

**Step 4 — 生成 KNOWLEDGEMAP.md**

调用 `scripts/knowledge_extractor.py generate` 将提取的 JSON 转换为 Markdown：
```bash
python scripts/knowledge_extractor.py generate \
  --input ./extracted_knowledge.json \
  --domain "领域名称" \
  --sources "./Reference/Template.docx" "./Reference/Playbook.pdf" \
  --output ./KNOWLEDGEMAP.md
```

**Step 5 — 用户审阅与迭代**

1. 向用户展示知识框架概要（所有顶级节点的 section_name + core_rule）
2. 建议用户审阅：是否有遗漏？概括是否准确？关键词是否覆盖日常用语？粒度是否合适？
3. 根据反馈迭代（新增节点/修改节点/补充参考文件）
4. 用户确认满意后，Stage 2 结束

**Step 6 — 质量自检**

完成前验证：所有 [[wikilink]] 指向实际存在的 Reference/ 文件、core_rule 均 ≤80 字、每个节点至少 3 个关键词、"关联经验"字段为空（等待 Stage 3）、文件全部使用相对路径。
可调用 `scripts/knowledge_extractor.py validate` 自动检查链接有效性。

### 核心产出物
- `KNOWLEDGEMAP.md`：结构化知识地图（含 YAML frontmatter 和 [[wikilink]] 链接）
- `Reference/` 目录中的参考文件原件
- 知识节点与参考文件具体段落之间的精准链接

---

## Stage 3：实习

> **深度参考：** `references/stage3_experience.md` 包含对话策略、变量字典设计、去重/冲突处理机制和质量检查清单

### 进入条件
Stage 2 已完成并经用户确认。

### 执行流程

**Step 1 — 接收与归档工作文件**

1. 用户提供 3-5 份实际工作中产生的最终版本文件
2. 将文件复制至子技能的 `Archives/` 目录
3. 调用 `scripts/knowledge_extractor.py parse` 将文件转换为可阅读的纯文本

**Step 2 — ASC 预分析**

在向用户提问之前，先独立审阅工作文件：
- 将文件内容与 `KNOWLEDGEMAP.md` 比对，标记匹配的知识节点
- 识别与"标准做法"不同的处理方式（这些通常是最有价值的经验点）
- 识别知识框架中未覆盖的新内容
- 基于预分析结果形成针对性提问清单

**Step 3 — 结构化对话（三轮）**

分三轮与用户对话，逐步提取项目背景与经验：

- **第一轮：项目背景**（填充 Meta-Card 变量）。根据 Stage 1 定义的领域专属变量，引导用户提供项目的"坐标信息"（如谈判地位、法域、行业、交易规模、风险偏好等）
- **第二轮：关键决策与亮点**。基于 Step 2 的预分析，针对性询问用户为何采取了与标准做法不同的处理方式，以及哪些做法值得复用
- **第三轮：红线与底线**。确认哪些是不可逾越的红线条款，哪些可根据商业条件灵活调整

**Step 4 — 生成经验条目**

为每个有价值的经验点生成标准化条目，包含：
`entry_id` / `title` / `trigger_conditions`（具体的变量组合）/ `adjustment_logic`（做了什么+为什么）/ `knowledge_links` / `archive_links` / `confidence`（high=用户明确说明, medium=ASC推断）/ `red_line` / `source_type`

调用 `scripts/experience_builder.py generate` 生成 EXPERIENCELOG.md：
```bash
python scripts/experience_builder.py generate \
  --input ./experience_entries.json \
  --domain "领域名称" \
  --output ./EXPERIENCELOG.md
```

**Step 5 — 回填知识框架链接**

调用 `scripts/experience_builder.py backfill` 将经验链接回写到 KNOWLEDGEMAP.md 的"关联经验"字段：
```bash
python scripts/experience_builder.py backfill \
  --experience-log ./EXPERIENCELOG.md \
  --knowledge-map ./KNOWLEDGEMAP.md
```

**Step 6 — 去重与冲突检查**

调用 `scripts/experience_builder.py check` 检查经验条目是否有重复或冲突：
```bash
python scripts/experience_builder.py check --input ./EXPERIENCELOG.md
```
如发现冲突，提示用户裁决并细化触发条件以消除歧义。

**Step 7 — 用户审阅与确认**

1. 展示经验概要（所有条目的 title + trigger_conditions）
2. 确认总结方式是否符合用户思维习惯、触发条件是否够具体、红线标记是否准确
3. **特别说明：** Stage 4 的持续学习将沿用此框架继续积累经验，如有调整意见现在提出
4. 用户确认后，Stage 3 结束

### 核心产出物
- `EXPERIENCELOG.md`：经验总结索引（含 YAML frontmatter 和 [[wikilink]] 双向链接）
- `Archives/` 目录中的工作文件原件
- `KNOWLEDGEMAP.md` 中"关联经验"字段已回填为具体经验链接
- 经验条目与知识框架、工作文件之间的完整双向链接网络

---

## Stage 4：实际工作（注入子技能的运行时指令）

> **深度参考：** `references/stage4_runtime.md` 包含完整的检索决策树、匹配策略、意图解读 Prompt、冲突对话模板和注入模板

**再次强调：** Stage 4 的内容不是 ASC 自身执行的，而是 ASC 在 Stage 1 创建子技能时写入子技能 `SKILL.md` 的运行时指令。

### ASC 在 Stage 1 的注入操作

在 Stage 1 生成子技能 `SKILL.md` 时，ASC 应：

1. 读取 `references/stage4_runtime.md` 第 4.3 节的注入模板
2. 根据子技能的具体领域进行调整：
   - 将"领域变量"替换为 Stage 1 定义的实际变量名称
   - 将示例替换为该领域的实际场景
   - 根据输出格式调整差分分析的触发条件
3. 将调整后的指令文本写入子技能 `SKILL.md` 的"持续学习机制"区域（替换占位注释）
4. 确保 scripts/ 目录路径引用正确

### 4.1 知识与经验调用（三级检索优先级）

子技能收到用户指令后，按以下决策树执行检索：

```
收到用户指令 → 提取关键词和上下文线索
    │
    ├─ 优先级 1: 检索 KNOWLEDGEMAP.md（按 keywords 字段匹配）
    │   ├─ 命中 → 沿 [[wikilink]] 提取关联经验条目 + Archives 文件片段
    │   └─ 未命中 ↓
    │
    ├─ 优先级 2: 检索 EXPERIENCELOG.md（按 trigger_conditions 变量匹配）
    │   ├─ 命中 → 沿 [[wikilink]] 提取关联 Archives 文件片段
    │   ├─ red_line:true 条目 → 无论匹配度如何，涉及相关章节就始终提示
    │   └─ 未命中 ↓
    │
    └─ 优先级 3: 基于 Reference/ 参考文件 + 通用领域知识执行
```

链接解析由 `scripts/link_resolver.py` 执行（`--max-chars 800`），精准截取目标段落，避免全文加载。技能在工作中应简要提及参考了哪些知识节点或经验条目。

### 4.2 持续学习闭环

子技能在实际工作中通过三类事件触发学习：

**事件 A — 背景信息捕获**（用户下达指令时）：从自然语言中提取项目变量和关注要点，暂存为会话上下文。

**事件 B — 反馈意图提取**（用户要求修改时）：判断反馈级别——
- 流程级缺陷（遗漏步骤）→ 当场提议更新 `SKILL.md`
- 知识级缺陷（规则错误）→ 当场提议更新 `KNOWLEDGEMAP.md`
- 经验级调整（情境改进）→ 暂存，等待事件 C 统一处理

**事件 C — 差分分析与经验生成**（用户提交最终文件时）：
1. 归档最终文件至 `Archives/`
2. 调用 `scripts/diff_analyzer.py diff --min-significance moderate` 对比初稿与定稿
3. 结合事件 A/B 暂存信息，LLM 推断每个变更的修改意图
4. 转化为经验条目（`source_type: diff_analysis`, `confidence: medium`）
5. 调用 `scripts/experience_builder.py check` 检测重复/冲突
6. **向用户展示拟新增条目，获得确认后方可写入**
7. 调用 `scripts/experience_builder.py append` 追加至 EXPERIENCELOG.md
8. 调用 `scripts/experience_builder.py backfill` 更新 KNOWLEDGEMAP.md 关联经验链接

**核心约束：** 所有经验写入和文件更新必须经用户确认。技能不得自行修改 SKILL.md 或 KNOWLEDGEMAP.md。经验冲突时必须询问用户区分"红线条款"与"可商榷的商业条款"。

---

## 外部工具脚本

以下 Python 脚本作为 ASC 的外部工具存在于 `scripts/` 目录中。ASC 创建的子技能在 `SKILL.md` 中声明"何时调用"这些工具，不在 SKILL.md 中内嵌代码。

| 脚本 | 对应机制 | 用途 | 调用时机 |
|---|---|---|---|
| `knowledge_extractor.py` | 2.1 | 从参考文件提取知识框架 → KNOWLEDGEMAP.md | Stage 2 |
| `experience_builder.py` | 2.2 | 构建标准化经验卡片 → EXPERIENCELOG.md | Stage 3 |
| `link_resolver.py` | 2.3 | 解析 [[wikilink]] 并精准提取上下文 | Stage 4 运行时 |
| `diff_analyzer.py` | 2.4 | 对比初稿与定稿，生成差异报告 | Stage 4 持续学习 |

**关键约束：** ASC 创建的技能运行过程中所涉及的所有文件保存、读取和链接，必须强制使用相对于技能根目录的相对路径（如 `./Archives/xxx.docx`）。

---

## 行为规则

1. **严格按阶段顺序执行：** 不得跳过阶段或在用户确认前进入下一阶段
2. **不得生成未被用户确认的文件：** 每个阶段的产出物需经用户审阅和确认
3. **不得假设参考文件内容：** 必须实际阅读用户提供的文件
4. **信息不足时必须提问：** 不要猜测用户的意图
5. **相对路径强制：** 所有文件引用使用相对路径，确保跨设备可移植
6. **双链语法统一：** 使用 `[[文件名#标题或块ID]]` 格式建立跨文件引用
7. **隐私优先：** 提取经验时捕获模式和推理，不捕获机密细节

---

## 子技能文件结构规范

ASC 创建的每个子技能必须遵循以下文件结构：

```
{Skill_Name}/
├── SKILL.md                 # 技能指令与运行机制（Stage 1 产物）
├── KNOWLEDGEMAP.md          # 结构化知识地图（Stage 2 产物）
├── EXPERIENCELOG.md          # 动态项目经验库（Stage 3 产物 + Stage 4 更新）
├── Reference/               # 静态参考文件库（Stage 2 产物）
│   ├── [template files]
│   └── [playbook files]
└── Archives/                # 工作文件归档库（Stage 3 产物 + Stage 4 更新）
    ├── [project final files]
    └── ...
```
