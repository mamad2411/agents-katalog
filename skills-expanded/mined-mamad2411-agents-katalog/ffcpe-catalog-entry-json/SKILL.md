---
name: ffcpe-catalog-entry-json
description: >-
  Use when authoring or validating an FFCPE (Firefly Creative Production for Enterprise) custom-action catalog-entry.json
  for the run-workflow service (App Builder actions). Covers installing the Adobe I/O
  CLI and this plugin, schema shape, org/auth, agent discovery, customActionConfig,
  validation, workflow usage, and troubleshooting. Use **`aio ffcpe catalog`** to
  validate/register—never raw curl. Older searches may say **Workflow Builder**; same plugin and topic **`ffcpe`**.
---

# Catalog entry JSON (`catalog-entry.json`)

Use this skill to **author, review, or fix** a JSON document that registers an App Builder action with the **run-workflow** catalog so it can be used in workflows. For every catalog operation (list, register, inspect, …), use the **`aio ffcpe catalog`** commands from **@adobe/aio-cli-plugin-ffcpe**—do not suggest **`curl`** or ad-hoc HTTP clients.

## File naming and placement (App Builder projects)

**Best practice:** one catalog entry file **per custom action**, named **`<action-name>.entry.json`**, in the **same directory** as that action’s web and worker sources:

```text
actions/<action-name>/
  <action-name>.web.ts
  <action-name>.worker.ts
  <action-name>.entry.json
```

- **`<action-name>`** should match the OpenWhisk action basename and your **`mountFfcpeNodeRoutes`** / manifest naming where practical.
- The file content is the full catalog payload (**`handlerType: "custom-action"`**, **`inputs`** / **`outputs`**, **`customActionConfig`**, discovery fields)—not a stub or pointer file.
- Pass this path to **`aio ffcpe catalog validate --file …`** and **`register --file …`**. A repo-root **`catalog-entry.json`** is fine for one-off samples; prefer **`<action-name>.entry.json`** co-located when the app has multiple actions.

Scaffolding web/worker layout: skill **`ffcpe-app-builder-actions`** in [ffcpe-custom-node-sdk](https://github.com/adobe/ffcpe-custom-node-sdk).

## Install Adobe I/O CLI and the FFCPE plugin

1. **Node.js** — Use a supported LTS version (this plugin expects **Node 18+**).
2. **Adobe I/O CLI (`aio`)** — Install globally, then confirm it runs:

   ```sh-session
   npm install -g @adobe/aio-cli
   aio --version
   ```

3. **This plugin (`@adobe/aio-cli-plugin-ffcpe`)** — Install into `aio` as a plugin. Use **one** of:

   ```sh-session
   aio plugins:install @adobe/aio-cli-plugin-ffcpe
   ```

   Or install from a **Git URL** (fork, feature branch, or internal mirror):

   ```sh-session
   aio plugins:install https://github.com/adobe/aio-cli-plugin-ffcpe
   ```

   Replace the URL with your org’s repo if you do not use `adobe/aio-cli-plugin-ffcpe`.

4. **Verify** the **`ffcpe`** topic is available (older material may use the name **Workflow Builder** for the same capability):

   ```sh-session
   aio ffcpe catalog --help
   ```

5. **Authenticate for catalog calls** (same session the CLI uses for other Adobe I/O commands):

   ```sh-session
   aio login
   aio console org select
   ```

If **`aio ffcpe`** is not found after install, run **`aio plugins`** and confirm **`@adobe/aio-cli-plugin-ffcpe`** is listed; reinstall with **`aio plugins:install`** if needed.

## `orgId` and auth

- **Do not include `orgId` in the catalog JSON body.** The API sets it from **`x-gw-ims-org-id`** or the Bearer access token (IMS profile / JWT).
- Registration requires a resolvable org; otherwise the API returns **401** with **`orgId is required`**.
- **Composite key:** `(orgId, actionType, version)`. Different orgs can implement the same `actionType`; one org can ship multiple versions (e.g. `1.0.0` and `2.0.0`). You may reuse a built-in `actionType` to provide an **org-specific override**.

## Required shape (custom actions)

- **`handlerType`:** `"custom-action"`.
- **`customActionConfig`:** required; valid **HTTPS** **`submitEndpoint`** and **`statusEndpoint`**; optional polling: `pollIntervalMs` (default often 3000), `maxPollAttempts` (e.g. 100), `timeoutMs` (e.g. 300000).
- **`version`:** valid semver (e.g. `1.0.0`).
- **`inputs` / `outputs`:** at least one port each; port **`name`** unique within each array.
- **`parameters`:** each **`name`** unique within `parameters` (array may be empty).

The API may accept legacy names (`inputPorts`, `outputPorts`, `enabled`, `appBuilderConfig`) but prefer **`inputs`**, **`outputs`**, **`disabled`**, **`workflowEnabled`**, **`customActionConfig`**.

## Agent and discovery (required for registration)

These fields help agents suggest and chain your action. At least one entry each; refine later with PUT.

| Field | What to put | Min |
|-------|-------------|-----|
| **`relatedActions`** | `actionType` values that chain or complement yours | 1 |
| **`usage.commonPatterns`** | When this action fits in a workflow | 1 |
| **`usage.bestPractices`** | Tips for better results | 1 |

**Image-oriented example:**

```json
"relatedActions": ["input-images", "remove-background", "image-analysis"],
"usage": {
  "commonPatterns": [
    "Chain after background removal for product descriptions",
    "Use for accessibility captions"
  ],
  "bestPractices": [
    "Use clear prompts; high-res input improves results",
    "Specify output format expectations"
  ]
}
```

**Video-oriented example:**

```json
"relatedActions": ["input-videos", "video-transcribe", "preview-videos"],
"usage": {
  "commonPatterns": [
    "Process video clips for analysis",
    "Generate subtitles from video"
  ],
  "bestPractices": [
    "Ensure supported video formats",
    "Clear audio improves transcription quality"
  ]
}
```

Discover valid `actionType` values with **`aio ffcpe catalog list`** (add **`--include-core`** to include Adobe built-ins). Use **`--json`** for raw API-shaped output.

## Full catalog entry example

Use HTTPS App Builder / Runtime API URLs from **`aio app deploy`** output. Replace placeholders with your deployed web action base URL + route suffixes.

**Deriving endpoints after deploy:**

```text
# Deploy prints:
https://3326322-myproject-stage.adobeioruntime.net/api/v1/web/my-package/my-action-web

# Catalog:
submitEndpoint → …/my-action-web/submit
statusEndpoint → …/my-action-web/status
```

Use **`/api/v1/web/`** (not `/apis/v1/`). The Runtime hostname namespace is lowercase.

```json
{
  "actionType": "image-to-text",
  "version": "1.0.0",
  "name": "Image to Text",
  "description": "Analyzes images and returns text descriptions.",
  "category": "custom",
  "disabled": false,
  "workflowEnabled": true,
  "aliases": [],
  "tags": ["ai", "image", "text"],

  "inputs": [
    {
      "name": "image",
      "type": "image",
      "required": true,
      "mimeTypes": ["image/jpeg", "image/png", "image/gif", "image/webp"],
      "description": "One or more images to analyze"
    }
  ],

  "outputs": [
    {
      "name": "text",
      "type": "text",
      "mimeTypes": ["text/plain"],
      "description": "Text description of the image(s)"
    }
  ],

  "parameters": [
    {
      "name": "prompt",
      "type": "string",
      "required": false,
      "defaultValue": "Describe what is happening in these images.",
      "description": "Custom prompt for image analysis"
    }
  ],

  "relatedActions": ["input-images", "remove-background", "image-analysis"],
  "usage": {
    "commonPatterns": [
      "Chain after background removal for product descriptions",
      "Use for accessibility captions"
    ],
    "bestPractices": [
      "Use clear prompts; high-res input improves results",
      "Specify output format expectations"
    ]
  },

  "handlerType": "custom-action",
  "customActionConfig": {
    "submitEndpoint": "https://3326322-myproject-stage.adobeioruntime.net/api/v1/web/my-package/my-action-web/submit",
    "statusEndpoint": "https://3326322-myproject-stage.adobeioruntime.net/api/v1/web/my-package/my-action-web/status",
    "pollIntervalMs": 3000,
    "maxPollAttempts": 100,
    "timeoutMs": 300000,
    "authentication": { "type": "ims_service_token" }
  }
}
```

## `customActionConfig.authentication`

**Default for App Builder + `mountFfcpeNodeRoutes`:** use **`ims_service_token`**. The SDK enables IMS inbound auth on `/submit` and `/status` unless you pass **`authenticate: null`**. If the catalog declares **`none`** but the web action still requires IMS, run-workflow calls fail (and manual curl returns `Missing required header(s): Authorization, x-api-key`).

Only use **`none`** when the web action explicitly disables auth (`authenticate: null` in **`mountFfcpeNodeRoutes`**) and your security review allows it.

| JSON | Use case |
|------|----------|
| `{ "type": "ims_service_token" }` | **Recommended default.** Run-workflow obtains an IMS service token and calls your endpoints with **`x-api-key: run-workflow-service`** and **`Authorization`**. Matches default **`mountFfcpeNodeRoutes`** auth. |
| `{ "type": "none" }` | No authentication — only when web action passes **`authenticate: null`** |
| `{ "type": "api-key", "headerName": "X-API-Key", "secretName": "MY_API_KEY" }` | API key header; `secretName` references an env var or secret |
| `{ "type": "bearer", "secretName": "MY_BEARER_TOKEN" }` | Bearer token from env/secret |

## Managing the catalog (Adobe I/O CLI)

Always use **`aio ffcpe catalog …`** (this plugin), not raw HTTP. Prereqs: **`aio login`**, **`aio console org select`**, and this plugin installed. Optional: **`--base-url`** / **`AIO_FFCPE_CATALOG_BASE_URL`**, **`--org-id`**, **`--api-key`**, **`--json`** on commands that support them.

| Goal | Command |
|------|---------|
| Register new action | `aio ffcpe catalog register --file ./actions/<action-name>/<action-name>.entry.json` (optional **`--strict`**) |
| Inspect one action | `aio ffcpe catalog inspect <actionType>` (optional **`--version <semver>`**) |
| List actions | `aio ffcpe catalog list` (filters: **`--workflow-enabled`**, **`--category`**, **`--include-tags`**, **`--exclude-tags`**, **`--include-core`**, **`--compact`**, **`--json`**) |
| Full replace | `aio ffcpe catalog update <actionType> --file ./actions/<action-name>/<action-name>.entry.json` (optional **`--version`**, **`--strict`**) |
| Disable (hide from UI by default) | `aio ffcpe catalog disable <actionType>` |
| Re-enable | `aio ffcpe catalog enable <actionType>` |
| Delete | `aio ffcpe catalog delete <actionType>` (optional **`--version`** to delete one semver; omit to delete all custom versions for that type) |
| Validate file only | `aio ffcpe catalog validate --file ./actions/<action-name>/<action-name>.entry.json` |

Run **`aio ffcpe catalog <command> --help`** for the exact flag set.

## Workflow JSON: `actionSource` and ports

When both built-in and custom catalog entries share an **`actionType`**, **`actionSource`** picks the implementation:

| Value | Behavior |
|-------|----------|
| Omitted or **`"built-in"`** | Prefer built-in, then catalog (backward compatible). |
| **`"custom"`** | Only your org’s custom catalog entry; built-in ignored. Fails if no custom exists. Org comes from auth—do not put `orgId` in the workflow for this behavior. |

Example action node forcing custom **`remove-background`**:

```json
{
  "actionId": "rb-001",
  "actionType": "remove-background",
  "actionSource": "custom",
  "parameters": {}
}
```

**Connections:** `sourcePort` / `targetPort` must match **`outputs[].name`** and **`inputs[].name`** from the catalog (and from upstream/downstream nodes). Mismatched port names are a common cause of runtime failures.

**Minimal pattern:** `input-images` → `outputs` port connects to a custom action’s input port name (e.g. `image`). For chained flows (e.g. input → remove-background → image-to-text), each **`connections[]`** entry wires one source **`actionId`** + **`sourcePort`** to target **`actionId`** + **`targetPort`**.

## Validation rules (register-time)

1. **`actionType`** unique per org for a given **version**; may match a built-in for an org override.
2. **`actionType`** kebab-case (lowercase letters, numbers, hyphens).
3. **`handlerType`** must be **`"custom-action"`** for these registrations.
4. **`customActionConfig`** required when `handlerType` is `custom-action`.
5. **`submitEndpoint`** and **`statusEndpoint`** must be valid **HTTPS** URLs.
6. **`inputs`:** at least one port.
7. **`outputs`:** at least one port.
8. Port **`name`** unique within `inputs` and within `outputs`.
9. Parameter **`name`** unique within `parameters`.
10. **`orgId`** is enforced by the API from auth, not from the JSON body; callers must send auth that resolves an org.
11. **`relatedActions`:** required, ≥1 entry.
12. **`usage.commonPatterns`:** required, ≥1 entry.
13. **`usage.bestPractices`:** required, ≥1 entry.

## Agent workflow

1. Confirm **`actionType`**, **`version`**, endpoints, ports, parameters, and auth.
2. Fill **`relatedActions`** and **`usage`** with concrete, accurate strings (use catalog list to pick real `actionType` IDs).
3. Emit final JSON in a fenced **`json`** block; **omit `orgId`**.
4. Suggest **`aio ffcpe catalog validate --file …`** then **`aio ffcpe catalog register --file …`** (same JSON file).

## Troubleshooting

### `orgId is required` (401)

- Org could not be resolved for the CLI request.
- Run **`aio console org select`** and retry, or pass **`--org-id`** on **`aio ffcpe catalog`** commands if you must override.

### `relatedActions` / `usage.commonPatterns` / `usage.bestPractices` required

- Add at least one item to each (see **Agent and discovery** above).
- Use **`aio ffcpe catalog list`** (and **`--include-core`** if you need built-in IDs) to pick valid **`relatedActions`** targets.

### Action type already exists

- Another registration already uses that **`actionType`** for your org/version context.
- Use **`aio ffcpe catalog update <actionType> --file …`**, or choose a different **`actionType`**.

### Invalid endpoint URL

- **`submitEndpoint`** / **`statusEndpoint`** must be valid **HTTPS** URLs (typically your Runtime web action URLs).
- Copy the **web action base URL** from **`aio app deploy`**, then append **`/submit`** and **`/status`**.
- Use **`/api/v1/web/<package>/<web-action>`** — not **`/apis/v1/`**.

### Auth mismatch (`Missing required header(s): Authorization, x-api-key`)

- Default **`mountFfcpeNodeRoutes`** enables IMS inbound auth.
- Catalog must declare **`"authentication": { "type": "ims_service_token" }`**, not **`none`**, unless the web action passes **`authenticate: null`**.
- After fixing auth in **`.entry.json`**, run **`aio ffcpe catalog update <actionType> --file …`**.

### Action registered but workflow fails

- Confirm App Builder app is deployed and implements the expected submit/status contract.
- **Port names** in the catalog must match what the app and workflow connections expect.
- Check **`actionSource`** if both built-in and custom implementations exist.
