---
name: bc-data-catalogue-api
description: "BC Data Catalogue API skill. Use when working with BC Data Catalogue for action. Covers 22 endpoints."
version: 1.0.0
generator: lapsh
---

# BC Data Catalogue API
API version: 3.0.1

## Auth
OAuth2 | ApiKey ckan_api_key in header

## Base URL
https://catalogue.data.gov.bc.ca/api/3

## Setup
1. Set your API key in the appropriate header
2. GET /action/tag_list -- verify access

## Endpoints

22 endpoints across 1 groups. See references/api-spec.lap for full details.

### action
| Method | Path | Description |
|--------|------|-------------|
| GET | /action/tag_list | Get a list of tags |
| GET | /action/status_show | Get the site status |
| GET | /action/package_list | Get a list of all packages (datasets) |
| GET | /action/package_search | Find packages (datasets) matching query terms |
| GET | /action/package_show | Get metadata about one specific package (dataset) |
| GET | /action/package_activity_list | Get the activity stream of a package (dataset) |
| GET | /action/package_activity_list_html | Get the activity stream of a package (dataset), HTML format |
| GET | /action/package_autocomplete | Find packages (datasets) matching a query |
| GET | /action/package_relationships_list | Get package (dataset) relationships |
| GET | /action/package_revision_list | Get list of revisions for a package (dataset) |
| GET | /action/organization_activity_list | Get the activity stream of an organization |
| GET | /action/organization_activity_list_html | Get the activity stream of an organization, HTML format |
| GET | /action/organization_follower_count | Get number of followers of an organization |
| GET | /action/organization_follower_list | Get users following an organization |
| GET | /action/organization_list_for_user | Get organizations that a user has a given permission for |
| GET | /action/organization_revision_list | Get organization revisions |
| GET | /action/organization_show | Get details of a specific organization |
| GET | /action/organization_list | Get names of all organizations |
| GET | /action/organization_autocomplete | Get names of organizations that match a query string |
| GET | /action/resource_search | Find resources |
| GET | /action/resource_show | Get metadata for a specific resource |
| GET | /action/related_list | Gets items related to a package (dataset) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all tag_list?" -> GET /action/tag_list
- "List all status_show?" -> GET /action/status_show
- "List all package_list?" -> GET /action/package_list
- "Search package_search?" -> GET /action/package_search
- "List all package_show?" -> GET /action/package_show
- "List all package_activity_list?" -> GET /action/package_activity_list
- "List all package_activity_list_html?" -> GET /action/package_activity_list_html
- "Search package_autocomplete?" -> GET /action/package_autocomplete
- "List all package_relationships_list?" -> GET /action/package_relationships_list
- "List all package_revision_list?" -> GET /action/package_revision_list
- "List all organization_activity_list?" -> GET /action/organization_activity_list
- "List all organization_activity_list_html?" -> GET /action/organization_activity_list_html
- "List all organization_follower_count?" -> GET /action/organization_follower_count
- "List all organization_follower_list?" -> GET /action/organization_follower_list
- "List all organization_list_for_user?" -> GET /action/organization_list_for_user
- "List all organization_revision_list?" -> GET /action/organization_revision_list
- "List all organization_show?" -> GET /action/organization_show
- "List all organization_list?" -> GET /action/organization_list
- "Search organization_autocomplete?" -> GET /action/organization_autocomplete
- "Search resource_search?" -> GET /action/resource_search
- "List all resource_show?" -> GET /action/resource_show
- "List all related_list?" -> GET /action/related_list
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
