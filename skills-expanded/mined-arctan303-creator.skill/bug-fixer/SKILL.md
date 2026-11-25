---
name: bug-fixer
description: Diagnose reproducible failures and restore established behavior. Investigate missing facts; unresolved changes to user experience belong to product requirements.
---

# 缺陷修复技能 (bug-fixer)

## Purpose

用可复现证据定位根因并恢复已经明确的预期行为。不要靠猜测修复，也不要把新的产品决策伪装成 Bug。

## Trigger

- 报错、失败测试、审查意见或稳定复现步骤表明既有行为失效。
- 正确行为能由 Product Spec、公开接口、历史行为、测试或用户确认确定。
- 仅改变内部实现且不新增能力、不改变外部契约。

证据矛盾时先按 `AGENTS.md` 核对有效性与替代关系，区分未完成工作、回归、已批准变更和过时测试/文档。仅正确行为仍未决，或修复必须改变公开契约时，转交 `product-spec-builder`。

## Required context

- 预期行为及来源。
- 实际现象、复现步骤、日志或失败测试。
- 范围、非目标、完成证据和 R0/R1/R2。
- 相关代码、历史变更和当前验证入口。

缺少复现条件时，先形成最小诊断假设；无法验证任何假设则停止。

## Workflow

1. 复现问题，区分已证实事实、合理推断和未知项。
2. 提出有证据的有限根因假设，优先验证最能区分原因的检查；独立调查可并行，避免重复写入和无界尝试，收敛到最小充分证据链。
3. 实施最小完整修复，不用大重构掩盖未知根因。
4. 复跑原失败证据，并补充与风险相称的回归检查。
5. 范围改变时更新相关契约，按具体影响重新评级；只有 R2 才自动要求 fresh reviewer，路线升级不自动等于 R2。
6. 修复后同步受影响现状、命令与任务状态，不引用已失效的历史决定。

## Output

- 根因与证据。
- 修改文件和修复说明。
- 原问题验证、回归结果、失败或跳过项。
- 风险级别、残余风险和 reviewer 结论（如适用）。

## Stop or escalate

- 正确行为需要用户或产品决策：升级为产品变更。
- 唯一方案会改变公开 API、数据、权限、业务流程或兼容性：升级为产品变更。
- 只能通过吞错、禁用检查或扩大范围隐藏问题：停止。
- 没有可复现或可替代验证证据：标记阻塞，不声明已修复。

## References

执行前读取 [stage-contract.md](references/stage-contract.md)。

根因未知、复现不稳/偶现、首次修复无效或症状可能不是原因时读[诊断方法](references/diagnosis.md)；验证修复及回归检查的有效性时读[验证方法](../../../.creator/references/verification.md)。
