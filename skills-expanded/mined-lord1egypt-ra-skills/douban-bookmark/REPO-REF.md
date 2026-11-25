# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/d/douban-bookmark/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 输入图书名称，把它加入豆瓣读书的「想读」收藏。适用于“把《xxx》加入豆瓣想读 / 愿望清单 / 想读列表”这类请求。实现方式：先用 HTTP 解析豆瓣搜索结果拿到最优图书详情页，再用 Playwright 持久化浏览器登录态打开详情页，执行豆瓣真实的两段式收藏流程（点“想读”→ 点“保存”）。首次登录后可长期复用浏览器 profile。
