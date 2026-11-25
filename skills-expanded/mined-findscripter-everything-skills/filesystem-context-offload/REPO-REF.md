# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 00-meta/filesystem-context-offload/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当工具输出撑爆上下文窗口、需要跨长任务持久化状态、子 Agent 间共享信息、或任务所需上下文超出单窗口时使用；做把大块内容写入文件、上下文窗口只留摘要/路径指针，再用 ls/glob/grep/按行读取按需召回（卸载工具输出、持久化计划、子 Agent 文件工作区、动态加载技能、持久化终端日志、自我修改指令）；不适用于单轮即结束、上下文本就装得下、或对延迟极敏感（文件 I/O 有开销）的场景。触
