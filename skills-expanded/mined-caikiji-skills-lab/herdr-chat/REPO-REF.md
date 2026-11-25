# Repo Ref
- source: https://github.com/caikiji/skills-lab (path: skills/deprecated/herdr-chat/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 子 agent 与主控在 Herdr 内双向通信的协议说明。当你在 herdr 管理的 pane 里作为子 agent（claude/codex）工作时必须遵守：向主控发消息用 herdr pane run 反向注入、消息前缀带 [名称] 标识、简短对话走 pane、长文写 .temp/msg/ 文件。主控方向的消息通过 agent prompt 到达，直接回复即可。要求 HERDR_ENV=1，
