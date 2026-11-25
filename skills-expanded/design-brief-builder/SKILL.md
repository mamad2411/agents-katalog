---
name: design-brief-builder
description: Turn visual goals, brand context and scenarios into a reasoned Design Brief. Use when visual or interaction rules change, not to restore established behavior.
---

# 设计规范技能 (design-brief-builder)

## Purpose

把“高级、简洁、现代”等主观表达转成可实施、可验证且有场景理由的视觉与交互规则。

## Trigger

- 0→1 产品需要建立视觉或交互规则。
- 产品变更需要新增或改变既有视觉、品牌或交互规则。
- 现有 Product Spec 已足以说明产品目标、用户和核心场景。

恢复既有视觉行为属于维护路线，不重新定义风格。

## Required context

- 相关可验收需求，来自现有 Spec、等价文件或用户明确确认。
- 用户、场景、平台和使用环境。
- 用户给出的风格词、品牌线索、截图、参考产品或反例。
- 已有 Design Brief 或设计系统（如果存在）。

## Workflow

1. 先解释主观词在当前产品语境中的具体含义。
2. 优先遵循已有项目准则并自主选择有依据的细节；只有未决方向实质改变体验且不能由已有决定收敛时，给出含理由与代价的候选并询问必要选择。存在多种专业实现本身不要求追问。
3. 将选定方向写成“设计意图 → 决策 → 参数 → 理由/代价 → 验证检查点”。
4. 只更新本次受影响的视觉、交互与可访问性，不为局部改动重做完整设计。
5. 原位更新已有设计规范，标记旧决定替代关系，联动相关需求和活跃任务；不创建重复副本。

## Output

- 已确认设计事实、临时假设和待确认项。
- 被选择及被放弃的方向与原因。
- 可执行的设计变量、关键状态和验收检查点。
- `docs/Design-Brief.md` 或项目约定的等价文件。

## Stop or escalate

- 产品目标或相关行为仍不可验收时补齐需求；已有明确选择时不因缺少同名 Spec 文件阻塞。
- 设计选择会改变产品范围或业务流程：升级为产品变更。
- 参考图未说明偏好时，先结合项目准则形成合理方案；只有无法收敛的体验取舍才追问一个必要问题。
- 多个风格要求互相冲突且无法建立临时假设：停止并请求选择。

## References

执行前读取 [stage-contract.md](references/stage-contract.md)。
