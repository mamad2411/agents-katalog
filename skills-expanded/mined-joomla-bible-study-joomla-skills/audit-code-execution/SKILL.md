---
name: audit-code-execution
description: Audit Joomla extensions for attacker-influenced data reaching server-side code, command, or object execution sinks — shell commands, eval and dynamic include, unsafe deserialisation, PHAR, and attacker-selected callables or class names. Use when reviewing RCE exposure in a Joomla extension, or when explicitly invoked for a code execution audit. Browser-side script execution belongs to audit-xss.
---

# Audit Joomla server-side execution

Audit the distributed extension for attacker-influenced data reaching a server-side execution or
object-instantiation sink.

## Boundaries

This audit owns OS command injection, dynamic PHP execution and inclusion, unsafe deserialisation,
and attacker-selected callables, classes, templates, or service factories that can execute unintended
code.

- Browser-side JavaScript execution belongs to `audit-xss`.
- Path escape at ordinary filesystem operations belongs to `audit-file-operations` — the overlap is
  `include`/`require`, which is this audit's when the concern is *executing* attacker-chosen code and
  theirs when the concern is *reaching* a path outside the root.
- Outbound HTTP fetches belong to `audit-ssrf-redirects`.

## Sinks and controls

Trace request data, headers, cookies, database records, extension configuration, filenames, remote
responses, queue and job payloads, cache entries, and webhook bodies into:

- `exec`, `system`, `shell_exec`, `passthru`, `proc_open`, `popen`, backticks, or libraries that
  invoke external programs;
- `eval`, generated PHP, dynamic `include`/`require`, and template compilation or rendering that
  treats data as code;
- `unserialize` and equivalent object reconstruction, **including PHAR metadata reached through file
  operations** on affected runtimes and libraries;
- dynamic callables, event names, class names, service aliases, reflection, and DI container lookups
  where an attacker can select something outside a strict allow-list.

Do not assume shell escaping makes a command safe. Determine whether arguments can alter option
parsing, executable selection, environment, working directory, or shell syntax — `escapeshellarg()`
does not stop a value that becomes `--output=/var/www/shell.php`. Prefer direct library APIs or
argument-vector execution.

For structured data prefer JSON. Where legacy deserialisation is unavoidable, verify integrity and
authenticity before parsing and restrict allowed classes.

Recognise fixed maps and framework-controlled dispatch before reporting. Joomla's own `task=` routing
and MVC factory resolution are constrained by design; a component that builds a class name from
request input is not.

## Workflow

### Step 1 — Audit

Report findings ordered by severity:

- **CRITICAL** — reliable remote code or command execution reachable by a guest or low-privilege
  user.
- **HIGH** — exploitable execution requiring authentication, or unsafe deserialisation of data whose
  integrity an attacker can influence.
- **MEDIUM** — execution requiring elevated extension privileges, a strong gadget or environment
  prerequisite, or constrained command-argument injection.
- **LOW** — dangerous machinery currently fed only by trusted constants, but likely to become unsafe.

For each finding document the source-to-sink chain, the attacker's control over it, any required
environment or gadget, the impact, and the narrowest safe redesign — with file and line references.

Do not claim deserialisation RCE without establishing attacker control **and** a plausible gadget
path; label unverified gadget availability clearly rather than implying a working exploit.

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

*Adapted for this suite from the `audit-code-execution` workflow in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. The MIT permission notice accompanies this adaptation;
full text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
