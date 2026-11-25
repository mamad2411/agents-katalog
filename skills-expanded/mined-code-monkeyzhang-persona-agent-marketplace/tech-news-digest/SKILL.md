---
name: tech-news-digest
description: 科技硬核技术信息追踪与聚合技能。当用户请求追踪AI/大模型/前沿技术动态、生成技术资讯摘要、或查询特定厂商的最新发布时使用。覆盖海外大厂、独角兽初创、国内厂商的官方技术博客和资讯渠道。
---

# 科技硬核技术信息追踪 (Tech News Digest)

## 1. 信息源注册表

### 1.1 海外大厂 (Big Tech)

| 公司 | 频道 | 链接 | 爬取验证 |
|------|------|------|----------|
| OpenAI | Blog/News | https://openai.com/blog | OK |
| OpenAI | RSS | https://openai.com/news/rss.xml | OK |
| Google DeepMind | Blog | https://deepmind.google/blog/ | OK |
| Google Research | Blog | https://research.google/blog/ | OK |
| Google AI (The Keyword) | Blog | https://blog.google/technology/ai/ | OK |
| Google Developers | Blog | https://developers.googleblog.com/ | OK |
| Anthropic | Research | https://www.anthropic.com/research | OK |
| Anthropic | News | https://www.anthropic.com/news | OK |
| Anthropic | Engineering | https://www.anthropic.com/engineering | OK |
| Meta AI | 官网 | https://ai.meta.com/ | 浏览器可访问 |
| Microsoft Research | Blog | https://www.microsoft.com/en-us/research/blog/ | OK |
| Azure AI | Blog | https://azure.microsoft.com/en-us/blog/tag/azure-ai/ | OK |
| AWS ML | Blog | https://aws.amazon.com/blogs/machine-learning/ | OK |
| Apple ML Research | Research | https://machinelearning.apple.com/ | OK |
| NVIDIA | Technical Blog | https://developer.nvidia.com/blog/ | OK |

### 1.2 海外独角兽/知名初创

| 公司 | 频道 | 链接 | 爬取验证 |
|------|------|------|----------|
| xAI (Grok) | 官网 | https://x.ai/ | 浏览器可访问 |
| Mistral AI | News/Blog | https://mistral.ai/news | OK |
| Cohere | Blog | https://cohere.com/blog | OK |
| AI21 Labs | Blog | https://www.ai21.com/blog | OK |
| DeepSeek | 官网 | https://www.deepseek.com/ | OK |
| Hugging Face | Blog | https://huggingface.co/blog | OK |
| Databricks | Blog | https://www.databricks.com/blog | OK |
| Perplexity | Hub | https://www.perplexity.ai/hub | 浏览器可访问 |
| Runway | News | https://runwayml.com/news | OK |
| Cerebras | Blog | https://www.cerebras.net/blog | OK |
| SambaNova | Blog | https://sambanova.ai/blog/ | OK |
| Groq | Blog | https://groq.com/blog/ | OK |
| Inflection AI | 官网 | https://inflection.ai/ | OK |
| Reka AI | 官网 | https://reka.ai/ | OK |
| Stability AI | 官网 (Press > News & Updates) | https://stability.ai/ | 浏览器可访问 |
| Weights & Biases | Blog | https://wandb.ai/blog | 浏览器可访问 |

### 1.3 国内厂商

| 公司 | 频道 | 链接 |
|------|------|------|
| 百度 (文心) | 开发者平台 | https://developer.baidu.com/ |
| 阿里巴巴 (通义) | 开发者社区 | https://developer.aliyun.com/ |
| 腾讯 (混元) | 云开发者 | https://cloud.tencent.com/developer/ |
| 字节跳动 (豆包) | 火山引擎 | https://www.volcengine.com/ |
| 华为 (盘古) | 华为云 | https://www.huaweicloud.com/ |
| 商汤 | 官网 | https://www.sensetime.com/ |
| 科大讯飞 (星火) | 官网 | https://www.iflytek.com/ |
| 月之暗面 (Kimi) | 官网 | https://www.moonshot.cn/ |
| 智谱AI (GLM) | 官网 | https://www.zhipuai.cn/ |
| MiniMax | 官网 | https://www.minimaxi.com/ |
| 百川智能 | 官网 | https://www.baichuan-ai.com/ |
| 阶跃星辰 | 官网 | https://www.stepfun.com/ |

### 1.4 学术/聚合平台

| 站点 | 链接 |
|------|------|
| ArXiv cs.AI (AI) | https://arxiv.org/list/cs.AI/recent |
| ArXiv cs.CL (NLP) | https://arxiv.org/list/cs.CL/recent |
| ArXiv cs.LG (ML) | https://arxiv.org/list/cs.LG/recent |
| ArXiv cs.CV (CV) | https://arxiv.org/list/cs.CV/recent |
| Hugging Face Daily Papers | https://huggingface.co/papers |
| Papers With Code | https://paperswithcode.com/ |

## 2. 社交媒体账号 (X/Twitter)

| 账号 | 说明 |
|------|------|
| @OpenAI | OpenAI 官方 |
| @GoogleAI | Google AI |
| @GoogleDeepMind | DeepMind |
| @AnthropicAI | Anthropic |
| @MetaAI | Meta AI |
| @MistralAI | Mistral |
| @GoogleResearch | Google Research |
| @huggingface | Hugging Face |
| @ai21labs | AI21 Labs |
| @JeffDean | Jeff Dean (Google) |
| @GoogleOSS | Google Open Source |
| @kaborofficial | Google AI 负责 |

## 3. 使用方式

### 3.1 每日/每周技术资讯摘要
当用户请求"今日技术动态"、"本周AI新闻"等时：
1. 优先从 **已验证可直接爬取的 OK 源** 抓取最新内容。
2. 对于**浏览器可访问**的源，说明无法直接爬取，建议用户自行访问。
3. 按以下维度整理摘要：
   - **模型发布**: 新模型/新版本发布
   - **研究突破**: 重要论文/研究进展
   - **工程实践**: 工具链/基础设施/最佳实践
   - **行业动态**: 融资/合作/政策
   - **开源项目**: 新开源项目/版本更新

### 3.2 特定厂商查询
当用户问"OpenAI 最近有什么更新"等时：
1. 定位对应厂商的信息源链接。
2. 抓取最新内容。
3. 按时间线整理关键更新。

### 3.3 主题追踪
当用户关注特定技术方向（如"Agent"、"RAG"、"推理优化"等）时：
1. 从多个源交叉检索相关内容。
2. 汇总不同厂商在同一方向上的进展对比。

### 3.4 输出格式

生成摘要时使用以下模板：

```markdown
# 技术资讯摘要 - YYYY/MM/DD

## 模型发布
- [厂商] 模型/产品名 - 一句话描述
  - 链接

## 研究突破
- [机构] 论文/研究名 - 一句话描述
  - 链接

## 工程实践
- [厂商] 工具/框架名 - 一句话描述
  - 链接

## 行业动态
- 简要描述
  - 链接

## 开源项目
- 项目名 - 一句话描述
  - 链接
```

## 4. 注意事项

1. **时效性**: 技术资讯变化快，始终从源站实时抓取，不要依赖缓存信息。
2. **准确性**: 区分"官方发布"和"媒体报道"，优先引用官方来源。
3. **标注来源**: 每条信息必须附带原始链接。
4. **爬取限制**: 标注为"浏览器可访问"的源无法程序化抓取，需提醒用户自行访问。
5. **国内厂商**: 国内站点通常需要中文搜索，注意使用正确的中文关键词。
