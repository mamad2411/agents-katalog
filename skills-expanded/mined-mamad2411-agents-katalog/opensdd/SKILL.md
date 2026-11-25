---
name: opensdd
description: "Open Spec-Driven Development — 编码前规范阶段工作流。为 AI 智能体提供需求规格、验收规格、架构设计、模块详细设计、任务计划、入口指引共 6 类文档的规范化生成流程，产物作为后续 AI 自主编码阶段的契约依据。【注意：本技能由人类主动加载调用，AI 不应在未被人类明确要求时自行触发整个流程】"
metadata:
  author: zhgstudio
  version: 3.8.2
---

# OpenSDD — 编码前规范阶段工作流

## 技能概述

本技能解决的是 **AI 自主编码前"先想清楚再写"** 的问题。通过 5 个角色的分阶段协作，生成各类规范文档，作为后续编码阶段的契约依据。

**核心原则**：本技能各阶段主要产出规范文档，经人类评审定稿后作为编码阶段契约依据。**两个代码例外**：(1) 阶段 T-2 的 TE Agent 根据 `ACCEPTANCE.md` 和 `API.md` 生成端到端验收测试代码（`tests/e2e/`），作为可执行的规格声明；(2) 设计师在阶段三可临时创建实验性代码（`docs/modules/{NN}-{name}/tmp/`）用于推演接口可行性或验证数据流，用完即弃，不进入版本管理（详见 phase-3.md §10）。

> **加载方式**：本技能由**人类主动加载调用**——人类在需要时手动启动某个阶段，AI **不应**在未被人类明确要求时自行启动整个多阶段流程。人类已启动某阶段时，AI 可按下方「阶段自动触发条件」规则自动匹配对应 phase 文件加载。

---

## 核心目录拓扑

```text
AGENTS.md                   # 全局入口指引（多阶段增量积累，人类最终锁定。存在时各阶段 AI 均自动加载）
docs/
├── SPEC.md                 # 需求规格（PM Agent 产出），产品入口准入依据，人类必须严格审查
├── ACCEPTANCE.md           # 验收规格（TE Agent 产出），产品出口门禁依据，人类必须严格审查
├── ARCHITECTURE.md         # 总体架构设计（Architect Agent 产出）
├── PLAN.md                 # 任务计划（Project Manager Agent 产出）
├── coding-protocol.md      # 编码阶段自动执行协议（Project Manager Agent 产出）
├── DECISIONS.md            # 决策记录（可选）——存储被拒绝或遗留暂不处理的事项及理由，仅审查/审视/评审过程加载
│
└── modules/                # N. 模块详细设计
    ├── 01-{name}/
    │   ├── API.md    # 对外接口定义（本模块可读写，依赖方只读）
    │   └── DESIGN.md    # 内部实现细节（本模块可读写）
    ├── 02-{name}/
    │   ├── API.md
    │   └── DESIGN.md
    └── ...

tests/
├── e2e/                    # 验收测试代码（TE Agent T-2 产出，黑盒 E2E）
└── results/                # 测试结果文件（编码阶段测试运行后生成，供 opensdd-check 覆盖率检查消费）
    ├── ut.json             # 单元测试结果
    ├── component.json      # 组件测试结果
    ├── integration.json    # 集成测试结果
    └── e2e.json             # E2E 验收测试结果
```

> **技能自身目录**：技能目录下除上述 phase 文件外，还包含 `coding-protocol.md` 静态文件，阶段四 PM Agent 将其完整复制到下游项目 `docs/coding-protocol.md`。

> 注：`tests/results/` 下的 JSON 文件是所有阶段测试运行的产物，在规范阶段（阶段一至四）不存在属正常行为。`opensdd-check` 的覆盖率检查在文件缺失时返回 WARN 而非 FAIL。

### 命名规范

- 模块目录使用 **两位数字 + 连字符 + 英文短名** 格式，如 `01-auth`、`02-task-core`
- 模块目录名必须与 `ARCHITECTURE.md` 中的模块引用表中的名称严格一致
- 两位数字是模块的**固定标识**（类似出厂编号），**追加或插入均可，但已有编号永久固定不重排**。已有 01、02，则新增为 03（或插入 01.5 等方案自定）。模块一旦编号即永久固定，不因其他模块的增删而重排
- 设计阶段可接受序号不连续（如跨模块评审失败导致跳过）
- 模块退役规则参见 `AGENTS.md` 中的「模块退役协议」章节（由 Architect Agent 在阶段二写入）

### 编号体系

OpenSDD 使用三层编号体系实现从需求到任务的完整追溯链：

| 层级 | 格式 | 所在文档 | 示例 |
|------|------|----------|------|
| 需求 | `REQ-{DOMAIN}-{NNN}` | `SPEC.md` | `REQ-AUTH-001` |
| 特性 | `{MODULE}-F{NNN}` | `docs/modules/{NN}-{name}/DESIGN.md` | `AUTH-F001` |
| 任务 | `T-{MODULE}-{NNN}` | `PLAN.md` | `T-AUTH-001` |

追溯关系：`REQ-{DOMAIN}-{NNN}`（需求）→ 1 个或多个 `{MODULE}-F{NNN}`（特性，分布在同模块或不同模块）→ 每个 `{MODULE}-F{NNN}` 对应唯一 `T-{MODULE}-{NNN}`（开发计划中的编码任务）。

完整链路：`REQ-{DOMAIN}-{NNN}` → `{MODULE}-F{NNN}`（1:N）→ `T-{MODULE}-{NNN}`（1:1）。

任务通过 `[module-name/DESIGN.md#{MODULE}-F{NNN}]` 引用到具体特性，特性通过其模块归属关联到源头需求。

**编号设计原则**：
- **需求（REQ）**：`DOMAIN` 为业务领域缩写（大写，2-15 字符），与模块目录名解耦。同领域内编号稀疏递增（如 001, 005, 010），支持插入
- **特性（Feature）**：`MODULE` 为模块目录名去除数字前缀后的名称（如 `01-auth` → `AUTH`、`02-task-core` → `TASK-CORE`，目录名中的连字符保留为大写后的分隔符）。模块内编号稀疏递增
- **任务（Task）**：`MODULE` 与 Feature 一致，确保同一模块的任务可聚合。模块内编号稀疏递增

**编号范围能力上限**：三位数字编号（NNN）的容量为 000-999，即每个领域最多 999 条需求、每个模块最多 999 个特性/任务。此范围为能力上限，不支持更大编号——超大项目应拆分为多个子项目。

### 编号定义格式

所有编号（REQ、Feature、Task）在各自文档中的**定义位置**必须出现在行首（列表项`- `、标题行或表格行首），嵌入段落文本的视为交叉引用，不计为定义。

推荐格式：
- 需求（SPEC.md）：`- **REQ-{DOMAIN}-{NNN}** (P{priority}): {描述}`
- 验收场景组标题（ACCEPTANCE.md）：`## REQ-{DOMAIN}-{NNN}: {场景组名}`
- 特性（DESIGN.md）：`### {MODULE}-F{NNN}: {特性名}`
- 任务（PLAN.md）：`| T-{MODULE}-{NNN} | ... |`

### 文档语言

所有文档使用人类在项目启动时指定的语言。人类在启动阶段一时须交代文档语言（如"使用中文"或"使用 English"）。

**语言一致性的约束范围**：要求统一的是文档的**主体叙述语言**（行文、描述、解释性文字）。标识符（变量名、函数名、类名）、代码片段、URL、专有名词、API 路径等不受此约束，允许与主体叙述语言不同。

### 严格字符规范

所有产物中的字符级语法规则采用精确匹配，不接受形似替代字符：
- 连字符仅限 U+002D (`-`)，不接受 em dash (`—`)、en dash (`–`) 等
- 空白符仅限 U+0020 (空格)，不接受全角空格、Tab、NBSP 等
- 换行符仅限 LF (U+000A)，不接受 CRLF
- 标点仅限 ASCII 标点，不接受全角标点

生成文档时直接遵循此规范，不依赖事后检查修正。

---

## 文档作用

| 文档 | 作用 | 使用者 |
|------|------|--------|
| `SPEC.md` | 原始需求的全面细化，覆盖业务边界、用户旅程、优先级、非功能性约束。二级标题须带固定编号（`## 1. 业务背景与目标` ~ `## 5. 边界与排除项`） | 所有角色 |
| `ACCEPTANCE.md` | 验收场景定义，从 SPEC.md 衍生的结构化 Given/When/Then 场景，作为编码结束后最终验收门禁的唯一依据 | TE Agent |
| `ARCHITECTURE.md` | 总体架构设计 + 公共设计（技术栈、全局编码规范、跨模块契约），模块引用表指向各模块目录 | Architect、Designer |
| `modules/{NN}-{name}/API.md` + `DESIGN.md` | 该模块的接口定义与内部实现，代码开发必须严格遵循 | Designer、编码阶段的开发者 |
| `PLAN.md` | 基于 DESIGN.md 拆分的开发任务跟踪表，仅含任务条目和完成状态，不含方案细节 | 编码阶段的开发者 |
| `coding-protocol.md` | 编码阶段自动执行协议的完整版本（扫描循环、单任务执行、阻塞处理、验收门禁） | 编码阶段的 subagent |
| `tests/e2e/` 中的验收测试代码 | ACCEPTANCE.md 的可执行实现，由 TE Agent T-2 阶段根据 API.md 接口签名绑定生成 | 编码阶段开发者（执行时）、TE Agent（审查时） |
| `AGENTS.md` | 项目级工程规则与约束的入口指引。包含文件/目录权限、提交规范、开发阶段测试规范、升级条件、决策记录机制、模块目录说明、验收测试规范、编码阶段自动执行协议（精简版，完整协议见 `coding-protocol.md`）等。跨模块依赖关系以 `ARCHITECTURE.md` 模块依赖矩阵为准。由 OpenSDD 各阶段增量积累，人类最终锁定。**存在时由 AI 工具内置自动加载至系统提示词层** | 所有角色（存在时） |
| `DECISIONS.md` | 决策记录（可选）。存储被明确拒绝或遗留暂不处理的事项及其理由。**仅审查/审视/评审过程加载**，其他阶段不需要读取 | 人类（评审时），AI（仅评审相关操作时） |

---

## 文档引用深度约定

OpenSDD 使用四种引用深度模式管理文档间的内容关联，减少重复的同时保持追溯链完整：

| 模式 | 术语 | 定义 | 表现形式 |
|------|------|------|---------|
| **REF** | 标识引用 | 目标文档仅含一个不可解析的标识符指向源文档的条目，读者须自行查阅源文档获取具体内容 | `REQ-AUTH-001`、`[01-auth/DESIGN.md#AUTH-F001]` |
| **INCLUDE** | 显式包含 | 目标文档包含来自源文档的有明确边界的内容块，同时声明来源路径。块内内容须与源文档保持一致，变更时须同步更新所有 INCLUDE 位置 | 标记块 `<!-- 继承自 ARCHITECTURE.md §公共设计 -->` + 具体内容 |
| **SYNTHESIZE** | 综合重述 | 目标文档基于源文档内容重新组织表述，形成独立完整的段落，不复用源文档原文 | ACCEPTANCE.md 中场景的 Given/When/Then 描述；AGENTS.md 中工程规则章节；DESIGN.md 中每条 `{MODULE}-F{NNN}` 的业务描述段 |
| **EXCLUDE** | 有意识排除 | 目标文档故意不含某类信息，即使源文档中有 | PLAN.md 不含方案细节；ACCEPTANCE.md 不含技术实现细节 |

### 决策规则

对每对源文档与目标文档之间的信息项，按以下优先级顺序判断引用深度：

1. **EXCLUDE 判断**：此信息是否应在目标文档中被故意排除？→ 是 → **EXCLUDE**
2. **REF 判断**：源文档和目标文档在所有使用场景下是否总是同时加载？→ 是 → **REF**
3. **INCLUDE 判断**：此信息稳定不变且规模小（≤10 行）？→ 是 → **INCLUDE**
4. **SYNTHESIZE 判断**：目标文档是否需要在脱离源文档时也能独立理解？→ 是 → **SYNTHESIZE**
5. 以上均不满足 → **REF**

各阶段执行时的具体引用深度要求，由对应 phase 文件在行为规则中细化。SKILL.md 仅定义框架和决策规则。

### 规范依赖声明

对于 REF 模式中的"规范继承"场景（ARCHITECTURE.md → API.md / DESIGN.md），API.md 和 DESIGN.md 须在其头部包含以下形式的规范依赖声明：

```markdown
> **规范依赖**：本文件的命名规范遵循 `ARCHITECTURE.md`「全局编码规范」章节，错误格式、分页规范、时间格式、审计字段等跨模块契约遵循「公共设计」章节，技术栈遵循「技术栈标准」章节。
```

规范依赖声明不是 INCLUDE（不复制具体内容），而是 REF 模式的具象化——明确依赖路径，使读者和 AI Agent 可知需要查阅哪个源文档的哪个章节。此声明由设计师在阶段三生成模块文档时写入。

---

## 五角色模型

| 角色 | 阶段 | 读 | 写 |
|------|------|----|----|
| **PM Agent**（产品经理） | 阶段一 | — | `docs/SPEC.md` |
| **TE Agent**（测试工程师） | 阶段 T-1 | `SPEC.md`（只读） | `docs/ACCEPTANCE.md`、追加 `AGENTS.md`「验收测试规范」章节 |
| **TE Agent**（测试工程师） | 阶段 T-2 | `ACCEPTANCE.md` + 各模块 `API.md`（只读）+ `ARCHITECTURE.md`（模块引用表与依赖矩阵） | `tests/e2e/` 验收测试代码、追加 `AGENTS.md` 测试运行命令、目录说明与失败元数据格式规范 |
| **Architect Agent**（架构师） | 阶段二 | `SPEC.md`（只读） | `docs/ARCHITECTURE.md`、写入 `AGENTS.md` 主体 |
| **Designer Agent**（模块设计师） × N | 阶段三 | `ARCHITECTURE.md` + `SPEC.md` + 所依赖模块的 `API.md`（只读，由主会话传递） | `docs/modules/{NN}-{name}/API.md` + `DESIGN.md`（由 subagent 执行） |
| **Project Manager Agent**（项目经理） | 阶段四 | 全部已定稿设计文档 | `docs/PLAN.md`、`docs/coding-protocol.md`、追加 `AGENTS.md`「PLAN.md 任务规范」与「编码阶段自动执行协议」（精简版）章节 |

每个角色启动新的 AI 会话，只加载职责范围内的文件。每阶段产物经人类评审定稿后，才能进入下一阶段。

> **会话管理说明：** 每个角色启动新会话的操作由**人类**手动完成。如果使用的 AI 平台不支持洁净会话隔离，人类可以在同一会话中手动重置上下文。本技能定义的"新会话"是指认知上的上下文隔离——确保同一角色只加载职责范围内的文件。

### 角色职责边界

各角色的行为边界由其读写范围自然界定：
- **PM Agent** 聚焦业务需求，不介入技术方案讨论
- **TE Agent** 只做验收场景定义与测试代码生成，不评审设计，不干预编码，不读取 `DESIGN.md`
- **Architect Agent** 只做整体架构与公共设计，不深入模块内部设计
- **Designer Agent** 只设计当前模块（由 subagent 执行），不写代码，不读取所依赖模块的 `DESIGN.md`
- **Project Manager Agent** 只做任务跟踪，不修改设计内容

此外，各阶段执行中还应遵守：
- 不允许创建 `_v2.md`、`_final.md`、`.bak.md` 等版本残留文件，物理覆盖即可
- `PLAN.md` 的每条任务必须引用对应 `DESIGN.md` 的章节
- AI 仅允许 `git add`、`git commit`、`git push`（仅推送当前分支），不创建/切换分支，不执行 `merge`、`rebase`
- `AGENTS.md`（存在时）由 AI 工具**内置自动加载**至系统提示词层，各阶段 AI 角色无需主动读取。尚未生成时不读取

---

## 整体流程

```
阶段一: SPEC.md
  │
  ├──→ 阶段 T-1: ACCEPTANCE.md ──────────────────────→ 阶段 T-2: tests/e2e/ ──┐
  │                                                                          │
  └──→ 阶段二: ARCHITECTURE.md → 阶段三: 模块设计 ─────→ 阶段四: PLAN.md ──────┤
                    AGENTS.md     API.md+DESIGN.md                           │
                                                                             │
                                                                          最终定稿
```

> **注**：T-2（验收脚本生成）须等待阶段三全部 `API.md` 定稿后方可执行，与阶段四（PLAN.md）可并行。

### 核心约束

- 每个阶段以人类明确回复"定稿"为晋级条件
- 阶段三中：每个模块由独立的 subagent 按依赖顺序串行完成设计，全部模块一次性完成，每个模块之间不穿插人类评审。全部模块设计完成后，由人类评审
- 所有文档使用人类指定的统一语言

---


## 变更传播协议

当需求或设计需要修改时：

1. **标记影响范围**：评估受变更影响的文档（SPEC / ARCH / API / DESIGN / PLAN / ACCEPTANCE / tests/e2e）
2. **保存旧状态**：在当前分支 `git add -A && git commit -m "snapshot: pre-change backup"`
3. **修改源头文档**：从受影响的最上游文档开始修改（需求变更 → SPEC.md；架构变更 → ARCHITECTURE.md）
4. **级联更新**：
   - `SPEC.md` 变更 → 评审是否需要更新 `ARCHITECTURE.md` → 受影响模块的 `API.md` / `DESIGN.md`；同时评审 `ACCEPTANCE.md` 中的验收场景是否需要同步更新
   - `ARCHITECTURE.md` 变更 → 评审各 `API.md` / `DESIGN.md` 是否需要同步更新；如涉及模块结构变更（增删模块、重命名），同步更新 `AGENTS.md` 中的模块目录说明
   - `API.md` / `DESIGN.md` 变更 → 更新 `PLAN.md` 中的引用关系，确保 `[module-name/DESIGN.md#{MODULE}-F{NNN}]` 可追溯链完整；如果 `API.md` 接口签名变更，同步更新 `tests/e2e/` 中的对应验收测试代码
   - `ACCEPTANCE.md` 变更 → 评审 `tests/e2e/` 中的对应验收测试代码是否需要同步更新
    - `SKILL.md` 变更 → 同步更新 frontmatter 中的 `metadata.version` 字段，并同步更新根 `package.json` 的 `version` 字段（版本一致性由仓库级测试保障，两处须同时修改）
5. **重新评审**：仅重新评审受影响的文档和模块

---

## 与编码阶段的关系

本技能产出的文档作为编码阶段的契约依据：

- AI 开发工具 **默认会自动加载 `AGENTS.md`** 了解项目规则
- 然后根据当前要开发的模块，读取 `ARCHITECTURE.md`（公共设计部分）+ 当前模块的 `API.md` 和 `DESIGN.md` + 所依赖模块的 `API.md`
- 通过 `PLAN.md` 了解任务优先级和完成状态
- 严格遵循 `API.md` 中的接口定义和 `DESIGN.md` 中的实现规范实现代码
- **跨模块接口变更必须升级给人类仲裁**，不允许编码阶段私自修改接口契约。跨模块接口变更包括但不限于：接口签名变更（HTTP 方法/路径、参数名/类型/必选性）、请求/响应数据结构变更（新增必选字段、删除字段、修改字段类型）、错误码新增/删除/语义变更、接口废弃或移除。新增接口（不修改已有契约的定义）和新增可选字段不视为跨模块接口变更

测试体系的两层职责划分记录于 AGENTS.md 的「开发阶段测试规范」（UT/组件/集成，由 Architect Agent 在阶段二写入）与「验收测试规范」（E2E，由 TE Agent 在 T-1 阶段写入）两个章节。

编码阶段全部任务标记为 `[x]` 后，须执行**最终验收门禁**：
1. 执行 `tests/e2e/` 下的全部验收测试
2. 根据 `ACCEPTANCE.md` 判断每项失败是测试问题（类型 A）还是产品缺陷（类型 B）
3. 对类型 B 的失败，按结构化失败元数据中的 `module` / `featureIds` 追溯至对应模块，按串行方式逐模块启动 subagent 修复
4. 全部通过 = 项目完成

---

## 项目结构验证

本技能自带 OpenSDD 结构合规性检查工具 `opensdd-check`（位于 `opensdd/opensdd-check/`）。它是三层质量门禁的 Layer 1 自动化层，供人类手动执行或 AI 在 `finalization.md` 流程中调用。

- 人类手动执行：`node <技能目录>/opensdd-check/index.js`（默认检查当前目录）
- 指定项目路径：`node <技能目录>/opensdd-check/index.js --path <项目根目录>`
- 严格模式（将所有警告视为错误）：`node <技能目录>/opensdd-check/index.js --strict`

**AI 行为约束**：人类意图为 opensdd 合规检查时，AI 必须加载 `finalization.md` 执行完整三层质量门禁，不得跳过任何层或自行创建替代方案。

---

## 阶段自动触发条件

各阶段由 AI 根据用户意图自动匹配加载对应的 phase 文件，无需人类手动指定阶段编号。触发场景和前置门禁列中的文件存在性检查用于判断是否应加载该阶段：

| 阶段 | phase 文件 | 角色 | 典型触发场景 | 前置门禁 |
|------|------|------|-------------|----------|
| 阶段一：需求规格 | [phase-1.md](phase-1.md) | PM Agent | 人类表达需求定义、项目规划等意图，且 `docs/SPEC.md` 不存在 | 无（项目起点） |
| 阶段 T-1：验收规格 | [phase-T.md](phase-T.md) | TE Agent | 人类表达验收场景定义等意图，且 `docs/ACCEPTANCE.md` 不存在 | `docs/SPEC.md` 已定稿 |
| 阶段二：总体架构设计 | [phase-2.md](phase-2.md) | Architect Agent | 人类表达架构设计、技术选型等意图，且 `docs/ARCHITECTURE.md` 不存在 | `docs/SPEC.md` 已定稿 |
| 阶段三：模块详细设计 | [phase-3.md](phase-3.md) | Designer Agent | 人类表达模块设计、接口定义等意图，且对应模块 `API.md`/`DESIGN.md` 不存在 | `docs/ARCHITECTURE.md` 已定稿 |
| 阶段 T-2：验收脚本 | [phase-T.md](phase-T.md) | TE Agent | 人类表达生成验收测试代码等意图，且 `tests/e2e/` 不存在 | `docs/ACCEPTANCE.md` + 各模块 `API.md` 均已定稿 |
| 阶段四：任务计划 | [phase-4.md](phase-4.md) | Project Manager Agent | 人类表达任务拆分、计划排期等意图，且 `docs/PLAN.md` 不存在 | 各模块设计均已定稿 |
| 项目质量审查 / 最终定稿 | [finalization.md](finalization.md) | AI（三层门禁）/ 人类 | 人类表达"检查项目是否符合opensdd规范""opensdd合规性检查""用opensdd技能审视项目""opensdd最终定稿"等 opensdd 特定意图 | 无（检查范围由文档存在性自适应级联） |

**触发规则**：
- **意图清晰时**：AI 结合用户当前意图和项目文档实际状态综合判断应加载的阶段
- **意图模糊时**：AI 不得猜测，应向人类反馈当前项目文档状态并提供可选阶段供选择，人类给出明确指示后才执行动作
- **前置门禁不满足时**：AI 应告知人类当前完成状态和下一步建议，不跨阶段加载
- **会话已有阶段产物时**：AI 应提示人类完成当前阶段的评审定稿后再启动新阶段，不在同一会话中跨阶段执行
- **phase 文件优先加载**：AI 匹配触发条件后，必须先加载对应 phase 文件，由其定义的流程决定后续操作。不得跳过加载直接执行工具或自行判断

执行时须严格遵守对应 phase 文件中定义的角色职责、上下文范围、输入输出和晋级条件。
