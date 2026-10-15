---
name: broker-fuse
description: Price Shield — sets the unbreachable floor price below which the AI will never adjust. The hard-stop risk control for AI-assisted pricing. Use when user wants to set a minimum price, price floor, or risk boundary. Trigger: "set minimum price", "price floor", "底价", "最低价", "I won't sell below", "fuse", "/broker-fuse".
---

# broker-fuse: Price Shield (Global Interceptor)

The hard-stop safety mechanism that gives users confidence to delegate pricing authority to the AI.

**This is a GLOBAL INTERCEPTOR, NOT a sequential step.** Every publish action (`broker-card`) and every auto-repricing action (`broker-schedule`) MUST validate against the floor. It is the gate that all price-mutating operations pass through.

## Core Principle

The user delegates daily price adjustments to the AI, but retains ultimate control via an unbreachable floor. The AI operates within a safe zone; the fuse is absolute.

Every price change — whether initial publish or later auto-repricing — flows through the shield check. If suggested_price < floor_price, the action is BLOCKED and logged to the audit trail. This is the technical implementation of the pricing safety boundary.

## Workflow

1. Present risk profiles for reference:

| Profile | Floor | Effect |
|---------|-------|--------|
| Fast Sale | 55% of recommended | Faster liquidity, less profit |
| Balanced (recommended) | 70% of recommended | Trade speed and profit |
| Profit Protection | 85% of recommended | Wait for right buyer |

2. User sets exact floor price (or accepts a profile suggestion)
3. Validate: floor must be < current listing price
4. Write fuse to listing state
5. Explain what happens:
   - Above floor: AI auto-adjusts without asking
   - Below floor: Repricing pauses, user is notified
   - Scheduler will never cross the floor

## Script

```bash
python3 scripts/fuse.py --item-id <id> --set 200        # Set floor at ¥200
python3 scripts/fuse.py --item-id <id> --auto balanced   # Auto-calculate
python3 scripts/fuse.py --item-id <id> --check 150       # Check if ¥150 breaches
```
