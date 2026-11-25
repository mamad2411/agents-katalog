---
name: azure-data-lake-storage-rest-api
description: "Azure Data Lake Storage REST API skill. Use when working with Azure Data Lake Storage REST for root, {filesystem}. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure Data Lake Storage REST API
API version: 2019-10-31

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET / -- verify access
3. POST /{filesystem}/{path} -- create first resource

## Endpoints

12 endpoints across 2 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | List Filesystems |

### {filesystem}
| Method | Path | Description |
|--------|------|-------------|
| PUT | /{filesystem} | Create Filesystem |
| PATCH | /{filesystem} | Set Filesystem Properties |
| GET | /{filesystem} | List Paths |
| HEAD | /{filesystem} | Get Filesystem Properties. |
| DELETE | /{filesystem} | Delete Filesystem |
| PUT | /{filesystem}/{path} | Create File | Create Directory | Rename File | Rename Directory |
| PATCH | /{filesystem}/{path} | Append Data | Flush Data | Set Properties | Set Access Control |
| POST | /{filesystem}/{path} | Lease Path |
| GET | /{filesystem}/{path} | Read File |
| HEAD | /{filesystem}/{path} | Get Properties | Get Status | Get Access Control List | Check Access |
| DELETE | /{filesystem}/{path} | Delete File | Delete Directory |

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
