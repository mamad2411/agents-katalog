# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/workbuddy-checkin-skill/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 当用户想要在 WorkBuddy 上完成每日签到（获取签到积分）时使用此技能。若 WorkBuddy 未运行则自动启动，使用 Playwright 通过 CSS Selector 定位 DOM 元素并点击：先点击左下角用户菜单（class="user-menu"），等待 2 秒后，再点击「立即领取 →」按钮（class="daily-checkin-banner-action"）完成签到。触发关键
