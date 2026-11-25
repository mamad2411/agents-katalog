---
name: share-build
description: Share a mobile build with testers through buildtree. Use when someone wants to send, share, distribute, install or test an Android or iOS build, wants the install link or QR code for a build, or asks for the latest build of an environment or branch.
---

# Share a build with testers

buildtree gives every uploaded build an install link and a QR code. Testers open the link on their phone and tap Install. Your job is to find the right build and hand back the links in a form the user can forward.

## Steps

1. If the user did not name the app, call `buildtree_list_projects` and use the only project, or ask which one when there are several.
2. Work out which build they mean:
   - "latest", "current", "the build on dev" means the environment's checkpoint: call `buildtree_get_install_links` with `project` and `environment`, no `branch`.
   - A branch or feature name ("the payments branch build") means a pre-merge build: pass `branch` too.
   - A version number or a specific build: call `buildtree_list_builds` first, pick the matching id, then `buildtree_get_install_links` with `buildId`.
   - When the user names a platform, pass `platform` so the latest build of that platform is chosen.
3. Reply with the result. Always give the **pinned link** (installs this exact build), and mention the **folder link** when the user wants testers to always get the newest build for that environment or branch. The QR card renders by itself in hosts that support it; otherwise the QR image URL is in the result.
4. Offer a short message the user can paste to testers: app name, version, platform, the link, and the note that iPhone testers must register their device on the project's Devices page before an ad hoc build will install.

## Rules

- Do not create projects or change anything while sharing a build.
- If no ready build exists for the requested environment or branch, say so and suggest the closest one from `buildtree_list_builds` instead of guessing.
- Uploading a new build is not something this plugin does. Point the user at the buildtree CLI (`buildtree upload ./app.apk --env dev`), the dashboard, or the local buildtree MCP server in their coding agent.
- Never invent links. Only pass on URLs returned by the tools.

## Example

User: "Send the QA team the latest Android build on staging."

1. `buildtree_get_install_links` with `project: "acme"`, `environment: "staging"`, `platform: "android"`.
2. Reply: "Acme v2.4.0 (118), Android, staging checkpoint uploaded 2026-10-08. Install link: https://buildtree.sh/install/... Always-latest staging link: https://buildtree.sh/install/folder/acme/staging. Message for the team: ..."
