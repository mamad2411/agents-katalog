---
name: sop-ecom-pricing
description: >-
  SKU 定价算术 Skill，Shopee 巴西 / Mercado Livre。到岸成本 → 净利率 / 盈亏平衡价 /
  目标价反算 / 价格阶梯 / 优惠券余量（含巴西税费项）。当用户要算毛利、定价、
  盈亏价、该发多少券、SKU 结构是否合理时使用。中文「算毛利 / 定价 / 盈亏价 / 发券」同样触发。
  NOT for 竞品定价调研、市场价格带分析（那是 01 的活）。
allowed-tools:
  - Bash(python *)
  - Read
metadata:
  version: 0.4.0
  category: e-commerce/pricing
  license: MIT
---

# 02 · Product Strategy Skill（定价算术层）

> **定位**：把「到岸成本 + 费率 + 目标毛利」变成**可验算的数字**。
> 定价**决策**由人做，本 Skill 只保证算得准。

---

## 快速开始

```bash
# 平台预设（推荐）：费率来自 scripts/platform_fees.json，含价格分档佣金/固定费
# 可用平台：shopee_br / mercadolivre_br / mercadolivre_br_premium / amazon_br / tiktok_br
python scripts/sku_pricing.py calc --platform shopee_br --cost 935 --price 2199
python scripts/sku_pricing.py --list-platforms          # 查看全部预设与费率来源

# 多 SKU 矩阵 + 价格阶梯 + 券余量（读 CSV）
python scripts/sku_pricing.py matrix --file examples/sample-skus.csv --platform mercadolivre_br

# 手工口径（兼容旧用法，显式参数永远优先于预设）
python scripts/sku_pricing.py calc --cost 935 --price 2199 \
    --commission 14 --return 2 --ad 5 --tax 0 --target-margin 32

# 多 SKU 矩阵：净利率表 + 价格阶梯 + 券余量 + 结构提醒
python scripts/sku_pricing.py matrix --file examples/sample-skus.csv \
    --commission 14 --return 2 --ad 5 --tax 0 --target-margin 32
```

---

## 输出解读（五件事）

| 输出 | 怎么用 |
|---|---|
| `net_rate` 净利率 | 与 `target_margin` 比：低于 = 破目标（引流款可刻意低于，但须在盈亏价之上） |
| `break_even_price` 盈亏平衡价 | **售价底线** —— 促销/券后价跌破它就是真亏 |
| `target_price` 目标价 | 由目标毛利反算的定价参考（成本 ÷ 0.47 这类） |
| `coupon_headroom` 优惠券余量 | 净利率超出目标的部分 × 售价 = **发券不破目标的额度** |
| `price_ladder` 价格阶梯 | 相邻 SKU 价差：差太少互相蚕食，差太大留出空位给竞品 |

---

## 规则与口径

- 公式、税费口径（综合有效税率）、参数说明 → [references/pricing-rules.md](references/pricing-rules.md)
- 案例数据（电动滑板车四 SKU）→ [examples/sample-skus.csv](examples/sample-skus.csv)

## 三条提醒

1. **引流款净利率低于目标是策略不是事故** —— 但脚本会提醒你确认，且它必须高于盈亏平衡价
2. **高配款净利率常常低于主推款**（成本涨得比售价快）—— 脚本会提示检查
3. **税费别漏** —— `--tax 8` 就能把盈亏价抬高近三成，按自己的巴西税制折算填入
