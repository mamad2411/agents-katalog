---
name: broker-card
description: Listing card preview and auto-publish for C2C platforms. Generates platform-adapted listing cards for user review, then auto-publishes on confirmation. Also handles setting the repricing schedule and price shield before publishing. Use when user is ready to list an item after price research. Trigger: "publish", "list it", "上架", "确认发布".
---

# broker-card: Generate, Review, and Publish Listings

Generates platform-specific listing cards, collects schedule+fuse settings, and auto-publishes on user confirmation.

## Workflow

### Phase 1: Card Generation
For each target platform, generate a formatted listing card:

```
┌─────────────────────────────────────┐
│ 🛍️  闲鱼 Xianyu 上架卡片            │
├─────────────────────────────────────┤
│  📝 标题: [platform-optimized]      │
│  📂 分类: [platform category path]  │
│  💰 价格: ¥XXX                      │
│  📋 描述: [platform-tone adapted]   │
│  🏷️  标签: #tag1 #tag2 #tag3       │
│  ⚠️  成色: Grade X — [detail]      │
└─────────────────────────────────────┘
```

### Phase 2: Schedule + Shield (MANDATORY before publishing)
- **Price shield**: Unbreachable floor price. This MUST be set via `broker-fuse` before publishing. The publish script validates: if no floor is set, publishing is blocked.
- **Repricing interval**: How often to re-check prices (default 7 days)

Explain the trade-off: higher floor = more profit per sale but slower; lower floor = faster liquidity.

### Phase 3: Publish (floor-gated)
- Floor validation: script checks `listing.fuse_price > 0` and `listing.current_price >= listing.fuse_price`. Blocked otherwise.
- User says "发布" or "confirm"
- Script auto-publishes to each platform using stored session
- Each publish event is logged to the audit trail (`audit_logger.log_publish`)
- Each listing URL is saved to state manager
- System scheduler is registered for repricing checks

## Platform Adaptations

| Platform | Tone | Title Limit |
|----------|------|-------------|
| 闲鱼 Xianyu | Casual, authentic, community | 30 chars |
| 转转 Zhuanzhuan | Semi-formal, inspection-report | 40 chars |
| eBay | Professional, keyword-dense | 80 chars |
| Depop | Lifestyle, aesthetic | 60 chars |

## Script

```bash
python3 scripts/publish.py --item-id <id> --action generate  # Generate cards
python3 scripts/publish.py --item-id <id> --action publish   # Publish all
```
