---
name: analytics-account-management
description: Retrieves Google Analytics account and property information, as well as Google Ads links.
---

# Google Analytics Account Management Skill

Use this skill when the user asks for information about their Google Analytics accounts, properties, or linked Google Ads accounts.

## Tools to use
You have access to the Google Analytics MCP server which provides the following tools for account management:
- `get_account_summaries`: Retrieves a list of the user's GA accounts and properties.
- `get_property_details`: Returns specific details about a given property ID.
- `list_google_ads_links`: Returns a list of Google Ads accounts linked to a property.

## Instructions
1. When asked about accounts or properties, start by using `get_account_summaries` to find the relevant property IDs.
2. If detailed information for a specific property is needed, use `get_property_details` passing the property ID.
3. If the user asks about Google Ads integration or linked ads accounts, use `list_google_ads_links`.
4. Present the information clearly back to the user, ensuring property IDs are highlighted as they are often needed for running reports.
