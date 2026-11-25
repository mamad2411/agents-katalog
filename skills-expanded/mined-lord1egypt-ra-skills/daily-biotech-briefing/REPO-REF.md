# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/d/daily-biotech-briefing/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 生成每日生物医药早报，包含 GitHub Trending 日榜和5个生物医学方向（干细胞治疗、外泌体治疗、质谱诊断、拉曼诊断、卵巢癌检测）的最新微信文章摘要。每天早上10点通过 cron 触发，发送到用户 QQ 邮箱。使用 web_fetch 抓取 github.com/trending 和 wechat-article-search 技能搜索微信文章，curl 阅读正文。
