---
name: sf-intake
description: 为新请求创建或整理 SpecForge work item；用于用户提出新需求、bug、issue、重构、预研、低风险小改或边界不清的工作，需要分类 workflow、决定是否需要 PRD、校准 components flags，并写出可支撑下一步的 brief 时。
---

# sf-intake

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

## 运行模式检测

1. 当前目录向上存在 `.specforge/` 且有 active work item：**Embedded 模式**，按 artifact graph 写入正式 work item。
2. 存在 `.specforge/` 但无 active work item：**Lightweight 模式**，可以创建 work item；如果用户只想先整理想法，则输出 `specforge-import-ready.md` 格式内容。
3. 不存在 `.specforge/`：**Standalone 模式**，不要运行 `.specforge/...` 命令；用对话完成 intake 分类和 brief 草稿，输出 `specforge-import-ready.md` 格式内容，后续可在初始化后导入。

`sf-intake` 是分诊入口：判断 work item 类型、workflow、是否需要 PRD、是否需要 research、影响面 flags、是否需要拆分，并识别是否需要进入 `sf-brainstorm`。它负责 intake，不负责写完整 PRD、requirements、设计或实现代码。

## 必读

- `references/routing.md`：workflow 分类、brainstorm 分流、PRD 决策、follow-up 和 components flags。
- `.specforge/core/workflows/stages/discovery/SKILL.md`：discovery / research 输入输出和停止条件。
- `.specforge/core/workflows/stages/brainstorm/SKILL.md`：需要用户参与式取舍时的阶段母本。
- `.specforge/core/standards/workflow.md`：上下文加载、workflow 分类、scope、命名和 gate 边界。
- `.specforge/core/standards/product.md`：分析深度、PRD 决策、功能候选池、澄清和需求可测试性。

## 启动扫描

1. 读取 `.specforge/AGENTS.md`。
2. 读取 `.specforge/registry.yaml`。
3. 先读取 `.specforge/wiki/00-index.md`，再读取和请求相关的 `.specforge/wiki/` 长期事实；只读相关文件。
4. 运行 `node .specforge/core/scripts/status.mjs`，确认 active work item 数量。
5. 如果是已有代码项目或用户请求触碰既有模块，先判断 wiki 是否能给出相关模块、入口、API、数据、运行或风险线索。只有 wiki 缺基线、过期、冲突或无法覆盖本次请求时，才运行 `node .specforge/core/scripts/codebase-index.mjs --json` 并考虑路由 `sf-steering`。

## 执行序列

### A. 先分诊

1. 按 `references/routing.md#分诊顺序` 判断 active work item、拆分、kind、workflow、存量项目前置、PRD、components flags 和下一步。
2. 多个 active work item 时先让用户指定，不猜。
3. 混合请求先拆分，不创建万能 work item。
4. 已完成或 archive work item 的后续问题，按 follow-up 新建，并保留 parent/relation。

### A1. Workflow 协作选择

Workflow 类型由 AI 和用户共同确认，不由 AI 单方面决定：

1. 根据 `references/routing.md#Workflow 分类表` 推断最可能的 workflow 类型。
2. 向用户展示推荐结果和理由，格式：
   - 推荐：`<workflow>` — 一句话理由
   - 备选：`<workflow>` — 适用条件
3. 等待用户确认或纠正；用户说"你来定"时，写明授权内容和风险，再继续。
4. 用户确认后才写入 `work.yaml`，不提前创建。

### B. 再创建或整理 work item

没有 active work item 时创建：

```bash
node .specforge/core/scripts/create-work.mjs --workflow <workflow> "Work item title"
```

可在创建时直接声明已知影响面：

```bash
node .specforge/core/scripts/create-work.mjs --workflow feature --has-ui true --has-api true --has-db false "Work item title"
```

如果是已完成 work item 的后续问题，带上关联：

```bash
node .specforge/core/scripts/create-work.mjs --workflow issue --kind issue --parent <previous-work-id> --relation follow_up "排查提交审批失败"
```

### C. 写 intake 产物

写清：

- `00-intake/original-request.md`
- `00-intake/brief.md`

`brief.md` 必须包含：

- 背景和目标。
- PRD 决策：是否需要 PRD、深度、原因和下一步。
- Brainstorm 决策：`skip / light / deep`、原因和阻断项。
- 分析深度、代码库探索、外部研究或跳过理由、澄清记录和分析综合。
- Wiki 上下文入口：本次读取的 wiki 文件、入口路径、相关模块、上游 / 下游和需要补证的缺口。
- 候选功能池、推荐 MVP、用户已确认选择和明确延后项。
- 本次负责 / 不负责。
- 影响面矩阵：UI、frontend、backend、API、data、AI、integration、security、delivery、tests。
- 依赖、风险、澄清项。

### D. 校准 flags 和路由

1. 更新 `work.yaml` 中的 `workflow`、`kind`、`components` 和 relations。
2. 不确定的组件 flag 保持 `auto`；明确无影响才写 `false`。
3. 运行 `node .specforge/core/scripts/instructions.mjs`，确认 flags 和 workflow 已正确写入。

## 判定表

| 条件 | 状态 |
|---|---|
| 多个 active work item，且用户未指定 | 停止：先请用户指定 |
| 需求边界不清，无法判断 workflow | 停止：提一个关键澄清问题 |
| 产品 / 页面 / 全栈应用的 MVP 功能组合尚未确认，且无法安全默认 | 停止：需先完成方向取舍 |
| 已有代码项目缺少 wiki 基线 | 停止：需先建立 wiki |
| 需求触碰既有模块但 wiki 没有入口或明显过期 | 停止：路由 `sf-steering` 补齐项目画像 |
| 产品型 work item 需要 PRD，但缺少核心产品决策 | 停止：需先澄清产品方向 |
| `standard` / `deep` 缺少代码库探索证据或明确跳过原因 | 停止：补探索或写跳过理由 |
| `deep` 缺少外部研究证据或明确跳过原因 | 停止：补研究或写跳过理由 |
| 存在生产、安全、权限、数据迁移风险但没有足够上下文 | 停止：澄清或路由 discovery |

## 完成标准

- work item 已进入 `.specforge/work/active/`，或 Standalone / Lightweight 模式下输出了可导入内容。
- brief 足以支撑 PRD 或 requirements。
- PRD 决策清楚：需要就标记 `PRD required: yes`，不需要就写明跳过理由。
- Brainstorm 决策清楚：`skip / light / deep` 有理由。
- `work.yaml` 的 `workflow` 和 `components` 已与 brief 影响面矩阵一致。
- 完成后运行 `node .specforge/core/scripts/instructions.mjs`，将输出展示给用户，让用户知道当前 workflow 的下一步是什么。

## 不做

- 不直接实现。
- 不写完整 PRD、requirements、UI design 或 technical design。
- 不手工绕过 artifact graph；是否跳过 ui_design / technical_design 由 `components` 和 workflow schema 共同决定。
- 不把 Agent 推荐方案写成用户已确认选择。
