---
name: auto-e2e
description: record, replay, store login-state credentials, bind aliases, or run manual browser workflows as reusable single-file playwright scripts. use when the user invokes /auto-e2e or /aee with a url for step-by-step browser recording, /auto-e2e replay or /aee replay to verify against a prior record or inline json, /auto-e2e alias or /aee alias to bind a trigger word to an existing script, or /auto-e2e storage or /aee storage to capture or extend a named storage-state file under auto-e2e/.auth. keep an editable step queue, support explicit variables in one params object, and save outputs under the agent workspace auto-e2e folder.
---

# Auto E2E

## Version

Current skill version: `1.7.0`.

For every future edit to this skill, bump the semantic version and update both:
- `VERSION`
- `CHANGELOG.md`

Use this bump policy:
- patch: wording fixes, clarification, non-behavioral instruction tweaks
- minor: backward-compatible new capabilities, flags, or output files
- major: breaking changes to trigger shape, generated script contract, save paths, or runtime expectations

Read these references when needed:
- [references/recording-rules.md](references/recording-rules.md) for the session workflow, queue handling, record mode, replay mode, alias parsing, alias execution, runtime option parsing, and output contract.
- [references/replay.md](references/replay.md) for replay matching, direct replay JSON parsing, expected-outcome checking, and mismatch handling.
- [references/variables.md](references/variables.md) for explicit variable detection and parameter generation.
- [references/aliases.md](references/aliases.md) for alias binding, alias storage in package.json, ambiguity handling, and direct alias invocation.
- [references/browser-runtime.md](references/browser-runtime.md) for profile modes, storage-state reuse, optional storage-state initialization when the user explicitly asks for it, captured-credential defaults, incognito behavior, headless handling, and generated CLI contract.
- [references/storage-states.md](references/storage-states.md) for dedicated `/aee storage ...` capture flows, reset or append handling, `.auth` save rules, and named credential metadata.
- [references/versioning.md](references/versioning.md) for semantic-version maintenance rules.
- [assets/package.json](assets/package.json) for the default workspace package file that must exist beside generated scripts and hold alias metadata.

## Session workflow

1. Start recording when the user says `/auto-e2e <url>` or `/aee <url>` or otherwise clearly asks to begin an auto-e2e recording for a specific page.
   - Also recognize dedicated storage capture when the user says `/auto-e2e storage <name> <url>` or `/aee storage <name> <url>`.
2. Detect optional flags and browser runtime preferences from the same start message.
   - If the user includes `record`, enable record mode for this session.
   - Also extract browser runtime preferences when the user explicitly asks to:
     - reuse a profile;
     - reuse login state;
     - initialize a named login-state file when the user explicitly asks to create one if missing;
     - use incognito mode;
     - use headless mode;
     - keep headed mode.
   - Examples that should enable record mode:
     - `/auto-e2e https://example.com record`
     - `/auto-e2e record https://example.com`
     - `/aee https://example.com record`
   - Examples that should set runtime behavior:
     - `/aee https://example.com 用隐身模式`
     - `/aee https://example.com 复用 profile admin`
     - `/aee https://example.com 复用登录态 auth/user.json`
     - `/aee https://example.com 复用登录态 user1，不存在就新建`
     - `/aee https://example.com headless`
     - `/aee storage user1 https://example.com/login`
     - `/aee storage user1 append https://example-b.com/login`
3. Also recognize replay mode when the user says `/auto-e2e replay <query>` or `/aee replay <query>`, and also support `/auto-e2e replay { ...json... }` or `/aee replay { ...json... }`.
   - If the replay argument is ordinary text, search `auto-e2e/records/` for the best matching prior record based on the natural-language query.
   - If the replay argument is an inline JSON object, parse and validate it directly, use it as the replay baseline, and do not search `auto-e2e/records/`.
   - For direct JSON replay, require at least `targetUrl` as a non-empty string and `messages` as a non-empty array.
   - If one stored record is a clear best match, load it, open its `targetUrl`, and tell the user which record is being replayed.
   - If there is significant ambiguity between multiple strong stored matches, show the top few likely records and ask the user to choose before proceeding.
   - If the inline JSON is malformed or missing required fields, stop and ask the user to fix it instead of guessing.
4. Also recognize alias binding mode when the user says `/auto-e2e alias <alias-term> <script-query>` or `/aee alias <alias-term> <script-query>`.
   - Treat the alias term as the trigger word to bind.
   - Treat the remaining text as a natural-language description of the target script.
   - Search existing `.mjs` files under `auto-e2e/` and use related records under `auto-e2e/records/` as extra hints.
   - If one script is a clear best match, bind the alias immediately.
   - If there is significant ambiguity or multiple strong matches, ask the user to confirm the intended script before writing the alias.
5. Also recognize direct alias invocation when the user says `/auto-e2e <alias-term> ...` or `/aee <alias-term> ...` and the second token is not a URL, `replay`, or `alias`.
   - Load alias definitions from `auto-e2e/package.json`.
   - If the alias exists, resolve it to the stored script file and treat the remaining text as the current execution request and variable information.
   - When parsing the trailing text, separate business variables from browser runtime preferences instead of mixing them together.
   - Treat phrases like `用隐身模式`, `复用 profile admin`, `复用登录态 auto-e2e/.auth/admin.json`, `无头模式`, `有头模式`, `headless`, and `headed` as runtime preferences that belong under `params.browserRuntime`.
   - Treat phrases like `标题是新品提卡`, `金额 100`, or `用户名是张三` as business variables that belong at the top level of the single `params` object.
   - If the alias does not exist, say so clearly instead of guessing.
6. Maintain session state in memory for the current conversation:
   - `mode` as `record`, `replay`, `alias-bind`, `alias-run`, or `storage-capture`
   - `targetUrl`
   - `stepQueue[]` in order
   - `variables[]` with `name`, `description`, `sampleValue`, and optional `defaultValue` only when the user explicitly asks for one
   - `returnSpec` if the user asks to return JSON data at the end
   - `recordConversation` boolean
   - `conversationLog[]` when record mode is enabled
   - `scriptBasename` to be decided only when recording ends
   - `browserRuntime` with `profileMode`, optional `profileDir`, optional `storageStatePath`, optional `storageStateName`, optional `initializeStorageStateIfMissing`, and `headless`
   - `matchedRecord` when replay mode is enabled, whether loaded from a stored record file or from an inline replay JSON payload
   - `matchedScript` when alias binding or alias run is enabled
   - `aliasTerm` when alias binding or alias run is enabled
   - `replayCursor` for the current expected step index when replaying against a prior record
7. If record mode is enabled, append every recording-session user message and every agent reply to `conversationLog[]` using the raw original text. Do not summarize or normalize the message text in the saved record.
8. Interpret each later user message as one step unless the message is clearly a control message such as undo, cancel the last step, finish, abort, or replay confirmation.
9. Execute the step in the open browser first, then record the canonical script version of the step into `stepQueue`.
10. If the user asks to undo or cancel the last step, remove only the last recorded item from `stepQueue`. Do not change the browser. The user is responsible for restoring the page state manually.
11. In replay mode, after each executed step, compare the current outcome against the most relevant expected assistant reply from the matched record or inline replay payload.
   - If the current outcome is semantically consistent with the prior expected result, continue and advance `replayCursor`.
   - If the current outcome is inconsistent with the prior expected result, pause immediately and ask the user whether to continue, adjust the step, or stop.
12. In alias-run mode, use the matched script and its known variable names or metadata as guidance for mapping the user's trailing natural language into the single `params` object.
   - If the intended param mapping is clear, proceed.
   - Keep business variables at the top level of `params` and keep runtime controls under `params.browserRuntime`.
   - Example: `/aee 提卡 标题是双十一活动，金额 100，用隐身模式，无头运行` should map to `{ "cardTitle": "双十一活动", "amount": 100, "browserRuntime": { "profileMode": "incognito", "headless": true } }` when the bound script expects `cardTitle` and `amount`.
   - If one or more variables remain ambiguous, ask the user only about the missing or conflicting fields.
13. When the user ends ordinary recording or replay re-recording, generate the final files inside the agent workspace `auto-e2e/` directory:
   - `auto-e2e/package.json`
   - `auto-e2e/<content-summary-name>.mjs`
   - `auto-e2e/records/<content-summary-name>.json` only when `recordConversation` is true
14. When the user ends storage-capture mode, do not generate a workflow script. Save only the real storage state under `auto-e2e/.auth/<name>.json`, plus package metadata when applicable.
15. After alias binding, persist the alias metadata into `auto-e2e/package.json` under `autoE2E.aliases`.
16. Generate script runtime helpers so the saved Playwright script supports the same browser runtime options through the single `params` object and through CLI JSON input.
17. If the workflow was recorded while explicitly using a storage-state credential, make that credential the generated script default unless the runtime caller overrides it.
18. After saving, clean up the live recording environment for this session. At minimum, close any page, browser context, or browser instance that was opened for the live recording, replay, alias-run, or storage-capture run, unless the user explicitly asks to keep it open for more steps.
19. After cleanup, clear the in-memory session state for this run so stale `stepQueue`, `conversationLog`, replay state, alias state, storage-capture state, or runtime preferences do not leak into the next run.
20. After saving and cleanup, return a concise summary including the skill version, mode, output path, chosen script filename when present, whether a record JSON was written, whether an alias was written, whether a storage credential was written, required variables, browser runtime defaults, and how to run it when a script was generated.

## Recording rules

- Treat the user's message as a browser action only when it clearly describes an intended action on the current page.
- Supported first-version actions: click, hover, fill or clear inputs, select options, check or uncheck controls, keyboard actions including Enter, explicit waits for visible or hidden elements, and final data extraction for JSON output.
- Prefer resilient locators in this order: `getByRole`, `getByLabel`, `getByPlaceholder`, `getByText`, then `locator(...)` only as a fallback.
- Keep both a human-readable description and the exact generated Playwright code for each queued step, but the user does not need to see the code unless helpful.
- After each mutating step, insert the default settle behavior:
  1. wait until there are no network requests if possible;
  2. then wait one additional second.
- Implement settle behavior in generated code with a helper that gracefully falls back if `networkidle` never arrives.
- Do not record pure conversation, clarifications, or status acknowledgements as browser steps.
- In record mode, still save those non-step user and agent messages into `conversationLog[]`; only exclude browser-internal state dumps or tool traces.
- In replay mode, use the matched record only as guidance and a verification baseline. The newly generated script must reflect what happened in the current run, not blindly copy the old steps if the user intentionally changed them.
- In alias-run mode, do not silently invent script bindings or variable meanings. Resolve through stored alias metadata first, then ask a narrow follow-up only when required.
- When runtime preferences are not specified, default to `incognito` behavior with `headless: false` so live recording remains visible to the user unless they explicitly ask otherwise.
- When a saved script came from a run that explicitly used `storageState`, let that recorded credential become the script default runtime unless the caller overrides it.

## Variable handling

Only create variables when the user explicitly marks content as variable or clearly says it should become an argument. Examples:
- “这个邮箱是变量，变量名 email，当前值是 demo@example.com”
- “把收货人当成变量 recipientName，录制时先填 张三”
- “这一步里的搜索词后续会变化，提成参数 searchKeyword”

For variable rules and default-value behavior, follow [references/variables.md](references/variables.md).

## Output contract

Generate exactly one single-file ESM Playwright script that can be run by Node.

Requirements:
- Save the script under `auto-e2e/<content-summary-name>.mjs`.
- Choose `<content-summary-name>` by summarizing the recorded task in concise english kebab-case.
- Create or update `auto-e2e/package.json` if it does not already exist.
- Ensure the saved script uses Playwright directly, not `@playwright/test`.
- Default export exactly one async function receiving one object argument:
```js
export default async function run(params = {}) {
```
- Support CLI execution in the same file using a shebang and a direct invocation path that:
  - accepts exactly one JSON string argument;
  - parses it into the same `params` object;
  - prints the JSON return value to stdout.
- The CLI-facing JSON may include both business variables and browser runtime keys. Keep everything in the same top-level object to minimize cognitive load.
- Use `browserRuntime` inside `params` for runtime-only controls such as profile mode, storage-state path, profile directory, and headless override.
- Include helper logic to launch Playwright according to `browserRuntime` and to always close the browser or context in `finally`.
- If the user requested a JSON return payload, return a valid JSON-serializable object.
- If the user did not request a JSON payload, still return a small valid object such as:
```json
{ "success": true, "script": "create-card.mjs" }
```

## Default workspace package file

If `auto-e2e/package.json` is missing, create it based on [assets/package.json](assets/package.json).
That package file must make `node auto-e2e/<script>.mjs` workable after dependency install and must preserve alias metadata under `autoE2E.aliases`.

## Response style while recording

During live recording or replay:
- confirm what action was executed;
- mention whether it was appended, removed, or verified in the queue;
- when relevant, mention variable extraction decisions;
- when relevant, mention the active browser runtime mode if the user changed it;
- keep the reply short and operational.
