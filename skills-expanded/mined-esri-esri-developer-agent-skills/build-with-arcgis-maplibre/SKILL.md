---
name: build-with-arcgis-maplibre
license: Apache-2.0
description: "Use for displaying maps in a browser environment with MapLibre GL JS and ArcGIS services with @esri/maplibre-arcgis: Render ArcGIS basemaps, styles, sessions, feature layers, vector tiles, queries, and location services with authentication. Covers install, setup, debug, documentation, best practices, guidelines, explanations, and validation."
---

# Build with MapLibre GL JS and ArcGIS

MapLibre ArcGIS is an Esri-supported open-source integration. MapLibre GL JS renders/styles; `@esri/maplibre-arcgis` loads supported ArcGIS resources including feature layers, vector tiles, basemaps, and basemap sessions. Use it for maps, data services, geocoding, routing, places, and other location services. It is not the ArcGIS Maps SDK for JavaScript.

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## ArcGIS account requirements

Developers must have one of the following ArcGIS accounts to create applications with ArcGIS: ArcGIS Location Platform (free), or ArcGIS Online or ArcGIS Enterprise with a Creator, Professional, or Professional Plus user type. The account's user type, role, and privileges provide access to different resources and operations.

## Authentication

DO NOT SKIP: Refer to the `follow-arcgis-authentication-patterns` skill for ArcGIS authentication requirements, including the appropriate type of authentication for different audiences, use cases, and types of application. If the skill is not available, search the project for any existing authentication patterns, and if none are found, query `esri-mcp-server-for-developer-documentation` for authentication best practices.

## Installation and setup

Always install `maplibre-gl` and `@esri/maplibre-arcgis` packages via CDN or NPM and import `maplibre-gl/dist/maplibre-gl.css` for CSS. Use the [API reference](https://developers.arcgis.com/maplibre-gl-js/api-reference/) for current URLs and supported versions. For geocoding, routing, and other ArcGIS Location Services, use [ArcGIS REST JS](https://developers.arcgis.com/arcgis-rest-js/).

### New application

Try to infer requirements based on existing project files and the wording of the prompt. If uncertain, ask for clarification before proceeding.

#### New application with CDN

Use an `importmap` from `maplibre-gl` and `@esri/maplibre-arcgis` to current CDN ESM URLs. Add REST JS packages as necessary. Check the API reference using `esri-mcp-server-for-developer-documentation` for current supported versions. Most ArcGIS documentation shows CDN imports; use them for testing, demos, tutorials, samples, and lightweight quickstarts.

#### New application with npm

Use Vite unless another framework is specified. Install/import core packages and CSS as ESM through any Node package manager. React, Angular, Vue, and Svelte are other supported frameworks. If using a vite template or another framework-specific template, remove all template files that are not relevant to the user's request (e.g. counter.js). Use this method for actual development, larger projects, and production builds.

### Existing application

Before installing, identify package manager/lockfile, framework, CDN versus Node-module imports, and project-level TypeScript/ESLint configs, bundler (webpack/vite/other). Conform; install core packages as required. Preserve environment/credential conventions. For CommonJS, use synchronous native `require` on Node 22+ or asynchronous dynamic `import()` on Node 12+; Node <12 is unsupported.

## How to query documentation

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

Documentation can be queried using the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`):
```
https://developers-mcp.arcgis.com/mcp
```
Use the `search_esri_developer_docs` tool to surface authoritative documentation pages with `maplibre-arcgis-plugin` as the `focus_area` parameter in addition to a specified `search_term`; Use the `arcgis-rest-js` focus area for ArcGIS REST JS queries. Use the `fetch_esri_developer_docs` tool with the `page_url` parameter set to return the full content of a documentation page in Markdown format. 

Clearly indicate any recommendations and assumptions that are not grounded in the official documentation. If the MCP server is unavailable, consult official documentation URLs below.

## Documentation links

Official references - prefer the Esri MCP server for developer documentation (`esri-mcp-server-for-developer-documentation`) for all page lookups and fall back to URLs if not available.

- [MapLibre GL JS with ArcGIS guide](https://developers.arcgis.com/maplibre-gl-js/) - overview and app setup.
- [MapLibre ArcGIS API reference](https://developers.arcgis.com/maplibre-gl-js/api-reference/) - plugin APIs and factories.
- [API keys](https://developers.arcgis.com/maplibre-gl-js/access-tokens/create-an-api-key/) and [OAuth](https://developers.arcgis.com/maplibre-gl-js/access-tokens/create-oauth-credentials-for-user-authentication/) - browser credentials.
- [Basemaps](https://developers.arcgis.com/maplibre-gl-js/maps/how-to-display-a-basemap-style/display-a-basemap/), [sessions](https://developers.arcgis.com/maplibre-gl-js/maps/how-to-display-a-map-with-a-basemap-session/create-a-basemap-session/), [feature layers](https://developers.arcgis.com/maplibre-gl-js/data/style-a-feature-layer/), and [vector tiles](https://developers.arcgis.com/maplibre-gl-js/data/add-a-vector-tile-layer/) - core workflows.
- [@esri/maplibre-arcgis](https://github.com/Esri/maplibre-arcgis) - source repository for MapLibre ArcGIS.
- [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/) and [Style Specification](https://maplibre.org/maplibre-style-spec/) - renderer/style semantics for MapLibre maps.
- [Calcite Components](https://developers.arcgis.com/calcite-design-system/components/) - Esri-style UI.
- [Attribution](https://esriurl.com/attribution) - Required Esri attribution information.

## Patterns and guidelines

- Identify product, portal/service URL, resource type, build tool, and auth need. Use `esri-mcp-server-for-developer-documentation` for the latest ArcGIS capabilities and MapLibre docs for map/style behavior.
- Let MapLibre ArcGIS manage attribution automatically through its Esri-aware `AttributionControl`; never remove attribution provided by `BasemapStyle` or hosted layers; do not use the default MapLibre attribution property. Keep credentials out of source control.
- Treat basemap style `applyStyle`, basemaps session operations, and all hosted layer factories as async boundaries. Add sources/layers within a `map.onAdd` listener after initial basemap/style resolution. Preserve basemap version, source/layer IDs, glyphs, sprites, and attribution.
- Use MapLibre ArcGIS helpers to manage sources and layers - `addSourceTo(map, options)` and `addLayerTo(map, options)`. For items with multiple layers use `addSourcesTo` and `addLayersTo`, and use  `addSourcesAndLayersTo` as a single-line convenience method. Do not use the native `map.addSource` or `map.addLayer` for feature layers and vector tile layers.
- BasemapStyle is a full replacement for the map's `style` property; omit `style` from the `Map` constructor entirely when using with the BasemapStyle class.
- To view all available styles, use the static `getSelf` method of the BasemapStyle class. Use `arcgis/navigation` as the default.
- Do not specify a `loadingMode` for feature layers unless debugging. Recommend vector tiles for efficient large-scale display. Add MapLibre sources before style layers; preserve source IDs/types; use `source-layer` only for vector tiles; use unique source and layer IDs and type-compatible expressions.
- Handle empty results and auth/network/session/refresh errors without exposing tokens. Use `Popup.setText` for untrusted text; sanitize HTML; Avoid duplicate maps/layers, clean up on teardown, prefer paint/layout changes over source data updates, query needed fields, and smoke-test.
- Use ArcGIS REST JS for geocoding, routing, places, elevation, and user authentication; Do not install REST JS if those services are not required. If using REST JS for authentication, acquire access tokens as strings from the `AuthenticationManager` and pass through to basemaps, sessions, and hosted layers. Reference the `build-with-arcgis-rest-js` skill for guidance as applicable.
- Authentication: Use API keys only for location services; avoid using them to authenticate feature layers or vector tile layers and recommend user authentication as an alternative. Keep app-auth credentials/secrets server-side if using.
- Use Calcite Components as a default UI framework. Reference the `calcite-design-system` skill for usage and guidelines as applicable.

## Validation process

Validate that:
- [ ] Install: Check manifest/lockfile/dependencies, API versions, imports, CSS, container dimensions, credentials, style/attribution, console/network errors, style/source/layer IDs, and vector `source-layer`.
- [ ] Credentials have required privileges/item access; portal, OAuth client, and redirect URI match.
- [ ] Basemap style loads through `BasemapStyle.applyStyle`; attribution remains visible.
- [ ] Feature sources precede layers; IDs/types/expressions are valid; vector `source-layer` values come from the service style.
- [ ] Queries/geocoding handle empty, auth/network/rate-limit cases and untrusted text; no key/token/secret is committed, logged, or exposed.
- [ ] Browser smoke test covers reload/multiple zooms with no console/network source, layer, style, or auth errors; examine GitHub releases for version-dependent behavior. Actual behavior requires manual developer validation.
- [ ] Verify the provided item ID or service URL is supported by the feature layer / vector tile layer class. Check console error messages for detailed information. Inform the user if the item or service is not supported and do not attempt a workaround.
