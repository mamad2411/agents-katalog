---
name: fcode-javascript
description: Write JavaScript (Node.js v22) for Factorial Code processes and modules — the async main() entry point with module.exports = { main }, fcode.context.parameters, fcode.import(), datastore/storage/env helpers, auto-installed dependencies, and return-value formats. Use when creating or editing .js process or module code for Factorial Code (fcode).
license: MIT
metadata:
  category: factorial-code
---

# Factorial Code — JavaScript

Guidelines for writing JavaScript that runs on Factorial Code. Runtime is
**Node.js v22**. For the platform model (processes, modules, datastore) see
`fcode-core-concepts`.

| Aspect | Guideline |
|---|---|
| Runtime | Node.js v22 |
| Process entry file | `index.js` |
| Entry point | `async function main()` |
| Export (required) | `module.exports = { main }` |
| Parameters | `fcode.context.parameters` |
| Variables | `process.env.X` or `fcode.env.X` |
| Import a module | `fcode.import("module-slug")` |

## Gotchas

- **Always export** `main`: `module.exports = { main }`. Without it the process
  won't run.
- **Never call `main()` yourself** — Factorial Code invokes it.
- **`fcode.import()` names must be hardcoded string literals**, never variables:
  `fcode.import("shopify-client")` ✅, `fcode.import(name)` ❌.
- **Datastore stores only strings/numbers** — `JSON.stringify` objects before
  `set`, parse after `get`.
- Use `async/await` for all async work; wrap the main flow in `try/catch`, log
  the caught error with context via `fcode-logs` (see Logging), and throw
  actionable errors. Use `const`/`let`, never `var`.
- Never hardcode or log secrets — read them from `process.env`.

## Process template

```javascript
async function main() {
  const { parameters } = fcode.context;

  // Your code here

  return { message: "Success!" };
}

module.exports = { main };
```

## Helpers

```javascript
// Execution / process / schedule metadata
const { id, comment } = fcode.execution;
const { id: processId, name: processName } = fcode.execution.process;
const { id: scheduleId } = fcode.execution.schedule; // when run from a schedule
const timezone = fcode.execution.timezone;

// Environment variables (secrets/config)
const apiKey = process.env.API_KEY; // or fcode.env.API_KEY

// Import a Factorial Code module (hardcoded name only)
const { myFunc } = fcode.import("module-name");
const { myFunc: v1 } = fcode.import("module-name", "v1.0"); // pinned version

// Run another process
await fcode.processes.run("process-identifier", options);
```

## Logging

Log through the shared `fcode-logs` module — level-gated logging inherited by
every workspace. It reads the `LOG_LEVEL` team variable
(`debug | info | warn | error`, default `info`) and forwards to the matching
`console.*`, so call sites read like bare `console` calls:

```javascript
const log = fcode.import("fcode-logs");

log.info("sync started", { processSlug }); // console.log  when LOG_LEVEL ≤ info
log.debug({ requestPayload });              // console.debug only when LOG_LEVEL=debug
log.warn("token missing — skipping");       // console.warn  when LOG_LEVEL ≤ warn
log.error("sync failed", err.message);       // console.error — always emitted
```

**Be verbose.** Log the start/end of the main flow, every external call, and each
major decision at `info`; dump payloads and intermediate state at `debug` (free
in production — gated off unless `LOG_LEVEL=debug`). **Always log inside `catch`:**
record the error with context — what operation, which inputs — at `error` before
re-throwing, or at `warn` for a recovered/skipped path. `error` is always emitted.

Set `LOG_LEVEL=debug` in a local or dev workspace to trace a full run; production
stays at `info`. Never log secrets.

## Dependencies

External npm packages install automatically — just `require` them. When the
import name differs from the package name, declare it with `@add-package`:

```javascript
// @add-package axios
const axios = require("axios");
```

## Datastore & storage

```javascript
// Datastore (strings/numbers only)
await fcode.datastore.set("key", "value");
await fcode.datastore.set("key", JSON.stringify({ name: "John", age: 30 }));
const value = await fcode.datastore.get("key");
await fcode.datastore.del("key");

// Storage (files)
const fs = require("node:fs");
const path = require("node:path");
const localPath = path.join(process.env.TMP_DATA_DIR, "localfile.txt");

await fcode.storage.upload("path/myfile.txt", fs.createReadStream(localPath));
const files = await fcode.storage.list();
const stream = await fcode.storage.download("path/myfile.txt");
stream.pipe(fs.createWriteStream(localPath));
await fcode.storage.delete("path/myfile.txt");
```

**Local disk:** write temp files under `process.env.TMP_DATA_DIR`.

**Form file uploads:** a form file field (`"ui:widget": "file"`) is uploaded to
Storage before execution and arrives as an `fcode.storage://…` reference (an
array if multiple files). Strip the prefix to download:

```javascript
const { context: { parameters } } = fcode;
const stream = await fcode.storage.download(
  parameters.inputFile.replace("fcode.storage://", "")
);
```

## Variables & schedules

Read/write team variables and manage process schedules at runtime — scoped to
your own team, no API token needed (like datastore/storage):

```javascript
// Team variables (config/secrets)
await fcode.variables.set("API_KEY", "secret", { sensitive: true });
const v = await fcode.variables.get("API_KEY"); // { key, value, ... } or undefined
const all = await fcode.variables.list();
await fcode.variables.delete("API_KEY");

// Schedules (cron or one-off dateTime) for a process
const schedule = await fcode.schedule.create("my-process", {
  cron: "0 0 6 * * SUN", // or: dateTime: "2026-04-24T12:30:00.000"
  input: { parameters: { foo: "bar" } },
});
const schedules = await fcode.schedule.list({
  processId: fcode.execution.process.id,
});
await fcode.schedule.pause(schedule.id);
await fcode.schedule.resume(schedule.id);
await fcode.schedule.delete(schedule.id);
// delete every schedule for a process (pass the process UUID)
await fcode.schedule.deleteForProcess(fcode.execution.process.id);
```

`fcode.variables.set/delete` only persist server-side; they are not reflected in
`fcode.env` within the same run (`fcode.env` is a snapshot taken at start).

## Sending email

Send email with the built-in `fcode.sendMail` — no SMTP setup required. The mail
server and credentials live in the executor manager, never in your process.

```javascript
const info = await fcode.sendMail({
  to: "user@example.com", // string or string[]
  subject: "Report ready",
  text: "Plain-text body", // provide text, html, or both
  html: "<b>HTML body</b>",
});
// info => { messageId, accepted, rejected }
```

- The `From` address is fixed by the platform; a `from` you pass is ignored.
- Each execution can send up to 3 emails by default; once the limit is reached, further calls throw.
- Locally (`fcode run`) there is no manager, so the email is logged, not sent.

## Return values

```javascript
// Standard
return { message: "Success!" };

// Custom HTTP status (webhooks)
return { status: 404, body: { message: "Not found" }, headers: { "Content-Type": "application/json" } };

// Transient (not persisted in execution results)
return { transient: true, data: sensitiveData };
```
