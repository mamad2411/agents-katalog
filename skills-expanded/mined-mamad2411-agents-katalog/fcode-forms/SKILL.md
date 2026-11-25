---
name: fcode-forms
description: Embed a Factorial Code process's input-parameter form on a webpage — the three embed methods (data attributes, Fcode.initForm, FcodeForm React component), driving behavior from the process return value (message/formErrors/redirect/jsCallback/nextProcessId), styling/themes, i18n, multi-step flows, and automatic file uploads to Storage. Use when embedding, configuring, styling, or wiring up submission callbacks for a Factorial Code (fcode) form.
license: MIT
metadata:
  category: factorial-code
---

# Factorial Code — Forms

A Factorial Code Form embeds a process's input-parameter form on any webpage.
Each submission starts a process execution with the form data, and the result is
handled in-page (messages, redirects, callbacks). For the schema itself, see
`fcode-json-schema`.

## Gotchas

- **The form *is* the process's `parametersSchema.json`** — there is no separate
  form definition. To change fields/validation/labels, edit the schema, **not**
  the embed code.
- **`team` and `process`/`processId` are both mandatory** on every embed.
- **The `Forms` flag must be enabled** — on the process Dashboard, or via
  `"form": { "enabled": true }` in the process's `metadata.json` + `fcode push`
  — or the embed won't render.
- **Never put secrets in embed code, `options`, or behaviour functions** — they
  run in the browser.
- **Form submissions run under a request timeout** (about a minute) — keep the
  synchronous process fast, or run long work asynchronously (see below).
- Prefer driving UX from the **process return value** (below); reserve
  `onSuccess`/`onError` for client-only logic.

## Enable a form

1. Create the process and define its input parameters (these become the fields).
2. Enable the `Forms` flag — either on the process Dashboard, or from the CLI
   workspace in `processes/<slug>/metadata.json`, then `fcode push`:

```json
{
  "name": "Contact request",
  "tags": [],
  "form": { "enabled": true }
}
```

For marketplace app processes, `form` also takes an optional
`"appRole"` (`INSTALL` | `SETTINGS` | `USER_FACING_FORM`) marking the
process's role in the app; add `"visibility": { "isPublic": true }` to make
the form publicly accessible. Field reference in `fcode-cli`.

Read submitted values in process code like any parameters:
`const { context: { parameters } } = fcode;`

## Embed a form

Two mandatory inputs, taken from the platform URLs:

- **`fcode-team-id`** — from `https://code.factorial.dev/platform/<fcode-team-id>`
- **`fcode-process-id`** — from `.../<fcode-team-id>/processes/<fcode-process-id>`

Load the SDK once (needed for the data-attribute and `Fcode.initForm` methods):

```html
<script defer src="https://code.factorial.dev/sdk/forms.js"></script>
```

**Method 1 — data attributes** (SDK replaces the element):

```html
<div data-fcode-form-team="<fcode-team-id>" data-fcode-form-process="<fcode-process-id>"></div>
```

**Method 2 — `Fcode.initForm`** (selector or DOM element):

```html
<div id="my-fcode-form"></div>
<script>
  Fcode.initForm("#my-fcode-form", { team: "<fcode-team-id>", process: "<fcode-process-id>" });
</script>
```

**Method 3 — `FcodeForm` React component** (React 17/18; install
`@factorialco/fcode-react-forms`):

```jsx
import FcodeForm from "@factorialco/fcode-react-forms";

const MyComponent = () => (
  <FcodeForm team={"<fcode-team-id>"} processId={"<fcode-process-id>"} />
);
```

In SSR frameworks (e.g. Next.js), import it dynamically with `ssr: false`.

## Handle submission results

Default: a loading overlay shows during execution; on success the form is
replaced with a success message, on error an error message.

**Callbacks** (same shape across methods):

```js
Fcode.initForm("#my-fcode-form", {
  team: "<fcode-team-id>",
  process: "<fcode-process-id>",
  onSuccess: (formId, processExecutionResult, formSubmittedData) => {},
  onError: (formId, error, formSubmittedData) => {},
});
```

With data attributes, point to global functions via
`data-fcode-form-on-success="HANDLER_NAME"` / `data-fcode-form-on-error="..."`.

**Drive behavior from the process return value** (no client code needed):

```js
return { message: "Thanks, <b>we received your request</b>." };            // success message (HTML allowed)
return { status: 400, body: { formErrors: {                                 // inline validation errors
  fields: { email: "Invalid email." }, global: ["A global error."] } } };
return { redirect: { url: "https://example.com", timeout: 2000 } };         // redirect after submit
return { jsCallback: `analytics.track("User Registered");` };               // run JS in the page
```

## Keep it fast, or go async

The submission waits for the process to finish, under a request timeout (about a
minute). Heavy work done inline — slow API calls, large exports, multi-record
syncs — will blow the timeout and fail the submit.

**Go async when the work can be slow:**

- **Embed `async: true`** — the submission returns `201` + an execution ID
  immediately instead of waiting for the result (see `references/advanced.md`).
- **Hand off to another process** — kick off the heavy work with
  `fcode.processes.run("process-identifier", options)` (see `fcode-javascript` /
  `fcode-python`) and return a quick acknowledgement (`message`/`redirect`)
  rather than awaiting it inline.

**Stay synchronous only when** the request is genuinely fast, or when data must
flow between steps. For passing data, don't block the submit — instead:

- **`preRenderProcess`** computes server-side `variables` before the form
  renders (see `references/advanced.md`).
- **Multi-step forms** carry state forward via `nextProcessId` + `variables`
  (below).

## Multi-step forms

Each step is its own process. Return the next process ID to advance:

```js
return { nextProcessId: "719d7c83-..." };
```

The SDK then renders the form for `nextProcessId`. Each later step receives all
previous steps' data and results in `fcode.context.parameters` under a `steps`
array. Return a `variables` node alongside `nextProcessId` to pass state forward.

## Automatic file uploads

A file field is `"type": "string"` with `"ui": { "ui:widget": "file" }`. On
submit the file is **uploaded to Storage before the process starts**, and the
parameter arrives as an `fcode.storage://…` reference (an **array** if multiple
files allowed). Strip the prefix to download:

```js
const { context: { parameters } } = fcode;
const stream = await fcode.storage.download(
  parameters.inputFile.replace("fcode.storage://", "")
);
```

Uploaded files count toward storage limits — delete them at the end of the
process if only needed transiently.

## Advanced

For styling/themes, initial/hidden values, async submission, custom headers,
API-host override, variables replacement, internationalization, client-side
behaviour functions (`onChange`, field transformers), and modal rendering, read
`references/advanced.md`.
