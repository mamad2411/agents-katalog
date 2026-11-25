---
name: dragoncraft-hub
description: 雕龙·总览 | DragonCraft Hub - description: ［何时使用］当需要管理/导航/查询 22 个叙事场景 skill 时；当需要统一入口、场景对比、依赖关系图时
author: ant (CEO 助理)
created: 2026-04-30
version: 1.1.0
skill_type: 核心🔴
allowed-tools: [Bash, Read, Write, Exec]
tags: [dragoncraft, dragoncraft-hub, narrative, storytelling]
---

# 雕龙·总览 (DragonCraft Hub)
**描述**：叙事 Skill 套件管理器。统一管理 23 个场景 skill，提供导航、对比、依赖关系图。

## 🎯 功能

### 场景清单

| # | Skill | 场景 | 核心输入 | 输出格式 | 特殊合规 |
|---|-------|------|---------|---------|---------|
| 1 | narrative-personal-ip | 个人IP | 做过/看重/遭遇/学到 | 完整版/短视频版/简介版 | 无 |
| 2 | narrative-brand | 品牌 | 为什么存在/相信什么/经历什么/成为什么 | 品牌宣言/创始人故事/手册摘要 | 无 |
| 3 | narrative-product | 产品 | 用户问题/产品动机/解决方案/用户改变 | 发布文案/用户故事/手册摘要 | 无 |
| 4 | narrative-funding | 融资 | 市场机会/团队能力/商业模式/融资需求 | BP故事线/pitch/尽调问答 | 无 |
| 5 | narrative-sales | 销售 | 客户问题/客户犹豫/说服方式/客户改变 | 客户案例/销售话术/异议处理 | 无 |
| 6 | narrative-organization | 组织变革 | 变革动因/变革内容/阻力点/目标状态 | 内部信/路线图/FAQ | 无 |
| 7 | narrative-charity | 公益 | 受助群体/行动/改变/行动号召 | 公益故事/募捐文案/志愿者招募 | 无 |
| 8 | narrative-legal | 法律 | 案件事实/争议焦点/法律依据/主张 | 代理词/事实陈述/法律意见书 | **强制全面披露** |
| 9 | narrative-medical | 医疗 | 病情/治疗方案/医患决策/结果 | 沟通脚本/患者故事/知情同意书 | **强制全面披露** |
| 10 | narrative-social | 社交媒体 | 平台/受众/热点/人设 | 爆款文案/话题标签/互动设计 | 无 |
| 11 | narrative-creative | 创意产品 | 创意概念/目标用户/差异化/用户体验 | 创意说明/用户故事/视觉脚本 | 无 |
| 12 | narrative-lifestyle | 生活方式 | 日常生活/价值观/美学/影响对象 | 宣言/内容规划/视觉指南 | 无 |
| 13 | narrative-tech | 科技 | 技术痛点/技术壁垒/市场机会/商业模式 | 技术故事/pitch/竞品分析 | 无 |
| 14 | narrative-controversy | 争议话题 | 争议焦点/立场/证据/目标 | 立场声明/辩论稿/回应策略 | **承认对立观点合理性** |
| 15 | narrative-art | 艺术 | 作品/创作理念/观众体验/作品影响 | 艺术家陈述/展览前言/作品解读 | 无 |
| 16 | narrative-psychology | 心理 | 心理困境/疗愈过程/成长改变/帮助对象 | 疗愈故事/心理科普/互助指南 | **不得替代专业医疗建议** |
| 17 | narrative-sustainable | 可持续 | 环境问题/行动/改变/下一步 | 可持续报告/行动号召/品牌承诺 | **不得"漂绿"** |
| 18 | narrative-education | 教育 | 课程主题/目标学员/认知误区/学员困境 | 口播稿/视频文案/课程详情页 | 无 |
| 19 | narrative-retrospective | 复盘 | 项目名称/实际结果/关键转折/决策情绪 | 口述稿/书面故事/反事实清单 | 无 |
| 20 | narrative-crisis | 危机公关 | 事件简述/已确认事实/受影响方/核心承诺 | 公开声明/内部信/直播话术 | **强制全面披露** |
| 21 | narrative-personal-brand | 个人品牌 | 主题/认知/是否延续前作 | 新故事/引用标注/宇宙地图/下期建议 | 无 |
| 22 | narrative-product-launch | 产品发布 | 产品名称/发布节奏/目标用户/用户认知 | 碎片地图/顿悟脚本/指引/奖励/排期 | 无 |
| 23 | narrative-book | 书籍写作 | 章节主题/目标读者/燃冰案例/GitHub Skill | 公众号文章版/小红书卡片版/GitHub README 版 | 无 |

### 依赖关系图

```
narrative-suite（管理器）
  ↓
narrative-workflow（编排引擎）
  ↓
narrative-meta（底层操作系统）
  ├── 八刀评估
  ├── 去AI化检测
  ├── 伦理审查
  ├── 人格映射
  └── 记忆管理
  ↓
22 个场景 skill（调用 narrative-meta 模块）
```

### 使用方式

1. **导航**：告诉我你的场景，我推荐对应的 skill
2. **对比**：告诉我两个场景，我输出对比表
3. **依赖查询**：告诉我 skill 名称，我输出依赖关系
4. **批量生成**：告诉我多个场景，我批量生成叙事

## 🔗 依赖关系

本 Skill 依赖以下元 Skill 模块：

| 依赖模块 | 来源 Skill | 用途 |
|---------|-----------|------|
| 八刀评估 | narrative-meta | 质量打分 |
| 去 AI化检测 | narrative-meta | 7 条规则检测 |
| 伦理审查 | narrative-meta | 三条原则检查 |
| 人格映射 | narrative-meta | MBTI 叙事人格推荐 |
| 记忆管理 | narrative-meta | 存储/检索用户历史叙事 |

**调用方式**：通过 narrative-workflow 编排调用，或直接调用 narrative-meta 对应模块。

---

*版本：1.1.0 | 最后更新：2026-04-30*
