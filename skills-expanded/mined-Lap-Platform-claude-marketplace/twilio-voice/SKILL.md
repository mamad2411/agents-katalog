---
name: twilio-voice
description: "Twilio - Voice API skill. Use when working with Twilio - Voice for Archives, ByocTrunks, ConnectionPolicies. Covers 32 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio - Voice
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://voice.twilio.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/ByocTrunks -- verify access
3. POST /v1/ByocTrunks -- create first ByocTrunks

## Endpoints

32 endpoints across 7 groups. See references/api-spec.lap for full details.

### Archives
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v1/Archives/{Date}/Calls/{Sid} | Delete an archived call record from Bulk Export. Note: this does not also delete the record from the Voice API. |

### ByocTrunks
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/ByocTrunks |  |
| GET | /v1/ByocTrunks |  |
| GET | /v1/ByocTrunks/{Sid} |  |
| POST | /v1/ByocTrunks/{Sid} |  |
| DELETE | /v1/ByocTrunks/{Sid} |  |

### ConnectionPolicies
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/ConnectionPolicies |  |
| GET | /v1/ConnectionPolicies |  |
| GET | /v1/ConnectionPolicies/{Sid} |  |
| POST | /v1/ConnectionPolicies/{Sid} |  |
| DELETE | /v1/ConnectionPolicies/{Sid} |  |
| POST | /v1/ConnectionPolicies/{ConnectionPolicySid}/Targets |  |
| GET | /v1/ConnectionPolicies/{ConnectionPolicySid}/Targets |  |
| GET | /v1/ConnectionPolicies/{ConnectionPolicySid}/Targets/{Sid} |  |
| POST | /v1/ConnectionPolicies/{ConnectionPolicySid}/Targets/{Sid} |  |
| DELETE | /v1/ConnectionPolicies/{ConnectionPolicySid}/Targets/{Sid} |  |

### DialingPermissions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/DialingPermissions/Countries/{IsoCode} | Retrieve voice dialing country permissions identified by the given ISO country code |
| GET | /v1/DialingPermissions/Countries | Retrieve all voice dialing country permissions for this account |
| POST | /v1/DialingPermissions/BulkCountryUpdates | Create a bulk update request to change voice dialing country permissions of one or more countries identified by the corresponding [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) |
| GET | /v1/DialingPermissions/Countries/{IsoCode}/HighRiskSpecialPrefixes | Fetch the high-risk special services prefixes from the country resource corresponding to the [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) |

### Settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/Settings | Retrieve voice dialing permissions inheritance for the sub-account |
| POST | /v1/Settings | Update voice dialing permissions inheritance for the sub-account |

### IpRecords
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/IpRecords |  |
| GET | /v1/IpRecords |  |
| GET | /v1/IpRecords/{Sid} |  |
| POST | /v1/IpRecords/{Sid} |  |
| DELETE | /v1/IpRecords/{Sid} |  |

### SourceIpMappings
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/SourceIpMappings |  |
| GET | /v1/SourceIpMappings |  |
| GET | /v1/SourceIpMappings/{Sid} |  |
| POST | /v1/SourceIpMappings/{Sid} |  |
| DELETE | /v1/SourceIpMappings/{Sid} |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a Call?" -> DELETE /v1/Archives/{Date}/Calls/{Sid}
- "Create a ByocTrunk?" -> POST /v1/ByocTrunks
- "List all ByocTrunks?" -> GET /v1/ByocTrunks
- "Get ByocTrunk details?" -> GET /v1/ByocTrunks/{Sid}
- "Delete a ByocTrunk?" -> DELETE /v1/ByocTrunks/{Sid}
- "Create a ConnectionPolicy?" -> POST /v1/ConnectionPolicies
- "List all ConnectionPolicies?" -> GET /v1/ConnectionPolicies
- "Get ConnectionPolicy details?" -> GET /v1/ConnectionPolicies/{Sid}
- "Delete a ConnectionPolicy?" -> DELETE /v1/ConnectionPolicies/{Sid}
- "Create a Target?" -> POST /v1/ConnectionPolicies/{ConnectionPolicySid}/Targets
- "List all Targets?" -> GET /v1/ConnectionPolicies/{ConnectionPolicySid}/Targets
- "Get Target details?" -> GET /v1/ConnectionPolicies/{ConnectionPolicySid}/Targets/{Sid}
- "Delete a Target?" -> DELETE /v1/ConnectionPolicies/{ConnectionPolicySid}/Targets/{Sid}
- "Get Country details?" -> GET /v1/DialingPermissions/Countries/{IsoCode}
- "List all Countries?" -> GET /v1/DialingPermissions/Countries
- "Create a BulkCountryUpdate?" -> POST /v1/DialingPermissions/BulkCountryUpdates
- "List all HighRiskSpecialPrefixes?" -> GET /v1/DialingPermissions/Countries/{IsoCode}/HighRiskSpecialPrefixes
- "List all Settings?" -> GET /v1/Settings
- "Create a Setting?" -> POST /v1/Settings
- "Create a IpRecord?" -> POST /v1/IpRecords
- "List all IpRecords?" -> GET /v1/IpRecords
- "Get IpRecord details?" -> GET /v1/IpRecords/{Sid}
- "Delete a IpRecord?" -> DELETE /v1/IpRecords/{Sid}
- "Create a SourceIpMapping?" -> POST /v1/SourceIpMappings
- "List all SourceIpMappings?" -> GET /v1/SourceIpMappings
- "Get SourceIpMapping details?" -> GET /v1/SourceIpMappings/{Sid}
- "Delete a SourceIpMapping?" -> DELETE /v1/SourceIpMappings/{Sid}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
