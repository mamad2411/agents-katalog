---
name: audit-sensitive-output
description: Audit Joomla extension responses, logs, exports, errors, mail, and caches for injection into a downstream interpreter or disclosure of sensitive data. Covers response headers, CSV formula injection, log forging, error disclosure, mail header injection, and cache isolation. Use when reviewing non-HTML output sinks in a Joomla extension, or when explicitly invoked for this audit. Browser script execution belongs to audit-xss.
---

# Audit Joomla sensitive output and non-HTML injection

Audit non-HTML output sinks for data disclosure, injection into a downstream interpreter, and
accidental reuse of private output across users.

## Boundaries

This audit owns response headers, downloads, CSV and spreadsheet exports, logs, exceptions and error
responses, outbound mail construction, and cache isolation.

- Browser HTML and JavaScript execution belongs to `audit-xss`.
- Secret creation and cryptographic handling belong to `audit-secrets-crypto` — a secret that exists
  in the wrong form is theirs; a correctly-formed secret written into a log is this audit's.
- Object-level selection of *which* records a response contains belongs to `audit-object-access`.

Cross-reference a shared root cause rather than duplicating it.

## Sinks and checks

Trace request values, headers, database content, extension parameters, remote responses, and
exception data into:

- **HTTP headers and redirects** — reject CR/LF and control characters, construct
  `Content-Disposition` filenames safely, and keep attacker values out of security and caching
  headers.
- **CSV and spreadsheet exports** — neutralise cells beginning with a formula control character
  (`=`, `+`, `-`, `@`, tab, CR) as the target format requires, while preserving the intended data.
  Joomla components with a CSV export and a user-supplied title field are the usual case.
- **Logs and audit trails** — prevent log forging and control-character injection; keep credentials,
  tokens, session identifiers, personal data, and unbounded attacker content out of them.
- **Exceptions, debug pages, and API errors** — avoid stack traces, filesystem paths, queries,
  configuration, secrets, and oracle-like differences reaching unauthorised users. Under Joomla's
  API application an uncaught exception is rendered as JSON; check what that JSON actually contains
  when Debug is off.
- **Mail** — recipients, sender, reply-to, subject, and multipart boundaries: prevent header and
  recipient injection and unauthorised use as a relay or bulk-mail endpoint.
- **Caches** — include identity, view access level, language, and any tenant or site context in the
  cache key. A privileged response served from cache to another user is the failure mode; Joomla's
  view-level and page caching both make it easy to reach.

Recognise framework APIs that already reject unsafe headers or partition caches correctly. A value
being personal or attacker-controlled is not itself a finding — establish that the sink mishandles it
or exposes it to an unintended audience.

## Workflow

### Step 1 — Audit

Report findings ordered by severity:

- **CRITICAL** — unauthenticated disclosure of credentials or broad highly sensitive datasets, or a
  cache isolation failure exposing privileged content widely.
- **HIGH** — exploitable mail relay, persistent log or audit forgery affecting security decisions,
  sensitive cross-user cache leakage, or formula injection in a likely privileged workflow.
- **MEDIUM** — stack, query, or path disclosure; constrained personal-data leakage; header injection
  with limited impact; or formula injection requiring significant interaction.
- **LOW** — excessive but non-sensitive diagnostics, or defence-in-depth output hardening.

For each finding give the data source, the output sink and its format, the unintended interpreter or
audience, the privileges required, the impact, and a format-correct mitigation — with file and line
references. **Keep any discovered secret or personal data redacted** in the report.

Report and await user feedback. Do not change code in this step.

### Step 2 — Feedback round

The user is a subject matter expert and may reclassify or overrule a finding after giving more
context.

### Step 3 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into smaller, individually implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

---

*Adapted for this suite from the `audit-sensitive-output` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
