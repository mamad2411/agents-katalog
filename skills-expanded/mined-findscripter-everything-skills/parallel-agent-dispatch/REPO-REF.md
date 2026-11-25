# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 00-meta/parallel-agent-dispatch/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当面对 2 个以上彼此独立、无共享状态也无先后依赖的任务（如多个互不相关的测试失败、多个子系统各自损坏）时使用；为每个独立问题域派发一个子 Agent 并发处理，再回收摘要、查冲突、跑全量验证整合产物；不适用于失败相关联、需通览全局状态、还在探索性排障或会争抢同一文件/资源的场景。触发词：并行、子 Agent、独立任务
