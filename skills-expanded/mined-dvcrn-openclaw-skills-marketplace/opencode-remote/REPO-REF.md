# Repo Ref
- source: https://github.com/dvcrn/openclaw-skills-marketplace (path: plugins/entropy-xcy--opencode-remote/skills/opencode-remote/SKILL.md, branch: main)
- mined: 2026-10-15
- desc: 通过 HTTP API 远程操作 OpenCode 服务器。用于管理远程 OpenCode 实例的会话、监控状态和执行任务。\n \n 核心功能：\n 1. 管理多个\"主session\"（每个有独立的四词短名、endpoint、任务）\n 2. 向 session 发送消息（默认不指定agent，延续之前使用）\n 3. 自动监控：发送消息后自动开始每5分钟进度汇报\n 4. 创建 sessi
