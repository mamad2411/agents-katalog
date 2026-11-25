---
name: aem-headless
description: AEM headless review — Content Fragment models, GraphQL persisted queries, CF Java integration, CORS, and Dispatcher rules for headless delivery
allowed-tools: Read, Grep, Glob
argument-hint: "[CF model path, persisted query path, or Java class]"
---

Review `$ARGUMENTS` for AEM headless issues. Report each finding as **Blocking** / **Warning** / **Suggestion**.

## Content Fragment models

- CF model definition not under `/conf/<project>/settings/dam/cfm/models/` — Blocking
- Field `name` changed on an existing model — breaks all existing fragments silently — Blocking
- Required fields added to a model with existing fragments — prevents fragment editing — Warning
- Missing `fieldLabel` on model fields — authors have no guidance — Warning
- Model placed in `ui.apps` instead of `ui.content` — models are mutable content — Blocking

## GraphQL persisted queries

- Ad-hoc GraphQL queries used instead of persisted queries — blocked by Dispatcher in production — Blocking
- Persisted query not stored under `/conf/<project>/settings/graphql/persistedQueries/` — Blocking
- No pagination on queries that could return unbounded result sets — Warning
- Sensitive JCR paths or internal structure exposed in response fields — Warning
- Query not tested against the fragment variations it needs to support — Suggestion

## Java / Sling Model integration

- `resource.adaptTo(ContentFragment.class)` result not null-checked — Blocking
- `ContentFragment.getElement(name)` result not checked for null or missing element — Blocking
- Fragment creation done via raw JCR writes instead of the `FragmentTemplate` API — Warning
- `SlingHttpServletRequest` adapted to `ContentFragment` directly — Blocking

## Dispatcher and CORS

- `/graphql/execute.json/*` not allowed in Dispatcher filter rules — persisted queries blocked — Blocking
- CORS policy hardcoded in a servlet filter instead of `ui.config` OSGi config — Warning
- Caching headers not set on GraphQL responses — unbounded cache TTL — Warning

## Delivery

- Fragment variations not handled in consuming code — Warning
- Language copies not considered in CF model or query — Suggestion
