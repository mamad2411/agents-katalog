---
name: domino-extensions
description: Build and operate Domino UI Extensions (mount a published Domino App at a Domino UI mount point with page context). Covers extension_manifest.json, the official installer versus the manual Extensions API, App publish and identity requirements, auth and host rules for Extension backends, and the /api/extensions/beta routes. Use when creating an Extension, wiring mount points, publishing an Extension App from a project, pointing an Extension at a new App version, or automating the Extension install lifecycle. Not for generic App deployment alone (see domino-apps) or SPA scaffolding (see domino-ui-bootstrap).
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY, outside a run a Personal Access Token or service account token. Creating an Extension needs admin permissions; publishing its App with extended identity propagation needs a SysAdmin or CloudAdmin.
---

# Domino Extensions

Applies to Domino 6.3 and Domino Cloud.

An **Extension** surfaces a published **App** at a Domino UI **mount point** (Project sidebar, Dataset details page, Dataset file three-dot menu, Model details page, Admin panel). Domino opens the App in a new tab and passes the originating page's context as query parameters. One App can back several Extensions; pointing an Extension at a newer App version is an admin configuration change, not a rebuild.

## When to use other skills

| Goal | Skill |
|---|---|
| Vite/React design system, `@dominodatalab/extensions-tools`, proxy-safe URLs | [domino-ui-bootstrap](../domino-ui-bootstrap/SKILL.md) |
| `app.sh`, ports, prefixes, App publish chain (`/api/apps/v1`), CI | [domino-apps](../domino-apps/SKILL.md), [domino-apps/API-APPS.md](../domino-apps/API-APPS.md) |
| Authentication, hosts, pagination and errors for any Domino API call | [domino-api-intro](../domino-api-intro/SKILL.md) |
| Governance from an Extension backend | [domino-governance](../domino-governance/SKILL.md) |

Docs: https://docs.domino.ai/cloud/platform-capabilities/features/extensions (overview), https://docs.domino.ai/cloud/platform-capabilities/features/extensions/create-manage-extensions (build your own), https://docs.domino.ai/cloud/platform-capabilities/features/extensions/install-domino-official-extensions (official catalog). The same pages exist under `/6.3/`.

## Requirements on the App

1. **Extended identity propagation enabled** ("Allow App to act for viewers in Domino" on the Access & sharing step; `content.extendedIdentityPropagationToAppsEnabled: true` on the App version over the API). Only a SysAdmin or CloudAdmin can publish an App with it on; without it the App cannot back an Extension (`POST /api/extensions/beta/extensions` returns 400). The deployment needs `SecureIdentityPropagationToAppsEnabled` and `com.cerebro.domino.apps.extendedIdentityPropagationToAppsEnabled`, both on by default on Cloud and 6.3. Once enabled on an App it cannot be disabled.
2. **A framework that reads proxied HTTP headers**: Flask and Dash do by default; Shiny needs Shiny Server Pro. The per-request viewer token arrives in the `Authorization` header after the viewer consents.
3. **Published and viewable**: an Extension inherits the App's access controls; users without view access see it listed and are prompted to request access.
4. Domino's App guidelines: call Domino APIs from backend code only (never from frontend JavaScript), authenticate with the per-request bearer from `Authorization` (never an API key), keep the App stateless or protect cached data like its source, declare dependencies in the Compute Environment's Dockerfile.

## Mount points and context

| `uiMountPointTypeConfigs` key | Where | Query parameters passed to `/` |
|---|---|---|
| `projectSidebar` | Project navigation sidebar | `projectId` |
| `dataset` | Dataset details page | `datasetId` |
| `datasetFileContext` | Three-dot menu of a file in a Dataset | `datasetId`, `datasetSnapshotId`, `filePath` |
| `modelDetails` | Model details page | `modelId`, `modelVersionId` |
| `adminPanel` | New page in the Admin panel | none |
| `netAppVolume`, `netAppVolumeFileContext` | NetApp Volume pages (API only) | `netAppVolumeId`, `netAppVolumeSnapshotId`, `filePath` |

`urlConfig.contextualQueryParams` accepts only the spec enum (the eight names above), and the App receives exactly what the config lists. The file parameter is `filePath`, not `datasetFilePath`. Read the parameters on the App's root route, validate the ones you need and return a clear 400 when they are missing, and call Domino with the forwarded `Authorization` header. A worked Flask example and the exact config shapes are in [API-EXTENSIONS.md](./API-EXTENSIONS.md).

## Create an Extension (custom App)

1. **Build and preview** the App in a workspace (App Preview), then **Publish App** as a SysAdmin or CloudAdmin with extended identity propagation on. Over the API: [domino-apps/API-APPS.md](../domino-apps/API-APPS.md).
2. **Create the Extension** from the App's three-dot menu (**Create Extension**) or **Admin panel > Extensions > Create Extension**: pick the App version and add one or more mount points. Needs admin permissions (a 403 means they are missing; see API-EXTENSIONS.md). Over the API: `POST /api/extensions/beta/extensions` with `name`, `enabled`, `appId`, **`appVersionId`** (a version with extended identity propagation on) and `uiMountPointTypeConfigs`; all five are required, `description` is optional. Body and the other routes: [API-EXTENSIONS.md](./API-EXTENSIONS.md).
3. **Manage** from Admin panel > Extensions: toggle enabled, **Manage Extension > Edit** to change mount points or the App version, **Delete** to soft-delete. Publishing a new App version does not move the Extension; edit it in the UI or `PATCH` `appVersionId` over the API.

## Official Extensions (manifest-driven)

Domino-built Extensions are installed, upgraded and uninstalled from **Admin panel > Extensions > Manage Domino-official Extensions**; the installer reads `extension_manifest.json` (`manifestSchemaVersion: 1`, sections `project`, `app`, `extension`) from a GitHub release and creates the Project, Compute Environment, App and Extension itself. Do not edit those managed entities by hand. Manifest fields, lifecycle rules and the install routes: [MANIFEST.md](./MANIFEST.md).

## Auth and hosts in Extension backends

| Call | Credential and base |
|---|---|
| Platform API as the **viewer** | Forward the request's `Authorization` header unchanged to `$DOMINO_API_HOST/api/...`; answer 401 when it is missing. Consent expires (8 hours by default, up to 30 days) |
| Platform API as the **publisher** | `$DOMINO_API_PROXY/api/...` with no header, or a bearer from `$DOMINO_API_PROXY/access-token` |
| Governance `/api/governance/v1/*` | Base URL per the `domino-governance` skill; bearer PAT or service account, never an API key |
| Model inference | The `url` from the endpoint record, not a hand-built host |
| Automation outside any run | Public deployment URL plus PAT or service account token |

Until a viewer consents, Domino redirects every request, JSON included, to `/app-consent`. The bearer is the viewer's own credential: take the viewer from its `preferred_username` claim, never `domino-username` (not sent here; clients can forge it); never log or store the token, never call without it (`$DOMINO_API_HOST` runs header-less calls as the publisher). No browser links from `DOMINO_API_HOST` or `DOMINO_USER_HOST`; put the public URL in a project environment variable. Slash, routes, scripts: [API-EXTENSIONS.md](./API-EXTENSIONS.md#identity-urls-and-scripts).

## Reference files

- [API-EXTENSIONS.md](./API-EXTENSIONS.md): `/api/extensions/beta` routes, create body, mount config shapes, Flask context example, patch and delete.
- [MANIFEST.md](./MANIFEST.md): `extension_manifest.json` fields, official install lifecycle and routes.
