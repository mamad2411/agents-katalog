---
name: sf-requirements
description: 生成或更新 SpecForge work item 的 requirements；用于 active work item ready artifact 为 requirements，或需要把 PRD / brief 转成可测试行为、边界、用户故事、验收标准和影响面 flags 时。
---

# sf-requirements

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

## 运行模式检测

1. 当前目录向上存在 `.specforge/` 且有 active work item：**Embedded 模式**，按 artifact graph 写入 `01-spec/requirements.md`。
2. 存在 `.specforge/` 但无 active work item：**Lightweight 模式**，可把用户提供的 brief / PRD 草稿整理成 requirements 草稿；需要落档时输出 `specforge-import-ready.md` 格式内容，或先路由 `sf-intake` 创建 work item。
3. 不存在 `.specforge/`：**Standalone 模式**，不要运行 `.specforge/...` 命令；输出 `specforge-import-ready.md` 格式内容，保留 SHALL 需求、AC、非目标、影响面建议和未决问题，后续由 `sf-intake` 导入。

`sf-requirements` 把 brief（和可选 PRD）升级为可测试、可审查、可路由到后续设计阶段的需求规格。它不写 UI 方案、接口方案、数据库方案或实现任务。

## 必读

- `references/requirements-authoring-guide.md`：PRD 转译、第三方 skill、访谈镜头、写作细则和 flags 回写。
- `.specforge/core/workflows/stages/requirements/SKILL.md`：内部需求质量标准、停止条件和完成标准。
- `.specforge/core/standards/product.md`：PRD 输入、候选功能、用户故事、验收标准和可测试需求。
- `.specforge/core/standards/workflow.md`：范围、非目标、写入边界和中文协作。
- `.specforge/core/skills/ORCHESTRATION.md`、`README.md`、`registry.json`：第三方 requirements skill 的选择、边界和来源风险。

## 启动扫描

1. 运行：

```bash
node .specforge/core/scripts/instructions.mjs
```

2. 确认 ready artifact 包含 `requirements`，再运行：

```bash
node .specforge/core/scripts/create-artifact.mjs requirements
```

3. 读取：
   - `00-intake/original-request.md`
   - `00-intake/brief.md`
   - `00-intake/brainstorm.md`（如果存在）
   - `00-intake/prd.md`（如果存在）
   - `.specforge/wiki/00-index.md` 和相关 `.specforge/wiki/` 文件
   - `01-spec/requirements.md`（如果是更新）

## 执行序列

### A. 检查前置门禁

1. 如果 `brief.md#PRD 决策` 标记需要 PRD，但 `00-intake/prd.md` 不存在或 `Decision Status` 不是 `approved-for-requirements`，先回到 `sf-prd`。
2. 如果存在 `brainstorm.md`，读取其中用户确认、明确延后和未决问题。
3. 如果 PRD 或 brainstorm 没有回答目标用户、MVP 边界或成功标准，按 `[NEEDS CLARIFICATION]` 标记并暂停。

### B. 转译为可测试行为

1. 按 `references/requirements-authoring-guide.md#PRD 转译规则` 显式完成 PRD 转译。
2. 从 brief 的 Wiki 上下文入口和相关 wiki 中提取既有产品规则、模块边界、API / 数据约束和已知风险，只转成需求约束或影响面，不展开全仓代码探索。
3. 把 PRD / brief 中的用户故事、候选功能和验收种子转成 `REQ-*`、`AC-*`、NFR、非目标或待澄清项。
4. 需求正文使用系统行为语言，不复制 PRD 原文，不写实现方案。
5. 如需用户故事或验收样例，按 `references/requirements-authoring-guide.md#第三方 Skill 归一化` 读取 `user-stories`。

### C. 写 requirements

1. 写入 `01-spec/requirements.md`。
2. 每条 `MUST` 需求至少有一个 `AC-*`。
3. 适用时覆盖正常路径、失败路径、空状态、边界值、权限差异和重新验证触发条件。
4. 涉及依赖或工具链选择时，写 `[NEEDS DEPENDENCY DECISION]` / `[NEEDS TOOLING DECISION]`，不要替用户选择。
5. 标出非目标、依赖、风险、重新验证触发条件和已知歧义；无法确认的行为必须写 `[NEEDS CLARIFICATION]`，不得猜测或包装成已批准规格。
6. **新增字段或数据变更时，必须枚举所有读取或展示该数据的页面**（不仅是新增/编辑表单，还包括列表页、详情页、只读视图、导出等），每个页面单独列为影响面，不得合并或遗漏。

### D. 回写 flags 和路由

1. 按 `references/requirements-authoring-guide.md#影响面回写` 校准 `work.yaml` / `brief.md` 的 components flags。

## 判定表

| 条件 | 状态 |
|---|---|
| `brief.md` 要求 PRD，但 PRD 缺失或未 approved | 停止：PRD 尚未就绪 |
| 目标用户、成功标准或范围无法判断 | 停止：澄清或补充探索 |
| intake 证据包不足以支撑需求 | 停止：补探索、研究或澄清记录 |
| 存量项目相关 wiki 缺入口且无法判断既有边界 | 停止：退回 `sf-intake` 或 `sf-steering` 补上下文 |
| 产品功能组合、目标用户或版本边界没有确认 | 停止：需先完成方向取舍 |
| 需求互相冲突 | 停止：列冲突并请求决策 |
| 验收标准无法定义 | 停止：补清触发、条件、系统响应和可见结果 |
| 需要产品或业务决策才能继续 | 停止：不要包装成已批准规格 |

## 完成标准

- `01-spec/requirements.md` 可以独立支撑后续影响面判断。
- PRD 中每个已确认 MVP 能力都能追溯到 requirements 中的需求或非目标。
- PRD 的每个验收种子都已转成最终 AC、NFR、非目标或待澄清项。
- 每个 user-visible / operator-visible 行为都有验收标准。
- 影响面 flags 已校准。
- 所有未决问题都显式标记 `[NEEDS CLARIFICATION]`、`[NEEDS DEPENDENCY DECISION]` 或 `[NEEDS TOOLING DECISION]`。
- **按需求规模裁剪**：单字段 / 单页面 / 配置类小需求，`PRD 转译边界`、`行为覆盖矩阵`、`用户流程` 等章节可省略或合并为一行摘要；不要为了填满模板而生成无意义内容。目标是让用户有审批欲望，而不是让文档看起来完整。
- 完成后运行 `node .specforge/core/scripts/instructions.mjs`，将输出展示给用户，让用户知道当前 workflow 的下一步是什么。

## 不做

- 不写设计方案。
- 不把未澄清需求包装成已批准规格。
- 不把 `brainstorm.md` 里的 Agent recommendation 当成用户已确认需求。
- 不把 PRD、第三方 skill 模板或用户故事原样复制成 requirements。
- 不把产品指标、路线图或方案备注伪装成已批准系统行为。
- 不用故事点、排期或 Sprint 信息替代验收标准。
