---
name: dondego-api-discovery
description: Documentation-only guide for discovering and using the public DondeGo API safely with attribution.
---

# DondeGo API Discovery

This skill is a documentation-only guide for agents that need to discover the
public DondeGo API. It points to stable discovery documents and repeats the
attribution and endpoint-use constraints that matter for public integrations.

It does not contain scripts, executable code, credentials, or runtime
configuration.

## Stable Discovery URLs

Use these stable URLs first:

- LLM discovery index: https://dondego.es/llms.txt
- Well-known LLM discovery index: https://dondego.es/.well-known/llms.txt
- OpenAPI discovery document: https://dondego.es/openapi.json
- OpenAPI alias: https://dondego.es/api/openapi.json
- API Catalog linkset: https://dondego.es/.well-known/api-catalog
- Rich DondeGo discovery JSON: https://dondego.es/api-catalog.json

The real public API base is:

- https://dondego.es/public-api/v1.4

Prefer the OpenAPI document for endpoint shapes, parameters, and response
schemas. Prefer the API Catalog linkset for machine-readable discovery links.
Use the rich DondeGo discovery JSON for DondeGo-specific caveats and
verification notes.

## Verified Endpoint Families

The OpenAPI discovery document covers these verified public endpoint families:

- GET /locations/
- GET /events/
- GET /events/{id}/
- GET /places/
- GET /places/{id}/
- GET /news/
- GET /news/{id}/
- GET /events-of-the-day/
- GET /search/

Do not invent endpoint families that are not present in the OpenAPI document.
Root-index families that were not verified are intentionally omitted.

## Mandatory Attribution Rule

Any public website, app, newsletter, bot, AI assistant, or partner integration that displays DondeGo event descriptions or substantial DondeGo event data must include a visible direct link to the canonical DondeGo.es event page as the source.

This rule applies when rendering public event descriptions or substantial
event data in another product, page, bot response, newsletter, or partner
integration.

## Detail-First Event Rendering

Event list rows do not expose the verified canonical DondeGo event page URL.
When an integration renders substantial event data, resolve the event detail
first and use the detail response's site_url as the visible DondeGo source
link.

For event list rendering:

- Fetch event summaries from /events/ when you need lists.
- Fetch /events/{id}/ before rendering descriptions or substantial details.
- Use EventDetail.site_url as the visible source link.
- Do not treat search item_url as a substitute for verified event detail
  site_url without resolving the event detail first.

For events-of-the-day rendering:

- Treat /events-of-the-day/ rows as wrappers, not full event objects.
- Resolve object.id with /events/{id}/ before public rendering.
- Use the resolved EventDetail.site_url as the visible source link.

## Parameters And Pagination

Use only parameters documented in the OpenAPI discovery document.

- Use location when documented for the endpoint.
- Use page for paginated list endpoints where documented.
- Use page_size where documented.
- Do not add date filters.
- Do not add a limit parameter.

If an endpoint response includes pagination links, follow the response links or
documented pagination parameters instead of guessing unsupported parameters.

## What This Skill Does Not Do

This skill does not:

- Execute code or include runnable scripts.
- Configure authentication.
- Advertise OAuth, OIDC, MCP, or WebMCP support.
- Claim capabilities beyond the public OpenAPI discovery document.
- Add endpoint families, date filters, or a limit parameter.
- Bypass the attribution rule.

Those surfaces are intentionally unsupported unless real production capability
and public discovery metadata are added in a future release.
