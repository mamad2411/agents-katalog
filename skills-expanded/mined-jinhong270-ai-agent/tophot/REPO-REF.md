# Repo Ref
- source: https://github.com/jinhong270/ai-agent (path: Xiao-Q/skills/tophot/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 用于拉取并展示热点内容（接口为 https://hotspot.api4claw.com/hotspots/platform/{平台名}?timestamp=$TIME_STEMP，返回 JSON 数组）。按 source_name 分组标题。默认会提示用户创建定时任务（不自动执行），在用户确认后提供 cron 注册命令。不使用本地 user_id。适用于用户查询每日热点、微博热点、新闻联播、知乎
