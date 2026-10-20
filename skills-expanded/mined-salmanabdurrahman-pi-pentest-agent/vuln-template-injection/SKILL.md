---
name: vuln-template-injection
description: Client-side and mixed template injection validation — detect AngularJS expression injection, Vue.js template interpolation abuse, React JSX injection via dangerouslySetInnerHTML, and mixed client/server renderer bypasses; confirm expression evaluation with inert mathematical probes; never escalate to DOM-based XSS chains without separate destructive-risk approval.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Template injection — client-side and mixed renderer validation

Use this skill to validate client-side template injection and mixed client/server renderer injection on an authorized, in-scope target. Confirm that user-controlled input reaches a client-side template engine (AngularJS, Vue.js, React/JSX, Knockout, Ractive, Moustache/Handlebars in client mode) and is evaluated as template expressions. Detect injection with mathematical expression probes and inert Angular/Vue syntax. Never chain template injection to DOM-based XSS, credential capture, or cookie theft without separate destructive-risk approval.

## Required inputs

- Written scope naming the target, authorized injection parameters for template testing, and explicit permission for client-side template injection validation.
- Valid authorization cache. Caution risk class: client-side template injection can escalate to XSS if the template engine evaluates arbitrary JavaScript. Limit probes to mathematical expressions and safe engine identifiers.
- Known client-side framework from recon — AngularJS (`ng-app`, `{{ }}` interpolation), Vue.js (`v-bind`, `{{ }}` delimiters), React (JSX, `dangerouslySetInnerHTML`), Knockout (`data-bind`), Ractive (`{{ }}`), Ember (Handlebars). Inspect page source and JavaScript bundles for framework signatures.
- List of candidate injection points: form fields reflected in the DOM, URL parameters rendered in templates, search results displayed via client-side binding, user profile fields rendered by SPA frameworks, comment/message fields displayed without sanitization.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are used.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — framework detection

Before injecting, identify which template framework is in use and which delimiter syntax is active:

1. **AngularJS** (1.x): look for `ng-app`, `ng-controller`, `ng-bind`, `ng-model` attributes in the HTML. AngularJS uses `{{ }}` by default but can be configured to use `{[{ }]}`, `[[ ]]`, or other delimiters via `$interpolateProvider`.
2. **Vue.js**: look for `v-bind:`, `v-model:`, `v-if`, `v-for` attributes, or `{{ }}` in HTML templates. Vue 3 supports both `{{ }}` and `v-text`.
3. **React/JSX**: look for `react-root`, `data-reactroot`, `__REACT_DEVTOOLS_GLOBAL_HOOK__` in JS. React itself does not use template delimiters — injection occurs when `dangerouslySetInnerHTML` or `eval()` processes user input.
4. **Knockout.js**: look for `data-bind="text: ..."` attributes. Knockout uses `<!-- ko -->` comment bindings and `data-bind` attributes for rendering.
5. **Handlebars/Mustache (client-side)**: look for `<script type="text/x-handlebars-template">` or `Handlebars.compile()` calls in JS. Uses `{{ }}` triple-brace `{{{ }}}` for unescaped output.
6. **Ember.js**: uses Handlebars under the hood with `{{ }}` and `{{#each}}` block helpers.

Record the framework, version (if visible), and active delimiter syntax.

### Phase 2 — AngularJS expression injection

AngularJS (1.x) evaluates expressions inside `{{ }}` in the context of the Angular `$scope`. This is the most common client-side template injection:

**Detection probes**:
```text
{{7*7}}                     → 49 (expression evaluated)
{{constructor.constructor('alert(1)')()}}  → bypass (sandbox escape attempt)

Other AngularJS probes:
{{'a'.constructor.prototype.charAt=[].join;$eval('x=alert(1)')}}
{{$on.constructor('alert(1)')()}}
```

Procedure:
1. Inject `{{7*7}}` into a reflected parameter.
2. If `49` appears in the output → AngularJS expression injection confirmed.
3. If the raw `{{7*7}}` appears → the parameter is reflected but not evaluated by AngularJS. Try different delimiters or a different injection point.
4. AngularJS sandbox escape payloads are not permitted without destructive-risk approval. Document "AngularJS expression injection confirmed — sandbox escape and XSS escalation possible" and stop.

### Phase 3 — Vue.js template injection

Vue.js evaluates `{{ }}` expressions in the component's data context:

**Detection probes**:
```text
{{7*7}}                     → 49 (if within Vue template scope)
{{constructor.constructor('this.$root')()}}  → Vue root instance (advanced)
```

Vue template injection is less common than AngularJS because Vue templates are typically pre-compiled at build time. Injection only works when `v-html` or dynamic template compilation (`Vue.compile()`) processes user input:

1. Inject `{{7*7}}` into a parameter rendered via `v-html`.
2. If `49` appears → Vue template injection confirmed.
3. If the raw expression appears or is HTML-encoded (`&lbrace;&lbrace;7*7&rbrace;&rbrace;`) → properly escaped, not injectable.

### Phase 4 — React JSX injection

React does not use runtime template delimiters. Injection occurs through `dangerouslySetInnerHTML` or `eval()`:

**Detection**:
1. Identify React-rendered components in the DOM (`data-reactroot`, React DevTools).
2. Inject an HTML payload: `<img src=x onerror=console.log(1)>`.
3. If the payload renders as HTML (not text) and the `onerror` handler fires → the app is passing user input to `dangerouslySetInnerHTML` or similar unsafe rendering. This is a DOM-based XSS, not template injection, but the workflow is similar — report using vuln-dom-xss skill.
4. For React: report as unsafe rendering, not template injection.

### Phase 5 — mixed client/server renderer injection

Modern frameworks (Next.js, Nuxt, SvelteKit, Remix) may render templates on both server and client. The same parameter can be vulnerable in both contexts:

1. Server-side: test with SSTI probes (see vuln-ssti skill). If the server evaluates `{{7*7}}` → server-side template injection.
2. Client-side: after server rendering, the client-side framework may hydrate and re-evaluate the same expression. Test with the framework-specific probes above.
3. Record whether the injection occurs on the server (visible in raw HTML source), the client (visible only after JavaScript execution), or both.

### Phase 6 — Handlebars/Mustache client injection

Client-side Handlebars templates process user input when the app calls `Handlebars.compile(userInput)`:

**Detection**:
```text
{{7*7}}                     → 49 (if evaluated as Handlebars helper expression)
{{#with "s" as |string|}}   → Handlebars block helper test
  {{#with "e"}}              
  {{#with split as |conslist|}}
    {{this.pop}}
    {{this.push (lookup string.sub "constructor")}}
    {{this.pop}}
    {{#with string.split as |codelist|}}
      {{this.pop}}
      {{this.push "return require('child_process').execSync('id').toString()"}}
      {{this.pop}}
      {{#each conslist}}
        {{#with (string.sub.apply 0 codelist)}}
          {{this}}
        {{/with}}
      {{/each}}
    {{/with}}
  {{/with}}
{{/with}}
```

The Handlebars RCE chain is complex and requires destructive-risk approval. Do not test beyond `{{7*7}}` without approval. Document "Handlebars expression injection confirmed — RCE chain may be possible via prototype manipulation" and stop.

## Decision points

- **Stop at expression evaluation**: if `{{7*7}}` renders as `49` in any client-side template engine → template injection confirmed. File the finding.
- **Distinguish SSTI from client-side injection**: server-side (visible in HTML source) is higher severity (SSTI, RCE possible). Client-side (visible only in DOM after JS) is XSS-adjacent (lower severity, but still reportable).
- **React `dangerouslySetInnerHTML` is not template injection**: it is unsafe rendering/DOM-based XSS. Route to vuln-dom-xss skill.
- **Handlebars triple-brace `{{{ }}}`**: if the app uses triple-brace Handlebars, user input may be rendered as raw HTML without template injection. That is an XSS vector, not a template injection.

## Prohibited behavior

- Escalating client-side template injection to DOM-based XSS, cookie theft, keylogging, credential capture, or page defacement.
- Using AngularJS sandbox escape payloads to execute arbitrary JavaScript in the victim's browser.
- Using Handlebars prototype-manipulation chains to achieve RCE in Node.js server-side Handlebars.
- Modifying the DOM to phish credentials, redirect users, or load external scripts.
- Testing template injection in a way that stores payloads visible to other users (stored template injection → affects all users).

## Stop conditions

- `{{7*7}}` renders as `49` in the DOM → client-side template injection confirmed. Stop that parameter.
- Framework identified and expression evaluated → sufficient for finding. Stop.
- Raw expression reflected as text or HTML-encoded → properly escaped, not injectable. Document.
- Framework sandbox prevents dangerous expression evaluation → defense in place, but still document as a potential risk area.

## Evidence — client template injection matrix

For each tested parameter, record:

```text
Parameter: <name> | endpoint: <URL> | method: <GET | POST>
Framework: <AngularJS 1.x | Vue.js | Handlebars (client) | Knockout | mixed>
Expression evaluated (7*7=49): <yes | no | HTML-encoded>
Render context: <server-side (HTML source) | client-side (DOM only) | both>
XSS escalation possible: <yes | likely | no | not tested (no approval)>
Impact: <none | client template injection | SSTI + client injection (mixed)>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a parameter × framework matrix. Never store: AngularJS sandbox escape payloads, Handlebars RCE chains, `constructor.constructor` payloads, Vue.js root-instance manipulation code, or any payload that could be replayed for XSS exploitation.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected parameter, framework, CVSS estimate (5.5–7.0 for client-side template injection, 7.5–8.5 for mixed client/server injection with SSTI potential, 8.0–9.5 for AngularJS sandbox escape capability), and remediation guidance.
2. Reference the template injection matrix.
3. Recommend: use framework-provided sanitization (`ngSanitize` for AngularJS, `v-text` instead of `v-html` for Vue, avoid `dangerouslySetInnerHTML` in React), pre-compile templates at build time (never compile user input at runtime), migrate from AngularJS 1.x to Angular (2+) which does not use runtime expression evaluation, use a Content Security Policy that blocks inline script execution, and audit all `innerHTML`, `insertAdjacentHTML`, and `document.write()` calls.
