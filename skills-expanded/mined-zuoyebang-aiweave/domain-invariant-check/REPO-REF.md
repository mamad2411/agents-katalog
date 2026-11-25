# Repo Ref
- source: https://github.com/zuoyebang/aiweave (path: templates/skills/domain-invariant-check/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 审计代码是否真正保护了领域不变量。扫描 service 方法，对照 docs/service/{module}_service.md §7 业务规则 / 隐式约束 / 业务状态机，校验伪码 [INVARIANT-CHECK: I-N] 标记与代码实现的一致性。命中标 🔴 严重（结构性问题）或 🟡 待复核。
