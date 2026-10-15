---
name: ugc-tracker
description: Track real UGC creator performance — manage creator roster, monitor view counts on their posts (IG/TikTok), calculate base pay + performance bonuses, and report payout summaries. Automates the $15/video + 100K/250K/500K/1M bonus tier system.
---

# UGC Tracker

Manages a roster of real human UGC (user-generated content) creators. Tracks their post view counts via yt-dlp, calculates base pay and performance bonuses, and generates payout reports.

## Quick Start

```bash
# Add a creator and their first post
python3 skills/ugc-tracker/scripts/track.py add "Jane Smith" --handle @janesmith --platform tiktok --post https://tiktok.com/@janesmith/video/123

# Check view counts for all tracked posts
python3 skills/ugc-tracker/scripts/track.py check

# Show payout report
python3 skills/ugc-tracker/scripts/track.py report

# Post report to Slack
python3 skills/ugc-tracker/scripts/track.py report --slack
```

## Commands

| Command | Description |
|---------|-------------|
| `add <name> --handle @username --platform <platform> --post <url>` | Add a creator and a post to track |
| `add <name> --post <url>` | Add another post to an existing creator |
| `remove <name>` | Remove a creator and all their posts |
| `list` | Show all creators and their tracked posts |
| `check` | Scrape view counts for all tracked posts |
| `check <name>` | Check view counts for one creator only |
| `report` | Show full payout summary |
| `report --unpaid` | Show only unpaid amounts |
| `report --slack` | Send report to Slack channel |
| `mark-paid <name>` | Mark all current bonuses for a creator as paid |
| `mark-paid <name> --base` | Also mark base pay as paid |

## Bonus Tier Table

| Views | Bonus |
|-------|-------|
| 100,000 | $25 |
| 250,000 | $50 |
| 500,000 | $100 |
| 1,000,000 | $250 |

Bonuses are cumulative — hitting 1M views triggers all four tiers ($425 total in bonuses + $15 base).

Base pay is $15 per video, regardless of views.

## Data Format

State is stored at `~/.clawdbot/ugc-tracker/creators.json`:

```json
{
  "creators": {
    "creator_id": {
      "name": "Jane Smith",
      "handles": {
        "tiktok": "@janesmith",
        "instagram": "@janesmith.ig"
      },
      "posts": [
        {
          "url": "https://tiktok.com/@janesmith/video/123",
          "platform": "tiktok",
          "added_at": "2026-03-01T00:00:00Z",
          "base_pay": 15.0,
          "base_paid": false,
          "views": 0,
          "last_checked": null,
          "bonuses_paid": [],
          "bonuses_owed": []
        }
      ]
    }
  }
}
```

- `bonuses_paid` — list of threshold keys (e.g. `"100000"`) already paid out
- `bonuses_owed` — list of `{threshold, amount, key}` objects currently owed

## Environment Variables

Loaded from `~/.clawdbot/.env`:

| Variable | Purpose |
|----------|---------|
| `SLACK_BOT_TOKEN` | Post reports to Slack |
| `ANTHROPIC_API_KEY` | Reserved for future AI analysis |

## Cookies

View count scraping uses yt-dlp with platform cookies:
- TikTok: `~/.clawdbot/cookies/tiktok.txt`
- Instagram: `~/.clawdbot/cookies/instagram.txt`

Falls back to unauthenticated scraping if cookies are missing (may have lower success rate for private content).

## Example Report Output

```
UGC Tracker Report — 2026-03-09

Creator          Posts   Base Pay   Bonuses    Total Owed
Jane Smith       3       $45        $75        $120
Mike Jones       1       $15        $0         $15
-----------------------------------------------------
TOTAL            4       $60        $75        $135
```
