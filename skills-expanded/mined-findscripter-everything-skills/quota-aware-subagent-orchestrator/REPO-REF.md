# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 04-ai/quota-aware-subagent-orchestrator/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当一个任务横跨 3 个以上文件/组件、想多智能体并行推进、且曾在任务中途撞上配额耗尽时使用；做任务分解为隔离子智能体使命、按规模与复杂度路由模型（默认便宜快模型，贵模型限 1 个）、上下文隔离派发、依赖分轮并行执行并做轮间抽检与集成校验，产出一份 Mission Brief 编排蓝图与可交付集成结果；不适用于单文件改动、修单个 Bug、写 50 行内小脚本或只生成计划/回答问题。触发词：配额感知编
