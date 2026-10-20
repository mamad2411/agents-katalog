---
mode: agent
description: Demo step 2 - build the session countdown web app inside the generated demo project.
---

Skip clarification. Do not ask clarifying questions and do not wait for plan confirmation. Build this end to end, verify it, and report the result when finished.

## Azure authentication and project preflight

Complete this read-only preflight before creating or modifying application files:

1. Confirm the current workspace contains `project-orchestrator.json`, `reports/installation-verification.json`, and `.github/skills/azure-discovery/SKILL.md`. Stop if this is the Project Orchestrator source repository or installation verification is not `passed`.
2. Run `/azure-discovery -Gov` with `usgovarizona` as the target location. This is the only stage allowed to start the configured Azure CLI login flow. It must initialize or reuse `.azure/environment.json`, select `AzureUSGovernment` and the recorded subscription, authenticate immediately when the current session is missing or stale, and write current `reports/azure-discovery.json` and `reports/azure-discovery.md` evidence. If an existing valid profile selects another Government region, update it to `usgovarizona` for this demo.
3. Validate that `az cloud show --query name -o tsv` returns `AzureUSGovernment` and `az account show --query id -o tsv` returns a subscription ID. Stop now if either check fails after the discovery login flow; do not defer authentication until deployment.
4. Validate that `reports/azure-discovery.json` records `cloud` as `AzureUSGovernment` and `location` as `usgovarizona`. The discovered report must be no older than 14 days.
5. Set the workflow's deployment location from the discovery report, for example:

   ```powershell
   $discovery = Get-Content ./reports/azure-discovery.json -Raw | ConvertFrom-Json
   $location = [string]$discovery.location
   ```

6. Stop before application implementation if discovery, authentication, Azure Government selection, or location validation fails. Do not silently switch clouds, regions, or subscriptions.

This app workflow does not synthesize Speech and must not require `AZURE_SPEECH_KEY` or run the Project Video `azure-preflight` command. Project Video performs its own Speech readiness and approval checks only when `/project-video` is invoked. Discovery is read-only and does not authorize resource creation, deployment, Speech synthesis, or other billable work. The later deployment and Project Video approval gates remain required.

## Objective

Build a functional web app for the demo session titled **Skills Orchestrator**.

## Content

- Page and heading title: `Skills Orchestrator`
- Welcome line: `Welcome to the GitHub Copilot Skills Orchestrator Session`

## Schedule

- Scheduled start: **2:00 PM Central Time on September 17, 2026**. Use the ISO value `2026-09-17T14:00:00-05:00`; the `-05:00` offset is correct because Central is on daylight time in September.
- The session lasts **60 minutes**.
- Render all displayed times through `Intl.DateTimeFormat` with time zone `America/Chicago` so they stay correct on any machine.

## Behavior

Three phases, driven by the current time:

1. **Before the start time** - show `Starting soon`, the scheduled start time, and a live countdown until the start.
2. **Between start and start + 60 minutes** - show a live countdown to the end of the session.
3. **After start + 60 minutes** - show a thank-you message with the presenter's contact information.

## Test mode

- Provide a test mode that reads the current date and time and sets the start time to **30 minutes before now**, so the page is mid-session with a visibly moving countdown.
- Test mode is the default. A `?mode=live` query parameter selects the real schedule and `?mode=test` forces test mode.
- Show a visible badge indicating which mode is active, so the wrong mode is never presented by accident.
- Support an `?at=<ISO timestamp>` override that pins the clock, so any phase can be previewed instantly during rehearsal.

## Presenter information

Put the presenter details in a single configuration module, keeping each link's display label separate from its URL so the rendered text stays readable:

| Field | Display | Link target |
| --- | --- | --- |
| Presenter | Anthony Marsiglia | - |
| Role | Principal Cloud Solution Architect | - |
| Email | anmarsig@microsoft.com | `mailto:anmarsig@microsoft.com` |
| LinkedIn | anthony-marsiglia-045b30b2 | `https://www.linkedin.com/in/anthony-marsiglia-045b30b2` |
| GitHub | QuyDu/Skills-Orchestrator | `https://github.com/QuyDu/Skills-Orchestrator` |

Every URL must carry an explicit `https://` scheme; a scheme-less value such as `www.linkedin.com/...` resolves as a relative path and produces a broken link. Render outbound links with `rel="noopener noreferrer"`.

## Scannable codes

On the **thank-you screen only**, show three QR codes so the audience can capture your details:

1. **Save contact** - a vCard 3.0 payload carrying the name, role, email, and both URLs. Use CRLF line endings; some scanners reject an LF-only card.
2. **LinkedIn** - the LinkedIn profile URL.
3. **GitHub repo** - the repository URL.

Generate every code as an SVG at build time using `qrcode` as an exact-pinned devDependency, writing into the build output directory. Do not fetch QR images from an external service at runtime: the demo must work without internet, and the presenter's details must not be sent to a third party. Use error-correction level `M` and a white background so they scan reliably from a projector. Give every code descriptive alt text.

## Implementation requirements

- TypeScript compiled with `tsc`, matching the project's declared stack. No runtime dependencies; QR generation happens at build time only.
- Keep all schedule and phase logic in a pure module with no DOM access, so it is unit testable.
- Add unit tests using `node:test` covering: the published start time formats as 2:00 PM CDT on September 17 2026, test mode backdates the start by 30 minutes, phase boundaries at start and at start + 60 minutes, countdown formatting, and that countdowns never go negative.
- Wire `npm run build`, `npm test`, and `npm start`. `npm start` must serve the app locally with a zero-dependency Node static server that refuses to serve files outside the project root.
- Follow the scoped instructions in `.github/instructions/`.

## Verification

Run the tests, start the server, and confirm in the browser that all three phases render correctly.

## Deployment to Azure Government

After the app builds and every test passes, deploy it using the project's own governed entry point at `infra/deploy.ps1`. Do not author a new deployment skill and do not hand-roll `az deployment` calls.

Use `skillsdemo` as the site name. It is 10 characters, inside the 12-character limit, and yields the resource group `rg-skillsdemo`. Reuse `$location` from the validated Azure discovery report; do not replace it with a hard-coded region.

1. Reconfirm the Azure CLI session established during the beginning preflight is still signed in and targeting Azure Government. `az cloud show --query name -o tsv` must return `AzureUSGovernment` and `az account show --query id -o tsv` must return a subscription ID. If the session expired or changed after preflight, stop and report the exact prerequisite; do not switch clouds or start another interactive login at deployment time.
2. Explain that deployment will create `rg-skillsdemo`, billable Azure Government resources, and a public endpoint. **Stop here and ask the presenter for explicit approval before any Azure mutation.** Proceed only on an explicit yes.
3. After approval, create the resource group, then preview the exact changes:

   ```powershell
   az group create --name rg-skillsdemo --location $location -o none
   ./infra/deploy.ps1 -SiteName skillsdemo -AzureGov -Location $location -AppServiceSku B1 -NoKeyVault -WhatIf
   ```

   The resource group must exist before `-WhatIf`, because the preview uses a resource-group deployment.

4. Show the complete preview. Stop and report if it contains unexpected changes. On the already granted approval, run the same deployment command without `-WhatIf`, then publish the built site to the created web app and report the resulting HTTPS URL.
5. The application must bind to the port supplied by App Service through `process.env.PORT`. Set an explicit startup command if the platform does not detect one.
6. Verify the deployed URL over HTTPS: confirm the page loads and that all three phases render using the `?mode=` and `?at=` overrides.

Never place secrets, connection strings, or service keys in app settings; the web app authenticates with its managed identity.

## Constraints

- Do not commit or push.
- Do not add runtime dependencies.
