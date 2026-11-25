---
name: tines-export-to-3b
description: Your guide to reading a Tines story export JSON and rebuilding it as a 3B workflow. Use this whenever you see a Tines export JSON, are asked to migrate or convert a Tines story to 3B, or hit Tines concepts like actions, Event Transformation, formulas, credentials, teams, or links and need the 3B equivalent in order to build it.
license: Apache-2.0
compatibility: Tines 3B
---

# Building a 3B workflow from a Tines export

You'll be handed a Tines story as a JSON export and asked to rebuild it in 3B. This guide tells you, for each Tines piece, what to build in 3B and how. Treat it as a starting map, not gospel: some mappings are unproven, so when something looks ambiguous (especially formulas, dates, and type coercion), flag it rather than guessing silently.

When a mapping uses a named volume for a queue, join, deduplication, delayed work, or retained files, use `workflow-volume-design` before choosing its file layout and schedule.

## Flag these up front (not portable / needs human input)

- **5-minute (300s) per-step execution ceiling** — there's no way today to run a step longer than that, so long running steps or delays need to be considered up front and broken up (durable state in a volume + cron continuation).

## Always: write a migration report in the workflow README

After building, document the migration in the workflow README. Cover:

- **Link back to the original** - If the JSON export contains a `story_url` then include this at the top of the migration report as a hyperlink "View original story on Tines".
- **What was migrated** — the Tines actions and how each maps to its 3B step.
- **What changed shape** — anything that isn't a 1:1 port (fan-out → single-run loops, Implode → SQLite join, formulas → code), so the user knows where behavior may differ.
- **What needs a human** — flag everything you couldn't fully reproduce or that needs the user to finish: e.g. agentic AI actions, missing credentials, anything where a formula/date/type-coercion translation is uncertain.
- **What to double-check** — call out the silent-failure risks (missing fields, type coercion, cross-run dedup) so the user knows where to verify.
- **Existing Tines dependencies** — any calls back to Tines for Resources / Records etc. This will be important for the customer if they look to ever decommission their Tines Stories infrastructure and move fully to 3B.

Treat this report as a required deliverable, not optional polish — it's how the user audits a migration they didn't watch happen.

## The one thing to internalize first

**3B has no per-event routing or fan-out.** Where Tines splits a list into N events and runs downstream steps once per event, you keep a **single run**: the array rides on stdin, and each step loops over it. The outputs match Tines, but two things differ — side effects must loop explicitly, and there's no per-event isolation. This pattern shows up in Explode, Condition, and no-match links, so get comfortable with it now.

## Resolving `META`, `INFO`, and `RESOURCE` references

The JSON export may reference values using `META`, `INFO`, or `RESOURCE` as the top-level key. You can use the `references` field in the JSON export to find the value for such references (e.g. `META.tenant.domain`, `RESOURCE.my_resource`, etc). The` references` field acts as a key-value dictionary of references used in the story, where the key is the fully-qualified reference as it appears in the story.

**IMPORTANT**: Note that for the references keyed with `RESOURCE`, the corresponding value is the **ID** of that resource, **NOT** the value of the resource.

If you cannot find a value for a given reference, or the `references` field does not exist in the JSON export, add the missing references to your migration report as something that requires human input.

## Send to Story settings

Inspect the story-level `send_to_story_enabled`, `entry_agent_guid`, `exit_agent_guids`, and `parent_only_send_to_story` properties of the JSON export.

When `send_to_story_enabled` is `true`, you must expose the migrated workflow as a connector. Use `entry_agent_guid` to identify the Tines action whose corresponding workflow step should begin the connector-facing workflow, and use `exit_agent_guids` to identify the corresponding workflow output steps that end it. Configure the connector entry with `route_type = "api"` and `route_auth = "connector"`, add an `api.json` contract for its request and response, and set `output = true` on the exit steps that return the response.

Handle `parent_only_send_to_story` as follows:

- **`true`** — expose only the connector entry. Do not give it public `external_id` access; set `route_auth = "connector"`.
- **`false`** — create two entry steps because one step cannot have multiple `route_auth` values. Give each entry its own route, but preserve the same request handling and downstream workflow behavior:
  - A connector entry with `route_auth = "connector"`.
  - A public API entry with `route_auth = "external_id"`.

## How to read the "Build" column

- **Rule** — fixed template, build it the same way every time.
- **Rule + AI** — fixed template, but you fill in the formula/code/values.
- **Decision** — don't build it; it's a product call (usually out of scope).

### 🎨 Match node colors to the Tines action colors

Tines action colors are determined by the action _type_. When you build the corresponding step in 3B, **set the node's color according to the source action type** using the map below. This keeps the rebuilt workflow visually legible and lets the user map a 3B step back to its original action at a glance.

| Tines color | Tines action type(s)                                            | Closest 3B color |
| ----------- | --------------------------------------------------------------- | ---------------- |
| **Indigo**  | case, form/page, group, record, run script, send to story, tool | purple           |
| **Blue**    | httpRequest, grpcRequest, mcpRequest, integrationProduct        | sky              |
| **Green**   | trigger (condition step)                                        | green            |
| **Mint**    | webhook                                                         | teal             |
| **Orange**  | eventTransformation                                             | orange           |
| **Magenta** | email                                                           | pink             |
| **Red**     | imap                                                            | red              |
| **Gold**    | llm                                                             | orange           |
| **Grey**    | groupInput, groupOutput                                         | (no equivalent)  |

- Where a single Tines action maps to multiple 3B steps (e.g. fan-out → loop, Implode → SQLite join), give the related steps the same color so the group stays identifiable.
- Color is a best-effort cosmetic aid, not a behavioral mapping.

---

## Cross-cutting (every story)

| Tines piece                          | Build in 3B                                 | How                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ------------------------------------ | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Formulas (Shiki, legacy Liquid)      | Code — there's no formula concept           | Rule + AI. Common functions map through a fixed table; nested/uncommon expressions you translate. Watch edge cases (missing fields, type coercion, dates) — they translate wrong silently.                                                                                                                                                                                                                                                                                 |
| Credentials / secrets                | Connector (the proxy injects auth by URL)   | Rule + human. The export never contains the secret, so a connector must be used to connect to the integration. **IMPORTANT:** Always use the `searchConnectors` tool find existing connectors for the relevant integration **before** prompting the user to create a new one with the `connectStepToApp` tool.                                                                                                                                                             |
| Integration templates (Slack, Okta…) | Connector + code                            | Rule + AI. Map to a connector, then generate the request code.                                                                                                                                                                                                                                                                                                                                                                                                             |
| Tines integration templates          | 'Tines Stories' connector + code            | Rule + AI. Map to a 'Tines Stories' connector, then generate the request code to perform the appropriate API interaction.                                                                                                                                                                                                                                                                                                                                                  |
| Resources                            | 'Tines Stories' connector + store in volume | Rule + AI. When a resource is referenced in a story, use the 'Tines Stories' connector to fetch the resource using the Resource API's `get` endpoint and store the resulting file in a volume. **IMPORTANT:** Fetch and read the API [documentation](https://www.tines.com/llm/docs/api/resources/get.md) before writing the API call as you may need to pass up the `typed_value` parameter. This must be done as a step **before** the resource is used in the workflow. |
| Story description / storyboard notes | README (workflow- or step-level)            | Rule. Action-specific notes go in that step's README; story-wide descriptions and storyboard annotations go in the workflow README. Don't drop them — they're the migrator's intent, and they make the rest of the migration legible.                                                                                                                                                                                                                                      |
| Monitoring / reporting / time-saved  | Mostly built in                             | Rule. Monitoring is supported today; richer reporting is in progress. Don't rebuild these per-workflow — they're platform features.                                                                                                                                                                                                                                                                                                                                        |
| Action color                         | Match the 3B node color to action _type_    | Rule. Colors aren't in the export — set them by action type per the color map (Indigo, Blue, Green, Mint, Orange, Magenta, Red, Gold, Grey). One action → many steps: share one color. Cosmetic only.                                                                                                                                                                                                                                                                      |

---

## Story structure

| Tines piece                     | Build in 3B                             | How                                                                                                                                 |
| ------------------------------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Story                           | One workflow                            | Rule. One workflow per story.                                                                                                       |
| Action (box)                    | One step folder                         | Rule. Preserve the name.                                                                                                            |
| Primary link                    | `links` in config.toml                  | Rule. `links = ["downstream"]`.                                                                                                     |
| Canvas x/y                      | Layout metadata                         | Rule. Copy positions across.                                                                                                        |
| Secondary (no-match) link       | A separate bucket a separate step reads | Rule. Non-matching items go to their own bucket — it's the one-run batch pattern, not a real per-event no-match link.               |
| Failure link                    | try/catch → failure step                | Rule. The error object flows to the failure step.                                                                                   |
| Fan-in (≥2 links into one step) | One step, runs once per incoming event  | Rule. No automatic merge — just like Tines (Combine runs twice for 2 events). To merge N events into 1, that's Implode, not fan-in. |
| Group / Group Input / Output    | Inline the inner diagram                | Rule. Group in/out become pass-through.                                                                                             |

---

## Actions

> Case, Records, and Event Transformation actions have their own section below this table.

| Tines action             | Build in 3B                                      | How                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------ | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Webhook                  | Route step                                       | Rule. Method + path from the export.                                                                                                                                                                                                                                                                                                                                                                         |
| HTTP Request             | Code fetch step                                  | Rule + AI. Map method/URL/headers/body/auth; add pagination + retry sub-templates.                                                                                                                                                                                                                                                                                                                           |
| Condition                | if-check in code                                 | Rule + AI. Use the operator table. Remember: no per-event routing — emit both buckets in one run, each downstream step reads its bucket.                                                                                                                                                                                                                                                                     |
| Run Script               | Matching 3B code step                            | Rule. Copy the language and code straight over.                                                                                                                                                                                                                                                                                                                                                              |
| Send to Story            | Workflow exposed as a connector                  | Rule + AI. Search for an existing workflow connector using the `searchConnectors` tool with the action's story name as the search term and perform the connection if one is found. If none can be found, prompt the user to set up a new workflow connector.                                                                                                                                                 |
| Send Email               | Native SMTP connector (or provider API)          | Rule + AI. Send email with the native SMTP connector, or use a provider API (SendGrid, Gmail, …). With the email-triggered step for receiving, 3B now both sends and receives email natively.                                                                                                                                                                                                                |
| AI (no tools)            | Code step + model connector                      | Rule + AI. Carry the prompt + options. Bring your own model.                                                                                                                                                                                                                                                                                                                                                 |
| AI with tools (Agent)    | Code step + model connector                      | Rule + AI. One `Run AI` step reads the transcript from stdin, calls the model, runs any tool calls (tools inline, or each as its own route step), appends the results, and links to itself until done — keep an explicit iteration cap. The **300s ceiling applies per iteration, not the whole agent** (each loop is its own execution). Only flag a single tool call/model turn that can’t finish in 300s. |
| gRPC / MCP               | MCP server connector / client library            | Rule + AI. MCP servers connect natively as connectors with full OAuth (usable in workflows and chat); 3B is also an MCP server itself (workflows, runs, spaces and chat exposed as tools for any MCP client like Claude), and you can expose your own custom MCP servers. gRPC and other protocols: rebuild with the client library.                                                                         |
| Page (results)           | `output = true` step                             | Rule + AI. A results page is an output step downstream of the data, reading stdin. A page at its own URL = storage mapping + a route step. To gate a public page behind SSO, set `route_auth = "sso"` on the route.                                                                                                                                                                                          |
| Page (form)              | Single route step: `GET` renders, `POST` handles | Rule + AI. A page with form fields and a submission button is a classic HTML form, not a React SPA. Build **one route step** that serves the form on `GET` and handles the submission on `POST` at the **same route**, then link that step to whatever runs next. Do **not** split the form and its handler across two routes.                                                                               |
| External database access | Native database connector                        | Rule + AI. Connect and query an external DB directly — no HTTP wrapper. **Postgres, MySQL and MongoDB** all connect natively today.                                                                                                                                                                                                                                                                          |
| Receive Email            | Email-triggered step                             | Rule. Set `email_address` in a step's config.toml; the inbound RFC 822 message becomes the step's input. The full deliverable address depends on operator config.                                                                                                                                                                                                                                            |

---

## Case action modes

Case actions only have a single possible mode. **IMPORTANT:** Always use the `searchConnectors` tool with the `tines` identifier to find any existing 'Tines Stories' connectors **before** prompting the user to create a new one with the `connectStepToApp` tool.

| Mode   | Build in 3B                      | How                                                                                                                                                                                                                                                                           |
| ------ | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create | 'Tines Stories' connector + code | Rule + AI. Use the 'Tines Stories' connector to call the Cases `create` endpoint. **IMPORTANT:** Fetch and read the [documentation](https://www.tines.com/llm/docs/api/cases/create.md) before writing the API call and use the action inputs to map out the request payload. |

## Record action modes

Record actions can have several modes. **IMPORTANT:** Always use the `searchConnectors` tool with the `tines` identifier to find any existing 'Tines Stories' connectors **before** prompting the user to create a new one with the `connectStepToApp` tool.

| Mode   | Build in 3B                      | How                                                                                                                                                                                                                                                                                                                                                                                         |
| ------ | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create | 'Tines Stories' connector + code | Rule + AI. Use the 'Tines Stories' connector to call the Records `create` endpoint. **IMPORTANT:** Fetch and read the API [documentation](https://www.tines.com/llm/docs/api/records/create.md) before writing the API call and use the action inputs to map out the request payload. Never send a value for the record type's default fields - `Timestamp`, `Story name`, and `Updated at` |
| Update | 'Tines Stories' connector + code | Rule + AI. Use the 'Tines Stories' connector to call the Records `update` endpoint. **IMPORTANT:** Fetch and read the API [documentation](https://www.tines.com/llm/docs/api/records/update.md) before writing the API call and use the action inputs to map out the request payload. Never send a value for the record type's default fields - `Timestamp`, `Story name`, and `Updated at` |
| Delete | 'Tines Stories' connector + code | Rule + AI. Use the 'Tines Stories' connector to call the Records `delete` endpoint. **IMPORTANT:** Fetch and read the API [documentation](https://www.tines.com/llm/docs/api/records/delete.md) before writing the API call and use the action inputs to map out the request payload.                                                                                                       |
| List   | 'Tines Stories' connector + code | Rule + AI. Use the 'Tines Stories' connector to call the Records `list` endpoint. **IMPORTANT:** Fetch and read the API [documentation](https://www.tines.com/llm/docs/api/records/list.md) before writing the API call and use the action inputs to map out the request payload.                                                                                                           |
| Get    | 'Tines Stories' connector + code | Rule + AI. Use the 'Tines Stories' connector to call the Records `get` endpoint. **IMPORTANT:** Fetch and read the API [documentation](https://www.tines.com/llm/docs/api/records/get.md) before writing the API call and use the action inputs to map out the request payload.                                                                                                             |
| Query  | 'Tines Stories' connector + code | Rule + AI. Use the 'Tines Stories' connector to call the Records `query` endpoint. **IMPORTANT:** Fetch and read the API [documentation](https://www.tines.com/llm/docs/api/records/query.md) before writing the API call and use the action inputs to map out the request payload.                                                                                                         |

## Event Transformation action modes

One Tines block, several modes — several of the hardest gaps live here.

| Mode                | Build in 3B                    | How                                                                                                                                                                |
| ------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Message only        | Code step                      | Rule + AI. Build the output object from config.                                                                                                                    |
| Extract / automatic | Code step                      | Rule + AI. Custom transform body.                                                                                                                                  |
| Explode             | One run, loop inside each step | Rule. Tines fans a 5-item list into 5 events; you keep one run — array on stdin, each step loops, emits one array. Side effects must loop; no per-event isolation. |
| Implode             | Volume join                    | Rule. **The real merge gap** — wait-for-N-then-combine, no native primitive. Write by group key, emit when size/time from config is hit.                           |
| Deduplicate         | Seen-set in a volume           | Rule. Window/TTL from config. Dedupes fine within one run; deduping across runs is the unproven part.                                                              |
| Throttle            | Queue in a volume              | Rule. Release on cron at the configured rate.                                                                                                                      |
| Delay               | Volume + cron durable wait     | Rule. **Do not** use an in-process sleep — it's capped at 300s max step time, so a 600s delay only waits ~290s. Use a durable wait.                                |

---

## Users, teams, and access

| Tines piece                        | Build in 3B            | How                                                                       |
| ---------------------------------- | ---------------------- | ------------------------------------------------------------------------- |
| Team                               | Space                  | Rule. Stories live in a team, so migrate at the team level, not per user. |
| Roles / custom roles / permissions | 3B roles / user groups | Rule. Similar but not identical — map with care.                          |
