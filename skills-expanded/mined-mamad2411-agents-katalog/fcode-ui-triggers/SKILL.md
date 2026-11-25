---
name: fcode-ui-triggers
description: Surface a Factorial Code process as a button inside the Factorial product UI — the `uiTrigger` block in a process's metadata.json (location id, label, icon, awaitResult), what the process receives when a user clicks, the `{ data }` / `{ errors }` result envelope for synchronous triggers, form-backed triggers, i18n labels, the icon allowlist, and how Factorial's `FactorialCodeTrigger` component renders them. Use when an app process should appear as an action button on a Factorial page, or when wiring a "Triggered from Factorial UI" trigger.
license: MIT
metadata:
  category: factorial-code
---

# Factorial Code — UI triggers

A UI trigger exposes a marketplace app's process as a **button inside
Factorial** (a page header, an actions dropdown, …). Factorial pages declare
*locations*; an installed app's process claims a location, and Factorial renders
one button per claiming process. Clicking it runs the process — or opens its
form. It sits next to the webhook and form triggers in the process's
`metadata.json` (field reference in `fcode-cli`).

## Gotchas

- **Only installed marketplace apps get buttons.** Factorial lists the triggers
  of the apps the company has installed, read from their deploy workspaces. A
  process in a plain workspace never shows up, and a trigger reaches customers
  the way the rest of the app does: dev → prod → deploy through a release.
- **The location id must come from the Factorial team that owns the page.**
  Locations are declared in Factorial's code (e.g. `calendar.header.admin`), not
  on the platform. The platform accepts any non-blank `locationId` (≤ 200
  chars) — an unknown one is silently dropped from the listing, so a typo means
  "no button", not an error.
- **The location decides the contract**, not the process: which context params
  are forwarded to the process, which keys of a synchronous result reach the
  page, and whether the location is `single` (one installed app at a time).
  Ask for those three things along with the id.
- **`awaitResult` is off by default: fire-and-forget.** The click queues an
  execution and the user sees "action started"; the return value is never shown.
  Turn it on only for fast work (< 50 s) whose outcome the user must see.
- **A form-enabled process opens its form instead of running.** With
  `"form": { "enabled": true }` the button opens the form in a dialog inside
  Factorial and `awaitResult` is ignored (the console hides the switch).
- **Trigger-opened forms are not authenticated yet.** The dialog sends no
  Factorial user token, so a form behind a trigger must be public
  (`form.authMode` absent or `NONE`) or every request gets a `401`. An
  authenticated flow is a platform follow-up.
- **Never authorize on `company_id` / `triggered_from_location` in a form.**
  On the *execute* path they are injected server-side and trustworthy; on the
  *form* path they arrive as pre-filled, client-editable fields.
- **Uncaught errors show a generic message.** A throw / crash reaches the user as
  "The action could not be completed" with no detail. Return `{ errors: [...] }`
  for anything the user should read.
- **Changes take up to five minutes to appear** — Factorial caches the trigger
  listing in the browser.

## Declare a trigger

In `processes/<slug>/metadata.json`, then `fcode push` (or the **Triggered from
Factorial UI** section of the process page in the console):

```json
{
  "name": "Sync report",
  "tags": ["acme"],
  "uiTrigger": {
    "enabled": true,
    "locationId": "compensations.cycle.header",
    "label": "Sync to Acme",
    "icon": "Refresh",
    "awaitResult": true
  }
}
```

| Field | Meaning |
|---|---|
| `enabled` | Turns the trigger on. `locationId` is required when `true` |
| `locationId` | The Factorial location the button renders at, as given by the page's owning team |
| `label` | Button text. Plain text, or `fcode.i18n("key")` tokens (below) |
| `icon` | One of the allowlisted names (below); omit for a text-only button |
| `awaitResult` | `true` runs the process synchronously and shows its outcome; `false`/omitted is fire-and-forget |

`fcode pull` writes `"uiTrigger": { "enabled": false }` for every process; the
other keys only appear when set, and `awaitResult` only when `true`.

An app may declare several triggers at one location — each renders its own
button — but a location marked `single` in Factorial admits **one installed
app**: installing a second app that claims it fails with a conflict naming the
first. Don't claim a `single` location from an app meant to coexist with others.

## What the process receives

The click runs the process with `fcode.context.parameters` set to:

- the location's **forwarded context params** — e.g. the id of the record the
  page shows (`cycle_id`), exactly the keys the location allowlists;
- `company_id` — the Factorial company whose user clicked (trusted: injected
  under a shared secret, overwriting anything the browser sent);
- `triggered_from_location` — the location id (trusted, same way).

A context-less location (a header button with no record in scope) forwards no
params at all — only the two trusted keys. The clicking user's locale is passed
as the execution locale, so `fcode.i18n` in the process speaks their language
(`fcode-i18n`).

```javascript
const { company_id, triggered_from_location, cycle_id } = fcode.context.parameters;
if (!cycle_id) throw new Error("cycle_id is required");
```

## Return a result (synchronous triggers)

With `awaitResult: true` Factorial waits for the execution and reads the return
value as an envelope:

```javascript
// Success — `data` is shown to the page. Only the keys the location allowlists
// (`result_keys`) get through; anything else is dropped before reaching the browser.
return { data: { synced: 42, report_url: "https://acme.example/reports/7" } };

// Controlled error — the messages render to the user, as plain text.
return {
  errors: [{ code: "missing_mapping", message: "Map the 'Bonus' concept in Acme first." }],
};
```

- `{ data }` → a success toast; the (filtered) `data` reaches the page's
  `onSuccess` handler. Return `{ data: {} }` when there is nothing to hand back.
- `{ errors: [{ code, message }] }` → the user reads your messages. Both fields
  must be strings; entries missing either are ignored. Use it for every
  expected failure (bad configuration, vendor rejection, nothing to do).
- Anything else (no envelope, a bare `{ message }`) still counts as **success**
  with an empty result — the execution finished.
- A throw, a platform `4xx`, or exceeding the synchronous budget (about 50 s;
  the execution may still finish in the background) → a generic error the user
  can't act on.

With `awaitResult` off the return value is only visible in the execution log;
long work belongs there, or behind `fcode.processes.run(...)` from a quick
synchronous trigger (see `fcode-javascript` / `fcode-python`).

## Form-backed triggers

Enable the form as usual (`fcode-forms`) and the button opens it in a dialog
inside Factorial, rendered with the f0 theme, pre-filled with the forwarded
params plus `company_id` and `triggered_from_location` as default values.
Declare those keys in `parametersSchema.json` (a `hidden` widget) if the process
needs them — and remember they are client-editable there. The submission result
follows the form conventions (`message`, `formErrors`, `nextProcessId`, …); a
`{ data }` envelope in the final step is handed to the page like a synchronous
trigger's.

```json
{
  "name": "Export cycle",
  "form": { "enabled": true },
  "uiTrigger": { "enabled": true, "locationId": "compensations.cycle.header", "label": "Export…", "icon": "Download" }
}
```

Keep the form public for now (no `authMode`, or `"authMode": "NONE"`) — see
the gotcha above.

## Labels and i18n

`label` may embed `fcode.i18n("key")` tokens — the same tokens a form schema
uses — resolved with each user's locale from the workspace's locale files, with
the primary-locale fallback and never a blank label (model, files and syntax in
`fcode-i18n`):

```json
"uiTrigger": { "enabled": true, "locationId": "calendar.header.admin", "label": "fcode.i18n(\"acme.sync.button\")" }
```

## Icons

Factorial renders only these names (case-insensitive); anything else falls
back to a text-only button, and the console shows the same list as a picker:

`Bell`, `Calendar`, `Chart`, `Document`, `Download`, `ExternalLink`, `Globe`,
`Graph`, `Link`, `Play`, `Refresh`, `Send`, `Settings`, `Sparkles`, `Star`,
`Upload`.

## How Factorial renders them (for Factorial engineers)

The Factorial side is generic — no per-app code. In the `factorial` monolith:

- A location is a YAML file under a component's `app/fcode_locations/`
  (`id`, optional `resource` + `param_key` for the record in scope,
  `forward_params`, `result_keys`, `single`, `legacy_ui`), validated by a CI
  spec. `calendar/header_admin.yml` is the reference.
- The page renders
  `<FactorialCodeTrigger locationId="…" params={{ cycle_id }} onSuccess onError />`
  from `frontend/src/modules/factorialCode/components/FactorialCodeTrigger`. It
  draws one button per claiming trigger (F0 `outline` button, or the legacy
  design-system button for `legacy_ui` locations), renders nothing while loading
  or when no installed app claims the location, and owns the form dialog. The
  underlying hooks (`useFactorialCodeTriggers` for the listing,
  `useFactorialCodeTriggerActivation` for the click) are exported for
  data-driven hosts such as dropdown menus.
- Activation goes through `FactorialCode::Interactors::ActivateUiTrigger`
  (authorizes with a policy-scoped read of the location's `resource`, forwards
  only `forward_params`, filters `data` to `result_keys`) and is proxied to the
  Factorial Code dashboard, which resolves the trigger live and runs the
  process. Everything is gated by the Factorial Code feature flag.

App developers don't touch any of this; they need the location's id and
contract from the team that owns the page.

## Checklist before shipping

1. Location id, forwarded params, `result_keys` and `single`-ness confirmed with
   the owning Factorial team.
2. `awaitResult` on only for fast, user-visible outcomes; the process returns
   `{ data }` / `{ errors }`.
3. A form-backed trigger's form is public and declares the pre-filled keys it
   reads.
4. Tested from a dev installation in Factorial, then promoted to `prod-` and
   released so the deploy workspaces pick it up (`fcode-release`, `fcode-ama`).
