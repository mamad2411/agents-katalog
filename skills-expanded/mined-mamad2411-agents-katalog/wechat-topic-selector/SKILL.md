---
name: wechat-topic-selector
description: 微信公众号选题助手 - 基于热榜内容拆解 + 用户方向匹配，智能生成爆款选题。支持多平台热榜获取、内容拆解分析、方向匹配打分，输出 3 个精选选题。
homepage: https://github.com/lucianaib0318/wechat-auto-publish
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":["python3","curl","mcporter"]}}}
---

# 微信公众号选题助手 📝

> **热榜驱动的智能选题引擎，让每一篇都踩在流量上**

基于全网热榜内容拆解 + 用户方向匹配，智能生成 3 个爆款选题。

---

## ✨ 特性

- 🎯 **方向定制** - 用户自定义领域（AI/职场/产品/技术等）
- 📊 **多平台热榜** - 微博、百度、CSDN、GitHub、知乎 5 大平台
- 🔍 **内容拆解** - 关键词提取、情绪分析、类型识别、角度挖掘
- 🤖 **智能匹配** - 方向匹配度打分（0-100 分）
- 📝 **标题生成** - 公众号风格标题模板
- 🔄 **角度多样** - 方法论/案例拆解/趋势预测/热点追踪

---

## 🚀 快速开始

### 基础用法

```bash
# 获取 AI 技术方向选题
python3 topic_selector.py --direction "AI 技术"

# 获取职场成长方向选题
python3 topic_selector.py -d "职场成长"

# 获取产品经理方向选题（5 个）
python3 topic_selector.py -d "产品经理" --top 5
```

### 指定平台

```bash
# 只获取技术类平台（CSDN + GitHub）
python3 topic_selector.py -d "AI 技术" --platform csdn,github

# 只获取社会热点平台（微博 + 百度）
python3 topic_selector.py -d "职场成长" --platform weibo,baidu
```

---

## 📊 输出示例

### 输入
```bash
python3 topic_selector.py -d "AI 技术"
```

### 输出
```
======================================================================
📝 微信公众号选题推荐 - AI 技术
生成时间：2026-03-13 16:50:00
======================================================================

【选题 1】匹配度：85 分
标题：《AI 技术人必看：2026 全球大模型深度对决的 3 个关键方法》
角度：方法论
来源：CSDN 热榜 - 2026 全球大模型深度对决：GPT-5、Claude 4...
关键词：AI, 大模型，技术
情绪：neutral | 类型：解读
链接：https://blog.csdn.net/xxx/article/details/xxx

----------------------------------------------------------------------

【选题 2】匹配度：75 分
标题：案例复盘 | openclaw/openclaw，给 AI 技术人的 5 点启示
角度：案例拆解
来源：GitHub Trending - openclaw/openclaw: ⭐280,000
关键词：AI, 技术
情绪：positive | 类型：热点
链接：https://github.com/openclaw/openclaw

----------------------------------------------------------------------

【选题 3】匹配度：65 分
标题：热评 | 沪深两市成交额突破 1 万亿元，AI 技术人怎么看？
角度：热点追踪
来源：知乎热榜 - 沪深两市成交额突破 1 万亿元
关键词：热点
情绪：positive | 类型：热点

======================================================================
✅ 选题生成完成！

💡 下一步：
   1. 选择一个选题
   2. 运行内容创作：python content_creator.py --topic '<选题标题>'
   3. 生成完整文章并发布
```

---

## 🔧 核心功能

### 1️⃣ 热榜获取

支持 5 大平台：

| 平台 | 获取方式 | 数据类型 |
|-----|---------|---------|
| **微博热搜** | mcporter (weibo MCP) | 社会热点 |
| **百度热搜** | Jina Reader | 综合热点 |
| **CSDN 热榜** | Jina Reader | 技术文章 |
| **GitHub Trending** | GitHub MCP API | 开源项目 |
| **知乎热榜** | Tavily 搜索 | 热门问题 |

### 2️⃣ 内容拆解

每个话题自动分析：

```python
{
    'keywords': ['AI', '大模型', '技术'],  # 关键词
    'emotion': 'positive',                 # 情绪（positive/negative/neutral）
    'type': '解读',                        # 类型（教程/解读/新闻/热点）
    'angle': ['方法论', '案例拆解']        # 切入角度
}
```

### 3️⃣ 方向匹配

匹配度计算（0-100 分）：

- **关键词匹配**（40 分）- 方向关键词与话题重合度
- **热度匹配**（30 分）- 情绪正向 + 内容类型
- **角度匹配**（30 分）- 方法论/案例拆解加分

### 4️⃣ 标题生成

公众号风格标题模板：

| 角度 | 模板示例 |
|-----|---------|
| **方法论** | 《{方向}人必看：{话题}的 3 个关键方法》 |
| **案例拆解** | 案例复盘 | {话题}，给{方向}人的 5 点启示 |
| **趋势预测** | {话题}，{方向}赛道要变天了？ |
| **热点追踪** | 热评 | {话题}，{方向}人怎么看？ |

---

## 📁 项目结构

```
wechat-topic-selector/
├── topic_selector.py       # 主程序
├── SKILL.md                # Skill 文档
├── README.md               # 项目说明
├── requirements.txt        # Python 依赖
├── examples/
│   └── output_sample.md    # 输出示例
└── topic_results.json      # 选题结果（运行后生成）
```

---

## 🎯 使用场景

### 内容创作者
- 每日选题灵感
- 追热点不迷路
- 保持领域垂直度

### 企业新媒体
- 批量生成选题库
- 团队选题评审
- 内容规划参考

### 个人公众号
- 快速确定写作方向
- 提高文章打开率
- 蹭热点有技巧

---

## ⚙️ 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|-----|------|------|--------|
| `--direction` | `-d` | 用户方向/领域 | 必填 |
| `--platforms` | `-p` | 热榜平台列表 | weibo,baidu,csdn,github,zhihu |
| `--top` | `-n` | 返回选题数量 | 3 |

---

## 📊 匹配度参考

| 分数 | 说明 | 建议 |
|-----|------|------|
| **80-100** | 高度匹配 | 强烈推荐，立即写 |
| **60-79** | 中度匹配 | 可以考虑，结合判断 |
| **30-59** | 低度匹配 | 备选选题 |
| **<30** | 不匹配 | 已过滤 |

---

## 🔗 完整工作流

```
1. 选题生成
   ↓
python3 topic_selector.py -d "AI 技术"

2. 内容创作
   ↓
python3 content_creator.py --topic "<选题标题>"

3. 文章排版
   ↓
python3 formatter.py --input article.md

4. 自动发布
   ↓
python3 publisher.py --article article_formatted.md
```

---

## 🙏 致谢

- [weibo-mcp](https://github.com/ModelContextProtocol/servers) - 微博 MCP 服务
- [GitHub MCP](https://github.com/modelcontextprotocol/servers) - GitHub MCP 服务
- [Jina AI](https://jina.ai/) - 网页读取服务
- [Tavily](https://tavily.com/) - 搜索服务

---

**Made with ❤️ for WeChat Official Account creators**
