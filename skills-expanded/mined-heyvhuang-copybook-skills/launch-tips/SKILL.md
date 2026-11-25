---
name: launch-tips
description: "上线推广 · 12 条：上线前检查清单、搜索引流小工具、VPS 加固。"
disable-model-invocation: true
---

# 上线推广 · 12 条

Copybook 的 12 条「上线推广」技巧，收藏多的在前。每条要用的文字、放到哪里、最后得到什么，都在 references/ 里它自己的文件中。

- 用户点名技巧时，用点名的那条。用户只说了要做什么时，从适用于实际执行者的技巧里，选最符合用户目标和限制的一条。几条同样合适时，选一条即可。选中后，用一句话说明选了哪条、为什么，再读它的文件照着做。另一条也合适，而且换用它会明显改变做法或结果时，顺带点出它的名字和区别。
- 用户什么都没说：把下面的列表（每条的名字和做什么）给用户看，问用哪条。
- 都不合适就直说，并建议用 copybook，它会在全部 146 条里找。

| 技巧 | 做什么 |
| --- | --- |
| [上线前网站检查：20 项页面](references/pre-launch-site-check-20-items.md) `pre-launch-site-check-20-items` | vibe coding 做的网站要上线：设计、手机、各种状态、真实流程和上线细节，查完一次修好。 |
| [上线前检查：20 项网站速度](references/pre-launch-check-site-speed.md) `pre-launch-check-site-speed` | vibe coding 做的网站打开慢：图片字体、前端、数据库接口和服务器各查一遍，一次修好，重新测速。 |
| [上线前检查：4 个测试 subagent](references/pre-launch-4-test-subagents.md) `pre-launch-4-test-subagents` | 自己先往坏里试：4 个只测不改的 subagent 用 16 个问题查安全、数据、操作、环境，按轻重修。 |
| [拉 Google 搜索用户的免费小工具](references/free-tool-page-for-google-search.md) `free-tool-page-for-google-search` | 想从 Google 搜索拉用户：3 个有人搜的免费小工具，你挑的做成独立 SEO 页，结果下面只放你的按钮。 |
| [上线前检查：25 项页面背后](references/pre-launch-25-behind-page-items.md) `pre-launch-25-behind-page-items` | 页面背后也会出事：密钥、账单、收钱、监控和上线当天查完一次修好，要你做的列在最后。 |
| [VPS 加固：只走 Cloudflare，SSH 走 Tailscale](references/vps-lockdown.md) `vps-lockdown` | 用了 Docker，ufw 拦不住：访客只能经 Cloudflare 进来，SSH 只有你能经 Tailscale 登录。 |
| [上线前检查：6 个法律坑](references/pre-launch-check-6-legal-traps.md) `pre-launch-check-6-legal-traps` | 按产品实际业务和适用法规，核查数据收集、字体、会话录屏、营销邮件、续费和用户上传。 |
| [Google 搜索检查：已上线网站 12 项](references/google-search-check-12-items.md) `google-search-check-12-items` | 拿名字在 Google 上搜不到你用 AI 做的网站：抓取、每个页面和全站，一次修好。 |
| [low effort 写、high effort 验的两个 subagent](references/builder-and-verifier-subagents.md) `builder-and-verifier-subagents` | high 多花的 token 主要买到验证：builder 用 low、verifier 用 high，一条规则让新功能都走一遍。 |
| [Overnight market research for startup ideas](references/overnight-startup-idea-research.md) `overnight-startup-idea-research` | Looking for a startup idea people would pay for: a night of quoted, linked complaints, then 3 scored ideas nobody covers yet. |
| [动手前的市场判断](references/market-read-before-you-build.md) `market-read-before-you-build` | 还没调研就给建议：25-40 家竞争对手逐家记下，反复出现的抱怨排好序，再看你的方向会死在哪。 |
| [扩容检查：缓存、队列、负载均衡](references/scaling-check.md) `scaling-check` | 应用现在真需要扩容吗：6 种方案对照你的代码逐一判断，每条附文件证据和每月大概多花多少钱。 |
