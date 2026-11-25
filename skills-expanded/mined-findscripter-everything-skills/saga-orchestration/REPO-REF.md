# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 02-engineering/saga-orchestration/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当需要跨多个服务协调一个无法用单一 ACID 事务保证一致性的长流程（下单履约、审批流、多步业务工作流）、并要在任一步失败时按反向顺序执行补偿（refund/release/cancel）时使用；做 Saga 编排型/协同型设计、状态机建模与补偿逻辑实现，产出可落地的编排器代码与失败回滚方案；不适用于单库本地事务、强一致同步调用，或无补偿语义的只读流程。触发词：saga、分布式事务、补偿事务、最终
