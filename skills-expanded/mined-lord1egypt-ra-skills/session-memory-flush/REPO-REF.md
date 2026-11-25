# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/s/session-memory-flush/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 在 OpenClaw session 即将因 idle/reset 释放前，扫描 `openclaw sessions --json` 可见会话，读取 transcript，提炼高价值上下文并写入 workspace memory 文件，降低新 session 的失忆感。用于 main、native subagent、cron、dreaming 等会话的 idle 前摘要回收；当需要安装、验证、调
