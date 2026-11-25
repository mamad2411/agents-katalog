# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 07-productivity/kanban-agent-pipeline-orchestrator/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当想把现有看板（Asana/Linear/GitHub Projects）当成分布式状态机、编排多个 Claude Code worker 跑完「构建→评审→测试→集成」全自动开发流水线时使用；做的事是把 SPEC 拆成带依赖的看板任务、按传递优先级派单、用确定性门禁（tsc/eslint/test）+对抗式评审把关、逐任务记成本、无守护进程崩溃可恢复；不适用于单 worker 小改动、无看板/P
