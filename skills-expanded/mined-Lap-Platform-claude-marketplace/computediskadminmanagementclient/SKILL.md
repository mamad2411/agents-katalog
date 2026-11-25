---
name: computediskadminmanagementclient
description: "ComputeDiskAdminManagementClient API skill. Use when working with ComputeDiskAdminManagementClient for subscriptions. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# ComputeDiskAdminManagementClient
API version: 2018-07-30-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/disks -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/disks | Returns a list of disks. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/disks/{DiskId} | Returns the disk. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all disks?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/disks
- "Get disk details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/disks/{DiskId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
