---
name: tags-and-properties
description: Manage Domino tags and properties via the Tags (Taxonomy) API at /api/taxonomy/v1. Covers namespaces and tags (create, list, update, deprecate, delete; tag entities such as projects, models, datasets, apps, project templates, NetApp volumes, environments; query by tag; autocomplete; merge; CSV import/export) and properties (typed metadata fields - text, number, date, boolean, url, user, organization, select, multi_select - with per-entity values, groups and versioned entities like model_version/app_version). Use when organizing entities with tags, building hierarchical namespaces, defining typed metadata fields, setting property values, finding entities by tag, bulk-tagging during onboarding, or migrating a taxonomy across environments.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token. Defining namespaces, tags and properties needs the Librarian or admin role.
---

# Domino tags and properties

Applies to Domino 6.3 and Domino Cloud.

The Tags API (`/api/taxonomy/v1`) manages two metadata systems:

- **Tags**: hierarchical labels grouped into **namespaces** (the key) with tags as the
  values. An entity either has a tag or not.
- **Properties**: typed metadata fields (`text`, `number`, `date`, `select`, ...), each
  holding one value per entity.

Docs:
https://docs.domino.ai/cloud/reference/api/tags-api,
https://docs.domino.ai/cloud/platform-capabilities/core-concepts/knowledge-management/tags,
https://docs.domino.ai/cloud/platform-capabilities/core-concepts/knowledge-management/properties.

## Configuration

Auth follows [domino-api-intro](../domino-api-intro/SKILL.md#authentication). In a run:

```bash
if [ -n "$DOMINO_API_PROXY" ]; then
  BASE="$DOMINO_API_PROXY/api/taxonomy/v1"; H="Accept: application/json"   # proxy adds the token
else
  BASE="$DOMINO_API_HOST/api/taxonomy/v1"
  H="Authorization: Bearer $(curl -s http://localhost:8899/access-token)"
fi
```

Outside Domino, `BASE="$DOMINO_API_HOST/api/taxonomy/v1"` with
`H="Authorization: Bearer $PAT"` (a PAT or service account token). The
examples pass `-H "$H"`; with the proxy it is only an `Accept` header. Never use
`DOMINO_USER_API_KEY`.

## Which path applies

Routes are identical on both targets. The entity types differ: run
`curl -s "$DOMINO_API_HOST/version"` and read `version`.

| Target | `entityType` / `allowedEntities` values |
|--------|------------------------------------------|
| Domino 6.3 | `dataset`, `project`, `project_template`, `model`, `model_version`, `app`, `app_version`, `netapp_volume`, `environment` |
| Domino Cloud (6.4 and later) | the 6.3 list plus `policy`, `policy_version`, `data_source` |

Other values return `400`. Casing matters (`Project` is rejected).

## Permissions

Building and changing the tag structure and property definitions needs the
**Librarian** role or an admin role (CloudAdmin on Cloud, SysAdmin on 6.3). Anyone can
apply tags and set property values on assets they own; admins can on any asset.

## Quick start: tag a project

```bash
# 1. Find the tag
curl -s -H "$H" "$BASE/tags/autocomplete?q=clinical"
# {"items":[{"id":"<tag-id>","path":"Clinical_Data / SDTM"}]}

# 2. Apply it
curl -s -X POST -H "$H" -H "Content-Type: application/json" \
  -d "{\"entityType\":\"project\",\"entityId\":\"$DOMINO_PROJECT_ID\",\"tagIds\":[\"<tag-id>\"]}" \
  "$BASE/rpc/tag-entity"

# 3. Verify
curl -s -H "$H" "$BASE/entity-tags?entityType=project&entityIds=$DOMINO_PROJECT_ID"
```

More workflows (hierarchy, discovery, autocomplete, properties): [WORKFLOWS.md](./WORKFLOWS.md).

## Rules and gotchas

- `tagIds` on `GET /entities` and `entityIds` on `GET /entity-tags` are array parameters:
  repeat them (`?tagIds=A&tagIds=B`). `/entities` returns entities that carry **all** of
  the given tags (AND). Filter by type with `entityTypes` (plural) on `/entities` and
  `/tags/{tagId}/entities`.
- A namespace with `allowMultipleAssignments: false` (the default) holds one tag per
  entity; applying another tag from it replaces the existing one.
- Tag and namespace `status` is `active` or `deprecated`. Deprecate (via `PUT`) to stop
  new assignments without touching existing ones.
- `DELETE /tags/{id}` and `POST /tags/bulk-delete` remove the tags **and their
  assignments** without confirmation. `DELETE /namespaces/{id}` removes the namespace and
  its tags but fails while any tag is still assigned: untag first or deprecate the
  namespace instead. Confirm destructive calls with the user. Pin tag ids, not labels, in
  automation.
- `POST /rpc/copy-entity-tags` and `/rpc/copy-property-values` are marked "Internal,
  service-account only" in the spec and **replace** the target's tags or values; they are
  not user workflows.
- `GET /config` returns the limits: `maxDepth`, `maxLabelLength`,
  `maxSelectAllowedValuesCount`, `maxSelectAllowedValueLength`.

## Properties

1. **Definitions** (`/properties`): `label`, `type`, `allowedEntities`, optional
   `groupName` and `allowedValues` (`select`, `multi_select` only). `type` is immutable.
   Reference: [PROPERTIES.md](./PROPERTIES.md).
2. **Values** (`/property-values/{entityType}/{entityId}`): `PATCH` a batch of
   `{propertyId, value}` or `{propertyId, values[]}` items; empty `value` clears.
   `model_version` and `app_version` take `?version=`. Reference:
   [PROPERTY-VALUES.md](./PROPERTY-VALUES.md).

## Reference files

- [API-TAGS.md](./API-TAGS.md): concepts, endpoint table, curl reference for namespaces, tags, entity tags, tree, config, troubleshooting
- [WORKFLOWS.md](./WORKFLOWS.md): worked workflows and taxonomy design practices
- [PROPERTIES.md](./PROPERTIES.md): property definitions
- [PROPERTY-VALUES.md](./PROPERTY-VALUES.md): property values, versioned entities, copy policies
- [BULK-OPS.md](./BULK-OPS.md): bulk delete, merge, copy tags and values between entities
- [IMPORT-EXPORT.md](./IMPORT-EXPORT.md): CSV export, validate and import

## Spec discovery

Published specs and per-deployment documents: [API-SPECS.md](../domino-api-intro/API-SPECS.md).
Your deployment's copy of this service's OpenAPI document is
`https://<domino-domain>/docs/openapi/data_taxonomy_service-swagger.json` (unauthenticated).
