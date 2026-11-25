---
name: build-with-arcgis-rest-js
license: Apache-2.0
description: "Use this skill when REST JS is mentioned by a user or task, for querying docs related to REST JS, modifying existing applications that use ArcGIS REST JS packages, or building javascript and typescript web apps, web pages, node.js environments, clients and servers: To access arcgis services, web services, and location services, ArcGIS Location Platform, ArcGIS Online, or ArcGIS Enterprise, to integrate, consume, write, edit, search, read, query, and configure: requests, authentication, developer credentials, user portal and organizations, portal content, basemaps, feature services, elevation services, geocoding, places and maps, routing, and calculating routes. Use for REST JS documentation search, information, context, design and best practices, output guidance, validation, edge cases, and troubleshooting. Use when building custom methods that invoke the REST JS request method against ArcGIS services, and migrating from direct ArcGIS REST API calls to ArcGIS REST JS wrappers."
---

# Build with ArcGIS REST JS

ArcGIS REST JS is a suite of compact, modular JavaScript wrappers for the ArcGIS REST API that runs in Node.js and modern browsers. It handles authentication workflows and includes packages for developer credentials, feature services, portal operations, elevation, geocoding, demographics, places, routing, basemap sessions, and generic REST API requests. "ArcGIS REST JS" is synonymous with "REST JS" in this skill and in general.

Use ArcGIS REST JS for programmatic access to ArcGIS resources and operations from a browser or Node.js environments using a modular, package-based API instead of manually composing REST requests; and managing, building, and handling authentication objects, classes, request objects, and error objects for ArcGIS services.

## Package selection matrix

Choose packages related to user task:

- Base request, request options, fetch, and core authentication: `@esri/arcgis-rest-request`
- Hosted feature layer query/edit: `@esri/arcgis-rest-feature-service`
- Geocoding, address lookup, batch geocode, reverse geocode, autosuggest: `@esri/arcgis-rest-geocoding`
- Places of interest, nearby search, bounding box search, place details, category search: `@esri/arcgis-rest-places`
- Routing, directions, service areas, closest facility, travel cost matrix, fleet routing, and snap to roads: `@esri/arcgis-rest-routing`
- GeoEnrichment and demographics, queryDemographicData, data collections, analysis variables, standard geography: `@esri/arcgis-rest-demographics`
- Portal members, groups, content, sharing, and organization settings: `@esri/arcgis-rest-portal`
- Programmatically create and manage API keys, developer credentials, and OAuth 2.0 app credentials: `@esri/arcgis-rest-developer-credentials`
- Basemap sessions and session tokens: `@esri/arcgis-rest-basemap-sessions`

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## ArcGIS account requirements

Developers must have one of the following ArcGIS accounts to create applications: ArcGIS Location Platform (free), or ArcGIS Online or ArcGIS Enterprise with a Creator, Professional, or Professional Plus user type. The account's user type, role, and privileges provide access to different resources and operations.

## Authentication

DO NOT SKIP: Refer to the `follow-arcgis-authentication-patterns` skill for ArcGIS authentication requirements, including the appropriate type of authentication for different audiences, use cases, and types of application. If the skill is not available, search the project for any existing authentication patterns, and if none are found, query the Esri MCP server for developer documentation for authentication best practices.

## Installation and setup

Refer to the [installation guide](https://developers-mcp.arcgis.com/mcp/installation) via MCP or doc query for instructions and code samples on how to install ArcGIS REST JS in a client browser or node.js environment. Prefer ESM over CommonJS. Use CDN setup when appropriate.

### New application

Try to infer requirements based on existing project files and the wording of the prompt. If uncertain, ask for clarification before proceeding.

### New application with CDN

Use CDN setup with an import map to load ArcGIS REST JS modules in a browser environment without a bundler. CDN setup with a script tag is also possible, and the loaded packages will be added each individually as a property to `globalThis.arcgisRest`.

### New Node.js application or bundler setup

Use NPM to install ArcGIS REST JS in a Node.js environment or when using a bundler:

```bash
npm install @esri/arcgis-rest-js
```

Import the desired modules from `@esri/arcgis-rest-js` as the following example:

```javascript
import { request } from "@esri/arcgis-rest-js";
```

### Existing application

For existing applications, ensure that the installed version of ArcGIS REST JS is compatible with your project. If upgrading from an older version, review the [Release Notes and Migration Docs](https://developers.arcgis.com/arcgis-rest-js/release-notes/) for any breaking changes or required code modifications. Update your import statements and usage patterns as necessary to align with the current version of the library.

## How to query documentation

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

Documentation should be queried using the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`):

```
https://developers-mcp.arcgis.com/mcp
```
Use the `search_esri_developer_docs` tool to surface authoritative documentation pages with `arcgis-rest-js` as the `focus_area` parameter in addition to a specified `search_term`. Use the `fetch_esri_developer_docs` tool with the `page_url` parameter set to return the full content of a documentation page in Markdown format. 

Clearly indicate any recommendations and assumptions that are not grounded in the official documentation. If the MCP server is unavailable, consult official documentation URLs below.

## Documentation links

Official references - Use the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`) for all documentation lookup. Fall back to fetching documentation URLs if it is unavailable.

- [ArcGIS REST JS Introduction](https://developers.arcgis.com/arcgis-rest-js/introduction/) - Use this for a quick overview of the purpose, capabilities, and contents of ArcGIS REST JS as a library, tool, and product. Ideal for basic queries about REST JS

- [ArcGIS REST JS API reference](https://developers.arcgis.com/arcgis-rest-js/api-reference/) - Use for quick reference and technical lookup, and during implementation for all ArcGIS REST JS packages, classes, interfaces, types, enums, implementation details, and configuration steps. Use for discovering and confirming function signatures, options, parameters, and return contracts. Prefer this documentation as the ultimate source of truth for developing applications with REST JS.

- [ArcGIS REST JS GitHub Repo](https://github.com/Esri/arcgis-rest-js) - Source code to the open source ArcGIS REST JS library.

- [Authentication](https://developers.arcgis.com/arcgis-rest-js/authentication/) - Use this link for examples of using ArcGIS REST JS to authenticate and sign in with an API key, or `ApiKeyManager`, `ArcGISIdentityManager`, or `ApplicationCredentialsManager` classes for API key, user, or app credentials authentication on a browser or node.js server environment.

- [Installation](https://developers.arcgis.com/arcgis-rest-js/install/) - Use this link for instructions on how to install ArcGIS REST JS in your project.

- [Create an API key](https://developers.arcgis.com/arcgis-rest-js/authentication/tutorials/create-an-api-key/api/) - Use this link for examples how to use REST JS to create an API key programmatically.

- [Release Notes and Migration Docs](https://developers.arcgis.com/arcgis-rest-js/release-notes/) - Use this link for new release notes, and migration guide instructions between versions, and for troubleshooting version regressions, incompatibilities, breaking changes, and core updates.

- [System Requirements](https://developers.arcgis.com/arcgis-rest-js/system-requirements/) - Use this when troubleshooting and verifying system compatibility prerequisites for REST JS.

- [Data, Datasets and Open Data](https://developers.arcgis.com/documentation/datasets/) - Use this to find resources for data sources, open data, test data, layers, map layers, feature layers, services, free, public, and private datasets.

- [Errors and Error Handling](https://developers.arcgis.com/arcgis-rest-js/error-handling/) - Use this for a basic summary of the different errors in REST JS and how to handle them effectively.

- [Querying Data with Feature Services](https://developers.arcgis.com/arcgis-rest-js/data/) - Use this link for an overview of data services and for examples of using `arcgis-rest-feature-service` to query features from a data service, hosted data service, feature service, and feature layer.

- [Geocoding](https://developers.arcgis.com/arcgis-rest-js/geocode-and-search/) - Use this link for an overview of geocoding and for examples of using `arcgis-rest-geocoding` for geocoding, address search, autosuggest, and reverse geocoding.

- [Routing](https://developers.arcgis.com/arcgis-rest-js/route-and-directions/) - Use this link for an overview of routing and for examples of using `arcgis-rest-routing` to find routes, directions, and service areas.

- [Places](https://developers.arcgis.com/arcgis-rest-js/places/) - Use this link for an overview of the places API and for examples of using `arcgis-rest-places` to discover and search places nearby, on a map.

- [Data Enrichment](https://developers.arcgis.com/arcgis-rest-js/demographic-data/) - Use this link for an overview of data enrichment and how to use `arcgis-rest-demographics` to access global demographic data, and the ArcGIS GeoEnrichment service.

- [Elevation](https://developers.arcgis.com/arcgis-rest-js/elevation/) - Use this link for examples of using `arcgis-rest-elevation` to find the elevation of points or locations on a map.

- [Spatial Analysis](https://developers.arcgis.com/arcgis-rest-js/spatial-analysis/) - Use this link for an overview and code examples to perform spatial analysis.

## Patterns and guidelines

Before recommending implementation steps, gather:

- Runtime: browser, Node.js, serverless, or mixed.
- ArcGIS product target: ArcGIS Location Platform, ArcGIS Online, or ArcGIS Enterprise.
- Authentication pattern: public access, API key, user sign-in, or app credentials.
- Necessary package imports : geocoding, routing, feature services, portal, elevation, places, demographics, etc.
- Deployment constraints: CORS limitations, proxy availability, secret storage, multi-tenant requirements.
- User intent/goals
- Required ArcGIS services
- Produce implementation plans grounded in Esri docs and the REST JS API Reference.
- Explicitly document assumptions.
- Establish account prerequisites, security constraints, environment verification steps, and edge-cases.

Agent guidance and security requirements:

- Never hardcode or expose secrets in commitable source code or prompts, Always isolate secrets to a file that is local and covered in a .gitignore.
- Isolate server-side credentials within the server environment, and do not expose them to browser clients.
- Multi-user apps: model per-user sessions and token refresh behavior.
- Recommend setting least-privilege and referrer restrictions on public API keys/access tokens.
- Never include tokens and sensitive headers in logs.
- Handle pagination and service limits explicitly.
- If docs conflict, prefer the API reference, then the most current official documentation, and note the conflict explicitly.
- Never import every package by default.
- Justify each package choice by feature requirement.

## Validation process

For ArcGIS REST JS, provide validation steps that can be used by the agent to verify its work. This should include:

- [ ] ArcGIS REST JS package selection matches the requested capability.
- [ ] Guidance is grounded in official docs and API reference queried via MCP.
- [ ] Authentication configured without exposing secrets..
- [ ] Auth context, token presence, scope, expiration, privilege, and credential type matches runtime and service.
- [ ] Required parameters, expected geometry/reference systems, payload shape, methods, classes and properties all match against the API reference.
- [ ] Policy/network constraints, CORS, proxy, firewall, trusted origins, and organization security settings are considered.
- [ ] Confirm portal/service URL points to intended environment, and request endpoints are correct.
- [ ] A representative {domain}/self service request succeeds in target runtime.
- [ ] Error-handling paths validated with a simulated failure.
- [ ] Outstanding manual setup steps are explicitly called out.
- [ ] Confirm all assumptions documented.

## Gotchas and Edge Cases

- ArcGIS Online vs Enterprise base URL mismatches can cause auth and routing failures.
- Token audience mismatches can fail despite valid login.
- Service max record limits require pagination strategies.
- Spatial reference mismatches can produce incorrect geometry interpretation.
- Secure resources may appear available in one environment but fail in another due to org-level policy.
- ArcGIS Online and ArcGIS Enterprise may differ in org policies, endpoint behavior, or available services.
- Token expiration causes intermittent failures if no refresh strategy exists.
- Browser CORS and referrer restrictions can block requests despite valid credentials.
