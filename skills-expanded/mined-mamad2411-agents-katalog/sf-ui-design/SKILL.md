---
name: sf-ui-design
description: 生成或更新 SpecForge work item 的 UI design；用于 ready artifact 为 ui_design，或需求涉及页面、交互、视觉风格、状态矩阵和 Pencil 原型证据时。
---

# sf-ui-design

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

## 运行模式检测

1. 当前目录向上存在 `.specforge/` 且有 active work item：**Embedded 模式**，按 artifact graph 写入 `01-spec/ui-design.md`，并产出 Pencil 证据。
2. 存在 `.specforge/` 但无 active work item：**Lightweight 模式**，可先做 UI 方向访谈、页面地图和状态矩阵草稿；需要落档时输出 `specforge-import-ready.md` 格式内容，或先路由 `sf-intake` 创建 work item。
3. 不存在 `.specforge/`：**Standalone 模式**，不要运行 `.specforge/...` 命令或调用 `.specforge` 下的 Pencil 脚本；输出可导入的 `specforge-import-ready.md`。Standalone 草稿不等同于正式 Pencil 证据。

`sf-ui-design` 把 requirements 中的用户可见体验转成可审查的 UI 设计证据。它不写技术架构、API、数据库设计或实现任务。

SpecForge 固定使用 **Pencil** 做正式 UI 原型。Figma、HTML、ASCII、截图、竞品和第三方设计 skill 只能作为参考输入；最终必须归一为 `01-spec/ui-design.md`、`01-spec/ui-mockup.pen` 和 `01-spec/ui-mockup-export/*.png`。

## 必读与按需 Reference

必读：

- `references/design-mode-routing.md`：判断 Product UI / Brand Surface / Hybrid，并决定后续 reference 读取顺序。
- `references/ui-design-process.md`：UI 方向访谈、第三方 UX / Pencil reference 编排、Pencil 保存门禁、视觉 review 和完成标准。

按需读取：

- `references/admin-product-ui-contracts.md`：Product UI / 管理端 / shadcn 场景的组件层级和 Admin Component Contract。
- `references/pc-business-system-spec.md`：PC 端业务系统 UI 规范。用户提供或确认该规范、或项目是后台 / 管理系统 / 数据管理工具时读取。
- `.specforge/core/workflows/stages/ui-design/SKILL.md`：内部 UI 设计母本。
- `.specforge/core/artifacts/templates/ui-design.md`：写入骨架。
- `.specforge/core/standards/product.md`、`.specforge/core/standards/design.md`、`.specforge/core/standards/workflow.md`、`.specforge/core/standards/engineering.md`。
- PC 端业务系统场景还要读取 `.specforge/core/standards/pc-ui-design-spec.md`；该文件的具体数值优先于通用 `design.md` 基准。
- `.specforge/core/skills/ORCHESTRATION.md`、`README.md`、`registry.json`：第三方 skill 选择、边界和来源风险。
- 需要操作 Pencil 时读取 `.specforge/core/skills/ui-ux/pencil/SKILL.md`，再按需读取其 `references/*.md`。

## 启动扫描

1. 运行：

```bash
node .specforge/core/scripts/instructions.mjs
```

2. 如果输出是 `Instructions blocked`，按 `Route` 处理阻断。尤其当 blocker 为 `ui-direction-unconfirmed` 时，停止 UI design，向用户输出体验方向确认卡。
3. 确认 ready artifact 包含 `ui_design` 且没有阻断后，再运行：

```bash
node .specforge/core/scripts/create-artifact.mjs ui_design
```

4. 读取 `00-intake/brief.md`、`00-intake/prd.md`（如果存在）、`00-intake/brainstorm.md`（如果存在）、`01-spec/requirements.md`、现有页面 / 组件库 / 设计系统 / 用户提供的参考材料。

## 执行序列

### A. 判断 UI 影响

1. 判断本 work item 是否有页面、组件、角色视图、流程、文案、状态、响应式或可访问性变化。
2. 无 UI 影响时，在 `01-spec/ui-design.md` 写 N/A、理由和验证方式，然后停止。
3. 有 UI 影响时，先检查 UI 方向是否已由用户、现有设计系统或明确低风险默认确认。

### B. 对齐体验方向

1. 先按 `references/design-mode-routing.md` 判断 Design Mode，再按 `references/ui-design-process.md#UI 设计访谈` 列出 `已确认 / 高影响未知 / 可安全默认`。
2. 没有现成设计系统或确认方向时，给 2-3 个互斥体验方向、推荐项和取舍；如果方向会影响信息架构、核心流程或视觉气质，先向用户确认方向。
3. 用户确认后，立即在上游 artifact 或 `ui-design.md` 写入 `[UI DECISION CONFIRMED]` 或 `UI Direction Status: confirmed`，并记录来源。
4. 用户未确认体验方向前，不创建 Pencil 原型，不写完整页面方案。

### C. 写 UI design

1. 写 Design Mode、Visual Style Brief、页面地图、信息架构、用户流程、微文案、状态矩阵、无障碍预审和明确不做项。
2. 若采用 PC 端业务系统规范，按 `references/pc-business-system-spec.md` 填写 `ui-design.md#4` 的设计系统来源、核心 token、页面结构和组件约束。
3. 若实现层采用 shadcn/ui 或场景是管理端，按 `references/admin-product-ui-contracts.md#Admin Component Contract` 写清 Admin Component Contract；shadcn 只作为 primitive / registry 层。
4. 第三方 skill 只作为参考镜头，按 `references/ui-design-process.md#第三方 Skill 和 Reference 编排` 归一化到 SpecForge 结构。
5. 每个参考产品、截图或设计稿都要写“采用什么、不采用什么、如何落地”。

### D. 创建、保存并校验 Pencil

1. 使用 Pencil 创建或更新 `01-spec/ui-mockup.pen`，截图目录固定为 `01-spec/ui-mockup-export/`。
2. 空 `.pen` / 空画布最多读取一次；确认空后立即创建第一屏，禁止空读循环。
3. 每次完成 `pencil_batch_design` 后，必须执行 `references/ui-design-process.md#Pencil 保存与重读门禁`：保存 / 持久化、重新打开或重读目标 `.pen`、确认第一屏非空，再导出截图。
4. 保存后重读失败、`.pen` 仍为空、或连续创建失败 2 次时，停止并记录阻断原因；不得把 HTML / ASCII 当正式替代。

### E. Review 和路由

1. 基于导出截图做视觉质量 review，并至少修一轮 Pencil。
2. 把 review 发现、修改动作、保存后重读证据和最终结论写入 `ui-design.md`。
3. 把 review 结论写入 `ui-design.md`，确认 Pencil 原型已保存且可重读。

## 判定表

| 条件 | 状态 |
|---|---|
| UI 方向尚未确认 | 停止：需先完成体验方向取舍 |
| 关键体验方向、页面范围或角色流程尚未确认，且默认假设风险高 | 停止：提问澄清 |
| 第三方 skill 输出未归一化到 SpecForge artifact | 停止：先归一化 |
| Pencil 原型未保存、保存后重读失败或 `.pen` 仍为空 | 停止：记录阻断，不进入后续阶段 |
| 有 UI 影响但没有 `.pen`、导出截图或明确 Pencil 阻断原因 | 停止 |
| 原型与 requirements 的角色、流程、权限或异常态不一致 | 停止：修正 |

## 完成标准

- `01-spec/ui-design.md` 存在。
- 有 UI 影响时，包含 Visual Style Brief、确认来源、页面地图、流程、状态矩阵、微文案、无障碍自查和明确不做项。
- Product UI / 管理端 / shadcn 场景包含组件封装契约，能指导实现阶段复用项目级组件。
- UI 方向确认可追溯；Agent recommendation 不能伪装成用户选择。
- 有 UI 影响时，存在非空且保存后可重读的 `01-spec/ui-mockup.pen`、`01-spec/ui-mockup-export/*.png`，或明确 Pencil 阻断原因。
- `ui-design.md#9. Pencil 原型证据` 记录 Pencil 保存状态、保存后重读校验和截图证据。
- 有可视原型时，包含视觉质量 review 和至少一轮修正记录。
- 所有 `[NEEDS UI DECISION]` 已清除。
- 完成后运行 `node .specforge/core/scripts/instructions.mjs`，将输出展示给用户，让用户知道当前 workflow 的下一步是什么。

## 不做

- 不写业务代码。
- 不写前后端架构、API、数据迁移或部署设计。
- 不让用户选择 Figma / HTML / ASCII / Pencil 等工具通道；工具固定为 Pencil。
- 不在 implementation 阶段重新发明视觉风格。
- 不在用户尚未确认 UI / 视觉 / 体验方向时创建 Pencil 原型或填充完整 UI design。
