---
name: sop-ecom-toolkit
description: >-
  跨境电商运营 AI 工具箱总入口（Shopee 巴西站 / Mercado Livre 专精，PT-BR）。
  覆盖 7 条工作流：市场调研、产品策略与定价、Listing 文案、商品图（9 图框架）、
  短视频物料、广告诊断、评论分析，以及"诊断→回改→复测"闭环。
  当用户要"看类目 / 定价 / 写标题 / 写详情页 / 做主图 / 做详情图 / 9 张图 /
  做视频 / 分镜 / 配音字幕 / 广告诊断 / ROAS / ACOS / 差评分析 / 卖点提炼 /
  优化转化"时使用。中文「做图 / 做视频 / 看类目 / 算价格 / 分析评论」同样触发。
  NOT for 账号操作、刷单测评等平台禁止行为、纯 Excel 透视。
allowed-tools:
  - Bash(python *)
  - Read
  - Write
metadata:
  version: 0.4.0
  category: e-commerce/operations
  license: MIT
---

# AI Cross Border Ecommerce Agent Toolkit（总入口）

本文件夹是**伞形 Skill**：先按下面的路由表判断用户要做哪件事，
**再打开对应子模块的 SKILL.md 严格照做**——子模块里有各自的规则卡、
算术脚本与底线约束，本文件只负责路由，不替代子模块的细节。

## 全局三条底线（任何子模块都继承）

1. **不编数据** —— 输入缺字段报 `[INPUT_MISSING]` 并列出可用列，不许猜；
   指标一律跑 `scripts/` 下的脚本，Agent 不心算
2. **合规优先** —— 刷单/诱导评价/虚假宣传/恶意举报等平台禁止行为不做
   （见 `docs/03_Compliance_Guard.md`、`docs/05_SOP_Gap_Register.md`）
3. **买家可见文本 = 目标市场母语（PT-BR）**，内部备注用中文；
   所有数字必须溯源到 `spec_table`

## 路由表

| 用户要做的事 | 打开哪个子模块 |
|---|---|
| 看类目 / 市场容量 / 集中度 / 价格带 / 配置机会 | [Agents/01_Market_Research_Agent/SKILL.md](Agents/01_Market_Research_Agent/SKILL.md) |
| 定价 / SKU 结构 / 优惠券额度 / 目标毛利反算 | [Agents/02_Product_Strategy_Agent/SKILL.md](Agents/02_Product_Strategy_Agent/SKILL.md) |
| 标题 / 详情页 / 卖点提炼 / 关键词分类 / 合规扫描 | [Agents/03_Listing_Creative_Agent/SKILL.md](Agents/03_Listing_Creative_Agent/SKILL.md) |
| 主图 / 白底图 / 场景图 / 9 张图 / 图合规检查 | [Agents/04_Product_Image_Agent/SKILL.md](Agents/04_Product_Image_Agent/SKILL.md) |
| 视频 / 分镜 / AI 视频 Prompt / 配音 / 字幕 | [Agents/05_Product_Video_Agent/SKILL.md](Agents/05_Product_Video_Agent/SKILL.md) |
| 广告诊断 / ROAS / 盈亏线 / 预算动作 | [Agents/06_Advertising_Optimization_Agent/SKILL.md](Agents/06_Advertising_Optimization_Agent/SKILL.md) |
| 差评归因 / 评论统计 / 卖点排行 / 修补文案 | [Agents/07_Review_Analysis_Agent/SKILL.md](Agents/07_Review_Analysis_Agent/SKILL.md) |

**跨模块闭环**（用户在做完整运营时提醒他这条链路）：

```text
01 前置调研 → 02 定策略 → 03 写 Listing → 04 图 + 05 视频 → 上架
→ 06 广告诊断 + 07 评论分析 → 回流 03/04（iterate：只改症状指向的部分）→ 复测
```

闭环纪律：**一次只改一个病因；不属于症状的环节不动；未达标不 加码同一动作，回诊断重新定位。**

## 通用执行顺序

```text
1. 读路由表 → 打开子模块 SKILL.md
2. 按子模块的「最小输入」向用户要数据（导出 CSV / 产品照 / 参数表）
3. 跑子模块 scripts/ 下的脚本出确定性数字（命令都在子 SKILL.md 的速查表里）
4. 按 prompts/ 的规则产出内容
5. 有校验脚本的必须过校验，不过不交付
6. 涉及上架的提醒用户：平台规则为编写时公开值，发布前到卖家中心复核；
   定价模型未含巴西税费，使用前自行补税率
```

## 已知限制

- **不代执行**：不操作卖家后台、不代改价改预算（动作清单交人审批）
- **数据采集不在内**：类目/广告/评论导出由使用者提供
- **渲染不在内**：图与视频由生图模型/剪辑工具产出，本工具箱出规划与 Prompt
- 不做平台禁止的任何动作；请求涉及时拒绝并给合规替代

---

**文档**：[README](README.md) · [架构拆解](docs/00_Architecture_SOP_to_Agent.md) ·
[合规红线](docs/03_Compliance_Guard.md) · [路线图](ROADMAP.md)
