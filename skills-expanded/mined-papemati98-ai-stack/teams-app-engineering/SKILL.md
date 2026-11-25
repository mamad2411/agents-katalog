---
name: teams-app-engineering
description: "Build, extend, review or debug Microsoft Teams apps: web tabs, TeamsJS/Teams SDK, SSO/NAA, Adaptive Cards, bots/message extensions, app manifests and packages, including embedding InitechApp. Use for Teams-hosted application development and its real client UAT; not for general web work or tenant administration."
---

# Teams app engineering

Extend the current application and its hosting before scaffolding another one.
Teams hosts the user experience through a package; it does not host the web app,
backend or database. A working MCP connection is a development tool, not the
runtime authentication or permission model of the app you build.

## Short path

1. Read the existing project profile, relevant app code, dependency lockfile,
   manifest and auth design. Reuse the current task context and confirmed IDs.
   Select the smallest requested surface and preserve existing business flows.
2. Use only the relevant reference below. Make the tab/identity/data boundary
   explicit in the existing TODO. For live tenant work use
   `m365-workspace-operator` and its existing `cloud-org-operator` gate; offline
   development and packaging do not require a cloud login.
3. Implement in the current stack. Use `design-ui` for UI and the existing
   design/UAT path; do not create another design plan merely for Teams. Keep
   real CRM/mail/payments and notifications disabled in development.
4. Check the changed behavior and package; independently exercise the actual
   Teams journey for supported roles/clients before claiming readiness.
   A Playground result or standalone browser page does not prove Teams UAT.

| Needed slice | Reference |
| --- | --- |
| Choose tab/native feature/bot, existing app, toolkit or SDK | [Surface and tooling](references/surface-and-tooling.md) |
| SSO, NAA, token audience, user/tenant authorization | [Authentication](references/authentication.md) |
| Iframe, headers, context, manifest, ZIP and icons | [Tab and package](references/tab-and-package.md) |
| Teams client tests, debugging, rollout and recovery | [UAT and debugging](references/uat-and-debugging.md) |

Optional offline package check:
`python scripts/validate_teams_package.py <app-package.zip>`.
It checks common packaging defects only, not full Microsoft schema, permissions,
hosting, authentication or actual client behavior. Use it within existing build
checks, not as a new approval ceremony. No network, extraction or file writes.

Scaffolding, installing dependencies, registering Entra apps, provisioning Azure,
opening tunnels, publishing/installing a Teams app and deploying backend code are
distinct operations. Reuse verified tools and existing authorization. Do not
automatically provision/deploy, add paid AI services or widen tenant permissions.
