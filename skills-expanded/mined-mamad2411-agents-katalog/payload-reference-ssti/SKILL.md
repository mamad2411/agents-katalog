---
name: payload-reference-ssti
description: Server-Side Template Injection reference framework — defensive taxonomy organized by template engine (Jinja2, Twig, Freemarker, Velocity, ERB, EJS, Pug, Smarty, Mustache/Handlebars), safe canary strategy via polyglot inert markers, engine fingerprinting through syntax differentials, and sandbox-escape awareness with strict no-code-execution boundary.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: conditional
evidence-outputs: [reference-notes, validation-plan, safe-canary-log, redaction-decision]
---

# Payload Reference SSTI

Use this skill as a defensive reference framework for Server-Side Template Injection assessment. Organize payload knowledge by template engine family (Python/Jinja2, PHP/Twig, Java/Freemarker/Velocity, Ruby/ERB, Node.js/EJS/Pug, .NET/Razor, Go templates), engine fingerprinting through syntax differentials, and the sandbox-escape landscape. Every payload discussion maps to a safe canary strategy — confirming template injection via inert marker evaluation (e.g., `{{7*7}}` evaluating to `49`) without escalating to code execution, object traversal, or file access. This skill is a reference and triage aid. It never provides code-execution runbooks. All active validation routes through `pentest_agent_execute_tool` with authorization, scope, and approval gates.

## Required inputs

- Template context: where user input is rendered (email template, web page, PDF report, notification body, error page, CSV export, or configuration file template).
- Technology hints: web framework (Flask, Django, Spring, Express, Rails, Laravel), template engine name from documentation or error messages, or template syntax observed in legitimate output.
- Affected parameter, input format (form field, JSON value, URL parameter, HTTP header, file upload metadata), and any observed input validation.
- Target and scope file when any live system is mentioned.
- Authorization cache before target contact.
- Desired output: validation plan, safe canary design, engine fingerprint, triage decision, or redaction guidance.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` when target context exists.
3. `pentest_agent_validate_target` before any live URL, host, API, or account is contacted.
4. `pentest_agent_check_authorization` before active validation.
5. `pentest_agent_build_command` → `pentest_agent_execute_tool` for all active checks.
6. `pentest_agent_append_evidence` for redacted notes.

## Defensive payload taxonomy

### Category 1 — safe polyglot detection (inert markers)

Goal: confirm template injection using inert mathematical expressions that evaluate harmlessly. The expression result proves injection without any risk.

**Universal polyglot canary**: `${{<%[%'"}}%\.` — this string contains syntax fragments from multiple template engines. If any fragment causes a parsing error, the engine type is partially revealed through the error message. If the entire string is reflected without error, the engine may be Mustache/Handlebars (logic-less, ignores unknown syntax).

**Mathematical canaries** (safe — arithmetic only):
- `{{7*7}}` — Jinja2, Twig, Liquid, Nunjucks: evaluates to `49` if injected into expression context.
- `${7*7}` — Freemarker, Velocity, Spring EL: evaluates to `49`.
- `<%= 7*7 %>` — ERB, EJS: evaluates to `49`.
- `#{7*7}` — Thymeleaf, older JSP EL: evaluates to `49`.
- `{{= 7*7 }}` — Mustache (some implementations): may compute.
- `{% print(7*7) %}` — Jinja2 statement tag: outputs `49`.

**Safe string concatenation canaries**:
- Jinja2: `{{ 'hell' ~ 'o' }}` → `hello`.
- Freemarker: `${'hel' + 'lo'}` → `hello`.
- ERB: `<%= 'hel' + 'lo' %>` → `hello`.

**Safe object introspection canaries** (confirm template context without sensitive data):
- Jinja2: `{{ self.__class__.__name__ }}` — returns the current template class name (e.g., `Template`), confirming access to the Python object model without executing code.
- Freemarker: `${.data_model.key_set()}` — returns the keys available in the data model, which can confirm template context without executing Java methods.
- Limit introspection to class/module names only. Do not traverse to `__subclasses__`, `__globals__`, `__builtins__`, or any method that grants access to executable functions.

### Category 2 — engine fingerprinting through syntax differentials

Goal: identify the specific template engine using syntax differences without triggering code execution.

**Tag syntax identification**:
- `{{ ... }}` — Jinja2, Twig, Liquid, Nunjucks, Mustache (variable), Handlebars, AngularJS, Vue.js (client-side — not SSTI).
- `${ ... }` — Freemarker, Velocity, Spring EL, Thymeleaf (inline).
- `<% ... %>` / `<%= ... %>` — ERB (Ruby), EJS (Node.js), ASP.NET Web Forms.
- `{% ... %}` — Jinja2 (statement), Twig (statement), Liquid (statement).
- `{# ... #}` — Jinja2 (comment), Twig (comment).
- `#{}` — JSP EL (older), Thymeleaf.
- `@{}` — Thymeleaf (link expression).
- `*{}` — Thymeleaf (selection expression).
- `~{}` — Thymeleaf (fragment expression).
- `{!! ... !!}` — Blade (Laravel, unescaped output).
- `{{{{ ... }}}}` — Mustache (raw variable).

**Error-based fingerprinting**: inject an intentionally malformed expression for each engine and observe the error message. Jinja2 errors mention `jinja2`, `TemplateSyntaxError`, or `UndefinedError`. Twig errors mention `Twig`, `Twig_Error`. Freemarker errors mention `freemarker.core`, `InvalidReferenceException`. ERB errors are Ruby `SyntaxError` or `NameError`. These errors are safe to trigger — they do not execute code and reveal the engine for defense assessment.

**Comment syntax identification**:
- Jinja2/Twig: `{# comment #}` — if the text `comment` disappears from the output, Jinja2 or Twig is confirmed.
- Freemarker: `<#-- comment -->` — HTML-comment-style template comment.
- ERB: `<%# comment %>` — Ruby-style comment.
- Velocity: `#* comment *#` or `## single line`.

### Category 3 — engine-specific safe canaries

**Jinja2 (Python)**:
- Safe canary (mathematical): `{{ 7*7 }}` → `49`. Simplest and most reliable.
- Safe canary (string): `{{ 'hello'.upper() }}` → `HELLO`. Confirms method invocation on safe strings.
- Safe introspection (do not go deeper): `{{ config.__class__.__name__ }}` → confirms access to config object's class. Stop here — do not traverse to `__subclasses__` or `__globals__`.
- Blocked path: `{{ ''.__class__.__mro__[1].__subclasses__() }}` → traverses to Python subclass tree. This is the entry point for code execution. Reference for defense only; never execute in active validation.

**Twig (PHP)**:
- Safe canary: `{{ 7*7 }}` → `49`.
- Safe canary: `{{ 'hello'|upper }}` → `HELLO` (Twig uses filters with pipe syntax).
- PHP version: `{{ constant('PHP_VERSION') }}` — returns PHP version string. Safe information disclosure.
- Blocked path: `{{ _self.env.registerUndefinedFilterCallback('exec') }}` — registers a callback for code execution. Reference only.

**Freemarker (Java)**:
- Safe canary: `${7*7}` → `49`.
- Safe introspection: `${.data_model.key_set()}` → lists template variables. May expose variable names; record this as potentially sensitive.
- Blocked path: `${"freemarker.template.utility.Execute".new()("id")}` → executes system command. The `Execute` class is a known Freemarker sandbox escape vector. Reference only.

**Velocity (Java)**:
- Safe canary: `#set($x = 7*7) $x` → `49`.
- Velocity has no sandbox — any accessible Java class can be invoked. This makes SSTI in Velocity inherently critical. Engine fingerprinting alone confirms a critical finding.
- Blocked path: `#set($runtime = $class.forName('java.lang.Runtime'))` — gains Runtime access. Reference only.

**ERB (Ruby)**:
- Safe canary: `<%= 7*7 %>` → `49`.
- Safe canary: `<%= 'hello'.upcase %>` → `HELLO`.
- Safe introspection: `<%= self.class.name %>` → returns the current binding class (e.g., `ERB` or `Binding`).
- Blocked path: `<%= system('id') %>` — executes system command via Kernel#system. Reference only.

**EJS (Node.js)**:
- Safe canary: `<%= 7*7 %>` → `49`.
- Safe introspection: `<%= Object.keys(process) %>` — lists process object keys (process version, environment variable names, not values). More revealing than needed; prefer the mathematical canary.
- Blocked path: `<%= process.mainModule.require('child_process').execSync('id') %>` — code execution via require. Reference only.

**Pug (Node.js)**:
- Safe canary: `#{7*7}` → `49`.
- Blocked path: `#{function(){return require('child_process').execSync('id')}()}` — inline function with code execution. Reference only.

**Smarty (PHP)**:
- Safe canary: `{$smarty.now}` → current timestamp. Safe, reveals Smarty engine.
- Safe canary: `{7*7}` → `49` (if math enabled).
- Blocked path: `{system('id')}` — if `{php}` tags are enabled, direct PHP execution. Reference only.

**Mustache/Handlebars (logic-less)**:
- Safe canary: `{{7*7}}` → `{{7*7}}` (reflected, not evaluated). Logic-less engines do not evaluate expressions — they only substitute variables. Confirms the engine is logic-less; SSTI in Mustache/Handlebars typically cannot escalate beyond variable access.
- Variable access: `{{admin}}` or `{{config}}` — may expose template variables. Record variable names, not values.

### Category 4 — sandbox and escape awareness (reference only)

Goal: understand sandbox escape patterns for defense assessment and patch prioritization.

**Jinja2 sandbox**: Jinja2's `SandboxedEnvironment` restricts access to attributes starting with underscores, blocks `__subclasses__`, and limits built-in function access. Without `SandboxedEnvironment`, Jinja2 templates have full Python object access. Check whether `app.jinja_env` in Flask uses `SandboxedEnvironment` — it does NOT by default.

**Freemarker sandbox**: Freemarker has an `ObjectConstructor` configuration that can be disabled. If `new()` is allowed, the `Execute` utility class becomes available. Freemarker templates should never have `new()` enabled in production.

**SSTI + file read**: many engines provide file read capabilities (Jinja2 `open()`, Freemarker `TemplateLoader`, ERB `File.read()`). File read via SSTI is a separate finding from code execution — less severe but still critical if the filesystem contains secrets.

**SSTI + SSRF hybrid**: template engines that can make HTTP requests (Freemarker `URLTool`, Jinja2 `urllib`) combined with SSTI create an SSRF vector. This is a finding on its own regardless of whether code execution is available.

## Decision points

- **Mathematical canary evaluates → confirm SSTI**: record the engine family and the canary expression used. Do not escalate beyond introspection of class/module names.
- **Polyglot causes parse error → engine fingerprint confirmed from error**: record the error details. The error message itself may contain version info — redact internal paths from evidence.
- **Logic-less engine confirmed (Mustache/Handlebars) → limited SSTI**: document that the engine does not evaluate expressions. Variable name exposure is the primary risk. Record variable names, not values.
- **`__subclasses__` or sandbox-escape path requested → refuse**: code execution via SSTI requires separate destructive-workflow authorization. Document the vector and recommend sandbox configuration.
- **Template variable exposure includes secrets → stop immediately**: do not enumerate further variables. Document the exposed variable names and recommend data-model sanitization.

## Prohibited behavior

- Traversing to `__subclasses__`, `__globals__`, `__builtins__`, `__mro__`, or any Python object chain beyond the first class name introspection.
- Calling `system()`, `exec()`, `eval()`, `popen()`, `Runtime.exec()`, `ProcessBuilder`, `child_process.exec()`, or any code execution function.
- Reading files via `open()`, `File.read()`, `IO.read()`, `fs.readFileSync()`, or any file-access function in the template context.
- Making HTTP requests from template context (SSTI → SSRF).
- Using `import`, `require`, `include`, or module-loading directives within templates.
- Executing any `{% %}` statement tag in Jinja2/Twig beyond `print()` or simple assignment.
- Accessing Flask `config`, `request`, `session`, or `g` objects unless the existence of template injection is already confirmed and the object name is needed for engine fingerprinting (class name only).

## Stop conditions

- Mathematical canary fails across all tested syntaxes → stop, document SSTI not confirmed.
- Engine fingerprint confirms Velocity → stop, document critical finding (Velocity has no sandbox; any SSTI is critical by default).
- Error message reveals internal file paths → stop, redact from evidence, document the information disclosure.
- Template variable enumeration reveals `SECRET_KEY`, `DATABASE_URL`, or credential-like values → stop, do not read further variables, recommend immediate variable name obfuscation.

## Evidence

Record: affected parameter and template context, engine family and version (if confirmed via safe canary), safe canary expression used (e.g., `{{7*7}}`), evaluation result, introspection depth limit applied (e.g., "stopped at class name, did not traverse"), and redaction decisions for any error messages containing internal paths.

Never store: evaluated code output beyond the safe canary, object traversal results beyond class name, template variable values (especially config, secrets, credentials), file contents, or stack traces with filesystem paths.

## Report handoff

1. When an SSTI surface is confirmed, hand off to `vuln-ssti` for active validation with `pentest_agent_execute_tool`.
2. Reference this payload taxonomy in the finding as the detection rationale — link the safe canary used, the engine identified, and the expression evaluation depth observed.
3. If framework-specific behavior (Jinja2 sandbox, FreeMarker configuration, Velocity escape) was identified, include it in the handoff notes to guide the active validator.
4. Recommend: use logic-less templates or template engines that do not evaluate expressions, sandbox or disable dangerous functions in template engines, validate and sanitize user input before template rendering, and never pass user-controlled strings directly to `render()`, `evaluate()`, or `parse()`.
