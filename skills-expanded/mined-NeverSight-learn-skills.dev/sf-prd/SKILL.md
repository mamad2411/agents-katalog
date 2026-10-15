---
name: sf-prd
description: 生成或更新产品需求文档（PRD）；用于产品型 work item、AI 功能、后台工具、全栈应用或高层模糊需求在 requirements 前明确核心问题、目标用户、功能候选、MVP 边界、成功指标、风险和路线图时。
---

# sf-prd

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

`sf-prd` 把 brief 的分析结论升级为可对齐产品、设计与工程的 PRD。它回答“为什么做、给谁做、第一版交付哪些价值、哪些先不做”，不替代 `sf-requirements`。requirements 才回答“系统必须表现出哪些可测试行为、边界和验收标准”。

PRD 不是固定问卷。它是一份产品决策文档：先识别当前需求最可能出错的决策点，再用少量高价值问题、候选功能池和可防守假设，把模糊想法推进到可进入 requirements 的状态。

面向 B 端、运营商、大数据、AI 应用、管理后台、数据看板、驾驶舱或任务配置平台时，使用 `references/prd-authoring-guide.md#B 端运营商 / 数据产品镜头` 补充业务 KPI、部门角色、使用频率、PC / 移动端、数据口径、接口来源、脱敏、审批和审计问题。该镜头只补足产品事实，不把 PRD 扩写成 UI design、接口设计或技术方案。

## 必读

- `references/prd-authoring-guide.md`：PRD 深度、第三方 skill 编排、访谈镜头、PRD 模板和质量标准。
- `.specforge/core/artifacts/templates/prd.md`：写入骨架。
- `.specforge/core/workflows/stages/brainstorm/SKILL.md`：候选功能池和用户确认纪律。
- `.specforge/core/workflows/stages/discovery/SKILL.md`：research / discovery 输入和跳过理由。
- `.specforge/core/standards/product.md`：PRD 决策、功能候选、MVP、目标和指标。
- `.specforge/core/standards/design.md`：用户流程和体验方向。
- `.specforge/core/standards/workflow.md`：非目标、scope 和中文协作。
- `.specforge/core/skills/ORCHESTRATION.md`、`README.md`、`registry.json`：第三方 PRD skill 的选择、边界和来源风险。

## 启动扫描

1. 运行：

```bash
node .specforge/core/scripts/status.mjs
node .specforge/core/scripts/doctor.mjs
```

2. 找到唯一 active work item；如果存在多个 active work item，先让用户指定目标，不猜。
3. 读取：
   - `00-intake/original-request.md`
   - `00-intake/brief.md`
   - `00-intake/brainstorm.md`（如果存在）
   - 已存在的 `00-intake/prd.md`（如果是更新 PRD）
   - `.specforge/wiki/` 中与产品、用户、业务、竞品、设计系统或既有架构相关的长期事实

## 执行序列

### A. 判断能否写 PRD

1. 读取 `brief.md#PRD 决策`，确认本 work item 需要 PRD。
2. 读取 `brainstorm.md` 的用户确认、明确延后和未决问题。
3. 如果需要多方案取舍但没有用户确认，暂停并向用户提问。
4. 如果原始需求仍模糊且没有可追溯确认摘要，按 `references/prd-authoring-guide.md#需求摘要确认` 先输出摘要并等待用户确认，不直接写完整 PRD。
5. 如果目标用户、核心问题、MVP 边界或高风险角色/数据/AI 质量决策缺失，按 `references/prd-authoring-guide.md#自适应产品访谈` 提出少量高价值问题。

### B. 选择深度和参考输入

1. 按 `references/prd-authoring-guide.md#PRD 深度` 选择 `prd-lite / prd-standard / prd-deep`。
2. 如需第三方参考，按 `references/prd-authoring-guide.md#第三方 PRD Skill 编排` 选择 `create-prd` 或 `opportunity-solution-tree`。
3. 第三方输出只作为候选和检查视角，必须归一化到 SpecForge PRD 结构。

### C. 裁剪候选和写 PRD

1. 先整理候选功能池，不直接替用户定 MVP。
2. 拆分 `MVP / 可选增强 / 后续版本`，写清非目标。
3. 使用 `.specforge/core/artifacts/templates/prd.md` 或 `references/prd-authoring-guide.md#PRD 模板` 写入 `00-intake/prd.md`。
4. 没有内容的章节写 `N/A` 并说明原因，不留空。
5. 可进入 requirements 时，把 `Decision Status` 写为 `approved-for-requirements`；否则写 `needs-decision` 并暂停。

### D. 回写 brief 和路由

PRD 完成后，回写或补充 `00-intake/brief.md`：

- 功能候选池。
- 用户选择。
- 影响面矩阵。
- Components flags 推荐。
- 待澄清项。
- `PRD required: yes`
- `PRD depth: <实际深度>`

不要让 `brief.md` 和 `prd.md` 在 MVP、非目标、components flags 上互相矛盾。

## 判定表

| 条件 | 状态 |
|---|---|
| 多个 active work item | 停止：请用户指定目标 |
| `brief.md#PRD 决策` 不需要 PRD | 停止：跳过本阶段，brief 已标记跳过理由 |
| 需要多方案取舍但缺少 `brainstorm.md` 或用户确认记录 | 停止：需先完成方向取舍 |
| 目标用户、核心问题或 MVP 功能边界无法确认 | 停止：提问澄清 |
| 成功指标完全缺失，且无法安全给出默认指标 | 停止：提问 |
| 存在产品方向、角色权限、合规/数据风险或 AI 质量目标冲突 | 停止：等待用户或业务负责人决策 |
| 用户要求 PRD 直接替代 requirements / UI design / technical design | 停止：说明边界 |

## 完成标准

- `00-intake/prd.md` 存在且内容足以支撑 `sf-requirements`。
- `Decision Status` 为 `approved-for-requirements`，或者明确标记为 `needs-decision` 并暂停。
- 功能边界、非目标、成功指标、风险和路线图已有用户确认或明确默认假设。
- 产品型需求的功能候选池已经裁剪为 MVP / 可选增强 / 后续版本。
- AI 功能已经写明评估策略、人工兜底、安全隐私和成本边界。
- `brief.md` 已同步，所有 `[NEEDS ... DECISION]` 已清除。
- 完成后运行 `node .specforge/core/scripts/instructions.mjs`，将输出展示给用户，让用户知道当前 workflow 的下一步是什么。

## 不做

- 不写技术方案。
- 不写接口契约、错误处理、边界条件或工程实现细节；这些进入 requirements / technical_design。
- 不把用户故事里的验收种子包装成最终 requirements；必须交给 `sf-requirements` 转译。
- 不替用户做关键产品决策；可以给推荐方案，但要标明假设并等待确认。
- 不把延后功能列入 MVP。
