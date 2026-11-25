---
name: google-ads-bidding-budgets
description: Use this skill for managing automated bidding strategies, setting up campaign budgets, and optimizing ad spend in Google Ads.
---

# Google Ads Bidding and Budgets Skill

This skill guides the implementation of bidding strategies and budget management via the Google Ads API.

## Core Responsibilities
- **Budget Management**: Creating and updating shared budgets or campaign-specific budgets (`CampaignBudget`).
- **Bidding Strategies**: Applying automated bidding strategies like Target CPA, Target ROAS, Maximize Conversions, or Maximize Clicks.
- **Bid Adjustments**: Setting device, location, or ad schedule bid modifiers.

## Best Practices
1. **Portfolio vs Standard**: Use portfolio bidding strategies for goals spanning multiple campaigns, and standard strategies for single-campaign goals.
2. **Budget Delivery**: Ensure the budget delivery method (Standard or Accelerated) aligns with the account's goals (Note: Accelerated delivery is deprecated for many campaign types).
3. **Validation**: Validate that the chosen bidding strategy is compatible with the campaign's network settings and conversion tracking setup.
