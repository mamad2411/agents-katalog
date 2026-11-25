---
name: google-ads
description: Manage Google Ads campaigns - setup, create campaigns, generate reports, and optimize performance
---

# Google Ads Skill

A comprehensive skill for managing Google Ads campaigns via direct API integration.

## Commands

- `/google-ads` - Main router, shows available subcommands
- `/google-ads-setup` - Configure credentials and business settings
- `/google-ads-create` - Create campaigns with keyword research and ad copy
- `/google-ads-report` - Generate performance reports
- `/google-ads-optimize` - Get optimization suggestions

## Architecture

This skill uses **subagent delegation** to preserve context:
- Coordinator commands spawn specialized subagents
- Large datasets written to JSON files
- Main context receives summaries only

## Integration Points

- **Google Ads API**: Direct API calls via `google-ads-api` npm package
- **DataForSEO MCP**: Keyword research and volume data
- **Copywriter Skill**: Ad copy generation with character limits

## Configuration

Each project using this skill needs:
1. `google-ads.config.json` - Business and campaign settings
2. `.env` - Google Ads API credentials

## Safety Features

- All campaigns created PAUSED
- Preview before creation
- Dry-run mode available
- User confirmation required for mutations

## Reference Documentation

See `references/` for:
- `api-guide.md` - Google Ads API patterns
- `campaign-structures.md` - Best practice campaign structures
- `config-schema.md` - Configuration schema documentation
