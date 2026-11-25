---
name: harness-zh
description: "配置 harness，定义专业智能体，并生成这些智能体所使用的技能——元技能（meta-skill）的简体中文版本。触发场景：(1) 用户说『给这个项目搭一个 harness』『构建 harness』『配置 harness』；(2) 用户请求『harness 设计』『harness 工程化』；(3) 为新领域/新项目建立基于 harness 的自动化体系；(4) 重构或扩展已有 harness；(5) 用户请求『harness 点检』『harness 审计』『harness 现状』『智能体/技能同步』等运维/维护任务；(6) 用户提到『组织 agent』『设计工作流』『多 agent 协作』『搭建自动化流程』『agent 怎么分工』『agent 团队』等表达。等同于 skills/harness 的功能，仅语言不同，按用户使用的语言选择其一即可。"
---

# Harness — Agent Team & Skill Architect

为特定领域/项目构建 Harness，定义各个 Agent 的角色，并生成 Agent 所使用的 Skill 的元 Skill（meta skill）。

**核心原则：**
1. 生成 Agent 定义（`.claude/agents/`）与 Skill（`.claude/skills/`）。
2. **将 Agent 团队（Agent Team）作为默认执行模式。**
3. **在 CLAUDE.md 中注册 Harness 指针（pointer）。** —— 仅记录最少量的指针（触发规则 + 变更历史），以便在新会话中自动触发编排器（orchestrator）Skill。
4. **Harness 不是固定物，而是不断进化的系统。** —— 每次执行后都要吸收反馈，持续更新 Agent、Skill 与 CLAUDE.md。

## 工作流（Workflow）

### Phase 0: 现状审计（Audit）

当 Harness Skill 被触发时，首先确认既有 Harness 的现状。

1. 读取 `项目/.claude/agents/`、`项目/.claude/skills/`、`项目/CLAUDE.md`
2. 根据现状分支执行模式：
   - **全新构建**：Agent/Skill 目录不存在或为空 → 从 Phase 1 开始完整执行
   - **既有扩展**：已有 Harness，并需要追加新 Agent/Skill → 按下方 Phase 选择矩阵仅执行必要 Phase
   - **运维/维护**：对既有 Harness 的审计·修改·同步请求 → 跳转至 Phase 7-5 运维/维护工作流

   **既有扩展时的 Phase 选择矩阵：**
   | 变更类型 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
   |----------|---------|---------|---------|---------|---------|---------|
   | 新增 Agent | 跳过（复用 Phase 0 结果） | 仅决定编排位置 | 必需 | 需要专属 Skill 时 | 修改编排器 | 必需 |
   | 新增/修改 Skill | 跳过 | 跳过 | 跳过 | 必需 | 连接关系变化时 | 必需 |
   | 架构变更 | 跳过 | 必需 | 仅受影响 Agent | 仅受影响 Skill | 必需 | 必需 |
3. 将既有 Agent/Skill 列表与 CLAUDE.md 记录进行对照，检测不一致（drift）
4. 将审计结果汇总汇报给用户，并确认执行计划

### Phase 1: 领域分析（Domain Analysis）
1. 从用户请求中把握领域/项目
2. 识别核心作业类型（生成、校验、编辑、分析等）
3. 基于 Phase 0 的审计结果，分析与既有 Agent/Skill 的冲突/重复
4. 探索项目代码库 —— 把握技术栈、数据模型、主要模块
5. **检测用户熟练度** —— 通过对话中的上下文线索判断其技术水平，据此调节后续沟通语气。对编程经验较少的用户，避免不加解释地使用专业术语。

### Phase 2: 团队架构设计（Team Architecture Design）

#### 2-1. 选择执行模式

**Agent 团队是最高优先级的默认值。** 当有 2 个以上 Agent 协作时，必须首先考察是否采用 Agent 团队。团队成员之间通过直接通信（SendMessage）与共享任务列表（TaskCreate）自我协调，通过发现共享、冲突讨论、遗漏补全来提升结果质量。

| 模式 | 何时使用 | 特性 |
|------|----------|------|
| **Agent 团队**（默认） | 2 人以上协作、需要实时协调·反馈交换、相互引用中间产物 | 通过 `TeamCreate` + `SendMessage` + `TaskCreate` 自我协调 |
| **子 Agent（Sub Agent）**（备选） | 单 Agent 作业、只需向主体返回结果即可、团队通信开销过大时 | 直接调用 `Agent` 工具，使用 `run_in_background` 并行 |
| **混合（Hybrid）** | 各 Phase 特性不同时 —— 如：并行收集（子 Agent）→ 基于共识的整合（团队） | 按 Phase 混合团队/子 Agent |

**决策顺序：**
1. 首先考察是否可按 Agent 团队设计 —— 2 人以上即为默认
2. 仅当结构上不需要团队通信（只需结果传递）、且团队开销大于收益时，才选择子 Agent
3. 各 Phase 特性差异明显时考虑混合 —— 将各 Phase 的执行模式在编排器中明示

> 详尽比较表和分模式决策树请参见 `references/agent-design-patterns.md` 中的 "执行模式" 一节。

#### 2-2. 选择架构模式

1. 将任务分解为专业领域
2. 决定 Agent 团队结构（架构模式请参见 `references/agent-design-patterns.md`）
   - **流水线（Pipeline）**：顺序依赖作业
   - **Fan-out/Fan-in**：并行独立作业
   - **专家池（Expert Pool）**：按场景选择调用
   - **生成-校验（Generate-Verify）**：生成后再进行质量审核
   - **监督者（Supervisor）**：中央 Agent 管理状态并动态分发
   - **分层委派（Hierarchical Delegation）**：上级 Agent 向下级递归委派

#### 2-3. Agent 拆分标准

以专业性·并行性·上下文·复用性 4 个维度判断。详细标准表请参见 `references/agent-design-patterns.md` 中的 "Agent 拆分标准" 一节。

### Phase 3: 生成 Agent 定义

**所有 Agent 必须以 `项目/.claude/agents/{name}.md` 文件形式定义。** 禁止不创建 Agent 定义文件、直接把角色塞进 Agent 工具 prompt 的做法。理由：
- Agent 定义必须以文件形式存在，下一会话才能复用
- 必须明示团队通信协议，才能保证 Agent 间协作质量
- Harness 的核心价值在于 Agent（谁）与 Skill（怎么做）的分离

即便使用内建类型（`general-purpose`、`Explore`、`Plan`），也要生成 Agent 定义文件。内建类型通过 Agent 工具的 `subagent_type` 参数指定，Agent 定义文件则承载角色·原则·协议。

**模型设置：** 默认使用 `model: "opus"`，以保证最高推理质量。对于低复杂度的结构化任务（格式转换、模板填充、数据抽取等），可降级为 `model: "sonnet"` 以节约成本。在编排器中为每个 Agent 明示所选模型及其理由。

| 任务复杂度 | 推荐模型 | 示例 |
|---|---|---|
| 高（推理密集、创作、架构设计、QA） | opus | 编排器、分析、综合判断、质量审查 |
| 中（遵循模板、结构化生成） | sonnet | 格式转换、数据抽取、模板填充、简单 CRUD |

**团队重组：** 每个会话仅能激活一个 Agent 团队，但可以在 Phase 之间解散旧团队、组建新团队。像流水线模式那样在不同 Phase 需要不同专家组合时，先将上一团队的产物保存为文件，再清理团队并创建新团队。

将每个 Agent 定义到 `项目/.claude/agents/{name}.md`。必备章节：核心角色、作业原则、输入/输出协议、错误处理、协作。在 Agent 团队模式下，还需追加 `## 团队通信协议` 章节，明示消息的接收/发送对象以及作业请求的范围。

> 定义模板与实际文件全文请参见 `references/agent-design-patterns.md` 中的 "Agent 定义结构" 以及 `references/team-examples.md`。

**包含 QA Agent 时的必备事项：**
- QA Agent 使用 `general-purpose` 类型（`Explore` 为只读，无法执行校验脚本）
- QA 的核心不是"存在确认"，而是 **"跨边界比对"** —— 同时读取两侧代码，比对 shape
- QA 不是整体完成后执行 1 次，而是 **在每个模块完成后立即增量执行**（incremental QA）
- 详细指南：参见 `references/qa-agent-guide.md`

### Phase 4: 生成 Skill

将每个 Agent 使用的 Skill 生成到 `项目/.claude/skills/{name}/SKILL.md`。详细编写指南请参见 `references/skill-writing-guide.md`。

#### 4-1. Skill 结构

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter (name, description 必需)
│   └── Markdown 本文
└── Bundled Resources (可选)
    ├── scripts/    - 重复/确定性作业的可执行代码
    ├── references/ - 条件加载的参考文档
    └── assets/     - 用于输出的文件（模板、图片等）
```

#### 4-2. 编写 Description —— 主动诱导触发

description 是 Skill 的唯一触发机制。Claude 倾向于保守地判断是否触发，因此 description 要写得 **主动（"pushy"）**。

**坏例子：** `"处理 PDF 文档的 Skill"`
**好例子：** `"读取 PDF 文件、提取文本/表格、合并、拆分、旋转、加水印、加密、OCR 等执行所有 PDF 作业。当提及 .pdf 文件或请求 PDF 产物时，必须使用本 Skill。"`

要点：同时描述 Skill 做什么 + 具体触发场景，并与相似但不应触发的情况区分开。

#### 4-3. 正文编写原则

| 原则 | 说明 |
|------|------|
| **阐明 Why** | 不要使用 "ALWAYS/NEVER" 之类的强硬指令，而是传达之所以这样做的理由。LLM 理解理由后，在 edge case 中也能做出正确判断。 |
| **保持精简（Lean）** | 上下文窗口是公共资源。SKILL.md 正文以 500 行以内为目标，对决策无实质帮助的内容要删除或转移到 references/。 |
| **泛化（Generalize）** | 比起只适配特定例子的狭窄规则，应讲清原理，让 Skill 能应对多样输入。禁止过拟合（overfitting）。 |
| **重复代码要 bundling** | 若发现 Agent 在测试执行中普遍编写相同脚本，则提前 bundle 到 `scripts/`。 |
| **使用命令式语气** | 使用 "做……"、"执行……" 之类的命令/指示语气。 |

#### 4-4. Progressive Disclosure（渐进披露）

Skill 通过 3 级加载系统管理上下文：

| 级别 | 加载时机 | 大小目标 |
|------|----------|----------|
| **Metadata**（name + description） | 始终存在于上下文中 | ~100 词 |
| **SKILL.md 正文** | Skill 触发时 | <500 行 |
| **references/** | 仅在需要时 | 无上限（脚本无需加载即可执行） |

**大小管理规则：**
- 当 SKILL.md 接近 500 行时，将细节分离到 references/，正文中留下"何时去读该文件"的指针
- 超过 300 行的 reference 文件应在顶部包含 **目录（ToC）**
- 若存在按领域/框架的变体，则在 references/ 下按领域拆分，仅加载相关文件

#### 4-5. Skill–Agent 连接原则

- 1 个 Agent ↔ 1~N 个 Skill（1:1 或 1:多）
- 也允许多个 Agent 共享同一个 Skill
- Skill 承载"如何做"，Agent 承载"谁来做"

> 详细编写模式、示例、数据 schema 标准请参见 `references/skill-writing-guide.md`。

### Phase 5: 集成与编排（Orchestration）

编排器（orchestrator）是 Skill 的特殊形态，负责把各个 Agent 与 Skill 串成单一工作流，统筹整个团队。如果说 Phase 4 中生成的各 Skill 定义了"各 Agent 做什么、怎么做"，那么编排器就定义了"谁在何时按什么顺序协作"。具体模板请参见 `references/orchestrator-template.md`。

**既有扩展时的编排器修改：** 非全新构建、而是既有扩展时，不要新建编排器，而是修改既有编排器。新增 Agent 时，在团队组成·作业分配·数据流中反映新 Agent，并在 description 中补充与新 Agent 相关的触发关键字。

Phase 2-1 选择的执行模式不同，编排器的模式也不同。编排器模式的详细模板（Agent 团队/子 Agent/混合）请参见 `references/orchestrator-template.md`。

#### 5-1. 数据传递协议

在编排器内明示 Agent 之间的数据传递方式。推荐组合：团队模式用「任务型 + 文件型 + 消息型」，子 Agent 模式用「返回值型 + 文件型」。文件型传递时，在 `_workspace/` 下保存中间产物，文件名约定 `{phase}_{agent}_{artifact}.{ext}`。仅最终产物输出到用户指定路径。

> 各策略的详细说明请参见 `references/orchestrator-template.md`。

#### 5-2. 错误处理

在编排器内包含错误处理方针。核心原则：重试 1 次后仍失败，则跳过该结果继续推进（在报告中注明缺失）；相冲突的数据不做删除，而是并列标注来源。

> 按错误类型划分的策略表请参见 `references/orchestrator-template.md` 中的 "错误处理" 一节。

#### 5-3. 团队规模指南

| 作业规模 | 推荐成员数 | 每人作业数 |
|----------|------------|--------------|
| 小规模（5~10 个作业） | 2~3 人 | 3~5 个 |
| 中规模（10~20 个作业） | 3~5 人 | 4~6 个 |
| 大规模（20 个以上作业） | 5~7 人 | 4~5 个 |

> 团队成员越多，协调开销越大。3 个专注的成员胜过 5 个涣散的成员。

#### 5-4. 在 CLAUDE.md 注册 Harness 指针

Harness 构建完成后，在项目的 `CLAUDE.md` 中注册最小量指针。CLAUDE.md 每个新会话都会加载，因此只要记录 Harness 的存在与触发规则，其余交给编排器 Skill 处理即可。

**CLAUDE.md 模板：**

````markdown
## Harness：{领域名}

**目标：** {Harness 的核心目标一行}

**触发：** 当收到与 {领域} 相关的作业请求时，使用 `{orchestrator-skill-name}` Skill。简单问题可直接回答。

**变更历史：**
| 日期 | 变更内容 | 对象 | 事由 |
|------|----------|------|------|
| {YYYY-MM-DD} | 初始构建 | 全体 | - |
````

**不要放进 CLAUDE.md 的内容：** Agent 列表、Skill 列表、目录结构、执行规则细节。理由：Agent/Skill 列表由编排器 Skill 与 `.claude/agents/`、`.claude/skills/` 管理，放入 CLAUDE.md 只是重复。CLAUDE.md 仅承载 **指针（触发规则）+ 变更历史**。

#### 5-5. 后续作业支持

编排器不仅要处理初次执行，还要处理后续作业。必须保证以下三点：

**1. 编排器 description 中包含后续关键字：**
仅凭初次生成的关键字，无法触发后续请求。description 中必须包含的后续表达："重新执行"、"再跑一次"、"更新"、"修改"、"补充"、"仅对 {部分} 重新执行"、"基于先前结果"、"改进结果"。

**2. 在编排器 Phase 1 追加上下文确认步骤：**
工作流开始时确认既有产物是否存在，据此决定执行模式：
- `_workspace/` 存在 + 用户请求部分修改 → **部分重跑**
- `_workspace/` 存在 + 用户提供新输入 → **全新执行**（移旧 _workspace）
- `_workspace/` 不存在 → **初次执行**

**3. Agent 定义中包含重复调用指引：**
在每个 Agent `.md` 文件中明示"存在先前产物时的行为"。

> 参见编排器模板的 "Phase 0: 上下文确认" 章节：`references/orchestrator-template.md`

### Phase 6: 校验与测试

校验生成的 Harness。详细测试方法论请参见 `references/skill-testing-guide.md`。

#### 6-1. 结构校验

- 确认所有 Agent 文件位于正确位置
- 校验 Skill 的 frontmatter（name、description）
- 确认 Agent 间引用的一致性
- 确认未生成 command

#### 6-2. 按执行模式校验

- **Agent 团队**：确认成员间通信路径、作业依赖、团队规模是否适当
- **子 Agent**：确认各 Agent 的输入输出连接、`run_in_background` 设置、返回值收集逻辑
- **混合**：确认各 Phase 的执行模式是否在编排器中明示，Phase 边界处数据传递是否未断

#### 6-3. Skill 执行测试

对生成的每个 Skill 执行实际运行测试。核心流程：编写 2~3 条现实测试 prompt → with-skill / without-skill 并行执行对比 → 定性/定量结果评估 → 迭代改进 → 重复代码 bundling。

> 详细的测试 prompt 编写、评估方法、迭代改进循环请参见 `references/skill-testing-guide.md`。

#### 6-4. 触发校验

校验每个 Skill 的 description 是否被正确触发：

1. **Should-trigger 查询**（8~10 条）—— 应触发该 Skill 的各种表达（正式/随意、显式/隐式）
2. **Should-NOT-trigger 查询**（8~10 条）—— 关键字相似但应匹配其他工具/Skill 的 "near-miss" 查询

**编写 near-miss 的要点：** "写一个斐波那契函数"这样明显无关的查询毫无测试价值。边界模糊的查询才是好的测试用例。本阶段也要同时确认与既有 Skill 的触发冲突。

#### 6-5. Dry-run 测试

- 审核编排器 Skill 的 Phase 顺序是否合理
- 确认数据传递路径上无空段（dead link）
- 确认每个 Agent 的输入是否与上一 Phase 的输出匹配
- 确认各错误场景对应的 fallback 路径是否可执行

#### 6-6. 编写测试场景

- 在编排器 Skill 中追加 `## 测试场景` 章节
- 至少描述 1 个正常流程 + 1 个错误流程

### Phase 7: Harness 进化

Harness 不是一次生成就结束的静态产物，而是根据用户反馈持续进化的系统。

#### 7-1. 执行后收集反馈

每次 Harness 执行完成后，向用户请求反馈。若无反馈则放行。不强求，但必须提供机会。

#### 7-2. 反馈落地路径

按反馈类型，修改对象不同：

| 反馈类型 | 修改对象 | 例 |
|-----------|----------|------|
| 产物质量 | 对应 Agent 的 Skill | "分析太表面" → 在 Skill 中追加深度标准 |
| Agent 角色 | Agent 定义 `.md` | "还需要安全审查" → 新增 Agent |
| 工作流顺序 | 编排器 Skill | "要先校验" → 调整 Phase 顺序 |
| 团队组成 | 编排器 + Agent | "这两个可以合并" → 合并 Agent |
| 触发遗漏 | Skill description | "用这个表达就不生效" → 扩展 description |

#### 7-3. 变更历史

所有变更都记录到 CLAUDE.md 的 **变更历史** 表中（与 Phase 5-4 模板中的 "变更历史" 章节为同一张表）。通过这份历史，可追踪 Harness 朝哪个方向进化，并防止倒退（regression）。

#### 7-4. 进化触发

不仅在用户显式地说"修改 Harness"时进化，在以下情况也主动提议进化：
- 同一类型的反馈反复出现 2 次以上时
- 某个 Agent 反复失败形成模式时
- 观察到用户绕过编排器手动处理作业时

#### 7-5. 运维/维护工作流

系统性地执行既有 Harness 的点检·修改·同步。Phase 0 中进入 "运维/维护" 分支时，遵循本工作流。

**Step 1：现状审计**
- 对比 `.claude/agents/` 文件列表与编排器 Skill 中的 Agent 配置 → 生成不一致清单
- 对比 `.claude/skills/` 目录列表与编排器 Skill 中的 Skill 配置 → 生成不一致清单
- 将审计结果汇报给用户

**Step 2：渐进式新增/修改**
- 根据用户请求执行 Agent 的新增/修改/删除、Skill 的新增/修改/删除
- 变更一次只做一项，每次变更后立即执行 Step 3（同步）

**Step 3：更新 CLAUDE.md 变更历史**

**Step 4：校验变更**
- 校验修改后的 Agent/Skill 结构（Phase 6-1 基准）
- 若修改范围影响触发，进行触发校验（Phase 6-4 基准）
- 大规模变更时，还需执行 Phase 6-3（执行测试）、6-5（dry-run）
- 最后确认 CLAUDE.md 与实际文件是否一致

## 产物清单（Checklist）

生成完成后需确认：

- [ ] `项目/.claude/agents/` —— **必须生成 Agent 定义文件**（即便使用内建类型也必须生成文件）
- [ ] `项目/.claude/skills/` —— Skill 文件群（SKILL.md + references/）
- [ ] 1 个编排器 Skill（包含数据流 + 错误处理 + 测试场景）
- [ ] 明示执行模式（Agent 团队 / 子 Agent / 混合 中择一，若为混合则逐 Phase 标注模式）
- [ ] 所有 Agent 调用中均明示 `model` 参数（默认 opus，低复杂度任务可用 sonnet）
- [ ] `.claude/commands/` —— 不生成任何内容
- [ ] 与既有 Agent/Skill 无冲突
- [ ] Skill description 以主动（"pushy"）方式编写 —— **包含后续作业关键字**
- [ ] SKILL.md 正文在 500 行以内，超过时分离到 references/
- [ ] 以 2~3 条测试 prompt 完成执行校验
- [ ] 完成触发校验（should-trigger + should-NOT-trigger）
- [ ] **在 CLAUDE.md 中注册 Harness 指针**（触发规则 + 变更历史）
- [ ] **在 CLAUDE.md 变更历史中记录 Agent/Skill 的新增/删除/修改**
- [ ] **编排器 Phase 1 中包含上下文确认步骤**（判别初次/后续/部分重跑）

## 参考

- Harness 模式：`references/agent-design-patterns.md`
- 既有 Harness 示例（含实际文件全文）：`references/team-examples.md`
- 编排器模板：`references/orchestrator-template.md`
- **Skill 编写指南**：`references/skill-writing-guide.md` —— 编写模式、示例、数据 schema 标准
- **Skill 测试指南**：`references/skill-testing-guide.md` —— 测试/评估/迭代改进方法论
- **QA Agent 指南**：`references/qa-agent-guide.md` —— 包含集成一致性校验方法论（通用 + 多领域示例）、边界 bug 模式、QA Agent 定义模板
