---
name: single-sign-on-overview
description: "Single Sign-On Overview API skill. Use when working with Single Sign-On Overview for resources. Covers 29 endpoints."
version: 1.0.0
generator: lapsh
---

# Single Sign-On Overview

## Auth
Bearer bearer

## Base URL
https://api.frontegg.com/team

## Setup
1. Set Authorization header with your Bearer token
2. GET /resources/sso/v1/saml/configurations/vendor-config -- verify access
3. POST /resources/sso/v1/configurations -- create first configurations

## Endpoints

29 endpoints across 1 groups. See references/api-spec.lap for full details.

### resources
| Method | Path | Description |
|--------|------|-------------|
| GET | /resources/sso/v1/saml/configurations/vendor-config | Get vendor's SAML config |
| GET | /resources/sso/v1/saml/configurations/sp-certificate | Get service provider certificate |
| GET | /resources/sso/v1/saml/configurations/sp-metadata | Get service provider metadata |
| POST | /resources/sso/v1/configurations | Create SSO configuration |
| GET | /resources/sso/v1/configurations | Get SSO configurations |
| DELETE | /resources/sso/v1/configurations/{configurationId} | Delete SSO configuration |
| PATCH | /resources/sso/v1/configurations/{configurationId} | Update SSO configuration |
| POST | /resources/sso/v1/configurations/metadata | Create SSO configuration using metadata |
| PUT | /resources/sso/v1/configurations/{configurationId}/metadata | Update SSO configuration using metadata |
| POST | /resources/sso/v1/configurations/{configurationId}/domains | Create SSO domain |
| DELETE | /resources/sso/v1/configurations/{configurationId}/domains/{domainId} | Delete SSO domain |
| PUT | /resources/sso/v1/configurations/{configurationId}/domains/{domainId}/validate/email | Validate SSO domain by email |
| PUT | /resources/sso/v2/configurations/{configurationId}/domains/{domainId}/validate | Validate SSO domain |
| PUT | /resources/sso/v1/configurations/{configurationId}/roles | Set SSO default roles |
| GET | /resources/sso/v1/configurations/{configurationId}/roles | Get SSO default roles |
| POST | /resources/sso/v1/configurations/{configurationId}/groups | Create an SSO group |
| GET | /resources/sso/v1/configurations/{configurationId}/groups | Get SSO group |
| PATCH | /resources/sso/v1/configurations/{configurationId}/groups/{groupId} | Update SSO group |
| DELETE | /resources/sso/v1/configurations/{configurationId}/groups/{groupId} | Delete SSO group |
| POST | /resources/sso/v1/configurations/excluded-emails | Exclude email from SSO |
| GET | /resources/sso/v1/configurations/excluded-emails | Get SSO excluded emails |
| DELETE | /resources/sso/v1/configurations/excluded-emails/{email} | Delete SSO excluded email |
| PUT | /resources/sso/v1/configurations/domains/{domain}/force-validate | Vendor only - Force SSO domain validation |
| GET | /resources/sso/v1/configurations/multiple-sso-per-domain | Get SSO per account (tenant) configuration |
| PUT | /resources/sso/v1/configurations/multiple-sso-per-domain | Create or update SSO per account (tenant) configuration |
| PUT | /resources/sso/v1/configurations/domains | Create or update SSO domains configuration |
| GET | /resources/sso/v1/configurations/domains | Get SSO domains configuration |
| GET | /resources/sso/v1/oidc/configurations | Get OIDC configuration |
| POST | /resources/sso/v1/oidc/configurations | Configure OIDC |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all vendor-config?" -> GET /resources/sso/v1/saml/configurations/vendor-config
- "List all sp-certificate?" -> GET /resources/sso/v1/saml/configurations/sp-certificate
- "List all sp-metadata?" -> GET /resources/sso/v1/saml/configurations/sp-metadata
- "Create a configuration?" -> POST /resources/sso/v1/configurations
- "List all configurations?" -> GET /resources/sso/v1/configurations
- "Delete a configuration?" -> DELETE /resources/sso/v1/configurations/{configurationId}
- "Partially update a configuration?" -> PATCH /resources/sso/v1/configurations/{configurationId}
- "Create a metadata?" -> POST /resources/sso/v1/configurations/metadata
- "Create a domain?" -> POST /resources/sso/v1/configurations/{configurationId}/domains
- "Delete a domain?" -> DELETE /resources/sso/v1/configurations/{configurationId}/domains/{domainId}
- "List all roles?" -> GET /resources/sso/v1/configurations/{configurationId}/roles
- "Create a group?" -> POST /resources/sso/v1/configurations/{configurationId}/groups
- "List all groups?" -> GET /resources/sso/v1/configurations/{configurationId}/groups
- "Partially update a group?" -> PATCH /resources/sso/v1/configurations/{configurationId}/groups/{groupId}
- "Delete a group?" -> DELETE /resources/sso/v1/configurations/{configurationId}/groups/{groupId}
- "Create a excluded-email?" -> POST /resources/sso/v1/configurations/excluded-emails
- "List all excluded-emails?" -> GET /resources/sso/v1/configurations/excluded-emails
- "Delete a excluded-email?" -> DELETE /resources/sso/v1/configurations/excluded-emails/{email}
- "List all multiple-sso-per-domain?" -> GET /resources/sso/v1/configurations/multiple-sso-per-domain
- "List all domains?" -> GET /resources/sso/v1/configurations/domains
- "List all configurations?" -> GET /resources/sso/v1/oidc/configurations
- "Create a configuration?" -> POST /resources/sso/v1/oidc/configurations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
