---
name: health-category-pointer
description: "Pointer to a library of 17 specialized Health skills. Use when working on health-related tasks."
risk: none
---

# Health Capability Library 🎯

This is a **pointer skill**. The 17 specialized Health skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **emergency-card** — 生成紧急情况下快速访问的医疗信息摘要卡片。当用户需要旅行、就诊准备、紧急情况或询问"紧急信息"、"医疗卡片"、"急救信息"时使用此技能。提取关键信息（过敏、用药、急症、植入物），支持多格式输出（JSON、文本、二维码），用于急救或快速就医。
- **family-health-analyzer** — 分析家族病史、评估遗传风险、识别家庭健康模式、提供个性化预防建议
- **fitness-analyzer** — 分析运动数据、识别运动模式、评估健身进展，并提供个性化训练建议。支持与慢性病数据的关联分析。
- **food-database-query** — Food Database Query
- **goal-analyzer** — 分析健康目标数据、识别目标模式、评估目标进度,并提供个性化目标管理建议。支持与营养、运动、睡眠等健康数据的关联分析。
- **health-trend-analyzer** — 分析一段时间内健康数据的趋势和模式。关联药物、症状、生命体征、化验结果和其他健康指标的变化。识别令人担忧的趋势、改善情况，并提供数据驱动的洞察。当用户询问健康趋势、模式、随时间的变化或"我的健康状况有什么变化？"时使用。支持多维度分析（体重/BMI、症状、药物依从性、化验结果、情绪睡眠），相关性分析，变化检测，以及交互式HTML可视化报告（ECharts图表）。
- **mental-health-analyzer** — 分析心理健康数据、识别心理模式、评估心理健康状况、提供个性化心理健康建议。支持与睡眠、运动、营养等其他健康数据的关联分析。
- **nutrition-analyzer** — 分析营养数据、识别营养模式、评估营养状况，并提供个性化营养建议。支持与运动、睡眠、慢性病数据的关联分析。
- **occupational-health-analyzer** — 分析职业健康数据、识别工作相关健康风险、评估职业健康状况、提供个性化职业健康建议。支持与睡眠、运动、心理健康等其他健康数据的关联分析。
- **oral-health-analyzer** — 分析口腔健康数据、识别口腔问题模式、评估口腔健康状况、提供个性化口腔健康建议。支持与营养、慢性病、用药等其他健康数据的关联分析。
- **rehabilitation-analyzer** — 分析康复训练数据、识别康复模式、评估康复进展，并提供个性化康复建议
- **sexual-health-analyzer** — Sexual Health Analyzer
- **skin-health-analyzer** — Analyze skin health data, identify skin problem patterns, assess skin health status. Supports correlation analysis with nutrition, chronic diseases, and medication data.
- **sleep-analyzer** — 分析睡眠数据、识别睡眠模式、评估睡眠质量，并提供个性化睡眠改善建议。支持与其他健康数据的关联分析。
- **tcm-constitution-analyzer** — 分析中医体质数据、识别体质类型、评估体质特征,并提供个性化养生建议。支持与营养、运动、睡眠等健康数据的关联分析。
- **travel-health-analyzer** — 分析旅行健康数据、评估目的地健康风险、提供疫苗接种建议、生成多语言紧急医疗信息卡片。支持WHO/CDC数据集成的专业级旅行健康风险评估。
- **weightloss-analyzer** — 分析减肥数据、计算代谢率、追踪能量缺口、管理减肥阶段

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/health/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/health`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
