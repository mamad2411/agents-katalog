---
name: publicist-china-bilibili
description: Bilibili (B站) commercial platform, 花火 platform, and pitch protocols for mainland China earned media. Use when targeting B站 for editorial or commercial placement.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# Bilibili (B站), China market

**Scope**. Only B站 commercial/editorial engagement. Pair with `publicist-china`.

## Platform rules (verified)

### Commercial platform: 花火
- **入驻门槛**. 粉丝 ≥1万 UP主必须入驻
- **非私域商单**. 必须通过花火完成合同签署、内容审核、结算
- **未入驻**. 无法接收平台分发广告需求
- **全流程闭环**. 内容→交易→分账一体化

### Content classification
- `editorial`, 纯创作投稿，无商业交换
- `商单` / `付费合作`, 付费，必须走花火 + 标识
- `激励计划`, 平台激励，非品牌方直接付费

## Pitch protocol

### Pre-pitch verification
1. **花火入驻**. UP主是否已入驻花火平台
2. **Account health**. 无违规、近期商单比例合理、粉丝活跃度高
3. **Vertical match**. 科技/数码/游戏/动画/生活/知识/汽车等分区
4. **Content style**. 深度测评/长视频/硬核科普, 社区偏好硬核、真实

### Contact flow (mandatory)
1. **花火平台** → 搜索UP主 → 发送需求 → UP主接单 → 平台合同/审核/结算
2. **Brief must include**. 核心卖点、必展示功能/体验、禁用词、标签要求、数据回传指标
3. **UP主制作** → 品牌审核草稿/成片 → 发布 → 数据回传

### Video content requirements (B站调性)
- **时长**. 深度测评 10-30分钟; 科普 5-15分钟; 短视频 1-3分钟
- **结构**. 引入(痛点/悬念) → 核心体验/数据/对比 → 优缺点诚实评价 → 结论/购买建议
- **弹幕友好**. 预留互动点(提问/投票/梗)
- **标签**. #广告 #合作 #品牌名 + 分区标签
- **封面/标题**. 高点击率风格，避免标题党

### Compliance checklist (per pitch)
- [ ] 花火平台报备完成
- [ ] 商单标识已添加 (视频开头/简介/弹幕)
- [ ] UP主粉丝≥1万 + 花火入驻确认
- [ ] 禁用词/医疗/金融清单提供
- [ ] AI生成片段 → 显性+隐性标识
- [ ] 功能性产品/医疗/金融 → `NEEDS_REVIEW` + 法务确认
- [ ] 数据回传: 播放量/完播率/互动率/转化率

## References
- `wiki/public-relations/providers/bilibili.md` (to create)
- 花火平台官方文档
- B站商业化合作指引

## What this skill does not do
- ❌ No video production
- ❌ No UP主联系方式导出
- ❌ No guaranteed 播放量
- ❌ No MCP/CLI tools (reference only)
