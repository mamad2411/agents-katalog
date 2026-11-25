# LinkedIn Sales Navigator API Integration

Search leads and accounts using the LinkedIn Sales Navigator REST API.

## Setup

1. Requires an active LinkedIn Sales Navigator contract
2. Get API token from https://developer.linkedin.com/
3. Set `LINKEDIN_SALES_NAV_TOKEN` in `.env`

## Available Methods

### Search Leads
```bash
python .claude/scripts/outreach/linkedin_sales_navigator.py search \
  --query "CTO" --location "San Francisco" --industry "Technology" --count 10
```

**Filters:** `--title`, `--company`, `--location`, `--industry`, `--seniority`, `--count`

### Get Lead Profile
```bash
python .claude/scripts/outreach/linkedin_sales_navigator.py lead --id "LEAD_ID"
```

### Search Accounts (Companies)
```bash
python .claude/scripts/outreach/linkedin_sales_navigator.py accounts \
  --query "fintech" --industry "Financial Services" --count 10
```

### Get Account Details
```bash
python .claude/scripts/outreach/linkedin_sales_navigator.py account --id "ACCOUNT_ID"
```

### Saved Leads
```bash
python .claude/scripts/outreach/linkedin_sales_navigator.py saved
python .claude/scripts/outreach/linkedin_sales_navigator.py save --id "LEAD_ID"
```

### Check Status
```bash
python .claude/scripts/outreach/linkedin_sales_navigator.py status
```

## Integration with Discovery Engine

Results feed automatically into the discovery engine as `DiscoveredPerson` objects via `parse_sales_navigator_results()`.

## Rate Limits

- Lead searches: 25/day
- Account searches: 25/day
- Lead lookups: 100/day
- Account lookups: 100/day
- Min delay between API calls: 2s

## Fallback

When no API token is configured, the LinkedIn adapter falls back to browser extension automation via WebSocket. Use the `--api` flag in `/linkedin` commands to prefer the API when available.

## Developed by 10x.in
