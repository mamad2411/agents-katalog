# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/s/safe-smart-web-fetch/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 安全网页抓取技能。获取网页内容时，默认先判断 URL 是否可能包含 token、是否为内网/本地域名、是否为私密链接；这三类一律不走第三方清洗服务，只走直接抓取。其余公开网页可按顺序尝试 Jina Reader、markdown.new、defuddle.md 获取干净 Markdown，失败再回退原始抓取。
