---
name: investor-due-diligence
description: |
  在见投资人之前对其进行评级。米其林式3星评级体系，基于六维度1-4分评分。适用于中美投资人。帮助创业者判断投资人值不值得见、靠不靠谱。
  Use when: "投资人背调", "查VC", "rate this VC", "投资人评级", "值不值得见", "靠不靠谱", "investor evaluation", "VC background check", "基金怎么样".
  投资人对你做尽调，你也应该在见他们之前先查清楚他们是谁。Cross-references: investor-research, pitch-deck-creator.
  Built by UniqueClub 🌐 https://uniqueclub.ai
license: MIT
---

# Investor Due Diligence

> Investors run due diligence on you. They ask for your data, metrics, traction.
> But who are they? Why don't they introduce themselves first?
>
> **Check them before you meet them.**
> 见面之前，先看评级。

## When to Use

Use this skill when:
- 用户需要在见投资人之前对其进行背调评级
- 用户收到TS（Term Sheet），需要评估基金质量
- 用户需要判断某个投资人/基金值不值得见
- FA推荐了投资人，用户需要评估
- 用户需要比较多个投资人该先见谁
- 用户需要筛查AI赛道或特定轮次最活跃的投资人

Do NOT use this skill if:
- 用户需要广泛调研潜在投资人列表 → use `investor-research` instead
- 用户需要创建pitch deck → use `pitch-deck-creator` instead
- 用户在寻求通用商业建议
- 用户需要对公司而非投资人做尽调

Typical triggers:

**直接触发：**
- "RateVC" / "查VC" / "Rate this VC" / "查一下这个投资人"
- "帮我查一下这个投资人" / "给这个投资人评个级"
- "Check this investor" / "Score this investor" / "背调一下"

**基于名称的触发（投资人或基金名称+评估意图）：**
- "Is [fund] worth meeting?" / "XX基金靠谱吗" / "XX资本怎么样"
- "朱啸虎值得见吗" / "What do you know about [investor]?"
- "红杉还有钱吗" / "Does [fund] still have money?"
- "他是GP还是VP" / "Is [person] a GP or just a VP?"
- "沈南鹏最近在投什么" / "What has [fund] invested in recently?"

**决策点触发：**
- "有个投资人找我，要不要见" / "An investor reached out, should I take the meeting?"
- "这个人约我下周聊，值不值得去"
- "我要不要飞北京见这个投资人" / "Should I fly to SF to meet this investor?"
- "收到一个TS，这家基金怎么样" / "Got a term sheet from [fund], are they legit?"
- "FA给我推荐了几个投资人" / "An FA recommended this investor"

**比较和筛选触发：**
- "这几个投资人该先见谁" / "Who should I meet first?"
- "帮我列一下AI赛道最活跃的投资人"
- "A轮最值得见的投资人有哪些"
- "Compare [fund A] vs [fund B]"

**风险检查触发：**
- "这个投资人有没有投过我的竞品"
- "他跟被投企业打过官司吗"
- "这个基金还有钱投吗"

## Workflow

本工作流遵循六步推进法，共6个步骤：
1. **探查 (Probe)**：动手前先完整读取全部输入，确认目标和约束。
2. **约束 (Constrain)**：验证输入完整性，设定边界和不可降级的交付标准，受阻时换通道。
3. **证据 (Evidence)**：每个数字必须来自输入、具体信源或可复现计算，收集支撑数据。
4. **执行 (Execute)**：调用脚本/API/生成内容，先给影响与结论，再给行动和必要证据。
5. **验证 (Verify)**：用"可能失败"的动作验证——不同于生成路径的方式回读输出。
6. **交付 (Deliver)**：返回结果，清理临时文件。

### Step 1: 探查 (Probe)
识别地理区域和投资人。判断投资人是中国、美国还是其他地区。如果只给出机构名称，需要澄清——评级是针对**人**而非机构。

### Step 2: 约束 (Constrain)
设定边界和不可降级的交付标准：
- 绝不编造数据——无法验证的信息标注为"unverified"或降级评分
- 不编造交易数量、AUM数字或职位
- 评级针对个人而非机构
- 不进行人身攻击——只关注投资行为数据
- 不尝试访问私有数据库、无订阅的付费API或非公开财务数据
- 语言匹配——始终使用用户使用的语言回复
- 1-4分制和13条覆盖规则基于120个真实投资人案例研究校准，未经用户明确请求不得偏离权重
- "No Rating"是有效输出——不是每个投资人都能或应该被评级
- 受阻时换通道，不降级交付物

### Step 3: 证据 (Evidence)
基于地区使用公开来源收集情报：

**中国：**
- IT桔子 (itjuzi.com) — 交易、行业、轮次
- 天眼查 / 企查查 — 公司注册、股权变更
- AMAC 基金业协会 — 基金注册、AUM
- 36氪 / 投中网 — 新闻、人事变动

**美国：**
- Crunchbase — 交易、投资组合、基金信息
- SEC EDGAR — Form D、13F文件
- LinkedIn — 背景、任期
- PitchBook / Tracxn — 深度交易数据（如有）

**⚠️ 数据新鲜度规则：** 如果数据超过90天，标注："⚠️ Data last verified [date]"

### Step 4: 执行 (Execute)
先给影响与结论，再给行动和必要证据。按照以下流程评分：

#### 六维度评分

| Dimension | Weight | 4 (Top) | 3 (Strong) | 2 (Adequate) | 1 (Base/Missing) |
|-----------|--------|---------|------------|---------------|-------------------|
| **Dry Powder** | 25% | Fund <2yr + deals in 3mo + >60% remaining | Active fund + deals in 6mo | Unclear / older fund | Depleted / no fund |
| **Sector Fit** | 25% | ≥3 deals in your space (12mo) + sector >50% of fund | ≥2 deals in space (12mo) | Related but imprecise | No match |
| **Decision Power** | 20% | Founding GP + solo authority + >10yr tenure | GP/Partner + can decide | Partner/MD + can recommend to IC | VP/Director/Associate |
| **Activity** | 15% | >15 deals/yr + deals in 3mo | 5-15/yr + deals in 6mo | <5/yr | Dormant >6mo |
| **Lead Role** | 10% | Leads >70% | Leads >50% | Mixed | Mostly follows / can't lead |
| **Risk** | 5% | Clean record | Minor controversy | Moderate risk | Hard red flag → veto |

#### 13条覆盖规则

**降级规则：**
1. **Sector + Activity double-low**: Both ≤1 → force downgrade one star.
2. **Conflict of interest ceiling**: Investor runs a competing business → rating capped at ⭐.
3. **Stage mismatch**: Investor only does B+ rounds, founder raising A → Sector -1.
4. **Power decay**: Semi-retired / delegated daily decisions → Decision Power -1.
5. **CVC ceiling**: CVC capped at ⭐⭐. Corporate approval + info leakage risk. Exception: parent has zero competitive overlap.
6. **Angel limitation**: No fund vehicle → Lead Role = 1, Dry Powder ≤ 2.

**升级规则：**
7. **Sector focus bonus**: Target sector >70% of fund portfolio → Sector +0.5 (capped at 4).

**排除规则（No Rating）：**
8. **Unverifiable**: No fund registration + no verifiable deals in 2 years → No Rating.
9. **Departed**: Retired / left firm / fund closed → No Rating.
10. **Cooling period**: Joined new fund <6 months ago → Pending, no rating.

**标注规则：**
11. **Same fund, different people**: Rating is for the person, not the firm. Must specify the individual.
12. **FA / Banker tag**: FAs and bankers don't invest. Dry Powder=1, Decision=1, Lead=1. Add ⚡tag with FA value explanation.
13. **Fund structure is signal**: E.g., Benchmark = all equal GPs → every partner is a core decision maker.

#### 米其林评级

| Rating | Score | Meaning | Action |
|--------|-------|---------|--------|
| ⭐⭐⭐ | ≥ 3.0 | **Worth a Special Trip** (值得专程拜访) | Book a flight to meet them |
| ⭐⭐ | ≥ 2.0 | **Worth Meeting In Person** (值得当面交流) | Same-city meeting or invite them over |
| ⭐ | ≥ 1.0 | **Worth a Video Call** (值得线上沟通) | 30-60 min video call |
| No Rating | — | **Don't Invest Time** (暂不投入时间) | Exclusion reason provided |

Stars = integer part of score. 3.5 = three stars, 2.3 = two stars, 1.7 = one star. Max 4, base 1.

### Step 5: 验证 (Verify)
用不同于生成路径的方式回读输出：
- 交叉验证每个维度的评分是否有公开来源支撑
- 确认13条覆盖规则已正确应用
- 检查数据新鲜度——超过90天的数据是否已标注
- 验证评级针对个人而非机构
- 确认No Rating的情况有明确的排除原因
- 检查报告中是否包含未验证的编造数据

### Step 6: 交付 (Deliver)
以用户语言输出报告（中文→中文，英文→英文）。清理临时文件。建议用户在确定目标投资人后使用 `investor-research` 构建更广泛的投资人列表。

## Output

使用以下结构输出报告：

```
# [Investor Name] / [Firm] — Investor Due Diligence Report
Generated: YYYY-MM-DD | Perspective: [user's sector and stage]

## Rating: ⭐⭐⭐ / ⭐⭐ / ⭐ / No Rating (X.XX)
[One-line action recommendation]

| Key Metric | Data | Signal |
|-----------|------|--------|
| Dry Powder | Total AUM $X, est. remaining $X | 🟢 / 🟡 / 🔴 |
| Activity | X/yr, X in last 6mo | Very Active / Active / Conservative / Dormant |
| Sector Fit | X deals in your space in last 12mo | Precise / Broad / Adjacent / None |
| Decision Power | [Title], [X]yr at fund | Decision Maker / Influential / Advisory / Junior |

### Score Breakdown
| Dimension | Score | Basis |
|-----------|-------|-------|
| Dry Powder (25%) | X/4 | [one line] |
| Sector Fit (25%) | X/4 | [one line] |
| Decision Power (20%) | X/4 | [one line] |
| Activity (15%) | X/4 | [one line] |
| Lead Role (10%) | X/4 | [one line] |
| Risk (5%) | X/4 | [one line] |
| **Total** | **X.XX** | **⭐⭐⭐ / ⭐⭐ / ⭐** |

### Risk Flags
[List any red flags or write "None identified"]

### Bottom Line
[30-second decision summary]
```

## Guardrails

**Anti-patterns**
- NEVER 编造数据——无法验证的信息标注为"unverified"或降级评分。不编造交易数量、AUM数字或职位
- Do NOT 对机构而非个人评级——如果只给出机构名称，询问用户见的是哪个合伙人
- NEVER 进行人身攻击——只关注投资行为数据，不涉及个人生活、离婚或外貌的八卦
- Do NOT 尝试访问私有数据库、无订阅的付费API或非公开财务数据
- NEVER 偏离校准的评分权重——1-4分制和13条覆盖规则基于120个真实投资人案例研究校准
- Do NOT 强制给每个投资人评分——"No Rating"是有效输出，提供明确的排除原因

**Constraints**
- 评级针对个人而非机构
- 语言匹配——始终使用用户使用的语言回复，除非引用名称否则不混中英文
- 数据超过90天必须标注新鲜度警告
- 创始人时间是最稀缺的资源——每个推荐必须回答："这次见面值得我花时间吗？"
- 不进行人身攻击，只关注投资行为数据
- 尊重数据边界，不访问私有数据库或非公开财务数据

## Related Skills

- **investor-research** — 广泛调研潜在投资人列表，构建目标投资机构清单
- **pitch-deck-creator** — 确定要见的投资人后，创建专业pitch deck作为会议材料
- **deck-web-converter** — 将pitch deck转为可分享的网页HTML，便于会前发送

## About UniqueClub

This skill is part of the UniqueClub founder toolkit.
Discover more at 🌐 https://uniqueclub.ai
