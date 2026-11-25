---
name: evenrealities-tracker
description: Automate Evenrealities order monitoring (daily checks, status history, change-only alerts). Uses fast-browser-use to fill the tracker form, compare statuses, and notify Telegram only when something changes, while logging everything into `memory/evenrealities-status-history.json`.
---

# Evenrealities Order Tracker

## Summary

- **Automatic monitoring**: checks each saved order every morning at 9 AM using `memory/evenrealities-orders.json`.
- **Signal-only alerts**: Telegram notifications are sent only when an order’s status changed since the last run.
- **Persistent history**: every order keeps the last known status plus timestamp so you can spot regressions.
- **Scriptable CLI**: `python3 scripts/tracker.py [--check|--config|--history]` lets you run the tracker or inspect config/history on demand.

The script quietly polls https://track.evenrealities.com, recomputes each order’s status, and only speaks up when there’s a meaningful change.

## Quick Start

### 1. Set Up Orders Configuration

Copy the example file and add your orders:

```bash
cp skills/evenrealities-tracker/references/evenrealities-orders-example.json \
   memory/evenrealities-orders.json
```

Edit `memory/evenrealities-orders.json`:

```json
{
  "orders": [
    {
      "email": "your-email@example.com",
      "order_id": "ORD-123456"
    },
    {
      "email": "another-email@example.com",
      "order_id": "ORD-789012"
    }
  ]
}
```

### 2. Create Daily Cron Job

```bash
clawdbot cron add \
  --name "Evenrealities order check" \
  --schedule "0 9 * * *" \
  --task "python3 /Users/thibautrey/clawd/skills/evenrealities-tracker/scripts/tracker.py --check"
```

That's it! The cron will run every morning at 9 AM.

## How It Works

**Daily Flow (9 AM):**

1. Script loads your orders from `memory/evenrealities-orders.json`
2. For each order, uses browser automation to:
   - Navigate to https://track.evenrealities.com
   - Enter email + order number
   - Click confirm
   - Extract status text
3. Compares status against history
4. **If changed:** Sends Telegram notification
5. **If unchanged:** Silent (no notification)
6. Updates `memory/evenrealities-status-history.json`

## Commands

### Check All Orders Now

```bash
python3 scripts/tracker.py --check
```

Output example:
```
🔍 Checking 2 order(s)...
============================================================

📦 Checking: user@example.com / Order #ORD-123456
   Status: SHIPPED
   (No change)

📦 Checking: other@example.com / Order #ORD-789012
   Status: PROCESSING
   ✨ CHANGED: PENDING → PROCESSING
   
✨ 1 change(s) detected!
   📦 ORD-789012: PENDING → PROCESSING
```

### Show Configuration

```bash
python3 scripts/tracker.py --config
```

### Show Status History

```bash
python3 scripts/tracker.py --history
```

## Configuration Files

### evenrealities-orders.json

Location: `memory/evenrealities-orders.json`

```json
{
  "orders": [
    {
      "email": "email@example.com",
      "order_id": "ORD-123456"
    }
  ]
}
```

**Fields:**
- `email`: Email used for tracking
- `order_id`: Order number (format: ORD-XXXXXX or similar)

Add as many orders as needed.

### evenrealities-status-history.json

Location: `memory/evenrealities-status-history.json` (auto-generated)

```json
{
  "email@example.com:ORD-123456": {
    "email": "email@example.com",
    "order_id": "ORD-123456",
    "status": "SHIPPED",
    "last_checked": "2026-02-02T09:00:00.000Z"
  }
}
```

Updated automatically on each run.

## Notifications

### When You Get Notified

✨ **Status CHANGED** → Telegram message sent

Example notification:
```
📦 Order Update!

Order: ORD-789012
Email: user@example.com
Previous: PENDING
New: PROCESSING
Time: 2026-02-02 09:00 AM
```

### When You DON'T Get Notified

✓ Status unchanged
✓ First check (no previous status to compare)
✓ No orders configured

## Browser Automation (Fast Browser Use)

The skill uses the `fast-browser-use` skill to:

1. Navigate to https://track.evenrealities.com
2. Fill email field
3. Fill order ID field
4. Click confirmation button
5. Wait 1-2 seconds for page response
6. Extract status text from result

No manual intervention needed — fully automated.

## Workflow

**Setup (one-time):**
1. Copy orders example
2. Edit with your orders
3. Create cron job

**Daily (automatic):**
1. 9 AM: Cron triggers
2. Script checks all orders
3. Compares to yesterday's status
4. If changed: You get notified
5. History updated

**Maintenance:**
- Add/remove orders: Edit `memory/evenrealities-orders.json`
- Check manually anytime: `python3 scripts/tracker.py --check`
- Review history: `python3 scripts/tracker.py --history`

## Troubleshooting

### "No orders configured"

Create/edit `memory/evenrealities-orders.json` with at least one order.

### "Failed to fetch status"

- Check that https://track.evenrealities.com is accessible
- Verify email and order ID are correct
- Browser automation might need adjustment if site layout changed

### "No notifications" (but orders exist)

- First run: Always silent (establishes baseline)
- Subsequent runs: Only notified if status changes
- Check history with `--history` to see stored statuses

### Change Cron Time

Edit the cron schedule. Example for 8 AM instead of 9 AM:

```bash
clawdbot cron remove <job-id>
clawdbot cron add \
  --name "Evenrealities order check" \
  --schedule "0 8 * * *" \
  --task "python3 /Users/thibautrey/clawd/skills/evenrealities-tracker/scripts/tracker.py --check"
```

## References

- Evenrealities tracking: https://track.evenrealities.com
- Fast Browser Use skill: Browser automation documentation
- Cron scheduling: Clawdbot cron documentation
