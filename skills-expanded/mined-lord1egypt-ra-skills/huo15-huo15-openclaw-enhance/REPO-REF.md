# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/h/huo15-huo15-openclaw-enhance/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 火一五·克劳德·龙虾增强插件 v6.7.13 — large-file-bridge 兜底死循环修 + 用户上传后流程引导：实测用户『我已经上传好了』后 AI 没调 enhance_upload_check 反被兜底又塞了一份上传链接死循环。根因：before_agent_reply 每轮都触发,injectedSessions 有 entry + body 不含 URL → 强制 appendT
