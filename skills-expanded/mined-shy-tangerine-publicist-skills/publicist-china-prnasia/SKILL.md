---
name: publicist-china-prnasia
description: PR Newswire Asia / Cision (美通社) wire service usage, ProfNet China interview hotline, and distribution protocols for mainland China earned media. Use when distributing press releases or accessing media databases in mainland China.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# PR Newswire Asia / Cision (美通社), China market

**Scope**. Wire distribution, media database research, ProfNet China. Pair with `publicist-china`.

## Services (2024 verified)

### 1. 美通社媒体人数据库 + Cision 媒体数据库
- **Coverage**. 1300+ 金融/科技/医疗/旅游/零售/B2B 垂类媒体
- **New 2024**. 新华企业资讯渠道, 分发至腾讯/新浪财经/《金融时报》中文版等头部
- **Social reach**. 微博/微信/百度等平台曝光 5亿次/年；社交关注者新增 21万，总计 280万
- **Use case**. 按地区/媒体类别/话题发现媒体联系人

### 2. ProfNet 中国大陆采访热线
- **Function**. 媒体需求 ↔ 企业专家 回应渠道
- **Rule**. ProfNet 机会必须按原始采访需求规定回复，**不得转成通用推销名单**
- **2024**. 亚太区 7000+ 新记者/媒体机构加入

### 3. 新闻稿分发
- **Channels**. 腾讯、新浪财经、金融时报中文版、1300+ 垂类媒体
- **Price band**. ¥3000-8000/篇 (套餐制)
- **Format**. 文字、图片、多媒体、视频新闻稿

## Usage protocol

### Media database research
1. **Define**. Topic, industry, region first
2. **Filter**. Use authorized Cision/美通社 functions
3. **Verify**. Cross-check journalist identity, beat, recent work on outlet official site
4. **Record**. `provider=PR Newswire Asia/Cision`, query date, filters, data class, contact channel

### ProfNet response
1. **Receive**. Original journalist request via ProfNet
2. **Qualify**. Match expert to hard requirements (beat, deadline, format, CST)
3. **Respond**. Via **original request channel only**, email/form specified in request
4. **Record**. `provider=ProfNet request`, provenance=`ProfNet request`

### Press release distribution
1. **Prepare**. Chinese headline, lead, verified facts, methodology, limitations, CST availability
2. **Classify**. `editorial` / `企业供稿` / `分发`, declare in release
3. **Distribute**. Select channel package (national/vertical/regional/social)
4. **Track**. Pickup reports, media monitoring, social amplification

## Compliance checklist
- [ ] Account authorized (valid 美通社/Cision subscription)
- [ ] PIPL cross-border check: journalist data → 境外CRM/模型需单独告知+同意+出境机制
- [ ] ProfNet response via original channel only
- [ ] Release classification declared (`editorial`/`企业供稿`/`分发`)
- [ ] AI-generated segments → 显性+隐性标识
- [ ] 敏感行业/外企采访政府国企 → `NEEDS_REVIEW` + 法务确认
- [ ] Current legal terms: `prnasia.com/legal/` + `PIPL-Customer-Privacy-Notice/`

## References
- `wiki/public-relations/providers/pr-newswire-asia.md` (to create)
- `wiki/public-relations/providers/profnet.md` (to create)
- `skills/publicist-china/references/contact-providers.md`
- 美通社 2024 亚太网络扩张新闻稿
- PR Newswire 白皮书 "5种扩大英文新闻稿影响力的创新策略" 2024

## What this skill does not do
- ❌ No credential storage (user provides)
- ❌ No automated distribution (use provider UI/API)
- ❌ No contact export beyond authorized fields
- ❌ No MCP/CLI tools (reference only)
