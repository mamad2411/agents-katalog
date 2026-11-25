---
name: service-quotas
description: "Service Quotas API skill. Use when working with Service Quotas for root. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# Service Quotas
API version: 2019-06-24

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

19 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Associates your quota request template with your organization. When a new Amazon Web Services account is created in your organization, the quota increase requests in the template are automatically applied to the account. You can add a quota increase request for any adjustable quota to your template. |
| POST | / | Deletes the quota increase request for the specified quota from your quota request template. |
| POST | / | Disables your quota request template. After a template is disabled, the quota increase requests in the template are not applied to new Amazon Web Services accounts in your organization. Disabling a quota request template does not apply its quota increase requests. |
| POST | / | Retrieves the default value for the specified quota. The default value does not reflect any quota increases. |
| POST | / | Retrieves the status of the association for the quota request template. |
| POST | / | Retrieves information about the specified quota increase request. |
| POST | / | Retrieves the applied quota value for the specified quota. For some quotas, only the default values are available. If the applied quota value is not available for a quota, the quota is not retrieved. |
| POST | / | Retrieves information about the specified quota increase request in your quota request template. |
| POST | / | Lists the default values for the quotas for the specified Amazon Web Service. A default value does not reflect any quota increases. |
| POST | / | Retrieves the quota increase requests for the specified Amazon Web Service. |
| POST | / | Retrieves the quota increase requests for the specified quota. |
| POST | / | Lists the quota increase requests in the specified quota request template. |
| POST | / | Lists the applied quota values for the specified Amazon Web Service. For some quotas, only the default values are available. If the applied quota value is not available for a quota, the quota is not retrieved. |
| POST | / | Lists the names and codes for the Amazon Web Services integrated with Service Quotas. |
| POST | / | Returns a list of the tags assigned to the specified applied quota. |
| POST | / | Adds a quota increase request to your quota request template. |
| POST | / | Submits a quota increase request for the specified quota. |
| POST | / | Adds tags to the specified applied quota. You can include one or more tags to add to the quota. |
| POST | / | Removes tags from the specified applied quota. You can specify one or more tags to remove. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
