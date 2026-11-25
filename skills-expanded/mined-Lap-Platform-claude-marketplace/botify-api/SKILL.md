---
name: botify-api
description: "Botify API skill. Use when working with Botify for analyses, projects. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# Botify API
API version: 1.0.0

## Auth
ApiKey Authorization in header

## Base URL
https://api.botify.com/v1

## Setup
1. Set your API key in the appropriate header
2. GET /analyses/{username}/{project_slug}/{analysis_slug}/crawl_statistics -- verify access
3. POST /analyses/{username}/{project_slug}/{analysis_slug}/urls -- create first urls

## Endpoints

26 endpoints across 2 groups. See references/api-spec.lap for full details.

### analyses
| Method | Path | Description |
|--------|------|-------------|
| GET | /analyses/{username}/{project_slug} | List all analyses for a project |
| GET | /analyses/{username}/{project_slug}/{analysis_slug} | Get an Analysis detail |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/crawl_statistics | Return global statistics for an analysis |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/crawl_statistics/time | Return crawl statistics grouped by time frequency (1 min, 5 mins or 60 min) |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/crawl_statistics/urls/{list_type} | Return a list of 1000 latest URLs crawled (all crawled URLs or only URLS with HTTP errors) |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/features/ganalytics/orphan_urls/{medium}/{source} | List of Orphan URLs |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/features/links/percentiles | Get inlinks percentiles |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/features/pagerank/lost | Lost pagerank |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/features/sitemaps/report | Get global information of the sitemaps found (sitemaps indexes, invalid sitemaps urls, etc |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/features/sitemaps/samples/out_of_config | Sample list of URLs which were found in your sitemaps but outside of the |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/features/sitemaps/samples/sitemap_only | Sample list of URLs which were found in your sitemaps, within the project |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/features/top_domains/domains | Top domains |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/features/top_domains/subdomains | Top subddomains |
| POST | /analyses/{username}/{project_slug}/{analysis_slug}/urls | Executes a query and returns a paginated response |
| POST | /analyses/{username}/{project_slug}/{analysis_slug}/urls/aggs | Query aggregator |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/urls/datamodel | Gets an Analysis datamodel |
| POST | /analyses/{username}/{project_slug}/{analysis_slug}/urls/export | Creates a new UrlExport object and starts a task that will export the results into a csv |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/urls/export | A list of the CSV Exports requests and their current status |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/urls/export/{url_export_id} | Checks the status of an CSVUrlExportJob object |
| POST | /analyses/{username}/{project_slug}/{analysis_slug}/urls/suggested_filters | Return most frequent segments (= suggested patterns in the previous version) |
| GET | /analyses/{username}/{project_slug}/{analysis_slug}/urls/{url} | Gets the detail of an URL for an analysis |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects/{username} | List all active projects for the user |
| POST | /projects/{username}/{project_slug}/features/url_rewriting/rules_validator | Match and replace parts of a URL based on rules passed in POST data |
| GET | /projects/{username}/{project_slug}/filters | List all the project's saved filters (each filter's name, ID and filter value) |
| GET | /projects/{username}/{project_slug}/filters/{identifier} | Retrieves a specific saved filter's name, ID and filter value |
| POST | /projects/{username}/{project_slug}/urls/aggs | Project Query aggregator |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get analysis details?" -> GET /analyses/{username}/{project_slug}
- "Get analysis details?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}
- "List all crawl_statistics?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/crawl_statistics
- "List all time?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/crawl_statistics/time
- "Get url details?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/crawl_statistics/urls/{list_type}
- "Get orphan_url details?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/features/ganalytics/orphan_urls/{medium}/{source}
- "List all percentiles?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/features/links/percentiles
- "List all lost?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/features/pagerank/lost
- "List all report?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/features/sitemaps/report
- "List all out_of_config?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/features/sitemaps/samples/out_of_config
- "List all sitemap_only?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/features/sitemaps/samples/sitemap_only
- "List all domains?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/features/top_domains/domains
- "List all subdomains?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/features/top_domains/subdomains
- "Create a url?" -> POST /analyses/{username}/{project_slug}/{analysis_slug}/urls
- "Create a agg?" -> POST /analyses/{username}/{project_slug}/{analysis_slug}/urls/aggs
- "List all datamodel?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/urls/datamodel
- "Create a export?" -> POST /analyses/{username}/{project_slug}/{analysis_slug}/urls/export
- "List all export?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/urls/export
- "Get export details?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/urls/export/{url_export_id}
- "Create a suggested_filter?" -> POST /analyses/{username}/{project_slug}/{analysis_slug}/urls/suggested_filters
- "Get url details?" -> GET /analyses/{username}/{project_slug}/{analysis_slug}/urls/{url}
- "Get project details?" -> GET /projects/{username}
- "Create a rules_validator?" -> POST /projects/{username}/{project_slug}/features/url_rewriting/rules_validator
- "List all filters?" -> GET /projects/{username}/{project_slug}/filters
- "Get filter details?" -> GET /projects/{username}/{project_slug}/filters/{identifier}
- "Create a agg?" -> POST /projects/{username}/{project_slug}/urls/aggs
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
