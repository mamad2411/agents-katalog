---
name: sf-router
description: SpecForge 工作流根入口。用于用户只说“sf”、询问当前到哪一步、提出新需求、说继续、想自动推进或不知道该用哪个 SpecForge 能力时；本技能只扫描仓库、判断状态并路由到一个 sf-* 子技能。
---

# sf-router

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

## 启动必读

开始任何判断前，先检查当前仓库是否接入 SpecForge：

1. 看是否存在 `.specforge/`。
2. 存在时读取 `.specforge/AGENTS.md`；缺失则提示骨架不完整，先补齐或运行 `sf-onboard`。
3. 运行 `node .specforge/core/scripts/doctor.mjs`。
4. 有 active work item 时，再运行 `node .specforge/core/scripts/instructions.mjs`。

`sf-router` 只做路由，不写规格、不实现代码、不批准 gate。用户只说“继续”时，默认路由到当前 ready artifact 对应的单个 `sf-*` 技能；只有用户明确说“继续做完 / 自动推进 / 不要停”时，才路由到 `sf-work`。

路由判断必须以当前文件和工具输出为准，不以聊天记忆为准。遇到 gate `REQUEST_CHANGES`、关键 `unknown`、缺 evidence 或多个 active work item 时，先输出阻断和目标技能，不自动推进。

## 内部技能母本

- 状态判断优先读取 `.specforge/core/workflows/stages/status/SKILL.md`。
- 新请求分诊或 discovery 判断优先读取 `.specforge/core/workflows/stages/discovery/SKILL.md`。
- 模糊产品、UI、AI 或技术路线取舍优先读取 `.specforge/core/workflows/stages/brainstorm/SKILL.md`。
- 根级 skill 只负责扫描和路由；阶段行为以对应内部 skill 为准。

## 体系速读

SpecForge 分成两层：

```text
AI 工具技能：sf-router / sf-*  负责让 AI 工具知道怎么工作，可 user scope 或 project scope 安装
项目目录：.specforge/          保存 core、wiki、hooks、项目事实和 work item
```

在 Agent 技能列表里输入 `sf` 前缀，应能看到 `sf-router` 和所有 `sf-*` 生命周期技能。

项目接入后只落一个目录：

```text
.specforge/
├── AGENTS.md
├── manifest.yaml
├── registry.yaml
├── core/
│   ├── standards/
│   ├── profiles/
│   ├── workflows/
│   ├── artifacts/
│   ├── scripts/
│   ├── skills/
│   └── hooks/
├── hooks/
│   └── local/
├── wiki/
└── work/
    ├── inbox/
    ├── active/
    └── archive/
```

## 场景路由表

| 用户说什么 / 当前状态 | 路由到 |
|---|---|
| 仓库没有 `.specforge/` | `sf-onboard` |
| 问“现在到哪一步 / 健康状态 / 能不能继续” | `sf-doctor` |
| 用户要求“理解项目 / 扫描项目 / 项目画像 / 架构地图 / 存量项目基线” | `sf-steering` |
| 提出新需求、新 issue、新 bug、重构想法，且没有 active work item | `sf-intake` |
| 用户要求“brainstorm / 头脑风暴 / 先讨论方案 / 帮我想想”，或现有 spec 出现未确认的产品、UI、AI、技术路线取舍 | `sf-brainstorm` |
| 用户要求 review / 检查任一已有 spec、需求、PRD、UI design、tech design 或 tasks | `sf-spec-review` 的 Artifact Review 模式 |
| 只有一个 active work item，用户只说“继续 / 下一步” | 运行 `instructions.mjs` 后按 ready artifact 路由 |
| active work item 需要深度分析 / brief 不足以支撑 requirements | `sf-discovery` |
| active work item 的 MVP、方案、UI 方向、AI 能力边界或技术路线尚未被用户确认 | `sf-brainstorm` |
| active work item 下一步是 gap_report / research | `sf-discovery` |
| active work item 是产品型，需要对齐产品目标和功能边界 | `sf-prd` |
| active work item 下一步是 requirements | `sf-requirements` |
| active work item 下一步是 ui_design | `sf-ui-design` |
| active work item 下一步是 technical_design | `sf-tech-design` |
| active work item 下一步是 tasks | `sf-tasking` |
| active work item 下一步是 spec_review gate | `sf-spec-review` |
| spec_review 已批准，准备写代码 | `sf-implement` |
| 下一步是 code_review gate | `sf-code-review` |
| code_review 已批准，需要测试和证据 | `sf-verify` |
| 用户要求“更新 wiki / 回写知识库 / 同步长期事实” | `sf-wiki` |
| 下一步是 wiki_sync | `sf-wiki` |
| 下一步是 closure，或 wiki_sync 已批准后需要 release / rollback / archive | `sf-close` |
| 用户明确说“继续做完 / 自动推进 / 不要停” | `sf-work` |
| 任一 gate 为 `REQUEST_CHANGES` / `REJECTED` | 读取对应 review/report，路由回负责修复的 `sf-*` |

## 路由决策树

1. 检查 `.specforge/` 是否存在。
   - 不存在：路由到 `sf-onboard`。
2. 读取 `.specforge/registry.yaml`。
   - 用户明确要求理解存量项目、刷新项目画像或补齐大型代码库上下文：路由到 `sf-steering`。
   - 没有 active work item，且用户提出新需求 / bug / 重构：路由到 `sf-intake`。
   - 没有 active work item，且用户问状态：路由到 `sf-doctor`。
3. 有多个 active work item。
   - 列出 active work item 的 id、title、status、path。
   - 要求用户指定要继续哪一个，不要猜。
4. 有一个 active work item。
   - 读取 `00-intake/brief.md` 和可选 `00-intake/prd.md`。
   - 运行 `node .specforge/core/scripts/instructions.mjs`。
   - 先检查 gate 状态：
     - `spec_review=REQUEST_CHANGES/REJECTED`：读取 `02-spec-review/spec-review-v1.md` 的 `Return to` 字段，路由到对应阶段；无法判断时路由到 `sf-spec-review` 解释阻断。
     - `code_review=REQUEST_CHANGES/REJECTED`：路由到实现修复阶段；如果 finding 指向 spec 缺口，按 review 的 return path 路由到对应 spec 阶段。
     - `verification=REQUEST_CHANGES/REJECTED`：优先路由到实现修复阶段；若只是缺证据且实现未变，路由到验证阶段重跑。
     - `wiki_sync=REQUEST_CHANGES/REJECTED`：路由到 wiki 同步阶段。
   - 如果 `brief.md`、`prd.md`、`requirements.md`、`ui-design.md` 或 `technical-design.md` 中存在 `[NEEDS DECISION]`、`[NEEDS PRODUCT DECISION]`、`[NEEDS UI DECISION]`、`[NEEDS TECH DECISION]` 且问题需要用户取舍，先路由到 `sf-brainstorm`，不要替用户拍板。
   - 如果 ready artifact 是 `requirements`，但 `brief.md#PRD 决策` 标记 `PRD required: yes` 或表格中 `PRD required | yes`，且 `00-intake/prd.md` 不存在、`Decision Status` 不是 `approved-for-requirements`，或仍有 `[NEEDS PRODUCT DECISION]`，先路由到 `sf-prd`，不要直接进入 `sf-requirements`。
   - 如果 `instructions.mjs` 返回 blocker `ui-direction-unconfirmed`，先路由到 `sf-brainstorm` 做 UI / 视觉 / 体验方向取舍；不要创建 `ui-design.md` 或 Pencil 原型。
   - 如果 `instructions.mjs` 返回 blocker `tech-direction-unconfirmed`，先路由到 `sf-brainstorm` 做技术栈 / 数据库 / 调度器 / AI provider / 部署 / 依赖方向取舍；不要创建 `technical-design.md`。
   - 如果 `instructions.mjs` 返回 blocker `dependency-decision-unconfirmed`，先路由到 `sf-brainstorm` 确认新增 / 替换依赖、SDK、插件、组件库、ORM、驱动、测试库或外部 provider；不要创建 `technical-design.md`。
   - 如果 `instructions.mjs` 返回 blocker `tooling-decision-unconfirmed`，先路由到 `sf-brainstorm` 确认包管理器、UI 组件库、样式方案、Python 依赖管理 / 虚拟环境、构建工具、测试 runner、任务运行器或 monorepo 工具；不要创建 `technical-design.md`。
   - 如果 ready artifact 是 `tasks` / `spec_review` / `implementation`，但 `technical-design.md` 仍有 `[NEEDS TECH DECISION]`、`[NEEDS DEPENDENCY DECISION]` 或 `[NEEDS TOOLING DECISION]`，先路由到 `sf-tech-design` 确认技术选型、新增依赖或工具链。
   - 如果 ready artifact 是 `tasks` / `spec_review` / `implementation`，但 `technical-design.md` 的 `Core Decision Review Status` 不是 `confirmed`、`delegated_default` 或 `not_required`，先路由到 `sf-tech-design` 展示核心决策摘要并等待确认。
   - 如果 ready artifact 是 `implementation`，但 `01-spec/tasks.md` 缺少 `_Impact:_` 或 `technical-design.md#0` 仍有关键 `unknown`，先路由到 `sf-tasking` 或 `sf-tech-design`，不要进入 `sf-implement`。
   - 如果 ready artifact 是 `closure`，但 `06-close/wiki-sync.md` 未证明唯一 current wiki、release / rollback 未覆盖 verification 残余风险，路由到 `sf-close` 并标明阻断点。
   - 根据 ready artifact 路由：
     - `requirements` → `sf-requirements`
     - `gap_report` → `sf-discovery`
     - `research` → `sf-discovery`
     - `ui_design` → `sf-ui-design`
     - `technical_design` → `sf-tech-design`
     - `tasks` → `sf-tasking`
     - `spec_review` → `sf-spec-review`
     - `implementation` → `sf-implement`
     - `code_review` → `sf-code-review`
     - `verification` → `sf-verify`
     - `wiki_sync` → `sf-wiki`
     - `closure` → `sf-close`
   - 如果没有 ready artifact，运行 `node .specforge/core/scripts/artifact-graph-status.mjs` 并路由到 `sf-doctor` 解释状态。
5. 用户明确要求自动推进。
   - 路由到 `sf-work`。
   - 仍然必须保留 doctor、instructions、gate evidence 和 verification 检查。

根路由只推荐下一步，不直接替子技能写产物。

## Spec Review 随时调用规则

`sf-spec-review` 不只属于最终 gate。只要用户要求审查任何已有 spec artifact，就路由到 `sf-spec-review` 的 Artifact Review 模式；不要因为 `requirements`、`ui_design`、`technical_design` 或 `tasks` 尚未全部完成而拒绝审查。

Artifact Review 不更新 gate，也不要求 ready artifact 为 `spec_review`。只有 ready artifact 是 `spec_review` 或用户明确要求执行 gate 时，才进入 Gate Review 并更新 `spec_review` gate。

## 扫描时必须关联的标准

- 状态判断：`.specforge/core/standards/workflow.md`
- 产品 / PRD 分流：`.specforge/core/standards/product.md`
- UI 分流：`.specforge/core/standards/design.md`
- 技术 / 实现 / 验证分流：`.specforge/core/standards/engineering.md`
- Wiki / close 分流：`.specforge/core/standards/wiki.md`

## 输出格式

只输出：

- 当前仓库是否接入 SpecForge。
- active work item、stage、gate 状态。
- 建议路由到哪个 `sf-*`。
- 一句话原因。
- 如果存在阻断，列出阻断 artifact / gate / 缺失 evidence。
- 如果是 `REQUEST_CHANGES`，列出应回到的 artifact / `sf-*` 技能，不要说“继续下一步”。

## 不做

- 不直接写 requirements / ui_design / technical_design / tasks。
- 不直接实现代码。
- 不批准 gate。
- 不把动态资产写到 `.specforge/` 之外。
