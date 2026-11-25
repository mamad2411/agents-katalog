---
name: compliance-api
description: "Compliance API skill. Use when working with Compliance for listing_violation_summary, listing_violation. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Compliance API
API version: 1.4.3

## Auth
OAuth2

## Base URL
https://api.ebay.com{basePath}

## Setup
1. Configure auth: OAuth2
2. GET /listing_violation_summary -- verify access

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### listing_violation_summary
| Method | Path | Description |
|--------|------|-------------|
| GET | /listing_violation_summary | This call returns listing violation counts for a seller. A user can pass in one or more compliance types through the <strong>compliance_type</strong> query parameter. See <a href="/api-docs/sell/compliance/types/com:ComplianceTypeEnum">ComplianceTypeEnum</a> for more information on the supported listing compliance types. Listing violations are returned for multiple marketplaces if the seller sells on multiple eBay marketplaces.<br /><br /> <span class="tablenote"><strong>Note:</strong> Only a canned response, with counts for all listing compliance types, is returned in the Sandbox environment. Due to this limitation, the <strong>compliance_type</strong> query parameter (if used) will not have an effect on the response. </span> |

### listing_violation
| Method | Path | Description |
|--------|------|-------------|
| GET | /listing_violation | This call returns specific listing violations for the supported listing compliance types. Only one compliance type can be passed in per call, and the response will include all the listing violations for this compliance type, and listing violations are grouped together by eBay listing ID. See <a href="/api-docs/sell/compliance/types/com:ComplianceTypeEnum">ComplianceTypeEnum</a> for more information on the supported listing compliance types. This method also has pagination control. <br /><br /> <span class="tablenote"><strong>Note:</strong> A maximum of 2000 listing violations will be returned in a result set. If the seller has more than 2000 listing violations, some/all of those listing violations must be corrected before additional listing violations will be retrieved. The user should pay attention to the <strong>total</strong> value in the response. If this value is '2000', it is possible that the seller has more than 2000 listing violations, but this field maxes out at 2000. </span> <br /><span class="tablenote"><strong>Note:</strong> In a future release of this API, the seller will be able to pass in a specific eBay listing ID as a query parameter to see if this specific listing has any violations. </span><br /> <span class="tablenote"><strong>Note:</strong> Only mocked non-compliant listing data will be returned for this call in the Sandbox environment, and not specific to the seller. However, the user can still use this mock data to experiment with the compliance type filters and pagination control.</span> |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all listing_violation_summary?" -> GET /listing_violation_summary
- "List all listing_violation?" -> GET /listing_violation
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
