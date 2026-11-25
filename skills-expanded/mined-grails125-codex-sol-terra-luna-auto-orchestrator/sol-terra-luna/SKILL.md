---
name: sol-terra-luna
description: 使用 Sol 主控、Terra 工程执行、Luna 探索与测试、Sol High 风险升级的分层开发工作流。
---
<!-- STL-SKILL-BEGIN -->
# Sol–Terra–Luna 工作流

当用户显式输入 `$sol-terra-luna`，或任务明显需要分层开发时，执行以下单一工作流：

1. **Sol 接管主线程**：确认目标、非目标、现有约束、风险、验收和回滚；没有任务契约时先创建契约。
2. **选择探索者**：简单只读定位交给 `luna_explorer`；根因不明且需要实验时交给 `terra_debugger`。
3. **拆成最小单元**：每个单元必须有允许范围、禁止范围、完成标准、验证命令和回滚方式。
4. **选择实现者**：R0 机械补丁使用 `luna_implementer`；R1/R2 常规工程使用 `terra_implementer` 或 `terra_debugger`。
5. **独立验证**：`luna_tester` 运行明确命令并返回退出码和关键日志；实现者不得用修改测试掩盖失败。
6. **独立审查**：`terra_reviewer` 只读审查 diff、正确性、兼容性、安全和测试缺口，不得审查自己的实现。
7. **条件升级**：只有满足 AGENTS.md 的升级门槛时才调用 `sol_escalation`；其输出仅用于决策，不直接改代码。
8. **Sol 最终验收**：对照任务契约决定接受、返工、补测、阻塞或回滚，并输出证据化结论。

不要在本 Skill 中重复项目全部规则；具体权限、并发、风险与验收门槛以最近的 `AGENTS.md` 和活动 `task.json` 为准。
<!-- STL-SKILL-END -->
