---
name: etsi-gs-mec-010-2-part-2-application-lifecycle-rules-and-requirements-management
description: "ETSI GS MEC 010-2 - Part 2: Application lifecycle, rules and requirements management API skill. Use when working with ETSI GS MEC 010-2 - Part 2: Application lifecycle, rules and requirements management for app_packages, subscriptions, user_defined_notification. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# ETSI GS MEC 010-2 - Part 2: Application lifecycle, rules and requirements management
API version: 2.1.1

## Auth
No authentication required.

## Base URL
https://localhost/app_pkgm/v1

## Setup
1. No auth setup needed
2. GET /app_packages -- verify access
3. POST /app_packages -- create first app_packages

## Endpoints

16 endpoints across 4 groups. See references/api-spec.lap for full details.

### app_packages
| Method | Path | Description |
|--------|------|-------------|
| POST | /app_packages | Create a resource for on-boarding an application package to a MEO |
| GET | /app_packages | Queries information relating to on-boarded application packages in the MEO |
| GET | /app_packages/{appPkgId} | Queries the information related to individual application package resources |
| DELETE | /app_packages/{appPkgId} | Deletes an individual application package resources |
| PATCH | /app_packages/{appPkgId} | Updates the operational state of an individual application package resource |
| GET | /app_packages/{appPkgId}/appd | Reads the content of the AppD of on-boarded individual application package resources. |
| GET | /app_packages/{appPkgId}/package_content | Fetch the onboarded application package content identified by appPkgId or appDId. |
| PUT | /app_packages/{appPkgId}/package_content | Uploads the content of application package. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| POST | /subscriptions | Subscribe to notifications about on-boarding an application package |
| GET | /subscriptions | used to retrieve the information of subscriptions to individual application package resource in MEO |
| GET | /subscriptions/{subscriptionId} | Used to represent an individual subscription to notifications about application package changes. |
| DELETE | /subscriptions/{subscriptionId} | Deletes the individual subscription to notifications about application package changes in MEO. |

### user_defined_notification
| Method | Path | Description |
|--------|------|-------------|
| POST | /user_defined_notification | Registers a notification endpoint to notify application package operations |

### onboarded_app_packages
| Method | Path | Description |
|--------|------|-------------|
| GET | /onboarded_app_packages/{appDId}/appd | Reads the content of the AppD of on-boarded individual application package resources. |
| GET | /onboarded_app_packages/{appDId}/package_content | Fetch the onboarded application package content identified by appPkgId or appDId. |
| PUT | /onboarded_app_packages/{appDId}/package_content | Uploads the content of application package. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a app_package?" -> POST /app_packages
- "List all app_packages?" -> GET /app_packages
- "Get app_package details?" -> GET /app_packages/{appPkgId}
- "Delete a app_package?" -> DELETE /app_packages/{appPkgId}
- "Partially update a app_package?" -> PATCH /app_packages/{appPkgId}
- "Create a subscription?" -> POST /subscriptions
- "List all subscriptions?" -> GET /subscriptions
- "Get subscription details?" -> GET /subscriptions/{subscriptionId}
- "Delete a subscription?" -> DELETE /subscriptions/{subscriptionId}
- "Create a user_defined_notification?" -> POST /user_defined_notification
- "List all appd?" -> GET /app_packages/{appPkgId}/appd
- "List all appd?" -> GET /onboarded_app_packages/{appDId}/appd
- "List all package_content?" -> GET /app_packages/{appPkgId}/package_content
- "List all package_content?" -> GET /onboarded_app_packages/{appDId}/package_content

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
