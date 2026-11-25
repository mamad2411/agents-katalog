---
name: audit-xss
description: Audit Joomla extension output paths for reflected, stored, and DOM-based cross-site scripting. Use when reviewing browser output escaping, rich HTML filtering, or client-side DOM insertion in a Joomla extension, or when explicitly invoked for an XSS audit. For non-HTML headers, exports, logs, mail, and caches see audit-sensitive-output; for server-side execution see audit-code-execution; for SQL injection see audit-sql-filtering.
---

# Audit Joomla cross-site scripting

Audit this repository's distributed Joomla extension code for attacker-influenced data reaching a
browser execution context without protection appropriate to that exact context.

## Boundaries

This audit owns reflected, stored, and DOM-based XSS.

It does not own SQL injection — that is `audit-sql-filtering`. Injection into non-HTML output sinks
(response headers, CSV and spreadsheet exports, logs, plain-text mail, cache keys) belongs to
`audit-sensitive-output`. Server-side code execution — `eval()`, dynamic `include`, unserialisation,
callable injection — belongs to `audit-code-execution`. If you notice any of those while tracing,
note it in one line and point at the owning skill; do not expand this audit to cover them.

Do not report a merely unfiltered value. A finding requires that the value reaches a sink capable of
executing script in a browser.

## Sources and sinks

Trace values from request data, cookies, headers, routing data, form arrays, database records,
extension parameters, remote responses, and previously stored rich text.

Administrator-supplied content is not automatically trusted: account compromise and delegated
administration still make stored XSS relevant, though privilege affects severity.

Inspect PHP layouts, view templates, modules, plugins, HTML-rendered email, custom document types,
JavaScript, and API data later inserted into the DOM. Cover at least:

- HTML text and attribute output, including hand-built tags and `data-*` attributes;
- URL-valued attributes, including dangerous schemes (`javascript:`, `data:`);
- inline JavaScript, `Text::script()` strings, `$doc->addScriptOptions()` payloads, JSON embedded in
  HTML, and event-handler attributes;
- DOM sinks — `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, and jQuery HTML
  insertion — when the value is not demonstrably safe;
- intentionally allowed HTML whose allow-list permits executable tags, attributes, CSS, or URLs.

### Joomla specifics

- `$this->escape()` in a view is `htmlspecialchars` with `ENT_COMPAT` by default — it does not escape
  single quotes. In an attribute delimited by single quotes, that is a hole.
- `HTMLHelper::_('...')` output is frequently pre-escaped, frequently not. Check the specific helper
  rather than assuming.
- `InputFilter` / `$input->get($name, null, 'html')` is a filter, not an output encoder — and its
  behaviour depends on the configured Text Filters per user group. Super Users are commonly
  configured with "No Filtering".
- Escaping performed by a parent layout counts. Recognise it before reporting a child layout.

Input filtering is defence in depth, not a substitute for output encoding. Verify the protection is
correct for the destination: HTML escaping is not sufficient for JavaScript, JSON, CSS, or URL
contexts.

## Workflow

### Step 1 — Audit

Map each source-to-sink path and determine whether an attacker with the stated privileges can control
the final value. Report only exploitable or convincingly risky paths, ordered by severity:

- **CRITICAL** — stored XSS reliably executed for Super Users, or across the administrator
  application, from guest or low-privilege input.
- **HIGH** — stored XSS affecting other users, or reflected/DOM XSS requiring little user
  interaction.
- **MEDIUM** — self-XSS with a credible escalation path, administrator-only stored XSS, or an exploit
  requiring significant interaction.
- **LOW** — defence-in-depth weaknesses where executable output is plausible but not currently
  attacker-controlled.

For every finding give the source, the transformations along the way, the sink and its output
context, the attacker's prerequisites, the affected users, and a context-correct mitigation. Include
file and line references. Separate confirmed findings from items that require runtime verification.

Report and await user feedback before changing any code.

### Step 2 — Feedback round

The user is a subject matter expert and may reclassify or overrule a finding after giving more
context — an escaping layer you did not read, or a value that cannot in fact be attacker-controlled.

### Step 3 — Plan fixes

Once the user is done giving feedback, check for remaining items to fix.

If none, say so and stop.

Otherwise break the fixes into small, independently implementable plans and write them to the
`.gitignore`'d `.plans` directory, clearing any existing files there first. Then propose running
those plans in parallel via subagents, on a cheaper/faster model — the planning work is already done.

---

*Adapted for this suite from the `audit-xss` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
