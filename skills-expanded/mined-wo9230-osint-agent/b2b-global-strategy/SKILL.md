---
name: b2b-global-strategy
description: "B2B制造业全球化市场战略规划。五步流程：多平台竞品识别→竞争格局分析→市场切入策略→区域市场开发→数字推广战略。智能检测产品渠道（纯B2B/B2B+B2C），自动跳过不相关分析。触发词：b2b-gtm, 出海战略, 全球化布局, market entry, go-to-market。"
---

# B2B 全球化市场战略规划

> 由 `/osint [产品关键词] b2b-gtm` 命令触发
> 核心哲学：中国制造的全球化不是"把产品搬到海外平台"，而是**找到结构性机会，用系统性方法建立可持续的竞争优势**。

## 为什么需要这个 Skill

```
痛点：
- 中国制造企业有产品能力，但缺乏全球市场的系统认知
- 不知道竞争对手是谁、在哪里、有多强
- 不知道该进哪个国家、用哪个渠道、花多少钱
- "铺平台+等询盘"的被动模式，转化率极低
- 年销几百万的工厂想做到1000万，不知道卡在哪里

解决：
- 系统性扫描4大平台的竞品格局
- 量化竞争强度，找到结构性空白
- 制定阶段性GTM路线图（0→100万→500万→1000万）
- 精准匹配目标区域市场
- 输出可执行的数字营销方案
```

---

## 五步战略分析流程

```
Step 1: 竞品地图          → 4平台扫描，建立20-30家对标企业库
         ↓
      [渠道检测]          → 自动判断：纯B2B / B2B+Amazon / B2B+DTC
         ↓
Step 2: 竞争格局          → 市场份额估算 + SEO难度 + 竞争定位图
         ↓
Step 3: 市场切入          → 差异化策略 + 0→1000万阶段分解
         ↓
Step 4: 区域优先级        → 国家评估矩阵 + Top 5 国家详细卡片
         ↓
Step 5: 数字推广          → 平台选择 + SEO + 内容 + 广告 + CRM
         ↓
      [输出报告]          → reports/osint/YYYY-MM-DD_[产品]_b2b-gtm.md
```

---

## 智能渠道检测（Step 1 完成后自动执行）

> 不同产品的渠道组合完全不同。模具机不需要分析Amazon，手机壳不需要分析ThomasNet。

### 检测方法

```
1. Amazon 检测
   WebSearch "[产品关键词]" site:amazon.com
   → 有结果 + BSR < 50000 → HAS_AMAZON = true
   → 无结果 或 BSR > 100000 → HAS_AMAZON = false

2. DTC/独立站 检测
   检查 Step 1 识别的竞品中，是否有 3+ 家拥有 Shopify/独立站
   → 有 → HAS_DTC = true
   → 无 → HAS_DTC = false

3. 主渠道判断
   → Alibaba 结果 > 100 + ThomasNet 有结果 → PRIMARY = "B2B平台"
   → Amazon BSR < 10000 + 多品牌竞争 → PRIMARY = "Amazon"
   → 竞品多数有独立站 → PRIMARY = "DTC"
```

### 渠道影响矩阵

| 检测结果 | Step 2 影响 | Step 3 影响 | Step 5 影响 |
|---------|------------|------------|------------|
| **纯B2B**（HAS_AMAZON=false, HAS_DTC=false） | 聚焦 Alibaba/ThomasNet/Google 竞争 | GTM 以 B2B 平台+展会为主 | 跳过 Amazon/Shopify 策略 |
| **B2B+Amazon** | 加载 osint-competitor 的 Amazon 层 | GTM 包含 Amazon 渠道 | 包含 Amazon 运营策略 |
| **B2B+DTC** | 加载 osint-pricing-anatomy 的 DTC 分析 | GTM 包含独立站渠道 | 包含 SEO+内容营销策略 |
| **全渠道** | 全部加载 | 全渠道 GTM | 完整数字营销组合 |

---

## 各步骤加载

执行分析时，按顺序加载对应子文件：

| 步骤 | 加载文件 | 条件性加载 |
|------|---------|-----------|
| Step 1 | `skills/b2b-global-strategy/step1-competitor-mapping.md` | 始终加载 |
| Step 2 | `skills/b2b-global-strategy/step2-competitive-landscape.md` | 始终加载 |
| Step 3 | `skills/b2b-global-strategy/step3-market-entry.md` | 始终加载 |
| Step 4 | `skills/b2b-global-strategy/step4-regional-markets.md` | 始终加载 |
| Step 5 | `skills/b2b-global-strategy/step5-digital-strategy.md` | 始终加载 |
| 参考 | `skills/b2b-global-strategy/references/b2b-platforms.md` | Step 1 需要时 |
| 参考 | `skills/b2b-global-strategy/references/regional-market-data.md` | Step 4 需要时 |

### 条件性复用现有 Skill

| 条件 | 复用 Skill | 用途 |
|------|-----------|------|
| HAS_AMAZON = true | `skills/osint-competitor.md` 的 Amazon 竞品层 | BSR/评价/品牌集中度分析 |
| HAS_DTC = true | `skills/osint-pricing-anatomy.md` | 倍率分析、渠道定价策略 |
| Step 3 战略分析 | `skills/strategic-growth-advisor/` 的 Porter/Hormozi/Martin | 五力分析、价值方程、战略选择 |
| 用户需要销售手册 | `skills/osint-sales-playbook.md` | 对识别的Top客户生成触达方案 |
| 用户需要深入调查某竞品 | `skills/osint-company.md` | 公司深度调查 |

---

## 脉弱交叉分析（B2B GTM 专用）

> 在 Step 5 完成后，执行 B2B GTM 专用脉弱检测。

```
□ 头部竞品集中在Alibaba但Google排名弱？ → SEO突破口
□ ThomasNet有大玩家但Alibaba没有？ → 市场信息不对称机会
□ 竞品员工增长但询盘关键词下降？ → 渠道转移信号
□ 某区域需求增长但无本地化竞品？ → 区域空白市场
□ 竞品定价高但评价差？ → 质价不符，切入窗口
□ 竞品有认证优势但产品线窄？ → 品类扩展机会
□ 某平台竞品密集但另一平台空白？ → 跨平台套利
□ 行业展会参展商减少但线上询盘增？ → 渠道迁移趋势
```

---

## 输出报告模板

文件名: `reports/osint/YYYY-MM-DD_[产品关键词]_b2b-gtm.md`

```markdown
# [产品类型] 全球化市场战略报告

> **分析日期**: YYYY-MM-DD | **产品**: [关键词] | **渠道**: B2B [+Amazon] [+DTC]

## 执行摘要
**核心结论**: [一段话概括]
**关键数据**:
- 全球市场规模: ~$X
- 竞争格局: [集中/分散/碎片化]
- 推荐切入区域: [区域名]
- 推荐渠道: [平台名]
- 12个月销售目标: ¥X万

**渠道检测结果**:
- Amazon: [✅ 有/❌ 无] — [依据]
- DTC/独立站: [✅ 有/❌ 无] — [依据]
- 主渠道: [Alibaba/ThomasNet/Google/Amazon]

## 第一章: 竞品地图
[Step 1 输出 — 4平台 × 5家 = 20家对标企业]

## 第二章: 竞争格局
[Step 2 输出 — 份额估算 + SEO + 定位图]

## 第三章: 市场切入策略
[Step 3 输出 — Where to Play + How to Win + 阶段目标]

## 第四章: 区域市场优先级
[Step 4 输出 — 评估矩阵 + Top 5 国家卡片]

## 第五章: 数字推广战略
[Step 5 输出 — 平台 + SEO + 内容 + 广告 + CRM]

## 第六章: 脉弱发现
| # | 交叉维度 | 发现 | 信号强度 | 机会 |
|---|---------|------|---------|------|

## 第七章: 行动计划
### Phase 0: 基础建设（0-3个月）
### Phase 1: 验证期（3-6个月）→ 目标: ¥100万
### Phase 2: 增长期（6-12个月）→ 目标: ¥500万
### Phase 3: 规模化（12-24个月）→ 目标: ¥1000万

## 附录: 数据来源
| 来源 | URL | 采集时间 |
|------|-----|---------|
```

---

*本 skill 产出仅供商业决策参考。市场数据基于公开信息估算，实际结果可能因执行力、市场变化等因素而异。*
