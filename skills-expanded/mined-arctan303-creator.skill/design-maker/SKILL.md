---
name: design-maker
description: Create prototypes, wireframes and interaction states when a visual artifact will reduce uncertainty. Optional for new or changed designs; not required for routine maintenance.
---

# 设计制图技能 (design-maker)

## Purpose

用最小必要的视觉产物消除页面结构、关键状态和交互上的开发不确定性。

## Trigger

- UI、布局、交互或品牌表达会显著影响开发计划。
- 用户需要在开发前检查关键页面或状态。
- 当前有效需求与设计规则已明确本次范围，但文字仍不足以指导实现。

没有明显界面、常规 UI 可直接计划或设计只会增加装饰时跳过。

## Required context

- 当前相关需求与设计规则（复用 Spec/Design Brief、等价文档或明确确认）。
- 页面/流程范围、目标平台和响应式约束。
- 用户提供的截图、品牌资产、参考图或原型资料。
- 按[读取流程](../../../.creator/references/project-design.md)实际读过的项目已采用设计入口、适用逐层引用与例外，以及现有组件、tokens 和素材；不加载未采纳的场景库作为运行时规则。

## Workflow

1. 映射需要视觉决策的关键流程和验收标准。
2. 选择线框图、高保真稿或实现注释中的最小充分产物。
3. 覆盖默认、空、加载、错误、成功和关键交互状态。
4. 标注全局变量、组件复用、响应式规则和与文档的映射。
5. 检查产物没有擅自扩大产品范围。

## Output

- 页面或流程清单。
- 关键布局、状态、交互与响应式规则。
- 设计稿、线框图或实现注释。
- 留给开发阶段处理的明确细节。

## Stop or escalate

- 必要需求、页面、流程或设计选择仍未决：在本次范围补齐必要项；仅暂停依赖部分，独立部分继续，不因缺少同名文档返回。
- 设计要求新增产品范围：升级为产品变更。
- 缺少品牌、内容或布局依据却要求高保真定稿：停止并说明缺口。

## References

执行前读取 [stage-contract.md](references/stage-contract.md)。
