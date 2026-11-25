---
name: wechat-article-search
description: "Search WeChat public account articles by keyword via Sogou WeChat Search. No API key required."
allowed-tools: Bash,Read
license: MIT
---

# 微信公众号文章搜索（WeChat Article Search）

## 适用场景

- 用户说"帮我搜某个关键词的公众号文章/最近文章"
- 需要快速拿到：标题、摘要、发布时间、公众号名称、可访问链接

## 工作流程

### 步骤1: 安装依赖

该脚本依赖 Node.js 包 `cheerio`，在本 skill 目录执行一次：

```bash
cd ~/.hermes/skills/social-media-clients/wechat-article-search
npm install
```

### 步骤2: 确认关键词与数量

### 步骤3: 执行搜索

```bash
node scripts/search_wechat.js "关键词"
```

## 可选参数

```bash
# 限制返回数量
node scripts/search_wechat.js "关键词" -n 15

# 保存到文件
node scripts/search_wechat.js "关键词" -n 20 -o result.json

# 解析真实微信文章直链
node scripts/search_wechat.js "关键词" -n 5 -r
```

## 参数说明

- `query`：搜索关键词（必填）
- `-n, --num`：返回数量（默认 10，最大 50）
- `-o, --output`：输出 JSON 文件路径（可选）
- `-r, --resolve-url`：尝试把中间链接解析成微信文章真实链接（会额外请求每条结果）

## 输出字段

文章标题、文章地址、文章概要、发布时间、来源公众号名称

## 常见问题

- 结果为空：尝试更换关键词、减少特殊字符，或稍后重试
- 解析真实 URL 失败：这是常态（反爬限制）；可提示用户用浏览器打开中间链接

## 注意事项

- 本工具仅用于学习和研究目的，请勿用于商业用途或大规模爬取。
- 使用本工具时请遵守相关网站的使用条款和规定。
- 过度使用可能导致 IP 被封禁，请谨慎使用。
