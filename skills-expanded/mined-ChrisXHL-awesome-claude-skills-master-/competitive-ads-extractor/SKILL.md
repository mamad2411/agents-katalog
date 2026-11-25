---
name: competitive-ads-extractor
description: 从广告库（Facebook, LinkedIn 等）中提取和分析竞争对手的广告，以了解哪些信息传达、痛点和创意方法是有效的。帮助激发灵感并改善您自己的广告活动。
---

# 竞争对手广告提取器

此技能从广告库中提取您的竞争对手的广告，并分析哪些是有效的——他们强调的问题、他们针对的用例以及产生共鸣的文案/创意。

## 何时使用此技能

- 研究竞争对手的广告策略
- 为您自己的广告寻找灵感
- 了解市场定位
- 识别成功的广告模式
- 分析有效的信息传达
- 发现新的用例或痛点
- 使用经过验证的概念规划广告活动

## 此技能做什么

1. **提取广告**: 从 Facebook 广告库、LinkedIn 等抓取广告
2. **捕获截图**: 保存所有广告的视觉副本
3. **分析信息传达**: 识别问题、用例和价值主张
4. **分类广告**: 按主题、受众或格式分组
5. **识别模式**: 发现常见的成功方法
6. **提供见解**: 解释为什么某些广告可能表现良好

## 如何使用

### 基本提取

```
Extract all current ads from [Competitor Name] on Facebook Ad Library
```

```
Scrape ads from [Company] and analyze their messaging
```

### 特定分析

```
Get all ads from [Competitor] focusing on their messaging 
about [specific problem]. What pain points are they highlighting?
```

### 竞争集

```
Extract ads from these 5 competitors: [list]. 
Compare their approaches and tell me what's working.
```

### 特定平台

```
Get LinkedIn ads from [Competitor] and analyze their 
B2B positioning strategy
```

## 示例

**用户**: "从 Facebook 广告库中提取 Notion 的广告，并告诉我哪些信息传达对他们有效。"

**过程**:
```
Accessing Facebook Ad Library...
Searching for: Notion
Found: 23 active ads

Extracting screenshots...
[████████████████████] 100%

Saved to: competitor-ads/notion/
- ad-001-collaboration.png
- ad-002-productivity.png
- ad-003-templates.png
...

Analyzing messaging...
```

**输出**:
```
# Notion 广告分析

## 概述
- 广告总数: 23 个活跃
- 主要主题: 生产力 (35%), 协作 (30%), 
  模板 (20%), AI 功能 (15%)
- 广告格式: 静态图片 (60%), 视频 (40%)
- CTA 模式: "Try for free", "Get started"

## 他们强调的关键问题

1. **信息分散** (8 个广告)
   文案: "Stop switching between 10 different tools"
   为什么有效: 许多团队面临的直接痛点

2. **会议过载** (5 个广告)
   文案: "Replace unnecessary meetings with async updates"
   为什么有效: 后疫情时代远程工作的痛点

3. **丢失文档** (4 个广告)
   文案: "Never ask 'where is that doc?' again"
   为什么有效: 普遍的工作场所挫折

## 成功的创意模式

### 模式 1: 对比前/后
- 展示混乱的工具环境 → 整洁的 Notion 工作区
- 用于 6 个高绩效广告
- 视觉隐喻即刻清晰

### 模式 2: 功能展示
- 实际产品使用的 GIF
- 在 5 秒内展示特定功能
- 用于新功能 (AI, 模板)

### 模式 3: 社会证明
- "Join 20M users" 信息传达
- 客户 Logo
- 用于 4 个针对企业的广告

## 有效的文案

最佳标题:
1. "Your team's knowledge, finally in one place"
   → 聚焦利益，直接解决痛点
   
2. "The all-in-one workspace"
   → 清晰的定位，广泛的吸引力
   
3. "AI that actually helps you work"
   → 解决对 AI 的怀疑，实用角度

最佳正文文案模式:
- 短句 (10 个词以下)
- 关注结果而非功能
- 包含具体数字 ("Cut meetings by 50%")

## 受众定位见解

基于广告变体:
- 初创公司创始人: 个人生产力角度
- 团队领导: 协作和对齐
- 企业: 安全和合规提及
- 学生: 免费计划、模板、组织

## 对您广告的建议

1. **测试“工具蔓延”痛点**
   → 基于他们的广告频率，共鸣强烈

2. **使用产品截图而非抽象视觉效果**
   → 他们所有顶级广告都展示实际 UI

3. **以问题为主导，而不是解决方案**
   → "Tired of X?" 表现优于 "Introducing Y"

4. **保持文案在 100 个字符以下**
   → 他们最短的广告似乎最频繁

5. **测试前/后视觉格式**
   → 他们创意中经过验证的模式

## 已保存文件
- 所有广告: ~/competitor-ads/notion/
- 分析: ~/competitor-ads/notion/analysis.md
- 最佳表现者: ~/competitor-ads/notion/top-10/
```

**灵感来源:** Lenny's Newsletter 中的 Sumant Subrahmanya 用例

## 您可以学到什么

### 信息传达分析
- 他们强调什么问题
- 他们如何针对竞争对手定位
- 产生共鸣的价值主张
- 目标受众细分

### 创意模式
- 有效的视觉风格
- 视频与静态图片表现
- 配色方案和品牌推广
- 布局模式

### 文案公式
- 标题结构
- 号召性用语模式
- 长度和基调
- 情感触发

### 活动策略
- 季节性活动
- 产品发布方法
- 功能公告策略
-由于重定向模式

## 最佳实践

### 法律与道德
✓ 仅用于研究和灵感
✓ 不要直接复制广告
✓ 尊重知识产权
✓ 使用见解来通知原创创意
✗ 不要剽窃文案或窃取设计

### 分析技巧
1. **寻找模式**: 什么主题重复？
2. **随时间跟踪**: 每月保存广告以查看演变
3. **测试假设**: 调整成功的模式以适应您的品牌
4. **按受众细分**: 针对不同目标的不同信息
5. **比较平台**: LinkedIn 与 Facebook 的信息传达不同

## 高级功能

### 趋势跟踪
```
Compare [Competitor]'s ads from Q1 vs Q2. 
What messaging has changed?
```

### 多竞争对手分析
```
Extract ads from [Company A], [Company B], [Company C]. 
What are the common patterns? Where do they differ?
```

### 行业基准
```
Show me ad patterns across the top 10 project management 
tools. What problems do they all focus on?
```

### 格式分析
```
Analyze video ads vs static image ads from [Competitor]. 
Which gets more engagement? (if data available)
```

## 常见工作流

### 广告活动规划
1. 提取竞争对手广告
2. 识别成功模式
3. 记录他们信息传达中的差距
4. 头脑风暴独特的角度
5. 起草测试广告变体

### 定位研究
1. 获取 5 个竞争对手的广告
2. 绘制他们的定位
3. 寻找未被充分服务的角度
4. 开发差异化信息传达
5. 针对他们的方法进行测试

### 创意灵感
1. 按主题提取广告
2. 分析视觉模式
3. 记录颜色和布局趋势
4. 改编成功模式
5. 创建原创变体

## 成功秘诀

1. **定期监控**: 每月检查更改
2. **广泛研究**: 也要查看相邻的竞争对手
3. **保存一切**: 建立参考库
4. **测试见解**: 运行您自己的实验
5. **跟踪绩效**: A/B 测试受启发的概念
6. **保持原创**: 用于灵感，而不是复制
7. **多平台**: 比较 Facebook, LinkedIn, TikTok 等

## 输出格式

- **截图**: 所有广告保存为图像
- **分析报告**: 见解的 Markdown 摘要
- **电子表格**: 带有广告文案、CTA、主题的 CSV
- **演示文稿**: 最佳表现者的视觉幻灯片
- **模式库**: 按方法分类

## 相关用例

- 为您的活动编写更好的广告文案
- 了解市场定位
- 在您的信息传达中寻找内容差距
- 为您的产品发现新用例
- 规划产品营销策略
- 激发社交媒体内容
