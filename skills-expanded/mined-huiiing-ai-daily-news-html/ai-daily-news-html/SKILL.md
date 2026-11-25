---
name: ai_daily_news_html
description: 搜索ai领域新闻，整合每日新闻，整合后生成美观的 HTML 新闻页面。
---

# AI Daily News HTML

搜索ai领域新闻，整合每日新闻，整合后生成美观的 HTML 新闻页面。

## 1. 新闻获取

搜索今日（24小时内）最新的前沿科技与产品资讯。

### 核心关注领域：
- **AI 领域**：大模型版本更新、AI Agent 形态、多模态技术突破、AI Native 应用创新
- **音视频产品**：AI 视频生成、实时流交互、平台产品改版
- **边缘计算**：端侧大模型、本地推理算力突破、IoT落地场景
- **核心大厂动态**：OpenAI, Google, Apple, Meta, 字节跳动, 阿里巴巴等头部公司的产品发布与战略

### 信息源要求：
严格使用 `references/sources.md` 中的信源，不得扩展到白名单外的信源。

**中文信源**：
- AIBase
- 36Kr AI
- 机器之心
- 量子位

**国际信源**：
- Reuters
- TechCrunch
- The Information
- The Verge
- WIRED
- VentureBeat

**官方信源**：
- Google DeepMind Blog
- OpenAI News
- Anthropic Newsroom
- Anthropic Engineering
- NVIDIA Blog

### 搜索流程：
1. **分领域搜索**：按四个核心领域分别进行搜索
   - AI 领域：使用相关关键词搜索
   - 音视频产品：使用相关关键词搜索
   - 边缘计算：使用相关关键词搜索
   - 核心大厂动态：使用相关关键词搜索

2. **搜索语言规则**：
   - 中文信源用中文搜索
   - 英文信源用英文搜索
   - 详细关键词见 `references/search-rules.md`

3. **信源访问工具链**：
   - **回退链**：web_fetch → agent-browser → tavily
   - 详细规则见 `references/sources.md` 和 `references/search-rules.md`

4. **时效性验证**：
   - 必须从文章页面本身确认发布时间在24小时内
   - 不能仅依赖搜索摘要
   - 详细规则见 `references/search-rules.md`

5. **去重规则**：
   - 同一事件合并
   - 优先官方来源
   - 详细规则见 `references/search-rules.md`

6. **数量控制**：
   - 标准：14-16条
   - 扩展：16-20条（新闻密集时）
   - 减少：8-14条（高质量新闻不足时）

## 2. 新闻处理

### 2.1. 新闻分类
每条新闻必须归类到以下6个分类之一：
1. 模型与产品发布
2. Agent与应用落地
3. 企业与商业化动态
4. 基础设施 / 芯片 / 算力
5. 政策 / 监管 / AI安全
6. 研究进展与技术趋势

详细分类定义见 `references/category-taxonomy.md`

### 2.2. 国内新闻数据格式

```json
{
  "id": "domestic-1",
  "title": "新闻标题，完整、事实性、有头有尾",
  "summary": "新闻摘要，50-100字，概括核心内容",
  "content": "详细新闻内容",
  "source": "36氪",
  "link": "https://www.36kr.com/...",
  "category": "模型与产品发布",
  "tag": "模型与产品发布",
  "hotness": 85,
  "date": "2026-04-07",
  "data_tags": ["标签1", "标签2", "标签3"]
}
```

### 2.3. 国外新闻格式

```json
{
  "id": "foreign-1",
  "title": "中文标题（翻译）",
  "title_en": "English title（原始英文标题）",
  "summary": "中文新闻摘要，50-100字（用中文概括）",
  "content": "原始英文内容，完整描述事件",
  "source": "TechCrunch",
  "link": "https://techcrunch.com/...",
  "category": "模型与产品发布",
  "tag": "模型与产品发布",
  "hotness": 90,
  "date": "2026-04-07",
  "data_tags": ["标签1", "标签2", "标签3"]
}
```

### 2.4. 字段说明：
- **id**：唯一标识，用于唯一标识每条新闻，格式为 domestic-1 或 foreign-1 等，其中 1 为新闻序号
- **title**：中文标题
- **title_en**：原始英文标题（仅国际新闻）
- **summary**：中文摘要，50-100字，概括核心内容
- **content**：新闻的具体内容
- **source**：新闻来源（来自s1信源白名单）
- **link**：真实可访问的原始链接
- **category**：新闻类别，使用s1的6个分类之一
- **tag**：与category保持一致，供HTML显示
- **hotness**：新闻的热度（agent智能判断生成）：
    - 范围 0-100
    - 参考因素：
        - 信源优先级（官方信源加分）
        - 内容重要性（模型发布、大厂动态加分）
        - 社会讨论度（热点话题加分）
        - 内容质量（标题、内容完整性加分）
- **date**：新闻日期，格式 YYYY-MM-DD
- **data_tags**：生成中文关键词标签，3-5个（agent智能生成），可选标签包括：开源、多模态、推理、企业服务、消费级产品、开发者工具、合规、融资、数据中心等

### 2.5. 整合新闻数据

将国内和国际新闻整合到一个数据结构中：

```json
{
  "date": "2026-04-07",
  "domestic_news": [...],
  "international_news": [...]
}
```

### 2.6. 生成 AI 摘要

基于所有新闻生成三种风格的 AI 摘要：

1. **故事性风格**：像讲故事一样，用生动的语言串联当天的新闻
2. **简洁版风格**：分点列出核心要点，简明扼要
3. **专业版风格**：更正式、专业的语言，适合深度阅读

### 2.7. 生成排行榜

基于热度评分（hotness），选取热度最高的前 6 条新闻生成今日热点排行榜。

### 2.8. 渲染 HTML 页面

使用 HTML 模板渲染最终页面。

模板位置：`templates/template.html`

需要替换的占位符：
- `{{DATE}}` - 日期，格式 YYYY-MM-DD
- `{{SIDEBAR_INDEX}}` - 侧边栏索引
- `{{RANKINGS}}` - 排行榜 HTML
- `{{DOMESTIC_NEWS}}` - 国内新闻卡片 HTML
- `{{INTERNATIONAL_NEWS}}` - 国际新闻卡片 HTML
- `{{NEWS_DETAILS_JSON}}` - 新闻详情 JSON 数据
- `{{SUMMARY_STORY}}` - 故事性摘要
- `{{SUMMARY_CONCISE}}` - 简洁版摘要
- `{{SUMMARY_PROFESSIONAL}}` - 专业版摘要

## 3. 输出格式

### 最终输出一个完整的 HTML 文件

保存名字建议：`ai_news_daily_YYYYMMDD.html`
路径可由用户自定义

## 4. 重要规则

1. **新闻真实性**：确保所有新闻内容和时间都是真实的，不要臆造新闻
2. **事实性**：只讲事实，不加主观评论
3. **完整性**：每条新闻要有头有尾
4. **美观性**：HTML 页面要美观、响应式，适配电脑端和手机端
5. **时效性**：必须具有时效性，新闻必须是当天的，不能是历史新闻
6. **链接真实性**：确保所有新闻链接都是可访问的对应的新闻原始链接，不能是死链，不能是广告推广
7. **信源白名单**：严格使用 `references/sources.md` 中的信源，不得扩展到白名单外
8. **分类规范**：严格使用6个分类，见 `references/category-taxonomy.md`
9. **搜索规则**：严格遵循 `references/search-rules.md` 中的所有规则

## 5. 使用场景

- 一键生成每日AI新闻汇总页面
- 定时任务自动化生成
- 结合其他 skill 形成完整的新闻系统
