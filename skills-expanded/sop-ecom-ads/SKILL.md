---
name: sop-ecom-ads
description: >-
  跨境电商广告决策层 Skill，Shopee 巴西与 Mercado Livre 专精。读广告导出报表 →
  像素级算术（盈亏线 ROAS / 可承受 CPC / 净贡献，含巴西税费）→ P0/P1/P2 分级动作清单。
  只建议，不执行 —— 不改后台、不自动调价。当用户要诊断广告、看 ROAS/ACOS、
  降预算降出价、广告亏钱分析、大促复盘时使用。中文「广告诊断 / 广告亏钱 / 预算怎么调」同样触发。
  NOT for 自动调价机器人、直接写平台后台、视频广告创意制作。
allowed-tools:
  - Bash(python *)
  - Read
  - Write
metadata:
  version: 0.4.0
  category: e-commerce/advertising-optimization
  license: MIT
---

# 06 · Advertising Optimization Skill（决策层）

> **定位**：广告的**决策层**，不是机器人。坐在你的数据源（平台广告报表导出）之上，
> 产出「改什么、改成多少、依据是什么」的动作清单。**执行由人决定。**

---

## 三条底线

1. **不执行** —— 本 Skill 永远不直接改后台预算/出价，动作清单给人审批
2. **不猜数字** —— 所有指标由 `scripts/ad_metrics.py` 计算，Agent 只解读；怀疑数字 → `[METRIC_SUSPECT]`
3. **不暂停广告** —— 止血手段是降预算降出价；暂停破坏连续性降权重（见 [actions.md](references/actions.md) 铁律）

---

## 快速开始（两条命令）

```bash
# 1) 算盈亏线与可承受 CPC —— 平台预设（与 02 共用 platform_fees.json，含价格分档固定费）
python scripts/ad_metrics.py calc --platform shopee_br --price 113.40 --product-cost 55 \
    --target-acos 25 --cvr 0.44

#    或手工口径（显式参数优先）
python scripts/ad_metrics.py calc --price 113.40 --product-cost 55 \
    --commission 14 --return 2 --tax 0 --target-acos 25 --cvr 0.44

# 2) 读广告导出报表 → 全量诊断 + P0/P1/P2 分级动作
python scripts/ad_metrics.py diagnose --file examples/sample-ad-report.csv \
    --price 113.40 --product-cost 55 --commission 14 --return 2 --tax 0 --target-acos 25
```

`--tax` 是**综合有效税率**（巴西 ICMS/PIS/COFINS/Simples Nacional 折算成占售价百分比）。
税率 8% 时盈亏线 ROAS 从 2.82 抬到 3.64 —— **不含税的盈亏线是骗人的**。

---

## 工作流

```text
① calc   成本结构 → 盈亏线 ACoS/ROAS、可承受 CPC
② diagnose  广告导出 CSV → 逐组漏斗指标 + 分级
③ 读分级 → 翻对应手册（references/playbooks.md）
④ 产出动作清单（含「本轮明确不动」清单）
⑤ 人审批 → 执行 → 3–7 天后复测
```

---

## 诊断顺序（固定，不可跳步）

```text
第0层 数据充分性（曝光<1,000 → 不动） → 第1层 无花费 → 第2层 CTR<2%（回流04）
→ 第3层 点击≥30零订单（回流03，广告端止血） → 第4层 ROAS 分级：
   < 0.5×盈亏线 = P0 止血 ｜ < 盈亏线 = P1 改善 ｜ < 目标 = P1 维持 ｜ ≥ 目标 = P2 放量
```

完整规则表见 [references/diagnosis.md](references/diagnosis.md)；
公式与列名映射见 [references/metrics.md](references/metrics.md)；
8 个场景手册见 [references/playbooks.md](references/playbooks.md)；
动作库（条件/幅度/频率/回滚 + Shopee 预算节律与"不要暂停"铁律）见
[references/actions.md](references/actions.md)。

---

## Shopee BR 特别约束（自动化必知）

| 规则 | 内容 |
|---|---|
| 预算节律 | 北京 11:00 → 休眠 R$10；北京 23:30 → 恢复激活值 |
| 已花费只可上调 | 当天已有花费，预算**不能下调**（等次日归零） |
| 二次确认弹窗 | 点确认后还有「修改前请确认 → 继续修改」 |

---

## 已知限制

| 限制 | 说明 |
|---|---|
| **不执行** | 动作清单给人审批；写后台属路线 B，未实现 |
| 搜索词报告未接 | 搜索词/否定词分析需平台导出（sqp 框架待补，见 ROADMAP） |
| 阈值为巴西站经验值 | CTR 3–5% 等基准来自 SOP 与实战，不同类目需校准 |
| 税率为简化口径 | 综合有效税率一个参数，不代表真实税制明细 |
| 无公开 API 平台 | Shopee 卖家侧无广告 API → 数据靠手动导出或浏览器自动化 |
