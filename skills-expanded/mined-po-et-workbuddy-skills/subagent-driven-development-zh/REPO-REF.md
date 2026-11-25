# Repo Ref
- source: https://github.com/po-et/workbuddy-skills (path: ported/skills/subagent-driven-development-zh/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 子代理驱动开发、每个任务派一个全新子代理实现、任务级评审加最终整分支评审、修复循环与五轮熔断、用账本文件抗上下文压缩、按任务复杂度选模型。当用户说「按这份计划派子代理执行」「每个任务开一个新 Agent 做」「实现完自动评审再进下一个」「上下文会被压缩，进度别丢」「这份 plan 你来调度执行」时使用。主循环：建隔离工作区与账本、通读计划并做冲突预扫 → 逐任务抽简报、派实现者、生成评审包、派任务
