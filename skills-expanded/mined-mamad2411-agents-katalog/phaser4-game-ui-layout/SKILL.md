---
name: phaser4-game-ui-layout
description: 为 Phaser 4 游戏建立可验证的 UI 布局合同、坐标空间、响应式重排与证据门禁；当实现或审查游戏 UI、HUD、弹层、滚动区域、安全区、断点、动态文案或视口适配时使用。
---

# Phaser 4 游戏 UI 布局

## 全局控制接入

控制面边界：可提议、可审查、可在已建立且任务授权有效的 Work Item 范围内修改，且必须回到 `$phaser4-game-workflow-control` 审计和状态迁移；仅实际 A4-A6 操作请求批准。

本领域可提议、审查，并仅在已建立且任务授权有效的 Work Item、Implementation Package、A 等级与路径内修改布局；所有动作与证据回到 [`phaser4-game-workflow-control`](../phaser4-game-workflow-control/SKILL.md) 审计和状态迁移。布局合同和 V 阶段不能旁路授权、A4-A6 操作批准或全局状态。

将 UI 布局从页面坐标修补转换为可追踪的布局合同，并把合同、实现、运行时证据接入全局控制面。仅负责布局关系、坐标空间、尺寸策略、响应式重排和布局证据；不拥有全局状态、审批、玩法规则、资源生产、视觉方向或发布放行。

## 核心流程

1. 读取项目的 GDD/TDD、当前候选、总控审核漏斗和适用视觉阶段；确定稳定 UI ID、坐标空间、参照物、状态与平台输入。
2. 复制 [合同模板](assets/ui-layout-contract-template.yaml)，按 [布局合同](references/layout-contract.md) 补齐目标视口、区域、锚点、尺寸、断点、安全区、滚动、动态内容、覆盖回退和证据矩阵。
3. 用 [Phaser 适配器](references/phaser-adapter.md) 设计唯一布局入口：把视口、安全区、方向、内容尺寸和状态作为输入，分离资源 origin、布局停靠点和动画偏移，保证重排幂等。
4. 运行 `node scripts/validate_ui_layout_contract.mjs <contract>` 和对应 `node:test` 测试。格式或关系错误在候选形成前修复；绝对定位、固定尺寸、固定/悬浮元素在合同依据完整时只标记 `specialized_review`。
5. 按 [证据矩阵](references/evidence-matrix.md) 生成同一候选的边界、方向、字号、语言、安全区、动态状态和窄高度证据。
6. 按 [工作流门禁](references/workflow-gates.md) 接入 V0–V5、F0–F4 和 G0–G3；布局结构或参照关系变化退回 V1，F3 只接受绑定当前候选的工程证据。

## 资源导航

- 需要字段、关系表达或不变量写法时，读取 [references/layout-contract.md](references/layout-contract.md)。
- 需要 Phaser Scale、Camera、Container、DOM Overlay、resize 或重排边界时，读取 [references/phaser-adapter.md](references/phaser-adapter.md)。
- 需要 V/F/G 门禁、退回和候选绑定规则时，读取 [references/workflow-gates.md](references/workflow-gates.md)。
- 需要组合测试、等价类削减或冻结 Golden 条件时，读取 [references/evidence-matrix.md](references/evidence-matrix.md)。
- 合同验证器只接受 JSON-compatible YAML（合法 YAML 1.2 的 JSON 子集），详见合同参考；直接使用 Node.js `JSON.parse`。

## 所有权与输出

布局技能输出合同版本、布局计算输入/输出、不变量和证据索引。玩法继续独占规则、状态和交互；架构维护坐标空间与模块边界；美术维护纯表现资源和预制数据；QA 只读验证可达、截断、遮挡、触控、滚动和证据。布局计算与 Phaser GameObject 测试验证关系不变量，不把孤立绝对坐标当作通用验收标准。
