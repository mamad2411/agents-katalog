---
name: ahp-decision-helper
description: Help users make decisions among multiple alternatives using the Analytic Hierarchy Process (AHP). Use when the user needs to choose between multiple options, compare alternatives, rank choices, or decide which option is best for their situation. Triggers on phrases like "帮我选", "哪个更好", "帮我分析", "帮我决定", "优先级", "对比", "AHP", "层次分析法", or any multi-criteria decision scenario.
---

# AHP Decision Helper

Guide users through the Analytic Hierarchy Process to rank alternatives and identify the best choice.

## Workflow

### 1. Identify the Decision Context

Ask the user:
- What decision are they trying to make?
- What are the specific alternatives/options?

If alternatives are not clear, help them articulate 2-5 concrete options.

### 2. Select Evaluation Criteria

Based on the decision domain, propose relevant criteria. Use the domain templates below as a starting point, but allow the user to customize.

**Common domains and suggested criteria:**

| Domain | Suggested Criteria |
|--------|-------------------|
| 买房/租房 | 价格、地段、面积、配套、交通、学区、房龄、户型 |
| 买车 | 价格、油耗/续航、空间、品牌、安全性、保值率、配置、外观 |
| 找工作/选Offer | 薪资、发展空间、工作强度、通勤、团队氛围、公司稳定性、行业前景 |
| 选手机/数码 | 价格、性能、续航、拍照、屏幕、品牌、售后、颜值 |
| 选城市/定居 | 生活成本、就业机会、气候、医疗教育、房价、人际关系、发展潜力 |
| 选课程/培训 | 价格、师资、口碑、课程质量、时间灵活度、就业前景、认证含金量 |
| 旅游/出行 | 预算、风景、舒适度、安全性、便利性、独特性、时间 |
| 通用决策 | 成本、收益、风险、时间、质量、便利性、满意度 |

Ask the user to confirm or modify the criteria list. Aim for 3-7 criteria.

### 3. Collect Pairwise Comparisons for Criteria

For each pair of criteria (i, j), ask: "相对于 [criterion_j]，[criterion_i] 的重要性如何？"

Use a 1-9 scale:
- 1 = 同等重要
- 3 = 稍微重要
- 5 = 明显重要
- 7 = 强烈重要
- 9 = 极端重要
- 2, 4, 6, 8 = 中间值
- 倒数 = 反向比较 (如果 j 比 i 重要，则取倒数)

Collect responses and build the criteria comparison matrix. For n criteria, there are n×(n-1)/2 unique pairs.

**Tip:** To reduce user burden, present comparisons in a natural conversational flow, grouping related comparisons together. You can also offer to use "标准权重" (equal weights) if the user wants to skip detailed comparison.

### 4. Collect Alternative Ratings for Each Criterion

For each criterion, ask the user to compare each pair of alternatives:
"在 [criterion] 方面，[alternative_i] 相比 [alternative_j] 表现如何？"

Use the same 1-9 scale. For each criterion with m alternatives, there are m×(m-1)/2 pairs.

### 5. Build Input JSON and Run Calculation

Construct the input JSON:

```json
{
  "criteria": ["criterion1", "criterion2", ...],
  "criteriaMatrix": [[1, x, ...], [1/x, 1, ...], ...],
  "alternatives": ["alt1", "alt2", ...],
  "alternativeMatrices": {
    "criterion1": [[1, y, ...], [1/y, 1, ...], ...],
    "criterion2": [...]
  }
}
```

Save to a temp file and run:

```bash
node ~/.agents/skills/ahp-decision-helper/scripts/ahp-calculator.js /path/to/input.json
```

### 6. Interpret and Present Results

Parse the JSON output and present results clearly:

1. **Overall Ranking**: Show all alternatives ranked by score
2. **Criteria Weights**: Explain which criteria matter most
3. **Consistency Check**: Confirm if judgments are consistent (CR < 0.1). If not, note it and suggest the user review their comparisons.
4. **Final Recommendation**: State the top choice with supporting rationale

Format example:

```
📊 AHP 决策分析结果

🏆 推荐选择：[最佳选项]

📈 综合得分排名：
1. [选项A] — 得分 0.452
2. [选项B] — 得分 0.331
3. [选项C] — 得分 0.217

⚖️ 准则权重：
• [准则1]: 45.2% (最重要)
• [准则2]: 31.5%
• [准则3]: 23.3%

✅ 一致性检验通过 (CR = 0.03 < 0.1)
```

### 7. Sensitivity Discussion (Optional)

If appropriate, ask: "如果 [某个准则] 的权重变化，结果会不会改变？" and discuss how robust the recommendation is.

## Scale Reference

| 标度 | 含义 |
|------|------|
| 1 | 两个因素同等重要 |
| 3 | 前者比后者稍微重要 |
| 5 | 前者比后者明显重要 |
| 7 | 前者比后者强烈重要 |
| 9 | 前者比后者极端重要 |
| 2,4,6,8 | 上述相邻判断的中间值 |
| 倒数 | 若因素i与j的重要性之比为a，则j与i之比为1/a |

## Script Location

`scripts/ahp-calculator.js` — Node.js script that computes AHP weights, consistency ratios, and overall scores. Accepts a JSON file path as argument and outputs results as JSON.
