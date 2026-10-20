---
name: publicist-china-douyin
description: Douyin (抖音) commercial ecosystem, 巨量星图 platform, and pitch protocols for mainland China earned media. Use when targeting 抖音 for editorial or commercial placement.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# Douyin (抖音), China market

**Scope**. Only 抖音 commercial/editorial engagement. Pair with `publicist-china`.

## Platform rules (verified)

### Commercial ecosystem: 完全闭环
- **巨量星图**, 官方创作者合作平台 (选品广场 + 投流系统)
- **选品中心**, 带货/接单必须挂载官方链接
- **AI逐帧扫描**, 视频内容+链接分析拦截暗广
- **未报备私单 = 暗广 = 拦截** (流量关停 + 电商权限降级)

### Content classification (强制)
- 所有品牌合作内容必须通过官方邀请链接发布
- 必须包含"付费合作伙伴"标签
- 否则无法获得 For You 推荐流量

### Creator tiers
| Tier | Fans | Typical Use |
|---|---|---|
| 头部达人 | 100万+ | 品牌声量引爆、高客单价转化 |
| 腰部达人 | 10万-100万 | 精准种草、垂类深度测评 |
| 尾部/素人 | <10万 | 口碑铺量、UGC氛围造势 |

## Pitch protocol

### Pre-pitch verification
1. **星图入驻**. Creator must be in 巨量星图
2. **Account health**. 无违规记录、近期商单比例合理、粉丝真实互动率
3. **Category fit**. Vertical match (美妆/3C/家居/母婴/汽车/游戏等)
4. **Content style**. 真实测评 vs 硬广, community prefers authentic

### Contact flow (mandatory)
1. **巨量星图** → 搜索达人 → 发送需求单 → 达人接单 → 平台生成合同
2. **Brief must include**. 核心卖点、必提话术、禁用词(极限词/医疗/金融)、标签要求
3. **Creator produces** → 品牌审核 → 发布 → 数据回传(阅读完成率/点击率/转化率)

### Video content requirements
- **前3秒**. 黄金钩子 (冲突/悬念/利益点/视觉冲击)
- **中段**. 产品演示/对比/专家背书/用户证言
- **尾部**. 明确CTA (挂链接/搜关键词/进直播间)
- **标签**. #广告 #合作 #品牌名 + 话题标签
- **时长**. 种草 30-60s; 深度测评 60-180s; 直播切片 15-30s

### Compliance checklist (per pitch)
- [ ] 巨量星图报备完成 (非私单)
- [ ] 付费合作标签已添加
- [ ] 选品中心挂载商品链接 (带货类)
- [ ] 极限词/违禁词清单提供给达人
- [ ] AI生成片段 → 显性+隐性标识
- [ ] 医疗/金融/功能性产品 → `NEEDS_REVIEW` + 法务确认
- [ ] 数据监测: 阅读完成率/点击率/转化率 回传确认

## References
- `wiki/public-relations/providers/douyin.md` (to create)
- 巨量星图官方文档
- PANews "暗广时代终结", 抖音商业体系最完整
- 2025 抖音电商生态白皮书

## What this skill does not do
- ❌ No video production
- ❌ No creator contact export
- ❌ No guaranteed viral/GMV
- ❌ No MCP/CLI tools (reference only)
