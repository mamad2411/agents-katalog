---
name: cxone-routing
description: Manage and interact with NICE CXone Admin APIs for Contact Center routing, skills, and campaigns.
---

# NICE CXone Routing Skill

This skill provides guidelines and patterns for working with the NICE CXone Admin API to manage routing configurations, skills, and campaigns.

## Key Concepts

- **Skills**: Configurations for specific channels (inbound phone, chat, email) that determine how contacts are routed to agents based on abilities and knowledge.
- **Campaigns**: Organizational groupings used primarily for reporting purposes. Every skill must be assigned to a campaign.
- **Routing**: Supported strategies include static or dynamic delivery, which can be influenced via Studio scripts and API configurations.

## Authentication
All API requests require a valid access token retrieved via OAuth2, Access Key, or OpenID Connect using the Authentication API.

## Admin API Endpoints for Routing
- **Skill Management**: Use the Admin API to create, update, or modify skill assignments for agents. 
- **Campaign Management**: Use endpoints to group skills and manage campaign-level settings.

## Best Practices
- Ensure your API application has the necessary security profile permissions in CXone Central to access Admin-level functions.
- Check the "Restrict Data" tab in the system configuration, as campaign and team data settings may limit the information returned by API responses.
- Responses are limited to 32 KB per request. Use pagination where applicable.
- Always inject a `CorrelationId` in your API headers for tracking and troubleshooting.
