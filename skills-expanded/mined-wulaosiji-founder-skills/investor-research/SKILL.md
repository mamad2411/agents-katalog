---
name: investor-research
description: |
  调研风险投资机构、天使投资人和融资资金来源。生成结构化的投资人调研报告，包含机构画像、投资 thesis、投资组合、联系策略和热介绍路径。
  Use when: "投资人调研", "找VC", "research investors", "VC list", "funding sources", "investor database", "天使投资人", "venture capital", "融资对象", "投资人画像".
  帮助创业者识别、评估并接触适合其融资轮次的投资人。Cross-references: investor-due-diligence, pitch-deck-creator, deck-web-converter.
  Built by UniqueClub 🌐 https://uniqueclub.ai
license: MIT
---

# Investor Research

> 专业的VC和天使投资人研究员。帮助创业者识别、评估并接触适合其融资轮次的正确投资人。

## When to Use

Use this skill when:
- 用户需要为其创业公司调研潜在投资人
- 用户需要构建目标投资人列表
- 用户需要了解投资人的投资 thesis 和投资组合
- 用户需要找到通往特定VC的热介绍路径
- 用户需要为投资人会议做准备

Do NOT use this skill if:
- 用户需要创建pitch deck → use `pitch-deck-creator` instead
- 用户需要将材料转为网页格式 → use `deck-web-converter` instead
- 用户需要对特定投资人做背调评级 → use `investor-due-diligence` instead
- 用户在寻求通用商业建议

Typical triggers:
- 「帮我找投资人」「VC调研」「目标投资机构列表」「融资对象」
- "research investors", "VC list", "find investors for startup", "funding sources"

## Workflow

本工作流遵循六步推进法，共6个步骤：
1. **探查 (Probe)**：动手前先完整读取全部输入，确认目标和约束。
2. **约束 (Constrain)**：验证输入完整性，设定边界和不可降级的交付标准，受阻时换通道。
3. **证据 (Evidence)**：每个数字必须来自输入、具体信源或可复现计算，收集支撑数据。
4. **执行 (Execute)**：调用脚本/API/生成内容，先给影响与结论，再给行动和必要证据。
5. **验证 (Verify)**：用"可能失败"的动作验证——不同于生成路径的方式回读输出。
6. **交付 (Deliver)**：返回结果，清理临时文件。

### Step 1: 探查 (Probe)
完整读取用户需求，收集以下信息（以编号列表形式一次性提出，不要逐个问）：

```
请提供以下信息，以便精准匹配投资人：

1. 融资阶段（天使轮/Pre-A/A轮/B轮等）
2. 行业领域（SaaS/AI/消费/医疗/金融科技等）
3. 目标融资金额（如：500万人民币 / 2百万美元）
4. 公司所在地（影响币种和区域偏好）
5. 目标投资人类型（只找VC / 天使投资人 / 两者都要）
6. 是否有偏好的投资机构或投资人？
7. 是否需要特定地区或币种的投资人（美元基金 vs 人民币基金）
8. 研究范围（Top 10 精准匹配 vs Top 50 广泛覆盖）
```

### Step 2: 约束 (Constrain)
验证输入完整性，设定边界和不可降级的交付标准：
- 不编造投资数据，未验证信息标注`[待确认]`
- 始终注明研究来源
- 无法找到具体支票金额时，基于典型基金行为提供范围
- 包含免责声明：投资格局变化迅速，需要验证
- 尊重投资人偏好（有些只受热介绍，有些偏好冷邮件）
- 受阻时换通道，不降级交付物

### Step 3: 证据 (Evidence)
每个数据必须来自具体信源或可复现检索。基于用户输入，使用以下方式进行研究：
1. **网络搜索**：投资人数据库和近期融资新闻
2. **投资组合分析**：分析其所在领域相似公司的投资方
3. **投资 thesis 匹配**：基于阶段和行业进行匹配

始终搜索并引用以下数据源：
- Crunchbase profiles
- VC机构网站和投资 thesis 页面
- 该行业近期融资公告
- 投资组合公司列表
- LinkedIn（合伙人背景）
- Twitter/X（投资人公开声明）

### Step 4: 执行 (Execute)
生成综合投资人调研报告（Markdown格式），先给影响与结论，再给行动和必要证据。

#### 报告结构

**Section 1: 投资人汇总表**

| Investor | Type | Stage | Check Size | Focus | Priority |
|----------|------|-------|------------|-------|----------|
| [Name] | VC/Angel | Seed/Series A | $X-$Y | Sector | A/B/C |

**Section 2: 详细投资人画像**

为每个高优先级投资人包含：

#### [Investor Name]
- **Type**: VC firm / Angel / Accelerator
- **Location**: [City, Country]
- **Fund Size**: $X million (if available)
- **Typical Check Size**: $Xk - $Yk
- **Preferred Stages**: Seed / Series A / Series B
- **Investment Thesis**: 2-3 sentences
- **Recent Investments**: 3-5 relevant portfolio companies
- **Key Partners**: Names and backgrounds
- **Decision Timeline**: Typical speed to decision
- **Warm Intro Path**: LinkedIn connections, portfolio founder intros, events

**Section 3: 外联策略**

为每个投资人提供：
1. **Why they fit**: 具体的 thesis 对齐
2. **Approach angle**: 在外联中应强调什么
3. **Warm intro candidates**: 可以介绍的具体人选
4. **Recent signal**: 任何创造时机机会的近期新闻或投资

**Section 4: 行动项**

优先级排序的下一步列表：
1. [ ] Reach out to [Contact] for warm intro to [Investor]
2. [ ] Apply to [Accelerator] by [Deadline]
3. [ ] Attend [Event] to meet [Partner]

### Step 5: 验证 (Verify)
用不同于生成路径的方式回读输出：
- 交叉验证每个投资人的投资数据是否来自可引用来源
- 确认未验证信息已标注`[待确认]`
- 检查支票金额是否合理（基于基金规模和阶段）
- 验证热介绍路径是否具体可行
- 确认免责声明已包含
- 检查行动项是否可执行且有优先级

### Step 6: 交付 (Deliver)
返回调研报告，清理临时文件。告知用户报告已生成，建议用户在联系投资人前先使用 `investor-due-diligence` 对目标投资人做背调评级。

## Output

### 输出格式
将报告保存为 `{CompanyName}_Investor_Research.md`，保存在当前工作目录。

### 报告章节顺序
1. Executive Summary
2. Investor Summary Table
3. Detailed Profiles (Top 10)
4. Outreach Strategy
5. Action Items
6. Appendix: Additional Investors (if applicable)

### 数据来源要求
- 始终注明研究来源
- 不编造投资数据，未验证信息标注`[待确认]`
- 无法找到具体支票金额时，基于典型基金行为提供范围
- 包含免责声明：投资格局变化迅速，需要验证

## 数据源参考

始终搜索并引用：
- Crunchbase profiles
- VC firm websites and investment thesis pages
- Recent funding announcements in the sector
- Portfolio company lists
- LinkedIn for partner backgrounds
- Twitter/X for investor public statements

## Guardrails

**Anti-patterns**
- NEVER 编造投资数据——使用`[待确认]`标注未验证信息
- Do NOT 省略研究来源
- Do NOT 提供过于宽泛的投资人列表而不做优先级排序
- NEVER 忽略投资人偏好（有些只受热介绍，有些偏好冷邮件）
- Do NOT 在未验证的情况下给出具体支票金额——提供范围或标注待确认

**Constraints**
- 所有数据必须来自可引用的公开来源
- 未验证信息必须标注`[待确认]`
- 支票金额无法找到时，基于典型基金行为提供范围
- 必须包含免责声明：投资格局变化迅速，需要验证
- 尊重投资人偏好（热介绍 vs 冷邮件）
- 不尝试访问私有数据库、无订阅的付费API或非公开财务数据

## Related Skills

- **investor-due-diligence** — 在联系投资人前，对目标投资人做米其林式3星背调评级，判断值不值得见
- **pitch-deck-creator** — 确定目标投资人后，创建专业pitch deck作为外联材料
- **deck-web-converter** — 将pitch deck转为可分享的网页HTML，便于邮件/微信传播

## About UniqueClub

This skill is part of the UniqueClub founder toolkit.
🌐 https://uniqueclub.ai
📂 https://github.com/wulaosiji/founder-skills
