---
name: wechat-fetch
description: 搜索并阅读微信公众号文章。脚本固定位置: workspace/skills/wechat-fetch/scripts/wechat_tool.py。遇到微信链接必须首选此工具。
homepage: https://github.com/Lingyuzhou111/dow-ipad-859
metadata:
  emoji: 💬
  requires:
    python: ["miku_ai", "camoufox", "markdownify", "beautifulsoup4", "httpx"]
  always: true
---

# 微信助手 (WeChat Fetch)

针对微信公众号文章的专用抓取和搜索工具。脚本内部集成“搜狗+必应”双模搜索和全文抓取自动降级机制。

## ⚠️ 核心准则 (Agent 提效必读)

1. **绝对路径**：本技能脚本位于 `workspace/skills/wechat-fetch/scripts/wechat_tool.py`。**严禁猜测 `/scripts/` 等其他位置**。
2. **搜索决策**：
   - 脚本已内置搜狗(Sogou)转必应(Bing)的自动降级搜索机制。
   - 如果搜索返回 "No results found"，说明全网无对应内容。**请立即停止重试**，向用户报告搜不到，不要反复更换关键词尝试。
3. **强制阅读器**：看到微信链接（mp.weixin.qq.com）**禁止使用 curl 或 web-fetch**，必须调用本工具的 `read` 命令。
4. **忽略报错**：脚本内置了自动降级逻辑。即便浏览器引擎加载失败，也会自动通过 requests 模式返回全文，请直接使用返回的文字进行总结。

## 快速调用命令

### 1. 阅读文章 (首选)
```bash
python3 "workspace/skills/wechat-fetch/scripts/wechat_tool.py" read "URL"
```

### 2. 搜索文章
```bash
python3 "workspace/skills/wechat-fetch/scripts/wechat_tool.py" search "关键词" 5
```

## 应用场景示例
- "帮我总结这篇文章: https://mp.weixin.qq.com/s/xxx" -> 直接调用 `read`。
- "搜一下最近关于 Seedance 2.0 的微信文章" -> 直接调用 `search`。
