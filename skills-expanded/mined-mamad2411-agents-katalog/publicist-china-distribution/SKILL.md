---
name: publicist-china-distribution
description: China multi-platform article distribution via Wechatsync (Chrome extension + CLI + MCP), platform selection decision tree, and format adaptation. Use when syncing drafted content to 29+ Chinese platforms.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# China multi-platform distribution, Wechatsync integration

**Scope**. Distribution layer only. Pair with `publicist-china` + platform-specific skills (wechat, xiaohongshu, zhihu, douyin, bilibili).

## Tool: Wechatsync (文章同步助手)
- **Repo**. `wechatsync/Wechatsync` (6.3k★, GPL-3.0, updated May 2026)
- **Modes**. Chrome/Edge Extension (primary) + CLI (`@wechatsync/cli`) + MCP Server + JS SDK
- **Platforms (29+)**. 微信公众号、知乎、头条、掘金、CSDN、小红书、百家号、网易号、搜狐号、B站、微博、豆瓣、简书、雪球、东方财富、WordPress、Typecho, X/Twitter, Hexo/Hugo
- **Architecture**. Browser extension uses your logged-in cookies; defuddle extraction; auto format conversion; image upload to each platform CDN
- **Output**. Drafts only (safety design), manual publish per platform

## Platform selection decision tree

```
Goal → Channel Mix
├─ 权威背书 (融资/重大官宣/获奖) → 央媒(人民/新华/央视) + 美通社/发稿平台
├─ 直接获客转化 (大促/APP下载) → 小红书(蒲公英) + 抖音(星图) + 垂类自媒体
├─ 长期SEO/长尾流量 → 百家号(百度权重) + 搜狐号/网易号/头条号 + 知乎(高权重)
├─ 品牌声量/种草 → 微信公众号(互选-原创定制) + 小红书(种草合集) + B站(花火深度)
├─ 技术/专业人群 → 知乎(专家回答) + 掘金/CSDN/思否 + 微信技术号
├─ 预算极低测试 → 自媒体矩阵(百家/搜狐/网易/头条/知乎/掘金)零成本
└─ 全域覆盖(预算充足) → 二八策略: 2成顶尖媒体背书 + 8成发稿平台批量投放
```

## Wechatsync integration steps

### 1. Setup (once)
```bash
# Chrome Extension: Chrome Web Store → "文章同步助手" / Wechatsync
# CLI: npm i -g @wechatsync/cli
# MCP: Add to Claude Desktop config
```

### 2. Login all target platforms in Chrome
- Each platform: login once → cookies persist
- No password enters Wechatsync (local browser only)

### 3. Prepare content
- Write in any editor (微信后台/掘金/Notion/Markdown file)
- Wechatsync extracts: title, body, cover, images (auto-download + re-upload)

### 4. Sync
- Click extension → select platforms → "同步"
- 3 concurrent pushes; auto format conversion per platform
- Check each platform draft → manual publish

### 5. CLI/MCP automation (optional)
```bash
wechatsync sync article.md -p zhihu,juejin,csdn,wechat
# or via MCP: "帮我把这篇文章同步到知乎、掘金、公众号"
```

## Format adaptation notes (per platform)
| Platform | Input Format | Special Handling |
|---|---|---|
| 微信公众号 | HTML (editor) | 封面图必选; 图片自动上传微信CDN |
| 知乎 | HTML (Draft.js) | 代码块保持; 无外链(仅bio) |
| 小红书 | ProseMirror JSON | 标题≤20字; 封面3:4; #话题标签 |
| 头条/百家/搜狐/网易 | HTML | 原创标识; 图片自动上传 |
| 掘金/CSDN/简书 | Markdown | 代码块/LaTeX优先; 目录生成 |
| B站 | HTML | 封面16:9; 分区标签; 视频配套 |
| 微博 | HTML | 140字限制(长文展开); @品牌方 |

## Limitations (honest)
- **Draft-only**, not true "one-click publish"
- **Chrome required**, no headless server mode without browser
- **小红书/抖音/头条 adapters** in private submodule (`wechatsync-private-adapters`)
- **Cookie expiry**, re-login needed periodically; no refresh token
- **Format fidelity**, complex tables/LaTeX may differ across platforms

## References
- `https://github.com/wechatsync/Wechatsync`
- `https://www.wechatsync.com`
- `skills/publicist-china-wechat/SKILL.md`
- `skills/publicist-china-xiaohongshu/SKILL.md`
- `skills/publicist-china-zhihu/SKILL.md`
- `skills/publicist-china-douyin/SKILL.md`
- `skills/publicist-china-bilibili/SKILL.md`

## What this skill does not do
- ❌ No content creation (upstream skills)
- ❌ No platform compliance (platform skills)
- ❌ No guaranteed placement
- ❌ No MCP/CLI tools beyond Wechatsync's own
