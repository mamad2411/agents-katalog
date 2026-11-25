---
name: google-ads-campaign-management
description: Use this skill when managing Google Ads campaigns, ad groups, and ads. Covers creating, updating, and pausing advertising entities.
---

# Google Ads Campaign Management Skill

This skill provides guidelines for interacting with the Google Ads API to manage advertising campaigns.

## Core Responsibilities
- **Campaign Creation**: Creating new campaigns with appropriate network settings.
- **Ad Groups & Ads**: Managing ad groups, responsive search ads, and display ads.
- **Entity Status**: Pausing, enabling, or removing campaigns and ad groups.

## Best Practices
1. **Mutate Operations**: When creating or updating entities, bundle multiple operations in a single `MutateOperations` request whenever possible to optimize network calls.
2. **Resource Names**: Always use the correct resource name formats (e.g., `customers/{customer_id}/campaigns/{campaign_id}`).
3. **Error Handling**: Implement robust error handling to catch `GoogleAdsException` and parse partial failures.
