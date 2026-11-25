# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/c/cron-callback-session/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 实现『用 A 会话调起/注入 B 会话』的能力（sessions_send）：cron 任务、外部进程或另一会话可向目标会话注入消息，唤醒其 agent 带完整上下文继续推进。适用于 OpenClaw 与 QClaw（同内核）。含 Windows 下 visibility 配置检查/修复、正确重启网关（SIGUSR1 bug 规避）、cron job 设计。当用户要求「定时任务完成后回到本对话继续
