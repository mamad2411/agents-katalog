---
name: grill-me-for-ui
description: 通过一次一问的设计访谈与确定性路由，把模糊 UI 需求、页面重设计、参考图或现有界面反馈收敛为 Art Direction、UI Brief、增量计划或视觉评审。用于“grill me for UI”“先访谈再设计”、新方向、视觉世界替换、增量扩展、现有 UI 精修、审美研究或实施后验证仍有重要设计取舍的场景。不要用于需求完整的单点样式修改、纯代码 Bug，或执行已经确认的实现计划。
---

# Grill Me for UI

判断当前只需要哪一种设计能力，并走最短路径。

## 硬规则

1. 一次只问一个会改变方案的高影响问题；先查证据，只问必须由用户决定的取舍。
2. 每题说明影响并给出推荐；先目标和内容，后方向、构图与细节。
3. 用户未确认设计基线前，不大规模实施或改写设计文件。
4. 使用真实内容和资产；不编造指标、客户、评价、奖项或品牌声明。
5. 一个主导概念，最多两个支持母题。
6. 用户可采用推荐、跳过、回退、结束访谈或缩小范围。
7. 验证只有 Pass 1、一个 Fix batch 和 Pass 2；没有视觉证据时不声称通过。

## Fast Exit

需求完整、低风险且没有设计取舍的单点 Token、尺寸或样式修改，不输出 Router Trace，不加载参考，也不访谈。纯代码 Bug 或已确认实现计划同样退出本 Skill。直接按现有系统实施并做一次定向 Review。

## Router Trace

在第一题或动作前，用 3–6 行记录：

```text
Surface：[Persuade / Operate / Read / Experience]
Baseline：[无可复用基线 / 现有实现 / 现有设计契约]
Scenario：[Greenfield / World Replacement / Extension / Refinement]
Scope：[受影响表面；适用时 T1 / T2 / T3]
Depth / Action：[适用时重写深度；一个主动作 + 最多一个支持动作]
Reference / Stop：[本轮唯一 Playbook；停止条件]
```

先检查当前表面、真实内容、实现、Token、组件和已确认决定。缺少 DESIGN.md 不等于 Greenfield。无法用一句证据说明分类时，本阶段只读取 `references/design-intelligence-router.md`，先解决 Trace，再进入下游阶段。

“阶段”是内部工作状态，不强制等于一次对话轮次：证据足以分类时可以在同一轮进入下一阶段；需要用户决定时只问一个分类问题并结束本轮。Trace 未解决前禁止预载下游 Playbook。

**硬停止：** Trace 任一字段为“待确认”或 `USER_DECISION_REQUIRED` 时，不得读取任何其他 reference；立即输出 Trace、只问一个分类问题并结束本轮。

## Token Discipline

- 默认只加载本文件和一份首要 Playbook；项目证据不算 Playbook。
- Extension T1/T2 与多数 Refinement 优先 `references/core-cheatsheet.md`。
- 禁止同一阶段加载两个内容重叠的 Playbook；输出模板只在交付时按条件追加。
- `*-deep.md` 是升级附录，只能在轻量检查命中其触发条件后追加，禁止预载。
- 分类是独立阶段；读取 Router 后不得在同一阶段预载 Interview、Research 或 Critique。
- 上下文已经很长时，缩小非关键证据、问题预算和输出，不以多加载文件补偿不确定性；不得跳过真实性、权限、失败恢复、安全或已确认约束。
- `examples/` 只供人类阅读与离线评估，运行时禁止加载。

## 最小路由

| 当前需要 | 首要 Playbook | 最小结果 |
|---|---|---|
| 分类或边界仍有歧义 | `references/design-intelligence-router.md` | 可解释的 Trace |
| Greenfield / World Replacement | `references/interview-map.md` | 双轮方向选择与核心 Brief |
| Extension T1/T2；方向正确但动作或边界未定位的 Refinement | `references/core-cheatsheet.md` | 局部决定或修改边界 |
| 风格词或文化语义含糊，外部参考会改变方向 | `references/aesthetic-research-protocol.md` | 2–3 个方向胶囊 |
| 完整 Art Direction 或构图系统 | `references/taste-calibration.md` | 可验收的视觉命题 |
| 已明确 polish / 定向动作；机械 audit、结构性诊断或生产加固 | `references/iteration-and-refinement.md` | 深度、动作和修复批次 |
| 实施后视觉证据确认 | `references/visual-critique.md` | 两轮内的验证结论 |
| 从实现提炼长期契约 | `references/design-md-template.md` | 可选 DESIGN.md |

动作只选一个主项：shape、research、critique、audit、polish、bolder、quieter、distill、typeset、layout、colorize、animate、delight、harden、adapt、verify 或 document。

## 路径护栏

- Greenfield / World Replacement 才默认双轮；先完成前轮边界，只有研究会改变方向时才插入 research，不因一个风格形容词提前安排。
- 方向选定后，需要完整 Art Direction 才在下一阶段切换 `taste-calibration.md`；否则直接形成范围相称的交付。
- World Replacement 必须有放弃旧视觉身份的明确授权，并锁定保留行为、迁移和回退边界。
- Extension 沿用相关旧契约；T1/T2 最多问 1–3 个当前表面问题，T3 目标明确时 Fast Exit。
- Refinement 先确认视觉身份仍正确，再选重写深度和主动作；身份错误时停止并请求 World Replacement 授权。
- Verify 只做视觉与机械 UI 验证；权限、数据和恢复行为需要独立功能证据。

## 停止与交付

Surface、Scenario、范围、主动作和成功结果明确，剩余未知不会改变下一阶段时停止。高风险 Operate 还需锁定权限、失败和恢复。不要因为“还能继续问”延长流程。

行动前先给不超过 12 行的共享理解。若仍有一个阻塞性用户决定，只问这一题并结束本轮；没有阻塞决定时直接交付。最多把 3 个非阻塞未知写成假设，不把它们变成问题或确认门。

局部决定和修改计划直接内联交付；只有需要持久交接时才加载输出模板：

- 方向与项目决定需要交接：`references/ui-brief-template.md`；
- 已生成核心 Brief，且存在复杂流程、状态、响应式、技术或正式验证：追加 `references/ui-brief-implementation-module.md`；
- 多页面、设计系统、World Replacement、持续扩展或跨 Agent：追加 `references/design-md-template.md`；
- 已生成 DESIGN.md，且已有或已明确决定建立可执行 Token：追加 `references/design-token-template.md`。

只有用户继续要求时进入视觉稿、Figma、实现或代码。用户中途结束时输出部分 Brief，并标明未确认分支。

## 深度参考，仅在触发时读取

- `references/taste-deep.md`：复杂品牌世界、完整视觉系统或需要解释高级审美判断；
- `references/visual-critique-deep.md`：用户明确要求深度 Critique，或短评审发现 P0/P1 且根因仍不清楚；
- `references/ui-vocabulary.md`：用户描述与 UI 术语存在歧义。
