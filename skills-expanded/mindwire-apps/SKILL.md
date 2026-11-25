---
name: mindwire-apps
description: Build, repair, save or publicly deploy an app using Mindwire Apps, Cloud port sharing and static Pages.
---

Turn the user's requested outcome into a working app using their existing project and tools. Respect their technology and design choices. Handle technical setup without requiring another AI account.

Use `apps_list` and `apps_get` before replacing an existing app. Keep its owning computer, project, files and saved identity unless the user requests a move. For a linked computer, pass the discovered `workspaceId`; local paths and URLs refer to that computer. An offline computer is not a reason to duplicate its app locally.

Build and start the app, then verify that its intended URL is usable. Register it with `apps_register`, providing a short name, an SF Symbol or bot icon, and its HTTP(S) URL. For a local service use `http://127.0.0.1:PORT/path`; the client handles authenticated port forwarding. Store credentials in the app environment, outside frontend code, links, startup commands and conversation output.

When the app needs startup assistance, provide an idempotent `startupCommand` that ensures its service is running and returns within 20 seconds. Reuse a service manager or detach the process and its output; a foreground web server will time out. A `healthPath` must stay on the same origin. Registration saves this command without executing it; opening an unavailable app invokes the readiness flow.

Update an existing shortcut through `apps_update` using the latest `expectedRevision`. Ordinary bots can edit apps they own; ask the manager to update another bot's app. Archiving removes the shortcut and pauses its schedules, while leaving files and services intact.

## Public deployment

A saved shortcut is private by default. When the user asks to publish or share publicly, use `apps_request_publish` with its `appId` and owning `workspaceId`. This returns a native action card for the user; it is a request, not a deployment receipt. The client owns account authorization, hosting adapters and subscription checkout. Never request their cloud token or start a checkout from a shell command.

For a running web app on a Mindwire Cloud computer, keep its saved loopback URL and working startup command. The Publish action verifies readiness, reuses an existing public port when present, or exposes the app's own port. Expose only the application, never Mindwire's daemon, SSH, databases, development inspectors or secret/admin services. Public access does not add authentication to the app: add sign-in before publishing private user data. A cloud-backed app must stay running for its public link to work.

For a static website, build a dedicated output folder inside the project (for example `dist` or `out`) containing `index.html` and public assets only. Set `staticDirectory` on `apps_register` or `apps_update` to that folder. Exclude source secrets, credentials, environment files, databases, dependency folders and symbolic links. The native Publish action validates the output and exports it from the cloud computer as an Oblien Page; later publishing updates the same page. Pages cannot run a backend: an app with server-side code uses port hosting instead.

On a local Mac or another computer without Mindwire Cloud hosting, the card opens the Mindwire Cloud subscription flow. Explain briefly that public hosting needs Mindwire Cloud. Buying a subscription does not copy the local project. After the user has a connected cloud computer, use the manager's existing linked-computer tools to arrange moving/building the app there with their approval; register the actual cloud-owned app and request publishing on that computer. Keep the local app working and do not silently overwrite it or claim that the migration happened.

After the user publishes, read `apps_get` and use its confirmed `publicUrl`. Keep the original `url` for private access. Never invent a URL or say it is live just because the action card appeared. If the user only asked to build locally, save the shortcut without requesting public deployment.

For requested reminders, background work or notifications, load `mindwire-automations`. Report what actually started and saved, with any remaining error. Successful registration returns the app card; do not invent a saved shortcut or a working deployment.
