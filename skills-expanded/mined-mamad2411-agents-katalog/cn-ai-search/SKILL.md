---
name: cn-ai-search
description: 中文AI Agent专用多平台聚合搜索工具，开箱即用，国内网络友好，自动总结结果
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["python3","node"],"env":["TAVILY_API_KEY"]}}}
---

# 🔍 cn-ai-search - 中文AI聚合搜索Skill

专为中文AI Agent/智能体优化的多平台聚合搜索工具，一次查询覆盖全网主流中文平台，自动去重过滤广告，输出干净结构化结果，支持AI自动总结。

## 🧠 设计理念：AI-First 搜索范式

传统搜索是给人用的——充满广告、SEO垃圾、重复内容。cn-ai-search 是专门为 AI Agent 设计的搜索：

- **无广告污染**：专为大模型设计的干净输出，没有任何广告干扰
- **结构化数据**：直接输出结构化结果，Agent 不用自己解析
- **多源融合**：一次查询覆盖多个平台，AI 获得的是全网视角
- **AI 总结层**：内置 AI 自动总结，把搜索结果变成可操作的洞察

## ✨ 核心特点

| 特点 | 说明 |
|------|------|
| 📦 **开箱即用** | 基础功能无需API密钥，安装就能用 |
| 🇨🇳 **中文全覆盖** | 百度、微信公众号、知乎、B站、微博、小红书全覆盖 |
| 🧹 **自动净化** | 过滤广告、SEO垃圾、重复内容，结果干净直接喂大模型 |
| 🤖 **AI自动总结** | 基于Tavily AI，自动汇总所有结果为结构化答案 |
| 🌏 **国内友好** | 对国内网络优化，海外服务器也能正常访问 |
| 🔧 **灵活扩展** | 支持自定义平台，每个平台独立维护，扩展方便 |

## 🚀 支持平台

✅ 基础可用（无需配置）：
- 百度搜索
- 微信公众号搜索（搜狗）
- 知乎搜索
- B站搜索
- 微博搜索

🔧 配置后可用：
- 小红书（需要Docker + mcporter）
- 抖音（需要mcporter）

## 📖 快速使用

```bash
# 同时搜索所有默认平台
cn-ai-search "AI Agent 商业化"

# 指定平台搜索（多个用逗号分隔）
cn-ai-search --platforms baidu,zhihu "你的搜索关键词"

# 开启AI自动总结
cn-ai-search --summarize "AI 创业 2026 机会"

# 按最新排序
cn-ai-search --sort latest "热点事件"

# 指定结果数量
cn-ai-search --count 30 "你的关键词"

# 输出纯文本
cn-ai-search --format plain "你的关键词"
```

## 🔧 安装

```bash
# 安装Python依赖
pip install -r requirements.txt

# 创建命令链接
ln -s $(pwd)/index.py /usr/local/bin/cn-ai-search
chmod +x /usr/local/bin/cn-ai-search
```

## ⚙️ 配置说明

### 免费版（开箱即用）
基础搜索功能完全免费，无需任何API密钥，直接使用。

### 高级功能（开启AI总结）
在`config.py`中填入你的Tavily API密钥即可：
```python
TAVILY_API_KEY = "你的tavily api key"
```
Tavily免费额度是1000次/月，足够个人使用，申请地址：https://tavily.com

### 小红书配置（需要Docker）
```bash
docker run -d --name xiaohongshu-mcp -p 18060:18060 xpzouying/xiaohongshu-mcp
mcporter config add xiaohongshu http://localhost:18060/mcp
```

## 💎 版本说明

| 版本 | 价格 | 功能 |
|------|------|------|
| 社区版 | 免费 | 支持百度/微信/知乎/B站/微博搜索，最多20条结果 |
| 专业版 | **$9.99 一次性授权** | 无限结果，AI总结功能，小红书/抖音支持，终身更新 |
| 企业定制 | $299 起 | 私有部署，定制功能，专属技术支持 |

**获取专业版：** 扫描下方二维码购买，购买后获取完整安装包和激活码。

## 🎯 适用场景

- AI Agent需要获取实时中文信息
- 商业情报搜集、商机挖掘
- 多平台内容聚合调研
- 市场分析、竞品分析
- 新闻热点追踪

## 📝 许可证

Copyright © 2026 钱爪爪 - 八方抓财小能手

社区版免费使用，商业使用请购买专业版授权。
