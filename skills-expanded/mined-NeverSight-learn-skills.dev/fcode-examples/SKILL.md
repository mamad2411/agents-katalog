---
name: fcode-examples
description: Reference implementations for Factorial Code — a complete marketplace payroll integration (outbound sync with file-export and API-push delivery flavors), a multi-process custom app lifecycle (multi-step setup form, webhook + schedule install, polling, uninstall), and utility processes (CSV export with signed URL + email, XML enrichment from an uploaded file). Use when building a Factorial Code (fcode) integration, custom app, or automation end to end and you want a proven, working pattern to adapt — read the matching reference before writing code.
license: MIT
metadata:
  category: factorial-code
---

# Factorial Code — reference implementations

Worked, production-shaped examples of complete Factorial Code apps. Each
reference in `references/` walks through one real sample: its architecture,
the key code, and how to adapt it. They complement the rule-focused skills
(`fcode-core-concepts`, `fcode-javascript`/`fcode-python`, `fcode-json-schema`,
`fcode-forms`, `fcode-cli`): those tell you *how to write fcode code*, this one
shows *what a finished app looks like*.

**Adapt, don't paste.** These are patterns to rebuild for the user's actual
vendor/requirements — rename slugs, variables, and mappings; drop what the use
case doesn't need.

## Which reference to read

| You are building… | Read |
|---|---|
| A marketplace integration that delivers Factorial data (payroll, leaves, …) to an external system | [`references/integration-acme.md`](references/integration-acme.md) |
| A custom app with install/uninstall lifecycle: setup form, webhooks, schedules | [`references/custom-app-linear.md`](references/custom-app-linear.md) |
| A one-shot automation: export/report generation, file processing | [`references/utility-processes.md`](references/utility-processes.md) |

## Pattern index

Where to find a specific pattern, regardless of which app you build:

| Pattern | Reference |
|---|---|
| Extending the `outbound-sync` base class (`OutboundSync`) | integration-acme |
| Per-item API push vs aggregate-to-file delivery | integration-acme |
| Reporting per-item sync status (`success` / `invalid` / `failed`) | integration-acme |
| Webhook entry point + challenge validation | integration-acme, custom-app-linear |
| Activating webhook / form triggers (and marketplace `appRole`) in `metadata.json` | integration-acme, custom-app-linear |
| Multi-step setup form (`nextProcessId` chaining) | custom-app-linear |
| Dynamic form dropdowns via `preRenderProcess` + `#/variables` | custom-app-linear |
| Creating webhooks + schedules at install, recording them for uninstall | custom-app-linear |
| Polling with a datastore cursor + idempotency (dedup map) | custom-app-linear |
| Best-effort uninstall / teardown | custom-app-linear |
| Storage upload + signed download URL + email with `fcode.sendMail` | utility-processes |
| Reading a form-uploaded file from Storage | utility-processes |
| Calling the Factorial API SDK (`factorial-sdk` module) | all three |

## The base workspaces (always present — never recreate)

Every fcode App workspace inherits shared modules from the base apps. Import
them with `fcode.import(...)` / `fcode.import_module(...)`; do **not**
reimplement them:

| Module | From | Provides |
|---|---|---|
| `factorial-sdk` | base-app | `createFactorialClient()` — authenticated `@factorialco/api-client` / `factorial-api-client` instance |
| `factorial-utils` | base-app | `checkWebhookChallenge()`, `getCompanyId()`, `setupWebhook()`, `deleteWebhookSubscription()` |
| `fcode-forms` | base-app | Form-schema builders: `selectField()`, `toOptions()`, … |
| `mail-helper` | base-app | `brandedHtml()` for styled email bodies |
| `error-handler` | base-app | Shared error handling |
| `outbound-sync` | base-integration-app | `OutboundSync` base class for marketplace syncs |

Integration apps inherit base-integration-app (which inherits base-app);
custom apps inherit base-app directly.

## Language variants

Every sample exists in JavaScript (Node.js v22) and Python (3.13) with
identical structure and behavior. References show JavaScript; the Python
variant differs only in idiom:

| JavaScript | Python |
|---|---|
| `processes/<slug>/index.js` | `processes/<slug>/main.py` |
| `fcode.import("slug")` | `fcode.import_module("slug")` |
| `fcode.sendMail(...)` | `fcode.send_mail(...)` |
| `module.exports = { main }` | top-level `def main():` |
| camelCase helpers | snake_case helpers |

