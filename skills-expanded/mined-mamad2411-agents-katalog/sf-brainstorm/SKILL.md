---
name: sf-brainstorm
description: 对模糊产品想法、UI/AI/技术方向或范围取舍做用户参与式头脑风暴；用于进入 PRD、requirements 或 technical_design 前先形成可确认的候选方案、研究证据和决策记录。
---

# sf-brainstorm

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

## 运行模式检测

1. 当前目录向上存在 `.specforge/` 且有 active work item：**Embedded 模式**，按 active work item 读取 brief / PRD / requirements 并写入 `00-intake/brainstorm.md`。
2. 存在 `.specforge/` 但无 active work item：**Lightweight 模式**，只做本阶段对话式 brainstorm；需要落档时输出 `specforge-import-ready.md` 格式内容，或先路由 `sf-intake` 创建 work item。
3. 不存在 `.specforge/`：**Standalone 模式**，不要运行 `.specforge/...` 命令；产出可后续导入的 `specforge-import-ready.md` 格式内容，必须保留用户确认、未决问题和推荐项边界。

`sf-brainstorm` 是用户参与式发散和收敛阶段。它把模糊诉求、产品方向、体验方向、AI 能力边界或技术路线问题整理成可选择的方案，并明确哪些选择已被用户确认。它不替用户拍板，不写最终 requirements，不实现代码。

## 启动

1. 读取 `.specforge/AGENTS.md`。
2. 读取 `.specforge/registry.yaml`，确认是否已有 active work item。
3. 有 active work item 时，读取 `00-intake/original-request.md`、`00-intake/brief.md`、可选 `00-intake/prd.md` 和已有 `00-intake/brainstorm.md`。
4. 无 active work item 时，只做对话式 brainstorm；若用户要落档，先路由到 `sf-intake` 创建 work item。
5. 读取 `.specforge/core/workflows/stages/brainstorm/SKILL.md`。

## 关联标准

- `.specforge/core/standards/workflow.md`：scope、artifact 边界和 gate 纪律。
- `.specforge/core/standards/product.md`：候选池、MVP、PRD 和 requirements 边界。
- 有 UI 方向时读取 `.specforge/core/standards/design.md`。
- 有技术选型或依赖版本问题时读取 `.specforge/core/standards/engineering.md`。
- `.specforge/core/skills/ORCHESTRATION.md`：第三方参考能力的总编排规则。
- `references/external-skills.md`：本 skill 的第三方 skill 选择表、读取深度和归一化格式。

## 第三方 Skill 联动

先读取 `.specforge/core/skills/ORCHESTRATION.md`。当本轮 brainstorm 需要第三方方法卡时，再读取本 skill 目录下的 `references/external-skills.md`，按其中的选择表决定使用哪个 skill、读到什么深度、归一化到哪里。

常见参考包括：

- `opportunity-solution-tree`：产品目标、用户机会、MVP、候选方向、实验和优先级取舍。
- `ux-designer`：体验方向、用户旅程、信息架构、交互和可访问性。
- `deep-research`：多来源研究、共识/争议和研究空白。
- `user-stories`：用户故事、验收口径和边界条件。
- `create-prd`：PRD handoff 检查、非目标和 release 分期覆盖。
- `playwright-skill`：只在 brainstorm 需要提前识别验证风险时参考，正式执行仍交给后续阶段。

第三方 skill 的输出必须先归一化为 `问题地图 / 方案对比 / 用户确认记录 / 后续阶段输入`。它不能替代事实查证，不能替代用户确认，也不能原样落入 `brainstorm.md`。

## 何时使用

- 用户说“先 brainstorm / 头脑风暴 / 我还没想清楚 / 你帮我想想”。
- intake 发现产品、页面、全栈应用、AI 能力、多角色流程、审批、权限、数据生命周期等方向尚未确认。
- PRD、requirements、UI design 或 technical_design 中出现会改变方向的 `[NEEDS ... DECISION]`。
- `instructions.mjs` 返回 `ui-direction-unconfirmed`，表示 UI / 视觉 / 体验方向还没有用户确认，必须先让用户取舍。
- `instructions.mjs` 返回 `tech-direction-unconfirmed`，表示新项目 / 空仓库路径的技术栈、数据库、调度器、AI provider、部署或依赖方向还没有用户确认，必须先让用户取舍。
- `instructions.mjs` 返回 `dependency-decision-unconfirmed`，表示本次可能新增 / 替换直接依赖、SDK、插件、组件库、ORM、驱动、测试库或外部 provider，但还没有用户确认。
- `instructions.mjs` 返回 `tooling-decision-unconfirmed`，表示本次可能选择 / 替换包管理器、UI 组件库、样式方案、Python 依赖管理 / 虚拟环境、构建工具、测试 runner、任务运行器或 monorepo 工具，但还没有用户确认。
- 技术选型不是显而易见的项目既有约束，需要和用户确认框架、版本、部署、成本、长期维护取舍。

## 边界

| 阶段 | 负责 | 不负责 |
|---|---|---|
| `sf-intake` | 创建/选择 work item、分类 workflow、写 brief 初稿 | 深入展开方案 |
| `sf-brainstorm` | 发散候选、查证当前事实、让用户做关键取舍 | 写最终规格或自动拍板 |
| `sf-prd` | 把已确认产品方向整理成 PRD | 重新发散所有可能 |
| `sf-requirements` | 把 PRD/brief 转成可测试行为和 AC | 做产品路线选择 |
| `sf-tech-design` | 把已确认技术方向细化为架构设计 | 在未确认情况下自动选型 |

## 铁律（不可越过）

```
每次只问一个问题。用户回答之前不得提出下一个问题。
```

把多个问题打包成「还有什么想法？」不是 brainstorm，是在逃避 brainstorm。

## Socratic 对话协议

**第一步：建立问题地图（内部，不输出给用户）**

内部将所有待确认事项分三类：
- `[已明确]` 用户已说过的、代码库已存在的
- `[必须确认]` 会改变架构/体验/成本/范围的高影响决策
- `[可安全默认]` 技术社区有明显最优解、低风险、后期可调整的

硬规则：

- 若对某项是否“明显最优”存在任何不确定，强制划入 `[必须确认]`，不得自行归入 `[可安全默认]`。
- 将所有 `[必须确认]` 按以下维度顺序排列：核心目标/范围 > 体验方向 > 数据与安全 > 集成与依赖 > 交付验收。依次提问，不得跳跃。
- 每轮对话结束前自检：是否还有未解决的高影响问题？如有，补写对应 `[NEEDS ... DECISION]` 后再输出回复或路由。

**`[必须确认]` 问题优先级排序（从高到低依次问）：**

1. **核心目标/范围**：这是为谁做的？解决什么核心问题？MVP 做什么，明确不做什么？
2. **体验方向**（有 UI 时）：什么感觉？参考哪类产品？主要用户是什么角色？
3. **数据与安全**：谁能看到数据？数据生命周期如何？有没有敏感数据或合规要求？
4. **集成与依赖**：会依赖哪些外部系统或服务？现有系统有哪些约束？
5. **交付验收**：怎么算做完？用户通过什么操作验证功能正常？

**正确的提问格式：**
1. 先给 1 句背景（为什么要问这个）
2. 提供 2-3 个选项（真实权衡，不是假选项）
3. 结尾清楚提问，等待回答

好的提问示例：
```
这个审批流需要支持多少人同时使用？这会影响我们选简单队列还是分布式事务。
A) 小团队（< 50 人并发）→ 简单队列即可
B) 中等规模（50-500 人）→ 需要考虑锁策略
C) 不确定 → 先按 B 设计，留扩展点

你们现在大概是哪种情况？
```

提问前检查：

- 本轮只包含一个会改变方向的问题。
- 选项之间有真实权衡，不只是同一建议的不同措辞。
- 问题不能太开放；用户看完选项后应能直接选择、组合或修正。
- 涉及技术栈、前端、后端、数据库、部署等多个维度时，按优先级拆成多轮问。

**收敛信号（满足全部才能进入下一阶段）：**
- ✅ 所有 `[必须确认]` 事项有用户答案或明确授权默认
- ✅ MVP 范围已明确（做什么，不做什么）
- ✅ 高风险决策（数据安全、成本模型、不可逆架构选择）已有结论
- ✅ 用户知道下一步是什么
- ❌ 任何 `[NEEDS ... DECISION]` 标记存在 → 不得宣布收敛

## 正向执行断言

- 沉默不是确认；必须等到用户给出明确答复才能继续。
- 会影响架构、体验、成本或范围的问题，现在就要问，不能推给后续阶段。
- 用户说“你来决定”时，必须写明授权内容、推荐理由、风险和回退点。
- 每轮只问一个会改变方向的问题；多问会降低答案质量。
- 对 Agent 明显不等于对用户明显；只要不确定，就归入 `[必须确认]`。

## 执行序列

### A. 启动时做一次

1. 读取 active work item 的 original request、brief、可选 PRD / requirements / UI / technical design 和已有 brainstorm。
2. 读取 `brief.md#Brainstorm 决策` 的模式，决定本轮深度：
   - `skip`：无需用户参与式取舍，记录跳过理由并回到 brief 指定下一步。
   - `light`：直接框定问题、给 2-3 个候选并收敛，不做五维全量发散。
   - `deep`：先做 Phase 1 发散，再做 Phase 2 聚焦。
   - 模式来源见 `sf-intake` 的“Brainstorm 分流规则”和 `core/artifacts/templates/brief.md#Brainstorm 决策`。
3. 需要当前事实时先查证；技术类优先官方资料，并记录日期。
4. 需要第三方方法卡时，按 `references/external-skills.md` 选择并读取最小必要内容；只把它转成候选、风险、问题地图或后续阶段输入，不把第三方输出直接当结论。
5. 建立问题地图：`[已明确] / [必须确认] / [可安全默认]`。
6. 按固定维度排序 `[必须确认]`：核心目标/范围 > 体验方向 > 数据与安全 > 集成与依赖 > 交付验收。

### B. 每轮对话循环

1. 只选择当前排序最高的一个 `[必须确认]` 问题。
2. 用“背景 1 句 + 2-3 个真实选项 + 清楚提问”的格式提问。
3. 等用户回答；不要同时抛下一个问题。
4. 用户明确确认后，立即更新确认记录：
   - UI / 视觉 / 体验方向：写 `UI Direction Status: confirmed` 或真实 `[UI DECISION CONFIRMED]`。
   - 技术栈 / 架构 / 数据库 / 调度器 / AI provider / 部署方向：写 `Tech Direction Status: confirmed` 或真实 `[TECH DECISION CONFIRMED]`；用户授权默认写 `Tech Direction Status: delegated_default`。
   - 新增 / 替换依赖：写 `Dependency Decision Status: confirmed` 或真实 `[DEPENDENCY DECISION CONFIRMED]`；用户授权默认写 `Dependency Decision Status: delegated_default`。
   - 工程工具链：写 `Tooling Decision Status: confirmed` 或真实 `[TOOLING DECISION CONFIRMED]`；用户授权默认写 `Tooling Decision Status: delegated_default`；沿用现有栈写 `Tooling Decision Status: existing_stack`。
5. 用户没有确认时，保留 pending，并补写对应 `[NEEDS ... DECISION]`。
6. 每轮回复前自检：是否还有未解决的高影响问题？如果有，不得宣布收敛。
7. 每轮结束都更新阶段记录：Embedded 模式写入 `00-intake/brainstorm.md` 并同步 `00-intake/brief.md`；Standalone / Lightweight 模式写入 `specforge-import-ready.md` 格式内容。

### C. 收敛时做一次

1. 写入或更新 `00-intake/brainstorm.md`：问题地图、事实证据、方案对比、推荐项、用户确认、明确延后 / 不做、未决问题。
2. 同步更新 `00-intake/brief.md`：澄清记录、功能候选池、用户选择、外部研究摘要、PRD 决策和 Brainstorm 决策。
3. 确认没有 `[NEEDS ... DECISION]` 阻断项；如仍有阻断项，输出暂停原因而不是路由到下游。

## 判定表

| 条件 | 状态 |
|---|---|
| 没有 active work item，且用户要求落档但尚未创建 work item | 停止：需先创建 work item |
| 用户尚未确认 MVP、核心方案、关键技术路线或不能安全默认的边界 | 停止：继续 Socratic 单问 |
| 需要当前事实支撑的判断尚未完成研究 | 停止：先补事实来源 |
| 方案之间成本、风险或用户价值差异未说明清楚 | 停止：补方案对比 |
| 任何 `[NEEDS ... DECISION]` 仍存在 | 停止：不得宣布收敛 |
| 用户确认的选择、授权默认、Agent recommendation 和未决问题已分清 | 完成条件之一 |
| `brainstorm.md` 足以支撑 PRD、requirements、UI design 或 technical design 继续推进 | 完成条件之一 |
| `brief.md` 已同步，所有 `[NEEDS ... DECISION]` 已清除 | 完成 |

## 停止条件

以“判定表”为准。任一停止条件命中时，不进入下游阶段。

## 完成标准

以”判定表”为准。只有完成条件全部满足，才能输出下一步路由。
- 完成后运行 `node .specforge/core/scripts/instructions.mjs`，将输出展示给用户，让用户知道当前 workflow 的下一步是什么。

## 不做

- 不直接写最终 requirements。
- 不直接实现代码。
- 不在用户未确认时把推荐方案写成已批准。
