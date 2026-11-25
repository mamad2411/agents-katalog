---
name: vibe-coding-prd
description: This skill should be used when the user asks to "帮我写一个用来vibe coding的PRD", "写一份给AI写代码用的PRD", "把这个需求/原始PRD/竞品分析整理成可以直接喂给Claude Code或Codex的PRD", or otherwise wants raw requirements, an engineering-facing PRD, or a competitor analysis turned into a concise, structured PRD document meant to be handed directly to a coding agent (Claude Code / Codex) for implementation. Trigger even when the user's input is just a vague product idea and needs to be clarified first.
---

把「需求描述 / 原始PRD / 竞品分析 / 模糊想法」整理成一份精简、结构化、可直接喂给编码 Agent（Claude Code / Codex）实现的 Markdown PRD。

## 何时用 / 不用

| ✅ 用本 skill | ❌ 不用 |
|---|---|
| 把需求/原始PRD/竞品分析转写成给编码 Agent 的 PRD | 直接开始写代码实现需求 → 正常开发流程 |
| 用户只有一句模糊想法，需要引导澄清后产出 PRD | 复刻一个已存在的网页/截图 → `web-clone-prompt` |
| 原始 PRD 是飞书文档，需要读取提炼 | 只是阅读/总结飞书文档，不产出 PRD → `lark-doc` |
| 产出物是可移植的 Markdown PRD 文件 | 写给人看的商业计划书/立项报告 |

## 核心原则

**关键决策必须弹框，细节推断必须标注**——这是本 skill 的确认纪律：

- **必须用 AskUserQuestion 弹框确认**的关键决策：输入类型判断有歧义时、需求定义、功能优先级取舍、技术栈选择、原型布局、是否为 AI 产品。禁止替用户拍板。
- **低风险细节默认推断 + 标注**：不影响功能取舍的细节（如提示文案措辞、字段命名、页面元素微调）不追问，直接采用合理默认值并在 PRD 的「假设与已确认决策」块标注 `[推断]`。
- **提问纪律**：每轮弹框最多 4 个问题，能批量问就批量问，绝不逐条盘问。同一决策不重复确认。

输出内容要精简，只以「编码 Agent 能看懂并直接动手实现」为标准。全程遵守 [references/conventions.md](references/conventions.md) 的精度家规：**用户确认过的决策逐字记录；所有规格写成可检验的字面量；命中反模式表左列的写法一律改写；商业价值/KPI/市场分析/排期按剔除清单删除；用户明确「不做」的功能写成否定约束**。

按 [references/prd-template.md](references/prd-template.md) 的骨架组装最终输出，保持章节结构统一。想看成品的信息密度长什么样，参考 [references/examples/](references/examples/) 中的真实案例。

## 工作流程

### Step 0：识别输入类型

判断用户输入属于以下哪一种：

1. **明确需求**（已有清晰的用户、场景、痛点）→ 跳到 Step 1。
2. **原始PRD**（写给工程师看的完整文档）：
   - 飞书文档链接/token → 使用 `lark-doc` skill 读取文档内容。
   - 粘贴文本或本地文件路径 → 直接读取。
   - 读取后做信息提炼：保留功能点、交互流程、数据/字段、边界条件、约束条件；剔除商业价值、市场背景、KPI/OKR、资源排期等内容。
3. **竞品分析** → 提炼功能点/差异点清单，仅作为 Step 2 功能清单设计的参考输入，不能直接照搬为本产品需求。
4. **完全不清晰**（只有一句模糊想法）→ 不得脑补，用 AskUserQuestion 做结构化引导提问（优先用多选题），至少覆盖：目标用户是谁、使用场景、核心痛点、期望的产品形态（Web / 小程序 / App / 桌面工具 / 命令行工具等）。可分多轮提问，每轮聚焦 1-4 个关键问题，不要一次性塞太多。

如果分类本身有歧义（例如输入既像原始PRD又像模糊想法），同样用 AskUserQuestion 让用户明确选择，不要自行判断走哪条分支。

### Step 1：需求定义确认

写出简短需求定义草稿：给谁 / 什么场景 / 解决什么问题 / 产品形态。信息不完全确定时用 AskUserQuestion 确认；信息已经很明确（用户原话已覆盖全部要素）时可以用文字复述确认，不强制弹框。

### Step 2：功能清单设计 + 优先级

- 输出功能清单：一级模块 → 二级功能 → 一句话功能描述。
- 用 AskUserQuestion 询问优先级（可分多次提问）：
  - 每个一级模块是否要做（做 / 不做 / 暂缓）。
  - 哪些功能是 MVP（优先开发），哪些是后续迭代。
  - 是否有明确的时间/排期要求。
- 根据反馈更新功能清单，标注优先级（P0=MVP / P1 / P2 / 不做）。

### Step 3：技术栈推荐

用户是技术小白，讲人话，不堆术语。

- 基于产品规模、复杂度、时限，先给一个**明确的整体推荐技术栈**（不要甩一堆选项让用户自己选），说明推荐理由。
- 再按功能模块给出具体实现建议（例如前端框架、要不要用现成 BaaS/后端服务、数据存储选型、是否需要鉴权体系等）。
- 用 AskUserQuestion 让用户确认或调整（选项中明确标出推荐项）。

### Step 4：原型图设计（框架版）

- 为核心主功能界面设计文字/ASCII 线框图（页面区块划分、关键元素位置、主要交互入口），不生成图片或 HTML 文件。
- 每设计完一个核心页面，用 AskUserQuestion 向用户二次确认布局是否符合预期，需要的话迭代调整。

### Step 5：明细功能模块设计

先判断是否为 **AI 产品**（涉及大模型/Agent 能力）；不确定时用 AskUserQuestion 确认，不要自行判断。

- **AI 产品**：输出 Agent 工作流（步骤/状态流转）、关键提示词设计要点（目标、输入变量、输出格式约束）、Tool 体系（每个 tool 的输入/输出/用途）。
- **传统产品**：按功能清单逐项展开：输入、处理逻辑、输出、状态、异常情况。

### Step 6：验收标准

为每个功能写「操作 → 预期结果」形式的具体验收标准（如「点击提交按钮 → 表单校验通过后跳转到列表页」「输入非法邮箱格式 → 输入框下方显示红色错误提示文案」）。禁止使用「体验良好」「性能优秀」「操作流畅」等无法验证的模糊表述。

### Step 7：组装 + 交付前自检

- 按 [references/prd-template.md](references/prd-template.md) 骨架，把 Step 1-6 的确认结果组装成完整 Markdown。PRD 顶部必须有「假设与已确认决策」块：用户弹框确认的逐字记录、推断项带 `[推断]`、不做的功能写成否定约束。
- **落盘前必须跑一遍模板末尾的「交付前 QUICK CHECKLIST」**，逐项对照 [references/conventions.md](references/conventions.md) 的反模式表和剔除清单，任何一项不通过先修再交付。
- 写入本地文件，默认路径为当前工作目录下 `PRD-<产品名英文/拼音slug>.md`（若用户指定了路径则使用用户指定的）。
- 不在对话中输出完整 PRD 全文，完成后告知用户文件路径，并给一句话摘要（模块数、功能数、是否为 AI 产品等）。

## 失败沉淀机制

本 skill 按「真实使用 → 暴露问题 → 固化规则」的方式生长：PRD 交给编码 Agent 后，凡出现「Agent 反问了 PRD 没写清的问题」「实现结果与用户预期偏差」的情况，把根因提炼成一条新规则——验收/表述类问题追加进 conventions.md 反模式表，流程类问题作为编号门禁追加到对应 Step。不要只修当次 PRD 而不沉淀规则。
