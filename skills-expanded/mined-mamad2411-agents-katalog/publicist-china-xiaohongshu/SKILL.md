---
name: publicist-china-xiaohongshu
description: Xiaohongshu (小红书) commercial cooperation rules, 蒲公英 platform reporting, and pitch protocols for mainland China earned media. Use when targeting 小红书 for editorial or commercial placement.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# Xiaohongshu (小红书), China market

**Scope**. Only 小红书 commercial/editorial engagement. Pair with `publicist-china`.

## Platform rules (2024-25 verified)

### Mandatory: 蒲公英平台报备
All brand-creator cooperation MUST report via 蒲公英. Unreported = "水下交易" = violation.

### Brand violation scoring (累积扣分制)
| Score | Penalty |
|---|---|
| 2分 | Warning |
| 4分 | Limit natural traffic for brand-related notes (past 28d + future 7d) |
| 6分 | Full-domain traffic limit (7 days) |
| 8分 | Full-domain traffic limit (28 days) |
| 10分 | Brand banned (28 days) |

**Service fee**. 10% platform commission on creator fee (private deal: 0% but illegal)
**Private deal risk**. Platform AI detects unreported commercial notes → brand penalized, creator throttled

### Content classification (required)
- `editorial`, pure organic, no commercial exchange
- `商单` / `付费合作`, paid, must report + label
- `利益相关申明`, non-cash benefits (free product, trip, etc.), must declare in note

**Declared notes**. Normal distribution (no extra throttling)
**Undeclared commercial**. Traffic limit / removal

### Pitch protocol

#### Pre-pitch verification
1. **Creator eligibility**. ≥5000 fans + 专业号认证 (entry ticket)
2. **Account health**. Check 盐值, recent commercial ratio (≤20%/month historically, now flexible but creators self-limit)
3. **Content fit**. Read last 10-20 notes for beat, style, engagement authenticity
4. **Category sensitivity**. Medical aesthetics, finance, functional products, before/after photos, P-heavy edits → high rejection risk

#### Contact flow
1. **蒲公英平台** → search creator → send brief → creator accepts → platform generates contract
2. **Brief must include**. Core message, required talking points, prohibited words (极限词: "最/唯一/100%有效"), disclosure format
3. **Creator drafts** → brand reviews → creator publishes → brand confirms completion

#### Note requirements
- **Length**. 普通分享≥100字; 教程/测评≥600字
- **Authenticity**. 对比图需注明"原相机+拍摄时间"
- **AI content**. 必须标注"AI生成"
- **No repost**. 3个月内重复内容 → 拉黑 + 历史笔记降权
- **Disclosure position**. 笔记开头或显著位置 "感谢XX品牌赞助" / #广告 #合作

### Compliance checklist (per pitch)
- [ ] 蒲公英报备完成 (not just creator verbal agreement)
- [ ] Brand violation score checked (pre-pitch)
- [ ] Creator eligibility verified (粉丝≥5000 + 专业号)
- [ ] Content classification declared in brief
- [ ] Disclosure format specified (开头/显著位置)
- [ ] 极限词清单 provided to creator
- [ ] AI segments → 显性+隐性标识
- [ ] Medical/finance/functional → `NEEDS_REVIEW` + 法务确认

## References
- `wiki/public-relations/providers/xiaohongshu.md` (to create)
- 小红书《品牌违规扣分管理规则》2024
- 小红书《社区公约2.0》2025
- 千瓜数据 商业合作指引
- 36氪 "小红书限流、封杀爆款笔记" 2024

## What this skill does not do
- ❌ No creator contact export (platform owns relationship)
- ❌ No guaranteed placement (creator/platform discretion)
- ❌ No MCP/CLI tools (reference only)
