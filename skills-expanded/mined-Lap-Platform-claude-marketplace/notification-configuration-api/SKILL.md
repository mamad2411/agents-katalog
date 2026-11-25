---
name: notification-configuration-api
description: "Notification Configuration API skill. Use when working with Notification Configuration for createNotificationConfiguration, deleteNotificationConfigurations, getNotificationConfiguration. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Notification Configuration API
API version: 6

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://cal-test.adyen.com/cal/services/Notification/v6

## Setup
1. Set Authorization header with your Bearer token
3. POST /createNotificationConfiguration -- create first createNotificationConfiguration

## Endpoints

6 endpoints across 6 groups. See references/api-spec.lap for full details.

### createNotificationConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /createNotificationConfiguration | Subscribe to notifications |

### deleteNotificationConfigurations
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteNotificationConfigurations | Delete a notification subscription configuration |

### getNotificationConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /getNotificationConfiguration | Get a notification subscription configuration |

### getNotificationConfigurationList
| Method | Path | Description |
|--------|------|-------------|
| POST | /getNotificationConfigurationList | Get a list of notification subscription configurations |

### testNotificationConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /testNotificationConfiguration | Test a notification configuration |

### updateNotificationConfiguration
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateNotificationConfiguration | Update a notification subscription configuration |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a createNotificationConfiguration?" -> POST /createNotificationConfiguration
- "Create a deleteNotificationConfiguration?" -> POST /deleteNotificationConfigurations
- "Create a getNotificationConfiguration?" -> POST /getNotificationConfiguration
- "Create a getNotificationConfigurationList?" -> POST /getNotificationConfigurationList
- "Create a testNotificationConfiguration?" -> POST /testNotificationConfiguration
- "Create a updateNotificationConfiguration?" -> POST /updateNotificationConfiguration
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
