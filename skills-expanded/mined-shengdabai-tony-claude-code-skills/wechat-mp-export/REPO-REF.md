# Repo Ref
- source: https://github.com/shengdabai/tony-claude-code-skills (path: skills/wechat-mp-export/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 导出用户自己拥有的微信公众号"盛大白"全部历史文章为 markdown。使用 Playwright 扫码登录 mp.weixin.qq.com 后台，调用官方 appmsg list_ex 接口翻页拉文章，逐篇拉 js_content 转 md。也支持 fetch_stats.py 补抓阅读量/点赞/分享数据写入 frontmatter。仅当用户要求"导出公众号"/"备份公众号文章"/"批量下载我
