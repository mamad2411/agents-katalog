---
name: azure-activity-log-alerts-api
description: "Azure Activity Log Alerts API skill. Use when working with Azure Activity Log Alerts for subscriptions. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure Activity Log Alerts API
API version: 2017-04-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/microsoft.insights/activityLogAlerts -- verify access

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/activityLogAlerts/{activityLogAlertName} | Create a new activity log alert or update an existing one. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/activityLogAlerts/{activityLogAlertName} | Get an activity log alert. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/activityLogAlerts/{activityLogAlertName} | Delete an activity log alert. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/activityLogAlerts/{activityLogAlertName} | Updates an existing ActivityLogAlertResource's tags. To update other fields use the CreateOrUpdate method. |
| GET | /subscriptions/{subscriptionId}/providers/microsoft.insights/activityLogAlerts | Get a list of all activity log alerts in a subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/activityLogAlerts | Get a list of all activity log alerts in a resource group. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a activityLogAlert?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/activityLogAlerts/{activityLogAlertName}
- "Get activityLogAlert details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/activityLogAlerts/{activityLogAlertName}
- "Delete a activityLogAlert?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/activityLogAlerts/{activityLogAlertName}
- "Partially update a activityLogAlert?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/activityLogAlerts/{activityLogAlertName}
- "List all activityLogAlerts?" -> GET /subscriptions/{subscriptionId}/providers/microsoft.insights/activityLogAlerts
- "List all activityLogAlerts?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.insights/activityLogAlerts
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
