# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-dvcrn-openclaw-skills-marketplace/daily-security-check/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: OpenClaw 每日安全巡检技能。按固定清单检查网关 loopback、防火墙提醒、API 密钥在 .env、SOUL.md 安全规则、认证异常，并执行 openclaw security audit 与 openclaw doctor，输出简短报告与 0–10 安全评分；可由 cron 定时触发，结果可投递到 Telegram 等。Use when user says \"安全巡检\", \"
