---
name: broker-delist
description: Post-sale cross-platform delisting. Automatically removes listings from all platforms when an item sells. Triggered automatically by the daily scheduler when it detects a sale, or manually when user says "卖了", "sold", "已卖出". No user confirmation needed — detection is sufficient to delist.
---

# broker-delist: Post-Sale Auto-Delisting

Automatically removes listings from all platforms when a sale is detected or reported. No user confirmation required.

## Trigger Paths

### Path A: Scheduler auto-detection
Daily repricing check scans each listing's status on its platform:
- Listing returns 404 → not found → check other platforms
- Listing page shows "sold" marker → confirmed sale
- On any platform detecting sale → auto-delist ALL other platforms

### Path B: User reports sale
User says "卖了" / "sold" → manually triggers delist on all platforms

## What Happens

For each platform where the item was listed:
1. Call platform delete/mark-as-sold API using stored session
2. Remove the listing URL from state
3. Update listing status to "sold" with sold_date
4. Remove the item from the scheduler's active list
5. **Log delist event** to audit trail (`audit_logger.log_delist`)

Finally:
- Notify user with delisting summary
- Clean up: if no more active listings, optionally remove the scheduler job
- All delist actions recorded in `~/.broker/audit.jsonl`

## Script

```bash
python3 scripts/delist.py --item-id <id>     # Delist from all platforms
python3 scripts/delist.py --item-id <id> --check  # Check status only
```
