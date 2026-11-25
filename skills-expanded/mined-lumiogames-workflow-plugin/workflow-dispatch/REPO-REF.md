# Repo Ref
- source: https://github.com/lumiogames/workflow-plugin (path: plugin/skills/workflow-dispatch/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 主 loop 要把多张 Workflow（workflow.games）单同时派给多个 worker 并合入时使用——从 Room 取 readiness=ready 且文件集互斥的单、各开独立 git worktree 并行派遣、收交回物以 diff 为准、主 loop 合入、合入后触发一次 reviewer、把结论写成 bug 单与评论。用户说派活、扇出、并行开工、几张单一起做时使用；单张单自
