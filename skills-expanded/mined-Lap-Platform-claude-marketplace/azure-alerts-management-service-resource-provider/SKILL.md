---
name: azure-alerts-management-service-resource-provider
description: "Azure Alerts Management Service Resource Provider API skill. Use when working with Azure Alerts Management Service Resource Provider for subscriptions. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure Alerts Management Service Resource Provider
API version: 2019-06-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/microsoft.alertsManagement/smartDetectorAlertRules -- verify access

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/microsoft.alertsManagement/smartDetectorAlertRules | List all the existing Smart Detector alert rules within the subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.alertsManagement/smartDetectorAlertRules | List all the existing Smart Detector alert rules within the subscription and resource group. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.alertsManagement/smartDetectorAlertRules/{alertRuleName} | Get a specific Smart Detector alert rule. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.alertsManagement/smartDetectorAlertRules/{alertRuleName} | Create or update a Smart Detector alert rule. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.alertsManagement/smartDetectorAlertRules/{alertRuleName} | Patch a specific Smart Detector alert rule. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.alertsManagement/smartDetectorAlertRules/{alertRuleName} | Delete an existing Smart Detector alert rule. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all smartDetectorAlertRules?" -> GET /subscriptions/{subscriptionId}/providers/microsoft.alertsManagement/smartDetectorAlertRules
- "List all smartDetectorAlertRules?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.alertsManagement/smartDetectorAlertRules
- "Get smartDetectorAlertRule details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.alertsManagement/smartDetectorAlertRules/{alertRuleName}
- "Update a smartDetectorAlertRule?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.alertsManagement/smartDetectorAlertRules/{alertRuleName}
- "Partially update a smartDetectorAlertRule?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.alertsManagement/smartDetectorAlertRules/{alertRuleName}
- "Delete a smartDetectorAlertRule?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/microsoft.alertsManagement/smartDetectorAlertRules/{alertRuleName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
