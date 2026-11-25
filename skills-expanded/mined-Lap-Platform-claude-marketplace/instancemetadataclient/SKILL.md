---
name: instancemetadataclient
description: "InstanceMetadataClient API skill. Use when working with InstanceMetadataClient for instance, attested, identity. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# InstanceMetadataClient
API version: 2019-08-15

## Auth
basic

## Base URL
http://169.254.169.254/metadata

## Setup
1. Configure auth: basic
2. GET /instance -- verify access

## Endpoints

4 endpoints across 3 groups. See references/api-spec.lap for full details.

### instance
| Method | Path | Description |
|--------|------|-------------|
| GET | /instance | Get Instance Metadata for the Virtual Machine. |

### attested
| Method | Path | Description |
|--------|------|-------------|
| GET | /attested/document | Get Attested Data for the Virtual Machine. |

### identity
| Method | Path | Description |
|--------|------|-------------|
| GET | /identity/oauth2/token | Get a Token from Azure AD |
| GET | /identity/info | Get information about AAD Metadata |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all instance?" -> GET /instance
- "List all document?" -> GET /attested/document
- "List all token?" -> GET /identity/oauth2/token
- "List all info?" -> GET /identity/info
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
